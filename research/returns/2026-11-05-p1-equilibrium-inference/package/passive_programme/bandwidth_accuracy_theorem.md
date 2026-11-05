# Joint horizon, bandwidth and accuracy law for a passive susceptibility

**Status:** in-session mathematical construction, independently checked with the physical-operation route. The approximation primitives are classical. Historical novelty of the joint law is not established. No physical experiment is claimed.

## 1. Model and proved statement

Let ν be an unknown probability measure on [1,κ], with the lower rate used as inverse-time unit. Define

    kν(t) = ∫ exp(−xt) dν(x),
    Hν(t) = ∫ (1−exp(−xt))/x dν(x),
    S(ν)  = ∫ 1/x dν(x).

H is the unit constant-input response and S=H(∞) its static gain. In dimensional variables x=λ/μ, t=μ t_physical, κ=Λ/μ and S=μχ, where χ is physical susceptibility. Total spectral mass, positive lower rate μ and upper bound Λ are declared prior information, not acquired by this theorem.

Assume 0<ε≤1/16, 0<τ≤1/64, 16≤κ≤∞. Set

    L = log(1/ε),
    F(τ,κ,ε) = √κ L log(1 + L/(τ√κ)).                 (1)

For κ=∞ take the continuous limit F=L²/τ.

**Theorem (logarithmic minimax precision).** Universal constants c,C>0 exist such that:

1. A finite linear estimator using O(min{√κ L,L²/τ}) bin means of H inside [0,τ] has uniform absolute error ≤ε if each bin mean has arbitrary additive error ≤exp(−CF). A single bounded constant drive supplies their noiseless means.
2. Even if the entire early step response on [0,τ] is available, observation error of radius exp(−cF) prevents any estimator from uniformly guaranteeing error ε. The obstruction consists of two finite positive spectral measures with susceptibility gap >4ε and exponentially close early responses. It applies to nonlinear estimators and adaptive sampling, because the whole observed function can be identical under both models.

This is absolute error in normalized susceptibility. It is not uniform relative error when S approaches zero. It does not exclude equilibrium fluctuation access, hidden-coordinate access, free state preparation, fixed known model order or longer experiments.

The regimes are

    F ≍ √κ L log[L/(τ√κ)]       when τ√κ ≪ L,
    F ≍ L²/τ                   when τ√κ ≳ L.         (2)

At fixed κ and ε, effort is polynomial in 1/τ. Exponential-in-1/τ behavior requires a class allowing growing bandwidth and hidden order. It is not a universal law for a fixed finite-bandwidth device.

## 2. Constructive upper bound from a constant input

Let L1=log(4/ε). Choose

    m = ceil min{√κ L1/2, L1²/(2τ)},
    n = m+1,  h = τ/n.                                (3)

At κ=∞ use the second branch. Put

    a=exp(−κh), b=exp(−h), d=b−a,
    v=(2−a−b)/d>1,                                    (4)

with a=0 for κ=∞. Define the Chebyshev residual

    Rm(z) = Tm((2z−a−b)/d)/Tm(v) = Σ_{j=0}^m wj z^j. (5)

Then Rm(1)=1, so Σwj=1, and all roots lie in (a,b). Its monomial coefficients alternate in sign.

Observe bin means Bj=h^−1 ∫_{jh}^{(j+1)h} H(t)dt, j=0,...,m. For z=exp(−hx), φ(hx)=(1−exp(−hx))/(hx), integration gives

    Bj = ∫ x^−1 [1−φ(hx)z^j] dν(x).

Hence

    Ŝ = Σ wj Bj,                                      (6)
    Ŝ−S = −∫ x^−1 φ(hx) Rm(exp(−hx)) dν(x),
    |bias| ≤ 1/Tm(v).                                 (7)

This uses one constant step, finite bin integrations and no ideal impulse or infinite-bandwidth readout.

### 2.1 Bias

Let β=arcosh v, l=1−b and u=1−a. Then

    β = 2 artanh √(l/u).

Since (1−exp(−κh))/(1−exp(−h))≤κ,

    β≥2/√κ.                                          (8)

For fixed b, v increases with a, so β is bounded below by its a=0 value:

    β≥arcosh(2exp(h)−1)
      =2 arcosh(exp(h/2))≥2√h.                        (9)

The last inequality follows from cosh(r)≤exp(r²/2). If the first branch of (3) determines m, (8) gives mβ≥L1. If the second determines it, m≥1 and

    mβ≥2m√[τ/(m+1)]≥√(2mτ)≥L1.

Consequently

    |bias|≤2exp(−mβ)≤ε/2.                            (10)

### 2.2 Exact finite noise amplification

Positive roots imply alternating monomial coefficients, yielding the exact identity

    W := Σ|wj| = |Rm(−1)|
       = Tm((2+a+b)/d)/Tm((2−a−b)/d).                (11)

Bin errors bounded by δ therefore create estimator error ≤Wδ. Taking δ≤ε/(2W) completes the finite precision certificate. Use log-cosh to evaluate (11) without overflow.

For the order bound, h<1 and κ≥2 imply

    d=exp(−h)[1−exp(−(κ−1)h)]
      ≥(1/(4e)) min{κh,1}.                           (12)

Using Tm(x)≤(2x)^m for x≥1 and dropping the denominator in (11),

    log W ≤ m log(8/d)
          ≤ C0 m [1+log_+(1/(κh))].                 (13)

Let r=τ√κ/L1. For r≤1, m≍√κ L1 and κh≍r, giving log W=O(√κ L1[1+log(1/r)]). For r≥1, m≍L1²/τ and κh≍r², giving log W=O(L1²/τ). Since L≤L1≤(3/2)L, both are O(F). The extra log(2/ε) in ε/(2W) is also absorbed by F. This proves the upper half.

## 3. Positive finite hard family

The classical inverse minimax formula is

    Em(K) := inf_{p∈Pm} ||x^−1−p||∞,[1,K]
           = (K−1)/(2K) [(√K−1)/(√K+1)]^m.          (14)

For m=0 this is the midpoint error. For m≥1 it follows from the Chebyshev inverse formula in Kraus–Vassilevski–Zikatanov, Theorem 2.1 and affine rescaling. It is prior machinery, not a new approximation primitive.

### 3.1 Exact measures via alternation

Let x0<...<x_{m+1} be the alternating extrema of the minimax error in (14). Define

    ci = 1/∏_{j≠i}(xi−xj),
    σ = [Σ ci δ_xi]/[Σ|ci|].                         (15)

The leading-coefficient identity in Lagrange interpolation gives

    ∫p dσ=0 for every degree-≤m polynomial p.         (16)

The signs of ci and of the minimax errors both alternate. Choose the overall sign of σ to obtain

    ||σ||TV=1, σ([1,K])=0, ∫x^−1 dσ=Em(K).          (17)

Its positive and negative parts each have mass 1/2. Therefore

    ν+=2σ+, ν−=2σ−                                  (18)

are probability measures on at most m+2 total rates. They match moments 0,...,m and satisfy

    S(ν+)−S(ν−)=2Em(K).                              (19)

These are genuine positive passive responses. A diagonal positive dynamical matrix and collocated couplings equal to square roots of the positive masses realize either measure. Construction and calibration of this realization still cost resources.

The alternation nodes can be computed by scalar root finding. Let q=(√K−1)/(√K+1). For ℓ=0,...,m+1 solve on [0,π]

    (m−1)θ + 2 arg(exp(iθ)+q) = ℓπ,                  (20)

and set x=(K+1)/2+(K−1)cosθ/2, then reverse the node ordering. The phase derivative is

    m−1 + 2(1+q cosθ)/(1+q²+2q cosθ)>0.

For m=0 it simplifies to (1−q²)/(1+q²+2q cosθ)>0. Alternatively, isolate extrema algebraically from the explicit minimax polynomial. Formula (15) supplies the weights.

### 3.2 Early data separation

Taylor expansion in the nonnegative variable x−1 gives, for 0≤t≤τ,

    |exp(−tx)−exp(−t)Σ_{j=0}^m[−t(x−1)]^j/j!|
      ≤[t(K−1)]^(m+1)/(m+1)!.

The polynomial integrates equally under ν±. Since ||ν+−ν−||TV=2,

    sup_[0,τ]|k+−k−|
      ≤2[τ(K−1)]^(m+1)/(m+1)!
      ≤2[eτ(K−1)/(m+1)]^(m+1).                     (21)

Integration also gives

    sup_[0,τ]|H+−H−|≤τ sup_[0,τ]|k+−k−|.            (22)

### 3.3 Joint-parameter choices

Let

    L0=log(1/(4ε)),
    K=min{κ,[L0/(8eτ)]²},
    m=floor(√K L0/4).                                (23)

The assumed range ensures K≥16 and m+1≥2. For s=√K≥4,

    log((s−1)/(s+1))≥−3/s.

The susceptibility gap is consequently

    ΔS ≥(15/16)exp(−3m/√K)
        ≥(15/16)(4ε)^(3/4)>4ε.                      (24)

Meanwhile m+1>√K L0/4, so

    R:=eτ(K−1)/(m+1)
      ≤4eτ√K/L0≤1/2.                               (25)

As m+1≥2,

    −log(2R^(m+1))
      ≥(√K L0/8) log[L0/(4eτ√K)].                  (26)

When K=κ, r0=τ√κ/L0≤1/(8e), and (26) is Ω(√κ L0 log(1+1/r0)). When K is set by the second branch of (23), (26) is Ω(L0²/τ), which dominates √κ L0 log(1+L0/(τ√κ)). Finally L/2≤L0≤L, so this is Ω(F) in both regimes.

Thus (21) is at most 2exp(−cF), after adjusting constants. The midpoint response (H++H−)/2 is consistent with both models under observation noise at least half their difference. Since their targets differ by >4ε, no estimator can succeed on both. An adaptive query rule obtains the same transcript from that same midpoint function, so adaptivity does not evade the bound.

The hard family has hidden order at most

    m+2=O(min{√κ L,L²/τ}),

and maximal physical rate μK. In the wide-band regime this fastest rate is O(L²/(μT²)). Hidden order and bandwidth are therefore paid parts of the family; they are not held fixed while its deadline shrinks.

## 4. Attribution and scope of possible contribution

The lower proof uses classical uniform approximation, alternation duality, positive moment matching and a Taylor remainder. The upper proof uses a classical Chebyshev residual applied to bin means of a constant step. Chebyshev acceleration of a matrix inverse is established machinery. The potential contribution is the matched joint time–bandwidth–accuracy law and its acquisition realization under the stated scalar observation interface.

Brown–Grabovsky already prove a close instability mechanism for extrapolating completely monotone functions. Their Theorem 2.1 gives exponent (2/π)arcsin(1/x0) for point extrapolation from [0,1] in a relative L² formulation on a larger unnormalized cone, with precision tending to zero at a fixed extrapolation point. That is strong prior art: positivity does not generally make long extrapolation well conditioned.

Here the target is an inverse spectral moment, the class is normalized with an explicit finite bandwidth parameter, and the displayed estimates are uniform in joint short-horizon/high-accuracy regimes. Whether exactly this joint minimax law is already published remains a literature-priority question. It is not a proved firstness claim.

## 5. Information-interface distinctions

- Equilibrium fluctuation access is different: for dX=−AXdt+√(2Θ)dW, a stationary initial state has Var(bᵀX)=Θ bᵀA⁻¹b. Independent equilibrium copies directly reveal static susceptibility. Preparation/mixing/hardware/independence must be priced if allowed.
- The hard family has growing hidden order. A fixed-order rational model is a stronger prior and may have a different law.
- Hidden-coordinate or matrix-oracle access permits ordinary linear solvers, often much better than the restricted scalar interface here.
- Coupling normalization, μ and Λ are certified inputs. Their uncertainty is systematic and does not disappear under averaging.
- A number-of-repetitions theorem additionally needs a noise model. The physical-operation route treats continuous Gaussian readout separately.
- Short observation horizon is not short total duration when reset, calibration or many repeated runs are required.
- Reuse is conditional on the same plant and kernel. Averaging does not remove clock bias, gain drift, initial-state errors or changing dynamics.

## Sources

1. J. K. Kraus, P. S. Vassilevski and L. T. Zikatanov, *Polynomial of best uniform approximation to x^−1 and smoothing in two-level methods*, arXiv:1002.1859v3; *Computational Methods in Applied Mathematics* 12(4), 448–468 (2012), DOI 10.2478/cmam-2012-0026. Theorem 2.1 is the classical inverse minimax error. The paper credits much earlier Chebyshev approximation. https://arxiv.org/abs/1002.1859 ; https://arxiv.org/pdf/1002.1859.
2. H. J. Brown and Y. Grabovsky, *On Feasibility of Extrapolation of Completely Monotone Functions*, *SIAM Journal on Mathematical Analysis* 56(6), 7713–7747 (2024), DOI 10.1137/24M1652325. Author manuscript https://sites.temple.edu/yury/files/2024/08/CMF.pdf. The paper's displayed volume/year is 2024 despite some search indexing labels saying 2025.
