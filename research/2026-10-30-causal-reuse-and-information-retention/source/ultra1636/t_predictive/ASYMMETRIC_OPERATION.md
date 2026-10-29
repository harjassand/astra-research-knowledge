# Asymmetric fresh-mixture projection: general construction in progress

30 October2026. This is a new proof state, not an accepted compiler announcement.
Root's OPERATION/LOCALIZATION_LEMMAS and Liu--Moitra2411.07536v1 Sections3,6,7 were
read before transfer. The teacher is Q, the low-rank target is P, and these are
NEVER identified. No conditional P query or post-compilation Q access is used.

The changed operation is an ASYMMETRIC KL sketch: fresh rows supply the FIRST
argument/importance distribution; propagated children enter only a clipped LOG.
This pays a different contract from a union-mixture L1/KL-preserving sketch.

## 1. Finite families and a uniform row

At a cut with remaining length L, let R_1,...,R_s be teacher conditional future
distributions at selected FRESH P prefixes. Append R_(s+1)=U_L, the uniform future
law. Set S=s+1 and mu=(sum R_i)/S. Thus

    R_i/mu<=S,  mu(f)>=1/(S O^L).

The uniform row is sampleable/evaluable and its restriction is exactly another
uniform row. It is one extra direction, not an oracle or an exponential table.

All candidate states are signed combinations z_alpha=sum alpha_i R_i with
sum alpha_i=1 and |alpha_i|<=C. Their integral is EXACTLY1; they need not be
pointwise nonnegative. Draw D fresh features f_j~mu, independently AFTER row
selection. Require z_alpha(f_j)/mu(f_j)>=tau. The uniform coefficients1/S give a
strictly feasible point regardless of the target. Uniform L1/negative-part
concentration ensures every feasible candidate has negative mass<=v, simultaneously
for all future adaptively chosen coefficient states.

Let theta>0, a<=1/O, and define absolute floors

    delta_L=theta a^L,     theta<=tau/(2S).

Then delta_L<=tau mu(f)/2. Write [z]_L=max(z,delta_L) pointwise. Its excess mass
k_z=integral([z]_L-z) is at most v+theta, since delta_L O^L<=theta.
These positive full densities are ANALYSIS objects, not new inference oracles.

## 2. Arbitrary propagated children and the convex program

Let W_1,...,W_k be any teacher child distributions, without a rank or P-closeness
premise. A propagated state is w_beta=sum beta_i W_i with |beta_i|<=C/a. It need
not have mass1 or be positive. Define w_plus=max(w_beta,delta_L).

At the fixed fresh features, every R_i and W_i density is evaluated OFFLINE.
Inference only combines these stored arrays. In particular no samples from the
children are required to define the projection measure mu.

For the current beta, minimize over the preceding convex coefficient set

    J_D(alpha)=D^(-1) sum_j
       [ z_alpha(f_j)/mu(f_j) * log(z_alpha(f_j)/w_plus(f_j))
          -z_alpha(f_j)/mu(f_j) ].                     (1)

The minus-linear term matters: exact normalization is sum alpha=1 in the FULL
space, rather than an empirical normalization. Its derivative is log(z/w_plus).
The program is convex and strictly feasible (uniform coefficients); its inputs
are cached values. An optimization tolerance is charged explicitly below.

Let K=max(S C,k C/a,1)+1 and B=log(K/delta_L). All clipped full densities lie in
[delta_L,K], so log([z]_L/w_plus) is bounded by B, independent of likelihood-ratio
spikes. The number of futures appears only through log(1/delta_L)=log(1/theta)+
L log(1/a). This is the key contrast with a child-dominating importance mixture.

## 3. Uniform asymmetric sketch lemma

For ANY alpha0,alpha,beta in the stated boxes, define

    g(f)=((z_alpha0(f)-z_alpha(f))/mu(f))
                 log([z_alpha]_L(f)/w_plus(f)).

Its magnitude is at most M=2 S C B. With coefficient sup-norm displacement lambda,
its Lipschitz constant is at most

    H=2 S^2 B+2 S C(S+k)/delta_L.

Indeed R_i/mu<=S controls the first factor; x->log(max(x,delta_L)) has Lipschitz
constant1/delta_L and the unweighted row densities are<=1. A net of the parameter
box of dimension d=2S+k and side2C/a with spacing lambda=xi/(4H), plus Hoeffding,
shows that

    D >= (8 M^2/xi^2)[d log(1+2C/(a lambda))+log(2/p_fail)]

suffices for uniform integration error<=xi (enlarge constants for noninteger D).
Only logH is used, so this sample bound is polynomial in S,k,C,1/a,1/xi,B and
log(1/p_fail), despite the absolute floor's exponentially small value.

The same net argument for (-z_alpha/mu)_+, bounded by S C and Lipschitz S^2,
gives a polynomial sample bound for uniform negative-mass error<=v. On feasible
states the empirical negative mass is0, hence the actual negative mass<=v.
Neither bound asserts that pointwise positive density follows from a finite grid.

## 4. A complete signed projection inequality

Let alpha* be the optimizer, z=z_alpha*, and suppose a feasible alpha0 exists with
||p-z_alpha0||1<=e, for a true probability density p. Uniform gradient integration
and an xi first-order optimization tolerance yield

    integral (z_alpha0-z) log([z]_L/w_plus) >=-2xi.       (2)

For positive unnormalized densities, log-sum gives

    integral [z]_L log(w_plus/[z]_L)
       <=(1+k_z) log(Z_w/(1+k_z)),  Z_w=integral w_plus.

Replacing [z]_L by z costs at most B k_z. Consequently, writing
Phi_delta(p,z)=sum p log(p/max(z,delta)),

    Phi_delta(p,z)
      <=Phi_delta(p,w_beta)+log Z_w
                +2xi+B(e+2k_z),                      (3)

provided Z_w<=K, as it is here. To check the last step, the remaining difference
from log Z_w is k_z logZ_w-(1+k_z)log(1+k_z)<=B k_z.
Thus this projection argument does not grant global positivity, an exact target
point in the feasible set, or a target-preserving conditional oracle.

## 5. Transition telescope, including rounding

At cut t let z_t have exact mass1 and negative mass<=v. Compute its token
marginals m_o from the cached teacher next-token rows. Output

    p_hat(o)=max(m_o,b)/M0, M0=sum_o max(m_o,b).

If v+O b<=1, then1<=M0<=1+v+O b<=2 and p_hat>=b/2=:a. Restrict z_t to token o
and divide by p_hat(o), using the cached teacher children and the exact uniform
child. This is w_o. No P approximation of those children is assumed.

Choose delta_(L-1)=delta_L/a. Then p_hat(o)delta_(L-1)>=delta_L, and exact
unnormalized chain rule gives

    sum_o p(o) Phi_(delta_(L-1))(p(.|o),w_o)
      <=Phi_(delta_L)(p,z_t)-D(p_tokens||p_hat).         (4)

Every reference normalization in(3) is also paid. Since m_o/p_hat(o)<=M0,

    Z_wo<=1+v+O b+v/a+theta,
    log Z_wo<=v+O b+v/a+theta.                         (5)

This DIRECT bound preserves the negative token-KL in(4); bounding the normalization
by a Jensen expression that cancels that KL would fail to control the output.

If all but gamma P-mass of cut histories have feasible proxies with error<=e,
use(3) there and the trivial clipped-log bound B at bad histories. Summing under
the actual P prefix law yields

    D(P||P_hat) <= Phi_initial +
      sum_t [v+O b+v/a+theta+2xi+B(e+2(v+theta)+gamma)]. (6)

The terminal potential is0 because the empty future row is1 and sum alpha=1.
Initialize with (1-lambda)Q+lambda U: Phi_initial<=Delta-log(1-lambda). Its token
row and child restrictions are cached in the same way, so no teacher calls remain
after compilation. Equation(6) is a GENERAL receiver, not a finite toy control.

## 6. Fresh approximate-spanner acquisition (next proof boundary)

The remaining acquisition proof must supply the distributional proxy premise of
(6) with polynomial full-trajectory P samples and Q calls. Unlike the old union
mixture, proxy positivity is now tested only on INDEPENDENT fresh-mixture features.
If a normalized signed proxy v has ||p-v||1<=e0, then padding toward mu by4tau
makes it feature-positive unless v(f)<-tau mu(f). This has mu-probability<=e0/tau,
so the full feature-batch failure is<=D e0/tau. This bound is for the P-distributed
target history, NOT for selected previous-basis children. There is no Nprev term.

A complete fresh-spanner proof/resource ledger and finite-precision compiler still
need to be bound to this receiver before claiming the central contract solved.
