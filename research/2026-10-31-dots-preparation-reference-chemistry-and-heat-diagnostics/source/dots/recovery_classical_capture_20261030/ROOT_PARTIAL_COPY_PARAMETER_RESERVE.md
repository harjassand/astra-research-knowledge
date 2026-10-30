# Proof-parameter reserve during a finite noisy copy layer
30 October 2026. Root local receiving lemma, conditional on the initial mixed-animal pullback and the actual rooted noise bound. Not a complete multirecord capture theorem.

Let the final new-graph animal weights be f_A=exp[-u L |A|+L k_A], L=log(1/theta), with 0<=k_A<=|A|. Suppose the copy pullback supplies an initial sharper parameter pair

 L_start=M L_end,  u_start=u_end/(2 C M), C>=1.

Set a(t)=u(t)L(t), and during the physical copy interval of duration tau choose a(t) increasing LINEARLY from u_end L_end/(2C) to u_end L_end, while L(t) decreases linearly from M L_end to L_end. Then exactly

 d f_A/dt = [-a'(t)|A|+L'(t) k_A] f_A
           <= -a_* |A| f_A,
 a_*=u_end L_end(1-1/(2C))/tau>0.

Thus the parameter path itself supplies a negative multiple of W, even with classical majority/reset service paused during the copy. No occupied-fraction assumption is used. Verify separately that all parameters along this path remain in the actual sparse-animal/coverage admissible region. The identities are about the proof observable, not a physical cooling operation.

Let U_t be the actual NOMINAL constant-depth local copy circuit, with U_tau=U_copy. Define the moving physical witness

 V(t)=U_t U_copy† V_new(u(t),theta(t)) U_copy U_t†.

At t=0 this is the exact full-copy pullback at the sharper parameters; at tau it is the desired new-graph ordinary witness. Its explicit derivative cancels the nominal copy Hamiltonian in the expectation derivative. This direction of conjugation matters; using U_t† V_new U_t would not describe the stated endpoint.

A local HP perturbation pulled back through this fixed-depth circuit has bounded support/incident-norm inflation. If the rooted oscillation calculation gives N^*V(t)<=C_eta eta W(t), uniformly over this fixed parameter path, choose eta<a_*/(2 C_eta). The actual positive state then obeys d E[V(t)]/dt<=-a_*/2 E[W(t)]. For Z(t)=1+K V(t), the same statement holds with K W(t). The bound includes arbitrary common bath and dirty target states admitted by the initial mixed-animal moment; no independent copy/reset outcomes or Pauli trajectories are used.

With a fixed root port that is NEVER a copy target, the copy gates preserve its actual Z value. Quantum read couplers controlled by that Z commute with the copy. In a joint quantum/rooted witness, any wrong-port read contribution can be paid from an additional portion of the parameter reserve, provided the same pointwise wrong-port-to-rooted-potential lower bound holds throughout the path. This costs a finite rate/time inequality; it is not automatic at arbitrary slow copy speed.

Remaining obligations: actual mixed-graph feature-map constants at the initial pullback; sparse-region admissibility of the parameter path; concrete noisy-reset acquisition of its starting moment; global phase-basin exits and simultaneous bad-block/source classification across growth. The local estimate alone is not an accepted noisy capture or stable read construction.
