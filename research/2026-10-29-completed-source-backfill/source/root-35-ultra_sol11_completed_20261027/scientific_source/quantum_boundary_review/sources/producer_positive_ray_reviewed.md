# A finite receiver for every positive perturbation direction

This extends general leakage to a finite operation beyond reset form.
The unrestricted contraction is NOT_ESTABLISHED in this programme.
Independent root derivation supports the theorem; a separate peer challenge
is in progress. No physical input or historical priority is asserted.

## 1. Exact input/output/precision contract

Use qutrit A,B, logical L=C^r, Omega=sum_i|ii> UNNORMALIZED, p=P_Omega/3.
Let C>0 on L, 0<mI<=C<=MI, kappa=M/m. Let H>=0 be ANY density operator on
ABL, TrH=1, without rank, reset, alignment or commutation restrictions.
Put A0=P_Omega tensor C and ell=Tr[((I-p)tensor I)H].

If ell=0, positivity forces H inside p tensor I, and Delta(A0+epsH)=0.
If ell>0, compute with exact rational/integer comparisons

    L0=ceil_log2(24r/ell), K0=ceil_log2(4kappa),
    j=ceil(4K0/ell), k=2L0+j+1.                         (1)

Then EVERY 0<eps<=m*2^(-k) has the finite certificate

    Delta(A0+epsH)>=eps*ell/3.                          (2)

An arbitrary finite qutrit-reference direction can be embedded into reference
dimension 3r, padding at most two dimensions. That is a mathematical input
embedding, not acquired physical hardware.

Input acquisition is not constant cost. Reading H costs Theta((9r)^2)
entries, with ordinary PSD/order factorization costs. Also
k=O(log(r/ell)+(log kappa)/ell). Tiny ell can make k exponential in the
input bit length, and forming the endpoint eps costs k bits. There is no
uniform polynomial-bit claim without a non-negligible leakage promise.

## 2. Finite proof

By homogeneity normalize m=1, I<=C<=kappa I, t=eps/m. Let
P=p tensor I, Q=I-P, R=p_antisym tensor I, S=I-R, H1=NH. The exact identity
N*(S)=(3/4)Q gives

    TrQH=ell, TrS H1=3ell/4,
    TrPH=1-ell, TrR H1=1-3ell/4.                       (3)

N is CPTP, so H1>=0, TrH1=1, ||H1||<=1.

Input pinching, the positive-P-block tangent, and the scalar entropy bound
on the 8r-dimensional input kernel give

    f(A0+tH)-f(A0)
      >=t(1-ell)(1+log3)+t*ell log t
                                  +t*ell log(ell/(8r)).

The E baseline is full rank with least eigenvalue1/3, so

    f(EA0+tEH)-f(EA0)>=t(1-log3).

For the N term, two-block entropy coherence is subadditive and at most
tlog2 (WEAK_RESET_PROOF.md). For 0<t<=1<=kappa,

    f(NA0+tH1)-f(NA0)
      <=t(1-3ell/4)(1+log(2kappa))
                       +(3t*ell/4)log t+t f(SH1S)+tlog2.

Every eigenvalue of SH1S is at most one, hence f(SH1S)<=0. Combining the
three inequalities with Delta(A0)=0 and dropping favorable terms proves

    Delta(A0+tH)>=t[(ell/2)log(1/t)
                    -ell log(24r/ell)-2log(4kappa)].    (4)

Before dropping terms the right side additionally contains ell/2 and
+(3ell/2)log(2kappa) inside its bracket. They are nonnegative.
Under (1), t<=2^(-k) makes the displayed bracket at least

    [(ell/2)k-ell L0-2K0]log2
      >=(ell/2)log2>=ell/3.

Here log2>=2/3; restoring m proves (2). This is a theorem-level finite
estimate, not merely an epsilon-log-epsilon asymptotic.

## 3. An invariant of the actual reset/bath closure

For reset seeds X=P_Omega tensor C+I_A tensor Y, the physical off-diagonal
reference block X01=E01 tensor C has square zero. This is preserved under
positive scaling, scalar/reference white additions, the actual operator-
bath lift X->X tensor U+I tensor V, flagged reference direct sums,
reference isometries and reference unitaries. Physical-unitary covariance
also preserves it: the maximally-entangled transpose identity makes the
off-diagonal block reference-unitarily conjugate to E01 tensor C.

This claim is limited to that declared reset/bath closure. It is not an
invariant of every independently known positive WH3 source class.
Unflagged sums with unrelated embeddings are not proved closure operations.

A literal target excluded by this closure is

    T_B=diag(1,-1,0), S_A=E01+E10,
    H_star=[I9+(1/4)S_A tensor T_B]/9.                  (5)

It is a density operator, H_star>=I9/12, Tr_B H_star=I3/3. Its off-diagonal
block T_B/36 has nonzero square. This exclusion is structural, not a
negative entropy deficit.

## 4. A new admitted point outside that closure

For r=1,C=m=M=1,H=H_star, ell=8/9,L0=5,K0=2,j=9,k=20.
The source

    X_star=P_Omega+2^(-20)H_star                        (6)

is certified by (2), whereas

    (X_star)01=E01+2^(-20)T_B/36,
    [(X_star)01]^2=2^(-40)diag(1,1,0)/1296 !=0.        (7)

Thus (6) is admitted by the new positive-ray operation and excluded by the
entire reset/bath closure listed above. It is not merely a larger reset
fixture. It is already a TP Choi source after scalar normalization:
Tr_B X_star=(1+2^(-20)/3)I3. Its normalized state is X_star/(3+2^(-20)).
The antisymmetric-isometry construction gives a literal alpha3 extension
with the certified nats margin

    I(Q1:Q2|R)-log3 >=8/[27(3*2^20+1)].                (8)

No extra flag is needed for this fixture. For a general H with nonuniform
physical marginal, the nine-Weyl flagged twirl of WEAK_RESET_PROOF.md
preserves normalized deficit and makes a TP Choi state. Reference dimension
grows from 3r to 27r. Physical implementation would require the nine
controlled Weyl choices and classical labels; those resources are not free.

## 5. What this operation does not supply

The finite receiver qualifies every positive-admixture direction near an
isometric equality source. Iteration does not yet reach an arbitrary
target: the premise requires the ORIGINAL isometric A0, not an arbitrary
previously accepted state. No positivity-preserving unflagged interpolation
or general channel-composition theorem is inferred.

C,H and exact margins are digital mathematical inputs/outputs. Physical
tomography, state preparation and CMI measurement are not acquired.
Historical priority and a civilisation-level capability are not established.
The unrestricted contraction remains NOT_ESTABLISHED in this programme.
