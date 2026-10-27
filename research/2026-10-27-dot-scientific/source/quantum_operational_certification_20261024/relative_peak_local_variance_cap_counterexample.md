# Actual peak-3/2 source refuting the proposed local variance caps

27 October 2026. Exact rational physical counterexample to a stronger local-moment route, NOT an entropy counterexample or an actual-anchor sign counterexample.

Use physical Q=C3 and reference R=C3⊗C2. Let PΦ be the maximally entangled projector on Q⊗C3 and set

A=PΦ⊗U+(I9−PΦ)⊗V,
U=diag(1,1/1000),
V=[[999,31],[31,10]]/1000.

Both U and V are faithful effects and their only eigenvalue equal to one is the first eigenvalue of U. Thus A is a faithful effect with unique top vector ψ=Φ⊗e1. The actual conditional expectation is EA=I9⊗B with B=(U+8V)/9. The source has relative peak at most3/2: on the PΦ sector A≤1.5EA is equivalent to 5U≤8V, while on the complement it is automatic from U+2V≥0. The exact principal minors of 8V−5U are positive.

Set Q=I−A, a=⟨ψ,EQψ⟩, b=⟨ψ,(EQ)^2ψ⟩. Then Qψ=0 and

a=1/1125,
b=a²+(31/1125)²=962/1265625,
b/a=962/1125≈0.8551111111.

Consequently

b>(5/6)a,
b>(3a+a²)/4.

This simultaneously disproves the universal index6 local-cap inference at relative peak3/2 and the proposed physical variance strengthening Varψ(EQ)≤(3/4)a(1−a). The latter is not rescued merely by restricting E to the actual physical-qutrit expectation: the construction above has exactly that E, and its reference dimension is six.

The candidate index6 auxiliary operator V6=(6EA−A)/5 is positive because A≤1.5EA. But its local gap is

⟨V6−V6²⟩=(6/5)[a−(6/5)b]<0,

so the received local-variance maximum principle cannot be invoked. This does not show that the actual top gradient is negative. The two-matrix actual anchor here is ⟨e1,log B−2log C e1⟩, C=(U+2V)/3, and a floating diagnostic is positive (about0.001); no sign theorem is extracted from that diagnostic. The whole operator-valued isotropic class already has a separate VALUE receiver.

No counterexample for a three-dimensional reference is asserted. The obstruction shows that a dimension-free peak3/2 proof cannot simply assert this local variance cap, and that any remaining proof must exploit a different mechanism or a narrower reference scope.

## Repaired near-unit-relative-peak family: both sectors retained

The obstruction can be made to satisfy A≤kEA for ANY prescribed k>1, however close to one. An initial trial fixing U22=t² checked only U≤kB and omitted V≤kB when k<9/8. That trial does not establish the assertion. The construction below explicitly pays both sectors.

It suffices to handle 1<k<9/8, since a smaller admissible k implies any larger peak bound. Define

c=(9/k−1)/8, d=k/(9−8k), so 0<c<1<d,
p=99/100,
h=2p²/[(1−c)(d−1)],
K=ch+2p²/(1−c),
U=diag(1,h t²),
V=[[1−t²,p t],[p t,Kt²]].

Choose any positive rational t sufficiently small that

t²<min{1/h,(1−p²)/K,(1−c)/2}.

The source is again faithful with unique top vector Φ⊗e1. Indeed I−V has first principal minor t² and determinant t²(1−p²−Kt²)>0, while U is a faithful effect. Also V−cU has first principal minor1−c−t²>0 and determinant

p²t²[1−2t²/(1−c)]>0.

Furthermore dh−K=2p²/(d−1), so dU−V has first principal minor d−1+t²>0 and determinant

p²t²[1+2t²/(d−1)]>0.

Thus cU≤V≤dU. These are EXACTLY the two relative-peak conditions for the physical isotropic source:

U≤k(U+8V)/9 iff V≥cU,
V≤k(U+8V)/9 iff V≤dU.

The same top moments are

a=8t²/9,
b/a=(8/9)(p²+t²)>(8/9)p²=1089/1250>5/6.

Hence no relative upper peak k>1 alone implies the index6 local variance cap in arbitrary reference dimension. The family remains inside the separately VALUE-paid operator-valued isotropic class. The increasingly large h,K as k approaches1 reflect the allowed extreme reference conditioning; this is not an entropy counterexample near the product marginal.

More generally, allowing p arbitrarily close to1 makes b/a approach8/9. Therefore the analogous local-variance cap b/a≤(n−1)/n fails, under arbitrarily narrow upper-relative-peak bounds, for every fixed n<9. This rules out that particular source-to-local-cap transfer, not the abstract calibrated principles or the relative-BKM VALUE theorem.
