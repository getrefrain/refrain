#!/usr/bin/env python3
"""PreToolUse hook: keep a subagent inside its directories.

Usage (from agent frontmatter):
    scope.py <write-paths> [<read-paths>]
Comma-separated repo-relative paths (dirs or files). Read paths limit
Read/Grep/Glob; omit to allow reading everything.

ponytail: does not police Bash; an agent can still write via the shell.
Add a Bash check if agents start doing that.
"""

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


def inside(path, allowed, root, cwd):
    rel = os.path.relpath(os.path.realpath(os.path.join(cwd, path)), os.path.realpath(root))
    return any(rel == a or rel.startswith(a + os.sep) for a in allowed)


def main():
    write = [a.strip("/") for a in sys.argv[1].split(",") if a]
    read = [a.strip("/") for a in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
    event = json.load(sys.stdin)
    tool, args = event.get("tool_name"), event.get("tool_input", {})
    cwd = event.get("cwd") or os.getcwd()
    root = repo_root(cwd)

    if tool in WRITE_TOOLS:
        allowed, path = write, args.get("file_path") or args.get("notebook_path")
    elif tool in READ_TOOLS and read is not None:
        allowed, path = read, args.get("file_path") or args.get("path")
    else:
        return 0

    # A search with no path covers the whole repo, so it is outside a read scope.
    if path and inside(path, allowed, root, cwd):
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
