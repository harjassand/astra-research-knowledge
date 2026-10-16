# Homogeneous generator reduction and a certified 32-generator value

Date: 2026-10-16. Separate extension; PROOF.md is unchanged. This uses standard permutation-symmetry reduction, not a claim of novelty for the symmetry method. It applies to the exact Schur-refresh optimization proved in that file.

## Exact reduction

Suppose all m independent generator multipliers equal the real number eta in [-1,1]. Full nonzero binary sector labels have K=2^m-1, c_j=eta^|j| and B_jk=eta^|j xor k|. The original objective is

f(z)=2h Re(c†z)-alpha z†Bz,
alpha=pq, h=sqrt(pq(1-p)(1-q)), ||z||_1<=1.

Since B is real positive semidefinite, writing z=x+iy gives z†Bz=x^T Bx+y^T By. Replacing z with x weakly improves f and does not increase its l1 norm. Hence a real maximizer exists.

Permuting the m bit positions preserves B, c, and the l1 ball. Average a real maximizer over the permutation group. Concavity makes the averaged objective no smaller; convexity preserves feasibility. Therefore there is an optimizer constant on each Hamming-weight class: z_j=x_w when |j|=w. Put N_w=binom(m,w) and u_w=N_w x_w. Then

||z||_1=sum_{w=1}^m |u_w|,
c^T z=sum_{w=1}^m eta^w u_w.

For any fixed label j of weight w, exactly binom(w,l)binom(m-w,v-l) labels k of weight v have overlap l and distance w+v-2l. Consequently the reduced matrix is

Bbar_wv = [sum_{l=max(0,v-(m-w))}^{min(w,v)} binom(w,l)binom(m-w,v-l) eta^(w+v-2l)] / binom(m,v),

for 1<=w,v<=m. Equivalently, let S_jw=1/N_w when |j|=w and zero otherwise. Then Bbar=S^T B S, proving that Bbar is symmetric positive semidefinite, despite the asymmetric-looking counting formula.

The exact endpoint value is thus

F=Q+max_{u in R^m, ||u||_1<=1} [2h sum_w eta^w u_w-alpha u^T Bbar u].

This is an exact value reduction from exponentially many complex coordinates to m real coordinates. It includes negative eta, although the bounded example below uses positive eta.

## Full-dimensional certificates without full-dimensional vectors

Let d_w=eta^w. For any reduced vector v, symmetry ensures that the full gradient h c-alpha B S v is constant on every weight class, with class-w entry h d_w-alpha(Bbar v)_w. Therefore the original full-space tangent certificate is exactly

max f <= alpha v^T Bbar v + 2 max_w |h d_w-alpha(Bbar v)_w|.

Any feasible reduced u supplies the original lower bound f(Su). No full vector of length 2^m-1 is needed to compute either bound, and matching bounds certify the full unrestricted problem, not just a numerical symmetry-restricted relaxation. The separately proved symmetry reduction would also suffice to transfer a reduced optimum.

## Bounded numerical search followed by exact rational certification

Only preinstalled NumPy/SciPy and Python Fraction were used. The script check_homogeneous.py uses a split-variable simplex representation u=u_plus-u_minus, u_plus,u_minus>=0, sum(u_plus+u_minus)<=1, and SLSQP with a 500-iteration hard cap. It then rounds to denominator 10^10, rescales radially if necessary to guarantee exact l1 feasibility, and evaluates exact rational primal/tangent bounds. Solver success is not used as the mathematical certificate.

For m=32, eta=1/4 and p=q=1/4, the unconstrained l1 condition fails substantially:

3[(5/4)^32-1] = 69793852863939760017027 / 18446744073709551616 > 1.

SLSQP terminates in six iterations. The rational candidate is exactly u_1=1, u_w=0 for w>1. Here

Bbar_11 = [1+31(1/4)^2]/32 = 47/512,
f(u) = 3/32-(1/16)(47/512) = 721/8192.

The tangent gradient has entries

g_w = (1/4)^(w-1) (352-15w)/8192.

The exact maximum absolute entry is at w=1, namely 337/8192. Thus

alpha u^T Bbar u + 2||g||_infinity
=47/8192+674/8192=721/8192=f(u).

Adding Q=7/16 proves the exact full-sector answer

F = 4305/8192 = 0.5255126953125.

The certificate gap is zero. There are 4,294,967,295 original bad-sector coordinates; none of their full arrays or matrices were constructed in this example.

The same pipeline at m=2 reproduces u_1=1 and the exact F=255/512 from PROOF.md. Independently, for every m=1,...,5, the script constructs the full binary-label matrix and checks every reduced entry against the exact class-average formula. All checks pass; results are saved in homogeneous_results.json. This is one bounded large homogeneous example plus the requested small validation cases, not a broad solver campaign.

## Cost and limitations

Precompute binomial coefficients and eta powers. Direct construction of the m-by-m reduced matrix uses O(m^3) rational arithmetic operations and O(m^2) storage. A dense reduced objective or tangent evaluation uses O(m^2) arithmetic. Integer coefficient size, rational numerator/denominator bit growth, requested numerical tolerance, and optimization conditioning still have to be charged. For rational eta, the displayed finite sums have polynomial-size exact representations in m and the input bit length; a generic optimizer is not promised to be rational or to have a simple closed form.

This removes the explicit exponential sector representation for the homogeneous value and its certificates. It does not prove a polynomial-in-m algorithm for arbitrary unequal generator multipliers. It also does not shrink the physical equality witness dimensions or change the full-channel/privacy/commutation assumptions of the underlying theorem.

## Closed certificate for this benchmark family

Root's further observation certifies the whole specific family p=q=eta=1/4 for every integer m>=2. Take u=e_1. Then

Bbar_11=(m+15)/(16m),
g_w=4^{-(w-1)}(11-15w/m)/256.

At w=1, g_1>=14/1024. For w>=2, because w<=m, |11-15w/m|<=11, and therefore |g_w|<=11/1024<g_1. Thus the tangent infinity norm is exactly g_1, matching the candidate's primal value, and

F=(135m-15)/(256m).

In particular m=32 gives 4305/8192 and m=64 gives 8625/16384. The bounded computation above was performed at m=32 only (plus m=2 and the small full-matrix checks); the m=64 value follows algebraically. This closed expression is specific to these p,q,eta, not a general homogeneous optimizer formula.
