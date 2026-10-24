# Independent exact matrix check of the pinching obstruction

Use the ordered basis (00,01,10,11,20,21), ψ=(|00>+|11>)/sqrt(2), u=|20>, σ=|ψ><ψ|+εI6, and H=|ψ><u|+|u><ψ|. Then Tr_A H=0 exactly. The only nonzero upper off-diagonal entries of H are H[00,20]=H[11,20]=1/sqrt(2).

Partial transposition sends the second term |11><20| to |21><10|. Therefore N(H)=−H^(T_A)/2 has top-to-bottom block

Y = −1/(2sqrt(2)) [[1,0],[0,0],[0,1],[0,0]].

The output baseline top block is P_singlet/2+εI4, where |singlet>=(|01>−|10>)/sqrt(2), and its bottom block is (1/4+ε)I2. Consequently

||Y||_HS²=1/4,
||P_singlet Y||_HS²=1/16,
||(I−P_singlet)Y||_HS²=3/16.

The singlet and complementary top eigenvalues are 1/2+ε and ε; the bottom eigenvalue is 1/4+ε. Each top-to-bottom metric contribution is counted twice because the tangent is Hermitian. Using the BKM divided difference therefore gives

g_output = 2(1/16) log[(1/2+ε)/(1/4+ε)]/(1/4)
         + 2(3/16) log[(1/4+ε)/ε]/(1/4).

This is exactly the root's two-term formula. Input vectors ψ,u are orthonormal eigenvectors with eigenvalues 1+ε,ε, so g_input=2log[(1+ε)/ε]. The ratio tends to 3/4, not 1/2.

The executable exact matrix check passes all these identities. Replaying `wh3_pinching_half_bound_interval.py` at ε=1/100 confirms a ratio in (0.56596673210596123972949, 0.56596673210596123972950) and an output-minus-half-input metric excess greater than 0.60888883754238.

For density-state use normalize σ by Z=1+6ε, retaining the tangent H. Both metrics acquire the same factor Z. Small enough positive or negative perturbations remain faithful. Physical 2⊕1 pinching removes H, preserves the reference marginal, and commutes with N. The entropy pinching identity then gives

F(σ/Z+tH)−F(σ/Z)
=2D(N(σ/Z+tH)||N(σ/Z))−D(σ/Z+tH||σ/Z)>0

for all sufficiently small nonzero t. The inequality follows from the strictly positive second derivative and its Taylor expansion, not from an unverified finite step size. This refutes free pinching monotonicity and half-contraction of cross-sector coherence. It does not refute F≤−log 3: the baseline has a nonzero safety margin.
