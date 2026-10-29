# Long memory does not give rapid full-Gibbs initialization

29 October 2026. An ordinary consequence of the accepted receiver, with its
precise limitation stated. Trace distance is D(rho,sigma)=||rho-sigma||_1/2.

Let T_t fix rho, and let Enc,Dec define a decoded qubit channel Lambda_t.
Assume the all-input receiver gives overlap fidelity at least 1-eta with
the identity for both logical basis states 0 and 1. Measuring the decoded
Z basis then distinguishes Lambda_t(0) and Lambda_t(1) with error at most
eta for each input. Consequently

    D(Lambda_t(0),Lambda_t(1))>=1-2eta.

For the single fixed state Dec(rho), the triangle inequality implies

    max_(b=0,1) D(Lambda_t(b),Dec(rho)) >=(1-2eta)/2.

Data processing now gives the actual full-system statement

    sup_omega D(T_t(omega),rho) >=(1-2eta)/2,               (M1)

where the supremum includes the two legitimate initial states Enc(b).
Thus if eta<1/4 throughout the proved storage interval, this exact sampler
cannot mix all initial states to rho in trace distance 1/4 within that
interval. This conclusion needs no spectral-gap theorem or detailed balance.

It is not a lower bound on arbitrary state-preparation algorithms, on preparing
the ancilla tau=Tr_L(UrhoU†), or on a sampler restricted to one logical sector.
Logical mixing can be slow while syndrome/ancilla equilibration is fast.
Those restricted preparation tasks need a separate constructive argument.
In particular (M1) must not be used either to grant or to rule out efficient
thermal encoding in the present theorem.
