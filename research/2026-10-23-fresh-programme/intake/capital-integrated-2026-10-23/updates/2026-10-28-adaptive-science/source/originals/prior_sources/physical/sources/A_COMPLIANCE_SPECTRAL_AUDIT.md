# Static relative compliance and the Bose-conductance limit

This audit treats a finite connected scalar cell with one backbone coordinate,
one intercell spring `K`, total mass `M`, backbone mass `m`, and side mass
`m_s=M-m>0`. In mass-normalized coordinates,

`D(s)=D0+s vv^T`, `s=4K sin^2(q/2)`, `v=e_b/sqrt(m)`,

where `D0` is positive semidefinite with the unique translation nullvector
`z=sqrt(mass)/sqrt(M)`. Set `u=v-z/sqrt(M)` and `w=-(M/m_s)u`. Then
`z^T v=1/sqrt(M)` and `u^Tz=0`.

## Exact compliance identity

For every `s>0`, `D(s)` is positive definite: a null vector would have to be
both a multiple of `z` and orthogonal to `v`, which is impossible unless it
is zero. Let `y=D(s)^(-1)u`. Multiplying `D(s)y=u` by `z^T` gives

`s(z^T v)(v^T y)=z^T u=0`,

so `v^T y=0` and therefore `D0 y=u`. The general solution is
`y=D0^+u+gamma z`. Since `v^TD0^+u=u^TD0^+u` and `v^Tz=1/sqrt(M)`,
the constraint `v^Ty=0` fixes `gamma=-sqrt(M) u^TD0^+u`. Thus

`u^T D(s)^(-1)u=u^TD0^+u`,

and the asserted identity follows exactly:

`w^T D(s)^(-1)w=(M/m_s)^2 u^TD0^+u`, for every `s>0`.

It is independent of wave number, not a small-`s` approximation. For a single
backbone-to-side spring of stiffness `k`, it reduces to the familiar
relative-coordinate compliance `1/k`.

## Endpoint formula and inverse-cubic spectral moment

Write the ordered endpoint eigenvalues as `alpha_0=0,alpha_1,...` for `D0`
and `beta_0,beta_1,...` for `D0+S vv^T`, where `S=4K`. Dark eigenvalues
cancel from all formulas below. With

`q(t)=v^T(D0+tI)^(-1)v`,

the translation-mode decomposition gives

`q(t)=1/(M t)+u^T(D0+tI)^(-1)u`,
`c:=u^TD0^+u=lim_(t down 0)[q(t)-1/(M t)]`.

The determinant lemma says

`prod_j(t+beta_j)/prod_j(t+alpha_j)=1+S q(t)`.

Expanding at zero and using
`prod_j beta_j/prod_(j>0)alpha_j=S/M` yields

`c = (1/M)[sum_j 1/beta_j - sum_(j>0)1/alpha_j] - 1/S`.

Thus the static compliance `C=w^TD(s)^(-1)w` is determined exactly by the
inverse-squared-frequency endpoint moment:

`C=(M/m_s)^2 c`.

There is an equivalent passband formula. Let
`Omega^2=S/M`,
`chi(omega)=sum_j 1_[sqrt(alpha_j),sqrt(beta_j)](omega)`, and
`chi_rig=1_[0,Omega]`. Then endpoint integration gives

`integral_0^infinity [chi(omega)-chi_rig(omega)]/omega^3 d omega`
`= (1/2)[sum_(j>0)1/alpha_j - sum_j1/beta_j + 1/Omega^2]`
`= -M c/2 = -m_s^2 C/(2M)`.

The difference integral is finite because both indicators equal one on a
nonzero acoustic interval at the origin. The `omega^-3` weight emphasizes
the low-frequency deficit; this identity alone is not a conductance estimate.

## All-network implication when compliance tends to zero

Fix `m,M,K,theta` with `m_s>0`, and consider any sequence of finite connected
single-link cells, allowing their internal dimensions and spring networks to
vary. Let `C_n` be their relative compliance. If `C_n -> 0`, then
`c_n=C_n(m_s/M)^2 -> 0`.

Let `mu_n` be the spectral measure of `u_n` for the positive eigenspaces of
`D0_n`, so

`q_n(t)=1/(M t)+integral_(0,infinity) (lambda+t)^(-1) d mu_n(lambda)`,
`integral lambda^(-1)dmu_n=c_n`.

Positivity implies the uniform-in-`t>0` bound

`0 <= q_n(t)-1/(M t) <= c_n`.

Consequently the determinant ratios converge for every `t>0`:

`P_n(t)=prod_j(t+beta_(n,j))/prod_j(t+alpha_(n,j))`
`=1+S q_n(t) -> 1+Omega^2/t`.

But the same endpoint ratio is the Stieltjes transform of the nonnegative
passband measure `nu_n(d omega)=2 omega chi_n(omega)d omega`:

`log P_n(t)=integral (omega^2+t)^(-1) d nu_n(omega)`.

Each `nu_n` has fixed total mass
`integral dnu_n=sum_j(beta_(n,j)-alpha_(n,j))=S/m`. The limiting transform
`log(1+Omega^2/t)` is exactly that of
`nu_rig(d omega)=2 omega 1_[0,Omega](omega)d omega`. Bounded positive measures
have vaguely convergent subsequences; uniqueness of the Stieltjes transform
therefore forces every vague limit to be `nu_rig`. Some mass
`S/m-S/M` can escape to arbitrarily high frequencies, so this is vague, not
total-variation, convergence.

The Bose integral nevertheless converges. On any compact interval
`[epsilon,R]`, its integrand relative to `nu_n` is the bounded continuous
function `g_theta(omega)/(2 omega)`, so vague convergence gives convergence
to the rigid-chain integral. The omitted tails are uniform in the network:

`integral_0^epsilon g_theta chi_n d omega <= epsilon`,
`integral_R^infinity g_theta chi_n d omega <= integral_R^infinity g_theta d omega`,

because `0<=chi_n<=1`, `g_theta<=1`, and the Bose weight decays
exponentially. Taking `epsilon down to zero` and `R up to infinity` proves

`C_n -> 0  =>  J_theta(chi_n) -> J_theta(chi_rig)`.

Therefore no sequence of such networks at fixed `m,M,K,theta` can have
compliance tending to zero while retaining a fixed positive Bose-conductance
reduction relative to the rigid chain. In particular, if the fixed-resource
optimum has saving `Delta>0`, then the set of networks with saving at least
any fixed `delta>0` has compliance bounded away from zero (a qualitative
bound depending on the resources and `delta`; this argument gives no explicit
constant or rate).

This conclusion is for the scalar rank-one intercell model and ideal-contact
ballistic Bose functional. It does not assert a bound for diffusive
conductivity, added intercell bonds, multiple backbone coordinates, or
nonharmonic materials.

## Audit of the explicit one-sided slope and Gibbs-range bound

For the same `delta=chi_rig-chi`, the rank-one interlacing gives `0<=chi<=1`,
so `delta>=0` below `Omega` and `delta<=0` above it. Also
`integral delta/omega=0`. Put `h_theta(omega)=omega g_theta(omega)` and
`H_theta(t)=h_theta(t^(-1/2))`. With `x=1/(2 theta sqrt(t))`, direct
differentiation gives

`H_theta'(t)=4 theta^3 x^5(2x coth(x)-3)/sinh^2(x)`.

The expression in the supremum defining `C_B` tends to zero as `x->0` and
`x->infinity`, is continuous for `x>0`, and is positive at some finite `x`;
thus `0<C_B<infinity` and `H_theta'(t)<=4 C_B theta^3`. Integrating this
one-sided derivative inequality from `Omega^(-2)` to `omega^(-2)` yields

`h_theta(omega)-h_theta(Omega) <= 4 C_B theta^3 (omega^(-2)-Omega^(-2))`

for `omega<Omega`, with the reverse inequality for `omega>Omega`. Multiplying
by `delta(omega)/omega` gives `<=` on both sides because `delta` changes sign
at `Omega`. The anchor term cancels by the log moment, leaving

`J_rig-J <= 4 C_B theta^3 integral delta/omega^3`
`=2 C_B theta^3 (m_s^2/M) C`.

The constant and sign agree with the owner derivation. This is uniform over
finite network order and retuning: it uses only the scalar rank-one
passband-indicator property, the exact log/compliance moments, and the Bose
weight. It does not extend as written to multichannel spectra whose spectral
weight can exceed one.

For the finite periodic ring, removing its one global translation mode leaves
positive normal-mode frequencies `omega_k`. The quantum Gibbs position
variance in a normal coordinate is
`(hbar/(2 omega_k)) coth(hbar omega_k/(2 k_B T)) >= k_B T/omega_k^2`.
Applying this scalar inequality modewise gives
`Cov(eta)>=k_B T D_ring^+`. The Fourier transform of a force/readout vector
localized to one cell has a factor `1/sqrt(N)` at each wave number; since
`w^T D(s)^(-1) w=C` for every nonzero `s` and the same pseudoinverse identity
holds at `s=0` on `z^perp`, the local static compliance is
`(1/N) sum_q C=C`, independent of ring length and intercell spring.
Therefore `Var(Y)>=k_B T C` (about its equilibrium mean). If each internal
relative coordinate `y_j=x_j-x_b` has centered rms at most `d`, the L2
triangle inequality and positive weights `m_j/m_s` summing to one imply
`sqrt(Var(Y))<=d`, hence `C<=d^2/(k_B T)`.

Combining gives the explicit uniform low-temperature bound

`(J_rig-J)/(pi^2 theta/3)`
`<= (6 C_B/pi^2)(m_s^2/M) d^2 k_B T/hbar^2`.

With variable backbone mass constrained by `m>=m0`, replace `m_s^2` by
`(M-m0)^2` for a topology-uniform bound. Since the rigid-chain integral
divided by `pi^2 theta/3` tends to one as `theta->0`, no fixed fractional
conductance reduction survives a temperature-retuned sequence with a common
finite equilibrium displacement cap in this model. The implication is
one-sided: it does not claim the best achievable improvement under a fixed
range cap, nor does it assert a specific device-level material bound.
