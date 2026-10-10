# Fractional-replica gate for an amplifier entropy mechanism

10 October 2026. Root direct mathematical investigation; no novelty or foundational-result claim.

## Intended mechanism and decisive test

A possible pure-product amplifier proof would express integer output moments as cyclic integrals and use multilinear Gaussian extremality. Before attempting a large replica calculation, test whether even ALL thermal upper bounds on integer moments would entail the required von Neumann entropy bound. This logical sufficiency test does not assume the integer moment bounds have been established for the channel.

## Exact obstruction

For gain two, the vacuum amplifier output is thermal with eigenvalues t_k=2^(-k-1). Its integer m-th trace moment is 1/(2^m-1), and its von Neumann entropy is 2 log 2.

Consider instead the rank-three flat state sigma with eigenvalues (1/3,1/3,1/3). For every integer m>=2,

Tr sigma^m = 3^(1-m) <= 1/(2^m-1) = Tr tau^m.

Proof: 2^m-1<=3^(m-1), with equality at m=2. Induct because 2^(m+1)-1=2(2^m-1)+1<=2*3^(m-1)+1<=3^m.

Nevertheless S(sigma)=log 3<log 4=S(tau). Also the largest eigenvalue of sigma is 1/3<1/2, so adding the operator-norm bound does not repair the implication. Sigma can be realized on Fock levels 0,1,2 and has mean occupation one, the same as tau. Thus even a matching mean-energy constraint does not repair this inference.

Sigma is NOT asserted to be the output of a pure-product gain-two amplifier. This is an obstruction to using only those scalar moment and energy inequalities, not a channel counterexample or an entropy-inequality refutation.

## Consequence for research allocation

A proof of all integer replica bounds alone is insufficient. The indispensable new step must control fractional powers approaching one, establish genuine channel-specific spectral restrictions beyond these moments, or directly control entropy. Developing more integer cases without such a step would not close the landmark obligation and is not a justified depth programme.

The scalar thermal-sharp Fisher route was independently refuted in the companion investigation. No surviving fractional-power mechanism has been constructed here. This sufficiency check preserves a precise boundary rather than advertising a new proof route.
