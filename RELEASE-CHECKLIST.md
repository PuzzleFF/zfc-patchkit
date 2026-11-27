# v2.0 release review checklist

Scope: Nikon Z fc C 1.81. v2.0 remains a candidate on the public review branch.

- [x] The local candidate's measured size and SHA-256 match the version declaration and saved offline report.
- [x] Separate menu settings, measured recording duration, and untested cases in the release summary.
- [ ] Record the tested image hash, camera firmware, operator, individual results, and whether each observation belongs to the final image or its parent. Keep the original build report as generated.
- [ ] Triage the 27 warnings in the saved offline report and record their dispositions.
- [ ] Record whether stock rollback was observed and under what conditions. Document recovery limitations separately.
- [ ] Review the provenance of embedded bytes and third-party material. Check the proposed public files and assets for private data and material whose redistribution has not been cleared.
- [ ] Record the maintainer's decision after the evidence review.

A completed identity check establishes the identity of the local file. It does not establish hardware behavior or recovery.
