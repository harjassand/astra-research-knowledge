# Independent additive review: heterogeneous isotropic program inputs

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accepted** under the same fixed-frame, known-control and product-input conditions as the earlier noisy-transducer review, now allowing different input errors u,v.

The frozen B matrix has identical columns9i+j and9j+i exactly. Thus T=JB satisfies T SWAP=T on the full input space, not only on ideal rotation programs. Consequently the retained marginal of T(P tensor I)T† equals that of T(I tensor P)T†, and each is half the independently checked C1. Expanding tau_u tensor tau_v gives a_u a_v C0+(a_u b_v+b_u a_v)C1/2+b_u b_v C2. Exact independent algebra recovers

p=(405uv-360(u+v)+512)/864,
w=3[31(u+v)-9uv]/[405uv-360(u+v)+512].

For0<=u,v<=8/9, partial success derivative is(405v-360)/864<=0, so p>=p(8/9,8/9)=2/9. The error derivative is3[15872-4608v-9315v²]/denominator². Its numerator decreases over the interval and reaches4416>0 at8/9, so w increases strictly in each input error. Therefore u,v<=e implies p>=p(e,e) and w<=w(e,e), with exact isotropic retained output about the same q. The prior full-space covariance proof transfers these calculations from identity frame to every R.

A full classical transcript may specify different u,v. If the two states factor conditional on that transcript, the formulas apply branchwise. Coarsening the transcript can introduce classical correlations, but every successful branch has the same target projector and error at most w(e,e). The successful mixture therefore has that error bound as well: postselection only changes convex weights. The lower success bound also survives averaging. This does not assert unconditional quantum product structure after a shared cap, or factorization for a general memory-bearing source. All relevant quantum correlations must be absent conditional on the full transcript, not merely hidden by averaging its label.

The exact input-swap check and rational derivative/transfer checks are in `check_exact.py/json`. This receipt extends only the already received noisy-transducer interface; it does not independently accept the history-uniform growth/purification theorem that supplies bounds on u,v, nor a PBT resource/compiler theorem. No original files were modified.
