# Independent receiving-check costs

Both new receiving records passed in one execution. No producer imports,
old scientific replay, discovery search, floating solver or paid computation
was used.

| Scope | Wall seconds | CPU seconds |
|---|---:|---:|
| A5 three-action record | 0.004462732991669327 | 0.004465086 |
| Mixed 16-vertex four-action record | 0.011363262994564138 | 0.011365306999999998 |
| **Whole two-record gate** | **0.01593741100805346** | **0.015934076999999998** |

Peak process RSS: **12,320,768 bytes**.

The total includes both record reads, SHA256 and exact size authentication,
independent original-support expansion/binding, actual multiplicities and
star/triangle checks, full original matrix actions and noise, analytic
star-block least squares, projection normal equations, rational error norms,
and independent LDL recurrence plus full factor reconstruction of both PSD
matrices. It excludes process startup and final receipt serialization.
The individual rows are contained in the total, not additional charges.

Reading, inference, authoring, review and integration were not individually
metered and remain unknown. This short gate does not replace the producer's
construction, unsuccessful attempts, independent finite-certificate gate or
discovery costs.
