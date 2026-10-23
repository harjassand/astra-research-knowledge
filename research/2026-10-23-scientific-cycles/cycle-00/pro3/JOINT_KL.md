# Two directions of relative entropy restore a uniform hybrid bound

Principal construction with independent tail/anchor refinements, Astra PRO3, 21 October 2026. This extends the checkpoint in `PROOF.md` Section 8. The former nested-exponential bound is superseded below. Sharpness is established when 0<J<=K; the regime J>K remains open. This is an internally checked result; historical novelty and external acceptance are not asserted. The principal supplied indicator smoothing and the shared core argument; an independent challenger supplied the sharper outside-mass accounting and fixed-anchor Dirichlet inequality used here.

## 1. Setting and question

Let equivalent probability measures pi,q satisfy

    D(pi||q)<=K, D(q||pi)<=J, K,J>0.

Write W=dpi/dq. Let G be independence MH with proposal q, let L be any fixed pi-reversible Markov kernel, and fix 0<alpha<1. The **lazy random mixture** is

    C = [I + alpha G + (1-alpha)L]/2.

The chain starts with one draw from q. This theorem concerns this random mixture, not the nonreversible deterministic products LG or GL. No drift constants, weight moments, finite state space, or positive global spectral gap are assumed. Neither population KL bound is inferred from finite training data.

Define T_(K,J,alpha)(epsilon) as the supremum, over this class, of the first integer t at which TV(q C^t,pi)<=epsilon. The core result proves that this supremum is finite and that

    limsup_(epsilon->0) epsilon log T_(K,J,alpha)(epsilon)
       <= max(K,J).                                           (1.1)

Together with the lower bound in Section 5, this proves the exact leading coefficient K whenever 0<J<=K. For J>K the upper coefficient is not asserted to be optimal. K=0 or J=0 forces pi=q and is a separate trivial case.

## 2. A direct finite-time inequality

Choose B,R>e. Put

    S={1/B<=W<=R},
    a=pi(W>R), b=q(W<1/B),
    d=max(a+b/B, b+a/R).

Choose the fixed anchor M=exp(2K+1), A0={W<=M}, and s0=pi(A0)>=1/2.

For every integer t>=0,

    TV(q C^t,pi)
      <= d + sqrt[(M(B+1)+R)/(alpha s0 (2t+1))].               (2.1)

One may replace d by the sharper actual maximum max(q(S^c),pi(S^c)). One also has

    a<=K/(log R-1), b<=J/(log B-1).                            (2.2)

Thus every quantity on the right can be bounded from the declared contracts alone. An upper bound above one is simply uninformative, not a claim of larger-than-one TV.

### Proof: smooth the observable, not the initial density

Fix an event A and let g=C^t 1_A. Since C is Markov, 0<=g<=1. Let m be the mean of g under pi conditioned on A0; thus 0<=m<=1. Because both q and pi have total mass one,

    E_q g-E_pi g = integral (q-pi)(dx)(g(x)-m).                (2.3)

For any measurable set E, writing q_E=q(E), pi_E=pi(E), the outside integral obeys

    -m q_E-(1-m)pi_E
       <= integral_E(q-pi)(g-m)
       <= (1-m)q_E+m pi_E.

Its absolute value is therefore at most max(q_E,pi_E). For E=S^c this is at most d. This maximum, rather than the sum, is important for the leading coefficient.

The independence-MH Dirichlet form is

    E_G(g,g) = (1/2) integral pi(dx)pi(dy)
                          (g(x)-g(y))^2 / max(W(x),W(y)).

Restrict its second integration variable to A0. There max(W(x),W(y))<=max(W(x),M). Conditional Jensen gives

    E_G(g,g) >= (s0/2) integral pi(dx) (g(x)-m)^2/max(W(x),M).

Weighted Cauchy-Schwarz on the core now gives

    |integral_S(q-pi)(g-m)|
       <= sqrt[(2 E_G(g,g)/s0) I],
    I=integral_S pi(dx) max(W,M)(1/W-1)^2.                    (2.4)

On S intersect {W<=M}, use

    pi(dx)(1/W-1)^2 = q(dx)(1/W-2+W),

and W>=1/B to bound this part of I by M(B+1). On S intersect {W>M}, one has W>1 and W(1/W-1)^2=W-2+1/W<=W<=R, so that part is at most R. Consequently

    I<=M(B+1)+R.                                             (2.5)

The Dirichlet comparison is E_C >= (alpha/2)E_G. Reversibility and laziness make C a self-adjoint positive contraction on L2(pi). The spectral theorem gives, with f=1_A-pi(A),

    E_C(C^t f,C^t f)
       = integral_[0,1] (1-lambda)lambda^(2t) d< E_lambda f,f >
       <= Var_pi(1_A)/(2t+1)
       <= 1/[4(2t+1)].                                       (2.6)

Here (1-lambda)lambda^(2t)<=1/(2t+1); its exact maximum is smaller when t>0. Combining (2.3)--(2.6), with E_G<=2E_C/alpha, yields the square-root term in (2.1). Taking the supremum over A proves the TV bound. The density dq/dpi need not lie in L2: it was restricted to S before using Cauchy-Schwarz, while the evolved indicator is bounded.

Finally q(W>R)<=a/R and pi(W<1/B)<=b/B, giving d. The two inequalities in (2.2) follow by applying the binary entropy tail lemma from `PROOF.md` Section 2 first to (pi,q), then to (q,pi). The same lemma at M=exp(2K+1) gives s0>=1/2.

## 3. An explicit executable budget

For 0<epsilon<=1/2, choose

    R=exp(1+3K/epsilon), B=exp(1+3J/epsilon),
    M=exp(2K+1), U=M(B+1)+R,
    t=ceil[4U/(alpha epsilon^2)].                             (3.1)

Then a,b<=epsilon/3, so d<=epsilon(1+1/e)/3<epsilon/2 and s0>=1/2. The square-root term in (2.1) is at most epsilon/2. Hence this t ensures TV(q C^t,pi)<=epsilon.

The budget uses one initial proposal draw and t applications of the lazy random mixture. In expectation it uses alpha*t/2 additional independent proposals and (1-alpha)*t/2 local transitions. It requires only ordinary unnormalized MH ratios. The theorem assumes exact kernel probabilities in real arithmetic; it does not certify a floating-point implementation's exact law. Constants K,J may be used to choose the conservative budget; their availability is a substantive contract, not a free observable.

This guarantee is conservative and exponential. It is not evidence of a useful speedup over pure IMH. The practical significance is identifying a sufficient missing information condition for arbitrary reversible local moves.

## 4. Leading asymptotic coefficient

Fix K,J,alpha>0, with alpha<1. A direct time-domain proof is particularly short. Let

    R=B=t/(log t)^4

for sufficiently large integer t. The first term of (2.1) is bounded by

    [max(K,J)+max(K,J)/R]/[log R-1]
       = [max(K,J)+o(1)]/log t.

The second term is O_(K,alpha)((log t)^-2), because M is fixed. Thus, uniformly over the declared class,

    limsup_(t->infinity) log t * sup TV(q C^t,pi)<=max(K,J).

TV is nonincreasing in t for each fixed kernel. Inverting this uniform upper bound proves (1.1). Equivalently, choose both tail budgets about (1-o(1))*epsilon, so log R~K/epsilon and log B~J/epsilon; the **sum** M(B+1)+R then has leading logarithm max(K,J)/epsilon. The earlier product BR proof gave a valid but weaker K+J coefficient. That loss is removed by the fixed-anchor inequality.

## 5. Meaning and unresolved sharpness

The one-sided counterexample in `PROOF.md` has reverse KL diverging as its parameter p tends to zero. It therefore does not contradict this theorem. Forward KL bounds target mass in high-W regions; reverse KL bounds proposal mass in low-W regions. After excluding both small tails, the Dirichlet form controls an evolved indicator on the shared core. This is why the two controls enter the same cost bound.

Choosing L=I gives a lazy independence sampler; the two-state family in `PROOF.md` then implies

    liminf_(epsilon->0) epsilon log T_(K,J,alpha)(epsilon) >= K.

Its reverse KL tends to zero, and multiplying the transition rate by the fixed factor alpha/2 does not affect the leading logarithmic coefficient. The full two-state proof is also given in `JOINT_KL_FUNNEL_NOTE.md`. An independently derived entrance-to-trap lower family with a fixed skewed path proposal supplies the reverse-KL-dependent lower coefficient (1-alpha)J. That file gives exact finite conditions and a binomial-subordination argument retaining the coefficient under laziness. Therefore

    max(K,(1-alpha)J)
       <= liminf_(epsilon->0) epsilon log T_(K,J,alpha)(epsilon)
       <= limsup_(epsilon->0) epsilon log T_(K,J,alpha)(epsilon)
       <= max(K,J).                                         (5.1)

In particular, for 0<J<=K the limit exists and equals K.

The precise next owner question is to determine the sharp leading coefficient in the remaining **J>K, same lazy-mixture** envelope. The current upper proof does not exploit the probability that a global correction occurs before an initial local transfer. The current lower construction loses the factor (1-alpha) for exactly that competition. Seek a sharper transient comparison or a matching multi-state construction. The present reversible entrance mechanism cannot produce a doubly exponential barrier because reverse KL and detailed balance force a compensating local escape rate. Do not extend the already-settled one-sided toy example merely to generate more numerical evidence.
