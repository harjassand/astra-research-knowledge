# The MEMORY moment gate can be uniform at all low temperatures

29 October 2026. Analytic sharpening; no new scalar/model fixture. This
does not change or re-qualify the frozen preparation theorem.

The earlier A_B=C_B(1+ceil(b))^4 is adequate for PROOF(7)--(8), but is
unnecessarily large for a FIXED passive bath with a positive spectral gap.
For b>=1 and Re z>=1/4,

    |exp(-bz)|<=exp(-1/4)<=4/5,
    |1-exp(-bz)|>=1/5.

The analytic square root of 1-exp(-bz) is fixed by its positive real
value; it has no zeros in the right half plane. Each thermal multiplier

    c_b(z)=[1-exp(-bz)]^-1/2,
    exp(-bz/2)c_b(z),    exp(-bz/4)c_b(z)

has absolute value <=sqrt(5)<3 in that half plane. Around each real
nu in[1/2,3/2], Cauchy's estimate on the radius1/4 circle gives

    |thermal_multiplier^(k)(nu)|<=3*4^k k!              (1)

for EVERY b>=1. This is temperature-uniform; no raw b^k bound is needed.
It applies to both square-root bath filters h_phys,b and their symmetrized
q_b after multiplication by the fixed flat f_minus.

Use the frozen F_j and T_k from clock_controller/RESOURCE_RECURRENCE.json.
For k=0,...,4, the new multiplier bounds are

    3*4^k k! =3,12,96,1152,18432,
    4T_k      =12,48,300,2712,32556.

Thus each new product derivative bound is at most FOUR times the B_k
already used in its exact C_B=64(1+max B_k) recurrence. With the constant

    A_0=4C_B,  C_B=22806356488960,                      (2)

four integrations by parts give g0,g1,g2<=4A_0 uniformly for all b>=1.
The convolution bound therefore pays

    sup_(b>=1) integral_R |u C_b(u)|du<=32 A_0^2.

Consequently the multi-time MEMORY receiver can use

    eta<=256alpha^2 A_0^2,
    alpha<=epsilon_0/(40A_0)=epsilon_0/(160C_B).         (3)

This bath coupling is independent of temperature, volume, block duration
and elapsed time, for the specified memory budget. The positive one-particle
gap and the chosen fixed spectrum are essential.

No such uniform-coupling assertion follows for microscopic-bath proximity
to the intended BARE-Hamiltonian KMS controller: its Lamb renormalization,
finite-temperature target and local same-block approximation remain separate.
Equations(1)--(3) strengthen only the exact fresh-block MEMORY comparison.
Nor do they make the finite closed bank an all-time reservoir.
