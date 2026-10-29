# Two-sided flow transformation and the fixed-native-port boundary

30 October 2026. Complementary constructive comparison for the nonlinear mobility diagnostic. No new worker or numerical fixture. This note distinguishes two actual physical interconnections that can have the same geometric constraint but different mobility, noise, native-current accounting, and resources.

## 1. Result and its consequence for selection

A conventional lossless multiport transformer can supply

\[
M_{\rm tr}=QMQ,\qquad
Q=I-H(H^*H)^{-1}H^*,\qquad BH=0,
\tag{1}
\]

without learning M. Its reciprocal two-sided constitutive relation is

\[
j=Qu,\qquad e=Qf.
\tag{2}
\]

Here u is the flow at the internal bath/device ports, e their effort, and j is the flow at the physical output ports under effort f. Power is conserved: \(f^*j=e^*u\). This is standard transformer machinery, not a new physical principle.

If the outputs in (2) are actually connected to the native carrier-displacement ports, this is a strong ordinary solution: it removes the selected circulation, and its unforced visible density law can remain exactly unchanged for arbitrary unknown native mobility, including an appropriately supplied nonlinear port. It is stronger than preserving a macroscopic Gaussian density action.

If the original native carrier motion is u, (2) changes an apparatus output while that native motion remains u. Calling Qu the native current would then change the task. To make j the actual native displacement, one needs an actual flow-conversion/interposition capability, a reconnected bath-to-carrier interface, or an additional actual circulating-carrier flow port. The existing reciprocal force attachment to a fixed native current port does not supply that capability.

There is a sharp passive fixed-port obstruction. For positive definite M,

\[
QMQ\le M\quad\Longleftrightarrow\quad QMH=0.
\tag{3}
\]

At an unchanged native dissipative current port, a linear passive force-only impedance attachment has low-frequency symmetric mobility at most M. Thus the generic QMQ law cannot be obtained by that attachment. Its apparent improvement over the force-constraint law is paid by changing which actual flows pass through the original dissipative elements. This is not a theorem excluding every nonlinear, time-dependent controller outside that specified constitutive interface.

## 2. Ordinary ideal supplier, including force and thermal noise

At temperature one, take a supplied internal linear port

\[
u=Me+\sqrt{2M}\,\xi,
\tag{4}
\]

with reciprocal positive mobility M. Connecting the ideal transformer (2) gives

\[
j=QMQf+Q\sqrt{2M}\,\xi,
\qquad
S_j=2QMQ.
\tag{5}
\]

Both force and noise are transformed. Keeping the original noise while replacing only the deterministic mobility would not give this passive equilibrium law.

The same algebra applies to a complete causal linear bath port with admittance Y(s):

\[
Y_{\rm out}(s)=QY(s)Q,
\qquad
S_{\rm out}(\omega)=Q S_{\rm bath}(\omega)Q
=2\operatorname{Re}[QY(i\omega)Q].
\tag{6}
\]

This does not reconstruct an arbitrary unknown bath from its equilibrium measure. It presumes the actual open effort/flow ports and their complete response/noise law. The ideal transformer itself stores no energy, but that idealization is not a finite-propagation apparatus guarantee.

A singular Q is an ordinary multiport transformer relation, not a forbidden inverse. One explicit interpretation is to resolve internal flows into an orthonormal basis of range Q and range H, transmit the allowed coordinates, and leave the excluded internal coordinates at zero effort. The excluded output flow is zero. Internal excluded currents can still circulate; they have not been erased from the original dissipative devices. Equivalently, use a lossless mode transformer, zero-effort termination of the internal excluded channel, and the inverse output mode transformer. The difference between an internal shorted channel and an output open channel is essential.

The primary literature gives precisely the reciprocal current/voltage matrix relation. Solgun and DiVincenzo, *Multiport Impedance Quantization*, arXiv:1505.04116, Section 3.1.1, equations (3.6)-(3.9), explicitly construct a Belevitch transformer with a rectangular turns matrix. Gernandt, Haller, Reis and van der Schaft, arXiv:2004.10821, Section 3.2.5, give the two-port power-conserving relation and its port-Hamiltonian interpretation. These actual sections were read for this note. Neither source supplies the locality or native-carrier identification needed here.

## 3. Exact visible-law preservation under the stronger port

Since BH=0,

\[
BQ=B,\qquad QB^*=B^*.
\tag{7}
\]

Suppose the visible storage has energy U(x), force \(f_0=-B^*\nabla U(x)\), and continuity \(dx=Bj\,dt\) or its stochastic-current analogue. Under (2), the internal device sees

\[
e=Qf_0=f_0,
\qquad dx=BQu\,dt=Bu\,dt.
\tag{8}
\]

Therefore a complete supplied causal internal port, driven by the same visible force and initialized in the same warranted state, has exactly the same closed visible trajectory law. This is a pathwise interconnection identity; Gaussianity, a finite predictive model, and estimation of M are unnecessary. Hidden memory can remain in the internal port if its complete actual constitutive interface has this form.

For a reversible state-dependent mobility model, the generator check is equally direct. If the actual equilibrium density generator is specified in divergence form,

\[
L_M\phi=e^{U}\nabla_x\!\cdot
\left(e^{-U}B M(x) B^*\nabla_x\phi\right),
\tag{9}
\]

then

\[
B Q M(x)Q B^*=B M(x)B^*
\tag{10}
\]

at every x, so the complete generator, including its thermal drift, is unchanged. It would be incorrect to infer the full nonlinear stochastic law from the covariance formula alone, or to omit the thermal drift.

This statement concerns the unforced storage dynamics and forces of the form B* times a visible potential. For an arbitrary external edge force f, the internal input becomes Qf. In general \(BM Qf\ne BMf\). Thus the transformer does not preserve every old force-response experiment, especially under heterogeneous mobility. Its force and work ports are those of (2).

If the internal hidden state is physically part of an unmodifiable carrier mechanism and its motion cannot be separated from the measured native flow, the open-port hypothesis has not been supplied. Equation (8) is then an architectural design, not an operation acquired from that hidden device.

## 4. The force-only reciprocal constraint is a different operation

Keep the native current itself j and add only reciprocal reaction forces H lambda. In an overdamped linear port,

\[
j=M(f+H\lambda)+\sqrt{2M}\,\xi,
\qquad H^*j=0.
\tag{11}
\]

Solving for the reaction gives

\[
M_c=M-MH(H^*MH)^{-1}H^*M.
\tag{12}
\]

The corresponding projected noise has covariance 2M_c. It is an M-weighted projection of raw increments, not the Euclidean output projection Q. The density covariance loss is

\[
B(M-M_c)B^*
=BMH(H^*MH)^{-1}H^*MB^*.
\tag{13}
\]

Consequently it vanishes exactly when BMH=0. This diagnostic remains load-bearing. The two-sided transformer does not refute it because the dissipative current in the transformer is u, whereas it is j in (11).

For a single ring with the entire circulation space protected, QMH=0 and BMH=0 coincide. For selective constraints on several rings, they need not coincide: M can mix the protected circulation with an allowed circulation while still leaving all density modes unchanged. That is exactly what unequal homogeneous ring resistances do in the accepted signed-ladder construction.

## 5. Passive fixed-port obstruction

### 5.1 Matrix proof

Choose orthonormal coordinates separating range Q from range H. Write

\[
M=\begin{pmatrix}A&C\\C^*&D\end{pmatrix},
\qquad
QMQ=\begin{pmatrix}A&0\\0&0\end{pmatrix}.
\]

Then

\[
M-QMQ=\begin{pmatrix}0&C\\C^*&D\end{pmatrix}.
\tag{14}
\]

A positive semidefinite block matrix with a zero diagonal block must have zero corresponding off-diagonal block: otherwise a vector with a suitably small signed second component makes its quadratic form negative. Thus (14) is positive semidefinite exactly when C=0, equivalently QMH=0. In that exceptional case QMQ=M_c.

### 5.2 Actual native dissipation

At a fixed deterministic native port with resistance M inverse, actual steady native motion j dissipates \(j^*M^{-1}j\). A passive controller driven only through the same effort/current port has no additional steady source of power. Hence a reciprocal static response j=Cf in this interface must satisfy

\[
f^*Cf\ge f^*CM^{-1}Cf\quad\hbox{for every }f.
\tag{15}
\]

For positive semidefinite C, this is equivalent to C at most M: conjugate by M inverse square root and use X squared at most X if and only if 0 at most X at most I. Therefore C=QMQ is impossible at the fixed port whenever QMH is nonzero.

This argument counts the original native dissipative current. It does not forbid a passive device from producing another output whose mobility exceeds M along some directions: transformers do exactly that by changing effort and flow ratios.

For a linear equilibrium frequency-domain force attachment, the same conclusion follows from an added positive-real impedance Z_c. This is the explicit stochastic port scope used for the mobility/noise comparison. The total native admittance is

\[
Y=(M^{-1}+Z_c)^{-1},
\qquad \operatorname{Re}Y\le M.
\tag{16}
\]

Indeed, writing the total impedance as K+iX with K positive and K at least M inverse gives
\(\operatorname{Re}Y=K^{-1/2}(I+(K^{-1/2}XK^{-1/2})^2)^{-1}K^{-1/2}\le K^{-1}\le M\).
The inequality survives ideal reactive constraint limits. Matched equilibrium controller noise gives the corresponding fluctuation-dissipation spectrum. The scope is a fixed Ohmic/Onsager port, or its specified low-frequency limit; arbitrary barrier-changing controls or a changed native bath are different ports.

Prepared nonequilibrium controller energy can power a finite transient, and an active current source can change the conclusion. Neither is a passive stationary counterexample to (15).

## 6. Concrete two-channel comparison and native-motion accounting

Let the two internal mobilities be m_1 and m_2, and protect their difference. Then

\[
Q=\tfrac12\begin{pmatrix}1&1\\1&1\end{pmatrix},
\]

\[
M_c=\frac{m_1m_2}{m_1+m_2}
\begin{pmatrix}1&1\\1&1\end{pmatrix},
\quad
QMQ=\frac{m_1+m_2}{4}
\begin{pmatrix}1&1\\1&1\end{pmatrix}.
\tag{17}
\]

The force-constrained common response uses the harmonic combination. The transformer output uses the arithmetic combination. The latter is larger when the mobilities differ; it has proportionately larger equilibrium output noise. There is no precision gain at unchanged response.

Take m_1=1, m_2=4 and f=(1,1). The fixed-current constraint yields j=(8/5,8/5). The transformer yields actual output j=(5/2,5/2), but its internal device currents are u=(1,4). Its external power is 5 and its internal dissipated power is 1+4=5.

If instead one claimed that the original native dissipative elements both carried 5/2, their dissipation would be

\[
(5/2)^2+(5/2)^2/4=125/16>5.
\]

That is the concrete missing power under the fixed-port interpretation. The transformer does not supply it; it carries different currents internally and externally.

For the two N-site rings, the same calculation applies to their normalized harmonic coordinates. With m_a=1/r_a, the accepted force-only signed ladder has common per-ring mobility 1/(r_1+r_2), whereas a true two-sided global transformer would have (1/r_1+1/r_2)/4. Both can be passive, but they are different physical interfaces and different work/noise laws.

## 7. What would make the transformer meet the actual native-displacement task?

There are three distinct implementations to keep separate.

1. **An apparatus readout or output shaft.** Leave native carrier motion u intact and report or use Qu on another channel. This is an ordinary useful transducer, but it does not suppress the originally requested native circulation.
2. **Actual interposition between baths and native carrier outputs.** Put the original dissipative elements behind the two-sided transformer and connect its output currents to the native storage/carrier channels. An electrical or mechanical device with accessible bath and output ports can implement this architecture in the ideal network model. The density dynamics then obey (8), and j is a real output carrier displacement. This meets the observable task on that constructed device, at the stronger reconnectable flow-port interface. It is not obtained by adding a force controller to the unmodified native dissipative current.
3. **An additional actual circulating-carrier port.** Supply a reciprocal flow contribution \(w=-(I-Q)u\) in parallel, so the total counted native current is j=u+w. To remain passive its reaction must also transform the effort to Qu's reciprocal value Qf. This requires a real carrier-flow converter with the needed correlation; a noiseless numerical subtraction, a sensor alone, or an uncounted apparatus current does not suffice.

In case 2, an electrical transformer transfers energy between windings, not the same carriers between its input and output. The output circuit may carry real charge, but the charge trajectories in the old dissipative elements remain different. Which branch current is the native observable must be fixed before the comparison.

These are capability boundaries, not a universal prohibition on passive physical construction. If the stronger flow interposition is genuinely available, it should change the selection: exact visible-law preservation is already supplied by ordinary transformer geometry.

## 8. Locality, bandwidth, and integer carriers

For a global harmonic H, Q is dense. An instantaneous Belevitch relation supplies nonlocal feedthrough. Factoring its known matrix into local ideal two-channel rotations or transformer junctions does not by itself restore finite propagation: a chain of massless algebraic constraints can transmit an input instantaneously along the entire chain.

For one uniform protected mode, one can explicitly accumulate the normalized partial sum using successive orthogonal two-channel mixers, retain the contrast outputs, remove the final sum channel, and apply the inverse mixing network. This uses order N ideal mixers; ratios can be chosen with magnitudes at most one. On a spatial ring, however, the response path spans order N distance. A physical finite-response version must pay propagation, loading, matching, internal storage and preparation. Its low-frequency transfer and thermal noise must be derived. The observation that N distance is shorter than N squared observation time is an opening for construction, not a proof that unknown loads leave an adequate response band. No such finite-bandwidth universal transformer is asserted here.

A local pointwise two-ring gear produces j_(1,i)=j_(2,i). That locks x_1-x_2 at each site and fails the independent nonflat-density task. The desired global constraint removes only the harmonic difference, so the pointwise gear is not an equivalent local realization.

Exact feedthrough also has a causal response test. A fresh localized internal flow or output force changes the ideal Q relation at distant sites immediately. Prepared correlations can reproduce some unconditioned covariance, but they cannot transmit that independently selected new input before the apparatus response reaches those sites. Both the force side and the flow side of a real transformer must be included.

There is a further literal boundary for lattice particles. On a ring, a single native hop has integer current increment e_i. Projecting it gives \(Qe_i=e_i-1_N/N\), which is fractional on every bond. On two rings with one protected harmonic difference the analogous subtraction is fractional across both rings. This is not a single permitted native particle transition with the same recorded density change. An actual implementation needs additional collective moves, physical circulating carriers, packet accumulation, or another microscopic transport port. This observation does not rule out an asymptotic particle construction; it rules out treating multiplication by Q as an acquired microscopic operation.

## 9. Source record and conclusion

Primary sources actually opened and read:

- Solgun and DiVincenzo, *Multiport Impedance Quantization*, arXiv:1505.04116, Section 3.1.1 and equations (3.6)-(3.9): https://arxiv.org/pdf/1505.04116 . The actual rectangular current/voltage transformer relation is the close ordinary construction.
- Gernandt, Haller, Reis and van der Schaft, *Port-Hamiltonian formulation of nonlinear electrical circuits*, arXiv:2004.10821, Section 3.2.5: https://arxiv.org/pdf/2004.10821 . The actual transformer current, voltage and power relations were read.
- Van der Schaft and Maschke, *Port-Hamiltonian systems on graphs*, arXiv:1107.2006, Sections 2.1-2.3: https://arxiv.org/pdf/1107.2006 . The graph flow/effort and power-conserving interconnection definitions were read.

The algebraic construction and passive boundary above were developed directly for this task. No novelty is claimed for transformer congruence, constrained Onsager mobility, or power-conserving interconnection. No new fixture, apparatus validation, or precision budget was added.

The appropriate conclusion for the nonlinear attack is conditional and concrete: the force-only native-current interface retains the BMH diagnostic; an actual two-sided native flow interface can bypass it and preserve the full density generator. Establishing that stronger local finite-bandwidth interface is a separate physical construction, not a consequence of writing QMQ.
