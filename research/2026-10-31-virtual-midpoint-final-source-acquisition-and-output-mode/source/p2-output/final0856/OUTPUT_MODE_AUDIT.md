# Independent audit: quantum gain and an initial-state-rejecting output mode

Date: 2026-10-31. No external research and no edits to the root files. This audits the proposed quantum-gain extension of the existing finite-mode cancellation construction.

Companion executable: [audit_output_mode.py](audit_output_mode.py).

## Verdict

The resonant filter, signed-kernel transport argument, finite-pole asymptotic argument, and fixed passive multimode extension are sound under the qualifications below. A single input-independent CP ideal instrument gives the claimed square-root-plus-probability bound on the complete logical/source channel.

The main corrections or boundaries are:

1. With scalar decay exp(-lambda t), the commutator with the future output creation mode uses lambda conjugate. Thus it is sqrt(kappa) k(t)* if k was defined using exp(-lambda t). This changes only the sign of the local Y term; the real transport kernel and all stated probability bounds survive.
2. A fixed known scalar pole per logical sector is covered. An operator-valued, dynamically changing pole driven by a noncommuting source is not covered by a finite scalar-exponential annihilator.
3. For a family of general multimode receivers, one physical homodyne phase must make all relevant DC responses point in the desired directions. Individual nonzero DC responses do not guarantee this.
4. Fresh Gaussian input must give the required pointer distribution conditional on the logical sector and actual prior history. An unconditional Gaussian quadrature marginal alone does not imply the one-sided Q bound.
5. Arbitrarily fast source evolution is allowed; arbitrary ill-defined unbounded Hamiltonian sums are not. A valid propagator/dilation and the weak commutator identity used below must be supplied.

No new independent reset of the retained cavity or source is needed in the ideal theorem. Fresh Gaussian input, the physical output measurement, fixed receiver poles, and exact or qualified filtering remain supplied resources.

## 1. Scalar resonant identities

Put a=kappa/2, z=exp(-aT), and

\[
w_0(t)=1-\frac{2e^{-at}}{1+z},\quad
V=T-\frac2a\tanh(aT/2),\quad
w=w_0/\sqrt V.
\]

For every T>0,

\[
\int_0^T w^2=1,\qquad
\int_0^T w(t)e^{-at}dt=0,\qquad
\int_0^T w(t)dt=\sqrt V.
\]

The annihilation cancels the initial receiver operator itself, not merely its expectation or its variance. Initial receiver/source/reference correlations therefore do not reintroduce that initial operator.

The response kernel is exactly

\[
k(t)=\frac{(1-e^{-at})(1-e^{-a(T-t)})}
{a(1+e^{-aT})\sqrt V}\ge0.
\]

It satisfies

\[
\int_0^T k(t)dt=\frac{\sqrt V}{a}.
\]

Thus the minimum pointer displacement is

\[
\mu_-=2\sqrt\kappa g_-\int k
=4g_-\sqrt{V/\kappa}.
\]

These are exact identities in the linear receiver model.

## 2. Complex poles: the conjugation convention

Use

\[
\dot a=-\lambda a-\sqrt\kappa\,b_{\rm in}
\]

for the free scalar receiver, and define the measured free output mode by

\[
B_s=\int_0^T w(t)b_{{\rm out},s}^{\rm free}(t)dt.
\]

For u>=t,

\[
[a_s^{\rm free}(t),b_{{\rm out},s}^{\rm free}(u)^\dagger]
=\sqrt\kappa\,e^{-\lambda_s^*(u-t)}.
\]

Consequently, with

\[
k_s(t)=\int_t^T w(u)e^{-\lambda_s(u-t)}du,
\]

\[
[a_s^{\rm free}(t),B_s^\dagger]=\sqrt\kappa\,k_s(t)^*.
\]

Writing X_s=B_s+B_s^dagger and Y_s=i(B_s^dagger-B_s),

\[
a_s^{\rm free}+a_s^{{\rm free}\dagger}
=\sqrt\kappa[
\operatorname{Re}k_s\,X_s+\operatorname{Im}k_s\,Y_s]
+A_{\perp,s}.
\]

The complement commutes with B_s and B_s^dagger. The imaginary kernel is therefore local in Y_s. Using the unconjugated coefficient in the annihilation-operator decomposition would incorrectly leave a noncommuting complement.

The same real physical w is used for every sector. Different B_s are mathematical free-picture coordinates for the same measured output statistic, not sector-conditioned hardware filters.

## 3. Transport proof without assuming a classical gain trajectory

Let W=s be fixed in a logical sector, s in {+1,-1}. Let G(t) be a self-adjoint source operator satisfying

\[
g_-I\le G(t)\le g_+I,\qquad 0<g_-\le g_+<\infty.
\]

The source need not be in a known state, commute with its Hamiltonian, or be redrawn during the window. After separating the selected pointer mode, the interaction has the form

\[
H_s(t)=s\,\beta(t)G(t)X+K_s(Y,t),
\]

where K_s is local in Y, possibly an unbounded Hermitian operator on the source and complementary modes. Constants such as sqrt(kappa) may be absorbed into beta.

For the convention [X,Y]=2i, the pointer velocity is -2s beta G. Set

\[
m(t)=2[g_-\beta(t)_+-g_+\beta(t)_-],\qquad
\mu=\int_0^T m(t)dt.
\]

For s=+1, use a bounded smooth increasing function f and a threshold b(t) with b'(t)=-m(t), b(T)=0. The weak Heisenberg identity gives

\[
\frac{d}{dt}\langle f(Y-b(t))\rangle
=\langle[m(t)I-2\beta(t)G(t)]f'(Y-b(t))\rangle
\le0.
\]

The inequality uses G commuting with Y as an operator factor, positivity of f', and the spectral gain bounds. It does not assume a classical sample path for G. Local Hermitian potentials disappear from this commutator, even if they rotate the source arbitrarily rapidly.

Approximating the half-line indicator yields

\[
\Pr(Y_{\rm out}\ge0\mid s=+1)
\le\Pr(Y_{\rm in}\ge\mu\mid s=+1).
\]

The opposite-sector argument gives the corresponding left-tail inequality. If the sector/history-conditioned initial Y distribution is centered Gaussian of variance v,

\[
p_{{\rm wrong},s}\le Q(\mu_s/\sqrt v)
\]

when mu_s>0. Signed beta is allowed. The gain's upper bound is essential during negative-kernel intervals.

This proof can equivalently be written as a continuity equation for a Hilbert-space-valued wavefunction. The bounded-observable proof avoids assuming that every arbitrary input has a differentiable position wavefunction.

## 4. Freshness and arbitrary retained correlations

Fresh Gaussian Markov input on a new time interval, independent of the retained receiver/source/past record, is a sufficient condition. The receiver and retained source may remain arbitrarily correlated with each other and with an inaccessible reference.

Once initial-receiver cancellation is exact, B_s is a bath-only normalized mode. If all input ports have the same centered gauge-invariant thermal covariance, every such passive mode has the same quadrature variance v. The modes B_s for different sectors need not be independent. Their individual conditional marginals suffice.

The same reasoning applies after actual prior histories: fresh future input increments can remain independent of the past while the retained apparatus state is highly history dependent. No reset or independent redraw of the retained source follows or is required.

A colored input, a reused temporal mode, or an input correlated with the logical sector does not acquire this property from its unconditional thermal/noise marginal alone.

For an explicit marginal-only counterexample, take a joint logical/pointer wavefunction whose Y density is exactly a centered Gaussian f(y), but whose logical amplitudes have conditional weights

\[
p_+(y)=\tfrac12[1+\tanh(Ky)],\qquad p_-(y)=1-p_+(y).
\]

This is a valid finite-smoothness state for finite K. Under exact opposite constant shifts, its total wrong probability is

\[
2\int_\mu^\infty f(y)p_+(y)dy>Q(\mu/\sqrt v),
\]

approaching 2Q as K grows. Thus an unconditional Gaussian Y marginal cannot replace the conditional freshness statement. For a pure vacuum marginal, factorization with other systems follows automatically.

## 5. Finite fixed scalar poles

Let each relevant pole lambda_s have positive real part. Choose a linearly independent real basis phi_j for the span of Re exp(-lambda_s t), Im exp(-lambda_s t), dropping zero and redundant functions. Let

\[
h_T=\operatorname{Proj}_{\mathrm{span}\{\phi_j\}}1,\quad
w_0=1-h_T,\quad V=\|w_0\|_2^2,\quad w=w_0/\sqrt V.
\]

Then V>0, the startup operator cancels for every admitted pole, and

\[
\int w=\sqrt V,\qquad
\int_0^T k_s(t)dt=\frac{\sqrt V}{\lambda_s}.
\]

In particular, with beta_s=Re k_s,

\[
\int\beta_s=\operatorname{Re}(1/\lambda_s)\sqrt V.
\]

### Uniform bound on the projection correction

Let G_T be the real Gram matrix and b_T the vector of integrals of phi_j. Because the basis is independent and exponentially decaying, for any fixed T0>0:

\[
G_T\ge G_{T_0}>0\quad(T\ge T_0),\qquad
\sup_T\|b_T\|<\infty.
\]

Hence the projection coefficients G_T^-1 b_T are uniformly bounded. Since each basis function is integrable, L=sup_{T>=T0}||h_T||_1 is finite. Also

\[
V=T-\|h_T\|_2^2=T-O(1).
\]

This is ordinary finite-dimensional Gram inversion on a fixed independent nuisance basis, not an inverse of an unknown quantum source map.

For a_s=Re lambda_s, the negative kernel area obeys the explicit bound

\[
\int_0^T(\beta_s)_-dt
\le\frac{1/(a_s|\lambda_s|)+L/a_s}{\sqrt V}.
\]

The bound follows by writing the kernel as the positive DC background Re(1/lambda_s)/sqrt(V), minus an exponentially decaying terminal transient and the convolution of h_T.

Therefore, with the sqrt(kappa) convention restored,

\[
\mu_s=
2\sqrt\kappa\left[
g_-\operatorname{Re}(1/\lambda_s)\sqrt V
-(g_+-g_-)\int(\beta_s)_-
\right],
\]

and

\[
\mu_s=
2\sqrt\kappa g_-\operatorname{Re}(1/\lambda_s)\sqrt T
+O(T^{-1/2}).
\]

Every fixed finite gain ratio is eventually admitted. The constants are not uniform over unbounded detunings, nearly unidentified poles, or changing operator-valued poles.

## 6. Fixed passive multimode receiver

Let a be an M-component annihilation vector and include all input/loss ports in C:

\[
da=Aa\,dt-i\,lWG\,dt-C^\dagger dB_{\rm in},\qquad
dB_{\rm out}=Ca\,dt+dB_{\rm in}.
\]

Require physical passive realizability

\[
A+A^\dagger=-C^\dagger C
\]

and stability ||exp(At)||<=M0 exp(-alpha t). Let C_o be the monitored row.

Use one real filter orthogonal to every real and imaginary column function of C_o exp(At), and normalize its constant-orthogonal projection as above. Then the selected output mode has no initial receiver contribution.

For

\[
B=e^{i\varphi}\int_0^T w(t)b_{{\rm out},o}^{\rm free}(t)dt,
\]

the commutator vector is

\[
c(t)=[a(t),B^\dagger]
=e^{-i\varphi}\int_t^T
w(u)e^{A^\dagger(u-t)}C_o^\dagger du.
\]

The force quadrature is

\[
l^\dagger a+a^\dagger l
=\beta(t)X-\operatorname{Im}(l^\dagger c(t))Y+A_\perp(t),
\quad \beta(t)=\operatorname{Re}(l^\dagger c(t)).
\]

The complement commutes with the pointer mode. An exact integration and the startup orthogonality give

\[
\int_0^T\beta(t)dt=\chi\sqrt V,\quad
\chi=\operatorname{Re}
\left[-e^{-i\varphi}l^\dagger(A^\dagger)^{-1}C_o^\dagger\right].
\]

If the fixed DC response is nonzero, one physical phase phi can make chi positive.

Let L bound the L1 norm of the nuisance projection. A useful explicit constant is

\[
B_{\rm const}=\|l\|M_0\|C_o\|
\left(\alpha^{-2}+L/\alpha\right).
\]

Indeed, the terminal difference between the finite step response and its DC limit has L1 norm at most ||l||M0||C_o||/alpha^2, and the projected nuisance contributes at most ||l||M0||C_o|| L/alpha. Thus

\[
\int\beta_-\le B_{\rm const}/\sqrt V,
\]

\[
\boxed{
\mu\ge
2g_-\chi\sqrt V
-2(g_+-g_-)B_{\rm const}/\sqrt V.
}
\]

With V=T-O(1), Gaussian error decreases exponentially in T in this ideal receiver/measurement model.

### Sector families and identifiability

For a family A_s,C_{o,s},l_s, one may annihilate the union of the finite nuisance spans, but the physical filter and homodyne phase remain common. It is necessary for this proof that the corresponding chi_s all be positive for the desired sign convention.

Nonzero responses individually are insufficient. If the W=-1 sector has the negative of the W=+1 DC response, then multiplication by W can give the same physical output signal in both sectors. No sign classifier can separate those identical signals.

Stable dynamics alone is also insufficient: passivity/physical realizability and the covariance of all input ports are what make the canceled free output a normalized canonical Gaussian bath mode.

## 7. Full instrument, not only correct labels

Strong fine-record opacity means each actual Kraus operator factors as identity on the logical representation within a W sector, tensored with a source/output map. It does not mean every normalized logical marginal remains unchanged after conditioning on a fine outcome when the initial source was correlated with the logical state.

Let the complete physical readout have two reported labels b=+,-, possibly with a retained finer record. Write its sector-restricted CP pieces as Phi_{b|s}. Define a fixed ideal comparison by first pinching the input into sector s, running all physical record maps in that sector, and reporting s rather than b:

\[
\Psi(\rho)=
\sum_s |s\rangle\langle s|\otimes
\sum_b\Phi_{b|s}(\Pi_s\rho\Pi_s).
\]

The finer record and source output may be retained in the second factor. This is a single CP trace-preserving ideal instrument; it uses neither an inverse nor input-dependent completion. Within each sector it is logical identity jointly with an allowed trace-preserving source channel.

For a given input including an arbitrary reference, let q_+,q_- be wrong-label weights and c_+,c_- correct-label weights. Write q=q_++q_-, so c_++c_-=1-q. Diagonal reclassification costs q in half trace norm. The cross blocks cost at most

\[
\sqrt{c_+q_-}+\sqrt{c_-q_+}
\le\sqrt{q(1-q)}.
\]

Hence

\[
d(\Phi(\rho),\Psi(\rho))
\le q+\sqrt{q(1-q)}
\le p+\sqrt p
\]

if the sector error bounds give q<=p (with the intended positive-shift Gaussian bounds p<=1/2). This applies to the joint retained source/reference instrument. Source disturbance and steering are included in the source channel, not falsely identified with identity return.

Adaptive composition can use physical prefixes:

\[
\Phi_m\cdots\Phi_1-\Psi_m\cdots\Psi_1
=\sum_j
\Psi_m\cdots\Psi_{j+1}
(\Phi_j-\Psi_j)\Phi_{j-1}\cdots\Phi_1.
\]

Thus every local error is evaluated on an actual prior apparatus/source/history state. The fresh-input and receiver-domain hypotheses must hold on those actual states. No independent reset of the retained source is implied.

## 8. Infinite-dimensional and physical qualifications

A clean mathematical formulation assumes a normal unitary/dilation propagator for which bounded smooth f(Y) obey the weak commutator identity used in Section 3. Local-in-Y Hermitian terms must strongly commute with the pointer spectral projections in the relevant direct-integral sense; a merely formal expression is insufficient.

There is a natural sufficient construction in the proposed linear bosonic model. Move a self-adjoint H_E into the interaction picture. Then G_E(t)=exp(iH_E t)G_E exp(-iH_E t) remains bounded, strongly continuous, and between the same positive bounds, without any bound on [H_E,G_E].

On a finite-particle bosonic core, a linear field interaction with uniformly bounded one-particle coefficient norm C has an n-th Dyson term bounded by

\[
\frac{(2g_+CT)^n}{n!}
\sqrt{\frac{(m+n)!}{m!}}\|\psi_m\|.
\]

The series converges for finite T, uniformly in any source-Hamiltonian frequency bound. This supplies a route to the unitary limit on a dense core and then all normal initial states. Smooth bounded functions of Y with bounded derivatives support the bounded-commutator/weak-Heisenberg argument.

Thermal Markov input can be represented with a doubled vacuum field; finite thermal variance changes the coefficient norms but not the argument. The construction still requires the actual linear coupling and finite coefficient norms. Arbitrary nonlinear receiver couplings, operator-valued changing poles, or ill-defined white-noise Hamiltonian products are not silently included.

Exact startup cancellation is not uniform under calibration mismatch for an unrestricted initial receiver. Any nonzero residual coefficient can be amplified by an arbitrarily displaced initial state. Finite filter/pole precision therefore requires an initial-energy/tail constraint or a separately certified residue budget.

Finally, the ideal theorem removes initial-state reset and source-bandwidth requirements within its model. It does not remove detector inefficiency, fresh-field preparation, homodyne duration, retained-data holding errors, or symmetry-breaking exposure. Increasing T is still a real full-cycle resource cost.

## Executable scope

The companion script checks scalar cancellation and the detuned conjugation, fixed passive multimode startup cancellation and integrated response, canonical bath-mode normalization, signed negative-area diagnostics, a two-sided CP ideal comparator on correlated/reference inputs, and the unconditional-Gaussian-marginal counterexample.

It does not certify a hardware model, rounding enclosure, domain assumption, or noise calibration.
