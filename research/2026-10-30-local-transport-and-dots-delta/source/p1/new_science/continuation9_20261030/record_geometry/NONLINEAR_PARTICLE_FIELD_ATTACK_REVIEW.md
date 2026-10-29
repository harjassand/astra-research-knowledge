# Receiving review: the exact nonlinear particle-field claims

Existing record-geometry role. Actual inputs:

- `../NONLINEAR_PARTICLE_FIELD_ATTACK.md`, SHA-256 `6c3495f6f410cd5dc5fbd0e3a059dbc5ce4a7c095b824f440c3120be80239606`.
- `../NONLINEAR_PARTICLE_FIELD_CORRECTION.md`, SHA-256 `31a700ff6a22d1dcd01ae0781264d8c60e48041ae9984373c5312d989387a841`.

Exact snapshots are `NONLINEAR_PARTICLE_FIELD_ATTACK_REVIEWED_6c3495f6f410.md` and `NONLINEAR_PARTICLE_FIELD_CORRECTION_REVIEWED_31a700ff6a22.md`. No root file was edited and no new numerical fixture was needed.

**Accepted together:** marked-hop detailed balance, product invariance, finite-N nonexplosion, the exact protected-current counter, the full-horizon superexponential protected-current bound at the declared complete conditional Markov interface, and the protected-force shifted invariant law. The nonlinear density/action receiver is not proved or accepted.

## 1. Marked balance and invariance

On an active edge, delta is +1 or -1. The marked map

\[
F_i(\eta,q,p)=(\eta^i,q+g\delta e_i,p)
\]

is an involution with unit continuous Jacobian. After the swap delta changes sign, so the reverse shift restores q. The energy change is exactly `Delta E=g delta q_i+g^2/2`. The canonical eta factor is unchanged. With the stipulated reciprocal prefactor, independent of q,p,

\[
\mu(dx)c_i(\eta,h)\min\{1,e^{-\Delta E}\}
=\mu(dF_i x)c_i(\eta^i,h)\min\{1,e^{\Delta E}\}.
\]

This balances the complete particle/memory event. It would not follow from visible detailed balance alone or from an inferred intervention rate.

The continuous field matrix `[[0,-aA*],[aA,0]]` is skew-adjoint and divergence free in the stated energy coordinates. The p bath has drift `-gamma AA*p` and covariance `2gamma AA*`. Both preserve the Gaussian product, including the degenerate case. Summing the generators preserves mu for every fixed h. Mixing of conserved p coordinates and full identity-reversal self-adjointness are unnecessary and are not asserted.

## 2. Nonexplosion and current counting

The total native jump intensity is at most `c_+N` on one ring and `2c_+N` on two. Poisson proposals and thinning give finitely many jumps on any bounded interval. Between them, a finite-dimensional linear SDE is globally defined; every jump has finite magnitude. This proves nonexplosion without hidden mixing or an energy-growth estimate.

For `h_0 in ker A`, the continuous part of `h_0*q` vanishes. A native event increments it by g times that native current increment tested against h_0. Equation (5) is therefore pathwise exact and includes all native particle displacement. Field transport remains the separate apparatus channel declared in the source.

For one ring `S=sum q_i` is constant between particle events and changes by exactly +g or -g at a native hop. This, rather than Gaussianity of the path, closes the temporal interpolation below.

## 3. The density ceiling and whole-horizon estimate

Writing `rho_0=dnu_0/dmu<=exp(CN)`, invariance gives `P_t^*1=1`. Positivity of the adjoint semigroup implies `rho_t<=exp(CN)` at every deterministic t. Thus the Gaussian equilibrium marginal `S~N(0,N)` gives

\[
\Pr_{\nu_0}(|S(t)|>b)
\le2\exp\left(CN-\frac{b^2}{2N}\right).
\]

With `b=epsilon gN^2/4` and O(1+N^2T) integer times, this proves equation (6), including the initial endpoint. A deterministic allowed particle configuration and independent thermal q,p have density at most the canonical configuration count, bounded by `2^N`. Two rings give `4^N`. Arbitrary retained records need not preserve this ceiling conditionally.

The native event count K_j on any unit interval has upper tail dominated by a Poisson variable of mean `c_+N`. Independence between intervals is not needed. Chernoff's bound gives, for fixed epsilon and large N,

\[
\Pr(K_j>\epsilon N^2/4)
\le e^{-c_\epsilon N^2\log N}.
\]

If all sampled values satisfy `|S(j)|<=epsilon gN^2/4` and all interval counts satisfy `K_j<=epsilon N^2/4`, then

\[
|S(t)-S(0)|
\le |S(\lfloor t\rfloor)|+gK_{\lfloor t\rfloor}+|S(0)|
\le3\epsilon gN^2/4.
\]

There is no uncounted continuous field contribution. Union bounds and the exact counter prove (7), allowing for the final partial unit interval. The two exponents divided by N are

\[
C-c\epsilon^2\kappa_NN^2+o(1),
\qquad -c_\epsilon N\log N+o(1).
\]

They tend to minus infinity if `kappa_NN^2 -> infinity`. For the signed two-ring sum, equilibrium variance becomes 2N and the rate bound becomes `2c_+N`; only constants change. This is a genuine full-horizon bound for a non-Gaussian process.

Conditional application requires the actual future marked rates and Brownian/Poisson laws to remain the stipulated ones after conditioning on the old record and h. The density ceiling by itself cannot justify conditioning on exposed future randomness. At the complete conditional Markov interface the proof is pointwise in the record and h, and can be averaged while retaining that record. The correction explicitly adds this qualification.

The ceiling transfers the superexponential event estimate; it does not transfer finite-action lower probabilities or supply a density action. The source preserves that distinction.

## 4. The protected force is a shifted stationary law

For constant `f in ker A`, let

\[
E_f(q,p)=\tfrac12\|q-f/g\|^2+\tfrac12\|p\|^2.
\]

The marked event changes E_f by `Delta E-f_i delta_i`. Therefore the work-modified rates balance

\[
\mu_f=\mathrm{canonical}(\eta)\otimes N(f/g,I)_q\otimes N(0,I)_p.
\]

Since Af=0, the centered continuous field equations and their thermal law are unchanged after shifting q. Thus mu_f is invariant. Pairing each marked event with its reverse yields zero stationary mean native current at every edge. The protected work is also an exact endpoint, `f*J(t)=(f/g)*[q(t)-q(0)]`.

The correct energy statement is

\[
\mathbb E_{\mu_f}E-\mathbb E_\mu E
=\frac{\|f\|^2}{2\kappa}.
\]

The total mean energy also includes the thermal baseline. The correction's phrase **excess mean stored energy** is therefore necessary and correct.

An invariant law is not an exact preparation or convergence theorem. On one ring `S/g mod 1` is conserved. In particular,

\[
\mathbb E_\mu e^{2\pi iS/g}=e^{-2\pi^2N/g^2},
\qquad
\mathbb E_{\mu_f}e^{2\pi iS/g}
=e^{2\pi i(\sum_i f_i)/g^2}e^{-2\pi^2N/g^2}.
\]

For generic protected f these differ, so switching on the force from the unforced mixture does not imply convergence to that exact shifted mixture of residue sectors. The correction explicitly limits the stationary current claim to the actual shifted invariant initializer. This closes the scope issue; it does not infer a loading protocol.

## 5. The unproved receiver and target remain separate

The exact statements do not establish preservation of nonflat exclusion heat or rare density histories. The allowed prefactors lack a uniform positive lower bound and may depend on the full configuration, so these results do not even implicitly assert a common native hydrodynamic law for that whole class.

The source correctly identifies activity-weighted field replacement under actual tilted histories as unresolved and declines to infer it from the static product measure. I have not attempted that missing proof. The separate conditional variational note `MOBILITY_WEIGHTED_DENSITY_ACTION.md` diagnoses a further issue: even the ordinary reciprocal metric constraint need not preserve rare density histories when mobility varies in space. That note does not identify the limit of the particle-field process.

The close particle/link-field and winding predecessor remains the previously read Levrel--Maggs primary construction, [Boundary conditions in local electrostatics algorithms](https://arxiv.org/pdf/0805.1869), especially its periodic-boundary identities. Its Maxwell curl/Gauss-law geometry differs from the stipulated scalar-wave transducer. Neither that predecessor nor this receiving review supplies the new marked operation by analogy.

## Final receipt

The exact reviewed original and correction are accepted together for the specific invariant, stationary-force, and whole-horizon protected-current claims. The correction carries the correct original SHA and resolves the excess-energy, residue-sector, and complete conditional future-law qualifications. No nonlinear density/action, cross-sector preparation, apparatus, or historical-priority claim is accepted. No extra tests were required.

## Final correction receipt after the native-interface clarification

The root subsequently added item 4 to the correction without changing the original attack. I read the updated `../NONLINEAR_PARTICLE_FIELD_CORRECTION.md`, SHA-256
`ce0af85387965d85973dad267687a17c5b980870e40d755c71b524d7e78a8408`.
The exact new snapshot is `NONLINEAR_PARTICLE_FIELD_CORRECTION_REVIEWED_ce0af8538796.md`; the earlier correction snapshot is preserved too.

Item 4 explicitly states that arbitrary reciprocal prefactors with only a common upper bound do not warrant ordinary heat or a known baseline mobility even before adding the controller. A nonlinear receiver must first supply or establish that native interface; the geometry calculation uses an explicit homogeneous exclusion reference. This matches the qualification already identified in Section 5 of this review. **Final acceptance is pinned to the original attack plus this updated correction.** The added item changes no proof of invariance, nonexplosion, or the protected-current tail, and requires no new test.
