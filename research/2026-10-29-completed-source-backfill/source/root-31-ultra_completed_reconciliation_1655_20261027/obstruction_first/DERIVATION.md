# Constructed finite-input interface

## 1. The source theorem and the actual obstruction

For even L, H_L=sum_j S_j·S_{j+1}, with local spin2. Write
Z_L(b)=Tr exp[-b(H_L+aL)]. The source gives a real compact self-adjoint spatial
operator X_b with Z_L(b)=Tr X_b^L. Hence both

    S(L,b)=Z_(2L)(b)/Z_L(b)^2,
    T(L,b)=Z_L(2b)/Z_L(b)^2

are purities of probability distributions. Source Proposition4.3 turns a finite
pair sufficiently near1 into a gap for every larger even length. This theorem
and its all-spin extension are prior work.

The task is not merely to approximate a ground vector: rigorous upper bounds
on Z_L need every uncomputed state counted. The construction below provides
that count at explicit finite dimension. It does not assume the desired gap.

## 2. Explicit spin matrices and signed translation

In the physical weight basis m=−2,...,2, the squared raising entries are4,6,6,4.
Each hopping entry of a bond is2,3, or sqrt(6); the diagonal is m_j*m_k.
The pi twist reverses hopping on the closing bond, leaving SzSz unchanged.
Thus H=H0+sqrt(6)H1 with integer sparse H0,H1. `spin_chain.py` constructs every
magnetization sector, not a selected subset.

Let R rotate the last letter to the front. At the pi seam, the commuting signed
translation acts by T|w>=(-1)^(m_last)|Rw>. On total magnetization M,
T^n=(-1)^M. Its eigenvalues are tau_k=exp[i(2*pi*k-pi*M)/n]. An orbit of length
r contributes at k precisely when n divides k*r. The orbit vector's coefficients
are the accumulated signs times tau_k^(−t)/sqrt(r). The implemented projection
therefore retains the seam phase rather than applying ordinary momentum to a
twisted Hamiltonian. Direct checks cover n=3,4,5,6 and both twists.

## 3. A counted low-energy trace enclosure

Let H be a finite Hermitian D-by-D block. Let Q have K columns, let c be a real
cutoff, and alpha>0. Suppose

    A=H-cI+alpha QQ* >0.                                  (1)

On ker Q*, H-cI=A>0. By min-max, H has at most K eigenvalues below c.
No correctness claim from the producer of Q is needed.

Suppose ||Q*Q-I||<=delta<1 and ||HQ-QD_theta||<=r, with real diagonal D_theta.
Set Qbar=Q(Q*Q)^(-1/2), a genuine isometry, and

    e=r/sqrt(1-delta)
      +2*sqrt(1+delta)*||D_theta||*((1-delta)^(-1/2)-1).

Then ||HQbar-Qbar D_theta||<=e. To see this, expand the residual after polar
normalization; the extra commutator is bounded by twice the distance of
(Q*Q)^(-1/2) from I. This is deliberately conservative.

Let P=I-Qbar Qbar*. The operator

    Htilde=Qbar D_theta Qbar* + P H P

differs from H by at most eta=2e: in the orthogonal two-by-two decomposition,
the compressed diagonal error and off-diagonal block each have norm<=e.
If max(theta)+eta<c, the trial subspace gives at least K eigenvalues below c,
so (1) gives the exact count. Moreover PHP has spectrum>=c-eta; otherwise Weyl
would force K+1 energies below c. The first K energies are consequently paired
with the ordered theta values within eta. All other energies are>=c. Therefore

    sum_i exp[-b(theta_i+eta+a n)] <= Z_block(b)
    Z_block(b) <= sum_i exp[-b(theta_i-eta+a n)]
                 +(D-K)exp[-b(c+a n)].                    (2)

For K=D, the Weyl pairing holds directly without a complement. For K=0 only
positivity and the tail are needed.

### Verification of (1)

The Cholesky routine supplies a candidate L, not a premise. Let epsilon bound
||A_true-LL*||. Compute an approximate inverse X of L and bound
rho=||I-LX||<1. Then

    ||L^-1|| <= ||X||_F/(1-rho)=B,
    lambda_min(A_true) >= B^-2-epsilon.                   (3)

A positive right side proves (1). Every block passed with a positive margin.

The actual `validate_trace.py` evaluates all scalar combinations with mpmath
interval arithmetic. For a complex D-term product it bounds rounding by
gamma_(8D+8), gamma_k=k*u/(1-k*u), u=2^-53, times Frobenius norm products.
Stored-array norm bounds also pay their complete positive-sum rounding error.
An additive1e-280 guard covers negligible underflow contributions. Residuals
are explicitly recomputed, so correctness of Cholesky, eigsh, and triangular
solve is not assumed. The claimed matrix bounds remain conditional on the
declared usual IEEE operation model for the executed products.

The orbit coefficients are independently enclosed with interval sin/cos and
sqrt; their error is below1e-14. Disjoint supports bound the projection error
by sqrt(n) times that coefficient error. Integer H0,H1 and an interval check
of sqrt(6), followed by COO accumulation bounds, give a matrix-input error
strictly below the declared conservative1e-9 for all used blocks. This is paid
in both the positivity and eigenvalue residual bounds.

The common c=-a*n+log(5^n/tail)/b is rounded upward, with tail=1e-5. Multiplying
by block dimensions and magnetization multiplicities then proves the TOTAL
tail bound. The largest count-validation margin at issue is not inferred from
selected good orbits or eigenvectors; all D=5^n states are covered.

## 4. An actual finite-ring MPS normalization

Let A_s,B_s be integer matrices and N=2M. The unnormalized amplitude is
Tr(A_s1 B_s2 ... A_sN-1 B_sN). Put E_A=sum_s A_s tensor A_s and similarly E_B.
For O_AB0+sqrt(6)O_AB1, insert the physical Heisenberg bond between A and B;
O_BA is defined analogously. Ordinary trace contraction gives

    V=Tr[(E_A E_B)^M],
    U0+sqrt(6)U1 =
       Tr[(E_A E_B)^(M-1) O_AB]
       +Tr[(E_B E_A)^(M-1) O_BA].                        (4)

The energy PER BOND is (U0+sqrt(6)U1)/(2V). The two-site unit cell accounts
for the factor2. All difference-of-charge blocks are included in (4).

`tebd_trial.py` uses established infinite TEBD to find a trial, with exact U(1)
support. The rounded tensors at scale10^8 retain that support. The subsequent
`mps_periodic_certificate.py --exact --n 64` uses Python arbitrary-precision
integer arrays throughout (4). It also constructs four-site physical amplitudes
explicitly and applies an independently built sparse H0+sqrt(6)H1, obtaining
the same norm and both numerator integers. No TEBD truncation-error claim enters
the variational inequality.

The resulting V>0 and integer comparison, using rational endpoints with
q_low^2<6<q_high^2, prove

    (U0+sqrt(6)U1)/(2V) < -4761/1000.

Thus E0(64)<−64*4761/1000 and Z64(b)>1 for EVERY b>0 at that shift. The
source reference4.76124816 is not thereby justified at arbitrary lengths.

## 5. A finite-input countermodel with all-length trace positivity

Read `data/moment_counting_witness_positive.json`. On a real Hilbert space let
each J eigenvalue act on the stated number of spin0 representations, and each
N eigenvalue act on that number of spin1 representations. X is diagonal on
these multiplicity spaces and scalar on each representation, hence is real,
self-adjoint, finite rank, and commutes with SO(3).

For every integer n,

    Tr X^n = J_n+3N_n,
    Tr X^n U_P = J_n-N_n,
    Tr X^n U_g = J_n+chi_1(g)N_n,  -1<=chi_1(g)<=3.        (5)

All eigenvalues are rational and all multiplicities are positive integers.
Exact Fraction arithmetic puts both expressions in (5) strictly inside each
acquired n=4,...,8 trace interval. The construction LP and floating root search
are only producers; their residuals are not used as evidence.

Two J eigenvalues equal v=11/10; every other modulus is<1069/1000. Directed
recurrence checks positivity of the two endpoint traces divided by v^n for
n=4,...,740. The minimum lower bound is2.566760436637393e-6, at n=7,I. For n>=741,
both normalized endpoint traces are bounded below by

    2-3*(dimJ+dimN)*(1.069/1.1)^n.

At741 this exceeds0.1049479742 and increases thereafter. Equations (5) then
give positivity for every proper rotation at every integer length>=4.

At every even n, the two equally largest eigenvalue weights imply p_max<=1/2,
so sum p_i^2<=1/2. This countermodel can never supply spatial purity>1/2 at
the tested beta. Its even traces exceed2v^n>1, including64.

Changing from a_ref to a=4.761 multiplies X by the positive number
exp[12*(a_ref-a)]. This multiplies each nth moment by exactly the trace-shift
conversion factor, preserving all the properties just proved.

The conclusion concerns the listed fixed-beta inputs. The local physical
kernel, physical Hilbert-space dimension at all temperatures, temperature
convexity for a common Hamiltonian, and the extra cyclic twist are additional
structure. No impossibility claim is made once that structure is supplied.

Qualitative uniqueness of a finite-temperature leading mode is also insufficient
to give a quantitative seed length from these inputs. Replace the two copies
of v by one v and one v+epsilon, with any rational0<epsilon<=10^-8. All acquired
moments increase by no more than8*epsilon*(1.1+10^-8)^7, below1.6e-7 and strictly
smaller than every upper-window margin. Exact rational arithmetic verifies this
uniform stability inequality. All twisted traces increase, so all-length
positivity and normalization survive. The largest modulus is now simple.
For any even n,

    S(n)<=p_max<=r^n/(1+r^n),  r=1+epsilon/1.1.

For any prescribed finite N, choosing epsilon<min(10^-8,1.1*log(5)/N) keeps
that bound<5/6 at every even n<=N. Thus even adding qualitative simplicity
does not extract a uniform finite seed-length bound from this snapshot data.
This remains a spatial fixed-beta family, not a local all-temperature model.

### Why the ordinary cyclic-twist repair is acknowledged

The alternative source initialization projects onto the A4-invariant sector.
Its moment is [Z(I)+3Z(P)+8Z(C)]/12. Each physical twisted partition function
is positive, hence this invariant eighth moment is>=Z8(I)/12>14.9094 at the
reference shift and beta12. A60-element average is likewise>=Z8(I)/60>2.9818.
Those masses cannot give a decaying remainder by the source's bare removal of
one unit-sized mode. This does not prohibit better polynomial, sector, or
temperature arguments, nor does it prove a continuum-beta lower bound.

## 6. Actual replay commands and scope

Run from this owned folder, with PYTHONDONTWRITEBYTECODE=1 and
OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=VECLIB_MAXIMUM_THREADS=2 (or1).

    python3 verify_bridge.py
    python3 validate_trace.py 8 0 --output <new-owned-output.json>
    python3 validate_trace.py 8 1 --output <new-owned-output.json>
    python3 mps_periodic_certificate.py --input data/tebd_trial_chi32.json \
      --n 64 --exact --output <new-owned-output.json>

The source full-column verifier was read through its mathematical appendices
and README, but was not rerun. This branch actually ran the cores named above,
plus `spin_chain.py`, `moment_attack.py`, `positive_moment_repair.py`, and the
ordinary MPS search cores. `verify_bridge.py` passed independently of those
producer imports; it does not redo their dense matrix calculations.

The first simple counting-spectrum witness is retained in
`moment_counting_witness.json` as a failed intermediate: its odd I trace at9
is negative. The weighted LP's first apparent success was also rejected by an
independently computed equality residual; rescaling the variables fixed the
solver conditioning. Neither is used as a scientific conclusion.
