# Finite-horizon torus transfer by complete zero-component replay

Principal-investigator construction, developed in parallel with Q1's path-prefix
variant and challenged by Q2/R1. This is an adapter to a published infinite-volume
cluster theorem, not a verbatim theorem of Hartarsky--Toninelli. Correctness and
historical originality must be assessed separately.

## Contract

Let phi on healthy bits be a finite monotone DNF

    phi(x) = OR_j AND_(a in A_j) x_a,

with finitely many finite nonempty forcing sets. On a side-M torus start from
all healthy bits 1 and evolve

    omega_(z,n+1) = (1-B_(z,n)) phi(theta_z omega_n).

Each B_(z,n) is a fixed measurable function of independent microscopic Poisson
increments in a deterministic spatial guard of infinity-norm radius g, during slab n. The
same local function defines a field B^infinity on Z^d. Slabs are independent.
No state-dependent or adaptively selected primitive support is permitted.

Suppose the infinite B-driven cold process is dominated in its zero set by an
iid-death perturbed attractive eroder whose upper-invariant spacetime trajectory
has an anchored k-connected zero-cluster tail f(u). Hartarsky--Toninelli,
arXiv:2212.08437v2, Corollary 9.5 supplies f(u)=p^(c(u+1)) for sufficiently small
iid death p. Spatial LSS domination can be applied separately in each independent
infinite slab. No LSS theorem on a finite torus is assumed here.

Use Euclidean distance on torus space times integer time. Fix k larger than
every causal input offset (a,-1), and fix ell with

    ell + k + g + 2 < M/4.

Consider the full zero set in layers 1,...,N, with undirected edges between
points at spacetime distance at most k.

## Sequential first crossing

Reveal layers in chronological order. Within a layer reveal its zero output
vertices in a fixed deterministic spatial order; the outputs are already
determined from the preceding layer, so this ordering does not change the CA.
Stop at the first insertion making a zero component have diameter at least ell.
Let z=(x,n) be the inserted anchor and C its merged component.

Every prior component had diameter less than ell. Any prior component joined
to z has a point within distance k of z, so all its points lie within ell+k
of z. Thus the ENTIRE C lies in this deterministic spacetime ball, even if
many new-layer vertices would later join it. Since diam(C)>=ell, C contains
a path from z reaching distance at least ell/2.

For every nonfault zero (y,t) in C, the DNF formula supplies, for EACH forcing
set A_j, at least one zero parent (y+a_j,t-1). All older layers have already
been revealed, and each such parent is k-near. Hence each belongs to C.
Recursing stays in C. There are no zero nodes at time 0. This is closure under
the zero ancestors needed to force the outputs, not closure of the entire
backward light cone. Healthy inputs outside C are irrelevant to this forcing.

## Fixed local witness and replay

For each possible deterministic anchor z, choose the deterministic spatial
patch of infinity-norm radius ell+k+g+2 around x. The size condition above makes this patch
and all relevant offsets faithfully liftable to Z^d. Copy torus primitive
Poisson increments in that patch through layer n to the lift; extend with
independent primitives outside. The resulting full primitive field has the
ordinary infinite independent Poisson law. Do NOT copy an adaptively chosen
region, and do NOT identify distinct lift variables across periodic images.

The first-crossing event at z implies existence of a finite set C in the inner
patch that is k-connected, contains z, reaches distance ell/2, and satisfies:
each of its nodes either has B=1 at its preceding transition, or has one parent
in C from every A_j. This closed-witness event depends only on the copied fixed
primitive patch. In the infinite CA, induction in time makes every node of C
zero. At a fault the output is zero; otherwise its selected zero parents force
every DNF conjunction to zero. Additional outside zeros can only help.

Thus the fixed-anchor closed-witness probability is at most the infinite cold
CA's probability of a k-connected zero path from z to distance ell/2. Couple
that process below the iid-death CA in healthy-bit order, and couple the iid
cold process above its upper-invariant healthy trajectory. The published
cluster bound gives at most f(ell/2).

Union over at most N M^d deterministic insertion anchors yields

    P(any zero spacetime component reaches diameter ell by layer N)
       <= N M^d f(ell/2).

For fixed k,g, ell=M/128 and sufficiently large M, this is

    <= C N M^d exp(-c M).

There is no bound uniform over all times on a finite torus: eventual absorbing
all-zero histories are consistent with this finite-horizon result.

## Application gates

The sweep application must separately prove its exact envelope domination,
input-independent block forcing flag, literal finite primitive guard,
infinite LSS hypothesis, deterministic eroder property, and whole-slab halo.
Those are not consequences of replay. Once whole-slab halo maps a macroscopic
instantaneous syndrome component to a macroscopic coarse zero component, the
fixed local-filling decoder proves homology invariance up to this first escape.
Then failure is bounded directly by first escape; a second time integral or
an all-time uniform torus marginal is neither needed nor justified.
