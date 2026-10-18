#!/usr/bin/env python3
"""PreToolUse hook: keep a subagent inside its directories.

Usage (from agent frontmatter):
    scope.py <write-paths> [<read-paths>]
Comma-separated repo-relative paths (dirs, files or fnmatch globs). "." means the whole repo;
a leading "!" excludes a path and wins over any allow. Read paths limit
Read/Grep/Glob; omit to allow reading everything. A search whose root contains
an excluded path is blocked, since its results could include that path.

ponytail: does not police Bash; an agent can still write via the shell.
Add a Bash check if agents start doing that.
"""

import fnmatch
import json
import os
import subprocess
import sys

WRITE_TOOLS = {"Edit", "Write", "NotebookEdit"}
READ_TOOLS = {"Read", "Grep", "Glob"}


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


def permitted(path, entries, root, cwd, search):
    rel = os.path.relpath(os.path.realpath(os.path.join(cwd, path)), os.path.realpath(root))
    allow = [e for e in entries if not e.startswith("!")]
    for d in (e[1:] for e in entries if e.startswith("!")):
        if under(rel, d) or (search and under(d, rel)):
            return False
    return any(under(rel, a) for a in allow)


def main():
    write = [a.rstrip("/") for a in sys.argv[1].split(",") if a]
    read = [a.rstrip("/") for a in sys.argv[2].split(",") if a] if len(sys.argv) > 2 else None
    event = json.load(sys.stdin)
    tool, args = event.get("tool_name"), event.get("tool_input", {})
    cwd = event.get("cwd") or os.getcwd()
    root = repo_root(cwd)

    if tool in WRITE_TOOLS:
        allowed, path = write, args.get("file_path") or args.get("notebook_path")
    elif tool in READ_TOOLS and read is not None:
        # A search with no path starts at cwd.
        allowed, path = read, args.get("file_path") or args.get("path") or cwd
    else:
        return 0

    search = tool in ("Grep", "Glob")
    if path and permitted(path, allowed, root, cwd, search):
        return 0
    agent = event.get("agent_type", "this agent")
    print(
        f"{agent} may only {'write' if tool in WRITE_TOOLS else 'read'} "
        f"{', '.join(allowed)}; blocked {tool} on {path or '<whole repo>'}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
