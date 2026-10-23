# A positive spectral witness and a necessary restriction on linear inputs

## Scope

This is an analytic all-length consequence of the actual Cycle7 bulk token
classification. It neither solves the complete spectrum of H nor supplies a
capacity converse. Its receiving use is to distinguish a genuine positive-input
reparametrization from merely improving the norm estimate on the old linear
family.

Let H=H_k be the explicit symmetric-prefix input observable from Cycle7,
sigma=diag(1/2,1/4,1/4)^tensor k, and Q the number of nonzero ports. Thus H is
Hermitian, charge preserving, and input offdiagonal. Set

    C_k = sum_{n=0}^{k-2} (k-1-n) Pr(S_n=0),

where S is the simple symmetric walk. This is the exact collision sum already
proved in Cycle7, not a newly fitted sequence.

## Theorem: a one-sided spectral lower bound

For every k>=2, with

    psi_k = ((|0>+|1>)/sqrt(2))^tensor k,

one has

    <psi_k,H psi_k> = C_k/4.

Consequently

    lambda_max(H_k) >= C_k/4
      = k^(3/2)/(3 sqrt(2 pi)) + O(sqrt(k)).

In particular the positive spectrum is not O(k).

### Proof

Fix an oriented endpoint pair i<j, with binary input charges 0 at i and 1
at j. All remaining binary charge patterns occur with probability 2^(-k)
in psi_k, and every colored input wire is |1>. In the inherited exact block
classification:

* For h>d, the color block is P_A(I-SWAP). It annihilates the repeated-color
  vector, since swapping two |1> wires does nothing.
* For h=d, the block is P_A/2. A color permutation fixes the repeated-color
  vector, giving matrix entry 1/2.
* For h<d, the H block is zero.

The reverse orientation is the adjoint. Its contribution is identical.
Therefore each oriented endpoint charge-pattern sector with h=d contributes
2^(-k) to <psi_k,H psi_k>. Summing spectators and endpoint locations gives

    <psi_k,H psi_k>
      = (1/4) sum_{i,r>=0, i+r<=k-2} Pr(M_i=M_r)
      = C_k/4.

The maxima are independent walks on disjoint spectator intervals; the exact
collision identity and its asymptotic are the Cycle7 theorem. The Rayleigh
principle gives the spectral inequality. This uses only the already proved
bulk input operator; no raw identity through a bath vacuum is asserted.

## Corollary: charge-only repair cannot remove the restriction

Consider any normalized candidate

    rho = sigma^(1/2) [ I - t H + f(Q) ] sigma^(1/2),

where t>=0 and f is real. Since Tr(sigma H)=0, normalization requires
Tr(sigma f(Q))=0. Positivity necessarily implies

    t C_k <= 4.

Indeed psi_k has exactly the same binomial charge distribution as sigma,
so <psi_k,f(Q) psi_k>=Tr(sigma f(Q))=0. The relative density has Rayleigh
expectation 1-t C_k/4. Congruence by the faithful sigma^(1/2) preserves
positivity, proving the claim.

For the Cycle8 density, t=(ln 2)b/2. Hence a necessary condition is

    b C_k <= 8/ln 2.

It follows that this specific linear direction, even with an arbitrary
normalized scalar-in-charge diagonal repair, cannot remain positive along
a family k(b) with b k(b)^(3/2) -> infinity. In particular k proportional
to 1/b is excluded. This is a necessary O(b^(-2/3)) temporal restriction,
not a proof that positivity holds all the way to that order. The prior
sufficient O(b^(-1/2)) window and this necessary bound remain distinct.

The same conclusion applies to the smaller t=(ln 2)b/4 proposal, with the
constant changed to 16/ln 2. A nonlinear clipping or Gibbs operation is a
different input family and is not excluded by this witness.

## What the witness does not mean

The pure product psi_k is an analytic spectral test. It is not asserted to
have high entropy or an inward bath drift; it is not a new physical coding
input. Thus this argument does not reopen the closed single-site iid route.
It does not bound capacities, general correlated input states, or feedback.
It does not imply a sharp asymptotic formula for lambda_max(H).

The charge-only form and normalization of the repair matter. If one drops
normalization, adding c I with c>=t||H|| makes the bracket positive for any
t. That changes the normalized coefficient after division by its trace.
It therefore does not refute the corollary, and exhibits why a free constant
repair is not an admissible unchanged linear density.

## Bounded diagnostics

`spectrum.py` builds the exact integer matrix 2H in conserved port-color
count sectors using the inherited token normal form. Floating eigenvalues
are diagnostic, not spectrum theorems. A run through all sectors k<=8 took
about 0.24 seconds in the child process (plus Python startup); selected
balanced sectors k=9..13 took about 18 seconds combined. No extrapolation is
used in the theorem. The exact witness replay is independent of those
eigenvalues and is in `witness_replay.py`.

Discovery, inference, and review costs are unmeasured. No full coding
experiment, physical bath simulation, or useful implementation claim follows.
