# Flagged weak coupling is an exact physical time change

This completed calculation tests one proposed source repair. It does not
resolve COMMON_QUESTION.md or exclude different source constructions.
Its input is the explicit flagged source operation in h1/WEAK_COUPLING.md,
read in full, rather than an assumed preservation of the hard witness.

## The actual source and both complementary outputs

A finite virtual memory M starts in tau. Each active emission applies
V_h:M->P tensor M. After k active emissions, average the original control
letters, discard the final memory, and call the ordinary physical input
rho_h^(k). Its true coherent information through N^k is a_k; put a_0=0.

At each physical tick independently choose active probability s. An active
tick uses V_h; a filler tick emits a fixed PURE state on the physical and
emitted-purifier registers, leaving M unchanged. Both types count as
channel calls. The physical channel copies the active/filler flag into
orthogonal flags at BOTH receiver and true environment. Conditional on
the filler flag it applies a genuine fixed dilation to the pure emission.
Its two filler output entropies are equal, say c_f.

These are ordinary finite channels. The active-sector dilation is the
genuine N isometry; the filler can be a one-dimensional orthogonal input
sector or the self-complementary sector constructed by h1. Orthogonal
branch flags at both outputs remove flag off-diagonals in both actual
output marginals, including when the source choice is implemented
coherently. Rational Choi data remain rational, with the enlarged input
normalization explicitly adjusted. No reference is delivered for free.

## Exact finite-block identity

Given a flag word with K active ticks, the active physical input is
EXACTLY rho_h^(K), because filler ticks left virtual memory unchanged.
Filler outputs are product states independent of the active outputs.
Therefore

    S(B^n|word)=S(B_h^K)+(n-K)c_f,
    S(E^n|word)=S(E_h^K)+(n-K)c_f.

The direct-sum flags contribute the SAME Shannon entropy at both outputs.
Subtracting the complete receiver and environment entropies proves

    I_c(rho_s^(n),N_flag^n)
      =sum_(k=0)^n binom(n,k)s^k(1-s)^(n-k) a_k.    (1)

Every inactive call, every flag and every genuine complementary output is
received. This is not a comparison conditioned on favourable success.

If a_k/k converges to r, physical dimension bounds |a_k|<=Ck. With
K~Binomial(n,s), choose k0 so |a_k-rk|<=epsilon*k for k>=k0. Then

    |E a_K/n-s*r|<=s*epsilon+C'k0/n.

Taking limits gives the FULL source rate

    r_s=s*r.                                      (2)

No effective k0 or memory mixing gap is needed. Equation(2) does not
make an uncomputable r effective. In particular, the declared diluted
source has the same rate SIGN as the original, with an actual factor s
in rate per physical channel use.

For a stationary original output process, write
e_Y(k)=S(Y_h^k)-k h_Y, Y=B,E. The diluted entropy rate is
h2(s)+(1-s)c_f+s h_Y, and exactly

    e_(Y,s)(n)=E e_Y(K).                            (3)

Thus the environment excess scale is transported, not made effective.
An original finite-block decomposition a_k=k*d+R_k+kappa_k becomes

    a_(s,n)=n*s*d+E R_K+E kappa_K.                 (4)

When the limits exist, both the proposed local signal and its signed
extensive history remainder scale by s. Dilution alone cannot improve
their ratio or make the latter second order in s.

## The actual square-root encoder satisfies the assumptions

For a product baseline omega_AR=tau_A tensor I_M/D, the N1680 canonical
square-root Kraus blocks are K_af=(sqrt(tau_A))_af I_M. Its retained-memory
map is exactly identity, while the physical/purifier emission is the fixed
pure vector |sqrt(tau_A)>.

For h1's orthogonally flagged source

    omega_s=(1-s)|1><1| tensor tau_A tensor I_M/D
                          +s|0><0| tensor omega_h,

the memory channel is exactly

    M_s=(1-s)id+s M_h.                              (5)

Its actual physical wrapper records the flag at both receiver and
environment. Hence(1)--(4) apply to this source. The Fisher/entropy
margin's exact attenuation s, proved by h1, agrees with its physical
clock. Small average product-distance has not purchased a better signed
bulk rate. The rare hard branch retains its original relative coupling.

Adding a genuinely different memory operation between active emissions
would change the conditional-history kernel; this theorem would then
need new hypotheses. It gives no no-go theorem for every weak-coupling,
mixed-catalyst or mixer construction, and does not optimize N_flag over
other encoders. A new signed bulk inequality or a different receiver
representation remains necessary for the full ordinary-capacity gap.
