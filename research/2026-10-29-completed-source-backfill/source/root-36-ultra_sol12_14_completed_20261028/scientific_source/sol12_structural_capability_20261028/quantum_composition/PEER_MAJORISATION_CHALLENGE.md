# Independent reconstruction of the all-nine SIC receiver

Construction attribution: `producer-workspace/selector_beyond_representations`, who
sent the majorization mechanism on 28 October 2026. This independent
challenge reconstructed the finite eigenvalue comparisons below; it did
not invent the peer's construction. Governing peer proof path is to be
added when the peer freezes it. The earlier exact Bell-to-SIC reduction
and five-support quantitative entropy receiver are my separate work.

Let S_i be the nine rank-one qutrit SIC projectors. For a subset J of
size m, C_J=sum_(i in J)S_i has trace m and squared trace
`Tr C_J^2=m(m+3)/4`. Also `sum_i S_i=3I`.
Let K have ordered eigenvalues k1>=k2>=k3. Scalar shifts cancel in
majorization, so set k2=0, x=k1-k2>=0, y=k2-k3>=0.
Write v_i=2Tr(S_i K), and let b be the nine ordered pair sums k_j+k_l.
Its first four partial sums are `2x,3x,4x,4x+max(0,x-y)`.

For m=1, C has largest eigenvalue one. For m=2, the overlap magnitude
1/2 gives spectrum(3/2,1/2,0). For m=3, if L is its largest eigenvalue,
`L^2+(3-L)^2/2<=9/2` implies L<=2. Thus the top m v partial sums
are at most 2x,3x,4x for m=1,2,3, by the Hermitian trace inequality
`Tr KC <= x lambda_max(C)-y lambda_min(C)` and C>=0.

For m=4, trace4 and squared trace7 give L<5/2: otherwise
`Tr C^2>=L^2+(4-L)^2/2>=59/8>7`. Also the eigenvalue spread obeys
`(L-l)^2<=2Tr(C-4I/3)^2=10/3<4`, so L-l<2.
If x<=y, `2(xL-yl)<=2x(L-l)<=4x`.
If x>=y, divide by x when nonzero and put t=y/x in[0,1]. The desired
bound is `2L-2tl<=5-t`, whose difference is affine in t, nonnegative
at t0 by L<=5/2 and at t1 by L-l<=2. Hence the fourth partial sum
also has the right direction. No assumed common eigenbasis is used.

Apply the same m1--4 statements to -K and use total sums
`sum v_i=6TrK=sum b_i`. This pays partial sums m5--8 by complement.
Therefore `v` is majorized by `b`. Convexity of exp gives exactly
`sum_i exp(2Tr S_iK)<=(Tr exp K)^2`.
The Gibbs transformation in `FULL_SIC_TARGET.md` consequently gives
`2S(sum p_i S_i)>=H(p)` for every nine-weight probability vector.
The symbolic nine-vector argument passes at this complete scope.

This proof uses established trace/majorization/Gibbs tools. No historical
priority claim follows. It is an all-Bell theorem, not an unrestricted
qutrit/reference theorem or an automatic comparison for arbitrary
noncommuting operator-valued Bell coefficients.

## Additional closure and equality consequences checked here

For any Bell rho_p and a>=0, normalize rho_p+aI by1+9a. Its Bell
probabilities are `(p_i+a)/(1+9a)`, so the all-nine result receives
its ENTIRE white curve. The inherited positive common-bath identity
therefore receives `rho_p tensor U+I9 tensor V` for all finite PSD U,V,
including noncommuting/singular baths. This is an immediate use of the
peer's new premise, not a new bath identity. Weyl-channel composition
convolves probabilities on Z3^2, so the full Bell probability simplex
also stays within the newly received class under arbitrary finite
sequential Weyl-channel composition. This does not prove composition
for arbitrary quantum channels.

The all-nine equality classification can be completed using the separate
five-support theorem. Every four-element C is positive definite:
if its minimum eigenvalue were zero, its squared trace would be at least
4^2/2=8, contradicting7. Thus the fourth majorization inequality is
strict for nonconstant K (also when x0,y>0). Strict exp convexity gives
strict dual inequality. For faithful M, choose K=logM: F(p)>0 unless
M=I/3. The purity identity then forces p uniform. If M is singular,
its support contains at most three SIC labels; the five-support receiver
is strictly positive unless p is a point mass. Therefore Delta is zero
exactly at the uniform vector and the nine pure Bell vertices.
