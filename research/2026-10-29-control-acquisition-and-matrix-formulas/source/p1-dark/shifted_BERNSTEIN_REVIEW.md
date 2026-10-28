# Scoped challenge of the positive Bernstein route

28 October 2026. Read `theory/SIMPLEX_LAW_ACQUISITION.md` and
`code/simplex_law.py` directly. This is an internal scoped derivation/check,
not an independent whole-proof audit. No prior files were edited.

## 1. The claimed dimension-free Bernstein bias is valid

The source has the variational form

    J(u)-c0 = min_y [ ||y||^2 + sum_i u_i (g_i+b_i^T y)^2 ],
    ||b_i||^2<=kappa, |g_i|<=G.

Fix an arbitrary physical u. Let y be its minimizer and set
r_i=g_i+b_i^T y. Let Uhat=(delta/k)N, where N is multinomial with k
draws, category probabilities p_i=u_i/delta and p_0=1-sum p_i. The zero
category adds no actuator. The positive Bernstein polynomial is exactly
E[J(Uhat)].

For a realization Uhat, put

    Hhat=I+sum_i Uhat_i b_i b_i^T >= I,
    z=sum_i (Uhat_i-u_i) r_i b_i.

The normal equations at the mean u show that the gradient at y of the
realized quadratic energy is 2z. Exact quadratic completion therefore gives

    J(Uhat)-c0 = ||y||^2+sum_i Uhat_i*r_i^2-z^T Hhat^-1 z.

Take expectations. The first two terms average to J(u)-c0, so

    0<=J(u)-E[J(Uhat)]=E[z^T Hhat^-1 z]<=E||z||^2.

The multinomial variance identity yields

    E||z||^2 = delta^2/k *
       [sum_i p_i r_i^2 ||b_i||^2-||sum_i p_i r_i b_i||^2]
      <=delta*kappa/k * sum_i u_i*r_i^2
      <=delta*kappa/k * (J(u)-c0)
      <=delta^2*kappa*G^2/k.                         (1)

The last step evaluates the energy at y=0. This argument does NOT assume
each |r_i|<=G; that tempting assumption is generally unavailable. The
weighted energy inequality is the reason the stated constant survives.

Thus, with positive Bernstein weights B_alpha(u),

    sum B_alpha R(node_alpha) <= R(u)
      <=sum B_alpha R(node_alpha)+delta^2*kappa*G^2/k.

For acquired midpoint/radius intervals, the code's positive interval

    [sum B_alpha midpoint - sum B_alpha radius,
     sum B_alpha midpoint + sum B_alpha radius + bias]

is sound, with noise amplification one. Its centered uniform radius is
epsilon+bias/2, centered at the Bernstein midpoint plus bias/2, as reported.
There is no need for q<1, a nonzero coupling, or a rank condition. Exactly
dark controls are covered. The node count remains binom(n+k,k).

## 2. Full-simplex task certificate has a precise objective

The current `SimplexLaw.task_certificate` correctly certifies

    maximize R(u)-price.u

or equivalently J(u)-price.u up to a common constant. Since the Bernstein
weights reproduce affine functions,

    R(u)-price.u <= max_alpha [R(node_alpha)-price.node_alpha]+bias.

The code uses upper node intervals for this bound. Its lower value at the
selected node and its degree-k interpolant's Bernstein coefficient bound
also have the correct direction. Taking their minimum is sound. The
face-by-face transform solves only coefficients on the current support after
all lower-support coefficients are known; the largest interior block has
binom(k-1,s-1) coefficients on an s-coordinate face.

This is NOT automatically the earlier objective Z(0)-Z(u)-price.u. With
nonzero prices, maximizing J-price and maximizing -1/J-price can choose
different actions. The declared objective must remain explicit. If the
earlier objective is wanted, the same node acquisition supports the direct
extension below; changing only the output label would be incorrect.

## 3. The same positive lattice can also certify the original Z objective

Assume warranted Q0-energy bounds zeta>=e^TQ0^-1e and
tau>=max_i v_i^TQ0^-1v_i. Whiten the original source:

    Z(u)=b^T(I+sum_i u_i a_i a_i^T)^-1 b,
    ||b||^2<=zeta, ||a_i||^2<=tau.

Let M=sum_i u_i a_i a_i^T, x=(I+M)^-1 b, and
D=sum_i(Uhat_i-u_i)a_i a_i^T. The second resolvent identity gives exactly

    Z(Uhat)=Z(u)-x^T D x+x^T D(I+M+D)^-1 D x.

The final term is nonnegative, its inverse is at most I, and E[D]=0. Hence

    0<=E[Z(Uhat)]-Z(u)<=E||D x||^2
      <=delta*tau/k * sum_i u_i(a_i^T x)^2
      =delta*tau/k * b^T(I+M)^-1 M(I+M)^-1 b
      <=zeta*delta^2*tau^2/k.                       (2)

The last inequality uses lambda/(1+lambda)^2<=lambda<=delta*tau.
A tighter optional spectral bound is max_(0<=lambda<=delta*tau)
lambda/(1+lambda)^2, at most 1/4. The displayed simple version suffices.

Thus B_k Z-bias_Z <= Z <= B_k Z, and for
G(u)=Z(0)-Z(u)-price.u,

    G(u) <= Z(0)+max_alpha[-Z(node_alpha)-price.node_alpha]+bias_Z.

After converting each actually acquired R interval monotonically to a Z
interval, a global regret certificate at a selected node x is

    max_alpha[-Z_alpha^- -price.node_alpha]+bias_Z
       -[-Z_x^+ -price.x].                          (3)

The common baseline cancels, so it need not be subtracted twice. This
conversion requires positive lower J and retains the actual propagated
node error; it does not treat raw R and Z noise as interchangeable.

The existing unnormalized specifications supply zeta=1/c_min and
tau=G^2/c_min+kappa. Equation (3) is therefore available without microscopic
matrix access if those same source-class bounds are warranted. This is a
proof of an optional extension, not a claim it is already implemented in
`simplex_law.py`.

### 3b. Usually sharper reuse through a scalar utility tangent

The original Z objective can also use the existing J-law global upper bound
directly, without the larger tau-based bias in (2). For any chosen positive
scalar anchor j0, concavity of f(J)=-1/J gives the exact global inequality

    -1/J <= -2/j0 + J/j0^2.

Let U_R(j0^2*price) be any valid all-simplex upper bound on
R(v)-j0^2*price.v from the current law's certificate. Then

    sup_v[-1/J(v)-price.v]
      <= -2/j0 + [U_R(j0^2*price)-r0]/j0^2.

If candidate x has acquired/compiled J(x)>=JL>0, its actual utility is at
least -1/JL-price.x. Therefore the original Z-objective regret is at most

    -2/j0 + [U_R(j0^2*price)-r0]/j0^2 + 1/JL+price.x. (4)

The common Z(0) cancels. The scalar anchor is an arithmetic choice; it must
not be substituted with an unknown exact J(x). A candidate's interval
midpoint is an admissible anchor, and the minimum of finitely many such
certificates is also valid. At the exact candidate anchor the utility
tangent is tight; with an acquired narrow interval it incurs only a small
extra slack. This extends the existing Bernstein/interpolant global bound
to the prior objective while preserving the same acquired source record.
Candidate generation and anchor search remain charged arithmetic, and
certificate validity does not rely on their optimization convergence.

## 4. Other scoped checks and remaining costs

The Lagrange unisolvence argument, coefficientwise rising-factorial bound
C_k=binom(2k-1,k), high-dimension sharpness limit, signed Taylor remainder
mass accounting, and Chebyshev residual polynomial were checked. No
mathematical defect was found in those displayed steps under their stated
premises. The q<16/9 threshold is a sufficient decay condition for that
particular interpolant bound, not for positive Bernstein approximation.

The finite node count, arithmetic, potentially large coefficient bit
lengths, all node preparations, control writes, calibration, reset/settling,
source stability and correlated-error intervals still matter. A positive
Bernstein rule has stable noise propagation but a 1/k bias bound; it does
not make the binomial acquisition cost disappear. Ordinary multivariate
interpolation, positive approximation and robust interval control can use
the same construction and information.
