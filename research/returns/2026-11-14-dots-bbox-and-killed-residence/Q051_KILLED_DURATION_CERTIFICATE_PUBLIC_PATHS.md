# A precise sufficient certificate for the missing duration

Native rate-one-per-site heatbath, L1600, n2560000, a all-minus, B={plus count≥n/2}. Let D be the remaining configurations, w=exp(−E), and c_xy=w_x q_xy. Kill the chain on K={a}∪B. No companion components are removed.

Choose, for every x∈D, an actual single-flip path γ_x ending in K. Truncate it at its first K hit. For every undirected edge e define

ρ = max_e [1/c_e · sum_x w_x |γ_x| m_e(γ_x)],

where m_e(γ_x) is the number of occurrences of the undirected edge e along the path. For simple paths it is the membership indicator. The assembled phase bound counts occurrences: a phase is monotone and has at most one occurrence, and all phases are summed. Alternatively loop-erasing the paths only reduces the bound.

For any function f vanishing on K, path telescoping and Cauchy–Schwarz give sum_D w_x f_x² ≤ρ sum_edges c_e(f_u−f_v)². Hence the killed generator's smallest eigenvalue is at least1/ρ. This is the exact required congestion quantity; a bound on each individual path's energy rise does not bound it.

Let Z_D=sum_D w_x. Spectral contraction and Cauchy–Schwarz imply

P_x(τ_K>t) ≤ min(1, sqrt(Z_D/w_x) exp(−t/ρ)),
E_x τ_K ≤ρ[1+ 0.5 log(Z_D/w_x)].

These apply in the original physical time convention, because c uses native rates; there is no hidden factor n from discrete-time normalization.

A crude explicit finite bound is enough here. For x∈D, E_x≤16n, because there are at most2n disagreeing bonds. Also E_y≥−.02n for every y∈D, because plus count<n/2. There are at most2^n such states. Thus

log(Z_D/w_x) ≤ n(log2+16.02),
E_x τ_K ≤ (1+8.357n)ρ <2.2×10^7 ρ.

In particular, an independently established congestion bound ρ≤10^82 would imply a uniform M<2.2×10^89, enough for the box63 renewal error budget. This includes every actual departure state and every thermal companion automatically. The elementary estimate is intentionally loose.

## What remains unproved
No R200 path-family congestion bound of this size has been obtained. A proposed ≤15.96-energy-rise path of length O(n) is only the first ingredient. Bounding load by the number of all states loses a factor2^n, which destroys the budget. The required next step is an injection or weighted reconstruction bound for erased/filled components, or a different killed-generator Lyapunov/spectral proof. Generic low-temperature asymptotics with unspecified prefactors do not supply this finite bound. The exact critical side400 also prevents silently applying a nondegenerate-field theorem.

This document is a fully specified sufficient theorem interface, not a proof that its congestion premise holds.

## Why a deterministic clearing script is not a stochastic-time proof
Even if each state has a length≤3n path with energy rise≤15.96, forcing that particular sequence under native dynamics can cost a product of site-selection probabilities. A naive uniformization minorization loses roughly n^(3n), which is vastly worse than the available10^82 congestion budget. Replacing this by an assertion that the chain follows any low-rise route is unjustified. Likewise deleting thermal companions before running the path changes the actual state and does not establish a domination for the stopping set {a}∪B: more plus spins can delay hitting a while accelerating B. This union is not a monotone target, so ordinary attractiveness does not order its hitting time.

## Updated quantitative target after raw-face counting
The subsequently proved box164 counting reduction gives p_exit<10^-450, λ_a<10^-7, and core numerator excess<1.087×10^-7. Thusρ≤10^446 would imply M<2.2×10^453 and outside correction<2.2×10^-4. This supersedes the earlier box63 target10^82. The path-load inequality and proof above are unchanged, and the congestion premise remains unproved.
