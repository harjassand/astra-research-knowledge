# Prediction certificates after binary normalization

The earlier control-cube certificate needlessly imposed h>=0. Its inverse argument only requires h>-1/U. Thus if sym(Lambda^(1/2) H Lambda^(-1/2)) >= h I with 1/U+h>0, then

    sup_{0<=D<=UI} ||D(I+HD)^(-1)||_Lambda <= 1/(1/U+h).

For positive D this follows from D^(-1)>=I/U. For zero coordinates restrict to the active principal block. The resolvent difference identity and interval prediction bound are unchanged, provided both center and all enclosed models retain positive shifted margin. In particular, a binary normalized map g(S)=a_S^T(I+B_SS)^(-1)1 needs diagonal stability of I+B, not of B. B has zero diagonal, so requiring a positive accretivity margin for B would be unnecessarily restrictive.

Let e0>=|f0-fhat0|, ea>=||a-ahat||_(Lambda^-1), and let sym_Lambda(I+Bhat)>=kappa_hat I and ||B-Bhat||_Lambda<=eB<kappa_hat. Then kappa=kappa_hat-eB>0, and for every subset S, with T_B(S) equal to (I+B_SS)^(-1) on S and zero elsewhere,

    |f(S)-fhat(S)| <= e0 + ea ||1||_Lambda/kappa
                       + ||ahat||_{Lambda^-1} eB ||1||_Lambda/(kappa*kappa_hat).

This certifies an acquired or fitted enclosure; it supplies no method for obtaining that enclosure from binary readings. It does not make optimization over all subsets efficient.

## Existence under the original real passive model

Let H0=P^T A^(-1)P with sym(A)>0. At fixed t>0 put L=diag(t^(-1)+H0_ii)>0. Before gauge normalization,

    I+B0=(t^(-1)I+H0)L^(-1).

With Lambda0=L^(-1), its weighted similarity is

    Lambda0^(1/2)(I+B0)Lambda0^(-1/2)
      = L^(-1/2)(t^(-1)I+H0)L^(-1/2),

whose symmetric part is positive definite. Gauge by a nonsingular real diagonal W transforms B=W^(-1)B0 W; Lambda=W^2 L^(-1)>0 gives the same positivity up to sign-diagonal orthogonal similarity. Thus the shifted certificate is compatible with this physical model, but its witness and margin remain unknown and must be verified from acquired enclosures. The binary normalized diagonal scaling is real positive here; no complex-actuator extension is implied.

This is a direct strengthening of an existing resolvent estimate, not a foundational breakthrough or measured capability.
