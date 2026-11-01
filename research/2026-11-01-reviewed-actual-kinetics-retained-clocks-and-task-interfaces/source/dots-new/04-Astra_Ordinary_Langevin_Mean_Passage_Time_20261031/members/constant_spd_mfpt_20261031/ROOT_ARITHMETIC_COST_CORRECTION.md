# Preserved independent review finding: root count is not root bit complexity

The original costs file overstates dimension independence of the two root costs.
Only the number of root calls is fixed. Nonsquare operands include a shift by
2P, with P=max(192,alpha*(bits(kappa)+2)+128), and thus can grow with dimension.
At kappa=3/7, the same q=2/3 root has guarded operand bound386 bits at m16 and
1538 bits at m512. The original tracked root proxy was accurate; its prose
interpretation was not. Corrected costs now distinguish these explicitly.

Every v1 file and its FROZEN_SHA256.json remain byte-for-byte unchanged. The v2
manifest adds corrected costs/navigation and this history; source code, theorem,
all exact endpoints, author tests and saved results are unchanged. No numerical
regeneration or new claimed execution is needed for this documentation repair.
The earlier v1 cost statement is historical, not the accepted current claim.
