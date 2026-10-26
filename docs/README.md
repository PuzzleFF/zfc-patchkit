# Documentation index

| File | What it covers |
|---|---|
| `MILESTONE-2026-10-25.md` | The whole result in one place: deliverables, measured evidence, what was learned, what is ruled out |
| `MODE-TABLE-MAP.md` | The 30-record video mode table: field layout, the index mapper, the quality mask, slow-motion grouping |
| `ZEBRA-GATE-FINDINGS.md` | How the photo-mode zebra patch was found and verified; the three veto points inside the gate |
| `BITRATE-VERIFIED.md` | Every measured bitrate, before and after, with the comparisons that validate the mode mapping |
| `TIER2-SPACE-FINDINGS.md` | Where code can be parked in this module; the ARM/Thumb calling trap; why video rotation metadata was parked |

## A note on paths in these reports

They were written inside the author lab repository, so you will see references
such as `build/sd/<label>/EG198581.BIN` for artifacts that are **not**
distributed here (a patched image is camera firmware, which this repository
does not ship).

Read them as "this is what was built and measured". To reproduce anything, run
`tools/verify_release.py`: it rebuilds every image from the specs and the
official firmware and prints the SHA-256 of each result.
