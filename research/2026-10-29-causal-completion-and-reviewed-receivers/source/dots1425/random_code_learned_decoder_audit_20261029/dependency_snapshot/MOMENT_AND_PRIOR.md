# Independent moment check and primary random-code predecessor
2026-10-29. Supporting calculation for root's random-encoder/learned-decoder composition; not an independent acceptance receipt for the whole architecture.

Let N:D->B be CPTP with Kraus rank at most r, and let its complement T:D->E have dimension at most r. Write a=Tr[T(I_D)^2] and b=Tr[N(I_D)^2]. For the first k columns e_i of a Haar unitary, form the normalized Choi state J_RE of T restricted to the code and Delta=J_RE-(I_k/k) tensor T(I_D/D). Then
 E||Delta||2²=(kD-1)/(kD(D²-1)) * (b-a/D), for D>1.

Derivation: the same-column Haar moment is (I+F)/(D(D+1)); the distinct-column off-diagonal moment E[|e_i><e_j| tensor |e_j><e_i|] is (F-I/D)/(D²-1). Thus
 ETrJ_RE²=(a+b)/(kD(D+1))+(k-1)(b-a/D)/(k(D²-1)).
Subtract the mean-product squared norm a/(kD²), yielding the displayed formula. The identity relating the channel/complement swap contraction to b follows directly from a Stinespring isometry and trace exchange. Since N(I_D)<=r I_B and TrN(I_D)=D, b<=rD. Also rankDelta<=kr. Jensen and Cauchy–Schwarz give E||Delta||1<=r sqrt[kD/(D²-1)].

Uhlmann applied to J_RE versus(I_k/k) tensor T(I_D/D) gives a decoding isometry with Fe at least their squared fidelity. Fuchs–van de Graaf then gives Fe>=1-||Delta||1. This is an existence statement about the optimal code decoder; the learned physical decoder is a separate operational bridge. The source must be fixed independently of the seed. The conclusion is an average over seeds, not every code.

## Direct primary predecessor
Rochus Klesse, *Approximate quantum error correction, random codes, and quantum channel capacity*, quant-ph/0701102v2, Sec4.2 Eq28: https://arxiv.org/pdf/quant-ph/0701102v2 . The paper already proves a Haar-code average optimum fidelity lower bound1-sqrt(k r)||N(I_D/D)||F. For the same-space channel setting stated there, b<=rD gives1-r sqrt(k/D), slightly sharper than the fixed-environment-marginal calculation above. Its Kraus-product proof extends to rectangular outputs by the same trace identities, but that extension should be identified as a transfer rather than misquoted as the paper's stated notation. The paper's random-code performance is established prior work, not a new theorem here.

The second-moment argument uses only degree(2,2) polynomials in the encoder unitary. Therefore an exact unitary2-design can replace Haar. Standard Clifford design and finite sampling precedents: Dankert–Cleve–Emerson–Livine quant-ph/0606161; Koenig–Smolin1406.2170. Their exact compiler details must be attached to any native-resource statement. The possible new transfer is not random coding itself, but feeding a code of bounded output support into an actual forward-query learned physical decoder without supplied N.
