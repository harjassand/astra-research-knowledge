TRIANGLE-STRIP ELIMINATION CONTRIBUTION

Read PROOF.md for the all-size result and precise remaining gap.
Read COSTS_AND_SCOPE.md for all observed authoring checks and unknown costs.
The accepted Cycle4 triangle classification and period-nine lemma are explicit
dependencies, available unchanged in the owner's embedded predecessor ZIP.

Executable receiving interface:
  strip_extension.extend_strip(n, left_pair, right_pair)
  strip_extension.reduce_long_strips(vertices, edges)
  strip_extension.extend_reduced_coloring(reduced_colors, strip_orders)

The first function accepts any n>=30 and any ordered distinct endpoint colors
from0,1,2,3. The latter two reduce and extend a supplied reduced coloring; they
DO NOT solve the reduced graph's four-coloring problem and do not verify its
treewidth. The support's actual strips, saturation and degree cap are checked.

Fresh exact diagnostic, without changing frozen RESULT.json:
  python check_strip_extension.py --output /tmp/cycle5_strip_replay.json

The saved result includes all144 boundary words and the complete new99-vertex
two-strip-plus-square fixture, including its8-vertex reduction and colors.
It is independent of old prism or period-nine benchmark fixtures.

Global recovery must use the original support and full action block after
extension. Original action cells contain strip contributions; applying a
reduced-support decoder to them without accounting for those terms is invalid.
