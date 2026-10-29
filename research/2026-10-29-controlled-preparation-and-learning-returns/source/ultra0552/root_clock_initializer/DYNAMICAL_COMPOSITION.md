# Uniform velocity accounting for the growing-penalty initializer

29 October 2026. Root construction; independent review PENDING, including
PROOF.md. This composes the new initialization operation with the already
reviewed EXACT algorithmic CKG storage model. It does not prove natural-bath
storage or finite-temperature robustness to unknown Hamiltonian errors.

## 1. Parameter choice and unchanged static premises

Fix the same source geometry and beta as PROOF.md. Take initialization
accuracy epsilon_n=n^-p for any fixed p>0. Choose dyadic lambda_n by that
proof, imposing all fixed clock-thermal and normal-form gates first. Thus

    Delta_n<=C_p log(en),
    lambda_n<=lambda_0<=lambda_T,

where C_p includes the enormous fixed baseline penalty. The thermal slab
number only increases when lambda decreases; beyond the admitted onset its
wrapping-tail bound M exp(-M/2) decreases. The full-clock Peierls and common-
good-projector bounds of b_conventional/clock_thermal remain uniform:

    s_k=2^k,
    R_k=floor(a s_k^(1/3))-1>=a s_k^(1/3)/2,
    p_k<=4 exp[-(c0/2)s_k].

a,c0 are the fixed constants in its DYNAMICAL_COROLLARY.md. The exact logical
algebra still commutes with Hsim,n at EVERY clock energy. Gibbs logical twirl
and Hamiltonian logical drift remain zero. Seed count and whole-jump strength
remain <=(3+63r)n, <=1 per seed, with coherent correction norm <3 per seed.
No rate is divided by n or by Delta_n.

## 2. The velocity that actually changes

Write Hsim,n=Delta_n Hbar(lambda_n). The interaction of Hbar has a uniform
fixed-range norm bound, since 0<lambda_n<=lambda_0 and clock dimension and
incidence are fixed. Fix ONE standard finite-range Lieb--Robinson bound for
this entire bounded family with constants C0,mu,v0. Time rescaling gives
for the actual Hsim,n the SAME C0,mu and

    v_n=v0 Delta_n <=C'_p log(en).                     (1)

This is a conservative bound: on-site penalties do not themselves spread
support, but no improved transport estimate is required.

The admitted CKG tails are

    d_R=C0 e^(-mu R/2)+2 e^[-R^2/(4v_n^2 beta^2)],
    rB_R=6C0 e^(-mu R/2)+2C1 e^[-pi R/(4v_n beta)]
                                  +6 e^[-R^2/(4v_n^2 beta^2)].

For x>=0, e^(-x^2/4)<=e e^(-x), by completing the square. Consequently there
are constants C,c>0 INDEPENDENT of n and v_n such that for R>=1,

    2rB_R+4d_R+2d_R^2
         <=C exp[-c R/(1+beta v_n)].                 (2)

For example take c<=min(mu/2,pi/4,1) and absorb fixed C0,C1 and products into
C. Replacing v_n beta by 1+v_n beta only weakens the exponential. This step
keeps the Gaussian, coherent-B, and jump cross-term tails instead of
treating their old constants as uniform without proof.

## 3. Lifetime in the declared parallel clock

The whole-support receiver gives for all three corrected logical Paulis

    delta_k=max_alpha ||L_n^* Oalpha||_rho
       <=C n {exp[-c0 s_k/4]
                      +exp[-c a s_k^(1/3)/(2(1+beta v_n))]}
       <=C' n exp[-b u_k],
    u_k=2^(k/3)/log(en_k),                            (3)

with fixed b>0. The source size bound n_k<=5g^(2k) implies log n_k=O(k),
while u_k grows exponentially in k up to that divisor. Thus n_k is eventually
absorbed into any fixed fraction of exp(b u_k).

For the IDEAL exact thermal encoder, the reviewed stationary-state theorem
gives 1-Fe<=3 time delta_k/4. Therefore for

    0<=time<=exp(b u_k/4),

eventually 1-Fe<=exp(-b u_k/2), and the reviewed Kraus-variance conversion
gives an all-input diamond error <=2sqrt(2)exp(-b u_k/4). The exact constants
can be weakened by another fixed factor without changing the conclusion.

The positive initializer of PROOF.md is within diamond error <=epsilon_n of
this ideal logical encoder: it changes only its logical-independent thermal
environment, uniformly over a reference. Evolution and decoding are CPTP,
so the initializer error is not multiplied by the storage time. Hence the
actual prepared-channel error is bounded by

    n_k^-p+2sqrt(2)exp(-b u_k/4).                      (4)

The source size relation yields 2^(k/3)>=(n_k/5)^alpha with
alpha=ln2/(6ln g). Thus the storage interval is at least

    exp[c n_k^alpha/log(en_k)].

For every fixed 0<alpha'<alpha this eventually includes exp(c' n_k^alpha').
This is a genuine positive stretched-exponential exponent with a polynomial
ideal initializer, after allowing logarithmically growing couplings.

## 4. Exact scope and resource boundary

This is an algorithmically initialized, model-wise two-body-QUDIT memory
family with known Hamiltonian, known exactly stationary quasilocal CKG
generator, constant per-site generator rate, and ideal local quantum gates.
The controller is Hamiltonian dependent. The physical clock penalty and
hopping strengths grow with n; their baseline may be catastrophically large.
It is not a fixed-coupling memory theorem, a fixed-radius dissipator, a
natural Davies bath, a native device, noisy encoding, or protection against
unknown energy-changing coherent errors. No implementation/advantage claim
or historical novelty is inferred from the mathematical composition.
