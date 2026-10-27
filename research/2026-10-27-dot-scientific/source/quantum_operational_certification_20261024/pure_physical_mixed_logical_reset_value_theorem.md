# Pure physical reset with arbitrary noncommuting logical mixed reset

Construction26 October2026; independently received PASS in pure_physical_mixed_logical_reset_independent_audit.md. This is an exact analytic theorem, not a numerical extension from pure reset flags.

## Whole source class

Let sigma and eta be arbitrary density matrices on a finite logical space L, not necessarily commuting. Let u be any unit qutrit vector. The actual TP channel

 E(rho)=p rho⊗sigma+q Tr(rho)|u><u|⊗eta, p+q=1,

has nonnegative WH3 deficit. Equality holds exactly when p q=0 or sigma eta=0. In particular, the reset may have arbitrary logical rank, including a rank-two mixed reset with genuinely noncommuting sigma and eta.

A known output isometric encoding may be inserted without changing the claim. This theorem does not receive a general physically mixed reset with coherent logical correlations, nor arbitrary entangled physical/logical reset states.

## 1. Exact coherence-loss identity

For positive X,Y on one logical space and0<=c<=1, define

 G_c(X,Y)=[[X,sqrt(c)sqrt(X)sqrt(Y)],
           [sqrt(c)sqrt(Y)sqrt(X),Y]],
 L_c(X,Y)=Tr f(G_c)-Tr f(X)-Tr f(Y), f(t)=t logt.

This is the entropy loss when two weighted projection sectors have squared overlap c. It is nonnegative. For c=1, the nonzero Gram spectrum is that of X+Y, so L_1=f(X+Y)-f(X)-f(Y).

By matched covariance take u=|0>. Put S=p sigma/3 and Q=q eta/3. Comparing to success and reset sectors in orthogonal reference flags (whose deficit is zero), the ACTUAL input, reference, and normalized output coherence losses give exactly

 Delta=L_(1/3)(3S,Q)+L_1(S,3Q)-4L_(1/2)(S,Q).            (1)

Here the input has one nonorthogonal logical sector with success weight3S, reset weightQ and squared overlap1/3. Its two other reset sectors are orthogonal. The reference has one overlapping qutrit coordinate with weights S,3Q and overlap1. The WH output has TWO overlapping antisymmetric/reset sectors, each with weights S,Q and squared overlap1/2; its remaining success and reset sectors are orthogonal. The factor4 is two sectors times the deficit's coefficient2. No logical eigenspaces are measured or exposed.

For an independent operator-block reconstruction, the nontrivial source block is

 T=[[S+Q,sqrt2 S],[sqrt2 S,2S]],

and the repeated unscaled output block is

 L=[[S+2Q,S],[S,S]],

with marginal block S+3Q. Their scalar spectators and trace-log constants yield(1). Physical reconstruction tests on60 complex noncommuting cases agree within3.52e-15, but the stated sector overlaps are the exact proof of the identity.

## 2. Positive log-power expansion with noncommutativity retained

At s>0 define P_X(s)=X(X+sI)^(-1). The determinant lemma for G_c gives

 L_c(X,Y)=integral_0^infinity sum_(n>=1)
          [c^n/n] Tr[(P_X(s)P_Y(s))^n]ds.               (2)

The product need not be Hermitian, but its nonzero spectrum equals that of the positive sandwich P_X^(1/2)P_Y P_X^(1/2). Thus every term in(2) is nonnegative. The determinant identity is first proved at positive s; singular endpoints follow by finite entropy continuity. Tonelli and finiteness of each L_c justify the positive series and the later finite linear combination, including c=1.

For n>=2, the integrand contribution to(1) is

 (1/3^n)Tr[(P_(3S)P_Q)^n]
 +Tr[(P_S P_(3Q))^n]
 -(4/2^n)Tr[(P_S P_Q)^n].                              (3)

Since P_(3Q)>=P_Q, positive sandwich order and eigenvalue monotonicity imply

 Tr[(P_S P_(3Q))^n]>=Tr[(P_S P_Q)^n].

Because4/2^n<=1 for n>=2, every term in(3) is nonnegative. This is a valid noncommuting trace-power comparison, not a false Loewner ordering of arbitrary matrix powers.

## 3. The signed linear term is paid after integration

For scalar a,b>0 let

 ell(a,b)=(log a-log b)/(a-b), ell(a,a)=1/a,
 J(a,b)=ab ell(a,b)=integral_0^infinity
                       [a/(a+s)][b/(b+s)]ds.

Diagonalize S and Q separately, with eigenvalues a_i,b_j and overlaps w_ij=|<i|j>|^2. The n=1 part of(1) integrates exactly to

 sum_(i,j) w_ij K(a_i,b_j),
 K(a,b)=(1/3)J(3a,b)+J(a,3b)-2J(a,b)
       =ab[ell(3a,b)+3ell(a,3b)-2ell(a,b)].              (4)

These weights arise from Tr P_X P_Y; no simultaneous diagonalization is asserted.

Set z=log(a/b) and psi(z)=z/(exp z-1), extended at0 by1. Homogeneity of J gives the exact scalar identity

 K(a,b)=a[psi(z+log3)+psi(z-log3)-2psi(z)].               (5)

The function psi is strictly convex on the real line. For z>0,

 psi''(z)=exp(z)[(z-2)exp(z)+z+2]/(exp(z)-1)^3>0:

the bracket and its first derivative vanish at0 and its second derivative is z exp(z)>0. For negative z, psi(-z)=psi(z)+z implies the same second derivative. At0, psi''(0)=1/6. Therefore(5) is strictly positive whenever a,b>0. Zero eigenvalues are interpreted continuously and contribute zero.

Consequently the integrated linear term is nonnegative. Together with(3), this proves Delta>=0 for all finite S,Q, including noncommuting and singular ones.

## 4. Equality

If S Q=0, all the products in(2) vanish, so Delta=0. Conversely, if their supports are not orthogonal, some positive eigenvalues a_i,b_j have w_ij>0. The strictly positive scalar payment(5) then makes the whole deficit positive. Thus Delta=0 exactly when S Q=0, including S=0 or Q=0. In normalized channel coordinates this is precisely p q=0 or sigma eta=0.

## Lineage and limitations

The old white-noise/operator-bath lift has a common identity baseline and does not directly cover I3⊗P_u⊗eta. The coherent-star theorem has a single pure successful main, not arbitrary noncommuting logical S,Q. The present proof retains those matrices through positive trace powers and pays only its signed linear term by an actual spectral-overlap integral.

A targeted internal lineage check did not find a prior receiver of this entire class. This is not a historical-priority claim, and no general mixed-reset positivity is inferred by convexly mixing pure physical resets.

Reproduction: pure_physical_mixed_logical_reset_check.py checks the exact source/coherence identity on actual channels. The proof itself is analytic and requires no finite numerical certificate.
