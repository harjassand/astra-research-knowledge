# Finite pulse duration can be charged locally

For a specified private random-Z controller acting over a finite window, the same product method remains valid even when the unknown own-parity-flipping interaction continues during the pulse.

Let a,b be the interaction actions outside the window, c its action inside, and eta the magnitude of the isolated private phase average. If F(a,b,eta) is the exact partial-node value from the preceding packet, a valid local certificate is

    R = sin²(min(arcsin sqrt(F) + c, pi/2)).

The joint endpoint effect is bounded by the product of these R values across coordinates, including overlapping windows and a shared bath.

This requires a genuinely hidden independent controller register and an exact local random-Z coupling; other Hamiltonian coefficients cannot read that register or its discarded environment. Without that condition a diagonal baseline can cancel the random pulse. The actual finite pulse is analyzed, rather than replaced for free by an instantaneous node channel.

For balanced phases +/-theta and controller Hamiltonian norm at most Omega_max, a square pulse requires tau>=theta/(2 Omega_max). If the concurrent interaction norm is bounded by J, use c<=J tau. These are conditional specifications, not measured hardware parameters or an error lower bound.

The finite-width certificate is not claimed sharp. The prior ideal and partial-node packets remain unchanged.
