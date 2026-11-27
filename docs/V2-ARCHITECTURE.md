# Z fc v2.0 feature scope and evidence

The v2.0 candidate targets Nikon Z fc firmware C 1.81. The public name is `zfc-v2`. The research reports use the name `zfc_all1b`. The recorded candidate size and SHA-256 are listed in the [README](../README.md).

| Area | Reported behavior | Review boundary |
|---|---|---|
| Ordinary and slow-motion recording | Longer menu settings | Recorded clips reached 34:32 and 10 minutes respectively. Full-duration and long 4K tests remain open. |
| Movie quality | Selectable quality and bitrate settings | Reports cover five MP4 modes. MOV was not tested. |
| Setup and zebra | Unified menu and independent photo zebra setting | Source-reported observations need per-case links to the final image. |
| Custom shutter sound | Selectable sound slots and preview | Source-reported observations are limited to the test setup. |
| Aspect ratios | LCD and EVF masks, playback zoom and mode transitions | Results for the final image and its parent should be recorded separately. |
| Configuration | Settings restored at cold boot | The reviewed reports do not establish behavior across all display and card states. |

The owner reports an initial camera test without observed issues. The saved offline checks and local SHA-256 check are separate evidence. For remaining release questions, see the [review checklist](../RELEASE-CHECKLIST.md).
