# Perth Solar Grid

A geospatial decision-support tool for the Perth metro area (South West Interconnected System). It builds two layers in one Python pipeline:

1. **Battery opportunity map**: ranks suburbs by rooftop solar, battery uptake and likely network constraint.
2. **Rooftop solar detection**: uses aerial or satellite imagery to check and fill gaps in registered solar data.

## Status

Stage 0: feasibility and data audit. No pipeline code yet. See [docs/SCOPE.md](docs/SCOPE.md) for the staged plan.

## Docs

- [Scope](docs/SCOPE.md): stages and risks
- [Decisions](docs/DECISIONS.md): what was decided and why
- [Data sources](docs/DATA_SOURCES.md): every source, with licence and known limits
- [Gotchas](docs/GOTCHAS.md): things that cost time

## Licence

Code is MIT licensed (see [LICENSE](LICENSE)). Third-party data keeps its own licence, listed in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md). No raw data is committed to this repo.
