# Lifetime acquisition compared with weak Poincaré theory

28 October 2026. Focused primary-literature comparison for the proposed
single-action-lifetime certificate for arbitrary fixed switching. This note
identifies the mathematical antecedents and the remaining observation-level
claim. It is not a historical-priority finding or a re-audit of the local proof.

## Conclusion

The proposed inequality is a one-scale weak-Poincaré/defective-Poincaré bound
for the energy of A_i^2. The deduction of decay from such an inequality and a
nonexpansive auxiliary norm is established theory. Obtaining a weak Poincaré
inequality from reversible decay is also established. The construction should
therefore be described as an observable specialization and application of that
machinery, not as a new general mechanism for decay without a spectral gap.

The useful candidate addition is the complete finite experimental contract:
single-action live/absorbed records acquire a common numerical bound, positivity
extends it from the prepared vector to all reachable order-bounded vectors,
and one confidence event then controls every switched-word tail. Together with
separately acquired short-word information, this can support a finite reusable
prediction procedure. This bounded comparison does not establish that the
complete contract is historically new.

## Primary antecedents actually checked

**Andrieu, Lee, Power and Wang (2026),** *Weak Poincaré inequalities for Markov
chains: theory and applications*, Annals of Applied Probability 36(1),
[DOI 10.1214/25-AAP2185](https://doi.org/10.1214/25-AAP2185).
Definition 3 gives the profile inequality

\[
\|g\|_2^2\le t\,\mathcal E(P^*P,g)+\beta(t)\Psi(g).
\]

Definition 1 specifies homogeneous sieve functionals and their nonexpansiveness.
Theorem 8 converts the inequality into quantitative L2 decay. The formal
setting is a time-homogeneous Markov kernel with invariant probability measure
and centered functions. Theorem 44 and the discussion preceding it identify
the converse connection under reversibility. These results already address
decay without a strict global gap.
[Accepted primary manuscript](https://wrap.warwick.ac.uk/id/eprint/192029/3/WRAP-Weak-Poincar%C3%A9-inequalities-Markov-chains-theory-applications-25%20-%20Copy.pdf),
§§2.1 and 3.2. The accessible
[arXiv version](https://arxiv.org/html/2312.11689v1) is older; some numbering
differs, so the theorem numbers here follow the accepted manuscript.

**Andrieu, Lee, Power and Wang (2022),** *Comparison of Markov chains via weak
Poincaré inequalities with application to pseudo-marginal MCMC*, Annals of
Statistics 50(6), 3592–3618,
[DOI 10.1214/22-AOS2241](https://doi.org/10.1214/22-AOS2241).
Proposition 23 is the strongest directly checked converse: a uniform bound
\(\|P^n g\|_2^2\le\gamma(n)\Phi(g)\) for a selfadjoint Markov operator yields
a WPI for P^2, with an explicit profile obtained by optimizing over n.
Definitions 1 and 4 and Theorem 8 supply the forward argument.
[Published primary PDF, pp. 3593–3595 and 3598–3599](https://awllee.github.io/papers/AOS2241.pdf).

**Feng-Yu Wang (2003),** *Functional inequalities for the decay of sub-Markov
semigroups*, Potential Analysis 18, 1–23,
[DOI 10.1023/A:1020535718522](https://doi.org/10.1023/A:1020535718522), is a
direct older antecedent for nonconservative semigroups. Its publisher abstract
explicitly concerns general functional inequalities characterizing sub-Markov
decay. Only that primary abstract and bibliographic record were accessible;
the exact theorem text was behind a subscription wall. This note does not
attribute the specific discrete-time lifetime or switching statement to it.

## Exact mathematical correspondence

The following is a direct mapping of the proposed assumptions to that
framework. Positivity here must mean **positivity preserving** (nonnegative
kernel entries), in addition to selfadjointness. Positive semidefiniteness alone
does not justify the pointwise domination step. ALPW's use of “positive” for
a reversible operator means positive semidefinite, so those meanings should
not be conflated.

For the common strictly positive unit vector v, put

\[
\Psi_v(x)=\|x/v\|_\infty^2,\qquad
\mathcal E_i(x)=\langle x,(I-A_i^2)x\rangle
              =\|x\|^2-\|A_i x\|^2.
\]

The assumption A_i v<=v makes Psi_v nonexpansive under every action.
Moreover, positivity gives the exact order-interval norm identity

\[
\sup_{\Psi_v(x)\le1}\|A_i^m x\|^2
=\|A_i^m v\|^2=f_i(2m).
\]

The upper bound follows from |A_i^m x|<=A_i^m v; equality is attained at x=v.
Thus one measured scalar supplies the uniform remainder coefficient required
by the familiar functional-inequality argument. The proposed relation

\[
\|x\|^2\le m\mathcal E_i(x)+f_i(2m)\Psi_v(x)
\]

is precisely its one-scale form. Its elementary spectral ingredient is
1-lambda^(2m)<=m(1-lambda^2) for |lambda|<=1; no spectral gap enters.

Equivalently, on a countable state space set mu_j=v_j^2 and
T_i g=v^(-1)A_i(vg). This is a symmetric sub-Markov operator on L2(mu),
and Psi_v becomes the usual squared L-infinity norm. The observed coefficient
is ||T_i^m||_(infinity to 2)^2. Because T_i1<=1, mu is generally subinvariant,
not invariant. The centered conservative ALPW theorem is therefore not a
literal plug-in theorem for the killed source; the shared energy argument
applies, and nonconservative functional-inequality theory is longstanding.

## Switching, scope and the actual acquisition obligation

Given a simultaneous upper bound s>=max_i f_i(2m), every switched orbit
starting at v remains in 0<=x<=v. The common one-step energy inequality gives

\[
\|x_{h+1}\|^2\le(1-1/m)\|x_h\|^2+s/m,
\qquad
z_h=s+(1-1/m)^h(1-s).
\]

This recursion uses the same inequality at whichever action is chosen next.
It requires neither commutation nor an identified representation. The
two-sided split of a fixed word and Cauchy–Schwarz then give the proposed
length-2h survival bound z_h. This is an elementary common-sieve extension
of the usual energy-decay argument. The inspected primary results do not
state the finite categorical acquisition and simultaneous every-word
certification contract.

A single acquired (m,s) has a limiting floor s. Calling it a complete WPI
profile requires additional bounds approaching zero; in ALPW's definition,
beta(t) must vanish. To certify a prescribed small tail, the experiment must
actually obtain a sufficiently small s, with its sampling and physical time
costs paid. No universal cheap-emission guarantee follows.

The structural common-v relation, reversibility, reproducibility of preparation
and correctness of the survival report remain premises. Scalar lifetime data
alone do not establish them. Confidence bounds and any adaptive choice of m
must be valid jointly for the choices used.

Finally, this does not contradict the two-state single-action obstruction.
Individual survival laws can bound all sufficiently long outputs while leaving
short mixed outputs and their ordering unidentified. A finite short-word cover
must obtain that missing joint information. The conclusion is a reusable tail
certificate plus paid short-word acquisition, not identification of switched
responses from lifetime marginals alone.

## Attribution to retain

Retain explicit credit to WPI/defective-Poincaré theory, reversible
decay-to-WPI arguments, positive-operator order domination and common-energy
iteration. The statement “finite native lifetime data can acquire an
all-switching tail under a shared excessive preparation vector” captures the
new package's operational point. Assertions of a first gap-free decay theorem,
a general new WPI, or superiority over methods supplied with the same acquired
profile would be unsupported.
