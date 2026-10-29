# Optical T2 does not acquire the new parked-memory noise

The source's fitted optical two-level coherence does not identify a unique
generator on the PROPOSED encoding (S-1/2,S+1/2,D-5/2). The cited Wu Methods
III.1--III.3 do not document those numerical Zeeman assignments or the field.
Laser and magnetic noise can agree on the original coherence
while disagreeing on the ground memory. Original0.52 visibility is not assigned
to this sequence.

An explicit SCENARIO uses independent magnetic and optical-phase Markov noise:
sqrt(f/(2T))*diag(-1,+1,-3) and sqrt((1-f)/(2T))*diag(+1,+1,-1), f in[0,1].
Their optical S-/D decay is1/T, ground S-/S+ decayf/T, and S+/D decay(1+3f)/T.
Equal magnetic sensitivity is useful only within this specified noise model.
An independent sqrt(2*gamma)*|S+><S+| dephaser leaves original optical qubit
calibration unchanged while adding gamma to S+ coherence decay. Optical T2
alone therefore bounds neither gamma nor the full new instrument. This is
an identification boundary, not an assertion that the apparatus has that fault.

Important source qualification: Wu et al., arXiv:2511.19687v2, III.3 explicitly
attribute their physical model to magnetic-field and trap-voltage fluctuations,
with Ramsey Tspin=2.8(3)ms and Tmotion=85(+98/-35)ms. They also fit an extra-wait
visibility decay tau_d=0.92(6)ms. Thus f=1,gamma=0 is a conditional extension of
their stated magnetic-noise model to the proposed three-level encoding; it is
not an arbitrary favorable embedding. Neither their stated assumption nor the
two-level Ramsey fit measures the parked ground-doublet coherence or establishes
noise completeness for added RF/optical controls. No source contrast or tau_d is
assigned to the new sequence. Primary: https://arxiv.org/html/2511.19687v2 .

noisy_kernel_model.py is an UNEXECUTED scenario library. Its current constructor
NativeModel(magnetic_fraction,extra_ground_rate,N=100,rtol=1e-7) requires f,gamma
explicitly; it has no default for either. No fixed favorable-noise run, noisy kernel or measured parkedT2
is claimed. It is not a governing positive result. The kernel receiver accepts
a separately warranted full-instrument error budget, including noise, all
modes, other Zeeman edges and analysis/readout. That budget is not supplied by
the source. A loaded apparatus experiment is outside authorized actions.
