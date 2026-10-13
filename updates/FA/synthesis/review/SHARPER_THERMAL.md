# Exact entropy penalty for the explicit singlet-cooling witness

13 October 2026. Integration-derived internal deduction, not external proof
review, historical priority, a physical channel implementation, or a material
free-energy computation. This is a refinement of the root thermal certificate,
not a change to the submitted CRAY theorem's quantifiers.

Let `P_s` have rank one and `P_t=I-P_s` have rank three. The explicit source
Schrodinger channel at `q=1/2` is

    Lambda(rho)=K0 rho K0 + (3/4) P_s Tr(P_t rho),
    K0=P_s+(1/2)P_t.

The root argument proves that a residual
`h_weak-Phi(h_strong)>=c0 I`, with `c0=(5-sqrt(13))/8`, implies

    F_strong-F_weak <= -c0-tau s(Lambda),
    s(Lambda)=min_rho [S(Lambda rho)-S(rho)].

Its elementary norm bound is `s>=-log(13/4)`. Here the exact entropy minimum can
be reduced to a scalar optimization without acquiring any environment state.

## Convexity and symmetry reduction

Entropy gain is convex. For an ensemble `p_i,rho_i`, data processing of its
Holevo information gives

    S(Lambda bar_rho)-sum_i p_i S(Lambda rho_i)
       <=S(bar_rho)-sum_i p_i S(rho_i),

so `s_gain(bar_rho)<=sum_i p_i s_gain(rho_i)`. This is standard quantum channel
mathematics, not a newly invented inequality.

The displayed channel is covariant under every block unitary
`U=exp(i theta)P_s+U_t`, where `U_t` is arbitrary on the triplet space. Entropy
gain is invariant under those unitaries. Convexity therefore shows that twirling
can only lower entropy gain. A minimizing input can be chosen as

    rho_x=(1-x)P_s+(x/3)P_t,  0<=x<=1.

The output has the same form with `x` replaced by `x/4`, and hence

    f(x)=H2(x/4)-H2(x)-(3x/4)log3,
    s(Lambda)=min_[0,1] f(x),

where `H2` is binary entropy with natural logarithms. For completeness,

    f''(x)=(3/4)/[x(1-x)(1-x/4)]>0.

The derivative tends to negative infinity at zero and positive infinity at one,
so there is a unique interior minimizer. Setting `y=x/(1-x)`, its stationary
equation is exactly

    y^3(4+3y)=27,   y>0.

The polynomial is strictly increasing for positive y. Substituting its
stationary equation into f gives the exact minimum

    s(Lambda)=-log(1+3y/4).

In particular, rational arithmetic gives `y<59/40`, because
`(59/40)^3(4+3*59/40)>27`. Therefore the conservative closed certificate is

    F_strong-F_weak <= -(5-sqrt(13))/8 + tau log(337/160).

This improves the root's same-channel `tau log(13/4)` penalty. The strict
negative-sign temperature window is enlarged to

    tau < [(5-sqrt(13))/8]/log(337/160).

It remains a sufficient universal bound under the full-Hilbert-space,
unrestricted-common-environment contract. It supplies neither fixed-sector
validity of the original cooling channel nor a necessary thermal condition.
The fixed-charge repair must be used for the distinct fixed-sector task.

The exact scalar expression avoids a generic minimum-entropy-gain oracle. Its
scope is only this explicitly symmetric channel; generic channels need not
admit this reduction. Outward logarithm evaluations or rational analytic bounds
must be paid when producing numerical interval certificates. The included
Python checks use floating logs only as diagnostics and separately verify the
rational polynomial bounds.

Primary prior-art locator opened in this review:
[Holevo, entropy gain](https://arxiv.org/abs/1003.5765), abstract only. It
establishes the existing entropy-gain context and does not establish novelty
of the paired-energy comparison or this channel calculation. No exhaustive
priority search was performed.
