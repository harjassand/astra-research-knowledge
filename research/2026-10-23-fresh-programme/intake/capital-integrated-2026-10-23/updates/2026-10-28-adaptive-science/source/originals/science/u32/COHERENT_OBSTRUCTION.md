# Why a finite positive gauge cannot be universal

This is a representation obstruction for the mechanism in
POSITIVE_GAUGE_THEOREM.md, not a learning lower bound for N952 and not a
novel quantum/classical separation claim. The positive-realization and
quantum-versus-classical distinction is established literature; see
[Monras and Winter (2014)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99),
[Adhikary et al. (2020), Section 2](https://proceedings.mlr.press/v108/adhikary20a/adhikary20a.pdf),
and [Fanizza, Lumbreras and Winter (2024), Sections 2.2-2.3](https://link.springer.com/article/10.1007/s00220-023-04913-4).
The explicit controlled two-action argument below is derived here to state
the exact remaining quantifier boundary. Its all-horizon approximation
argument is not used as an acquisition or practical-advantage claim.

## Legal rank-three CP family

Let the memory be one qubit, initialized to |0><0| at each supplied whole
process start. Choose theta/pi irrational. The finite legal action library is:

* R: conjugate by the real unitary U_theta=[[cos theta,-sin theta],
  [sin theta,cos theta]], returning a deterministic outcome zero.
* M: perform the projective Z readout with CP branches
  rho -> |0><0| rho |0><0| and rho -> |1><1| rho |1><1|.

Both outcome sums are TP; the maps are time homogeneous. Their matrices are
part of this mathematical counterfamily, not supplied to a count learner.
Repeatable starts and an architectural rank bound three satisfy N952's
interface. All reachable Hermitian states stay real symmetric. In homogeneous
Bloch coordinates (t,x,z), the signed observable realization is

    R = [[1,0,0], [0,cos(2theta),sin(2theta)],
                    [0,-sin(2theta),cos(2theta)]],
    M_0 = [[1/2,0,1/2], [0,0,0], [1/2,0,1/2]],
    M_1 = [[1/2,0,-1/2], [0,0,0], [-1/2,0,1/2]],
    c_0=(1,0,1),      trace=(1,0,0).

Three distinct rotations of c_0 span the three-dimensional real symmetric
space. Trace plus two rotated readout effects span its dual. Thus the exact
observable rank is three, not merely an empirical small singular value.
The event "after n discarded-outcome R actions, M returns zero" has probability

    p_n=(1+cos(2n theta))/2.                            (1)

## Finite positive models fail exact all-future realization

Suppose a valid finite positive controlled HMM with q hidden states gives the
same process. Discarding all outcomes of its R action gives a column-stochastic
matrix P. Its next M-zero probability is f^T P^n c with 0<=f<=1 and c a
probability vector. Any finite Markov chain has finitely many recurrent
classes, each with a finite period; its transient and nonperipheral modes
decay. Taking a common multiple m of those periods, every response sequence
f^T P^(km+r)c converges to a constant a_r for each residue r.

But theta/pi irrational implies that 2(km+r)theta modulo 2pi is dense on
the circle. Along that same residue class, (1) has liminf zero and limsup
one. It cannot converge. This contradicts exact equality for all n.

This argument already allows an arbitrarily large but finite number q of
classical states; increasing q beyond the minimal rank does not close the
gap. A signed three-dimensional OOM and a qubit CP instrument represent
the process exactly. Thus the positive finite realization searched for in
the acquired simplex theorem is an additional sufficient property, not a
consequence of finite CP memory or finite observable rank.

## Uniform approximation below one half also fails without a horizon

The same proof gives the stronger quantifier statement

    sup_(n>=0) |p_n-f^T P^n c| >= 1/2.                (2)

For any residue r, the positive model tends to a_r. Dense quantum subsequences
approach both zero and one, so the limsup error is at least
max(a_r,1-a_r)>=1/2. This is a lower bound on the single final binary readout
event, hence also on full transcript TV for at least one finite legal policy.
It applies to a valid stochastic finite model, not arbitrary nonnegative
matrices with unconstrained growing powers.

If a fitted model emits extra outcomes during R, one can either discard
them (the stochastic P argument above, using the event that ignores R
outcomes) or study its substochastic zero-outcome matrix. Discarding them
already proves (2) for the legal policy using only the final M readout.

There is no contradiction with finite-horizon approximation. A finite model
can retain enough classical phase resolution for any fixed maximum horizon.
Likewise a paid abort clock suppresses very long experiments and changes the
task. No lower bound in (2) has a fixed positive abort probability; no
impossibility is claimed for the clocked approximate reuse task.

## Geometric view of the same gate

The normalized reachable rotations are dense on the unit Bloch circle in
the real (x,z) plane. Rotated readout tests are dense in its dual circle.
Consequently the smallest closed reachable cone and the largest cone with
all future test probabilities nonnegative coincide with the real qubit PSD
cone; its trace-one section is a disk. A finite positive realization would
supply a polyhedral cone between them, forcing a finite polygon to equal
the disk. This restates the standard invariant-cone obstruction.

The useful next acquisition question is therefore a confidence geometry
supporting a nonpolyhedral observable cone (or another positive output-law
construction), with actual shot conditioning and adaptive-use cost. Merely
enlarging a finite simplex search cannot establish the universal theorem.
