# All Schmidt spectra with one off-diagonal product direction

## Exact theorem
For any normalized qutrit Schmidt vector
ψ=Σ_i sqrt(p_i)|ii>, p_i>=0, Σp_i=1,
and any off-diagonal Schmidt-basis product η=|j k>, j≠k,
every state ρ supported on span{ψ,η} satisfies
S(ρ)−2S((W3⊗id)ρ)+S(ρ_R)<=−log3.
This closes an entire rank-five support mechanism, not only the two
original numerical fixtures. It does not cover arbitrary superposed
product vectors u⊗w or every rank-five kernel space.

By simultaneous physical/reference relabeling take η=|10>. A diagonal
local unitary on A and its conjugate on R preserves ψ and rotates η's
phase arbitrarily. Thus the objective depends only on the modulus of
logical coherence. It suffices to prove monotonic increase in nonnegative
coherence at fixed diagonal weights, then pass to the pure-state boundary.
The latter obeys the scalar qutrit entropy bound proved in
rank_four_boundary_geometry_audit.md.

## Homogeneous coordinates prevent artificial coefficient signs
Let x,y,z>=0, S=x+y+z>0, and use the unnormalized vector
ψ0=sqrt(x)|00>+sqrt(y)|11>+sqrt(z)|22>.
Write
ρ=a|ψ0><ψ0|+b|10><10|+c(|ψ0><10|+|10><ψ0|),
where a,b>=0, c>=0, c²<=ab, and aS+b=1. In the normalized
orthogonal logical basis the density matrix is
[[aS,c sqrt(S)],[c sqrt(S),b]].
Set v=ab−c². Ultimately one can simply put S=1 and x,y,z=p_i.
Homogenizing avoids eliminating z=1−x−y, which would obscure positivity.

Put A=x+y and B=y+z. The exact2×2 and3×3 output blocks and reference
matrix are those in rank_five_two_plane_entropy_proof.md, with p0,p1,p2
replaced by x,y,z. Their trace is aS+b, independent of c.
The logarithm resolvent derivative gives

F'(c)/(2c)=integral_0^infinity
 [-S/DY+A/D2+B(az+t)/D3−y/DR] dt,

where
DY=t²+(aS+b)t+S v,
D2=t²+(aA+b)t+A v,
DR=t²+(aA+b)t+y v+a²xy,
D3=(az+t)[B v+t(aS+b+t)]+a²xy t.
All denominators are positive for t>0 in the interior, and D3 is
exactly the determinant of the unscaled3×3 output block plus tI.
The factor S in the input term is essential in these homogeneous variables.

## Uniform exact positivity certificate
The common numerator over DY D2 DR D3 is
N=−S D2 DR D3+A DY DR D3+B(az+t)DY D2 DR−y DY D2 D3.
It has the exact decomposition

N = xz·ab²t²(ay−t)² + P(a,b,v,t,x,y,z),

where EVERY coefficient of P is nonnegative. The adjacent exact symbolic
certificate expands P in seven independent nonnegative variables and
verifies every coefficient, along with the cleared-denominator identity.
A compact grouped coefficient list is saved in its JSON.

The mechanism is especially transparent before completing the square:
after factoring xz, the expanded polynomial has exactly one negative
monomial, −a²b²t³y. Its positive terms include a³b²t²y² and ab²t⁴.
Subtracting ab²t²(ay−t)² leaves +a²b²t³y, and every other monomial
was already nonnegative. Thus no inequality between the Schmidt weights
is required.

Consequently F'(c)>=0 for c>=0 throughout the logical state disk.
For x,z>0 and a>0, the polynomial is strictly positive for t>0, so
nonzero coherence strictly increases F in the mixed interior.
At c=sqrt(ab), ρ is pure. The pure-state qutrit entropy bound yields
F<=−log3. Zero eigenvalues, zero Schmidt weights, and c=0 follow by
continuity. No nonunitary filtering or unproved entropy invariance occurs.

## Scope and provenance
This enlarges the two previously certified geometries to all Schmidt
weights with a single off-diagonal Schmidt-basis product direction.
General full-Schmidt-plus-arbitrary-product planes remain open.
The underlying tools are standard resolvent differentiation, entropy
continuity, and exact polynomial positivity; historical priority of
this specific receiving theorem has not been established.
