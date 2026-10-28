# Bell-twirling cannot be a monotone bridge to unrestricted entropy

This instantiates the known N983 coherence/half-metric obstruction for
the newly paid Bell-diagonal region. It is not a negative entropy deficit
or a historical-priority claim.

Let Omega=|00>+|11>+|22>, v=|00>-|11>, H=i(Omega v*-v Omega*),
X0=aI9+P_Omega and X=X0+tH, with a=t=1/100. Both partial traces of H
vanish. Every Weyl-Bell diagonal of H is zero; the Bell-twirl of X is
EXACTLY X0. Both sources are faithful, share both uniform marginals and
have common trace309/100.

The changed input eigenvalues are a+3/2±sqrt(9+24t²)/2, with seven
others a. NX has three eigenvalues a and three pairs
a+1/2±sqrt(1+4c²t²)/2, c=1,1/2,1/2. certify.py independently checks
these characteristic polynomials and all nine Bell-projector diagonals.
Rational square-root brackets and atanh-log intervals give

    -0.00024220590656006 < Delta(X)-Delta(X0)
                         < -0.00024220590653898.

Exact rational endpoints and normalized differences are in RESULT.json.
Delta(X) itself is certified POSITIVE. Thus Bell-twirling can INCREASE
the objective; positivity after twirling does not pay coherence loss.

The local mechanism is exact too:
d²Delta(X0+tH)/dt² at0=4log301-6log101<0, since301²<101³.
Faithfulness follows from t²<a(a+3)/6 and is also checked by the exact
eigenvalue brackets. The finite test used actual qutrit-reference matrices,
retained both marginals/whole trace, and took about.379s including SymPy
and interval work, excluding interpreter startup.

Only the Bell-twirl shortcut is blocked. No unrestricted W3 violation,
impossibility of another coherent transfer, physical channel acquisition
or practical method advantage follows.
