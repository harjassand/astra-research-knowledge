# Uniform qubit residual-to-EB bound by a slow-mode affine chord

2026-10-29. Frozen analytic candidate; independent receiving review pending. No historical novelty claim.

Version: conservative constant 19200. The original draft is retained unchanged; future improvements must be separately versioned.

## Result
Let Psi be a qubit CPTP channel whose Bloch linear matrix T has s1(T)^2+s2(T)^2<=1, and let sigma be any fixed state of Psi, meaning Psi(sigma)=sigma. Self-compatibility is a sufficient condition for this singular-value premise, as proved below. Then there exists a CPTP entanglement-breaking qubit channel F fixing sigma and a Hermiticity-preserving linear map L such that

`id - F = L (id - Psi)`, `||L||diamond <= 19200`.

Consequently, for every finite quantum reference and every state rho,

`T(rho,(F tensor id)rho) <= 19200 T(rho,(Psi tensor id)rho)`.

The constant is deliberately crude. The near-preserved-mode construction has coefficient 72; the large final constant comes only from a crude 3x3 inverse bound in the uniformly separated case. This theorem does not assume unitality, faithfulness of sigma, normality, diagonalizability, or a positive-weight EB channel component.

Applied to the accepted actual-prior universal recovery Psi=R_sigma,Phi Phi of a self-compatible qubit Phi, self-compatibility survives applying R separately to its two outputs. Here sigma is the actual input mean and is fixed by Psi, NOT necessarily by Phi. For a finite ensemble without a reference, or with actual product mean sigma tensor omega on AR, define delta as the actual Holevo loss under Phi (respectively Phi tensor id_R). The accepted recovery theorem gives average residual <=sqrt(delta), hence one prior-adapted EB F has average error <=min(1,19200 sqrt(delta)), independently of the reference dimension. F tensor id_R is EB on A only, not globally EB on AR. An arbitrary correlated barycenter is not covered. This is a new analytic candidate, not a received theorem.

For faithful sigma, use the accepted CPTP support completion of the universal recovery outside supp Phi(sigma); it does not alter any relevant output. A singular qubit mean is pure, and every supported ensemble letter factors as sigma tensor its reference marginal, so replacement by sigma gives zero disturbance directly. The constants use natural-log Holevo loss. Implementing the prior-adapted comparator assumes the channel and prior are specified; no finite-data acquisition guarantee is asserted.

## 1. Compatibility singular-value inequality, including bias
Write the affine Bloch action r -> T r+t, with singular values s1>=s2>=s3. Pull back output Pauli measurements on the first two left singular axes through the two different output copies. Their Bloch vectors a,b are orthogonal of lengths s1,s2, though their scalar biases may be nonzero. For their joint effects G_st=(gamma_st I+g_st.Pauli)/2, positivity gives |g_st|<=gamma_st, normalization sum gamma_st=2, and marginal vector identities give a+b=g_++-g_--, a-b=g_+--g_-+. Therefore |a+b|+|a-b|<=2, so s1^2+s2^2<=1. In particular ||T||<=1 and ||wedge^2 T||=s1 s2<=1/2.

## 2. No eigenvalue near +1: replacement is enough
Suppose T has no real eigenvalue lambda>=99/100. Since T is real 3x3, any nonreal eigenvalues are conjugates. Every product of two eigenvalues has modulus <=||wedge^2 T||<=1/2. Thus at most one eigenvalue has modulus >1/sqrt(2), and a nonreal pair always has modulus <=1/sqrt(2)<3/4. All real eigenvalues lie in [-1,99/100).

It follows that |det(I-T)| >= (1/100)(1/4)^2=1/1600: among the three factors, at most one requires the 1/100 bound, and the other two are >=1/4. Since ||I-T||<=2, the largest singular value of adj(I-T) is at most4. Thus ||(I-T)^-1||<=6400.

Take F=replace_sigma, and define L(I)=0, L(Pauli_j)=sum_i[(I-T)^-1]_ij Pauli_i. Both deficits vanish on sigma, so their traceless-space identity extends to all operators. The rank-one Pauli-column bound gives ||L||diamond<=3||(I-T)^-1||<=19200.

## 3. A real slow eigenvalue
Now let lambda>=99/100 be real and g=1-lambda in[0,1/100]. Choose a real unit LEFT eigenvector w, T^T w=lambda w. In the orthonormal decomposition R w direct-sum w-perp,

`T = [[lambda,0],[a,B]]`, `s=(u,v)` for the fixed prior Bloch vector.

For every unit z in w-perp, the area of T w and T z is at least lambda |Bz|, because T w=(lambda,a) and T z=(0,Bz). Hence

`b:=||B|| <= ||wedge^2 T||/lambda <= 1/(2lambda) <= 51/100`.

Therefore `lambda-b>=12/25`, `1-b>=49/100`. The norm of T w gives `|a|<=sqrt(1-lambda^2)<=sqrt(2g)`. Define

`h=(lambda I-B)^-1 a`, `n=(1,h)`.

Then Tn=lambda n and w.n=1. Also `|h|<=sqrt(2g)/(lambda-b)<=5/16` (the final loose bound uses sqrt(.02)<.15).

Let `k=1-16g` (so 21/25<=k<=1). Define F by measuring the projectors onto the +/-w states and preparing states with Bloch vectors

`r_+ = s+k(1-u)n`, `r_- = s+k(-1-u)n`.

The resulting affine matrix is T_F=k n w^T and translation s-T_F s. It fixes sigma. What remains is to prove |r_+|,|r_-|<=1.

## 4. Positivity of both prepared endpoints
Because sigma is fixed, t=(I-T)s. The actual channel outputs on the +/-w pure states have first coordinates `u+lambda(+/-1-u)` and perpendicular coordinates

`x_+ = (I-B)v+a(1-u)`, `x_-=(I-B)v-a(1+u)`.

Put q_+=1-u, q_-=1+u. Output positivity gives

`|x_+|<=sqrt(2g q_+)`, `|x_-|<=sqrt(2g q_-)`,

since the exact radial slack is 2g q-g^2 q^2.

With p=(1+u)/2, p x_+ +(1-p)x_-=(I-B)v. The scalar inequality

`p sqrt(1-u)+(1-p)sqrt(1+u) <= sqrt(1-u^2)`

therefore gives `|v|<=sqrt(2g(1-u^2))/(1-b)`. In particular, for EACH sign,

`|v| <= [2/(1-b)] sqrt(g q_sign) < 5 sqrt(g q_sign)`.

Let `y_sign=v+(+/-1-u)h`. Using (lambda I-B)h=a gives

`(lambda I-B)y_sign=x_sign-g v`.

Hence

`|y_sign| <= [sqrt(2)+2g/(1-b)]/(lambda-b) * sqrt(g q_sign)`

and the bracket is <4 using g<=1/100, 1-b>=49/100, lambda-b>=12/25, and sqrt2<3/2.

The perpendicular part of r_sign equals `k y_sign+(1-k)v`, so its norm is at most `5 sqrt(g q_sign)`. Its first coordinate is +/-[1-16g q_sign]. The available radial slack is

`1-(1-16g q)^2 =16g q(2-16g q) >= (672/25)g q >=25g q`,

because q<=2 and g<=1/100. This dominates the squared perpendicular norm. Thus both prepared endpoints are valid states. F is explicitly a two-outcome EB CPTP channel.

## 5. Uniform deficit quotient
Set D=(I-B)^-1 and define the real 3x3 matrix

`Lmat=[[16,0],[(16I-D)h,D]]`.

Direct block multiplication, including at g=0, proves

`I-T_F = Lmat (I-T)`.

Indeed a=(I-B-gI)h and 1-k=16g. The bound

`||Lmat|| <=16+(16+100/49)(5/16)+100/49 <24`

follows by a three-block triangle bound. Define L(I)=0 and use Lmat on the Pauli subspace. Both deficits annihilate sigma, so the identity holds on all operators. Each Pauli-column map has diamond norm its Euclidean column length, giving ||L||diamond<=3||Lmat||<72.

The lambda=1 endpoint causes no inversion problem: a=0, positivity of actual +/-w outputs implies v=0, h=0, and F is ordinary dephasing in w. The same block identity still holds.

## Dependencies and limits
This is an elementary qubit channel geometry proof under the stated singular-value premise, which self-compatibility implies. It does not repair the rejected trace-nonincreasing left-resolvent claim. Its application to Holevo loss uses accepted universal averaged rotated-Petz recovery with its CPTP support completion, actual-prior identity, and product-barycenter reference factorization. No cheap recovery/measurement acquisition or many-noisy-qubit tensorization follows. No historical priority is asserted.

## Source dependencies for the Holevo application
The structural proof above is self-contained. Its recovery application imports the already reviewed universal-recovery theorem and support handling in `producer-workspace/REVIEW.md` and `producer-workspace/REVIEW.md`, based on Junge--Renner--Sutter--Wilde--Winter, arXiv:1509.07127v3, Theorem 2.1 and Remarks 2.2, 2.4. The trace-nonincreasing ordering obstruction remains exactly as recorded in `producer-workspace/TNI_ORDERING_OBSTRUCTION.md`; no such resolvent is used here.
