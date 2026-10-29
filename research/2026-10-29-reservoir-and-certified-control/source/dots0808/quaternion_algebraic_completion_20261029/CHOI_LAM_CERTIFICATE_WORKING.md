# Perturb-and-isolate beyond the SOS cone — completed, awaiting independent review

The accepted quaternion oracle has a complete but expensive rational-grid fallback. A nonnegative Choi–Lam quartic not representable as a quadratic-monomial SOS makes the fast SOS relaxation fail a small requested gap. This experiment tests a materially different algebraic mechanism, not another SOS level.

Input: f=w²x²+x²y²+w²y²+z⁴−4wxyz. The sum of its four nonnegative terms is at least4|wxyz|, so f>=0 on all real vectors; f(1/2,1/2,1/2,1/2)=0. Thus its true sphere minimum is independently known to be zero. This fact is an external check, not supplied as a solver shortcut.

All35 homogeneous quartic coefficients receive seeded rational perturbations. The exact l1 perturbation budget b is saved in input.json, with b<=epsilon/4 and epsilon=1/10000. Therefore |F−f|<=b on the unit sphere.

For the perturbed F, the exact critical ideal in chart w=1 uses partial_i F−q_i partial_0 F, i=1,2,3. A grevlex Groebner basis followed by FGLM produces shape polynomials A x+P(z), B y+Q(z), H(z), with degree H=40. Three additional projective boundary charts exclude every eigenray w=0. The separate resultant-boundary witness uses its own three-polynomial system and is not needed for this one-instance completeness argument.

certify_cholam.py isolates ALL real roots of H and refines rational intervals. The current run found28 real roots. At a stationary ray, the normalized value is partial_0 F(1,x,y,z)/(4(1+x²+y²+z²)); this Euler identity is evaluated with rational interval arithmetic. The smallest lower endpoint minus b bounds the original f globally. For each ray a rational unit quaternion is constructed by an arbitrary-precision stereographic map, and f is evaluated exactly to obtain an upper bound. A certificate is emitted only if upper−lower<=epsilon.

Status: COMPLETED. global_certificate_fast.json certifies all28 real stationary rays and original objective gap1.2935983156279698e−5 < epsilon1e−4. The original900s run timed out after15 values; the durable-cache successor re-isolated roots in545s. A separate fast=True exact refinement successor completed remaining values in123.5s using cached intervals and already-computed value rows. The slow successor remains a redundant bounded diagnostic; it is not needed for this certificate. Fast refinement changes computation only, not interval rigor or the proof. Governing executable is certify_cholam_fast.py, with input/shape/boundary and root caches hash-bound. The exploratory8192bit cap was not reached.

Scope: one small rational perturbation of one known non-SOS quartic, with executed exact global certification complete, receiving review pending. This does not yet establish an all-input success probability, bit-polynomial implementation, online speed advantage, or a practical padded control schedule. The generic resultant work is separate and unreviewed.
