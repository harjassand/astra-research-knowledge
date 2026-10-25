# Independent audit: noncommutative operator Schur-log transport

2026-10-25. **PASS.** `operator_schur_log_transport_theorem.md` establishes the stated Loewner comparison K_1(H,V)>=2K_beta(H,V), beta>=4, for PSD H,V satisfying H+V<=beta(beta-2)I, and its exact block-logarithm receiver. The proof does not assume H,V commute. The higher-rank trace-to-operator gap is correctly retained.

## 1. Norm convergence and faithful denominators

For s>0,

D_r(s)=(r+s)(V+sI)+sH >=(r+s)sI>0.

Therefore

0 <= [s/(r+s)]D_r(s)^-1 <= I/(r+s)^2.

This one bound proves norm integrability both at zero and at infinity, even if H or V is singular. The proof's separate near-zero and infinity estimates are consequently valid. No inverse at the isolated endpoint s=0 is needed.

## 2. The transport compares operators in the correct direction

Write W=beta(beta-2), R=W+1, and Delta=WI-H-V>=0. Expanding the denominators gives

D_1(s)=s(s+R)I-s Delta+V,
D_beta(t)=t(t+beta+R-1)I-t Delta+beta V.

Let N1=s(s+R), Nb=t(t+beta+R-1). Under the already audited exact positive scalar transport, the difference D_beta/Nb-D_1/N1 has coefficients

[s Nb-t N1]/(N1 Nb),
[beta N1-Nb]/(N1 Nb)

on Delta and V, respectively. The first numerator is st(t-s+beta-1), and the second is beta s(s+R)-t(t+beta+R-1). Both are nonnegative by the exact factorizations in the general-cap scalar proof, independently checked in the preceding audit.

Thus the difference is PSD as a sum of nonnegative scalar multiples of PSD matrices. No product of noncommuting PSD matrices is used. Both normalized denominators are faithful. Inverse operator monotonicity reverses their order, giving precisely

[D_1/N1]^-1 >= [D_beta/Nb]^-1.

The positive change of scalar measure converts the second integral to 2K_beta. Therefore integrating this pointwise Loewner inequality proves K_1>=2K_beta. The positive transport and inversion order are both essential and both are correct.

## 3. Rectangular block inversion independently reconstructed

For V>0, the block pencil

X_r=[[rI+ZZ*, Z sqrt V],[sqrt V Z*,V]]

is faithful since the Schur complement of V is rI>0. After adding sI, its upper Schur complement is

(r+s)I+s Z(V+sI)^-1 Z*.

Set a=r+s and H=Z*Z. Woodbury gives its inverse as

I/a-(s/a)Z[a(V+sI)+sH]^-1 Z*.

This confirms the factor s/(r+s), including rectangular Z and noncommuting V,H. There is no extra factor of r+s. Subtract this compressed resolvent from I/(r+s), and integrate the logarithmic resolvent identity. Norm convergence just established permits the fixed Z factors to pass through the integral. The result is exactly

Q log X_r Q-log r I=Z K_r(H,V)Z*.

Congruence preserves Loewner order, so the operator-integral theorem gives the claimed block-logarithm comparison. No common eigenbasis or simultaneous physical measurement is invoked.

## 4. Exact higher-rank receiving normalization

The stated source application can be made fully explicit. Let Q have rank k, A=aQ, and B=(a/R)X_1. At p=1/beta and q=(beta-1)/beta,

pA+qB=(aq/R)X_beta.

The compressed survivor is therefore

2Q log X_beta Q-Q log X_1 Q-2log beta I,

because all scale terms cancel using q^2/R=1/beta^2. The operator theorem makes this nonpositive whenever H+V<=WI.

The equal-trace condition is exactly

Tr(H+V)=k(R-1)=kW.

For k=1 this trace bound automatically implies the required operator cap. For k>1 it does not. This precisely identifies the missing allocation step rather than silently replacing a trace constraint by a Loewner constraint. Flatness and the saturated scalar Schur complement are additional structural assumptions in this receiver, not consequences of arbitrary higher-rank singularity.

## 5. The noncommutative higher-rank receiving class is nonempty

A simple exact example verifies that the operator hypothesis is not vacuous under equal trace. Take beta=4, R=9, W=8, upper dimension k=2, environmental dimension 3,

H=diag(2,1,0),
V=[[4,1,0],[1,4,0],[0,0,5]],
Z=[[sqrt(2),0,0],[0,1,0]].

Then Z*Z=H, V>0, [H,V]!=0, Tr(H+V)=16=kW, and

8I-H-V=[[2,-1,0],[-1,3,0],[0,0,3]]>0.

The latter positivity follows from principal minors 2,5,15. Thus A=aQ and B=(a/9)X_1 are actual equal-trace, rank-two-singular versus faithful comparison matrices satisfying the proved interface. Choosing a=1/2 normalizes both traces to one. This is an illustrative exact member of the theorem, not numerical evidence standing in for its proof.

## Conclusion and limits

The Loewner lift is valid and genuinely noncommutative. It supplies a higher-rank block-logarithm comparison under a specific operator resource bound, and an actual nonempty singular-boundary receiving class. It does not establish that equal trace supplies that bound for general rank, does not handle arbitrary nonflat A, and does not settle faithful active-cap endpoints or unrestricted WH3.
