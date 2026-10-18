# Refrain

Snapshot-keyed data gateway for AI agents: the data plane between agents and the warehouse.

Homepage: https://getrefrain.ai

## Status

Pre-alpha, under active spec development. There is nothing to install yet.

## How it is built

Refrain is built spec-first. Every behavior starts in a spec, then tests, then code:

1. `specs/` holds one spec per feature, with test vectors. See the [spec index](specs/README.md).
2. `tests/` holds tests written from the specs.
3. `src/` holds the code that makes the tests pass.

The [constitution](.specify/memory/constitution.md) sets the rules every spec, test and line of code must follow.

## Development

You need Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run ruff check .
uv run pytest
```

Until the first spec's tests land, `pytest` reports "no tests ran" and exits with code 5. That is expected.

## Community

- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Code of Conduct](.github/CODE_OF_CONDUCT.md)

## License

[MIT](LICENSE)
