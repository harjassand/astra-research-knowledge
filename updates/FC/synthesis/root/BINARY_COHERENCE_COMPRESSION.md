# The acquired binary histogram sharpens the kinetic coherence certificate

13 October 2026. Internal restricted derivation, priority and external correctness
UNKNOWN. Capital pin `b34e22e8f8ef8bd853595952fcbd9c74c5ace306`.
This uses the new histogram source and the separately proved activity identity.
UCP maps, relative-entropy data processing and qubit entropy are known ingredients.
No new physical operation or general quantum-coherence measure is claimed.

## 1. Same supplied and acquired information

Work in the same finite conserved sector as the source. Use TWO nonempty label
projectors P0,P1, H=D+T and beta>0, with

    T=B+B†,       B=P0 H P1,
    rho=exp(-beta H)/Z_H,       sigma=P0 rho P0+P1 rho P1,
    p=Tr(P0 rho),       a=-Tr(rho T)>=0.

Supply a calibrated K>=||B||=||T||. The histogram p and kinetic activity a are
already the source's measurements. The construction performs no additional
state tomography or measurement. For K=0, T=a=0 and Z_H=Z_D; handle this case
separately. Assume K>0 below. Write H2 for natural-log binary entropy, and set

    x=a/K,       r=sqrt((2p-1)^2+x^2),
    d_p(x)=H2(p)-H2((1+r)/2).                                 (1)

Then x<=2sqrt(p(1-p)), and

    D(rho||sigma)>=d_p(x),
    0<=log(Z_H/Z_D)<=beta a-d_p(a/K).                          (2)

The right side strengthens the activity bound that uses only a and K.

## 2. A constructive UCP compression and proof

Define the Heisenberg map Phi from2-by-2 matrices to operators on the full
selected sector by

    Phi([[u,z],[z*,v]]) = u P0+v P1+z B/K+z* B†/K,

extended complex linearly. Its Choi matrix is

    J_Phi=[[P0,B/K],[B†/K,P1]].

On |0> tensor range(P0) plus |1> tensor range(P1) this is
`[[I0,B/K],[B†/K,I1]]`, positive because B/K is a contraction. It is zero
on the complementary support. Thus Phi is completely positive, and
Phi(I2)=P0+P1=I. Its state adjoint Lambda is CPTP.

The compressed state is a qubit with diagonal(p,1-p) and off-diagonal z,
where `2K Re z=Tr(rho T)=-a`. The pinched state maps to diag(p,1-p).
Qubit positivity gives |z|<=sqrt(p(1-p)), proving the feasibility bound on x.
Its entropy decreases with |z|. Relative-entropy data processing therefore gives

    D(rho||sigma)>=D(Lambda rho||Lambda sigma)
       =H2(p)-S(Lambda rho)>=d_p(x).

The exact activity identity from the separate proof is

    log(Z_H/Z_D)=beta a-D(rho||sigma)-D(sigma||rho_D),
    rho_D=exp(-beta D)/Z_D.

Dropping the last nonnegative term proves(2). The channel is an analytic witness;
its implementation is not assumed or performed. The scalar result requires only
p,a,K, not knowledge or manipulation of the unknown global state.

The entropy lower bound itself is sharp on abstract qubit states with real
off-diagonal -x/2. This does NOT make the full partition upper bound minimax
sharp: the second relative entropy was discarded and Gibbs/model constraints
can supply additional information.

## 3. Comparison and confidence-safe computation

The previous activity proof uses

    f(x)=log2-H2((1+x)/2).

For fixed bias b=|2p-1| and feasible x,

    derivative_x d_p(x)=x*atanh(sqrt(b^2+x^2))/sqrt(b^2+x^2)
                       >=atanh(x)=f'(x).

Both functions vanish at x=0, so d_p(x)>=f(x). The inequality is strict for
x>0 and p!=1/2 in the interior. Therefore the new exponent never exceeds
the previous activity exponent or its log cosh(beta K) ceiling. Its total
subtraction is at most H2(p)<=log2; this is a bounded certificate improvement,
not elimination of arbitrary environmental uncertainty or preparation cost.

For uncertain p in[l,h] and a in[a_lo,a_hi], intersect with p in[0,1],
a>=0 and x<=2sqrt(p(1-p)). Empty feasibility is a calibration/model consistency
failure. It is unsafe to substitute empirical p and a directly into(2).

For a rectangular confidence set, the maximization is particularly simple.
At fixed x, d_p(x) increases with |2p-1|: its derivative in b is

    b*[atanh(sqrt(b^2+x^2))/sqrt(b^2+x^2)-atanh(b)/b]>=0,

with continuous limits at zero. Thus let p_* be the point in[l,h] closest to
1/2. It has both the smallest entropy penalty and the largest feasible activity
range. The worst exponent is the maximum of

    phi(a)=beta a-d_(p_*)(a/K)

over `[max(0,a_lo), min(a_hi,2K sqrt(p_*(1-p_*)))]`.
For fixed p_*, d_p is convex in a, so phi is concave. Its derivative is
`beta-a*atanh(r)/(K^2 r)`. A monotone scalar root search, clipped to the interval,
finds the maximizer. For p_*=1/2 it reduces to a_*=K tanh(beta K).
Endpoint limits and K=0 need explicit handling; outward arithmetic/root bounds
remain required for a machine certificate. A negative upper exponent is
inconsistent with the physical contract and must not yield C<1.

Exponentiate a valid upper bound, intersect with other valid microscopic graph
budgets, and use the source histogram calculation unchanged. Histogram and
kinetic confidence events can be shared and their failure probabilities combined;
they must be simultaneously valid under any stopping/selection protocol. More
general correlated uncertainty sets require their own safe maximization. K and
temperature calibration errors must also be charged.

## 4. Relation to capital, prior and scientific scope

N778/N779 show how UCP witnesses and entropy bounds can give environment-uniform
comparisons. They do not supply a physical local actuator or the present Gibbs
histogram. Here a different, explicit UCP compression translates already
acquired binary populations and kinetic expectation into a sharper entropy
penalty. The proof above, rather than topic adjacency, discharges that restricted
mathematical step. It retains all sector, equilibrium and diagonal-intervention
premises of the new source.

Coherence quantification from few measurements and two-level entropy compression
are established research. Primary context accessed here includes the abstract
of Smith et al., https://arxiv.org/abs/1707.09928 , and Nasreddine's2026 preprint
https://arxiv.org/html/2605.11024v2 (introduction, comparison/scope, Pythagorean
identity and two-level functional). The latter constrains other block data and
is not imported as a proof premise or treated as independently validated.
These locators preclude claiming that entropy compression or measurement-based
coherence quantification itself is new. Priority of this thermodynamic use remains
UNKNOWN; no comprehensive literature clearance was performed.

`binary_coherence_checks.py` independently constructs complex block Hamiltonians,
the Choi witness, compressed states and entropy/partition budgets. It separates
exact rational qubit positivity from floating finite diagnostics. No physical
measurement, external validation or practical materials advantage is established.
