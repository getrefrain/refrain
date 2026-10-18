"""Run: uv run pytest .claude/hooks"""

import json
import pathlib
import subprocess
import sys

import pytest

HOOK = pathlib.Path(__file__).with_name("scope.py")
ROOT = HOOK.parents[2]
IMP = ["src,pyproject.toml,uv.lock,~specs/*/tasks.md"]
TA = ["tests,~specs/*/tasks.md", "specs,tests,pyproject.toml"]
SW = ["specs,.specify/feature.json,!specs/000-prd.md,!specs/README.md"]
RO = [""]


def run(scope, tool, **tool_input):
    event = {"tool_name": tool, "tool_input": tool_input, "cwd": str(ROOT)}
    cmd = [sys.executable, str(HOOK), *scope]
    return subprocess.run(
        cmd, check=False, input=json.dumps(event), capture_output=True, text=True
    ).returncode


ALLOW = [
    (IMP, "uv run pytest -q"),
    (IMP, "uv run ruff format src && uv run ruff check --fix src"),
    (IMP, "uv add sqlglot==30.23.0"),
    (IMP, "cat > src/refrain/key.py <<'EOF'\nprint(\"don't > tests/x\")\nEOF"),
    (IMP, "echo hi > /tmp/x 2>&1; ls src 2>/dev/null"),
    (SW, "mkdir -p specs/002-outcome && touch specs/002-outcome/spec.md"),
    (SW, "uv run --with sqlglot python -I - <<'EOF'\nimport sqlglot\nEOF"),
    (SW, ".specify/scripts/bash/create-new-feature.sh --json --number 2 'Outcome contract'"),
    (SW, "git checkout -b 002-outcome"),
    (TA, "uv run pytest tests -q"),
    (TA, "git diff -- tests"),
    (RO, "uv run pytest && git status && git log --oneline -5"),
]

BLOCK = [
    (IMP, "echo x > tests/test_a.py"),
    (IMP, "sed -i '' 's/a/b/' CLAUDE.md"),
    (IMP, "cd tests && rm -f test_a.py"),
    (IMP, "bash -c 'rm -rf specs'"),
    (IMP, "echo '- [X] T1' >> specs/002-x/tasks.md"),
    (IMP, "uv run ruff format"),
    (IMP, "git checkout ."),
    (IMP, "git stash"),
    (IMP, "find . -name '*.pyc' -delete"),
    (IMP, "cp src/refrain/__init__.py tests/"),
    (IMP, "echo x > ~/x"),
    (IMP, "echo 'unterminated"),
    (SW, "rm specs/*"),
    (SW, "echo x > .specify/memory/constitution.md"),
    (TA, "cat src/refrain/__init__.py"),
    (TA, "cd src && ls"),
    (TA, "grep -r key ."),
    (TA, "git show HEAD:src/refrain/__init__.py"),
    (RO, "touch x"),
]


@pytest.mark.parametrize(("scope", "command"), ALLOW)
def test_bash_allowed(scope, command):
    assert run(scope, "Bash", command=command) == 0


@pytest.mark.parametrize(("scope", "command"), BLOCK)
def test_bash_blocked(scope, command):
    assert run(scope, "Bash", command=command) == 2


def test_file_tools():
    tasks = "specs/002-x/tasks.md"
    assert run(IMP, "Edit", file_path="src/a.py", old_string="a", new_string="b") == 0
    assert run(IMP, "Write", file_path="tests/a.py", content="") == 2
    assert run(IMP, "Edit", file_path=tasks, old_string="- [ ] T1", new_string="- [X] T1") == 0
    assert run(IMP, "Edit", file_path=tasks, old_string="- [ ] T1", new_string="- [X] T2") == 2
    assert run(IMP, "Write", file_path=tasks, content="- [X] T1") == 2
    assert run(TA, "Read", file_path="src/refrain/__init__.py") == 2
    assert run(SW, "Write", file_path=".specify/memory/constitution.md", content="") == 2
