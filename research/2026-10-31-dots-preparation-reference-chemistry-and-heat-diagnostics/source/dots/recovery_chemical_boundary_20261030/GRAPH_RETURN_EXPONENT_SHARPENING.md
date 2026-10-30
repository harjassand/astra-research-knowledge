# Sharpening the graph-acquired return exponent

30 October 2026. Unreviewed extension of GRAPH_ACQUIRED_DORMANT_RETURN_BOUND.md, with its exact structural assumptions. No reviewed source is edited. This is a probability kernel, not a weighted occupation kernel or a recurrence theorem.

Let L>=1 be maximum shortest conversion distance to A. Then the preceding actual-stage construction improves to

    P_x(tau_{D=0}<tau_clear) <= C n^{-1/(2L+1)}.

All constants depend on the fixed graph and rates. Two accounting refinements remove the need for widely separated cutoffs.

## Equal cutoffs and exact stopping

Take K=floor(n^{1/(2L+1)}), J=K, enlarging a finite small-n constant as necessary. It suffices to start at D=1, since every negative D jump is -1. Stop and charge the entire upper-exit event D>=J as failure. It requires at least (J-1)/2 nonlinear seed marks from D=1, so has probability at most C exp(-cJ): seeds are marked against clearing on their common (A)_2 clock. Conversion leaves D fixed and all other D changes are negative.

Low stages run below A=K and D=J, with the actual seed/horizon restarts described in the preceding file. In the common D-clock their total expected duration per low stage is at most

    C t_*,   t_*=C(K/n)^{1/L}.

Indeed, at every seed restart at least n-J type particles remain; their prescribed-path occupancy bound is valid without conditioning on survival, by pathwise domination up to the next seed. Horizon-only restart probability is exp(-cK). The number of seed interruptions before clearing has bounded geometric mean. On D=1 the sole dormant-entering birth has D-clock rate at most C K. Therefore a low-stage dormant entry costs at most C K t_*.

A high stage starts at A>=K, D<J and stops at clearing, A<K/2, D=0, or D>=J. The clearing compensator gives

    E integral_0^sigma (A_t)_2 dt <= 1/k0.

Throughout this high stage, A>=K/2. The total intensity of A-consuming conversion jumps is at most C A D, and hence their expected number is at most C J/K. Each such jump loses exactly one A. The only other A losses are nonlinear seed jumps, each of size at most two. To reach A<K/2 from A>=K, either there have been at least K/4 A-consuming conversions or at least K/8 seed marks (round constants harmless). Consequently

    P(high-to-low) <= C J/K^2 + C exp(-cK).

This is the crucial count refinement: charging the first A-consuming conversion was unnecessarily expensive.

Moreover the dormant-entering birth can only occur when D=1. Its high-stage compensator is bounded by

    C E integral A_t 1_{D_t=1} dt
       <= (C/K) E integral (A_t)_2 dt <= C/K.

It is incorrect to replace its intensity by A D on the entire high strip and retain the extra J factor. Births and the optional 2D channel increase A and cannot create a high-to-low crossing.

With J=K, the high-to-low probability is O(1/K). Conditional strong-Markov stage iteration thus has a bounded geometric sum for large n. The upper-D escape is paid once, globally, rather than once at each stage. An arbitrary high initial A causes no problem: losing at least K/2 is still necessary to enter A<K/2.

## Balance

The resulting bound is

    C [K(K/n)^{1/L} + K^{-1} + exp(-cK)].

For K=n^{1/(2L+1)}, both power terms are n^{-1/(2L+1)}. Finite n are covered by probability<=1. Strong Markov at the first D=1 entrance extends the bound to every positive-D initial state; n is conserved before clearing.

## What this does and does not acquire

A raw finite graph supplies L, path constants, and hence a quantitative population-uniform dormant-return probability. No direct-source O(1/n) clock, mixing law, or finite-population enumeration is assumed. For L=1 this proof gives n^{-1/3}; it does not retroactively alter the accepted specialized profile estimates.

The output remains unweighted. Cauchy-Schwarz can combine it with a separately earned profile bound, but cannot manufacture that bound. In particular, this estimate alone does not prove the required inverse-A reward / SAME occupation ratio, nor justify importing the full four-species correction to arbitrary conversion graphs.
