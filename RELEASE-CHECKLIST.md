# v2.0 release review checklist

Scope: Nikon Z fc C 1.81. v2.0 remains a candidate on the public review branch.

- [x] The local candidate's measured size and SHA-256 match the version declaration and saved offline report.
- [x] Separate menu settings, measured recording duration, and untested cases in the release summary.
- [ ] Record the tested image hash, camera firmware, operator, individual results, and whether each observation belongs to the final image or its parent. Keep the original build report as generated.
- [x] Classify the 27 warnings in the saved offline report. All 27 are the same category: two bytes of zero padding, at 27 distinct entries. The saved result records zero violations. This is a classification of the existing report and carries no additional runtime result.
- [ ] Record whether stock rollback was observed and under what conditions. Document recovery limitations separately.
- [ ] Resolve embedded-byte provenance before any formal release. The reviewed candidate tree contains no standalone firmware image. The patch specification contains embedded bytes, and the tree has a top-level MIT notice and project credits. The reviewed evidence does not trace the embedded bytes to their sources or establish redistribution permission for them. Retain the candidate status while that evidence is missing.
- [ ] Record the maintainer's decision after the evidence review.

A completed identity check establishes the identity of the local file. It does not establish hardware behavior or recovery.
