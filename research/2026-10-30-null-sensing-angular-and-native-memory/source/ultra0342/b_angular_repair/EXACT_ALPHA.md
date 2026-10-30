# Exact angular primitive

For A=[[a,b],[c,d]], put T=a²+b²+c²+d², X=a²+c²−b²−d², Y=2(ab+cd), Z=2(ad−bc), and (x,y,z)=(X,Y,Z)/T for A≠0. Let eta=(a dc−c da+b dd−d db)/T. Define

    alpha=T²[f(x,z) eta + p(x,z)(y dx−x dy)
                          + r(x,z)(y dz−z dy)].

Here dx,dy,dz mean exterior differentials of the NORMALIZED Hopf coordinates. The exact coefficients are:

| Function | Monomial | Coefficient |
|---|---|---|
| f | x | -66860312530151/36223662165912 |
| f | z | -3471947120321/400767559920 |
| f | x^3 | -9373706268721/36223662165912 |
| f | x^2*z | 449372611801/400767559920 |
| f | x*z^2 | 2602716940415/2786435551224 |
| f | z^3 | 1330009/1026480 |
| p | 1 | 2367718682557/2404605359520 |
| p | x^2 | 162784368743/2404605359520 |
| p | x*z | 2637067469/3963635208 |
| p | z^2 | 1330009/2052960 |
| r | 1 | 35172489484147/72447324331824 |
| r | x^2 | 9373706268721/72447324331824 |
| r | x*z | -8466667619/17175752568 |
| r | z^2 | 541957/2733264 |

This finite expression has common denominator T², homogeneous degree-three coefficients, and is smooth away from A=0. Set alpha(0)=0; it extends C² there. Omega=d alpha extends C¹, and is a legitimate angular correction. No C³ primitive/C² form at zero is claimed.

PRIMITIVE_CERTIFICATE.json also gives an exactly gauge-equivalent P5(A)/T primitive as100 sparse rational monomials. The displayed Euler-gauge form differs by −(1/4)d(i_A alpha_raw). receive_literal.py independently checks all four polynomial identities after denominators are cleared. Hence their exterior derivatives, and the completed density, are identical.

The defining literal sparse coefficients and determinant data are in PRIMITIVE_CERTIFICATE.json; PROOF.md gives the complete positivity/heat argument.
