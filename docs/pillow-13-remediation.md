# Pillow 13 candidate (review only)

This owned-fork candidate changes only the exact Pillow dependency and adds
credential-free image compatibility tests. It is not an upstream release,
security-audit clearance, merge authorization, or deployment authorization.
Independent review and downstream Hermes/Linux integration remain required.

## Provenance and scope

- PyPI browser-harness metadata identifies https://github.com/browser-use/browser-harness.
- Latest PyPI release at inspection (2026-10-22): 0.1.13, pins Pillow 12.3.0.
- Upstream main `c6a941287424f32e2d20c7b7b892c8493f46808d` still pins 12.3.0.
- Candidate deliberately starts at release tag v0.1.13,
  `c24e5072ee66f8499bacd663f4f4bcb089bc4492`, rather than importing unrelated
  unreleased main changes. The fork PR targets a dedicated branch at this tag.
- PyPI sdist SHA-256:
  `284dc547a042c309feafd9a9f4a74b2a8651b7963ea3ac6cb2f2d64889f6a8f3`.
  All tracked Python source and pyproject bytes match the tag. The packaged
  `src/browser_harness/SKILL.md` is the dereferenced root SKILL.md symlink;
  its contents match that tag's root SKILL.md.
- This retains package version 0.1.13 intentionally: consume only with a
  full reviewed Git commit reference, never confuse this candidate with the
  identically versioned published PyPI artifact. No package publication.

## Quarantine

All resolver/build operations used fixed
`--exclude-newer 2026-10-19T14:59:56Z`, preserving the three-day policy as of
2026-10-22T14:59:56Z. Pillow 13.0.0 artifacts were uploaded
2026-10-16T22:15:24.672561Z through 2026-10-16T22:18:09.718711Z,
none yanked; all became eligible by 2026-10-19T22:18:09.718711Z.
No exclusions, dependency overrides, or age-policy bypasses were used.

## Executed verification

Isolated macOS CPython 3.14.7 virtualenv; pytest 8.4.2 and pytest-asyncio 1.2.0.

- Release-tag baseline: 251 unit tests passed with Pillow 12.3.0.
- Added tests before changing the pin: 1 expected pin-contract failure,
  4 image tests passed. Updated deprecated test-only getdata calls to
  get_flattened_data before final run.
- Candidate: 256 unit tests passed, no skips/failures/errors, Pillow 13.0.0.
- New coverage: source + installed metadata exact pin, RGB/RGBA/grayscale
  contact-sheet decoding/resampling/font rendering, scaled privacy-mask
  pixels and JPEG save/decode. Existing screenshot-size tests also passed.
- `uv pip check`: all 18 installed packages compatible.
- `uv build --wheel`: succeeds under the same cutoff; wheel METADATA has
  `pillow==13.0.0` and unchanged other dependency pins.
- `git diff --check`: passes.

Reproduce from the repository with an isolated environment:

```sh
uv venv ../venv
uv pip install --python ../venv/bin/python \
  --exclude-newer 2026-10-19T14:59:56Z -e . \
  pytest==8.4.2 pytest-asyncio==1.2.0
../venv/bin/python -m pytest tests/unit -q
uv pip check --python ../venv/bin/python
uv build --wheel --out-dir ../dist --exclude-newer 2026-10-19T14:59:56Z
```

No live browser, production environment, MCP optional extra, or Linux runtime
was exercised here. Raw PyPI metadata, sdist, resolver logs, inventory, wheel,
JUnit XML, and machine-readable provenance/test summary are retained in the
owning task's `harness-remediation/evidence/` directory (not committed).
