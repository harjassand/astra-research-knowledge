# CRAY GENESIS: Translation-orbit compilation of infinite-lattice transport certificates

Research record, 13 October 2026. This is a proof-and-computation research artifact, not a peer-reviewed publication or a claim of independently established priority.

## Result and status

This investigation developed and implemented a finite algebraic compiler for **local dual witnesses for an infinite-lattice bulk diffusion coefficient**. The compiler identifies local currents orthogonal to every translation-summed local corrector, not merely to the finitely many correctors used in a numerical optimization. It combines exact orbit constraints, exact forbidden-transition constraints, numerical witness search, and independent rational evaluation.

The supplied certificates give rigorously outward-rounded enclosures for the one-dimensional Bertini–Toninelli exchange model:

| Particle density p | Lower endpoint | Upper endpoint | Exact interval width, approximately |
|---|---:|---:|---:|
| 1/2 | 0.714478906569 | 0.714542890949 | 6.3984379123e-5 |
| 4/5 | 0.346711554566 | 0.346715097176 | 3.5426081199e-6 |
| 19/20 | 0.096363247552 | 0.096363264947 | 1.7394350521e-8 |

These concern **collective/bulk diffusion**, not tagged-particle self-diffusion. They are bounds on the infinite-volume variational coefficient; no finite-volume extrapolation or stochastic error bar is involved. Identifying a variational coefficient with a particular hydrodynamic limit remains a separate model-dependent theorem.

Two further outputs are preserved: an explicit density-uniform rational enclosure, proving a two-term high-density asymptotic, and a no-go theorem showing that the exact local-current hierarchy cannot certify positive transport for box-closed cooperative vacancy dynamics, including the two-dimensional k=2 Kob–Andersen model.

The operation and these particular deductions were developed in this run. Broad novelty has not been independently established. The underlying Dirichlet principle is classical; the Thomson-type diffusion formula and the prospect of using it for rigorous numerical lower bounds are already explicit in Shapira [1]. Finite-dimensional primal optimization already exists in [2,3]. Gradient constructions and finite-path obstructions also have substantial prior art [1,5,6]. The contribution candidate is constructive compilation and its certified outputs, not invention of variational duality.

## Reproduction

Python 3.10 or later is sufficient for the standard-library verifier:

```sh
python verify.py
python selftest.py
```

`verify.py` reads the three JSON witness files, reconstructs each raw-polynomial current, checks every translation-orbit identity with unbounded integers, and evaluates both functionals with rational arithmetic. The verifier is specialized to the stated Bertini–Toninelli rate. It does not invoke an optimizer or use any stored decimal endpoint as evidence.

`selftest.py` also rejects an intentionally perturbed, nonconservative current; reproduces the elementary lower bound 2q/(1+q); and compares the upper-bound contraction with a direct 256-configuration evaluation of the original variational expression at four rational densities.

Numerical discovery and symbolic regeneration require NumPy, SciPy, and SymPy:

```sh
OPENBLAS_NUM_THREADS=1 python generate_certificates.py
python symbolic_bounds.py
```

The tested environment was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0. Floating-point changes between platforms may change generated witness coefficients slightly. Any generated witness must pass the independent verifier before its endpoint is used.

## 1. Why this task was selected

Three independent directions were screened before selective searches of the linked research repositories. Direct functional recovery in inverse problems is consequential, but observable-adapted inference already has a substantial theory; merely avoiding reconstruction does not create unavailable information. Observable-only quantum dynamics similarly has established operator and influence-matrix approaches [7]; a new construction must control the complexity of the representation it actually builds. Neither screen yielded a proved new efficient mechanism during this investigation.

Transport was selected because the scientifically relevant output is a coefficient, while the full long-time dynamics need not be reconstructed. Product equilibrium does not imply trivial dynamics when transitions are kinetically constrained [4]. Nevertheless, simply proposing a variational calculation is not novel: the existing specialized primal methods [2,3] must be treated as the baseline. The prospective missing operation was efficient, automatic construction of admissible **lower-bound** witnesses.

## 2. Setting and normalization

Let eta belong to {0,1}^{Z^d}, with product Bernoulli equilibrium mu_p, where 0<p<1 and chi=p(1-p). For each positive coordinate direction e_i, a nearest-neighbor exchange has a bounded local rate c_i(eta)>=0, invariant under swapping eta_0 and eta_{e_i}. Rates may vanish exactly. The generator counts each undirected bond once.

For a direction ell in R^d define

\[
a_i(\eta)=\ell_i(\eta_0-\eta_{e_i}),\qquad
G_i f=\sum_{x\in\mathbb Z^d}\nabla_{0,e_i}\tau_x f.
\]

The sum defining G_i f is finite when f is local. Use the standard bulk variational coefficient

\[
D_\ell=\frac{1}{2\chi}\inf_{f\;\mathrm{local}}
\mathbb E_p\sum_i c_i(a_i+G_i f)^2. \tag{1}
\]

The normalization gives D=1 for one-dimensional rate-one simple symmetric exclusion. Reversibility and the explicitly known product equilibrium are genuine assumptions, not estimated oracles. The coefficient in (1) is the starting mathematical target. The identities below require only (1), rather than a claim that a dual optimizer has finite support.

## 3. Exact local-current recognition

A candidate current consists of local functions j_i, each antisymmetric under its bond exchange. Require j_i=0 whenever c_i=0. Antisymmetry also makes j_i zero when the two bond occupations are equal. Write

\[
h=\sum_i j_i=\sum_A h_A\eta_A,
\qquad \eta_A=\prod_{x\in A}\eta_x,
\]

using the unique finite squarefree occupation expansion. Let [A] denote the translation class of a finite set A, and define

\[
(\mathcal O h)_{[A]}=\sum_{B\sim A}h_B. \tag{2}
\]

All sums in (2) are finite because h is local. Include the empty-set coefficient; in the current parameterization it is zero automatically.

### Theorem 1: complete finite test for local dual admissibility

For local antisymmetric j_i, the following are equivalent:

\[
\mathbb E_p\sum_i j_iG_i f=0\quad\text{for every local }f;
\qquad \mathcal O h=0. \tag{3}
\]

In particular, for a chosen finite support, exact admissibility can be recognized by a finite integer matrix, independently of the density.

### Proof

Define the finite covariance sum

\[
\langle\!\langle u,v\rangle\!\rangle
=\sum_x\operatorname{Cov}_{\mu_p}(u,\tau_xv).
\]

Product equilibrium and finite support make this well defined. Swap invariance and antisymmetry imply

\[
\mathbb E_p\sum_i j_iG_i f
=-2\langle\!\langle h,f\rangle\!\rangle. \tag{4}
\]

Also E_p h=0. In the orthonormal centered-product basis

\[
\xi_A=\prod_{x\in A}\frac{\eta_x-p}{\sqrt\chi},
\qquad h=\sum_{A\ne\varnothing}\widehat h_A\xi_A,
\]

independence gives

\[
\langle\!\langle h,h\rangle\!\rangle
=\sum_{[A]}\left(\sum_{B\in[A]}\widehat h_B\right)^2. \tag{5}
\]

If the left condition in (3) holds, put f=h in (4). Each orbit sum in (5) must vanish. Grouping the terms within each orbit then expresses h as a finite sum of translation differences of centered monomials. Expansion into raw occupation monomials preserves translation differences, so (2) vanishes.

Conversely, zero raw orbit sums express h as a finite sum of terms tau_x k-k. Each such term has zero covariance pairing with any local f because the spatial covariance sum telescopes. Equation (4) proves the converse. This also shows that the test is not a finite collection of approximate moment conditions. QED.

### Shape-graph interpretation

In one dimension every antisymmetric current can be written

\[
j=(\eta_0-\eta_1)g(\eta_{\mathbb Z\setminus\{0,1\}}).
\]

An environment monomial with support A contributes +1 at the shape [A union {0}] and -1 at [A union {1}]. Thus the orbit map before imposing legality is an incidence matrix on a graph whose vertices are **translation classes of finite particle shapes**. Its kernel is a space of circulations. Forbidden local environments give additional exact linear constraints. For indicator-valued rates, one may instead hardwire legality as j=(eta_0-eta_1)c g, which is what the implementation does.

Squarefree monomials span every function on a finite binary patch. Thus this construction does not assume an unproved compact ansatz and does not miss a local admissible current within the specified patch.

## 4. Two-sided certificate and exact gap

For a local corrector f and a current j passing Theorem 1 and legality, define

\[
U(f)=\frac{1}{2\chi}\mathbb E_p\sum_i c_i(a_i+G_if)^2,
\]

\[
L(j)=\frac{1}{2\chi}\mathbb E_p\sum_i
\left(2a_i j_i-\frac{j_i^2}{c_i}\right). \tag{6}
\]

On forbidden transitions both j_i and the corresponding quotient term are zero. Completing the square and using (3) yields the **exact identity**

\[
U(f)-L(j)=\frac{1}{2\chi}\mathbb E_p
\sum_{i:c_i>0}\frac{[c_i(a_i+G_if)-j_i]^2}{c_i}. \tag{7}
\]

It follows for every local f that U(f)>=L(j). Taking the infimum in (1) gives

\[
L(j)\le D_\ell\le U(f). \tag{8}
\]

This is a concrete constructive use of familiar Hilbert-space duality, not a claim that the completion-of-squares identity itself is new. Its computational importance is that all terms in (7) and (8) concern finite supports, while the bound quantifies the full infinite-volume target.

Neither the optimizer's convergence nor an unknown spectral gap is required for validity. Numerical optimization merely proposes witnesses. Approximation of trial coefficients can weaken a bound, but cannot invalidate it once exact admissibility is retained and the exact functionals are evaluated.

## 5. Executed compiler

The model is

\[
c(x,x+1;\eta)=1-\eta_{x-1}\eta_{x+2}. \tag{9}
\]

For the lower trial, the environment is {-6,-5,-4,-3,-2,-1,2,3,4,5,6,7}, twelve bits, together with the central bond. The dictionary uses every raw monomial not containing both forbidden-rate sites -1 and 2. Multiplication by c makes the omitted monomials redundant.

The exact orbit matrix has 3,072 columns and 5,460 rows. Its nullspace has dimension 204. No density-dependent approximation enters this nullspace construction. A Boolean zeta transform evaluates the 204 current coordinates on all 4,096 environment assignments; 3,072 assignments are legal.

At each target density, weighted least squares proposes the best current in this finite kernel. Only the 204 free coordinates are rounded, to denominator 2^40. Multiplying by the exact integer nullspace basis preserves every orbit equation exactly. The 10-site primal dictionary contains 511 translated-shape representatives. Its centered-product Gram form is factored by conditioning on the three allowed assignments of the rate sites. This avoids treating the full many-site configuration space as an unknown probability distribution.

The primal solve uses 53, 63, and 66 LSMR iterations at the three supplied densities. The verifier reconstructs and checks all current coefficients rather than trusting the nullspace computation performed during discovery.

### Measured resources

A complete regeneration of all three certificates, including imports, exact kernel construction, numerical search, rational evaluation, and output writing, was rerun under `/usr/bin/time -v`:

- Wall time: 9.19 seconds.
- Peak resident memory: 190,764 KiB, approximately 186.3 MiB.
- Exact kernel/context setup within the timed run: 4.449 seconds.
- Subsequent generation/evaluation per density: approximately 0.29–0.31 seconds.
- Standalone verification runs took roughly 0.03–0.10 seconds per certificate in this environment.

These are observations from this container, not portable performance guarantees or timings for the intellectual derivation and literature investigation. See `resource_usage.txt`, `regeneration_log.txt`, and `certified_results.json`.

### Scaling and exclusions

For s explicitly represented environment sites, the complete dictionary has size exponential in s. A Boolean zeta transform costs O(s 2^s) operations per coefficient column. Exact kernel construction and numerical optimization add polynomial costs in those explicit matrix dimensions, with coefficient bit lengths also relevant. The implementation does not establish a polynomial bound in inverse requested error, density, or spatial dimension.

There is no simulated system size N, trajectory duration T, mixing-time estimate, or sample variance in the certificate cost. This removes those costs, not the local-description complexity. Product expectations are exactly available in this class; an extension to an unknown or correlated equilibrium would have to pay for and certify those expectations separately.

## 6. Symbolic density-uniform result

A smaller, five-dimensional dual kernel (r=3), combined with a four-site primal corrector, gives for every 0<p<1:

\[
\boxed{
\frac{(1-p)(-p^4+4p^3+8p+5)}{5+3p+p^2-p^3}
\le D(p)\le
\frac{(1-p)(p^3-p^2+5p+3)}{(3-p)(p+1)}.} \tag{10}
\]

The lower current is j=(eta_0-eta_1)(1-eta_-1 eta_2) sum_A g_A eta_A. Its nineteen nonzero rational coefficient functions are in `symbolic_certificate.txt`. `symbolic_bounds.py` constructs the kernel, solves its five-dimensional symbolic quadratic problem, and checks all orbit cancellations and the claimed value exactly. Its denominator is nonzero on 0<p<1.

The explicit upper witness is, with h_i=eta_i-p,

\[
f=\frac{h_0h_1h_3-h_0h_2h_3}{(p-3)(p+1)}. \tag{11}
\]

The gap between the two rational expressions is

\[
\frac{2p^2(1-p)^3(1+2p-p^2)}
{(3-p)(p+1)(5+3p+p^2-p^3)}, \tag{12}
\]

which is positive on the full interval. Set q=1-p. The exact expansions are

\[
L_3(1-q)=2q-\tfrac32q^2+\tfrac78q^3-\tfrac{13}{32}q^4+O(q^5),
\]

\[
U_4(1-q)=2q-\tfrac32q^2+q^3-\tfrac58q^4+O(q^5).
\]

Consequently the inequalities, without assuming analyticity of D, prove

\[
D(1-q)=2q-\tfrac32q^2+O(q^3). \tag{13}
\]

This derivation was obtained here; publication priority for the particular coefficient has not been established by an exhaustive search. At p=1/2 the symbolic bounds are 151/212 and 43/60. Larger certified dictionaries give the much tighter numerical intervals above.

## 7. Comparison with specialized methods

Arita, Krapivsky, and Mallick [2,3] already minimize the standard diffusion functional over finite-dimensional local spaces, including for a Kob–Andersen model. A primal calculation being fast is therefore not evidence of a new computational capability.

Shapira [1] already supplies a dual diffusion principle and explicitly proposes numerical lower bounds as a future use. The paper gives an explicit combined lower bound D(1/2)>=0.691 for (9). The supplied compiler improves that particular displayed lower bound to 0.714478906569 while simultaneously certifying a narrow interval. The improvement over the displayed example is not a claim that 0.691 was the strongest possible specialized computation, or that no unpublished or unlocated stronger bound exists.

No optimized external implementation of the specialized primal or dual methods was benchmarked head-to-head. The substantiated gain is a reproducible automatic lower-witness construction and exact two-sided output; not a measured universal speedup over the best simulation or variational software.

## 8. A harder-case no-go result

Call the vacancy dynamics **box-closed** when, for every finite rectangular box Lambda, every configuration filled outside Lambda has no legal exchange that creates a vacancy outside Lambda. Consider bounded finite-range, translation-covariant currents obeying the same local legality rules.

### Theorem 2: local exact-current certificates have zero transport in box-closed dynamics

Every such current satisfying the exact orbit condition obeys, for every coordinate k,

\[
\mathbb E_p[(\eta_0-\eta_{e_k})j_k]=0. \tag{14}
\]

Hence its dual value is nonpositive in every direction; maximizing over any collection of these currents gives only the lower bound zero.

### Proof

First take a configuration filled outside Lambda. Each current vanishes except on finitely many bonds, and the raw orbit identity telescopes pointwise:

\[
\sum_{x,i}j_i(\tau_x\eta)=0. \tag{15}
\]

Box closure and legality make all currents on crossing bonds zero. On the finite configuration graph inside Lambda, (15) is therefore a divergence-free signed flow.

Equip the interior with the Bernoulli product measure and fix the exterior occupied. Multiply (15) by the particle first moment

\[
M_k(\eta)=\sum_{x\in\Lambda}x_k\eta_x
\]

and take expectation. For an interior bond (x,x+e_i), swap invariance and antisymmetry give

\[
\mathbb E[j_{x,i}M_k]
=-\tfrac12\mathbb E[j_{x,i}\nabla_{x,x+e_i}M_k]
=-\tfrac12\delta_{ik}\mathbb E[j_{x,i}(\eta_x-\eta_{x+e_i})].
\]

Thus the sum of expected displacement-current pairings over all interior bonds in direction k is zero. For bonds farther than the fixed current/rate range from the boundary, the expectation is precisely the infinite-product expectation in (14). Boundary contributions are at most a constant times the boundary-layer volume. Divide by the box volume and let all its side lengths tend to infinity. The boundary fraction vanishes, proving (14). Substitution into (6) gives L(j)<=0. QED.

### Application and relation to prior art

For the square-lattice k=2 Kob–Andersen rule, a particle can jump to a vacancy only when it has another vacant neighbor besides the destination, both before and after the jump. Starting with vacancies inside a rectangle and the exterior occupied, an exterior particle adjacent to that rectangle has only the destination as a possible vacant neighbor. It cannot make the first boundary-crossing jump. The box-closure hypothesis therefore holds.

The positive variational diffusivity of this cooperative model is established in [5]. That paper formulates its hydrodynamic theorem through softened rates tending to the hard constraint. The variational zero-softening limit equals the hard-rate infimum because the infimum over local f and the infimum over positive softening commute. This statement does not assert a hard-constraint hydrodynamic limit for arbitrary initial configurations.

Consequently, exact local dual kernels do not approximate the full divergence-free space in its energy norm: taking an exact kernel and taking the infinite-range closure do not commute. The obstruction concerns every local signed current, not only a particular numerical basis.

Related limitations were already visible in [5, Appendix A], which proves cooperative models non-gradient, and [1, Section 5.3], which explains why cooperative models require unbounded comparison paths. Theorem 2 provides a direct no-go statement for this entire exact local signed-current certificate hierarchy under an explicit geometric hypothesis. It should not be advertised as the first recognition that cooperative transport requires nonlocal mechanisms.

## 9. The operation still needed for genuinely hard cooperative transport

A larger local nullspace is not a route around Theorem 2. Adding a positive floor to forbidden rates also changes the scientific target and gives a monotone upper comparison, not automatically a lower certificate for the hard dynamics.

A viable different interface must retain a controlled conservation defect at finite stages and supply a genuinely nonlocal, legal completion. An exact quantitative target is as follows. Let j_R be a computable local legal current, not necessarily orbit-canceling, and produce an admissible completion J together with a proved energy-tail bound

\[
\|J-j_R\|_{c^{-1}}\le\varepsilon_R,
\qquad \|v\|_{c^{-1}}^2=\mathbb E_p\sum_{i:c_i>0}v_i^2/c_i.
\]

Then expansion of (6) and Cauchy–Schwarz certify

\[
D_\ell\ge L(j_R)-
\frac{2\|ca-j_R\|_{c^{-1}}\varepsilon_R+\varepsilon_R^2}{2\chi}. \tag{16}
\]

All finite terms in (16) can be compiled. But epsilon_R is **not** an available oracle: it must be derived from an explicit legal completion, for example a conservation-preserving random-radius routing construction, with certified routing congestion and tail probability. A spectral-gap guess or an unjustified statement that boundary errors are small cannot supply it.

No affordable, independently certified completion of this kind for the cooperative Kob–Andersen model was constructed in this run. Unbounded-path comparisons already exist [1,5]; merely naming one is not a discovery. The prospective advance would be constructive compilation of the unbounded object with useful, explicit resource and error control. Equations (14)–(16) locate this remaining task sharply while preserving the consequential transport problem.

## 10. Assessment

Established in this artifact: the local admissibility characterization, finite compiler, exact certificate identity, three machine-checked rational enclosures, the symbolic two-term asymptotic deduction, and the box-closure no-go proof.

Not established: independent publication priority for the compiler or the derived formulas; a general convergence theorem for local dual hierarchies; polynomial accuracy complexity; a practical solution of cooperative glass transport; or a historic-level computational breakthrough. Arithmetic checks do not replace independent review of the mathematical proofs.

The defensible result is a concrete constructive research operation with reproducible outputs and a proved boundary of applicability. Its strongest next consequential target is nonlocal current completion, not more local basis search on models excluded by Theorem 2.

## References consulted

[1] Assaf Shapira, *A Thomson-type variational principle for diffusion coefficients*, arXiv:2606.04636v2, 30 June 2026. Especially Sections 1.1, 3, 5.1–5.3 and Remark 5.4.

[2] Chikashi Arita, P. L. Krapivsky, Kirone Mallick, *Variational calculation of transport coefficients in diffusive lattice gases*, arXiv:1611.07719; Physical Review E 95, 032121 (2017).

[3] Chikashi Arita, P. L. Krapivsky, Kirone Mallick, *Bulk diffusion in a kinetically constrained lattice gas*, arXiv:1711.10616.

[4] Lorenzo Bertini, Cristina Toninelli, *Exclusion processes with degenerate rates: convergence to equilibrium and tagged particle*, arXiv:cond-mat/0304694; Journal of Statistical Physics 117, 549–580 (2004).

[5] Assaf Shapira, *Hydrodynamic limit for the Kob–Andersen model*, author-hosted manuscript, especially equation (2.5), Theorem 2.3, and Appendix A.

[6] Yukio Nagahata, *The Gradient Condition for One-Dimensional Symmetric Exclusion Processes* (1998), DOI:10.1023/A:1023025510497.

[7] Alessio Lerose, Michael Sonner, Dmitry A. Abanin, *Overcoming the entanglement barrier in quantum many-body dynamics via space-time duality*, arXiv:2201.04150.

[8] Matteo Giordano, Hanne Kekkonen, *Bernstein–von Mises theorems and uncertainty quantification for linear inverse problems*, arXiv:1811.04058.

The linked Astra and OpenAI mathematics repositories were selectively searched after independent direction selection. No repository result is used as a proof dependency here; this was not a comprehensive audit of either repository.
