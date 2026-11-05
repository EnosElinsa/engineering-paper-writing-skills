## What and why

<!-- The change and the reason for it. Link the issue it closes. -->

## Checks

- [ ] Shared rules edited only under `shared/`, then `python scripts/sync_shared.py`
- [ ] `python scripts/sync_shared.py --check`, `python scripts/validate_skills.py`, and `python -m unittest discover -s tests` pass
- [ ] Examples are synthetic, and no copyrighted or unpublished text was added
- [ ] Generic contracts stay domain-neutral, and field rules sit in a domain pack
- [ ] New gated rules have a failure case in `tests/gate-index.json` with a fixture
- [ ] `CHANGELOG.md` has an entry under `Unreleased`
