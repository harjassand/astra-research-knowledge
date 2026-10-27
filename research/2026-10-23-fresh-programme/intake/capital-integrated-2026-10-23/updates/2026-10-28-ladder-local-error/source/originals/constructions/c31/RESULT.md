# Resonance-pole result

The fixed-g small-detuning target is established by an explicit infinite-system contour deformation, followed by the exact two-dimensional hard-core compression and bounded analytic perturbation.

For the full physical Hη = Hg + η(nL − nR), g = 1/5, the bare-pair response has a simple outgoing resonance pole E(η), visible with nonzero residue in |LR⟩. It is analytic and even near η = 0, and

E(η) = E − η² B_out(E) + O(η⁴),

Im E(η) = −πρg(E)η² + O(η⁴), with ρg(E) > 0.

The sign is derived from the actual analytic pole, using the (H − z)⁻¹ convention. The outgoing sheet and positive local z/η domains are defined in PROOF.md. A finite fourth-order remainder bound is given there in terms of explicitly defined resolvent norms. No numerical usable η radius is claimed.

The needed separation is certified by exact rational interval computation: 5.9785 < E < 5.97865 < 6, while E+ + E− lies in (5.97931529997724990766, 5.97931529997724990767). Thus the internal two-band threshold at 6 and the nearby harmonic bound-bound pole do not obstruct the local construction.

Files:

- PROOF.md: full construction, continuation identity, simple-pole proof, coefficient, and remainder.
- certify_separation.py and separation_certificate.json: executed exact rational interval certificate, 1024 cells per band.
- contour_poles.py and contour_poles_*.json: executed, uncertified contour-quadrature checks retaining the full η perturbation and both hard-core constraints. These checks are not used to infer the infinite-system theorem.

Reproduce from this directory with `/usr/local/bin/python3 certify_separation.py 1024` and `/usr/local/bin/python3 contour_poles.py 100 0.2`. The certificate takes about 12 seconds on this host.

The supplied decimal πρg(E) ≈ 6.68375948395 × 10⁻⁸ remains uncertified; its strict positivity is analytical. The pole theorem does not establish an all-times exponential survival law, hardware lifetime, or practical advantage.

No primary pole-existence obligation remains within this construction. Independent audit has not been performed. The next quantitative attack is to bound the isolating radius and deformed resolvent norms, obtaining a numerical η radius and effective fourth-order error constant. The serialization failure encountered during the initial certificate run and its successful correction are recorded in PROOF.md.
