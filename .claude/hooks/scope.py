#!/usr/bin/env python3
"""PreToolUse hook: keep a subagent inside its directories.

Usage (from agent frontmatter):
    scope.py <write-paths> [<read-paths>]
Comma-separated repo-relative paths (dirs, files or fnmatch globs). "." means the whole repo;
a leading "!" excludes a path and wins over any allow; a leading "~" allows
only Edits that tick Markdown checkboxes ("- [ ]" -> "- [x]"). Read paths limit
Read/Grep/Glob; omit to allow reading everything. A search whose root contains
an excluded path is blocked, since its results could include that path.

Bash commands are parsed for the files they write (redirects, rm/mv/cp/tee/sed -i,
git and uv commands that touch the tree, ...) and, when read paths are set, every
existing path they name. Writes to temp dirs and /dev are allowed. A command that
cannot be parsed is blocked.

ponytail: Bash parsing is a guardrail, not a sandbox. Code run by an interpreter
(python -c, node -e, a script file) and paths built at runtime are not seen. Use
OS-level sandboxing per agent if that ever matters.
"""

import fnmatch
import glob
import itertools
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

WRITE_TOOLS = {"Edit", "Write", "NotebookEdit"}
READ_TOOLS = {"Read", "Grep", "Glob"}

OPS = set("();<>|&")
WRITE_REDIRECTS = {">", ">>", ">|", "&>", "&>>", "<>", ">&"}
HEREDOC = re.compile(
    r"<<-?[ \t]*(['\"]?)(\w+)\1([^\n]*)\n.*?^[ \t]*\2[ \t]*$", re.DOTALL | re.MULTILINE
)
WRAPPERS = {"sudo", "env", "command", "time", "nohup", "exec", "nice"}
UV_VALUE_OPTS = {"--with", "--python", "-p", "--extra", "--group", "--package", "--from"}
UV_VALUE_OPTS |= {"--directory", "--project", "--env-file", "--with-requirements", "--index"}
ALL_ARGS = {"rm", "rmdir", "touch", "mkdir", "truncate", "unlink", "shred", "tee", "mv"}
LAST_ARG = {"cp", "ln", "install", "rsync"}
GIT_TREE = {"reset", "clean", "stash", "merge", "rebase", "pull", "cherry-pick", "revert"}
GIT_TREE |= {"am", "apply", "checkout-index", "read-tree"}
GIT_READS = {"show", "diff", "grep", "blame", "cat-file", "archive", "format-patch"}
SAFE_DIRS = ("/dev", "/tmp", "/private/tmp", "/private/var/folders", tempfile.gettempdir())


def repo_root(cwd):
    out = subprocess.run(
        ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    return out.stdout.strip() or cwd


def under(rel, a):
    if rel == ".." or rel.startswith(".." + os.sep):
        return False
    return a == "." or rel == a or rel.startswith(a + os.sep) or fnmatch.fnmatchcase(rel, a)


def only_ticks(old, new):
    """True if new differs from old only by ticking "- [ ]" checkboxes."""
    if len(old) != len(new) or old == new:
        return False
    for i, (a, b) in enumerate(zip(old, new)):
        if a == b:
            continue
        line = old[:i].rsplit("\n", 1)[-1]
        if not (
            a == " " and b in "xX" and re.fullmatch(r"\s*- \[", line) and old[i + 1 : i + 2] == "]"
        ):
            return False
    return True


def permitted(path, entries, root, cwd, search):
    rel = os.path.relpath(os.path.realpath(os.path.join(cwd, path)), os.path.realpath(root))
    allow = [e for e in entries if not e.startswith("!")]
    for d in (e[1:] for e in entries if e.startswith("!")):
        if under(rel, d) or (search and under(d, rel)):
            return False
    return any(under(rel, a) for a in allow)


def strip_wrappers(words):
    while words:
        w = words[0]
        if w in WRAPPERS or re.fullmatch(r"[A-Za-z_]\w*=.*", w):
            words = words[1:]
        elif w == "uvx" or (w == "uv" and words[1:2] == ["run"]):
            words = words[1 if w == "uvx" else 2 :]
            while words and words[0].startswith("-"):
                words = words[2 if words[0] in UV_VALUE_OPTS else 1 :]
        else:
            break
    return words


def written(words, cwd):
    """Paths a simple command writes; "." when it may touch the whole tree."""
    if not words:
        return []
    name, args = os.path.basename(words[0]), words[1:]
    paths = [a for a in args if not a.startswith("-")]
    if name in ALL_ARGS:
        return paths
    if name in ("chmod", "chown", "chgrp"):
        return paths[1:]
    if name in LAST_ARG:
        return paths[-1:]
    if name in ("sed", "perl") and any(
        re.fullmatch(r"-[a-zA-Z]*i.*|--in-place.*", a) for a in args
    ):
        # The script is an argument too; only existing files can be edited in place.
        return [a for a in paths if a and os.path.exists(os.path.join(cwd, a))]
    if name == "dd":
        return [a[3:] for a in args if a.startswith("of=")]
    if name in ("curl", "wget"):
        flags = ("-o", "--output") if name == "curl" else ("-O", "--output-document")
        return [b for a, b in itertools.pairwise(args) if a in flags]
    if name == "patch":
        return ["."]
    if name == "xargs":
        return ["."] if set(args) & (ALL_ARGS | LAST_ARG | {"sed", "perl", "git"}) else []
    if name == "find" and set(args) & {"-delete", "-exec", "-execdir", "-ok"}:
        start = args[: next((i for i, a in enumerate(args) if a[:1] in ("-", "(", "!")), None)]
        return start or ["."]
    if name == "ruff" and (
        (args[:1] == ["format"] and not set(args) & {"--check", "--diff"})
        or (args[:1] == ["check"] and set(args) & {"--fix", "--unsafe-fixes"})
    ):
        return paths[1:] or ["."]
    if name == "uv" and args[:1] in (["add"], ["remove"], ["lock"]):
        return ["pyproject.toml", "uv.lock"]
    if name == "uv" and args[:1] == ["sync"] and not set(args) & {"--locked", "--frozen"}:
        return ["uv.lock"]
    if name == "git":
        while args and args[0].startswith("-"):
            args = args[2 if args[0] in ("-C", "-c") else 1 :]
        sub, rest = (args[0], args[1:]) if args else ("", [])
        if sub in ("rm", "mv", "restore"):
            return [a for a in rest if not a.startswith("-")]
        if sub == "checkout":
            if "--" in rest:
                return rest[rest.index("--") + 1 :]
            return [] if set(rest) & {"-b", "-B"} else ["."]
        if sub == "switch":
            return [] if set(rest) & {"-c", "-C", "--create"} else ["."]
        if sub in GIT_TREE:
            return ["."]
    return []


def git_read(words):
    """Pathspecs a git command shows file contents for; "." when unrestricted."""
    if not words or words[0] != "git":
        return []
    args = words[1:]
    while args and args[0].startswith("-"):
        args = args[2 if args[0] in ("-C", "-c") else 1 :]
    sub, rest = (args[0], args[1:]) if args else ("", [])
    patch = sub == "log" and any(a in ("-p", "--patch") or a.startswith("-L") for a in rest)
    if sub not in GIT_READS and not patch:
        return []
    if "--" in rest and not any(":" in a for a in rest):
        return rest[rest.index("--") + 1 :]
    return ["."]


def bash_paths(command, cwd):
    """(written, named) absolute paths of a Bash command. Raises ValueError if unparseable."""
    command = HEREDOC.sub(lambda m: m.group(3), command)  # heredoc bodies are data
    command = command.replace("\\\n", " ").replace("\n", " ; ")
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split, lex.commenters = True, ""
    cmds, pending = [([], [], [])], None  # (words, redirect writes, redirect reads)
    for t in lex:
        is_op = bool(t) and set(t) <= OPS
        if pending and not is_op:
            if not (pending == ">&" and re.fullmatch(r"\d+-?|-", t)):
                cmds[-1][1 if pending in WRITE_REDIRECTS else 2].append(t)
            pending = None
        elif is_op and ("<" in t or ">" in t):
            if cmds[-1][0] and cmds[-1][0][-1].isdigit():
                cmds[-1][0].pop()  # fd number, as in 2>/dev/null
            pending = t
        elif is_op:
            cmds.append(([], [], []))
        else:
            cmds[-1][0].append(t)

    def resolve(p):
        p = os.path.join(cwd, os.path.expanduser(os.path.expandvars(p)))
        return [os.path.realpath(x) for x in glob.glob(p)] + [os.path.realpath(p)]

    writes, reads = [], []
    for words, redirect_writes, redirect_reads in cmds:
        words = [os.path.expanduser(os.path.expandvars(w)) for w in words]
        core = strip_wrappers(words)
        for p in words + redirect_reads:
            reads += [x for x in resolve(p) if os.path.exists(x)]
        for p in git_read(core):
            reads += resolve(p)
        if core and core[0] in ("cd", "pushd"):
            cwd = resolve(core[1] if len(core) > 1 else "~")[-1]
        elif core and os.path.basename(core[0]) in ("bash", "sh", "zsh") and "-c" in core[:-1]:
            w, r = bash_paths(core[core.index("-c") + 1], cwd)
            writes, reads = writes + w, reads + r
        elif core and core[0] == "eval":
            w, r = bash_paths(" ".join(core[1:]), cwd)
            writes, reads = writes + w, reads + r
        for p in redirect_writes + written(core, cwd):
            writes += resolve(p)
    return writes, reads


def check_bash(command, write, read, root, cwd, agent):
    try:
        writes, reads = bash_paths(command, cwd)
    except ValueError as e:
        print(f"{agent}: cannot parse Bash command ({e}); split it up", file=sys.stderr)
        return 2
    safe = [os.path.realpath(d) for d in SAFE_DIRS]
    allow = [e for e in write if not e.startswith("~")]
    for p in writes:
        outside = os.path.relpath(p, os.path.realpath(root)).startswith("..")
        if permitted(p, allow, root, cwd, False):
            continue
        if outside and any(p == d or p.startswith(d + os.sep) for d in safe):
            continue
        print(
            f"{agent} may only write {', '.join(write) or 'nothing'}; Bash command writes {p}",
            file=sys.stderr,
        )
        return 2
    for p in reads if read is not None else []:
        if not permitted(p, read, root, cwd, True):
            print(
                f"{agent} may only read {', '.join(read)}; Bash command reads {p}", file=sys.stderr
            )
            return 2
    return 0


def main():
    write = [a.rstrip("/") for a in sys.argv[1].split(",") if a]
    read = [a.rstrip("/") for a in sys.argv[2].split(",") if a] if len(sys.argv) > 2 else None
    event = json.load(sys.stdin)
    tool, args = event.get("tool_name"), event.get("tool_input", {})
    cwd = event.get("cwd") or os.getcwd()
    root = repo_root(cwd)

    if tool == "Bash":
        agent = event.get("agent_type", "this agent")
        return check_bash(args.get("command", ""), write, read, root, cwd, agent)
    if tool in WRITE_TOOLS:
        allowed, path = write, args.get("file_path") or args.get("notebook_path")
    elif tool in READ_TOOLS and read is not None:
        # A search with no path starts at cwd.
        allowed, path = read, args.get("file_path") or args.get("path") or cwd
    else:
        return 0

    search = tool in ("Grep", "Glob")
    tick = [e[1:] for e in allowed if e.startswith("~")]
    allowed = [e for e in allowed if not e.startswith("~")]
    if path and permitted(path, allowed, root, cwd, search):
        return 0
    if path and tick and permitted(path, tick, root, cwd, search):
        if tool == "Edit" and only_ticks(args.get("old_string", ""), args.get("new_string", "")):
            return 0
        print(
            f"{event.get('agent_type', 'this agent')} may only tick checkboxes in {path}: "
            'use Edit with old_string containing the whole "- [ ] ..." line and change only [ ] to [X]',
            file=sys.stderr,
        )
        return 2
    agent = event.get("agent_type", "this agent")
    print(
        f"{agent} may only {'write' if tool in WRITE_TOOLS else 'read'} "
        f"{', '.join(allowed)}; blocked {tool} on {path or '<whole repo>'}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
