# Independent pointwise inverse-trace base-sector receivers

PASS, 27 October 2026, separately for scalar/reference-classical sources and doubly-flat qubit reference. No pinching/twirling lift to general coherent sources is received.

For a positive physical3x3 M of trace3, every eigenvalue lies below3, so e3(3e2-e3)=prod m_i prod(3-m_i)>0. Direct summation of1/m_i-4/(3-m_i)+1 gives the claimed cleared numerator. With centered eigenvalues, p<3 and e3=1-p+q. If q<0, positivity gives p+(-q)<1 and every term in the displayed decomposition is positive. If q>=0, the cubic's real-root discriminant gives q<=2(p/3)^(3/2), and the numerator decreases strictly with q. Exact substitution gives12r²(1-r)^3(r+2), with0<=r<1, strict unless p=0. The symbolic checker was replayed nonmutating and matched. Thus equality is exactly M=I, without an upper spectral cap.

Along I+s(M-I), unitality gives the exact derivative of2logdet NM_s-logdet M_s as R(M_s)/s. Integrating from identity proves the stated pointwise logdet result and strictness. Orthogonal reference-classical blocks with each marginal trace3 add exactly; no noncommuting reference reduction is inferred.

For physical3/qubit reference, full transpose followed by the qubit spin-flip unitary gives the actual output spectrum of[M+TrM I-(Tr_R M) tensor I-I tensor Tr_A M]/2. With both marginals flat this is(M+I)/2. Hence the inverse-trace objective is exactly sum(m_i-1)^2/[m_i(m_i+1)], and the logdet objective is sum log[(m_i+1)^2/(4m_i)]. Both are nonnegative and vanish only at identity, with no upper cap. This is an actual same-state spectral identity, not entropy congruence or pinching.

Consequently a hypothetical negative minimum in the received reference-two stationary problem must be both physically nonflat and nonclassical in reference. These exclusions do not establish the general inverse-trace sign.
