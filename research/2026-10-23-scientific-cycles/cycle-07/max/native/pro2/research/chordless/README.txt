CHORDLESS BOUNDARY CONTRIBUTION — CYCLE6

Read PROOF.md and COSTS_AND_SCOPE.md.

Actual operations:
  theta_boundary.extend_theta(lengths, terminal_colors)
  theta_boundary.free_three_color_theta(lengths)
  theta_boundary.cap_induction_witness(K)
  separator_profile.profile(vertices, edges, colors)
  separator_profile.join(left_profile, right_profile)

Theta lengths count edges; there are2..4 internally disjoint paths, all of
length>=2, with terminals0 and1. The prescribed-color extension rejects the
exact equal-terminal/four-short-branches obstruction. No hidden boundary
recoloring occurs. The ordinary three-color comparator CHOOSES terminals0,1;
it does not satisfy arbitrary equal prescribed terminal colors.

Fresh receiving checks without altering frozen saved output:
  python check_theta_boundary.py --output /tmp/cycle6_theta_replay.json
  python check_separator_profile.py --input /tmp/cycle6_theta_replay.json --output /tmp/cycle6_join_replay.json

RESULT.json contains actual selected graphs/colors, all boundary-case outcomes,
short-branch exhaustive counts, the free comparator and complete cap witnesses.
JOIN_RESULT.json contains the actual receiving profile/mass calculation.

The profile calculus is exact through parallel-join depth but DOES NOT prove
uniform masses. Its graph interface requires matching colors and intersection
exactly the two nonadjacent terminal vertices. No completed all-atom coloring,
new full-class query count, application speedup or external acceptance is claimed.

No old Cycle5 period/strip/prism fixture was replayed. Its source is unchanged.
