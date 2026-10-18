# Contributing to Refrain

Thanks for helping. This page covers how changes get in.

## Spec first

Behavior changes start in a spec with test vectors ([Constitution, Article I](.specify/memory/constitution.md)). Tests are written from the spec. Code is written to the tests.

Before you write code for new behavior, open an issue or a Discussion. We will agree on the spec change first.

A pull request that adds behavior without a spec gets the `needs-spec` label. It will not be merged until the spec exists.

See the [spec index](specs/README.md) for what exists and what is planned.

## Setup

You need Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/getrefrain/refrain.git
cd refrain
uv sync
```

## Checks

CI runs these on every pull request. Run them locally before you push:

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

CI also checks that:

- every `specs/*/*.json` file (the test vectors) is valid JSON;
- every `specs/*/tasks.md` has test tasks (tasks that touch `tests/`).

## Pull requests

- CI must pass.
- One approving review is required.
- Pull requests are squash-merged.

## Sign-off (DCO)

Sign off every commit under the [Developer Certificate of Origin](https://developercertificate.org):

```sh
git commit -s
```

This adds a `Signed-off-by` line with your name and email. There is no CLA.

## Code of Conduct

Everyone taking part follows the [Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Security

Do not report vulnerabilities in public issues. See [SECURITY.md](SECURITY.md).
