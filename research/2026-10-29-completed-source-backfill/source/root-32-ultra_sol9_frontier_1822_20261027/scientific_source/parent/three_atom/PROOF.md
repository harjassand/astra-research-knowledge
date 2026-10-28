# Exact conversion of a genuine support failure

Input: finite C1 F on real 2x2 matrices, base A, increments X,Y with
d=detX>0, detY=-e<0, and B(X)+(d/e)B(Y)=-eta<0, where
B(X)=F(A+X)-F(A)-DF(A):X. A failed polynomial/SOS selector is insufficient.
The earlier resolved PC quartics are not negative targets.

For small positive p put h=det(X-Y) and

    w1=p, w2=p*d/(e+p*h), w3=1-w1-w2,
    Z=-(w1*X+w2*Y)/w3.

The atoms A+X,A+Y,A+Z with those weights have exact mean A. Multiplying
their determinant defect by w3 leaves

    w1*detX+w2*detY-w1*w2*det(X-Y)=0.

Thus mean determinant is also detA. The Jensen defect is
J=p*B(X)+w2*B(Y)+w3*B(Z). As p tends to zero, w2/p tends to d/e and
Z=O(p). Differentiability gives B(Z)=o(p), hence J/p tends to -eta.

For polynomial inputs, let H bound the Hessian operator norm on the unit
ball around A, W=|X|1+(2d/e)|Y|1,
L=2d*abs(h)*abs(B(Y))/e^2, D=L+2H*W^2. Choose a positive dyadic p at most

    1/2, e/(2abs(h)), 1/(2(1+2d/e)), 1/(2W), eta/(2D),

omitting zero denominators. Then w3>=1/2, |Z|<=1 and J<=-eta*p/2<0.
For F=sum c_alpha A^alpha, a rational valid H is
sum |c_alpha|*n*(n-1)*R^(n-2), n=|alpha|>=2, R=max(1,|A|1+1).
The dyadic exponent is bounded by one plus log2 of the reciprocal smallest
bound. Finding the failed pair remains a separate acquisition cost.

The compiler checks the matrix/minor averages and full energies directly
with Fraction arithmetic. It records all exact atoms, weights, bounds,
defects and maximum output integer bit lengths in EXACT_WITNESSES.json.

## Three-point completeness, at its actual scope

If detX=0 and B(X)<0, the two atoms A+X and A-pX/(1-p) already suffice.
Otherwise scalar minor support at A is intersection of the upper bounds
B(X)/detX for positive determinants and lower bounds for negative ones.
One fixed increment of each sign bounds a feasible intersection inside a
compact interval. If the intersection is empty, two finite endpoints are
strictly reversed, supplying the construction above.

Conversely scalar supports at every A give minor-affine lower supports
whose supremum equals F on the graph. It is finite on all R5: any (B,s)
is the average of graph points B+Y and B-Y with detY=s-detB. Every support
is bounded by their finite F average. Thus a finite convex lift exists.
Hence a finite C1 energy on R^(2x2) is PC iff it obeys minors-Jensen for
all measures on at most THREE atoms. For a rational polynomial, strict
failures persist under rational approximation, so a rational witness exists.

These measures are arbitrary minor-preserving mixtures. They are not
automatically laminates, compatible gradients or gradient Young measures.
No non-QC conclusion follows. The established differentiable support test,
finite-mixture formula and ordinary convex separation are the foundations.
Aubert1988 Theorem1.3 and the remarks after Corollary1.4 ALREADY give the
support-interval and three-matrix characterization. Those are prior results.

## Executed target and controls

For the new even-Hopf F=(u+v)^2+(252/25)q^2+(99/25)q(u-v), use
A=diag(36,35), Rp=[[0,55],[-4,0]], Rm=diag(1,-2). Scale Rm by
-DF(Rm):A/(2F(Rm)). Rp has zero minimizing scale, so use 1/1024 instead.
This retains a true negative pair with eta approximately .0011069187374.
The compiler returns p=2^-26 and exact rational Jensen defect approximately
-1.6494374782e-11 (maximum output integer bit length324). The author's
separate larger-defect witness is preserved in the hopf branch.

Ordinary controls: the familiar DM energy |A|^4-(9/4)|A|^2 detA at A=0,
X=5I,Y=diag(1,-1) has pair margin100 and compiles a defect about-.00038154.
The coercive degree-six perturbation +|A|^6/1000000 also passes. The
ordinary positive energy |A|^4 correctly rejects the same proposed pair.
These are implementation controls, not new examples.

Primary sources read this episode: Fantuzzi et al. arXiv:2604.11124v1,
sections2.2/3.1; Dacorogna--Marcellini original PDF
https://www.mat.univie.ac.at/~stefanelli/cv/paper5.pdf .

The later source check acquired Aubert's primary text, M2AN22(1),1988,
printed pp.8-11, retained at hopf/sources/Aubert1988.txt. Root read the
governing passage including the explicit three-matrix statement. Public
primary route: https://www.numdam.org/item/M2AN_1988__22_1_5_0/ .

The family.py continuation converts the separate all-m>=197 exact family
cuts into finite rational witnesses at A=I. For any rational m>=197, the
positive cut has zero linear term; choose a nonzero dyadic t+ at most
min(1,det(R+)*(lower-upper)/(2F(R+))). Its extra quartic term consumes
at most half the strict cut gap. Use the negative cut's exact minimizing
scale, then apply the compiler. This is a finite algorithm for every such
rational input, given the proved all-parameter gap. Actual exact records
for m=197,198,256,1000,1000000 use at most1072-bit output integers.
Their small negative gaps are exact rational signs, not floating
subtraction. No deformation or QC implication is inferred.
