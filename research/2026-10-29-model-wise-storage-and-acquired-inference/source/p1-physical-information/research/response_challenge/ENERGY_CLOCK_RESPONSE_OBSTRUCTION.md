# An energy perturbation can preserve the complete parity ambiguity

2026-10-29. Controlled-realization collaborator construction, independently also identified by the root. This note closes the proposed generic response-first route at its actual scope. It does not say that mechanical response measurements are uninformative when their kinetic action is independently specified.

## Main conclusion and attribution

An energy-conjugate perturbation of resolved even observables need not add any identifying information. There is an explicit, established perturbation law for which **every controlled observed path is a causal time change of the unperturbed observed path**. Consequently an exact passive parity completion survives arbitrary admissible time-dependent fields, observation-based feedback, and the same native resets. The indistinguishability extends beyond linear response to all controlled path statistics and the work record supplied by those fields.

The departure-rate perturbation and its equilibrium-form response away from detailed balance are already explicit in Maes–Wynants (2010), equations (10) and the discussion following (20). Dembo–Deuschel (2010), Theorem 2.10 and Proposition 3.1, provides the broader invariant-measure and time-change framework. The project-specific step here is to apply that machinery to exact hidden parity completions and state the resulting full intervention-interface obstruction. No novelty is claimed for the perturbation law or the FDT formula.

## 1. Interface and control law

Let \(X\) be a finite, nonexplosive CTMC with row generator \(Q\), positive stationary distribution \(\pi\), and observed label

\[
Y_t=g(X_t).
\]

The labels in this theorem are deterministic functions of microscopic states. A singleton resolved port is allowed, as is a common hidden-interior label. Choose measured potentials \(V_k(x)=v_k(g(x))\). For a vector field \(h\), define

\[
a_h(y)=\exp[-\beta\sum_k h_k v_k(y)],\qquad
Q_h=D_h Q,\qquad D_h=\operatorname{diag}(a_h(g(x))). \tag{1}
\]

Thus every departure rate, including the escape rate, is multiplied by the same factor at a state. Conditional destinations at a jump do not change. This is a state-dependent clock operation, not a claim that every instrument implementing an energy perturbation has this kinetic law.

Equation (1) has the energy-conjugate ratio required by an energy change \(E_h=E-\sum_k h_kV_k\). For ordinary reverse pairs,

\[
\log\frac{q_h(x,y)}{q_h(y,x)}
=\log\frac{q(x,y)}{q(y,x)}
 +\beta\sum_k h_k[V_k(y)-V_k(x)]. \tag{2}
\]

An Arrhenius interpretation with fixed transition barriers and changed state well energies gives this departure-rate factor. Nonconservative affinities already present in the baseline rates are unchanged. For an even potential and an odd-variable reversal, the same identity holds with the reverse edge \(\theta y\to\theta x\).

This is an admissible family in the stated finite-state local-detailed-balance model class, not a constructed microscopic Hamiltonian device. A physical specification that also determines the field coupling in transition regions, bath mobility, or inertial equations can exclude the family. In particular, shifting all basin energies while holding transition barriers fixed is a physical barrier-height change, not a claim that a constant shift of the entire microscopic Hamiltonian changes dynamics. The native counterexample uses potentials supported only on resolved ports.

The allowed causal policy can choose \(h_t\) from laboratory time, the observed past, and an independent random seed. Require positive upper and lower clock-speed bounds on each finite horizon and a uniquely defined nonexplosive clock equation. Bounded piecewise continuous protocols and ordinary event-based feedback satisfy this condition. These assumptions exclude pathological undefined feedback and Zeno controls, not any information-bearing restriction to weak fields.

## 2. Observable-clock closure theorem

**Theorem.** Suppose two hidden Markov models have the same complete unperturbed observed path law for the stated initial preparations. Give them the same control law (1) through their common observed labels. Then they have the same controlled observed path law for every admissible causal field policy. If their native reset interfaces also give the same observed laws, the statement includes observation-based choices of reset port and reset time.

**Proof.** First fix the policy's external random seed. Given an unperturbed microscopic path \(X_s\), introduce an operational clock \(S_t\) by

\[
\frac{dS_t}{dt}=a_{h_t}(Y_{S_t}),\qquad S_0=0, \tag{3}
\]

where the feedback field is evaluated using the laboratory-time path \(\widetilde Y_u=Y_{S_u}\), \(u<t\). The standard time-change construction gives \(\widetilde X_t=X_{S_t}\) conditional intensities \(a_{h_t}(g(\widetilde X_t))q_{xy}\), precisely (1).

Crucially, equation (3) depends on the unperturbed path only through \(Y\). Under the stated uniqueness condition it defines a measurable causal transformation \(\mathcal T_h:Y\mapsto\widetilde Y\). Equal unperturbed observed laws have equal pushforwards under the same transformation. Averaging over the common external seed preserves equality. A reset terminates the current segment and restarts from the chosen preparation; condition on the observed reset history and apply the same argument successively. This proves the claim. \(\square\)

The theorem does not assume equal hidden dimension, equal generators, or a statewise coupling of the two hidden models. Hidden jumps that do not change the label are automatically included in the microscopic time change.

The usual control-work functional

\[
W_{control}=-\sum_k\int V_k(X_t)\,dh_k(t)
\]

is measured from the field and observed labels. Its law is consequently identical too. An energy current driving an unobserved nonequilibrium cycle is an additional physical resource, not this control-work record.

## 3. Generalized equilibrium survives the whole field family

Suppose a competing hidden model has a stationary-distribution-preserving physical involution \(\Theta\), even observations \(g(\theta x)=g(x)\), and generalized detailed balance

\[
Q^*=\Theta Q\Theta,\qquad Q^*=\Pi^{-1}Q^T\Pi.
\]

For each frozen field in (1), set

\[
\pi_h(x)=\frac{\pi(x)}{a_h(g(x))Z_h},\qquad
Z_h=\sum_x\frac{\pi(x)}{a_h(g(x))}. \tag{4}
\]

Then \(\pi_hQ_h=\pi Q/Z_h=0\), \(\pi_h\Theta=\pi_h\), and direct calculation gives

\[
(Q_h)^*=D_hQ^*=\Theta Q_h\Theta. \tag{5}
\]

The family remains generalized equilibrium under every frozen energy field, with the canonical reweighting \(\pi_h\propto\pi e^{\beta h\cdot V}\). This includes the escape-rate part of generalized balance; the proof is not restricted to off-diagonal flux ratios.

If two models have identical stationary output laws, their normalizers \(Z_h\) and the Radon–Nikodym factor of the initial preparation in (4) depend only on the common observed initial label. Thus stationary preparation at any frozen field also preserves the observed equivalence. This says that the preparations are statistically matched; it does not provide a physical preparation procedure for free.

## 4. Consequence for Astra's exact native-return completion

Use the completed shared-port construction in `branches/intervention_information_20261029/REVERSAL_INFORMATION_AND_INTERVENTION.md`, section 3. It gives a finite irreducible generalized-equilibrium model with the same actual singleton ports, native holds, and reciprocal weighted excursion kernel. Label each port separately and the whole hidden interior by one label. The original and completed models then have the same complete native observed process, including arbitrary resets to the ports.

Take potentials supported only on resolved ports. They are even because the completion fixes every port. Equations (1)–(5) prove that this exact completion survives **all fields on these resolved energy levels, all field strengths in the declared range, all admissible protocols, and all observation-based feedback and native reset choices**. Increasing the order of response estimation cannot resolve this ambiguity.

This is an exact finite-state statement. It uses no vanishing switching rate, unbounded hidden state count, instantaneous hidden evolution, or finite-horizon closure. Native escape-rate ceilings remain matched after applying a common bounded clock factor. A separately known preparation or hidden mixing constraint may impose further requirements and is not claimed to be preserved by an unspecified model replacement.

### Explicit five-state source and eight-state completion

Choose ports \(0,1\), hidden states \(2,3,4\), and stationary weights

\[
w=(1,1,2,3,5).
\]

Specify directed stationary fluxes \(f_{ij}=w_iq_{ij}\):

\[
f_{02}=f_{20}=1,\quad f_{12}=f_{21}=2,
\]

\[
(f_{23},f_{32})=(2,1),\quad
(f_{34},f_{43})=(3,2),\quad
(f_{42},f_{24})=(4,3).
\]

There are no other off-diagonal fluxes; choose diagonals by row conservation. Every vertex is balanced. The source has strictly positive ordinary entropy rate

\[
\sigma=\frac1{12}\left[\log2+\log(3/2)+\log(4/3)\right]
=\frac{\log4}{12}. \tag{6}
\]

It admits no nontrivial stationary-weight-preserving involution fixing the two ports: all three hidden weights are distinct and differ from the port weights. Thus this example is not merely the same five-state generator with an alternative admissible parity label.

All excursions enter and leave the interior through state 2. Writing \(S=Q_{II}\), the weighted return kernel is

\[
K(t)=\frac12[e^{tS}]_{22}
\begin{pmatrix}1&2\\2&4\end{pmatrix}, \tag{7}
\]

which is reciprocal for every duration. The shared-port completion has eight states, keeps the two ports once, and duplicates the three hidden states with weights \(w_i/2\). Its physical involution swaps the hidden copies, and its generalized entropy rate is zero. The theorem proves exact equality of every native controlled output under resolved-port energy clocks.

For a frozen field, the source's ordinary entropy is rescaled by \(1/Z_h\), since every normalized stationary flux is rescaled by that factor; the completion's generalized entropy remains zero. Their observable controlled data and field-work records still agree.

## 5. Why the measured FDT does not rescue this interface

For one potential \(V\), the derivative of (1) at zero is

\[
B^V=-\beta\operatorname{diag}(V)Q.
\]

Starting from \(\pi\), the impulse response of any terminal observable \(A\) is

\[
R_{V,A}(t)=\pi B^Ve^{tQ}A
=-\beta\frac{d}{dt}\langle V(X_0)A(X_t)\rangle_\pi. \tag{8}
\]

No detailed balance, involution, or zero entropy was used. Both competing models satisfy the same equilibrium-form formula. This is the known departure-rate example in Maes–Wynants, rather than a new FDT.

More generally, if a differentiable family \(Q_h\) has invariant distributions \(\pi_h\propto\pi e^{\beta hV}\), differentiating \(\pi_hQ_h=0\) gives

\[
\pi B^V=-\beta\pi\operatorname{diag}(V)Q,
\]

and hence the same response identity. This is the finite-state content of the invariant-measure FDT framework of Dembo–Deuschel. Their use of an invariant measure must not be misread as a conclusion of thermodynamic detailed balance.

There is still a valid positive direction: if a physically calibrated energy operation is guaranteed to maintain the canonical equilibrium family whenever the source is at equilibrium, a measured violation of (8) rules out that equilibrium hypothesis. Odd hidden states do not invalidate this necessary condition. What fails is its converse and any claim that the phrase energy-conjugate alone fixes the response law.

## 6. A common odd-variable control error

The symmetric edge tilt

\[
q_h(x,y)=q(x,y)e^{\beta h[V(y)-V(x)]/2}
\]

is a familiar energy perturbation for all-even reversible chains. It need not preserve generalized equilibrium when hidden variables are odd, even if \(V\) is even.

For example take uniform \(\pi\), \(\theta=(2\;3)\) fixing ports 0 and 1, and

\[
Q=\begin{pmatrix}
-3&0&2&1\\0&-3&1&2\\1&2&-3&0\\2&1&0&-3
\end{pmatrix}.
\]

This generator satisfies \(Q^*=\Theta Q\Theta\). For \(V=1_{\{0\}}\) and \(\beta=1\), the symmetric tilt has

\[
\left.\frac{d}{dh}(\pi_hQ_h)\right|_{h=0}
=(0,0,1/8,-1/8),\qquad \pi_h\propto\pi e^{hV}. \tag{9}
\]

It therefore fails the proposed equilibrium energy-family condition. Its hidden escape rates lose parity symmetry. Treating this kinetic rule as automatically supplied by physical energy conjugacy would create a false FDT inference against an equilibrium baseline. A mechanical perturbation of an underdamped system instead acts through its specified Hamiltonian force; the primary inertial response literature makes that action explicit.

## 7. Quantitative entropy needs a kinetic scale too

The local energetic ratio alone does not bound the magnitude of a response violation by the baseline entropy. To see this even in an all-even model, take a three-cycle with clockwise rates \(1+\delta\), counterclockwise rates \(1-\delta\), and uniform stationary law. Its entropy rate is

\[
\sigma_\delta=2\delta\log\frac{1+\delta}{1-\delta}\to0.
\]

For \(V=A=1_{\{0\}}\), \(\beta=1\), perturb rates by

\[
q_h(i,j)=q(i,j)\exp\{h[(V_j-V_i)/2+k_{ij}]\},
\]

where \(k_{01}=k_{10}=1/\delta\) and all other \(k_{ij}=0\). Since \(k\) is symmetric, the energetic ratio derivative is unchanged. But at \(t=0^+\) the response discrepancy is exactly

\[
R_{V,V}(0)+\left.\frac{d}{dt}\langle V(0)V(t)\rangle\right|_{0^+}=-2/3
\]

for every \(\delta>0\). The symmetric kinetic sensitivity diverges as \(1/\delta\). This does not produce identical full records, and does not rule out bounds that also use the measured kinetic scale. It rules out a positive universal entropy lower bound based only on this fixed response discrepancy, temperature, and potential range. Finite-amplitude derivative acquisition would also have to resolve the shrinking linear-response range.

## 8. Executable check and actual resources

`check_clock_response_obstruction.py` passes using exact rational arithmetic for all matrix identities. It verifies the five-state source and eight-state completion, six reciprocal Laplace-kernel identities, thirty field-dependent kernel identities, matched native hold factors, and 910 basis-observable/time-jet FDT checks. It also verifies the odd-variable symmetric-tilt failure (9) and five values of the unbounded-sensitivity counterexample. Displayed logarithms alone use floating point.

The arbitrary-protocol result is proved by the causal time-change argument; it is not inferred from those finite checks. There were zero physical source observations, zero physical preparations, and zero physical controls. The script and JSON are algebraic research artifacts, not an acquisition claim.

The useful next requirement is therefore specific: an additional operation must change something beyond an observer-measurable re-timing of an already acquired law, or the admissible physical model class must supply a kinetic/energetic restriction that excludes the exact completion. A response curve without that action contract does not do so.
