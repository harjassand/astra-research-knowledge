# Exact finite-phase recurrence via a dual measure

Candidate mathematical proof, independently challenged within this task but not externally reviewed or novelty-cleared. This is a **one-unbounded-coordinate / finite one-hot-mode** theorem, not the arbitrary-dimensional chemical recurrence conjecture. It does not assume stochastic averaging, a supplied stationary distribution, a spectral gap uniform in population, or fast/slow time separation.

## Contract

States are `(x,j)` with x a nonnegative integer and j in a finite set of one-hot internal modes. Complexes are `(a,j)` with integer a>=0. A finite directed complex graph is weakly reversible. Edge e:(a,j)->(b,k) has fixed rate kappa_e>0 and sends `(x,j)` to `(x+b-a,k)` at rate `kappa_e (x)_a`, zero when x<a. Ignore null state transitions. Handle each connected component of the mode graph separately; each such component is strongly connected because the complex graph is weakly reversible. Finite absorbing components are trivial.

Goal: positive recurrence and nonexplosion in every communicating class, with all exponential population moments for each class. No uniform bound over network sizes or rate constants is claimed.

## Imported finite matrix lemma (proved separately in this task)

For the frozen mode generator built from rates kappa_e(x)_a, let tau_j(x) be its directed tree polynomial and D=max_j degree(tau_j). Define integer beta_j=degree(tau_j)-D. Each tau_j has positive leading coefficient, regardless of signed lower falling-factorial coefficients. If every reaction satisfies

    delta_e := b-a+beta_k-beta_j = 0,

then x+beta_j is conserved and every communicating class is finite.

Otherwise put r=x+beta_j and write shifted rates

    l_e(r)=kappa_e (r-beta_j)_a.

All these rates are positive for sufficiently large integer r. Fixed shifts do not change tree leading degrees, so the frozen mode stationary vector p(r) still satisfies p_j(r)~alpha_j r^beta_j with alpha_j>0 (common normalization exponent already included in beta).

For any fixed 0<eta<theta, define the finite Metzler matrix

    (G(r)f)_j = sum_{e out of j} l_e(r)
               [exp(theta delta_e+eta |delta_e|) f_k-f_j].

Same-mode nonzero jumps contribute to the diagonal. Horizontal delta=0 jumps have no tilt. The finite matrix lemma asserts that G(r) is Hurwitz for all sufficiently large r. Its proof uses exact frozen stationarity, heights a+beta_j, and weakly reversible return paths to absorb every upward-edge quadratic burden into higher-order path energies and a downward sink. No uniform eigenvalue margin is needed in the following lift.

Choose, for completely rational matrix entries, theta=log4 and eta=log2. Then upward tilt factors are 8^delta and downward factors are 2^delta. Other theta give corresponding real coefficients.

## 1. Positive rational dual vector

For all sufficiently large r the nonsingular M-matrix -G(r)^T has a nonnegative inverse, strictly positive in each irreducible mode block. Set

    v(r) = (-G(r)^T)^(-1) 1.

Every entry is a positive rational function of r, since G has polynomial entries. Hence every v_j has at most polynomial growth and, for every fixed integer shift d,

    v_j(r-d)/v_j(r) -> 1.

Likewise, each nonzero polynomial rate l_e(r-d)/l_e(r)->1. There are finitely many edges, so a single finite threshold R guarantees for each delta_e !=0:

    v_j(r-delta_e) l_e(r-delta_e)
      <= exp(eta |delta_e|) v_j(r) l_e(r).

This uses only eventual positivity and rational-function leading terms, not a lower bound on the spectral gap. Exact algebraic/rational coefficient root bounds can find a threshold by clearing denominators whose signs are certified past their last real roots. No favorable polynomial complexity is claimed.

## 2. Exact unaveraged adjoint inequality

On sufficiently high feasible states define

    mu(r,j)=exp(-theta r) v_j(r)>0.

Extend mu arbitrarily positively on the finitely many remaining states. All transitions have bounded integer delta, so this extension changes adjoint calculations only in a finite band. For a state (r,k), the incoming edge e from mode j starts at residual r-delta_e. Its incoming mass equals

    exp(-theta r) exp(theta delta_e)
        v_j(r-delta_e) l_e(r-delta_e).

For delta_e!=0 bound this by the previous inequality. For delta_e=0 there is exact equality, including arbitrarily fast horizontal transitions. The outgoing loss is unchanged. Therefore, outside a finite set K,

    (L*mu)(r,k) <= exp(-theta r) (G(r)^T v(r))_k
                = -exp(-theta r) <0.

Both sum mu and sum mu q are finite, because mu is an exponential times a rational function and the total exit rate q is polynomially bounded. This is an inequality for the actual shifted CTMC, not its frozen approximation.

## 3. A finite dual measure implies positive recurrence

Remove absorbing singleton states. Let P be the embedded jump-chain matrix and nu=mu q. Then nu is a strictly positive finite measure and

    nu P-nu = L*mu <=0 outside K.

For a communicating class Gamma, every enabled transition has an enabled return path (follow the weakly reversible complex path with the same residual molecular vector), so Gamma is closed. If Gamma did not intersect K, strict negativity on every state would contradict sum_Gamma(nu P)=sum_Gamma nu; all sums are finite. Thus each nontrivial class intersects finite K.

Within a class put C=Gamma\K. Blockwise,

    nu_C >= nu_C P_CC + nu_K P_KC.

Iteration and nonnegativity give

    nu_K P_KC sum_{n>=0} P_CC^n <= nu_C.

The right side has finite total mass. Since every positive transition from K to C has positive weight under nu_K, every such excursion has finite expected jump length before returning to K. In particular it returns almost surely. The embedded chain on the finite return set K∩Gamma is irreducible, so its expected number of excursions to any specified return state is finite. The maximal mean excursion length over the finite K∩Gamma is finite. Consequently the original embedded chain is positive recurrent.

The CTMC cannot explode: the positive recurrent embedded chain visits a fixed finite-rate state infinitely often almost surely, and its independent exponential holding times there have an almost surely divergent sum. Physical expected return times are finite as well. Indeed every nonabsorbing state's enabled falling factorial rate is at least min_e kappa_e, so holding time means are uniformly bounded above. Alternatively the excursion occupation domination below directly controls physical occupation.

## 4. Tail statement

The invariant embedded-chain occupation measure on each class is dominated, up to a class-dependent constant, by nu: use the above excursion Green bound and the finite return-set weights. Dividing by q gives a continuous-time invariant probability dominated by a constant times mu. Thus its population tail has an exponential bound with any exponent strictly below theta. Since the matrix construction works separately for every fixed theta>0, all exponential moments of x are finite. Constants and thresholds may deteriorate arbitrarily with theta, network data and the communicating class. This is not a uniform Poisson-tail bound.

## Checks still needed before promotion

- Complete finite tilted-matrix lemma must be bound to its exact saved proof version.
- Independent end-to-end review must check the quadratic absorption constants, shifted-coordinate tree exponents, the embedded excursion argument, and the all-exponential-moments domination claim.
- Prior literature may already cover finite-mode strips; no historical novelty claim is made.
- A general reaction network need not have one unbounded coordinate or a finite internal state set. No reduction of that general case is established.
