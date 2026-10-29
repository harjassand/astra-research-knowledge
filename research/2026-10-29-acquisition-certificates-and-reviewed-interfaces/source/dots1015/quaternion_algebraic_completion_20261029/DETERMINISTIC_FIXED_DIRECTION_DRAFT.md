# Deterministic small perturbation from one certified good direction

2026-10-29 — additive author derivation, independent review requested. This does not modify the accepted generic template or Choi–Lam certificate.

## New exact witness
Let G be exactly the perturbed quartic in input.json (SHA47504933192c56f886a877e30d2dd7d20a4b1bfda82de3b22758eab546ac0dcd). The accepted Choi–Lam instance review binds its rational critical shape, degree40 U(z), and exclusion of all projective q0=0 critical rays.

check_fixed_good_direction_modp.py reduces the shape modulo prime1000000007. All required rational denominators are checked invertible. It verifies U remains degree40 and squarefree, and that norm N=1+P(z)²+Q(z)²+z² is invertible modulo U. It forms

 lambda(z) = (partial_0 G)(1,P(z),Q(z),z)/(4N) mod U.

The40×40 Krylov matrix with columns1,lambda,...,lambda^39 has determinant438433815 modulo the prime. Thus it is invertible over Q. Since Q[z]/(U) is a reduced40-dimensional algebra, lambda takes40 DISTINCT values on its complex points. Invertibility of N also lifts to Q, so all40 critical rays are nonisotropic. Every projective critical ray is covered, so a common Q=0,gradG=0 ray does not exist; the E-resultant is not identically zero. Its universal degree bound40 and the40 distinct normalized eigenvalues imply c40(G)Disc(R_G)!=0.

The separately accepted exact boundary-resultant witness proves B(G)!=0. Consequently Delta(G)!=0 for Delta=c40 Disc(R) B, the same polynomial as the accepted template theorem. This inference uses exact modular arithmetic and proof dependencies, not floating eigenvalues.

## Deterministic finite trial list
Delta is homogeneous of degree6972: c40 has degree68, discriminant has degree6864, and B degree40. Put A=sum_alpha |G_alpha|>0. For any input rational quartic F and epsilon>0 use the6973 rational values

 t_j = j epsilon/(4 A *6973),  j=1,...,6973.

The polynomial Delta(F+tG) in t has degree6972 with leading coefficient Delta(G)!=0, regardless of F. At most6972 distinct t are bad. Therefore at least one listed F+t_j G satisfies ALL good-template conditions. Each has coefficient-l1 distance at mostepsilon/4 from F.

Test the same exact good conditions and apply the same resultant-derivative coordinate extractor from the accepted theorem to the first good trial. A perturbed gap at mostepsilon/2 transfers to an original gap at mostepsilon. This is a deterministic terminating construction, with at most6973 fixed-template attempts and polynomial BIT cost in input/accuracy bit length. G and6973 are fixed constants. There is no random retry tail and no grid totalization needed in this theoretical construction.

## Controller and implementation scope
This strengthens theoretical template termination only. The actual complete universal template/eigenvalue extractor has not been implemented, and the exploratory critical/FGLM code's fixed-z shape condition is not automatically supplied by this trial test. The exact modular good-direction witness HAS been executed in0.87s. No full6973-trial optimizer run is claimed.

Under a supplied finite template implementation, the worst-case bit-operation bound can be chosen from public input-size/horizon bounds rather than a private hard-instance stopping time. This creates a polynomial-bit padding possibility at mathematical scope, with potentially astronomical constants; it does NOT establish a practical hardware clock, isolated source, buffering cost, or calibrated physical control. Conventional adaptive competitors can use the same optimizer.
