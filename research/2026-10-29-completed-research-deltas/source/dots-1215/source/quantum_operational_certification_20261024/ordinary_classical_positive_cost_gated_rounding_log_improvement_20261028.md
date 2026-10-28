# Parallel group gates: logarithmic positive-cost cube rounding and a matching SDP gap

28 October 2026. Author construction, with the parent contributing the sharper affine-covariance simplification; independent receiving pending. This strengthens, without editing, `ordinary_classical_positive_cost_gated_rounding_20261028.md` (SHA `d30bebfe86d4abc4154482d9b3a435de247c09e9dbc2ecf164dcabafbfa99e01`). The scope is a known product binary action set, not arbitrary full-CPTP decoders.

## 1. Setting and simultaneous cost-preserving covariance

Let N(z)=||a_0+sum_i a_i z_i||^2=(1,z)^T A(1,z), A>=0, z in{0,1}^n, and u(z)=m+sum w_i z_i with m>0,w_i>=0. A feasible moment matrix satisfies M>=0,M_00=1,M_0i=M_ii=p_i. Put d=m+sum w_i p_i,F=Tr(A M)/d and supply a>=max(1,||A||op).

Use delta=min(1/2,m/(64an)), discard p_i<delta, and partition the retained indices into L nonempty dyadic groups I with p_i in(p_I/2,p_I]. For EVERY group independently, form

    Y_I=M_I/p_I+diag(1-p_i/p_I),
    s_I=sign(N(0,Y_I)), B_I~Bernoulli(p_I),
    z_I=B_I(1+s_I)/2.

Concatenate all these group outputs, with zeros on the tail. Every output is a feasible binary vector. Across different groups the full random records are independent. Within a group, E z_I=(p_I/2)1 and

    Cov(z_I)=(p_I/4)E s_I s_I^T
             +p_I(1-p_I)11^T/4
            >= M_I/(2pi).                                (1)

Therefore

    E zz^T =Cov(z)+(E z)(E z)^T
            >=(1/(2pi)) blockdiag_I M_I,
    E u(z)<=m+sum_keep w_i p_i<=d.                        (2)

This covariance calculation is what permits simultaneous rounding despite arbitrary signs in the cross-group entries of A. One cannot merely discard cross-group expectation terms without it. The baseline cost m is paid ONCE, removing the extra grouping factor in the predecessor's one-group selection.

## 2. Approximation and finite cap

Put S_keep=Tr(A_keep M_keep) and S_I=Tr(A_II M_I). PSD Cauchy gives S_keep<=L sum S_I. If F>=1 and R_0=N(0)/m<F/4, the predecessor's tail calculation gives S_keep/d>=F/16. Equations(1)-(2) imply

    E||sum a_i z_i||^2 >=sum_I S_I/(2pi)
                           >=F d/(32pi L).

In fact the affine offset costs nothing in this step: writing B for the matrix with columns a_i,

    E N(z)=||a_0+B E z||^2+Tr(B^T B Cov z)
           >=sum_I S_I/(2pi)>=F d/(32pi L).

The baseline is needed only to ensure that S_keep controls the full relaxation numerator. Consequently

    max{R_0, E N(z)/E u(z)} >= F/(32pi L).                 (3)

The L=0 case is covered by the baseline. For a fully capped algorithm with L>=1, put

    t=F/(1024 L).

If R_0>=t, return zero. Otherwise the SMALL baseline case applies, and

    E[N(z)-2t u(z)] >=(32/pi-2)t d>6t m.                   (4)

As N(z)<=a(n+1), a successful sample N(z)>2t u(z) has probability at least t m/[a(n+1)], even after sufficiently small finite coupling error. Thus

    ceil[a(n+1)/(t m) log(1/beta)]                        (5)

independent simultaneous-rounding trials suffice except probability beta. Return the largest actually evaluated ratio among all trials and the baseline. All policies are feasible even on failed histories. For F<1, returning the baseline incurs at most additive-one relaxation loss.

The finite moment SDP, Gaussian sign sampling, rational evaluation and cap accounting are as in the independently received predecessor. The Gaussian coupling may be allocated across all groups; their total number of coordinates is at most n. Marginal variance one permits sign anti-concentration without any spectral floor. Numerical cost is polynomial in n,a,1/m and log(1/beta), not necessarily in log a. For the targeted leverage application a and1/m are already polynomial numerical bounds.

Thus the weighted PSD quadratic ratio on a product binary cube has an O(log(an/m)) relaxation rounding factor, with an additive constant and polynomial classical cap. The cost guarantee is real, not numerator-only Gaussian rounding. There are no new physical source calls in this classical subroutine.

## 3. The logarithmic loss is necessary for this basic moment relaxation

For any n>=1, take exact rational data

    m=1, a_0=0, a_i=2^i, w_i=4^i, p_i=4^(-i),
    r_i=2^(-i), i=1,...,n,
    M=[[1,p^T],[p, p p^T+(1/2)r r^T+diag(p_i/2-p_i^2)]].  (6)

This is strictly positive definite: its Schur complement is the displayed PSD rank-one term plus a strictly positive diagonal. Its diagonal satisfies M_ii=p_i and M_0i=p_i. Let A be the rank-one Gram matrix of (0,2,4,...,2^n). Then

    Tr(A M)=(sum_i 2^(-i))^2+n^2/2+n/2-sum_i4^(-i)
             >=n(n+1)/2,
    m+sum w_i p_i=n+1,
    F>=n/2.                                              (7)

For every nonzero binary z, let j be its largest active index. Geometric domination gives

    sum_i2^i z_i <2^(j+1),
    u(z)>=1+4^j,
    N(z)/u(z)<4.                                         (8)

The zero vector has ratio0. Hence the basic SDP integrality gap is at least n/8. Here ||A||op=sum_i4^i and log(an/m)=Theta(n), so the logarithmic order of(3) cannot in general be removed while retaining this particular basic moment relaxation. This is a gap only for the displayed BASIC PSD moment relaxation. For example M_12=5/64>p_2=1/16, so these feasible SDP moments violate the valid binary/RLT pairwise inequality M_ij<=min(p_i,p_j). The construction does not establish a logarithmic gap for an RLT-strengthened relaxation. It is not an unconditional hardness lower bound for cube optimization and not a physical acquisition lower bound. Moreover a grows exponentially with n in this family: the fixed cap's polynomial numerical-magnitude guarantee is not strongly polynomial or polynomial in arbitrary input bit length.

## 4. Scientific scope

The construction exploits independent product-coordinate groups. A full-CPTP decoder cannot in general be assembled by independently gating Choi-coordinate groups while preserving positivity and its input partial trace. The positive dual cost u(C)=m+Tr(WD) alone does not supply such a product representation. No change to the received generic k^6 source exponent follows without an additional genuine matrix-valued feasible rounding theorem. The equally informed conventional learner has all of the same classical controls.
