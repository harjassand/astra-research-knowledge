# Final boundary and infinitesimal-split review

I reviewed `BOUNDARY_PROOF.md`, `certify_boundary_split.py`, and the updated interval root construction in `certify_joint_cap.py`. The finite split certificate reran PASS. I found no load-bearing error.

For positive finite caps, the feasibility statement is correct. The physical load f=(-1,m_1,...,m_n) sums to zero, and the common-side trial displacement has f dot x=1 and energy k_incident. The pseudoinverse Rayleigh inequality therefore gives C>=1/k_incident>=1/kappa. The one-pendant construction supplies the converse. At cap-product equality, the actual compliance and total spring expenditure both saturate, all internal spring expenditure must be incident to the backbone, and equality in the Rayleigh inequality gives k_j=kappa*m_j. All branch squared frequencies then coincide and the active response is the single-pendant response. Dark star modes are possible, as the text states. The caps should be understood as positive numbers.

The modal-split perturbation has the correct resource and transport coefficients. Its exact compliance identity charges the added branch contribution epsilon/v. Expanding the remaining spring gives total stiffness `20+64*epsilon+O(epsilon^2)` at v=100. The new normalized coupling is `-v*sqrt(epsilon)`, its diagonal is exactly v, and its limiting old block is A0 or Api. Schur complementation therefore gives the two stated squared-edge shifts. Sherman–Morrison gives `Gpi=G0/(1-4*G0)` with the stated sign, and converting squared-edge separation to frequency bandwidth gives

`gamma=2*v^(3/2)*G0^2/(1-4*G0)>0`.

The old band edges are simple and separated from v=100. Their shifts are O(epsilon), but the dual is zero at them, so their contributions to the dual integral are O(epsilon^2). The new band contributes `epsilon*gamma*R1(10)+O(epsilon^2)`. All three exact resource moments cancel, so this is also the objective difference to first order. The interval certificate gives strictly negative R1(10) and strictly negative leading objective coefficient. These analytic expansions are enough for the asserted existence of an improving finite network at every positive spring slack; no uniform epsilon or fabrication-precision bound is being inferred.

The executed epsilon=1/10000 network includes all three passbands and certifies

`J_one-J_split in [0.000000054891912382394915,0.000000054891912382394916]`.

The cost and gain therefore support the exact claimed scope: at C_cap=1/20, every positive spring slack above the one-pendant feasibility boundary permits a strict extra-mode improvement. This does not prove the split optimal at its own budget or establish a practical-device benefit.
