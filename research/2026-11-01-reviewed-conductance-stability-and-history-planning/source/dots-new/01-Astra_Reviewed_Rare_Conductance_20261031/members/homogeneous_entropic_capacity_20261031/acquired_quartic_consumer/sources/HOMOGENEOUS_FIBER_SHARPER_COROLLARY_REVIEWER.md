# Separate sharper integrated-loss corollary

This derivation is separate from the unchanged root source `HOMOGENEOUS_FIBER_CAPACITY_CANDIDATE.md`, SHA-256 `84099bfdd17e90b5ac5b4560af97a8cbb5e7aa10aae8d575b508c9ea6c2db525`. The parent relayed the author's improved inequality; I independently checked it. It uses precisely the same hypotheses and output task, not a new parser or process model.

On 0<=y<=b=1/2 let v=1+kappa(1-y^2)^2, W=v^(m/p), s=1+2/p, and v_min=1+9 kappa/16. The reviewed original argument already gives

    K W <= C_m f(y)(-W'),
    f(y)=4 kappa y(1-y^2)/v(y)^s,
    C_m=m^(2/p-1)/[p^(1+2/p)(beta a)^(2/p)].

Since -W'>=0, 1-y^2<=1 and v>=v_min,

    f(y)<=4 kappa y/v_min^s.

There is no need to bound f' or assert monotonicity of f. Therefore

    integral_0^b K W
      <=(4 kappa C_m/v_min^s) integral_0^b y(-W')
      =(4 kappa C_m/v_min^s)
                         [integral_0^b W-b W(b)]
      <=(4 kappa C_m/v_min^s) integral_0^b W.

Evenness gives

    R1 <= [1+4 kappa C_m/v_min^(1+2/p)] R0.

The full-diffusion equilibrium conductance consequently obeys

    k_free/[1+4 kappa C_m/v_min^(1+2/p)]
        <=cap_mu(A,B)/mu(A)<=k_free.

This is at least as strong as the original f'-based estimate: its positive loss coefficient omits the nonnegative second summand in C_m D. Both estimates remain valid.

For p=4 and the nonnegative coupled quartic grammar, a=d_min/m and C_m=1/[8 sqrt(beta d_min)]. Thus the improved loss factor is

    1+kappa/[2 sqrt(beta d_min)(1+9 kappa/16)^(3/2)].

In the specified beta=d_min=kappa=1 case, v_min=25/16 and v_min^(3/2)=125/64. The additive loss is 32/125 and the total factor is exactly **157/125**. The original weaker **123/64** bound is not erroneous and has not been edited.

All metric, full-fiber boundary, normalizability (4m>p), actual coefficient/coercivity acquisition and capacity-not-MFPT qualifications are inherited unchanged. Dimension independence here is the explicit cancellation a=d_min/m within this grammar, not a general guarantee for arbitrary ill-conditioned coercivity inputs. No unknown partition-function evaluation or conditional-mixing oracle is introduced.
