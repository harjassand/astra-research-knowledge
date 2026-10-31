# A pure stationary quantum completion of a finite Markov source

Root working construction, 31 October 2026. Unreviewed. This opens a different organizing question beyond independent telegraph modes: can unobserved quantum reservoir dynamics represent the same classical source while exposing only a slow number of useful events? It is not yet a general efficient compiler or a novelty claim.

## 1. Input and exact completion
Let Q be a finite irreducible row generator on d states, with q_xy>=0 for x!=y, q_xx=-sum_(y!=x)q_xy, and a known strictly positive stationary probability pi. Let the microscopic generator be lambda Q, lambda>0. Set

|psi>=sum_x sqrt(pi_x)|x>.

For each directed edge x->y define

L_yx=sqrt(lambda q_xy)|y>(<x|-sqrt(pi_x/pi_y)<y|).

Let C=sum L_yx^dagger L_yx=lambda C0. For x!=z put
a_xz=q_zx sqrt(pi_z/pi_x), b_xz=q_xz sqrt(pi_x/pi_z),
(H_env)_xz=(i lambda/2)(a_xz-b_xz), and (H_env)_xx=0.

H_env is Hermitian. Stationarity gives H_env|psi>=0, and every L_yx annihilates |psi>. Thus the reservoir Lindbladian with Hamiltonian H_env and jumps L_yx has the pure stationary state |psi><psi|. Detailed balance makes H_env=0, but reversibility is not required for the construction.

## 2. Restriction to the classical observable algebra
For F=diag(f), the dissipative diagonal entries are

(D^dagger F)_xx=lambda sum_(y!=x) q_xy(f_y-f_x).

Here C_xx=2lambda sum_y q_xy, since the incoming stationary flow equals the outgoing flow. For x!=z,

C_xz=-lambda(a_xz+b_xz),
(D^dagger F)_xz=lambda(b_xz-a_xz)(f_x-f_z)/2.

The Hamiltonian contribution i[H_env,F]_xz is the negative of this off-diagonal term. Therefore

L_env^dagger(diag f)=lambda diag(Qf).

The whole commuting algebra of diagonal observables is invariant and evolves exactly as the specified classical chain. The off-diagonal quantum dynamics are a completion, not extra observable source data.

Let the system coupling be K=sum_j A_j tensor diag(f_j), with arbitrary bounded Hermitian A_j, and total Hamiltonian H0 tensor I+I tensor H_env+sqrt(lambda)K. The algebra of operator-valued diagonal functions is invariant under the joint Heisenberg generator: multiplication by f_j keeps it diagonal, while the system factor acquires i[A_j,.]. Starting the reservoir in |psi> gives the same initial diagonal functional pi as the stationary classical source.

It follows by finite-generator uniqueness that the reduced system process equals the process driven by the classical Markov state z(t), with Hamiltonian H0+sqrt(lambda)sum_j f_j(z(t)) A_j. System-only instruments preserve this observable algebra, so the equivalence extends to arbitrary retained references and adaptive system operations at prescribed times. Reservoir state and jump records are unobserved. No commutativity of the A_j is needed.

## 3. A source-conditioned activity bound independent of lambda
Write P=|psi><psi|, Pperp=I-P, pi_min=min pi_x. Irreducibility implies ker C0=span{|psi>}: each edge constraint forces v_x/sqrt(pi_x)=v_y/sqrt(pi_y). Let c>0 be any certified bound C0>=c Pperp. Its acquisition and possibly small value are source costs, not free constants.

Let B0=||(I_sys tensor Pperp)K(I_sys tensor |psi>)||. This is the system-to-excited-reservoir coupling norm. If the f_j are centered under pi, then B0^2=||sum_x pi_x A(x)^2||, where A(x)=sum_j f_j(x)A_j. More generally use the centered A(x)-sum pi A(x); a nonzero mean is a deterministic Hamiltonian term whose physical simulation cost must still be paid.

For theta>0 set kappa=exp(theta)-1 and a_theta=exp(theta)pi_min-kappa. Restrict to a_theta>0 and choose delta=2kappa/a_theta. Use the positive reservoir weight

V=I+delta Pperp.

Since every L_yx annihilates |psi>, C commutes with P and vanishes on it. Define R=sum L_yx^dagger P L_yx. Each jump has output |y>, so

L_yx^dagger P L_yx=pi_y L_yx^dagger L_yx,
R>=pi_min C.

For the generator tilted by exp(theta) on every jump,

D_theta^dagger V=kappa(1+delta)C-exp(theta)delta R
              <=-kappa C<=-lambda kappa c Pperp.

H_env commutes with P and hence with V. H0 does also. The remaining Hamiltonian commutator has only ground/excited blocks, with off-diagonal norm at most delta sqrt(lambda)B0. Completing the square against the negative excited block gives

G_theta^dagger V <= [delta^2 B0^2/(kappa c)] V
                 = [4kappa B0^2/(c a_theta^2)] V.

Starting in the pure stationary reservoir, Tr(Vrho0)=1. Positivity of the tilted evolution, V>=I and Gronwall yield

E exp(theta N_T) <= exp[4 T kappa B0^2/(c a_theta^2)].

This bound is independent of the microscopic multiplier lambda. Differentiating at theta=0 gives

E N_T <=4 B0^2 T/(c pi_min^2).

For example theta=pi_min/4 has kappa<=(4/3)theta and a_theta>=2pi_min/3, so

P(N_T>=12 B0^2 T/(c pi_min^2)+u) <=exp(-pi_min*u/4).

System-only CPTP controls leave V unchanged in the Heisenberg picture, so the same unconditional bounds hold with their records retained. They do not imply a pathwise intensity bound, a thinning source, or a bound after normalizing an arbitrarily rare postselection.

## 4. What is and is not earned
The construction gives a pure stationary quantum completion of any finite irreducible Markov source, including nonreversible sources, and a rate-independent jump-count bound with explicit source-conditioning costs c^-1 and pi_min^-1. The source matrix, stationary probabilities, state preparation and usable gap bound must be acquired and charged. They can be expensive; this is not fast-forwarding an arbitrary unknown Markov chain.

The no-jump reservoir generator before system coupling has off-diagonal entries lambda q_zx sqrt(pi_z/pi_x) and diagonal entries -lambda sum_y q_xy. It is a similarity transform of lambda Q^T, so it is positive in the original basis. Once the centered system coupling is included, an efficient source for the resulting operator-valued no-jump maps has not been constructed here. Small event count does not supply that operation, and the independent-mode tensor factorization is generally lost.

Thus this is a structural representation/activity theorem candidate, not a completed general-source simulator. The earlier many-independent-telegraph compiler remains separate and unchanged. Classical-observable-preserving quantum semigroups, dark-state reservoir engineering, quantum Markov extensions and stochastic-generator symmetrization are necessary ordinary comparators before any novelty claim.
