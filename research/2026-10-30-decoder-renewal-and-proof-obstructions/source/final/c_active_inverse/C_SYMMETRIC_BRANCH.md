# An exact typical-sector decoder, and its quadratic-rank obstruction

30 October2026. C construction. The input is the exact unknown flat mixed
qubit encoder N_U(rho)=U(rho tensor I_r/r)U*, D>=2r. No junk intervention,
unknown adjoint, controlled dilation or quantum switch is used. This is
the next independent construction after the exterior-hole admission
failure. It replaces rare determinant postselection by a positive
FULL-THROUGHPUT decoder summing all typical Young sectors. It nevertheless
fails the desired prediction: its optimal fidelity has a quadratic-rank
gate, and it never approaches a perfect general inverse.

## 1. One coherent physical-query block

Fix Q>=1, J=Q/2, d=Q+1. In the logical symmetric/Dicke space prepare

  |Phi_J> = (1/sqrt(d)) sum_(m=0)^Q |m>_R |Dicke_(Q,m)>_(A^Q).

Apply N_U to all Q logical inputs, keeping R and all physical outputs.
Append one late independently encoded arbitrary payload. This consumes
Q forward physical queries, on coherently entangled logical inputs,
followed by storage of Q physical carriers plus log(d) reference qubits.
The payload was not used during preparation. No programme can be retried
on the payload. Known Dicke preparation is an ordinary finite known-state
operation; its gates and all storage/control precision remain real costs.

We derive the BEST deterministic receiver for this specific programme,
allowing arbitrary known collective postprocessing. Thus its failure is
not just a poor guessed filter. It is not a lower bound for arbitrary
physical-query strategies or other coherent query inputs.

## 2. Eliminate the unknown physical frame without rare sectors

Put N=Q+1 and temporarily append a normalized logical Bell reference T
to the payload. Before U^tensor N, the logical state is
|Phi_J><Phi_J| tensor |Phi_2><Phi_2|; all N junk carriers are I_r/r.
Let P_pi permute N physical carriers and let c(pi) be its cycle count.
The partial permutation moments, matrices on R tensor T, are

  M_pi = r^[c(pi)-N] A0,  if pi fixes the payload position;
  M_pi = r^[c(pi)-N] A1,  otherwise,                         (1)

where

  A0 = I/[2d],
  A1 = [I/2 + (sum_a J_a^T tensor sigma_a^T)/Q]/[2d].       (2)

Here J_a are the ordinary spin-J generators in the chosen Dicke basis.
Both transposes are important; the reference system has not been
conjugated or supplied as a physical inverse. The logical moment is the
same for every permutation in each of the two double cosets
S_Q\S_N/S_Q, since each programme logical ket is symmetric. Compressing
a transposition between a query input and the payload gives
P_sym SWAP_(i,N) P_sym=I/2+(sum_a J_a tensor sigma_a)/Q,
which proves(2). The junk permutation trace gives the displayed cycle
factor, proving(1).

Averaging a receiver over known simultaneous U(D) rotations makes its
average fidelity independent of U without reducing it. Schur--Weyl
decomposition therefore lets us trace the unknown U(D) representation
space, retaining only its Young label lambda and permutation-multiplicity
space. This is an ordinary known Schur operation. It does not estimate U,
and is not a hidden common-frame oracle.

For a partition mu of Q, let f_mu be its symmetric-group dimension and

  c_mu(r)=product_[(i,j) in mu] (r+j-i).

The central group-algebra identity

  sum_(pi in S_N) r^c(pi) pi
     = product_(l=1)^N (r+X_l)

uses Jucys--Murphy elements X_l=sum_(i<l)(i,l). On a Young branch
mu -> lambda=mu+box, X_N has the added box's content t=j-i and
c_lambda(r)=c_mu(r)(r+t). Fourier inversion of(1) consequently gives the
following EXACT unnormalized R,T block, tensored with I_(f_mu):

  B_(lambda,mu)
    = f_lambda c_mu(r)/[N! r^N] * [r A0+t A1].               (3)

The physical lambda representation can be measured, then its restriction
to S_Q can be measured as mu. There is no coherence to lose between
these blocks in the averaged state. All remaining physical multiplicity
factors are maximally mixed and independent of R,T. Thus a branch needs
only a known spin-J-to-qubit decoder acting on R.

For clarity, the Fourier normalization can be checked on I_s/s^N:
its permutation moments are s^[c(pi)-N], and inversion gives the usual
block (dim U_lambda(s)/s^N) I_(f_lambda), not an extra inverse dimension.

## 3. Positivity, normalization and the literal branch operation

The eigenvalues of sum J_a^T tensor sigma_a^T are J and -(J+1), on total
spin J+1/2 and J-1/2 respectively. Thus r A0+t A1 is positive: its two
eigenvalues are

  (r+t)/(2d),  (r-t/Q)/(2d).

Every surviving mu has at most r rows. Every addable box has -r<=t<=Q,
so both quantities are nonnegative. This includes a zero eigenvalue on
the boundary. No numerical clipping, gap, inversion or postselection is
required. The branch probability is

  p_(lambda,mu)
     = w_(lambda,mu) [r+t/2],
  w_(lambda,mu)=f_lambda f_mu c_mu(r)/[N! r^N].              (4)

They sum to one, as proved below. Each branch is retained, including
ones with no useful payload correlation.

Twirl a branch's spin-to-qubit receiver by known SU(2) covariance. Its
adjoint must have the form D_b*(sigma_a)=b J_a^T. The unnormalized Choi
matrix of this map is

  [I+b sum_a J_a tensor sigma_a]/2.

It is trace preserving and positive exactly when

  -1/J <= b <= 1/(J+1).                                   (5)

These two endpoints are finite known channels. The negative endpoint is
a known spin-pi rotation, embedding into Q symmetric qubits, and partial
trace. The other endpoint is the opposite extremal Clebsch--Gordan
channel; factoring its displayed positive Choi matrix is an explicit
known finite Kraus construction. Both have source-independent controls.
Choose b=1/(J+1) when t>=0 and b=-1/J when t<0. Since branch fidelity is
linear in b, this is optimal among all CPTP branch receivers. The branch
Bell fidelity is

  F_(t>=0)=1/4 * [1+t/(2r+t)],
  F_(t<0) =1/4 * [1-t(Q+2)/(Q(2r+t))].                    (6)

This constructs an actual all-input CPTP circuit: prepare the programme;
on payload arrival Schur-transform the Q+1 physical carriers; measure
lambda and mu; discard physical representation and multiplicity spaces;
apply the selected known channel D_b to R. It has throughput one, but
the low fidelity below makes it an inadequate inverse. Exact known
Schur/CG circuits are ordinary machinery. Approximate compilation and
Q logD coherent storage must be charged for an implementation; no source
device or quantum circuit has been run in this work.

## 4. A scalar transition law gives the exact optimal fidelity

Let mu have the Schur--Weyl law of Q maximally mixed r-level carriers:

  Pr(mu)=c_mu(r) f_mu^2/[Q! r^Q].

Conditional on mu, draw an addable box with the ordinary Plancherel-up
transition

  Pr(lambda|mu)=f_lambda/[N f_mu],

and let T be its content. These are merely a FINITE classical law for
computing the circuit's exact fidelity; they are not a supplied hidden
junk measurement. The basic transition identities are

  E(T|mu)=0,  E(T^2|mu)=Q.                                 (7)

A direct proof avoids an asymptotic Young-shape assumption. Use the
normalized regular trace of C[S_N] and a primitive matrix idempotent
of mu in C[S_Q]. Conditional expectation to C[S_Q] annihilates X_N,
and sends X_N^2 to Q I, because all off-diagonal terms contain the new
letter N. On branching to lambda these trace weights are exactly
f_lambda/(N f_mu). This proves(7), including all boundary diagrams.

Equations(4),(7) give sum w=1/r and sum wt=0, hence sum p=1.
Using(6), and E T_+=E(-T)_+=E|T|/2, the optimum Haar/minimax fidelity
for this programme is EXACTLY

  F_sym(Q,r)=1/4 + (Q+1)/(8rQ) E|T|.                      (8)

No weak-coupling, large-r or moment closure is used. By Cauchy and(7),

  F_sym(Q,r)<=1/4+(Q+1)/(8r sqrt(Q)).                     (9)

In particular Q=O(r) gives F_sym=1/4+O(r^-1/2), even with the best
receiver for this coherently entangled programme. To reach any fixed
F_sym>=1/4+delta requires Q>=16delta^2 r^2 (use Q+1<=2Q).
The physical-query lower bound here is ONLY for this chosen programme.
It is not inferred from the normalized iid-Choi lower theorem.

There is also a separate single-irrep ceiling. At r=1 the only surviving
mu is the one-row diagram(Q). Its two branches have contents Q,-1 and
Plancherel probabilities1/(Q+1),Q/(Q+1). Equation(8) gives exactly1/2
for EVERY Q. The same1/2 is an upper bound uniformly for arbitrary r:
an invariant decoder with a larger Haar fidelity would have that fidelity
on U=V_logical tensor I_junk. Discarding the independent known junk then
contradicts the r=1 single-spin result. A larger or differently coherent
logical programme, or genuinely sequential feedback, is required even
before asking for linear rank scaling.

## 5. Executed discriminating consumer and the surviving question

`evaluate_symmetric_branch.py` enumerates partitions and addable boxes
with exact integer hook/content products. It checks every transition's
normalization, first and second content moments, every block's positivity,
and both full probability normalizations. It evaluates(8) without Haar
draws, a hidden-U oracle, a solver, or ambient density matrices.
The single declared test is Q=r=32: a real linear-query design point
of this analytic all-r construction, not a fitted new physical source.

The failure is explanatory. Admitting typical junk sectors removes the
exterior postselection catastrophe but does not create a full logical
reference frame: a single logical irrep is insufficient. The remaining
operation is coherent CONTROL OF THE LOGICAL SCHUR PROFILE across
different spins, or feedback on an already unknown memory/payload.
Ordinary unitary-learning/inversion and RDS constructions must be given
full strength at that gate. The general physical-query linear-versus-
quadratic question remains OPEN; neither of these two failed circuits
proves its negative answer.
