# Two misaligned rank-five planes: complete analytic entropy exclusion

## Declared geometries and result
Let ψ=Σ_i sqrt(p_i)|ii> and η=|10>. For each of
p=(1/3,1/3,1/3) and p=(3/5,3/10,1/10), every state supported on
K=span{ψ,η} obeys
F(ρ)=S(ρ)−2S((W3⊗id)ρ)+S(ρ_R)<=−log3.
These are genuinely misaligned product directions, not the previously
closed maximally correlated planes. The result concerns these TWO
Schmidt spectra, not every full-Schmidt-plus-product plane.

In the orthonormal logical basis(ψ,η), write
Y=[[a,c],[conj(c),b]], a+b=1, a,b>=0, |c|²<=ab.
Diagonal local unitaries U_A⊗barU_R preserve ψ and give η an arbitrary
phase, so the entropy objective depends only on |c|. Set c>=0.
We prove that F is nondecreasing in c at fixed a,b. Its maximum is
therefore at c=sqrt(ab), a pure physical input, for which the already
proved scalar qutrit entropy inequality gives F<=−log3.
Faithful logical states suffice for differentiation; boundaries follow
by finite-dimensional entropy continuity.

## Exact output blocks
Put u=p0+p1 and w=p1+p2. In orthonormal fixed support coordinates,
W3(ρ) is the direct sum of B2/2 and B3/2, where
B2=[[a u,c sqrt(u)],[c sqrt(u),b]],
B3=[[a p2,−a sqrt(p0 p2),0],
    [−a sqrt(p0 p2),a p0+b,−c sqrt(w)],
    [0,−c sqrt(w),a w]].
The reference state is
τ=[[a p0+b,c sqrt(p1),0],
   [c sqrt(p1),a p1,0],
   [0,0,a p2]].
These follow directly from the three skew Kraus operators. For example
v01=sqrt(p1)|01>−sqrt(p0)|10>, v02=sqrt(p2)|02>−sqrt(p0)|20>,
v12=sqrt(p2)|12>−sqrt(p1)|21>. The first block uses(v01/sqrt(u),|00>);
the second uses(|02>,|20>,v12/sqrt(w)).
The reference trace has the coherence c sqrt(p1), not c sqrt(p0).
This normalization is load-bearing.

## Rational-resolvent derivative
Put v=ab−c²>=0 and integrate over t>=0. Define the positive denominators
DY=t²+(a+b)t+v,
D2=t²+(a u+b)t+u v,
DR=t²+(a u+b)t+p1 v+a²p0p1,
D3=(a p2+t)[w v+t(a+b+t)]+a²p0p1 t.
The final determinant is det(B3+tI). Logarithm's resolvent identity,
with the trace-zero coherence derivatives, gives exactly

F'(c)/(2c)=integral_0^infinity
 [-1/DY+u/D2+w(a p2+t)/D3−p1/DR] dt.

The factors1/2 in the physical output are accounted for: differentiating
S(Bj/2) gives half the unnormalized entropy derivative, since the block
trace is c-independent; the objective coefficient−2 cancels that half.

Let N be the common numerator over DY D2 DR D3:
N=−D2 DR D3+u DY DR D3+w(a p2+t)DY D2 DR−p1 DY D2 D3.
The accompanying exact symbolic certificate proves N>=0 in each case:

- Uniform p: 243 N is a polynomial with28 nonnegative monomials.
- Biased p: (25000/3)N has only one negative monomial,
  −100 a²b²t³. Absorb it using the exact identity
  25a³b²t²+100ab²t⁴−100a²b²t³ =25ab²t²(a−2t)².
  After subtracting this square, every remaining coefficient is nonnegative.

The full explicit polynomials are stored in
rank_five_two_plane_entropy_certificate.json. The adjacent Python script
checks the cleared-denominator identity, square decomposition, and every
remaining coefficient exactly in SymPy. Thus F'(c)>=0 for the entire
logical state disk, rather than just the bounded numerical box.
For a,b>0 the numerator is strictly positive for t>0 in the mixed interior,
so coherence increases the objective strictly away from c=0.

## Receiving diagnostics and conditioning record
Before this proof, a deterministic21×21 grid and9 bounded local starts
were executed for each declared geometry. The initial overly loose box
approached output-support eigenvalues around10^−13 and is retained as a
conditioning-stop record, not an optimum certificate. The final bounded
box a∈[10^−4,1−10^−4], c/sqrt(ab)∈[0,.9999] stayed above minimum
output-support eigenvalues4.999e−9 and1.428e−9. Its best gaps below the
target were5.0170e−5 and.1007767853 respectively, both facing the pure
boundary. Those diagnostics are not used in the analytic proof.

At the logical maximally mixed point the Hessian is positive in the three
Pauli directions for both geometries, but global logical convexity was
not assumed or proved. Coherence monotonicity is the smaller sufficient
statement established here. Historical priority of this specific entropy
comparison has not been established; the resolvent and polynomial methods
are ordinary analytic tools.
