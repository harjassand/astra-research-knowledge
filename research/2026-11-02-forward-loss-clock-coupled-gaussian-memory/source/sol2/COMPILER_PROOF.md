# Forward contraction / loss-clock compiler for a coupled passive bosonic memory

Status: a new single-worker derivation and constructive existence claim. It is not an independently audited result, a historical-priority conclusion or an executed fault-tolerant circuit. The frozen first return is unchanged. This proof addresses the complete retained-memory operation rather than additional interpolation nodes.

## 1. Exact input/output contract

There are M retained bosonic modes b=(b_1,...,b_M), initially in vacuum. Their specified passive Markovian dynamics has one-particle Hermitian H and loss matrix E=[e_1,...,e_r], with

    A=-iH-EE^dagger/2,  L_mu=e_mu^dagger b.

All entries are known finite classical descriptions with paid precision. A may be nonnormal, H may mix modes arbitrarily, and EE^dagger may have rank one or a kernel. No simultaneous diagonalization, positive damping per coordinate, global system mixing gap or spectral gap of A is assumed. Let R>=1 bound ||A|| and ||EE^dagger|| (a bound from matrix entry sums suffices).

A finite-dimensional system interacts through

    D=H_S+V,
    V=sum_j Q_j(c_j b+b^dagger c_j^dagger),

where Q_j are bounded Hermitian system operators and may fail to commute with each other or H_S. Actual precision-capable controlled block-encoding circuits for H_S and Q_j are inputs, with their actual normalizations h and q_j and their gate/selection costs paid. Put a=sum_j q_j||c_j||. A norm promise without access is insufficient. The system state may be entangled with an arbitrary reference. System instruments at prescribed times may be added with their actual costs. The bath and emitted records remain private.

The desired operation is the complete system channel up to finite T, to prescribed diamond error epsilon, retaining the quantum bath memory between interactions and controls. We first compile the exact finite total-occupation cutoff N<=K, with integer K>=1, and then pay the first-stage infinite-Fock cutoff. H_S is time independent within each control-free interval; efficiently encoded time-dependent operators require an additional stated temporal approximation bound.

Apart from the actual supplied system-access costs, the claim derived below is polynomial gate/workspace cost in M,K,hT,aT,input lengths and log(1/epsilon), with only logarithmic dependence on R and known frequency/rate magnitudes. A whole polylogarithmic inverse-accuracy bound requires those supplied precision-capable system circuits to have at most polynomial logarithmic precision cost; otherwise their actual cost remains in C_D. This is stiffness removal, not optimality in T or K. It does not give an experimental device, thermal heat records, an unknown measured spectrum or arbitrary public bath access.

## 2. The free no-jump contraction is explicitly implementable

On the cutoff space, the free no-jump generator is

    G0=dGamma(A)=b^dagger A b,
    B(t)=exp(G0 t)=Gamma(F(t)),  F(t)=exp(At).

Since A+A^dagger=-EE^dagger<=0, ||F(t)||<=1 and ||B(t)||<=1. Gamma denotes bosonic second quantization, restricted to N<=K. It obeys ||Gamma(F)-Gamma(F')||<=K||F-F'|| for contractions, by telescoping F^tensor n on each n-particle sector.

This is a BLOCK construction, not an assumed dissipative inverse. For any contraction F form its one-particle Julia unitary

    U_F=[[F,sqrt(I-FF^dagger)],
         [sqrt(I-F^dagger F),-F^dagger]].

Second-quantize U_F on the M data modes and M fresh vacuum modes. Projecting the latter modes onto vacuum gives exactly Gamma(F). In a product of contraction blocks every fresh vacuum/failure register is retained through the entire coherent word and amplification; no discarded free-loss channel is substituted. A non-vacuum inner loss flag is a block failure, not an actual emitted-field event. Arbitrary unitary extensions on unused encoding states are allowed.

The one-particle matrix F and a decomposition of U_F into O(M^2) bounded-angle mode rotations can be computed reversibly from the supplied M-by-M matrices and the finite time word. Contractivity allows scaling/squaring with polynomial guard bits in log(1+Rt) and the requested absolute error: scale ||At|| below1, approximate there, then square. An initial error O(delta/2^s) suffices after s=O(log(1+Rt)) squarings. Large damping does not require an exponentially accurate relative value of an exponentially small entry. A computed F' can be divided by1+delta to enforce contractivity after an absolute delta error; Gamma's error remains O(K delta).

Each two-mode rotation is a bounded-angle evolution under a two-sparse number-preserving beam-splitter Hamiltonian. On total occupation<=K its norm is O(K); its row locations and sqrt[(n_i+1)n_j] weights are computed by reversible arithmetic on the binary occupation registers. Explicit weighted ladder-shift block encodings have normalization O(K). A segmented Taylor-LCU Hamiltonian simulator (or standard sparse/qubitized simulation) therefore gives a concrete cost O~(K) per bounded-angle rotation, rather than an unexplained Gaussian gate oracle. Finite angle words can be applied by binary controlled fixed-time rotations, with every time bit and synthesis call paid; no coherent arbitrary-duration oracle is assumed. The resulting free-block gate cost is O~(M^2 K) plus polynomial-size reversible small-matrix arithmetic. Occupation, time and arithmetic registers have polynomial size in M, log(K), input lengths, log(1+RT) and log(1/delta). No table of (K+1)^M states, 2^B times or K distinguishable photons is stored.

On unused states with combined data/fresh occupation>K the circuit can act as any explicitly chosen unitary extension. This leaves the signal block on the intended N<=K input exact and makes all inverse/amplification calls well defined.

## 3. A stiffness-free loss clock, acquired from a finite matrix

Define the stacked physical jump operator Jcal=column_mu L_mu and the scalar

    f(t)^2=||E^dagger F(t)||_F^2,
    J(t)=integral_0^t f(s)^2 ds
        =tr[I-F(t)^dagger F(t)] <= M.

The last equality follows by differentiating tr(F^dagger F). It is a trace over the M one-particle modes, not the exponentially large Fock space.

The exact intertwining identity

    a(v)Gamma(F)=Gamma(F)a(vF)

gives, on N<=K,

    ||Jcal B(t)|| <= sqrt(K) f(t).

It also constructs this normalized jump block. For v_mu(t)=e_mu^dagger F(t), prepare the color state with amplitudes ||v_mu||/f; rotate v_mu/||v_mu|| to one mode; block-encode its annihilator by amplitude sqrt(n/K) and a reversible decrement; rotate back; then apply Gamma(F) on the remaining particles. The output color is retained. This gives Jcal B(t)/(sqrt(K)f(t)) without a normalization proportional to ||E||. Zero or negligible components are zero-selected with an absolute allocated error, never resampled conditionally.

This is the load-bearing structural bound. Replacing f by ||E|| would reintroduce stiffness; taking a trace over the full Fock dimension would introduce an exponential memory cost.

## 4. No-jump propagation under noncommuting interaction

Let K0(t)=exp[(G0-iD)t]. It is a contraction because the Hermitian part of its generator is -sum L_mu^dagger L_mu/2. On N<=K use the explicit normalizer

    v=1+h+2a sqrt(K+1),  tau<=1/v.

Forward Dyson expansion gives

    K0(t)=sum_{k>=0}(-i)^k integral_{0<t1<...<tk<t}
      B(t-tk)D B(tk-t{k-1})...D B(t1) dt1...dtk.

Its kth contraction-word norm is at most (vt)^k/k!. Hence the tail after order q is <=sum_{k>q}(vt)^k/k!, independent of R. For vt<=1, q=O(log(1/delta)) is already sufficient; the usual factorial refinement gives log/loglog scaling.

The positive LCU coefficient sum is <=e<4. Prepare order weights (vt)^k/(4 k!), prepare k uniform finite time words, sort them reversibly while retaining permutation/seed labels, and SELECT the chronological product of B and D/v blocks with the exact phase (-i)^k. Left and right use the SAME seed basis; all inner word/failure work is retained until it is coherently unprepared. A zero-selected padding arm completes normalization4. Thus K0(t)/4 is acquired, not supplied.

A grid with 2^B cells is prepared in B qubits. Ordered-uniform cubature is justified by coupling each continuous uniform to its grid representative. Sorting is Lipschitz; derivatives of the free factors are bounded by KR. A polynomial-in-q times KR times the cell width bounds the word error. Thus B=polylog(R,K,1/delta) suffices; there is no loop over the number of resolved time cells. Time ties are allowed and the ordered word has a continuous limit. The source is defined uniformly for coherent finite durations t<=tau.

## 5. The first physical jump: cross time sources earn normalization

Duhamel yields the exact stacked amplitude

    Jcal K0(t)=Jcal B(t)-i integral_0^t Jcal B(s)D K0(t-s) ds.

For the convolution, use two DIFFERENT coherent time states on the SAME time-index basis: the left state has density f(s)^2/J(t), and the right state is uniform on[0,t]. SELECT uses the contraction product

    [Jcal B(s)/(sqrt(K)f(s))] [D/v] [K0(t-s)/4].

The row/column overlap is exactly

    integral_0^t Jcal B(s)D K0(t-s)ds / [4v sqrt(K t J(t))].

Attenuation by sqrt[J(t)/M] converts its denominator to 4v sqrt(KMt). This is a Cauchy-Schwarz SOURCE CONSTRUCTION, not a favorable L1 normalization assumed to be accessible. It only uses J(t), explicit vector annihilation, the already acquired no-jump block and coherent state preparation detailed below.

Set beta0(t)=sqrt(K)f(t), beta1(t)=4v sqrt(KMt), and

    w(t)^2=2[beta0(t)^2+beta1(t)^2]
          =2K f(t)^2+32K v^2 M t.

Then beta0+beta1<=w. A two-term LCU with coefficients beta0/w and beta1/w (and a zero-selected padding arm) implements Jcal K0(t)/w(t), with the -i interaction phase included in the second term. If J(t)=0 the convolution is zero. If J(t)<=M eta^2, omitting it changes the normalized block by at most eta because its explicit attenuation is <=eta; no rare normalizer is invoked.

The enclosing event mass is elementary:

    W(t)=integral_0^t w(s)^2 ds
        =2K J(t)+16K v^2 M t^2,
    W(tau)<=18KM.

All physical jump colors are retained in the amplitude, so the construction is valid for dense/multiple correlated losses too.

## 6. Complete first-event isometry and amplification

For arbitrary system/Fock/reference input the exact first-event map is the isometry

    V_tau psi=|none> K0(tau)psi
       +sum_mu integral_0^tau |jump,t,mu> L_mu K0(t)psi sqrt(dt).

Its completeness follows by integrating

    d[K0(t)^dagger K0(t)]/dt
       =-K0(t)^dagger sum L_mu^dagger L_mu K0(t).

Choose a known power of two A0 with

    sqrt(16+18KM)<=A0<2sqrt(16+18KM).

Prepare no-event outer probability16/A0^2, event time density w(t)^2/A0^2, and the remaining zero-selected padding probability. Controlled inner blocks from Sections4-5 yield the good block V_tau/A0. The outer kind/time/color labels are retained; only INNER source work is unprepared. This is the emitted-field bookkeeping: actual orthogonal output-field times/colors survive coherently until the complete isometry is amplified. No arbitrary interval dilation has been traced out and reintroduced in an inconsistent basis.

The success amplitude is the input-independent1/A0 because V_tau is an isometry. Let qA=ceil(A0), theta=pi/(4qA+2), and attenuate the good block by A0 sin(theta)<1. qA standard oblivious Grover iterations then amplify the IDEAL complete isometry exactly. For an approximate block, the usual rectangular-block Chebyshev bound controls its good-block error polynomially in qA times the base error; unitarity controls failure leakage by its square root. The accepted algebra in N1510 can be received at this precise complete-isometry interface; its independent-mode SOURCE is not received here. For a conservative finite construction, taking base block error delta <=[epsilon/(10^6 S(A0+1)^2)]^4 leaves ample slack. This costs only additional logarithmic precision, not a reciprocal rare-branch probability.

After complete amplification, the private outer time/color may be measured, retained or discarded as an ordinary quantum-jump record. The physical Fock state is retained, including all no-jump coherences and system entanglement. The output field is never fed back into the system, so reading this private orthogonal record is a valid unraveling for arbitrary subsequent system controls. Crucially, the good output of every INNER free block is the SAME vacuum under every coherent time partition; there is no duration-dependent one-photon basis to align. The explicit counterexample in DILATION_FAILURE.md shows why tracing an arbitrary free-channel dilation earlier would have been incorrect.

## 7. The time sources are explicit finite circuits

For a B-bit grid of[0,t], the left convolution time probabilities are

    p_j=[J(t(j+1)/2^B)-J(t j/2^B)]/J(t),

and the right probabilities are2^-B. For a binary prefix specifying an interval[a,b], its exact mass is [J(b)-J(a)]/J(t). Compute these masses reversibly from the M-by-M matrix exponential, then use the two child masses to perform a controlled rotation. One conditional arithmetic computation per level prepares the whole amplitude state; it does NOT enumerate2^B leaves. The outer source uses the equally explicit cumulative mass W(t)=2KJ(t)+16Kv^2Mt^2 and its interval differences. Color distributions use explicit finite vector norms. Order/time sources in Section4 are uniform or factorial lists of length q.

Small prefix masses are paid absolutely. At depth at most B there are at most2^B prefixes. Declaring any prefix of probability below eta^2/[100B2^B] arbitrary loses total probability at most eta^2/100 per level allocation. All other conditional ratios can be computed to uniform rotation error O(eta/B) using absolute mass precision polynomially smaller than that threshold. The required bit precision is O(B+log(B/eta)); the reversible circuit evaluates only the currently addressed prefix. Clipping and normalizing finite approximations gives genuine distributions. The same uniform bound applies when the duration is in a coherent time register.

Exponentially small f values are not evaluated relatively for free. In the convolution, omit J<=M eta^2 using its explicit attenuation. Otherwise retain only time-prefix masses above the preceding finite threshold. On a retained cell f^2 is bounded below by its mass divided by the cell width, up to exp(O(R Delta t)); this supplies a polynomial-in-2^-B lower bound and hence O(B+log(1/eta)) guard bits. In the direct term, omit beta0/w<=eta; when it is retained and t>=t0, w>=4v sqrt(2KM t0) supplies the corresponding lower bound for f. No running time is proportional to Rt just to resolve a vanishing vector.

For quadrature, f is log-Lipschitz: |f'|<=R f because (E^dagger F)'=(E^dagger F)A. Replacing f on one cell by its RMS changes it by a relative exp(O(R Delta t))-1. The normalized free-jump block is also Lipschitz with bound O((K+2)R), using the explicit intertwining construction. Thus the cross-source cubature needs logarithmic time bits, not a number of operations proportional to R.

For the outer clock retain its common L2 time coordinate; a finite cell is embedded as its normalized indicator. The small initial strip[0,t0] has actual jump isometry norm at most sqrt(K||E||^2 t0), and can be zero-selected at this paid cost. Choose t0 polynomially small in delta and1/(1+KR). On[t0,tau],

    |d log w/dt|<=R+1/(2t0),
    ||(Jcal K0)'||<=sqrt(K)||E||(KR+v).

These provide an explicit polynomial bound on the L2 clock error for a sufficiently fine finite grid. Consequently B=O(polylog(M,K,R,v,1/delta)) suffices. There is no assumed minimum physical waiting time. Continuous and discrete public timestamps are not compared in total variation; the private Kraus amplitude is compared on a common L2 space.

## 8. Actual emission count: a rate-independent global cap

Add a classical emitted-count register C. On the exact finite-K joint process, passive free evolution and actual lowering jumps conserve N+C. Only V changes it. Let M_k(t)=E[(N+C)_k]. The same weighted Cauchy-Schwarz as in the first-stage occupation proof gives

    d M_k/dt <=2k a sqrt(M_{k-1}M_k),
    M_k(t)<=(at)^(2k),
    E exp[s(N+C)]<=exp[(aT)^2(e^s-1)].

The jump part now cancels EXACTLY in a function of N+C because each counted lowering jump decreases N and increases C by one. H_S and number-preserving H commute with it. This proves, rather than assumes, a rate-independent bound for the ACTUAL emitted count. In particular, with lambda=(aT)^2,

    P(C>Jmax)<=exp[lambda(e-1)-Jmax].

Take Jmax=ceil(lambda(e-1)+log(100/epsilon))+1. Compare to the exact finite-K process frozen after this many actual jumps; never assume this MGF for the approximate implementation. An overflow has an unconditional CPTP fallback.

A fixed partition into at most ceil(vT)+p+1 control-free windows and at most Jmax actual jumps gives a deterministic call cap

    S<=ceil(vT)+p+Jmax+2.

Representative timestamps perturb the future exact capped channel by at most its finite generator norm O(v+KR) times the timestamp error. Choose the finite time word accordingly. For example, skip any residual window shorter than t_min=delta/[1+v+KR], paying its generator norm times t_min. This supplies a finite lower duration for arithmetic after a charged omission, rather than a physical minimum waiting time. A backward contractive hybrid charges at most S local isometry and clock errors, plus the exact count-tail error and tiny remaining-window omissions. This preserves arbitrary reference systems and prescribed-time instrument records without exposing private bath timestamps or normalizing rare outcomes.

## 9. Full resource statement and first-stage composition

Let C_D be the actual cost of the supplied system block encodings and their controlled selection, plus the explicit linear oscillator block. Let q=polylog[S(A0+1)/epsilon] be the inner Dyson order, and B=polylog[M,K,R,v,T,1/epsilon] the finite time/arithmetic precision. An explicit, deliberately nonoptimized gate upper bound has the form

    O(S A0 {q[O~(M^2 K)+C_D]+poly(M,r,B,input bits)}),

with polynomially many workspace bits in M,r,log(K),q,B and the actual system input size. Every Gaussian gate, jump direction, CDF prefix, phase, source list and amplification call is acquired above. R appears only through B and the supplied input bits. The dependence on T can be high: with the coarse vacuum cutoff K=O((aT)^2+log(1/epsilon)), the bound is not a near-linear-T theorem and does not establish a practical crossover.

For the actual stage-one bath, M=O(log^2(T/epsilon)), ||c||^2 is bounded, and its one-particle R grows only polynomially with T/epsilon while its parameter synthesis uses polynomial logarithmic guard bits. Receive its spectrum-to-channel bound, select K from its proved factorial tail, and allocate separate epsilon budgets to spectrum error, Fock cutoff, parameter rounding, actual count cap, source arithmetic, clocks and digital synthesis. With the stated precision-cost condition on the supplied system access, all terms above then have POLYLOGARITHMIC inverse-accuracy dependence at fixed T,h,a. This is a candidate complete-operation consequence beyond a mode-count statement. It does not assume the hierarchy is an exact thermal reservoir, and the first-stage two-quantum obstruction remains intact.

The detailed finite arithmetic, binary Fock gate construction, tiny-prefix bound, robust amplification argument and emitted-count factorial proof are supplied in FINITE_BIT_DETAILS.md. The matched complete-pipeline comparison is in PRIOR_COMPARISON.md. The derivation still requires an independent review of the whole finite-bit conjunction and a historical-priority assessment. No universal superiority over every reparameterization or physical platform follows from this theorem.
