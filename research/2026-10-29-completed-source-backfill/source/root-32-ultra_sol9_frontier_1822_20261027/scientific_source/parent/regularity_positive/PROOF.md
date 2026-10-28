# Constructing a local C1,1 representative from the accepted rational support

This is the positive counterpart to the peer's no-C2 representative theorem.
It is a direct application of an established convex Whitney extension
formula, with the necessary quantitative jet compatibility proved here.
It does not assert a new general extension theorem or cheap evaluation.

Let F be the previously ACCEPTED rational-selector quartic, p its degree-six
numerator, k(A)=p(A)/|A|^4 for A nonzero and k(0)=0. Its accepted inequality is

    B_F(A,X)-k(A)detX >= delta*(|A|^2|X|^2+|X|^4),
    delta=1/2400000.

Write C=sum of absolute ordinary degree-four coefficients of F, and
P=sum of absolute ordinary degree-six coefficients of p. In Frobenius norms,

    |k(A)|<=P|A|^2, |Dk(A)|<=10P|A|,
    |D^2F(A)|op<=12C|A|^2.

The bound on Dk follows by differentiating p/|A|^4: the numerator derivative
contributes6P|A|, and the denominator derivative4P|A|. The degree-two
homogeneity and these bounds prove k is C1 at zero with Dk(0)=0.

For fixed finite R>0 let E_R={(A,detA):|A|<=R}, and prescribe the 1-jet

    f(A,detA)=F(A),
    G(A,detA)=(DF(A)-k(A)cofA, k(A)).

Put U=12C+11P, V=10P, M_R=(U^2 R^2+V^2)/delta. For A,B in the ball,
d=|B-A|, r=max(|A|,|B|), segment differentiation gives

    |G(B,detB)-G(A,detA)|^2
        <=(U^2 R^2+V^2)*r^2*d^2.

Here the first four components have derivative norm at most U*r^2 and
the last has derivative norm at most V*r along the segment. Also
r^2<=2(|A|^2+d^2). The accepted strict support bound therefore gives

    f(mB)-f(mA)-G(mA):(mB-mA)
        >= |G(mB)-G(mA)|^2/(2M_R).

This is precisely the standard (CW1,1) condition. Theorem2.4 of
Azagra--Le Gruyer--Mudarra, arXiv:1706.02235v4, supplies the explicit formula

    h_R(z)=inf_{|A|<=R} [F(A)+G(mA):(z-mA)+(M_R/2)|z-mA|^2],
    g_R=conv(h_R),  mA=(A,detA).

It is a finite globally convex C1,1 function on R5, Lip(gradient)<=M_R,
and g_R(A,detA)=F(A) with the stated gradient for EVERY |A|<=R.
The graph matching is local in A; outside that ball it is not claimed to
represent F. Different R give different extensions, without a compatibility
claim. Near zero this constructs exactly the regularity allowed by the
peer's no-C2 obstruction. A polynomial energy can thus have an exact
convex local representative with Lipschitz gradient while having no exact
C2 representative on any neighborhood of its collapsed zero state.

## Acquisition, comparator and limits

The construction uses the already acquired exact rational selector and
strict certificate, not a physical material or a numerical fit. The new
algebra here verifies the full continuum jet condition and its finite
constant; it is not an extension based on finitely sampled strains.
The script independently expands F and p, records rational C,P,U,V,M_1,
and binds the accepted input proof/certificate by their actual hashes.

Evaluation still requires the four-dimensional nonlinear infimum in h_R
and a five-dimensional convex envelope. The primary formula reduces the
latter to at most six points in R5, but this is not a practical-runtime
claim. No continuum evaluation or finite network representation was
acquired. Convex Whitney extension is the equally informed ordinary
comparator and receives full credit. Also, no-C2 obstructions already occur
for simpler classical ADM-type energies; this is not exclusive to the new
all-polynomial-selector separator or a claim of world priority.

Primary source read: https://arxiv.org/html/1706.02235v4 , Theorem2.4,
its CW1,1 premise, and proof (L199-255 in retrieved HTML). Supporting
earlier theorem: Azagra--Mudarra arXiv:1603.00241v3, Theorem1.3.
