# Equality for arbitrary pure main plus isotropic reset

Status: separate consequence of the independently received `arbitrary_pure_main_isotropic_reset_whole_value_theorem.md`; root independently corroborated the classification. No decoder or mixed-main extension.

For finite reference space, X=|psi><psi|+I3 tensor Y, Y>=0, the homogeneous deficit is zero exactly when either psi=0, or psi is a nonzero scaled maximally entangled rank-three vector and Y annihilates its reference Schmidt support. The zero operator is included in the first case. No normalization is needed.

Write psi=sum_i |i> tensor v_i, Psi=[v_i], and K(s)=Psi*(Y+sI)^-1 Psi. The whole theorem gives F(K)>=F(rI), r=sqrt(e2(K)/3), and the integral of the scalar comparator is nonnegative.

If the main has rank one and is nonzero, K has one positive eigenvalue x(s), and F(x,0,0)>0: its derivative is 2x/[(x+1)(x+2)(x+3)] and its value at zero is zero. Thus the original integral is strictly positive.

If the main has rank two, K(s) is nonzero nonscalar for every s>0. The strict pair compensation in the whole theorem gives a strictly positive balancing gap at every such s (balancing a positive and zero eigenvalue first produces three positive eigenvalues). A compact interval gives a positive integral gap, hence strict original deficit. The same argument applies to a rank-three main whenever K(s) is nonscalar at even one positive s: continuity gives a positive gap on an interval.

Consequently equality with nonzero main forces K(s)=h(s)I3 for all s>0. Write the ORIGINAL finite spectral decomposition Y=sum_lambda lambda P_lambda. Uniqueness of rational partial fractions gives
Psi*P_lambda Psi=mu_lambda I3, mu_lambda>=0.
In particular Psi*Psi=c I3 with c=sum mu_lambda>0. The main is scaled maximally entangled. This scalar clock is realized EXACTLY, without a measure limit, by the finite physical-CQ source with three identical reset blocks diag(lambda), logical success vector with coordinates sqrt(mu_lambda/c), and main amplitude sqrt(c). Unoccupied reset eigenspaces contribute only zero-deficit spectators. The exact determinant integral gives equal homogeneous deficits for original and auxiliary sources.

Apply the equality classification in `pure_success_arbitrary_cq_reset_bath_collapse_theorem.md` (sections 1 and 6). If reset is absent the pure maximally entangled source has zero deficit. Otherwise normalize the finite auxiliary source; its nonzero main and reset weights are both positive. Zero deficit forces every positive reset eigenvalue to have zero success overlap, i.e. mu_lambda=0 for every lambda>0. Therefore Y Psi=0. Conversely that condition gives an orthogonal reset/main split; the reset product summand and the scaled maximally entangled pure summand both have zero deficit.

Strictness is obtained either from an actual positive balancing gap or from an EXACT finite scalar spectral-effect receiver. It is not inferred from strict positivity along growing-dimensional approximants.
