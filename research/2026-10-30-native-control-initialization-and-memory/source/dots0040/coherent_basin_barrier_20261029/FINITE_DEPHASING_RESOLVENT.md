# Exact finite-rate syndrome-disagreement resolvent for atomic SSF

2026-10-29. This is a proved mechanism-specific lemma for ideal atomic SSF, not a full coherent-memory theorem. It improves on the earlier conditional barrier by constructing an actual local inverse without assuming SSF mixing. Added physical operation: rate-kappa random conjugation by each bounded-weight stabilizer generator. This acts identically on codespace and uses no Pauli-frame key. Its implementation noise still must be charged/compiled.

## 1. Exact covariance, including feedback

Let S_j be all commuting stabilizer checks. An atomic SSF instrument has Kraus operators K_a=F_a Pi_a: Pi_a measures some commuting checks and F_a is its outcome-dependent Pauli correction. Each K_a is an eigenoperator of conjugation by every S_j, with eigenvalue +/-1. Consequently the entire instrument, and its Poisson generator L_SSF, commute with every Ad(S_j). This remains true when idle Kraus operators and records are included. No claim that the controller has classical hidden error labels is required.

For each admissible syndrome-disagreement vector delta, define

    P_delta(X)=sum_sigma Pi_{sigma+delta} X Pi_sigma.

Equivalently this is the character Fourier projector of the finite stabilizer-conjugation group. Therefore ||P_delta||_diamond<=1: it is an average of unitary channels with coefficients of modulus one. P_0 is the physical complete syndrome dephasing channel; P_delta for delta!=0 is not positive. Logical and retained-bath degrees of freedom are untouched.

Add the local engineered generator

    D_kappa = kappa sum_j (Ad(S_j)-I).

It acts as -2 kappa |delta| on P_delta. Redundant checks cause no problem: delta ranges over admissible joint eigenvalue differences, and |delta| counts the actual checks used in D. Since L_SSF preserves delta,

    exp[t(L_SSF+D_kappa)] P_delta
      = exp[-2 kappa |delta|t] exp[t L_SSF] P_delta,

hence EXACTLY

    ||exp[t(L_SSF+D_kappa)]P_delta||_diamond
      <= exp[-2 kappa |delta|t].                     (1)

This holds even if L_SSF has many stationary states, traps, or an extensive protected logical algebra. No global rapid-mixing theorem is used.

## 2. Uniform local offdiagonal inverse

Let V_Z be any bounded superoperator acting on s data qubits and an arbitrary common bath. On input in P_0 it creates at most 4^s syndrome-disagreement labels (expand left/right data Paulis and group their products). Therefore

    R_off V_Z P_0 := sum_delta!=0 integral_0^infty
           exp[t(L_SSF+D_kappa)] P_delta V_Z P_0 dt

is well-defined and obeys

    ||R_off V_Z P_0||_diamond
       <= (4^s-1)||V_Z||_diamond/(2 kappa).           (2)

The unperturbed generator times this integral is -Q V_Z P_0, where Q=I-P_0. This is an actual local-source inverse with an N-independent bound. It avoids summing over all exponentially many disagreement sectors. Its construction does not yet imply spatial quasi-locality of the *entire* superoperator: exterior SSF continues evolving. A local response comparison would subtract/resum that exterior evolution, then combine a Lieb-Robinson bound with the e^{-2kappa t} cutoff; that additional argument is not supplied here.

## 3. Resume diagonal noise exactly into the base generator

For each local unknown Hamiltonian h_Z and jump K_Z, decompose operators into stabilizer characters:

    h_Z=sum_a h_{Z,a},  K_Z=sum_a K_{Z,a}.

These Fourier components remain supported on Z (and the same bath): stabilizer conjugation does not enlarge Pauli support. Define the covariant local Lindbladian

    L_diag,Z = -i[h_{Z,0},.] + sum_a D[K_{Z,a}].

For syndrome-diagonal input,

    P_0 L_noise,Z P_0 = P_0 L_diag,Z P_0.             (3)

L_diag is a bona fide local Lindbladian, commutes with all stabilizer conjugations, and can be incorporated into the CPTP base generator together with SSF, bath-only evolution, and D_kappa. Equations (1)-(2) remain exact for that new base even for time-dependent diagonal noise (replace exponential by the propagator). Thus all diagonal noise and all exterior ideal dynamics are resumed before estimating offdiagonal source norms.

The difference V_off=L_noise-L_diag has no charge-preserving component: P_delta V_off P_delta=0. It consists of nonzero-charge Hamiltonian terms and cross-character jump/anticommutator terms. Their coefficients are signed; they cannot be treated as physical Poisson probabilities.

## 4. Exact second-order excursion estimate

For two local offdiagonal terms V_Z,V_W, the order-two diagonal memory kernel contains

    P_0 V_W U_base(t,s) P_delta V_Z P_0.

Its norm is at most ||V_W||||V_Z|| exp[-2kappa|delta|(t-s)] and its time integral at most ||V_W||||V_Z||/(2kappa|delta|). It vanishes unless W can change the same disagreement delta back to zero. In particular, if the check neighborhoods of Z and W are disjoint, no nonzero delta can be both created and removed, so the second-order term is exactly zero. Bounded check incidence and bounded primitive supports therefore prevent an N^2 count of independently positioned second-order return excursions.

This is not a Pauli Markov approximation: the kernel has finite temporal memory and can be signed. Higher orders are charge walks; the exact damping is exp[-2kappa integral |delta(u)| du]. They need a linked-cluster or selector argument before inferring a stable effective diagonal stochastic process. Replacing this kernel by a positive rate of order epsilon^2/kappa without controlling the remainder would be unjustified.

## 5. Remaining decisive obligations

1. Bound all connected returning charge excursions at fixed finite kappa, resumming disconnected diagonal/outside evolution before norms. The charge damping and local-source inverse solve the bare denominator problem but not the full cluster combinatorics.
2. Relate the resumed covariant L_diag noise to the existing memory theorem. Its conditional syndrome jump rates are bounded, and its no-jump evolution is syndrome-preserving; with a retained quantum bath this still requires a positive record domination proof, not an automatic CPTP-kick identification.
3. Prove the added stabilizer-dephasing operation for the actual physical transactional implementation. Atomic SSF covariance does not by itself imply covariance throughout partial controller transactions.

A full time-independent continuous-noise information phase is NOT proved. Unlike the first barrier note, however, the key inverse (2) is derived directly from the actual atomic measurement/feedback structure, with finite kappa independent of N and no clean SSF mixing assumption.
