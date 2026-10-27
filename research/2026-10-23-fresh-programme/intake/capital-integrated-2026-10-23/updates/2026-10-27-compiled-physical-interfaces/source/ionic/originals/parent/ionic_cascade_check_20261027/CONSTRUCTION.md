# Ordinary multistage escape from the one-reservoir turnover barrier

This exact ideal-model construction tests a hidden restriction in the fresh
worker's investigation. Its large optimum is valid for ONE well-mixed recycle
source. Enriched intermediate inventories are excluded there; they are charged
resources here. This is not acquired chemistry, a new separation technology,
an energy advantage, or an estimate of device throughput.

## Operation and premises

Use stages j=1,...,M-1, waste sink0 and product sinkM. Load each cohort into its
stage bed, wash without rebinding for fixed dose H, send the wash-released pool
one stage left, and completely elute the retained pool one stage right. Every
valve routes whole pools, never ion identity. Repeat until absorption. A finite
particle collection absorbs almost surely with finite expected visits. The
continuum ideal has an asymptotic endpoint; finite deadlines require explicit
residual-inventory accounting. The waste sink is a SEPARATE collector, rather
than recycling every reject into the original source. This consumes the feed
through staged pools and permits background discard; those operations are
explicitly outside the one-source bound as well as its inventory restriction.

Assume independent first-order release with rates a_L*k(t),a_N*k(t), a_N>a_L,
and the same law on every visit. Nonselective complete capture and elution,
accurate pool routing, intermediate beds/inventories and negligible losses are
ADDITIONAL IDEAL PREMISES, not consequences of bulk diffusivities or equal
equilibrium affinity. Every visit counts a gross capture. Bed occupancy,
water/solvent, regeneration, binding time, heat/work, dead volume and scheduling
remain charged but unquantified physical interfaces.

Choose the fixed wash dose so that right-going fractions are

    p_L=exp(-a_L H), p_N=exp(-a_N H)=p_L^rho, rho=a_N/a_L.

Each particle follows an absorbing nearest-neighbor walk: ordinary repeated
separation with counterflow and stored pools. There is no perfect species sorter.

## Exact recovery and gross captures

Let h_i(p) be product absorption probability and t_i(p) expected future captures
from feed stage i. They uniquely solve

    h_j=p h_(j+1)+(1-p)h_(j-1), h_0=0,h_M=1;
    t_j=1+p t_(j+1)+(1-p)t_(j-1), t_0=t_M=0.

For p!=1/2, their solutions are

    r=(1-p)/p, h_i=(1-r^i)/(1-r^M), t_i=(M h_i-i)/(2p-1).

Substitution verifies both recurrences. Uniqueness follows from the finite
absorbing chain/discrete maximum principle. At p=1/2, h_i=i/M,t_i=i(M-i).
Alternatively stopped drift gives E[final position]=M h_i=i+(2p-1)t_i.

For initial L0,N0, product purity is

    L0*h_i(p_L)/(L0*h_i(p_L)+N0*h_i(p_N)).

Gross background captures per recovered target are
N0*t_i(p_N)/(L0*h_i(p_L)), including retries. This is not total process cost.

## General scaling: storage changes the dilute exponent

For ANY fixed rho>1 choose p_L in(1/2,2^(-1/rho)), hence p_N=p_L^rho<1/2.
Define a=log[p_L/(1-p_L)]>0,b=log[(1-p_N)/p_N]>0. For target loss delta in(0,1),
purity loss epsilon in(0,1),feed ratio n=N0/L0>0, take integer feed i and
distance d=M-i satisfying

    i >= max(1,log(1/delta)/a),
    d >= max(1,log(2)/b,
             log[2n(1-epsilon)/((1-delta)epsilon)]/b).

The exact formulas give h_L>=1-exp(-a*i)>=1-delta and
h_N<=2 exp(-b*d)<=(1-delta)epsilon/[n(1-epsilon)]. The factor2 uses
M>=log(2)/b. Product purity is therefore at least1-epsilon. These are finite
stage counts, not an infinite-column limit. Gross background captures per
recovered target are bounded by n*i/[(1-2p_N)(1-delta)]. Target visits separately
obey t_L<M/(2p_L-1).

For fixed rho/recovery, stages grow logarithmically in feed dilution and inverse
impurity, and this gross-background bound is LINEAR in n regardless of added
purity stages. For weak contrast rho=1+kappa choose
p_L=2^(-(rho+1)/(2rho)),p_N=2^(-(rho+1)/2). As kappa tends to0 from above,
a~(log2)*kappa,b~(log2)*kappa,1-2p_N~(log2)*kappa/2. The sufficient stage count
is O((log n+log(1/epsilon)+log(1/delta))/kappa) in the dilute/small-error regime;
the background-capture bound is O(n*log(1/delta)/kappa^2) at fixed loss allowance.
These ideal resource scalings show WHY stored composition avoids the one-source
exponent. They do not supply real capture, transfer, time, work or economics;
historical novelty and physical advantage are unclaimed.

## Exact illustrative calculation

Take rho=133/103,p_L=27/50,M=90,feed i=15,N0/L0=10000. The kinetic ratio is
illustrative, not an acquired material rate. The true p_N is strictly between
451284/10^6 and451285/10^6, proved by EXACT powers:

    (451284/10^6)^103 < (27/50)^133 < (451285/10^6)^103.

Common-uniform coupling makes h_i monotone in p, so the upper endpoint bounds
background product. For p_N<1/2,

    t_i(p_N)=(i-M h_i(p_N))/(1-2p_N)<=i/(1-2p_N,upper).

No monotonicity of absorption TIME was assumed. Exact fractions give89 active
stages, target recovery0.9097476098990884, purity at least0.9955519496167978,
gross background captures per recovered target<=1692301.087 and all stage
captures per recovered target<=1693219.986. RESULT.json retains exact fractions
and strict90%/99% checks. check.py also solves four finite chains independently
by rational tridiagonal elimination, both drift signs and zero drift included.

The worker's approximately7.69e26 optimum belongs to a DIFFERENT restricted
family: infinitesimal capture cohorts returned to ONE source without enriched
intermediates. This cascade is outside that family; there is no contradiction
or matched hardware speedup. It prevents promotion of that large number into a
general kinetic-separation obstruction. Many-pool transfer is the extra interface.

## Physical and scientific boundary

The primary [Kautz et al., Nature Materials2026](https://doi.org/10.1038/s41563-026-02511-y)
reports capacitive ratchet pumping and50% dilution-cell conductivity reduction.
The publisher/primary abstract was checked. This does not acquire Li/Na capture
chemistry, release ratios, or this cascade's full cycle. Spatial ratchets are
outside the one-reservoir wash theorem and require their own electrodiffusion,
electroneutrality and load assessment.

A constructive ordinary comparator escapes severe one-source scaling through
stored intermediate pools. Their useful cost/reliability is the remaining
physical question. Historical novelty, realization and advantage are UNKNOWN.
