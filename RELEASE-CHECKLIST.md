# Release checklist

Run through this before tagging. Mirrors `publish/PUBLISH-GUIDE.md`.

- [ ] `README.md` states model, firmware version, verified features and risk
- [ ] `LICENSE` present (MIT)
- [ ] `.gitignore` blocks `*.bin` / `*.BIN` / `build/` / `__pycache__`
- [ ] `python tools/verify_release.py --firmware <official C 1.81>` -> all MATCH
- [ ] no firmware, no build output, no absolute paths, no personal data;
      `Get-ChildItem -Recurse -File -Include *.bin,*.BIN` must be empty
- [ ] `CHANGELOG.md` has an entry for this version
- [ ] tag pushed, release notes list the SHA-256 of every artifact
- [ ] release assets contain **no** firmware image
