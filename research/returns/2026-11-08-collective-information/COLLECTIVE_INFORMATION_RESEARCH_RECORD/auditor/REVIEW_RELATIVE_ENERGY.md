# Constructive hostile review: relative-energy collective dynamics

Auditor, 7 November 2026. This review followed the independently frozen auditor report; its bytes remain unchanged. Reviewed principal/RELATIVE_ENERGY_CONSTRUCTION.md version 1, SHA256 e5d8992ca884a7ad2891ff960acda189856420dcc825a97bc09da6e559dd8f95, and initial/principal.md SHA256 5f6ba087a4841711c9eb5842dfc8253bf40c3b5bd77306872db98755e485edbf. Subsequent requested checks cover principal/MASS_METRIC_REPAIR.md, the bitstring writer and the conditional-mixing source repair. No other researchers' initial/working notes were consulted for this review.

## 1. Verdict at the checked scope

The common-metric nonautonomous form estimate, the count-shell fluctuation estimate with volume-independent C_c, the finite-horizon Poisson/Dynkin estimate and the equilibrium-conditioned killed Schur-complement lifetime estimate are mathematically sound at their stated finite-state assumptions. The fixed-control mass-metric extension also has a valid contour proof, including nontrivial kernels. The imported exclusion gap is applicable, but its theorem/section citation needs an exact version correction.

Two constructive extensions are supplied here: an all-horizon changing-energy theorem controlled by total thermodynamic action, and a simpler pin writer which does not need to switch off the collective energy. A relative source-preparation repair for mean lifetimes is valid only with its pointwise source/error and apparatus conditions below.

This is a defensible acquired coarse-dynamics theorem for a special, explicitly engineered model class. The count-energy structure makes conditional equilibrium and conditional averages tractable; fast stirring and a shared finite kinetic dictionary are given physical structure. Strong macro interactions and an exponentially small macro gap are allowed, but this does not establish a general physical closure, generic materials discovery or practical advantage. Existing conditional averaging, exclusion estimates, form perturbation and Schur-complement/capacity machinery must receive direct credit. Novelty remains UNKNOWN.

## 2. Common-metric form lemma: full check

Let A_t,C_t be positive self-adjoint matrices in a fixed Hilbert space, with

|<v,(A_t-C_t)w>| <= d E_Ct(v)^(1/2) E_Ct(w)^(1/2),  d<1.

Then A_t>=(1-d)C_t. Write U_A for forward evolution under -A_t and similarly U_C. Duhamel gives

U_A(T,0)-U_C(T,0)=-integral_0^T U_A(T,t)(A_t-C_t)U_C(t,0)dt.

For h_t=U_A(T,t)^*g and k_t=U_C(t,0)f, h'_t=A_t h_t, k'_t=-C_t k_t. Hence

integral_0^T E_At(h_t)dt=(||g||^2-||h_0||^2)/2,
integral_0^T E_Ct(k_t)dt=(||f||^2-||k_T||^2)/2.

Bounding E_Ct(h_t)<=E_At(h_t)/(1-d), then applying Cauchy–Schwarz to the paired Duhamel integral gives d/[2sqrt(1-d)] ||f||||g||. No commutation, lower positive spectral gap, or control derivative is used. Piecewise continuous matrices and finite switching are covered. The result is an elementary parabolic energy estimate; it is not itself evidence of a new principle.

For common stationary pi, use density evolution in L2(pi), or the adjoint observable propagator with the control ordering made explicit. The operator-norm statement is unchanged. For retained g and arbitrary initial density f, block-diagonal C makes its retained expectation depend only on Pf, so the warmness factor ||f||_2 is legitimate. It does not imply a uniform arbitrary-source TV estimate independent of small pi(x).

## 3. Relative coupling and the local fluctuation calculation

For C=diag(A_00,A_11) in P/Q blocks, the assumption ||QBPf||^2<=C_c <f,PBPf> and A_11>=gamma Q imply

||A_11^(-1/2) QBP A_00^(-1/2)||<=sqrt(C_c/gamma)=d.

Pseudoinverses on positive ranges are legitimate: the displayed quadratic inequality forces QBP to annihilate ker(A_00). The off-diagonal bilinear form has two terms; their scalar products are bounded by d times the two-vector Cauchy–Schwarz inequality. There is no missing factor two.

For the stated count model, conditional measures are independent uniform shells across blocks because all nonuniform energy depends only on retained counts. The exact uniform-shell fact is load-bearing. Local mobility and kinetic multipliers must depend only on spins inside their own block, excluding the central spin, with both neighborhood degree and reverse incidence at most d. Under those assumptions:

- Swapping two sites changes S_r^+ or S_r^- by at most 2(d+1)b'_max. The two central indicators and at most 2d mobility values suffice; overlapping neighborhoods only reduce the count.
- The complete-graph exchange generator with rate one per unordered pair has gap m. Its Dirichlet form has factor 1/2; there are k(m-k) active pairs. Thus Var(S^+)<=L_s^2 k(m-k)/(2m)<=L_s^2(m-k)/2, and analogously Var(S^-)<=L_s^2 k/2.
- The energy multiplier is constant within each shell and at most C_E, so Var(q^+/-)<=V_0 E q^+/-, V_0=C_E L_s^2/(2b'_min).
- Conditional block independence removes cross-block covariance. Correlation of the two signs in one block is handled by Var(X+Y)<=2Var(X)+2Var(Y). The final sum is twice the coarse Dirichlet form, giving ||QBPf||^2<=4V_0 E_coarse(f).

Therefore C_c=2 C_E L_s^2/b'_min is valid and independent of block count and block sizes. This is a useful improvement over ||B||=O(N). The complete graph is used only for the variance proof, not assumed as physical stirring hardware. The actual conditional gap remains gamma=kappa min lambda_graph.

If microscopic mobilities couple across blocks, or if nonuniform internal energies W_r are introduced, these independence/uniform-shell proofs no longer apply automatically. Nonuniform conditional Poincare/concentration and covariance bounds must be derived separately. A mass-metric correction does not repair a missing fast conditional gap or C_c estimate.

The hypergeometric formula is correct for a specified ordered binary pattern: no binomial multiplicity is needed. Each site type has probability (m-k)/m or k/m for its central sign, then the correct conditional falling-factorial probability on the other m-1 sites. Site-specific known multipliers may still be summed, but an O(D_tab) per-block query assumes the declared shared type/multiplier form; arbitrary separately controlled sites cost at least their input/sum work.

### Exact source-version correction

The primary arXiv:0906.1238v3 is *A recursive proof of Aldous’ spectral gap conjecture*, dated 26 June 2009. Its main result is **Theorem 1.2**, not Theorem 1.1; **Corollary 1.3** directly states the exclusion gap consequence. Symmetric exclusion is **section 1.2.3**, not section 4.1.1. Theorem 1.2 gives IP gap = RW gap; the section 1.2.3 inclusions give IP gap <= EP gap <= RW gap for every nonempty/nonfull occupation, hence EP gap = RW gap. Connected finite weighted graphs and rate conventions match the principal construction. Empty/full shells have no Q component. Product independent blocks inherit the minimum gap. These are verified imports, not new exclusion results. Primary: https://arxiv.org/html/0906.1238v3 .

## 4. Finite-horizon Poisson/Dynkin and killed lifetime checks

Let S_t be the slow Markov generator, F the positive fast generator, P the fixed conditional projection and R=integral_0^infinity exp(-sF)Q ds. Write g_t for the backward coarse terminal observable, so g'_t=-PS_tPg_t, ||g_t||_infinity<=1. Set h_t=RS_tg_t. Then Fh_t=QS_tg_t and

g'_t+(-F+S_t)g_t=Fh_t.

Dynkin applied to g and h gives the error as two h boundary terms plus integral of h'_t+S_t h_t, with jump terms when S switches. With tau_F=||R||_infinity bounded by the integrated operator norms, ||S||<=L and total operator variation V_B, this yields the tighter sufficient bound

tau_F [2L+V_B+2TL^2].

Consequently the principal's tau_F[4L+2V_B+6TL^2] is conservative and valid. No global source warmness, macro gap or exponential Gronwall is hidden. The backward equation/control ordering should be retained explicitly. The tau_F bound by (2+log D_max)/gamma follows by integrating min(2,sqrt(D_max)e^(-gamma t)); log D_max<=Nlog2. It is polynomial but not horizon-free at fixed separation.

The learned-rate path-KL calculation is also correct: with qhat/q=1+s and |s|<=eta, -log(1+s)+s<=s^2/[2(1-eta)^2]. Total exit rate R_s gives KL<=R_s T eta^2/[2(1-eta)^2], and a [-1,1] observable costs at most sqrt(2KL)=eta sqrt(R_sT)/(1-eta). If a preparation error is expressed as TV rather than bounded-observable error, its contribution is **2TV** for this observable class.

For a target which is a union of fibers, killed forms are restrictions of the same positive forms to functions zero on the target. Conditional F and P remain valid on the complement. If all transient components reach the target, A_00 and the killed full operator are invertible on their transient spaces. The block inverse identity and relative off-diagonal norm give

(1-d^2)A_00<=S=A_00-A_01 A_11^(-1)A_10<=A_00,

P A^(-1)P=S^(-1).

For the source pi conditioned on the entire transient complement C, the mean is <1,A^(-1)1>_pi/pi(C). Since 1 is retained, the microscopic mean lies between the coarse mean and coarse mean/(1-d^2). Relative conductance accuracy at fixed pi gives the stated factors 1/(1+eta),1/(1-eta). An exponentially large mean does not force exponentially accurate b when this relative form structure is maintained. The equilibrium-conditioned source is an essential qualifier.

## 5. Fixed-control mass-metric repair: accepted proof and remaining scope

Reviewed principal/MASS_METRIC_REPAIR.md, SHA256 94848c7289ad558d537d977bbf63145f2923b6f2b5ad27447f52c18b7f141bf7. Let A,C>=0 be self-adjoint, |form(C-A)|<=d form(A) relatively, ||M-I||<=d<1, B=M^(-1)C. The proposed bound

sup_t>=0 ||exp(-tA)-exp(-tB)||<=8d/(1-d)

is valid in finite dimensions.

For z with pi/3<=arg(z)<=5pi/3, the scalar estimates stated in the principal proof are correct. With H=M^(-1/2) C M^(-1/2), the bound on (zM-C)^(-1) C^(1/2) follows from polar/range factorization, or Douglas' lemma. Since C>=(1-d)A and ker(C)=ker(A), replacing C^(1/2) by A^(1/2) on the right costs (1-d)^(-1/2); adjoints give the left bound. The resolvent identity is exactly

(z-B)^(-1)-(z-A)^(-1)
 =(zM-C)^(-1)[(C-A)-(M-I)A](z-A)^(-1).

The two terms have norms <=d/[(1-d)|z|] and 4d/[3(1-d)|z|], respectively, so the proposed 3d/[(1-d)|z|] is safe.

The Dunford contour must use the **long left arc**, radius 1/t, and the rays at +/-pi/3, closed beyond all eigenvalues by a large right arc. This encloses zero as well as the positive spectrum. The closing contribution vanishes since its real part is positive and large. The small arc contributes at most 2e d/(1-d). The two rays contribute at most [3d/(pi(1-d))]I with I=integral_1^infinity e^(-r/2)/r dr. An elementary bound I<=2e^(-1/2)-e^(-1)<1 follows by splitting at 2 and using 1/r<=1 then <=1/2. The total is below (2e+3/pi)d/(1-d)<8d/(1-d). Nontrivial kernels therefore cause no omitted inverse-gap singularity. At t=0 the difference is zero.

For two reversible chains, C=MB is self-adjoint in L2(pi), with learned conductances pihat(x)qhat(x,y). Thus mass error d_m and rate error d_q give the form constant d_m+d_q+d_m d_q. The birth/death weight reconstruction bound |log(pihat_U/pi_U)|<=8Neta follows from summing <=4eta log-ratio error over at most N count increments, then normalization. It is uniform over the newly supplied **fixed** U. Choosing eta=O(epsilon/(WN)) gives a polynomial accuracy requirement. This repairs frozen-control energy/weight uncertainty; it does not, by itself, cover arbitrary sequences of independently estimated stationary metrics.

A learned-Gibbs-conditioned source has an explicit warmness bound. If nuhat=pihat_U(.|C), then ||nuhat/pi_U||_2<=exp(4Neta)/sqrt(pihat_U(C)). At a fixed number of blocks the learned mass can be computed/sampled; a lower bound on it must remain in the source contract. A TV writing error adds 2TV for bounded terminal observables. For growing blocks, computing the weights may itself be hard.

Relative rate error alone is insufficient if the stationary measure changes. An exact cautionary family is the reflecting path {0,...,N}: true rates are 1 in each direction, learned up/down rates are e^delta/e^(-delta), delta=N^(-1/2). Every edge relative error tends to zero, but invariant weights change from uniform to proportional e^(2delta i). The stationary mean i/N changes from 1/2 to a quantity tending to 1. The mass-metric hypothesis correctly rejects this family, because its total mass error grows exponentially in sqrt(N). Statements about finite precision of energy must therefore use this repair or the finite-time contract, not silently treat every rate error as a common-pi conductance error.

## 6. New constructive extension: bounded total thermodynamic action

This is an elementary moving-metric extension of the principal's energy proof. It supplies a checked theorem for changing U, rather than an assertion that arbitrary thermodynamic switching is free.

### Statement

Let pi_t(x)=w_t(z)rho_z(x), z=phi(x), be positive stationary measures with a **fixed conditional family** rho_z. Assume piecewise C1 time dependence with finitely many jumps, and positive reversible generators A_t=F+B_t. Assume the principal's block-diagonal C_t and relative coupling condition hold uniformly with parameter d<1 in L2(pi_t); the conditional projection is fixed. Write D(d)=d/[2sqrt(1-d)]. Define

K_T=(1/2)integral_0^T max_x[-partial_t log pi_t(x)]_+dt
 +(1/2)sum_j max_x log[pi_(t_j-)(x)/pi_(t_j+)(x)].         (6.1)

The jump maxima are nonnegative for probability measures; they can harmlessly be replaced by their positive parts. If the initial source has W_0=||dmu_0/dpi_0||_2, then for every retained |g|<=1 the microscopic/coarse terminal expectation error is at most

W_0 exp(K_T) D(d).                                      (6.2)

If learned coarse generators at each t are exactly reversible in the same pi_t and have relative conductance error eta<1, an additional W_0 exp(K_T) D(eta) suffices. Initial source/readout/numerical errors add at their actual bounded-observable norms. This last learning clause assumes the true pi_t is maintained exactly; arbitrary estimated metrics need an additional argument, not an appeal to the fixed-control mass-metric theorem.

For Gibbs energies U_t depending only on counts, with fixed beta,

K_T<= (beta/2)integral_0^T osc_x(partial_t U_t)dt
 +(beta/2)sum_j osc_x(U_(t_j+)-U_(t_j-)).                 (6.3)

Thus a family with bounded total thermodynamic action has a horizon-free certificate, even if the dynamics continues for an arbitrarily long time after the last change. Extensive perturbations can make this sufficient bound exponential in N. Repeated bounded-amplitude cycles can make K_T grow with the number of cycles. This is not a claim that such exponential cost is necessary; the bound can be conservative.

### Complete proof

Use the counting-space isometry y_t(x)=p_t(x)/sqrt(pi_t(x)) for forward probability densities. With D_t=diag(pi_t), detailed balance makes

Atilde_t=D_t^(1/2) A_t D_t^(-1/2)

positive self-adjoint, and similarly Ctilde_t. The transformed dynamics is

y'_t=-(Atilde_t+V_t)y_t,
V_t=(1/2)diag(partial_t log pi_t).                        (6.4)

The transformed retained projection has block vector sqrt(rho_z), hence is time independent. Because V_t is constant on each fiber it commutes with that projection. Thus evolution under Ctilde_t+V_t is still block diagonal, and its retained block is exactly transformed coarse evolution. At a measure jump probabilities are continuous and y_(t_j+)=J_j y_(t_j-), where

J_j=diag sqrt(pi_(t_j-)/pi_(t_j+)),
||J_j||=exp(k_j),
k_j=(1/2)max_x log(pi_(t_j-)/pi_(t_j+)).                  (6.5)

The same jump acts in both dynamics and commutes with the retained projection.

Let nu_t=max(0,-lambda_min(V_t))=(1/2)max_x[-partial_t log pi_t]_+, and let K(t) be the cumulative integral of nu plus jump costs. For the forward comparison k_t solving -(Ctilde_t+V_t), the weighted energy identity/inequality gives

integral_0^T exp[-2K(t)] E_Ctilde_t(k_t)dt<=||k_0||^2/2.  (6.6)

Indeed d[exp(-2K)||k||^2]/dt equals -2exp(-2K)[E_Ctilde(k)+<k,(V+nu I)k>], with V+nu I>=0. At a jump its weighted norm cannot increase because ||J_j||<=exp(k_j). Summing the intervals proves (6.6).

For backward adjoint h_t=U_(Atilde+V)(T,t)^*g_T, the same argument in reverse time gives

integral_0^T exp[-2(K(T)-K(t))]E_Atilde_t(h_t)dt<=||g_T||^2/2.  (6.7)

At reversed jumps the adjoint J_j^* has the same norm bound. The relative form condition still yields E_Ctilde(h)<=E_Atilde(h)/(1-d). Duhamel for two systems with identical jumps has only the continuous generator-difference integrals; common jumps introduce no new forcing. Pair it with k_0,g_T. In each integrand, insert the two weights from (6.6)–(6.7); their inverse product is exactly exp(K(T)). Cauchy–Schwarz therefore gives

||U_(Atilde+V)(T,0)-U_(Ctilde+V)(T,0)||
 <=exp(K_T)d/[2sqrt(1-d)].                               (6.8)

The initial transformed density has norm W_0. The terminal vector sqrt(pi_T)g has norm <=1. Since the comparison's retained block propagates only the projected initial density, (6.2) follows. Apply the same estimate to coarse true/learned forms to get the learning clause.

Finally partial_t log pi_t=-beta(partial_t U_t-E_pi_t partial_t U_t), so max[-partial_t log pi_t]<=beta osc(partial_t U_t). For a jump, log(pi_old/pi_new)=beta DeltaU+log(Z_new/Z_old), whose maximum is at most beta osc(DeltaU). This proves (6.3).

### Source, resource and precision limits

This changes the mathematical drive scope, not the physical availability of U_t. One must pay count/field implementation, timing, energy, all control segments and their variation. For bounded K and W_0, selecting d,eta=O(epsilon exp(-K)/W_0) is sufficient. Since d^2=C_c/gamma, the required stirring scales as W_0^2 exp(2K)C_c/epsilon^2, with the actual graph-gap factor. Calibration precision and numerical precision must be selected accordingly. At K=Theta(N), this theorem alone does not establish polynomial total resources. A numerical log(T) algorithm for a frozen generator does not evaluate an arbitrary long, finely switched protocol at log(T) cost.

For the action bound, U_t must be computably specified with a warranted variation majorant. Estimating a continuous uncontrolled function from a finite mesh is not a free action certificate. A wrong unknown energy changes pi_t; the fixed-control mass-metric lemma does not automatically telescope with no accumulated switching cost.

## 7. Preparation repair: direct pinning without switching U off

The principal's original product-pinned-Gibbs writer is mathematically valid in its declared pin-mode Arrhenius model. Its spectral comparison is correct because neighbor-dependent b_i is unchanged by flipping the central spin. The stated time actually gives mixing TV<=zeta/8 under its pi_min bound, so the looser zeta/2 claim is safe. The target product Gibbs wrong-string probability is <=zeta/4. A global throttle [2cosh(betaH)]^(-1) keeps the maximum flip rate bounded and rescales the gap to at least b_min, if that extra clock-control range is available.

A stronger direct argument removes the Uoff operation and does not use global spectral mixing.

### Direct drift writer theorem

Let a target bitstring s be given. Pause stirring, keep the original possibly unknown/nonconvex count energy U with every one-spin increment bounded by J, and add on-site pin energy -H sum_i s_i sigma_i using +/-1 spin notation. Assume the same neighbor-dependent mobility law, b_min<=b_i<=b_max, continues to hold in this pin mode. Wrong bits then correct at rate at least

A=b_min exp[beta(H-J/2)],

and correct bits become wrong at rate at most

B=b_max exp[-beta(H-J/2)].

Let W(x)=number of wrong bits. Pointwise application of the generator gives

L W <= NB-(A+B)W,

so for any initial microscopic state or distribution,

E W_t <=N exp[-(A+B)t]+NB/(A+B)
       <=N exp(-At)+NB/A.                               (7.1)

Choose

H=J/2+(2beta)^(-1)log[4N b_max/(zeta b_min)],
t=A^(-1)log(4N/zeta).

Then B/A=zeta/(4N) and P(X_t !=s)<=E W_t<=zeta/2. This proof holds despite correlations, arbitrary nonconvex collective interactions and unknown actual U inside its increment bounds. No assumption about a pinned global gap or microscopic equilibrium sampling is used.

The maximal total flip rate is <=N b_max exp[beta(H+J/2)]. Dividing by A shows the expected event exposure before the writing time is <=

N(b_max/b_min)exp(beta J) log(4N/zeta).                    (7.2)

A hard event cap can be set by Poisson domination using the actual maximal rate and time. Pin switch work is bounded by O(NH) at either switch in the ideal spin-energy model; recording a thermodynamic heat/work claim still requires the apparatus/bath accounting.

Optionally throttle every pin-mode rate by exp[-beta(H+J/2)]. Then every single-site rate is <=b_max, the correction lower bound becomes b_min exp(-betaJ), and the required time is

t'=exp(betaJ)b_min^(-1) log(4N/zeta).                      (7.3)

The same distributional guarantee holds. This throttle is an additional writer-mode kinetic-control range; the original target-mode fixed a_min does not grant it. Its actual dynamic range, leakage and implementation cost must be supplied. A field of logarithmic magnitude suffices for ordinary inverse-polynomial write error, while exponential write accuracy below requires linearly growing fields.

### Relative lifetime source: valid with exact target-set semantics

Let C be the **entire non-target transient set**, target D=X\C, and nu=pi(.|C). Suppose ideal strings are drawn from nu and the conditional writer outputs the requested string with probability >=1-delta uniformly for every requested string. For any i in C, the actual mixture mu satisfies

(1-delta)nu(i)<=mu(i)<=nu(i)+delta.

If delta<=zeta nu_min with nu_min=min_(i in C)nu(i), then (1-zeta)nu(i)<=mu(i)<=(1+zeta)nu(i). Since tau_D=0 outside C and tau_D>=0 everywhere,

(1-zeta)E_nu tau_D<=E_mu tau_D<=(1+zeta)E_nu tau_D.       (7.4)

No arbitrary-TV stability of a huge mean was used. If C is only a selected subwell while its complement contains other non-target transient states, declaring all outside-C errors to have lifetime zero is invalid. Postselection on C is a different source and carries a normalization/detection correction.

For the count-energy model with |Delta U|<=J, osc(U)<=NJ along the hypercube. Therefore on any nonempty C, nu_min>=exp[-N(log2+betaJ)]. A one-block ideal draw uses N+1 known count weights followed by a uniform string at the sampled count. Choosing delta<=zeta exp[-N(log2+betaJ)] needs H=O(N+log(1/zeta)), and the throttled writer time is O(N+log(1/zeta)) at fixed beta,J,b bounds. The event bound and pin-switch energy are polynomial. This is a real stronger control contract, not fixed maximum field hardware.

The error guarantee includes **all** uncontrolled write-failure channels. An unknown fixed reset-error or stirring-leak floor cannot be removed by statistical readout repetition. The polynomial conclusion is conditional on the declared pin/throttle/noise mechanism implementing these rate and leakage bounds at polynomial actual cost. The energy barrier formula warrants exponentially small thermal wrong flips inside that model; it does not empirically certify every unknown apparatus error to exponential accuracy from polynomial trials.

### Nonuniform conditional source via native mixing

For a finite reversible count-conserving conditional chain with stationary mu_k and gap gamma,

|P_t(x,y)/mu_k(y)-1|
 <=exp(-gamma t)sqrt[(1/mu_k(x)-1)(1/mu_k(y)-1)]
 <=exp(-gamma t)/mu_min.                                 (7.5)

This is the spectral-gap Cauchy–Schwarz bound on centered point-mass densities. Hence t>=gamma^(-1)log[1/(zeta mu_min)] gives a uniform pointwise relative conditional error <=zeta, from any microscopic initial law in that shell. It is polynomial when the gap inverse and log(1/mu_min) are polynomial. For many independently mixed blocks allocate relative errors so their sum/product remains controlled, or use a global minweight/gap bound. A possible exponentially slow conditional Kawasaki gap is not repaired by the logarithm. Counts must really be conserved during this stage; flip/stir-switch leakage is an additional error channel.

## 8. Optional constructive removal of supplied one-block count energy

This is an additional checked operation within the same clamped finite-state kinetic model, not a claim about generic Hamiltonian learning. It addresses the concern that precise macro stationary weights were supplied. It requires the stronger clamps/pins and noise budgets already discussed.

For one block of N spins, leave one central spin free and hold all others in a specified bitstring with rest count k. Pause stirring. For a fixed neighbor pattern the central chain has rates

r_+=b exp[-beta DeltaU(k)/2],
r_-=b exp[+beta DeltaU(k)/2].

Starting the central spin in each sign and observing a common duration h gives transition probabilities

p_01=r_+/(r_++r_-)[1-exp(-(r_++r_-)h)],
p_10=r_-/(r_++r_-)[1-exp(-(r_++r_-)h)].

Therefore at any h>0,

DeltaU(k)=-beta^(-1)log(p_01/p_10),
r_++r_-=-h^(-1)log(1-p_01-p_10),
b=sqrt(r_+r_-).                                         (8.1)

There is no finite-difference derivative or multiple-jump truncation. The same neighbor mobility cancels in the forward/backward probability ratio. If a known kinetic multiplier is present, divide it out with its actual accuracy/conditioning.

Let C_E=exp(betaJ/2), h=1/(4b_max C_E). Then r_++r_-<=2b_max C_E and

p_01,p_10>=p_min:=b_min exp(-1/2)/(4b_max C_E^2),
1-p_01-p_10>=exp(-1/2).

These bounds follow by integrating a first transition with no later transition, or directly from the formulas. Thus inversion is uniformly conditioned at fixed declared parameters. With corrected binary readout contrast v, simultaneous probability accuracy alpha costs O(v^(-2)alpha^(-2)log(N/delta)) trials per direction/count. For alpha<=p_min/2, the increment error is at most 4alpha/(beta p_min). Acquiring all N increments to error epsilon_U/N and summing from the gauge U(0)=0 gives sup_k|Uhat(k)-U(k)|<=epsilon_U, using

O(N^3 v^(-2) beta^(-2)p_min^(-2)epsilon_U^(-2)log(N/delta))

shots. Each shot pays its N-spin writing/clamping/reset and h; this increases physical operation cost by the actual preparation cost, ordinarily at least O(N). A fixed unknown clamping/readout/timing bias must be below alpha; it is not averaged away. Other spins must really remain pinned, not merely have the correct initial count. Pins of logarithmic size can make their unwanted event probability over h polynomially small under the declared rate model. This source/clamp validity is a real apparatus premise.

This acquires a size-N count-energy table. It does not transfer unknown U_N to a new size without a specified shared energy family. A new supplied count perturbation V(k) may be added after acquisition; the absolute baseline potential error remains the same for every such fixed V, subject to its actual physical implementation and increment bounds.

### Relative mean-lifetime robustness with imperfect stationary weights

Here is a direct elementary comparison which does not require exact pi in both learned models. Let pi,pihat be reversible probability weights on the same transient state set C and full target graph, with

exp(-s)<=pihat_i/pi_i<=exp(s),
1-eta<=qhat_ij/q_ij<=1+eta.

For killed generators write K=D_pi A and Khat=D_pihat Ahat. These are symmetric positive-definite Dirichlet matrices. Conductance comparison gives

e^(-s)(1-eta)K <= Khat <= e^s(1+eta)K.

Their inverses have the opposite quadratic-form bounds. Khat^(-1) is entrywise nonnegative because it is a killed Green kernel times a positive diagonal. Let r=pi restricted to C and rhat=pihat restricted to C. The equilibrium-conditioned means are

m=r^T K^(-1)r/pi(C),
mhat=rhat^T Khat^(-1)rhat/pihat(C).

Entrywise rhat/r between e^(-s),e^s costs at most e^(+/-2s) in the positive Green-kernel quadratic form; denominator comparison costs one more factor e^(+/-s), and inverse-form comparison another. Hence

e^(-4s)/(1+eta) <= mhat/m <= e^(4s)/(1-eta).             (8.2)

For a uniform potential error epsilon_U, normalized Gibbs log-mass error is at most s=2beta epsilon_U. Local rate error from that potential and a relative mobility error eta_b is also controlled: eta can be taken as max((1+eta_b)e^(beta epsilon_U)-1, 1-(1-eta_b)e^(-beta epsilon_U)). Thus polynomial energy/mobility accuracy gives relative lifetime accuracy even if m is exponentially large. This comparison is separate from the all-horizon semigroup mass-metric result.

For the actual microscopic process, also include the principal's 1/(1-d^2) Schur factor. If the written physical source is pointwise within (1+/-zeta) of learned pi(.|C), its relation to the true pi(.|C) costs e^(+/-2s). A conservative complete bracket for physical mean M_phys versus learned coarse mhat is

(1-zeta)(1-eta)e^(-6s)
 <=M_phys/mhat
 <=(1+zeta)(1+eta)e^(6s)/(1-d^2).                         (8.3)

The source and target-set qualifications of section 7 apply. This removes a supplied exact energy from the one-block lifetime operation at explicit polynomial acquisition cost, but still assumes the special count-energy kinetic family and clamp/pin mechanism. No generic material or unknown spatial interaction is covered.

## 9. Physical and computational accounting that must remain explicit

1. Arbitrary efficiently evaluated U(k) is not automatically a naturally available local material Hamiltonian. Physical realization may need all-to-all couplings, global count readout/feedback or an external controller. Charge its actual count communication, field work, update/holding time and precision. A supplied polynomial evaluator is a computational input, not proof of polynomial physical realization.
2. Pausing stirring, clamping neighbors, initializing central signs, changing target energy and applying writer fields are actual interventions. The target-mode law does not itself grant these calibration/writer modes. Pin/throttle bounds above provide a concrete sufficient contract; unknown fixed systematic bias remains a floor.
3. Calibration from U=0 must set a known multiplier, preferably a=1. If a=1 is outside the hardware range, calibrate a known a_0 and divide it out with its lower bound and precision. The two-state inversion otherwise estimates b a_0 rather than b.
4. All-horizon relative-conductance confidence is uniform only because the same learned neighbor table is reused in both directions and for all declared controls. Rounding each directed rate independently can break that structure. Numerical evaluation should synthesize rates from the same stored positive table/potential, with certified precision. Unknown physical energy error needs mass/energy control, as in sections 5 and 8.
5. Scaling/squaring for a fixed finite coarse matrix can have polynomial log(T) arithmetic: use a stochastic base-step approximation, choose its error O(epsilon/2^s), s=O(log(R_sT)), and propagate positivity. This needs O(log(T/epsilon)) arithmetic bits and actual input-function evaluation precision. The original elementary readout samples need not be re-acquired to those numerical bits: a chosen learned estimator is a mathematically defined real/computable number. This does not turn a general many-block matrix or switched drive into a cheap object.
6. For many retained blocks the full state space is exponential. Ordinary coarse Monte Carlo of bounded final observables is a legitimate polynomial-in-T evaluator, with count-energy and sampling costs paid; it is not a polynomial-in-log(T) rare-event solver. The one-/fixed-block lifetime calculation is the tractable consequence actually supplied.
7. The equally informed incumbent knows the same count-energy structure, local table, stirring and source controls. It can perform ordinary conditional averaging, hypergeometric rate synthesis, birth/death formulas or coarse kinetic Monte Carlo. The present construction has not established an advantage over that incumbent. A direct comparison to uninformed microscopic brute force would not settle this.

## 10. Primary competitors and exact scope

**Hilder–Sharma, arXiv:2201.10256v2**, Theorem 3.1, already gives a uniform-in-time relative-entropy coarse-graining bound under a uniform conditional log-Sobolev inequality; its constant C(L,N,rho) is time independent. The constant-independent-of-effective-generator alternative is only stated on fixed [0,T]. Remark 3.2/3.9 and Theorem 4.5 explain the time/initial-positivity tradeoffs. Lemma 4.9 and Corollary 4.10 identify averaged/effective dynamics in the reversible setting. Therefore horizon-uniform conditional averaging itself must not be advertised as unprecedented. The principal's explicit relative-energy constants, nonautonomous common-pi control and volume-independent local C_c are the exact features to compare, not a generic first all-time bound. Primary: https://arxiv.org/html/2201.10256v2 .

**Blassel, arXiv:2610.36078v1**, Definition 3 and Theorem 5, already gives uniform-in-time non-asymptotic killed-process/conditioned-flow coarse-graining under orthogonal-semigroup scale separation, compatibility and quasi-stationary structure, including nonreversible processes. Its canonical projection uses the QSD; Theorem 5 assumes decay rate zeta>2(lambda^X+gamma^X), with explicit prefactors carrying slow spectral quantities, closure defects and initial-source information. It also studies data-driven diagnostics with a specified synthetic training prior and physical numerical tests. It does not give this count-shell kinetic-table acquisition or free QSD discovery. Conversely, the principal's unconditioned equilibrium-source mean lifetime comparison is not a replacement for all of its QSD/exit-event statements. Primary: https://arxiv.org/html/2610.36078v1 .

**Caputo–Liggett–Richthammer v3** is checked in section 3 above. The common-metric energy lemma, the mass-metric analytic-semigroup estimate and Schur complement belong to established functional-analytic/Markov machinery unless a focused priority search proves otherwise. No primary-source import in this review supplies an unproved general physical gap, source or apparatus efficiency.

## 11. Independent diagnostics and status

checks/check_multiblock_relative_energy.py is an independently constructed two-block, six-spin test (64 microscopic states, 16 retained count states), with nonzero count coupling -0.09 s_1 s_2, two mobility types, nonconstant neighbor patterns and changed count energies/kinetic drives. It checks detailed balance, the exact hypergeometric generator, actual relative coupling and the C_c bound, plus a switched-energy action certificate. All checks pass. At kappa=100000, actual C_c is 0.2276–0.2464 versus conservative analytic bounds 705.5–1290.9; actual d is at most 0.00090617. Hypergeometric error is <=8.9e-16. For its three-segment energy protocol, K=0.391357 and all-bounded-observable discrepancy is 9.39e-9 versus action certificate 0.0006705. These are synthetic finite diagnostics, not hardware evidence, infinite-size verification or priority evidence.

The finite-test implementation initially had an extra shell-size normalization in a diagnostic coarse Dirichlet matrix; correcting it to the indicator pullback R D_pi B R^T made that independent diagnostic consistent. This was a test-code normalization issue, not a change to the analytic model or a suppressed scientific counterexample.

The core proofs and additional statements in this review are marked checked at their explicit mathematical assumptions. Actual physical apparatus performance, a broader material class, priority and an equally informed practical advantage remain unestablished. The strongest justified continuation is to derive nonuniform conditional gaps/averages and calibration from a genuinely different physical class, or close a consequential matched-cost use of the present one; polishing this tractable mechanism alone does not resolve the broad research objective.


### Final independent targeted checks and primary pin

checks/check_mass_metric_and_writer.py passes 168 rank-one mass-metric cases, retaining an exact kernel and positive scales from 1e-100 to 1e100. The maximum observed error/certificate ratio is 0.06242. This is a stress diagnostic for the proved contour estimate, not proof of it.

The same independent script constructs a six-spin, two-block coupled count energy with the original interaction retained and an alternating target string. It verifies the generator drift inequality pointwise and uniformizes the full chain to test every initial microscopic state. At zeta=.05, the worst-source wrong-string probability is 0.0016542124, below the first-moment certificate .025. The optional throttled total exit bound is 3.633334 and its duration 39.52713. No physical trial was performed.

The Caputo citation correction was also checked against the principal's actual cached primary PDF sources/caputo-0906.1238v3.pdf: 23 pages, SHA256 64f1f657dd2935c86f27fc25d202d8b6249d2f915d551f2d14a9ecf3a2c8fb71. Its Theorem 1.2, Corollary 1.3 and section 1.2.3 match the correction above. Other primary HTML pins are in source/RELATIVE_ENERGY_SOURCE_MANIFEST.json.
