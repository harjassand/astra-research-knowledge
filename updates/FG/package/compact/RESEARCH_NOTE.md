# ASTRA FRONTIER — Conditional-envelope closure of hidden kinetics

Research checkpoint: 14 October 2026 (Australia/Brisbane).

## 0. Status and scientific objective

The retained objective is reliable molecular residence/reaction-time prediction under hidden conformational gating, without enumerating conformations, waiting for rare transitions, or assuming a useful committor, pathway list, metastable-rate oracle, equilibrium sample set, or affordable generic high-dimensional integration.

This checkpoint makes a concrete advance over the preceding explicit-state completion algorithm. It develops a **conditional-envelope closure**: bounds on local interaction weights and kinetic quadratic forms compile into two source-aware resolvent problems on retained coordinates. The hidden bath's states, rates, mixing time, internal partition function and equilibrium samples need not be constructed. It also implements an exactly checked, non-enumerative solver/certificate for a growing soft-East model and an authored continuous gated diffusion.

The central claimed mathematical construction is the two-source closure in Section 3, together with the spectral/source-response certificate that evaluates the retained problems. The proof uses established variational and inverse-order principles. Tensor trains, matrix-product operators, low-rank Poisson solves, source residual estimates, and functional a posteriori error bounds are established methods. **Historical novelty of the specific construction is unresolved. No fundamentally new mathematical principle, independently validated molecular prediction, state-of-the-art molecular speed advantage, or civilisation-changing capability is established.**

The important remaining acquisition problem is no longer an unavoidable explicit state list. It is obtaining useful global coefficient/interaction envelopes and an accurate compact response when the omitted region contains the kinetically decisive trap. Sparse observations alone do not establish those envelopes. The most difficult tested gate setting still gives an unusably broad interval.

### Executed highlights

- A 128-spin soft-East instance, with 2^128 transient configurations, has an exact all-state mean-lifetime enclosure using 62,120 stored tensor coefficients and no enumerated conformation list.
- A 128-coordinate continuous diffusion has an exact continuum enclosure [11735.2473695064, 11740.8172532523], upper/lower ratio at most 1.0004746286, using 32,032 tensor coefficients. There is no conformation grid, equilibrium sampling, or discretization of physical time. The interval is for the stated model in its intrinsic units, not a measured molecular lifetime.
- A 16-resolved-state conditional closure bounds every admissible hidden bath under a specified 100-fold local interaction-weight uncertainty by [18223.604862210872..., 18573.892539950375...]. The hidden bath can be arbitrarily large and non-Gaussian. The interval becomes very broad when the same uncertainty is placed in the dominant trap. This is an authored closure/falsification diagnostic, not an independently selected molecular benchmark.
- 4,253 exact rational implementation/algebra checks, 20 source-mass perturbation checks, and separately charged small hidden-bath reference solves were executed. These are internal audits, not external review or a proof-assistant formalization.

## 1. Inherited result and why another representation was needed

The preceding checkpoint represented every microscopic state and possible move. Its exact one-edge endpoint minimax theorem chose which unknown conductance to interrogate. The small-network sparse solver and a structurally correct specialized learner were faster. An adversarial unmeasured shortcut changed a lifetime by more than 11,961-fold without changing a sparse learner's observations.

The inherited source-aware Schur identity was

    K = A_OO - A_OH A_HH^{-1} A_HO,
    b = m_O - A_OH A_HH^{-1} m_H,
    gamma = m_H^T A_HH^{-1} m_H,
    F = gamma + b^T K^{-1} b.

A dead-end hidden state can leave homogeneous boundary conductance unchanged while making gamma arbitrarily large. It is therefore insufficient to approximate only a boundary conductance map or declare unobserved states absent.

This investigation changes the object represented. For a selected lifetime objective, the full K,b,gamma need not be reconstructed separately. It is enough to bound their combined positive-source resolvent response, including source normalization. This is not permission to discard gamma: the closure below bounds the full source functional before eliminating hidden coordinates.

The inherited report is `/mnt/data/astra_hidden_gate/RESEARCH_NOTE.md`. No theorem from either optional GitHub research repository is a load-bearing premise here.

## 2. Mechanisms examined and the necessary information

### 2.1 Low-rank response fitting alone

A tensor or learned coordinate representation can be small while missing precisely the component that dominates residence time. A small projected linear-system residual is not the residual of the physical continuous operator. An actual three-coordinate test below solves its degree-two Galerkin equations to floating residual about 10^-14, while the full continuum residual norm squared is about 0.3622. The omitted degree-three components matter.

The retained replacement is to compute a rigorous, source-weighted error contribution for every omitted mode rather than assume a fitted representation is complete.

### 2.2 Short-time measurements or finitely many spectral moments alone

The inherited hidden-tail example survives: survival laws exp(-t) and (1-p)exp(-t)+p exp(-t/T) differ uniformly by at most p but have means 1 and 1-p+pT. A short-time or small-amplitude fit needs an independently justified slow-tail/observability constraint. We did not implement or validate a new laboratory measurement that supplies it.

### 2.3 A smooth-force black-box obstruction

Fix a bounded domain with a reflecting boundary except for a nonempty absorbing part, and unit diffusion. Run any deterministic procedure that makes finitely many point queries of the energy and any finite collection of its derivatives on the zero potential. A small open ball away from every queried point and the absorbing boundary remains.

Construct a C-infinity potential U_H equal to -H on an inner ball, smoothly returning to zero inside a larger unqueried ball. Every queried energy/force/derivative remains unchanged. Choose a nonnegative smooth test function phi equal to one on the entire perturbed support, vanishing near absorption, and with its gradient supported only where U_H=0. Its Dirichlet energy E is independent of H. For m_H=exp(-U_H),

    <m_H,A_H^{-1}m_H> >= <m_H,phi>^2 / E.

The source pairing is at least v exp(H), where v is the inner-ball volume. Total mass is at most |Omega| exp(H). Consequently the equilibrium-conditioned mean is at least

    v^2 exp(H)/(E |Omega|),

which diverges. Thus finite local energy/force queries do not supply a uniformly valid finite upper lifetime bound over unrestricted smooth potentials. The statement is about this specified access class and initial law, not a no-go theorem for molecular science or every experiment.

A valid global regularity bound, an explicit bounded interaction law, a coercive physical inequality, or stronger measurement information can exclude this completion. Such information must be established, not inferred merely because a sparse fit agrees with observed forces.

### 2.4 Conditional envelopes rather than a supplied transport map

The surviving operation is to bound how hidden coordinates can change the **source density, kinetic quadratic form, and reaction/absorption term**, without estimating their equilibrium distribution or metastable transitions. These bounds generate retained-coordinate source-response problems. Their numerical solution is certified separately.

## 3. Conditional-envelope closure theorem

### 3.1 Model, target, and global input information

Write the full configuration as (x,y), with retained elementary physical coordinates x and unrepresented coordinates y. Let pi(dx) be a tractable reference measure on x. Let nu(dy) be any normalized reference measure on y, whose density, partition function, dimension, and internal interactions need not be evaluated.

The actual unnormalized equilibrium measure relative to pi times nu is w(x,y)>0. The initial law for the present theorem is the actual normalized equilibrium law on the pre-reaction domain. Let

    ell(x) <= w(x,y) <= u(x),       ell>0,
    Z_ell=<ell,1>_pi,             Z_u=<u,1>_pi.

The full reversible dynamics, including killing or a specified absorbing boundary, has a positive closed quadratic form mathfrak a_theta in L2(pi times nu). Its Poisson equation in this reference Hilbert space is

    A_theta t = w,
    tau_theta = <w,A_theta^{-1}w> / <w,1>.

A_theta is a **weighted form operator**, not necessarily minus the physical generator in L2(pi times nu). This distinction is essential when w is nonconstant.

Assume two retained positive form operators A_- and A_+ satisfy:

1. For arbitrary full-domain functions f,

       mathfrak a_theta[f] >= integral nu(dy) mathfrak a_-[f(.,y)].

2. For functions depending only on x,

       mathfrak a_theta[f(x)] <= mathfrak a_+[f].

3. A_- and A_+ have positivity-preserving inverses; the source/energy integrals and inverses used below exist.

These hypotheses hold for block-diagonal reversible diffusions when the gate diffusion and killing coefficients have pointwise envelopes. Hidden-coordinate diffusion contributes a nonnegative form and vanishes on x-only trial fields. Arbitrary cross-diffusion is not automatically covered: the first full-form inequality must then be established explicitly.

For example, with local coefficients

    D_-(x) <= D_x(x,y) <= D_+(x),
    k_-(x) <= k(x,y) <= k_+(x),

one may use

    mathfrak a_-[f] = integral pi ell (grad f . D_- grad f + k_- f^2),
    mathfrak a_+[f] = integral pi u   (grad f . D_+ grad f + k_+ f^2).

Dirichlet absorption can replace killing when its retained-coordinate geometry and positive inverse are justified. No unknown target surface is supplied by this theorem.

### 3.2 Two-source bound

Then

    <ell,A_+^{-1}ell> / Z_u <= tau_theta
                              <= <u,A_-^{-1}u> / Z_ell.       (CE)

This is the candidate compact source-aware operation. Its required description is (ell,u,A_-,A_+), not a hidden-state list. It does not require an equilibrium sampler, conditional free energy, hidden transition rates, bath mixing gap, or bath timescale separation.

The sources deliberately differ from the weights used in the operators. Replacing both quantities by a naively averaged generator would not establish (CE). Source mass and accumulated hidden residence are charged simultaneously.

### 3.3 Proof

For the upper bound, form order gives

    A_theta^{-1} <= (A_- tensor I)^{-1}.

Therefore

    <w,A_theta^{-1}w>
       <= integral nu(dy) <w(.,y),A_-^{-1}w(.,y)>_pi
       <= <u,A_-^{-1}u>_pi.

The second inequality follows from 0<w<=u and positivity preservation of A_-^{-1}; it is not an entrywise consequence of arbitrary matrix inverse order. Divide by actual mass at least Z_ell.

For the lower bound, choose the x-only test field v=A_+^{-1}ell>=0. The variational principle and the two envelope assumptions give

    <w,A_theta^{-1}w>
       >= 2<w,v> - mathfrak a_theta[v]
       >= 2<ell,v>_pi - mathfrak a_+[v]
        = <ell,A_+^{-1}ell>_pi.

Divide by actual mass at most Z_u. This proves (CE).

A numerical approximation of v need not be pointwise positive if one first certifies the retained quadratic response <ell,A_+^{-1}ell>. Positivity is used for the exact comparison proof, while the separate residual certificate is valid for arbitrary admissible retained trial fields.

The bound is generally conservative, not an exact extremum over all physical completions. The simultaneous source/form extrema may not be realizable by one hidden model.

### 3.4 Physically obtainable sufficient inputs

Suppose an explicit physical model has

    U(x,y)=U_g(x)+U_b(y)+sum_alpha V_alpha(x,y).

If each local term has a globally justified range

    V_alpha^-(x)<=V_alpha(x,y)<=V_alpha^+(x),

then

    ell(x)=exp[-beta sum_alpha V_alpha^+(x)],
    u(x)  =exp[-beta sum_alpha V_alpha^-(x)]

are valid interaction-weight envelopes. For bounded analytic features and parameter boxes, obtaining these termwise ranges is local interval algebra; the number of terms and the cost of bounding each term are charged. Treating the ranges independently can be loose, but is safe. General global optimization of an arbitrary interaction term is not assumed affordable.

U_b, its partition function, and its internal metastability disappear into the unknown nu. This remains valid with thermodynamic x-y coupling through w, not only a product physical equilibrium distribution.

Diffusion/mobility and reaction/absorption information remain essential separate inputs. A potential or its forces alone do not determine a kinetic generator. In this checkpoint, complete analytic generator laws and declared coefficient envelopes are the physical model inputs. No atomistic experiment that infers these global envelopes from sparse raw force measurements was performed.

### 3.5 Uniform bath and energy-envelope corollaries

If w=1 and retained gate forms are between a times and b times a reference killed gate form, while arbitrary hidden dynamics is nonnegative and vanishes on gate-only functions, then

    tau_g/b <= tau_full <= tau_g/a.                     (B)

No bath dimension, partition function, spectral gap or mixing time appears. An exact gate interval [L,U] gives [L/b,U/a]. The full operator need not have an upper bound by b times a gate-only operator: only the gate-only trial-form upper bound is needed.

If the interaction weight has global ratio R (after an irrelevant constant energy shift, 1/R<=w<=1), then

    tau_g/(b R^2) <= tau_full <= (R^2/a) tau_g.           (E)

This also accounts for the change in the initial equilibrium mass, rather than silently keeping it fixed. Pointwise x-dependent (CE) can be vastly tighter than this global scalar bound.

An arbitrary initial preparation is not automatically covered by (CE), (B), or (E). The known-operator two-load certificate below can treat a supplied represented preparation, but no binding-prepared molecular ensemble was calibrated here.

## 4. Exact conditional-closure diagnostics: strong hidden uncertainty

The closure compiler in `conditional_envelope.py` uses four retained soft-East gate bits and exact rational arithmetic. It does not receive any hidden-bath states, rates, equilibrium weights, or transition alphabet.

The retained q=1/26 and softness epsilon=10^-4 define the same microscopic model class used later. An interaction envelope is

    1 <= w(g,y) <= 1+(R-1) h(g),

where h is a specified elementary interaction feature. Gate-edge conductances are bounded using

    c_- = c_0 min(ell(g),ell(g')),
    c_+ = c_0 min(u(g),u(g')),

and the corresponding source envelopes are m_g ell and m_g u. Reaction conductance uses the local mass weight times the specified hazard. This is an authored diagnostic for source-aware completion, not a blindly selected protein or an unknown interaction support discovered from data.

At R=100:

| Interaction feature h | Closure lower (approx.) | Closure upper (approx.) | Upper/lower ratio |
|---|---:|---:|---:|
| Four retained bits all open | 18,223.604862 | 18,573.892540 | 1.019221646 |
| First retained bit open | 486.218110 | 429,584.939578 | 883.523117 |
| Four retained bits all closed | 27.844710 | 153,948,320.246432 | 5,528,817.598 |

The scalar global-energy envelope would allow a ratio R^4=100,000,000. The conditional source-aware operator distinguishes a large but low-impact uncertainty from uncertainty at the dominant trap. It does not declare the latter safe.

The known interaction envelope controls where the hidden perturbation can act. The all-open feature is not evidence of discovering an unknown interaction support. The source-response calculation, not an assumption of weak bath coupling everywhere, determines its aggregate possible kinetic effect.

For separate implementation checks, `conditional_reference.py` explicitly built small full models with 0,2,4,6 hidden bath bits, correlated Ising-type bath weights, and bath rate scale 10^-9. The actual density used a non-product interaction

    w(g,z)=1+99 h(g) [parity(z)],

and every gate/bath rate was derived from one reversible conductance model. The small references used 16,64,256,1024 states, respectively; their work is separately charged and is not part of the closure operation.

For the all-open envelope, reference means were approximately 18569.909, 18497.399, 18466.970 and 18449.775. All reference intervals lie inside the same closure interval. Two additional dominant-trap/first-open references also passed their much wider completion bounds. All full reference solves were checked with exact rational max-residual bounds, not just floating point values.

The theorem applies to arbitrarily large admissible baths. That is a uniform mathematical statement, not a claim to have simulated a million-coordinate bath. The hidden bath may contain additional pathways and arbitrarily slow internal kinetics, but may not violate the supplied gate-conductance, mass and target envelopes.

## 5. Source-response certificates for the retained problems

Let H be a positive self-adjoint operator and B a finite collection of source/load columns. For approximate response columns V, define

    R=B-HV,
    G0=B*V+V*B-V*HV,
    G=B*H^{-1}B.

Direct expansion gives

    G=G0+R*H^{-1}R.

If 0<C<=H is an acquired, tractably invertible form minorant, then

    G0 <= G <= G0+Gamma,       Gamma=R*C^{-1}R.           (SR)

All inequalities are Loewner inequalities on the finite source space. In a hidden-region Schur calculation, the columns can include retained boundary loads and the mass source. The mass-source diagonal contains the hidden internal-residence response gamma. This is not a source-blind boundary approximation.

For one normalized equilibrium source b=1,

    L=2<1,v>-<v,Hv>,
    r=1-Hv,
    L<=tau<=L+<r,C^{-1}r>.

A finite source basis does not certify arbitrary boundary data outside that basis. The present large experiments compute one lifetime source, not an entire Dirichlet-to-Neumann map.

For two represented loads, write E=G-G0. From 0<=E<=Gamma one obtains

    (Gamma_ab-sqrt(Gamma_aa Gamma_bb))/2
       <= E_ab <=
    (Gamma_ab+sqrt(Gamma_aa Gamma_bb))/2.

One proof writes E=Gamma^(1/2) T Gamma^(1/2), 0<=T<=I, and extremizes the two-dimensional symmetric cross functional. This gives a prepared-source route when its density/load can actually be represented and integrated. It does not supply that preparation information free.

These algebraic identities and functional error-estimation principles are established mathematics. The specific local-coercivity/spectral compiler and its use within (CE) are the construction being investigated for priority and usefulness.

## 6. Computing the certificate without microscopic enumeration

### 6.1 Spectral counters

For a reference minorant

    C=c I + lambda sum_i Q_i,

where Q_i are commuting projectors onto local nonconstant modes, let P_j project onto exactly j nonconstant coordinates. Then

    <r,C^{-1}r> = sum_{j=0}^n ||P_j r||^2/(c+lambda j).

The weights are coefficients of

    Z_r(z)=<r, tensor_i (P_i+z Q_i) r>.

A tensor-train response represents a function by products of small coordinate-dependent matrices. The coefficient counter contracts those matrices and a short polynomial index; it does not visit all microscopic configurations. Retaining the first J coefficients and charging every remaining coefficient with denominator c+lambda(J+1) is a rigorous upper bound. The weights are nonnegative.

For multiple local degrees, it is useful to additionally partition by the largest local degree. If a component has maximum degree j, its reference energy is at least the local eigenvalue lambda_j. This gives a hierarchy of exact spectral masks without constructing an exponentially large tensor coefficient array.

### 6.2 Floating proposal, exact witness

The solver uses ordinary two-site tensor-train variational sweeps (DMRG-style local positive linear solves and SVD truncation). No claim of a new optimizer is made. Ranks/degrees/sweeps are selected and their failures charged.

The verifier rounds tensor coefficients to explicitly defined dyadic rationals, creating a new exact trial function. The proposal's floating-point error, SVD error and lack of convergence need not be guessed. The exact trial is inserted into a rigorous residual formula.

Custom C++ GMP integer contractions compute source pairings, energies, full residual norms, and masked spectral weights. Python Fraction arithmetic constructs final rational bounds and outward-rounded decimal strings. In the continuous case, local Jacobi moments and operator coefficients are rational; no quadrature approximation is hidden.

A coarse globally valid ceiling from uniform killing, tau<=1/k_min, is also used. Where it beats the residual upper bound, the reported interval uses it rather than displaying a needlessly worse bound.

## 7. Independently specified model family: growing softened East chain

The softened East model is established prior art [1]. This run uses n transient binary coordinates, an always-facilitated left boundary, and a separate absorbing target flip facilitated by bit n:

    0->1 at site i: q a_i,
    1->0 at site i: (1-q) a_i,
    a_1=1,
    a_i=epsilon+(1-epsilon)x_{i-1},
    killing k(x)=q[epsilon+(1-epsilon)x_n].

The initial law is the analytic product Bernoulli(q) equilibrium over the transient coordinates. The kinetics is hierarchical; the thermodynamic integration is easy. The microscopic local formula and its interaction order are provided to every comparator. No metastable-to-metastable rates, important pathway list, committor or learned favorable coordinate transform is supplied. The physical interaction ordering is known from the model, not discovered from opaque queries.

For q=1/(k^2+1), an equilibrium/contrast basis gives rational local operators

    h=diag(0,1),
    N=(1/(k^2+1)) [[1,-k],[-k,k^2]],

and

    H=h_1+sum_{i=2}^n [epsilon I+(1-epsilon)N_{i-1}] h_i
      +q[epsilon I+(1-epsilon)N_n].

Consequently

    H>=epsilon[q I+sum_i h_i].

The source is the product constant basis vector. The operator has a three-state matrix-product representation constructed directly from its local physical terms. The certificate uses excitation counts j=0,1,2 and bounds the remaining counts collectively.

### 7.1 Dimension variation at fixed gate parameters

All rows use q=1/26, epsilon=10^-4, maximum tensor rank 16, three sweeps.

| n | Microscopic configurations | Stored coefficients | Exact lower | Exact upper | Ratio upper | Recorded solve+check time |
|---:|---:|---:|---:|---:|---:|---:|
| 32 | 4,294,967,296 | 12,968 | 48731.064724447431 | 48745.779385185315 | 1.000301956480 | 5.06 s |
| 64 | 18,446,744,073,709,551,616 | 29,352 | 48731.064724447223 | 48745.779386242872 | 1.000301956502 | 11.42 s |
| 128 | 340282366920938463463374607431768211456 | 62,120 | 48731.064724447223 | 48745.779386242823 | 1.000301956502 | 25.35 s |

This is actual all-state certification without a full state array. It is not a proof that rank stays small in general. Extending the East chain adds coupled upstream coordinates, not strictly inert independent spectators. Spectator count was varied separately in the conditional-bath tests.

### 7.2 Independent rarity failure

At fixed n=32 and q=1/26, changing epsilon from 10^-4 to 10^-6 while keeping rank16/three sweeps gave

    [1180064.290149295520, 26000000.000000000000],
    ratio <=22.032697893698.

The raw residual upper bound was about 4.981e9; the uniform-killing ceiling tightened it to 26e6. This remains a failed precision target. A larger physical lifetime is not proof of a useful computational advance. Earlier severe-gate pilots also retained wide residuals. They are preserved in the packet.

## 8. Continuous gated diffusion: no microscopic move alphabet

This is an **authored continuous East-like diagnostic**, not a published molecular benchmark or a calibrated atomistic system. It was chosen to permit an exact continuum audit of the operation. It is additional evidence, not a replacement for the independent soft-East family.

Let x_i lie in [0,1], rho=alpha+beta, q=alpha/rho, with reference beta density

    pi_i(dx) proportional to x^(alpha-1)(1-x)^(beta-1) dx.

Define a_1=1 and a_i=epsilon+(1-epsilon)x_{i-1}. The generator is

    L f = sum_i a_i [x_i(1-x_i) f_{ii}+(alpha-rho x_i)f_i],

with reversible no-flux endpoint realization. The reaction hazard is

    k(x)=kappa[epsilon+(1-epsilon)x_n],  kappa=rho q.

Equivalently the dimensionless local potential is

    U_i=(1-alpha)log x_i+(1-beta)log(1-x_i),

and mobility is a_i x_i(1-x_i). With alpha,beta<1, the density is endpoint-biased; the potential is singular and mobility degenerate at the endpoints. These features are mathematically well-defined with the chosen reversible realization but are not a claim of a realistic smooth atomistic force field. Polynomial test functions have vanishing weighted boundary flux because alpha,beta>0.

The initial distribution is the analytic equilibrium law. Computing the result uses the model's energy/mobility/reaction coefficients, not equilibrium samples or metastable rates. No force-field parameter inference from experiment was performed.

### 8.1 Exact local polynomial and continuum residual construction

The monic Jacobi polynomials are orthogonal for pi_i. Their moments and eigenvalues are

    E[x^k]=(alpha)_k/(rho)_k,
    lambda_j=j(j-1+rho).

Rational alpha,rho give rational moments, monic coefficients, Gram norms and multiplication-by-x matrices. The latter are tridiagonal. The float optimizer uses an orthonormal basis; the verifier converts to the monic basis and defines exact dyadic trial coefficients there.

A trial of local degree p has an actual H v of local degree at most p+1. Thus the **complete continuum residual** is represented by padding one local degree, not by pretending that the projected residual is the physical residual. No mode above that padded degree is present in H v for this polynomial-coefficient model. All infinitely many other continuum modes still enter the inverse-error estimate through the proven operator minorant.

    H>=epsilon[kappa I+sum_i h_i].

The exact certificate first isolates the subspace of local degrees 0/1. It counts j=0,1,2 excited coordinates there and charges the rest by kappa+3rho. For modes whose largest local degree is m>=2, it charges the denominator kappa+lambda_m. All weights are exact squared norms obtained by tensor masks.

### 8.2 Continuous results and independent parameter changes

q=1/26 and rho=1/10 are fixed. p is the local polynomial degree, maximum tensor rank is8, and each proposed solution uses two sweeps.

| n | epsilon | p | Coefficients | Exact lower | Exact upper | Ratio upper | Recorded solve+check |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 32 | 1/10 | 3 | 7,456 | 2040.9964062499 | 2040.9964096738 | 1.0000000017 | 3.18 s |
| 32 | 1/100 | 3 | 7,456 | 11735.2473695064 | 11740.8172532523 | 1.0004746286 | 3.13 s |
| 128 | 1/100 | 3 | 32,032 | 11735.2473695064 | 11740.8172532523 | 1.0004746286 | 14.97 s |
| 32 | 1/1000 | 3 | 7,456 | 48806.1406466724 | 73358.7919935868 | 1.5030647993 | 3.47 s |
| 32 | 1/1000 | 5 | 11,400 | 49743.1757263996 | 53767.9363414765 | 1.0809108095 | 21.35 s |

These are intrinsic model time units, not seconds of a physical molecule. Computational seconds in the last column are separate from those units.

For the degree-five hard case, a first coarse split that treated every higher mode as if it had eigenvalue lambda_2 gave ratio2.01784. Resolving the maximum-degree weights tightened the ratio to1.08091 **without changing the fitted function**. Most residual energy was in degree6, not in the slowest nonconstant modes. This motivated a certificate refinement rather than blindly increasing the global tensor rank.

The actual continuation spent resources on both degree3 and degree5 runs, and on the earlier coarse certificate. The 21.35s row is not an end-to-end cost that erases those earlier attempts.

### 8.3 Galerkin residual falsification

The three-coordinate degree-two audit gives a projected floating residual squared near numerical zero (small negative values about -5e-14 occur through cancellation), but exact full continuum residual squared0.3622350401445691. Its actual continuum interval is approximately [621.2832588307,627.0148259217]. A nearly exact solve of the truncated equations does not certify the continuum kinetics.

The large-system verifier includes this leakage automatically. It never uses a floating residual value or a convergence report as a certificate.

## 9. Independent spectator and uncertainty variation

The bath-extension theorem (B) was checked against small correlated baths with0,2,4,6 bits while holding the four-gate subsystem and eta=0.05 fixed. Bath flip rate scale was separately reduced from10^-6 to10^-12. All nonzero-eta exact reference intervals were contained in the completion bounds. At eta=0 the two independently computed numerical enclosures overlap; the full reference's residual interval was slightly wider than the gate interval, as can occur even when the true means coincide exactly.

For the 128-coordinate continuous gate certificate, uniform hidden effects in [1-eta,1+eta] imply the following bounds, independent of the number of hidden spectator coordinates:

| eta | Lower (outward at 2 decimals) | Upper (outward at 2 decimals) | Ratio, approximately |
|---:|---:|---:|---:|
| 0 | 11735.24 | 11740.82 | 1.000475 |
| 0.01 | 11619.05 | 11859.42 | 1.020686 |
| 0.05 | 11176.42 | 12358.76 | 1.105788 |
| 0.10 | 10668.40 | 13045.36 | 1.222802 |

The packet evaluates these formulas for bath-coordinate counts0,10,1000,1000000. No such large bath is simulated, integrated, or enumerated; these rows are applications of a uniform theorem. The bounds require the stated global relative effect on gate diffusion/conductance and reaction, not a claimed empirical fact about a particular solvent.

The nonconstant conditional-envelope diagnostics in Section4 additionally permit non-product physical equilibrium weights and distinguish low-impact from high-impact hidden interaction support. Their normalized bath distribution need not be known by the closure compiler.

## 10. Strong comparators and actual computational advantage

### 10.1 A specialized local-window solver is competitive or better

A source-aware tail-window baseline retains only the last w gate bits. In the product-equilibrium soft-East model, replacing the tail's left boundary facilitation by epsilon gives a valid lifetime upper bound. A Galerkin test depending only on the tail uses the average boundary facilitation epsilon+(1-epsilon)q and gives a lower bound. No rapid-equilibration premise for the discarded prefix is needed.

This method explicitly enumerates only2^w states, not2^n, and is a serious competitor. At q=1/26, epsilon=10^-4:

| Window w | Window states | Upper/lower ratio | Recorded construction+solve+exact-check time |
|---:|---:|---:|---:|
| 8 | 256 | 1.02169851 | 0.0264 s |
| 10 | 1,024 | 1.00305125 | 0.1878 s |
| 12 | 4,096 | 1.00035025 | 7.7010 s |

At roughly0.035% interval width, the32-gate tensor run took about5.06s, while the12-bit window took7.70s. The128-gate tensor run took25.35s, so the same window solver was faster. At percent-level accuracy, the window baseline was much faster. These single-run timings do not establish a general or statistically controlled speed ranking.

The real demonstrated improvement over the prior Astra implementation is removal of its compulsory full-state array. It is **not** superiority over every existing non-enumerative method.

### 10.2 Tensor and error-estimation prior art

Quantized/tensor-train chemical master-equation solvers already avoid explicit exponential probability arrays [2,3]. Tensor methods have been used for rare trajectories of East-type models [4]. Functional tensor-train PDE solvers already exploit products of one-dimensional integrals [5]. Tensor reduced-basis methods with a posteriori estimates [6] and functional error-majorant learning [7] are also established. Public MarkovMPS code directly targets tensor-train first-passage statistics [8]. These results preclude claiming that low-rank Poisson solving, high-dimensional factorized integration, or residual validation by itself is new.

The specific priority question is the conditional two-source envelope compilation and its exactly checked source/spectral backend, especially controlling arbitrary unrepresented baths and continuum leakage. The literature search was targeted, not exhaustive. No outside reviewer assessed this claim.

### 10.3 Molecular/path-based competitors

Optimized weighted ensemble already directs trajectories using local first-passage information [9]. TAMMBER already allocates atomistic exploration using uncertainty about missing transitions [10]. Descriptor-free AIMMD combines learned committors and path sampling and reports demanding ligand-kinetics examples [11]. Graph transformation computes finite-network first-passage quantities without waiting for trajectories once network information is supplied [12]. Variational dynamical-disorder bounds and MSM coarse-graining are older related work [13,14].

**No optimized-WE, TAMMBER, AIMMD or real-molecule head-to-head was executed.** A custom weak version of one would not establish comparison with the strongest method. Every future competitor must receive the same local coefficient law/envelopes, initial law, target, accuracy and all training/integration costs. This checkpoint has no measured atomistic advantage.

## 11. Resources, numerical precision, and validity ledger

### Representation and local physical inputs

Discrete experiments receive an explicit local microscopic generator. Continuous experiments receive the actual local differential coefficients and hazard. These are not metastable-to-metastable rates. Their physical accuracy is assumed as part of the model, not experimentally established here. The conditional closure requires global ranges for interaction weights and gate forms; no algorithm for acquiring such ranges for an unrestricted unknown force field is supplied.

All large response calculations use known analytic reference moments. They do not assume affordable arbitrary high-dimensional integration. Extending to an interacting retained equilibrium without a tractable certified contraction remains substantive work. The conditional closure can handle unknown interacting baths but does not magically make its retained-coordinate problems low rank.

### Cost as a function of representation size

For n coordinates, local basis size d and maximum tensor rank r, a stored response has O(n d r^2) coefficients. The local operator has constant bond dimension in the tested chains. The implemented two-site optimizer uses dense local solves whose dimension can be O(d^2 r^2); its worst-case arithmetic can therefore be large (a conservative cubic local-solve bound is O(n sweeps d^6 r^6)). This is not claimed to be an optimized tensor backend.

For a fixed number of spectral masks, contraction costs are polynomial in n,d,r and operator bond dimension. Counting all excitation sectors adds another n-dependent factor; the prototypes use only a fixed small number plus rigorously bounded tails. Exact integer sizes grow with the summed dyadic exponents and rational moment denominators. There is no promised polynomial bound on the rank needed for arbitrary kinetics.

The largest successful discrete representation stored62,120 coefficients and the continuous one32,032. No2^128 state array or128-dimensional quadrature grid was constructed. One-time compiler cost, interpreter startup, output serialization and resource reporting are not hardware-free; timing fields distinguish stages. Large-result times report measured operator assembly when available, solver sweeps and validation. Older discrete timings omit small serialization/export overhead. They do not include all exploratory failed attempts, literature search, software development or tool orchestration. No total energy-use or research-compute superiority is claimed.

### Exact certification versus empirical correctness

The final bounds are based on rational witnesses and integer contractions, subject to the written model/functional assumptions and the correctness of the supplied implementation.4,253 rational audit assertions check small expanded polynomial operators, local Jacobi differential identities, source-matrix residual identities, positive-semidefinite inequalities, Schur source terms and perturbations.20 further exact network tests check mass-changing energy envelopes. Eight small uniform-bath and six nonconstant-envelope references were evaluated with exact rational residual bounds.

This is not independent verification, a formal proof assistant, or experimental validation. Exact numerical arithmetic does not establish a physical force field or historical priority.

### Failures and corrections retained

- Strong-gate tensor trials can have large true residuals despite stable-looking means. Theepsilon=10^-6 discrete run remains broad after applying the best available trivial ceiling.
- The first continuum diagnostic inherited an irrelevant discrete-style float upper-bound field. It was never used for a final certificate; the field is now replaced with an explicit projected-Galerkin-only label. Original pilot logs are preserved and are not authoritative continuum enclosures.
- The first continuum bound grouped all degrees>=2 atlambda_2. Exact maximum-degree masks improved it without refitting. Initial certificate JSON files are retained where available.
- A bath test initially required containment of two different numerical intervals ateta=0, although the exact quantities are identical. The wider reference residual interval need only overlap the tighter gate interval. The test was corrected; all nonzero-eta intervals were contained.
- An attempted optional python-flint install failed due unavailable package-network access. The executed exact backend instead uses system GMP via compiled C++; no missing dependency is hidden.
- One exploratoryrank24 solver invocation exceeded a tool limit before completing its requested sweeps; a shorter completed run was subsequently recorded. It is not counted as an independent successful repetition. Other pilots and their timings remain in the packet.

## 12. Significance and the exact remaining construction

This checkpoint does not meet the full scientific completion standard. It does establish a source-aware conditional closure and working, exactly validated examples where a full microscopic state list is unnecessary. The continuous example also removes the discrete microscopic-rate query interface. The closure is capable of bounding a non-product hidden bath from local interaction and kinetic envelopes without evaluating its equilibrium distribution or internal timescales.

The unresolved physical step is obtaining *tight enough* envelopes for genuinely consequential unknown gates from realistic atomistic information. A known bounded feature can constrain an enormous hidden region. A pointwise force fit cannot exclude a deep unqueried pocket. When the allowed uncertainty lies in the dominant trap, the source-aware closure correctly stays broad; shrinking it by enumerating all states would not satisfy the mission.

The next research target should be the broad dominant-trap closure in Section4, not another large-n weak-interface example. Develop interface constraints that couple source mass and escape conductance rather than separately taking their worst cases. Candidate inputs include locally verified energy-barrier/geometry relations, mobility constraints and multiple physically controlled perturbations. The resulting constraints must be obtainable without metastable-rate measurements or hidden equilibrium preparation and must tighten the two-source response while retaining all unrepresented alternatives.

The second unfinished component is a unified continuous tensor compiler for nonconstantell/u and uncertain interaction operators. The general closure is proved and implemented on a small retained graph; the large exact continuum implementation currently covers the specified analytic model and constant-envelope bath extension, not arbitrary nonconstant molecular envelopes.

The third is a real matched benchmark against optimized WE, TAMMBER, AIMMD and strong tensor/window solvers under one explicit potential/mobility/target specification, with independently varied gate rarity, bath size and model uncertainty. Accuracy must concern the same preparation and reaction observable. A stable prediction or a large nominal state count is not a substitute for this test.

**Retain the objective: determine what unseen regions can contribute to kinetics from physically justified global information, not from an assumption that the learned representation has already found them.**

## References and access ledger

See `SOURCES.md` for exact primary URLs, versions and access scope. The report's proof claims are derived above; citations establish lineage and comparators, not novelty or validation of this checkpoint.
