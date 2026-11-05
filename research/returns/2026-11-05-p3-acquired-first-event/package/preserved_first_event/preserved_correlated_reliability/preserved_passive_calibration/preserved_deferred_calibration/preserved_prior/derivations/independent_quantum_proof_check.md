# Independent check of the new finite-control acquisition theorem

Reviewer: rare_interventions collaborator. Date: 5 November 2026.

## Status

This checks the NEW constructions developed by continuous_quantum and root in the current run. It does not revalidate the inherited, accepted P1 weak-control theorem.

The stronger decorated-trajectory recursion is sound under the global summed term-norm budget. The initial terse extension to only branchwise classical-feedback budgets was not justified: a later record-dependent insertion support can select an earlier differentiated site. The separate chronological proof below does establish the full classical-feedback result, with a weaker constant.

Both established versions yield exponential suppression for every fixed finite control/noise ratio and fixed source interaction arity. This is a proof check, not an experiment or a literature-priority determination.

## Model and exact claims

For w initially unencoded source qubits R, define

\[
\mathcal P_R=\prod_{i\in R}(\mathrm{id}-\operatorname{Ad}_{Z_i})/2.
\]

Its diamond norm is at most one. Actual hidden independent noise has generator

\[
\lambda\sum_i(\operatorname{Ad}_{Z_i}-\mathrm{id}).
\]

All source operations not preserving the relevant Z_i parity sectors must be implemented through bounded Hamiltonian terms H_a(t). Let B_a conservatively include all source sites where H_a is Z_i-noncommuting, put h_a=2\|H_a\|, and require |B_a|\le k. The apparatus starts independently of the unknown payload. Free maps preserve each relevant Z_i parity sector on the joint source, apparatus, and classical record.

Let B(t)=\int_0^t\Omega(u)\,du.

Under a GLOBAL full-operator term-norm budget \sum_{a:i\in B_a}h_a(t)\le\Omega(t), the established bound, for B(t)\le1, is

\[
\|\Phi_t\mathcal P_R\|_\diamond
\le[e^{-2\lambda t}+(1-e^{-2\lambda t})B(t)^{1/k}]^w.
\]

For constant \Omega, t_*=1/(2\Omega) gives the time-uniform acquired-output factor

\[
f_{\rm global}=e^{-\lambda/\Omega}+
(1-e^{-\lambda/\Omega})2^{-1/k}.
\]

For ONLY branchwise classical-feedback budgets

\[
\sup_r\sum_{a:i\in B_a}h_{a,r}(t)\le\Omega(t),
\qquad h_{a,r}=2\|H_{a,r}\|,
\]

the chronological proof establishes, for kB(t)\le1,

\[
\|\Phi_t\mathcal P_R\|_\diamond
\le[e^{-2\lambda t}+(1-e^{-2\lambda t})(kB(t))^{1/k}]^w.
\]

Taking t_*=1/(2k\Omega) yields

\[
f_{\rm CQ}=e^{-\lambda/(k\Omega)}+
(1-e^{-\lambda/(k\Omega)})2^{-1/k}.
\]

Thus \|\mathcal A_T\mathcal P_R\|_\diamond\le f^w for every acquired-output stopping time T, with the applicable factor. Do not give the stronger constant to the branchwise-only class without another proof.

## Common hidden-noise representation

Put \mathcal E_i=(\mathrm{id}+\operatorname{Ad}_{Z_i})/2. Then

\[
\lambda(\operatorname{Ad}_{Z_i}-\mathrm{id})
=2\lambda(\mathcal E_i-\mathrm{id}).
\]

Independent rate-2\lambda Poisson clocks applying \mathcal E_i therefore give a valid convex unraveling. Fix a clock trajectory on [0,t], let S\subseteq R be its hit sites, and let \tau_i be their first event times. This representation is legitimate because no noise-environment record is available.

## Global-budget decorated-recursion check

Introduce x_i\in[0,1] for i\in S and replace each H_a(u) by

\[
H_a(u)\prod_{i\in B_a\cap S:\ u<\tau_i}x_i.
\]

Every interpolated full propagator is CPTP. On x_i=0, all Z_i-noncommuting control before \tau_i vanishes; the first \mathcal E_i commutes backwards and kills \mathcal P_R.

For a decorated trajectory, let C be the union of explicit commutator insertion supports and U=S\setminus C. Each existing insertion commutes with every unresolved Z_j and its coefficient is independent of x_j. Thus the decorated trajectory still vanishes on x_j=0.

Apply the fundamental theorem of calculus to one i\in U. Duhamel differentiation inserts a term touching i. Mark ALL B_a\cap U, so subsequent derivatives never hit old insertion coefficients. At most k unresolved sites are removed.

The full-propagator segments partition [0,t], so the summed insertion integral is at most \int_0^t\sum_{a:i\in B_a}h_a(u)du\le B(t), without a segment-count factor. Induction gives

\[
\|\Phi_\omega\mathcal P_R\|_\diamond
\le B(t)^{\lceil|S|/k\rceil},
\]

because |U'|\ge|U|-k and B\le1 imply

\[
B\,B^{\lceil|U'|/k\rceil}\le B^{\lceil|U|/k\rceil}.
\]

The zero-unresolved-site case is CPTP contractivity. No missing factorial or ordered-partition factor was found.

### Feedback nuance

The nonchronological recursion can choose the next site using a support selected at a LATER time. If that support depends on a later classical record, summing after differentiating an EARLIER propagator does not follow from one current-record site budget. Final support tags alone do not repair this future-dependent selection. This is a proof limitation, not a counterexample to the stronger numerical bound.

## Earned branchwise-feedback proof

At current time u, let U be unresolved, with all its first events after u. Set \tau_U=\min_{i\in U}\tau_i. Remove ALL Hamiltonian terms touching U until \tau_U. The resulting base propagator \mathcal V_U is CPTP, preserves the U-transverse sector, and is killed by the first event at \tau_U.

Duhamel comparison gives the exact first-restored-interaction decomposition

\[
\mathcal U(t,u)\mathcal P_U
=\sum_{a:B_a\cap U\ne\varnothing}
\int_u^{\tau_U}
\mathcal U(t,v)\mathcal K_a(v)
\mathcal V_U(v,u)\mathcal P_U\,dv,
\]

where \mathcal K_a=-i[H_a,\cdot]. After insertion a, the operator remains transverse on U'=U\setminus B_a. Since v\le\tau_U, all first events for U' remain in the future. Support choices are now CHRONOLOGICAL.

Let F_U(u) bound the remaining channel on that transverse sector, uniformly over auxiliary systems and classical initial records. Then

\[
F_U(u)\le\sum_{a:B_a\cap U\ne\varnothing}
\int_u^{\tau_U}h_a(v)F_{U\setminus B_a}(v)\,dv,
\]

with the block-sum interpretation below.

Write b(u)=\int_u^t\Omega(v)dv and suppose kb(u)\le1. Induction proves

\[
F_U(u)\le[kb(u)]^{|U|/k}.
\]

Indeed, for s=|U| and removal r\le k,

\[
[kb(v)]^{(s-r)/k}\le[kb(v)]^{s/k-1}.
\]

The sum of all touching-term norms is at most s\Omega(v). Extending the integration endpoint to t gives exactly

\[
s\int_u^t\Omega(v)[kb(v)]^{s/k-1}\,dv=[kb(u)]^{s/k}.
\]

The negative exponent possible when s<k is integrable, so the calculation also covers that case. The empty unresolved set has bound one.

### Exact block-sum norm

With a classical record and arbitrary quantum reference, write X=\bigoplus_r X_r. Retain a support tag at the CURRENT insertion. If G_a(v) is the uniform future bound for U\setminus B_a, then

\[
\begin{aligned}
\sum_{r,a:B_a\cap U\ne\varnothing}
G_a(v)\|\mathcal K_{a,r}(v)X_r\|_1
&\le\sum_r\|X_r\|_1
\sum_{a:B_a\cap U\ne\varnothing}h_{a,r}(v)G_a(v)\\
&\le s\Omega(v)[kb(v)]^{s/k-1}\sum_r\|X_r\|_1.
\end{aligned}
\]

The preceding base propagator is CPTP and contracts the direct-sum norm. Subsequent support choices occur after the current insertion, so no later record selects an earlier differentiated site.

Do not sum individual maxima over records. Do not assert this intermediate estimate for arbitrary coherent record inputs. The final source-input channel still has its ordinary diamond bound because the record starts classical and stays classical.

## Averaging and stopping

The hit indicators are independent Bernoulli with p=1-e^{-2\lambda t}. Averaging the fixed-trajectory powers gives the displayed product bounds; for the stronger proof use B^{\lceil s/k\rceil}\le B^{s/k}.

If acquisition ends before t_*, retain its apparatus outputs unchanged and continue only hidden source dephasing until t_*, then trace out the source. For acquisition after t_*, use data processing. A classical adaptive stop flag is handled branchwise.

This does not permit the original source itself to become a protected output at zero cost.

## Matched fixed-k consequence and limits

Independent allowed rotations H_i=(\Omega/2)Y_i followed by Z readout acquire X visibility

\[
c(t)=\frac{\Omega}{\omega}e^{-\lambda t}\sin(\omega t),
\quad\omega=\sqrt{\Omega^2-\lambda^2},\quad\Omega>\lambda.
\]

The maximum occurs at T_*=\arctan(\omega/\lambda)/\omega and equals e^{-\lambda T_*}. Randomizing the rotation sign and compensating the reported sign cancels the initial-Z term. Weight-w parity visibility is c_{\max}^w, asymptotically

\[
\exp[-\pi\lambda w/(2\Omega)+O(\lambda^2w/\Omega^2)].
\]

Both upper bounds have a positive fixed-k exponent proportional to \lambda w/\Omega at strong control. Thus constant one-copy contrast of the specified global-coherence/parity family has matched scaling \Omega/\lambda=\Theta(w), with constants depending on k.

For states whose difference lies in \mathcal P_R, an N-copy hybrid argument gives output trace distance at most 2Nf^w. Success at least 2/3 requires N\ge1/(3f^w). Polynomially many copies only force order w/log(w) control, up to fixed-k constants.

- This matched construction is NOT a universal-purity acquisition algorithm.
- No matching optimal threshold for growing k has been established.
- Actual independent hidden Markovian dephasing is assumed. Control changing a non-Markovian bath spectrum is outside the claim.
- Prepared codes, coherent environment/purifier access, native extensive interactions, and unbounded meter Hamiltonians add resources.
- Every noncommuting measurement interaction must be charged.
- This is not a zero-capacity theorem or a prohibition on protected quantum computing.
- No physical experiment or new simulation was performed in this independent check.
- Literature priority remains separate from mathematical correctness.
