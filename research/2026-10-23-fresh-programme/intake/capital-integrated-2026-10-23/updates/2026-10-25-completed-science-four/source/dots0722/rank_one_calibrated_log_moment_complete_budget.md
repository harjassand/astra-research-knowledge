# Calibrated logarithmic moment inequality and the rank-one noise budget

2026-10-25. New analytic proof. The two-point argument extends the root's logarithmic endpoint lemma to every positive shift. No numerical optimization is a premise.

## 1. Scalar theorem

Let T>0 be a random variable satisfying E[1/(1+T)]=1/2 and m=ET<infinity. For every R>=0,

2 E log(R+T) <= 2 log(R+1) + log((R+4m)/(R+4)).                 (1)

At R=0 a negative infinite logarithmic expectation is allowed. For R>0 all integrals exist because the mean is finite.

First consider the unique two-point law on u<1<v satisfying the reciprocal constraint. Its weights are

p=(v-1)(1+u)/(2(v-u)), 1-p=(1-u)(1+v)/(2(v-u)),
m=(1+u+(1-u)v)/2.

Let H be the right side of (1) minus its left side. At v=1 the law is concentrated at 1 and H=0. Direct differentiation gives

H'(v)/(1-u) = 2/(R+4m)
 + (1+u) log((R+v)/(R+u))/(v-u)^2
 - (1+v)/((R+v)(v-u)).

Use log z >= 2(z-1)/(z+1), z>=1. The resulting lower bound is

H'(v)/(1-u) >= N / [(R+v)(2R+u+v)(R+4m)],

N=2R^2+R(v-3)+2
  +u[(4v-2)R+2(v^2-v+1)].

Every denominator is positive. Since v>=1,

N >= 2R^2-2R+2 = 2(R-1/2)^2+3/2 >0.

Thus H>=0. This computation also holds at R=0 for u>0.

Every admissible law is a mixture of these reciprocal-calibrated two-point laws and the point mass at 1. For completeness, write d(u)=(1-u)/(1+u) below 1 and e(v)=(v-1)/(1+v) above 1. The reciprocal constraint gives a common flux L=integral d dmu_-=integral e dmu_+. If L>0, use the pair mixing measure

[d(u)+e(v)] mu_-(du) mu_+(dv)/L.

Within a pair use probabilities e/(d+e), d/(d+e). Integrating recovers exactly the original law. The remaining atom at 1 is unchanged. Integrate the two-point inequality and use concavity of log(R+4m) in the pair mean m. This proves (1) for arbitrary laws. At R=0 use monotone convergence of log(R+T) after subtracting an integrable upper bound, or take R down to zero.

## 2. The exact two-moment entropy comparison

Let S>0 satisfy

ES=1/4, E[q/(q+4S)]=1/2, 0<q<=1.

Set T=4S/q, m=1/q, R=4r/q. Equation (1) becomes

E log(r+S) <= log(r+q/4)+(1/2)log((r+1)/(r+q)).                (2)

Write h(r,s)=(r+s)log(r+s)-r log r-s log s, with continuous zero conventions, and define

U_r=2E h(r,S)-h(r,1),
D(r)=2h(r,q/4)-h(r,q)-U_r.

For r>0, differentiation under the expectation is valid (log(1+S/r) is integrable), and

D'(r)=2[log(r+q/4)+(1/2)log((r+1)/(r+q))-E log(r+S)] >=0.

Also D(0)=0. For the latter, h(r,S)<=h(r,ES) by concavity in S, so its expectation tends to zero. Consequently

U_r <= 2h(r,q/4)-h(r,q) = q f0(r/q) <= k q,                 (3)

where f0(a)=2h(a,1/4)-h(a,1) and k=(1/2)log(32/27). The last sharp scalar filter maximum occurs at a=1/8. This theorem covers all r>=0 and arbitrary scalar distributions with the two exact moments. It supersedes the restricted r>=1/9 certificate without invalidating it.

## 3. Receiving consequence: complete rank-one lower/rank-one noise budget

Use the previously proved physical interface in rank_one_spectral_filter_scalar_upper_interface.md. Let x=|u><u|, ||u||=1, b=B0|v><v|, and y=x/4+3b/8. Initially assume B0>0 and 0<|<u,v>|^2<1. Let s_i be y's two positive eigenvalues on span{u,v}, and

pi_i=|<u,e_i>|^2/(4s_i).

Then sum pi_i=1, sum pi_i s_i=1/4. If q=Tr(x-3b/2)_+, the rank-one secular equation gives

sum pi_i q/(q+4s_i)=1/2.

For every positive input block B=[[a,z],[z*,x]], with arbitrary finite-dimensional upper space and all upper Schur remainders retained, that interface gives

2 C([[a,z/2],[z*/2,y]])-C(B)
 <= sup_r [2 sum pi_i h(r,s_i)-h(r,1)].

Applying (3) proves

Gamma(x,b) <= k Tr(x-3b/2)_+.

The harmless sign on the output off-diagonal is removable by an upper block unitary. For zero noise and orthogonal noise the result follows directly or by continuity. For collinear noise, approximate v by noncollinear vectors in an enlarged lower space with zero-padded input; for every fixed input B, entropy continuity and continuity of the positive-part trace yield the same inequality. Taking the supremum only afterwards avoids an unjustified interchange of supremum and limit. Scaling extends the statement to arbitrary nonzero rank-one x and rank-one positive b.

This is a complete arbitrary-upper-dimension coherence theorem for rank-one x and rank-one b. It is not a proof for arbitrary lower x,b, and it is not the full WH3 entropy conjecture. Combining it with the separately established two-source diagonal budget closes the corresponding invariant-channel class whenever its diagonal data meet that two-source hypothesis (in particular c=0).

## 4. Verification and provenance

The root supplied the unshifted two-point logarithmic argument. The extension here keeps the same harmonic calibration while shifting the logarithm, rather than shifting and recalibrating its harmonic center. Symbolic differentiation independently checked the displayed H' identity, and exact rational algebra checked its logarithmic lower bound. The proof itself is the elementary displayed calculation and mixture construction; no finite diagnostic is used as evidence of universality.

## 5. Stronger receiving theorem: arbitrary positive noise b

The noise-rank restriction in Section 3 is unnecessary. Let x=|u><u| have trace one and let b be ANY positive semidefinite operator on the finite lower space. Put y=x/4+3b/8. On the positive spectral support of y define

pi_i=|<u,e_i>|^2/(4s_i).

Since y>=x/4, u lies in the support of y and <u|y^+|u><=4 (the rank-one Schur-complement criterion). Thus sum pi_i<=1. Add an atom of mass 1-sum pi_i at s=0. The resulting probability law satisfies ES=1/4 and leaves the kernel unchanged:

<u|(y+tI)^-1|u>/4 = E[S/(S+t)], t>0.

The zero atom contributes zero to both h(r,S) and the filtered coherence. For R>0 the two-point proof works directly with u=0: all logarithms and denominators are finite, and the same positive numerator applies. The flux decomposition therefore proves the scalar theorem for T>=0 without a calibration-preserving approximation. The integrated entropy theorem remains valid.

Let H=x-3b/2=2x-4y. Because H is a rank-one positive perturbation of a negative semidefinite operator, it has at most one strictly positive eigenvalue. If q=Tr H_+>0, the determinant/secular equation is

1=2<u|(qI+4y)^-1|u>.

Consequently, INCLUDING the added atom at zero,

E[q/(q+4S)]
 = 1 - <u|(qI+4y)^-1|u> = 1/2.

All scalar hypotheses now hold, and the same spectral-filter Jensen and balanced two-source entropy transfer prove

2 C([[a,z/2],[z*/2,y]])-C(B) <= k q.

If q=0, H<=0 gives y>=x/2. Then h_y(t)<=1/(2+4t), while the input kernel is 1/(1+t). For any 0<=g(t)<=1,

(1-h_y(t)g(t))^2 >= 1-g(t)/(1+t),

because 2h_y(t)<=1/(1+t). Hence the exact coherence-difference integrand is nonpositive pointwise, and the desired bound is zero.

Homogeneity finally gives the complete statement for every rank-one x>=0, every b>=0, and every positive block B with lower block x:

2 C([[a,-z/2],[-z*/2,x/4+3b/8]]) - C(B)
 <= (1/2)log(32/27) Tr(x-3b/2)_+.

The case x=0 is trivial because positivity forces z=0. No condition is imposed on the rank of b, commutation of x and b, the upper Schur remainder, or the finite upper dimension. This strengthens Section 3 and supersedes its noise-rank limitation. The remaining open coherence problem requires rank(x)>=2.

## 6. Actual full invariant-channel receiving class

Combine Section 5 with diagonal_positive_part_two_source_theorem.md. In the exact 1+8 invariant-channel block map, suppose x has rank at most one, b is arbitrary PSD, and

c=alpha x+beta b, alpha,beta>=0.

Then all diagonal data are nonnegative mixtures of the same two positive sources x,b. The complete diagonal theorem gives

Delta_diag(x,b,c)>=k Tr(x-3b/2)_+.

Section 5 gives the opposite bound on the coherence cost for EVERY allowed upper block a,z. Since the exact physical deficit is

Delta_full=Delta_diag+C_input-2C_output,

it follows that Delta_full>=0. This is an arbitrary-memory, genuinely noncommuting global class of the full 1+8 coherent channel. It includes all mixed upper Schur remainders; neither purity nor a graph ansatz is assumed.

This does not cover arbitrary c outside the two-source cone, nor rank(x)>=2. Purification or pinching cannot remove these restrictions because no required sign of the associated difference of coherence losses has been established.

## 7. Strictness at a fixed rank-one lower/noise pair

For a fixed finite-dimensional pair with 0<q<1, the calibrated law is nonconstant: otherwise its two moments force q=1. The logarithmic inequality in Section 1 is strict for every positive shift for any nonconstant law. Hence D'(r)>0 for r>0 and D(r)>0. Therefore U_r<q f0(r/q)<=kq for every r>0. The finite spectral law gives U_r continuous on [0,infinity), U_0=0, and U_r=-(1/2)log r+O(1) at infinity because ES=1/4. Its supremum is attained and is strictly below kq. Thus Gamma(x,b)<kq for 0<q<1. This is a pair-dependent strict gap, not a quantitative uniform margin.

At q=1, positivity implies b u=0. The usual noiseless graph on u attains k, and all additional orthogonal lower noise is incoherent and cancels. At q=0 the proved bound is zero and z=0 attains zero. These endpoint facts do not imply a uniform radius or margin near either endpoint.
