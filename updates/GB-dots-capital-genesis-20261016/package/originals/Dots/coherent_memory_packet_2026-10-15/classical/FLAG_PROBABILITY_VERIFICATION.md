# Verification of primitive bad-flag inequality (B)

Pin: 3e8a972f2924272e1a89859d2f556b5b1f91d501.
Sources: original_theorem.md, Section 2; sweep_MONOTONE_ENVELOPE.md, Sections 4–7.
Scope: probability of the three literal local flags and parameter order. This does not independently verify the microscopic syndrome-envelope inclusion.

## Result

All three terms in (B) admit direct Poisson derivations with the stated constants. The slow prefactor 2 is conservative. Repeated clock labels do not invalidate the factorial denominator in the fast term. The parameter order gives a strictly positive size-independent existence threshold, with no useful numerical rate claim.

Fix integer s>=1, C>2(s+4)log8, R>=max(s+5,ceil(280eC)+10), b>=4, Delta=Cb/kappa, and m=floor(Rb/2). Work on a deterministic slab [a,a+Delta); translate its initial time to zero. All certificates are freshly reset at a; none uses actual prior infection or historical waiting times.

## 1. Slow lower-halfspace certificate

Let h(x)=sum_i x_i and declare vertices h<=-sb completed at time zero. For a target y in {0,...,b-1}^4, the relevant predecessor cone consists of x<=y coordinatewise with h(x)>-sb, together with its rank-zero boundary. It is finite. Define rank r(x)=h(x)+sb. Its maximum at y is

H_y=sb+h(y)<= (s+4)b-4 < H_*=(s+4)b.

For positive rank, let S_x=max_i T_(x-e_i) and T_x be the first ring of the rate-kappa clock at x strictly after S_x. Set W_x=T_x-S_x. Then T_x=S_x+W_x.

The W_x are jointly iid Exp(kappa), not merely individually exponential. Reveal complete clock processes in increasing rank. S_x is measurable using strictly lower-rank processes and never uses x's own clock; conditional on all those lower processes, the residual of x's independent homogeneous Poisson process after that specified S_x is Exp(kappa), with a law independent of the revealed data. The clocks at equal rank are independent. Induction over the finite cone yields joint independence of all the W_x. Revealing more than just completed times is harmless and makes this conditional argument explicit.

Unroll the max recursion: T_y is the maximum of sums of W_x along directed predecessor paths from y to rank zero. Every such path has H_y positive-rank vertices, with at most 4^H_y direction words. A fixed path never repeats a vertex because rank strictly decreases. For its sum S, the exponential moment at kappa/2 is E exp(kappa S/2)=2^H_y. Markov and a union bound give

P(T_y>t) <= 8^H_y exp(-kappa t/2)
          <= 8^H_* exp(-kappa t/2).

Dependence between different paths or different target certificates does not matter. Union over the b^4 targets and put t=Delta:

P(slow flag) <= b^4 exp(((s+4)log8-C/2)b)
             <= 2b^4 exp(((s+4)log8-C/2)b).

Thus the literal source slow term is valid with room to spare.

The convenient W construction can use clocks beyond the slab to analyze T_y. The event T_y<=Delta itself is determined entirely by slab increments: scan increasing ranks and declare a certificate failed if its required ring has not occurred by Delta. No future primitive enters the flag. These finite cones lie within the stated guard: a predecessor is at fine l1 distance at most H_* from the target, and R>=s+5 provides more than sufficient spatial padding.

## 2. Structural fast words, including repeated clocks

For a currently queried output w, a clock that can update it is either its own clock or one of six clocks at w-e_i-e_j. The own update reads at most five old inputs; each lower-corner update reads four old inputs. Hence there are at most 5+6*4=29 choices of (clock center, old input). The source's 35 is a valid overcount.

A structural backward word of length m fixes these choices successively, and hence fixes a list of clock labels c_1,...,c_m. Labels may repeat, including self-retention loops. For a fixed word, existence of a realizing strict-time sequence is bounded by the expected number of its realizations.

For independent rate-kappa Poisson processes, the joint factorial moment density of m distinct marked events is kappa^m, including when several labels coincide. Integrating over the ordered simplex 0<t_1<...<t_m<Delta gives

E(number of realizations of a fixed word)=(kappa Delta)^m/m!.

For repeated labels this is the factorial moment measure of the same Poisson process, not an erroneous independent-wait approximation. Distinctness of marks follows from the strict inequalities. Markov's inequality and a union bound over at most 35^m words and b^4 output sites yield exactly

P(fast flag) <= b^4 (35 kappa Delta)^m/m!.

An observation time anywhere in the slab creates no extra union factor: if a dependency tree at time t contains m clock events, its final event occurs at some time <=t<=Delta, so it is already among these ordered tuples. The tuple count allows every final event time in the slab. Initial-state leaves have no clock event; births are separately excluded by the birth flag.

Old-state simultaneous update semantics are essential. Recursive inputs at a mark refer to the configuration immediately before it; the same mark cannot be reused through another output at equal time. Across the finite guard, different Poisson marks tie with probability zero. Thus every genuine m-event dependency is a strict-time word counted above.

A backward input step changes fine l1 position by at most two, including the offset to its clock center. All first m centers lie within l1 distance at most 2m<=Rb of a target. Therefore the local primitive guard includes every such word; a word leaving it must have already supplied an m-event prefix. The flag can be defined and tested using local slab packets alone.

Using m! >= (m/e)^m, Rb>=4 and m>=Rb/4,

P(fast flag) <= b^4(35eCb/m)^m
             <= b^4(140eC/R)^m
             <= b^4 2^(-m).

No independence between words is asserted or needed.

## 3. Guarded births

The union of coarse cells of infinity radius R+2 has fine side length (2R+5)b. Any elementary face meeting this guard has a base at most one fine lattice unit outside it in each coordinate. There are six face orientations. Consequently the source's conservative count

F_guard <= 6((2R+5)b+3)^4

bounds all relevant face labels. For independent per-face sector-fault streams of rate sigma, the probability of at least one such birth in the slab is

1-exp(-sigma F_guard Delta) <= sigma F_guard Delta
                           <= 6sigma((2R+5)b+3)^4 Delta.

A sector stream may combine two independent Pauli types, e.g. Z and Y, whose rates sum to sigma. Sharing Y faults between sectors does not affect either marginal or the final union bound. Canceled syndrome faults still count as births by definition.

The touching faces lie within the larger coarse radius R+3 packet guard. On sufficiently large finite tori this entire local construction lifts injectively. Wrapped duplicate face labels can only lower the face count, but injectivity is needed for the iid certificate/path interpretation used above; it is already part of the large-M replay regime.

## 4. Time locality and conditioning

For every deterministic a, stationary independent increments give the same flag distribution. In particular this holds uniformly over all slabs nDelta and all spatial translations, and conditionally on the complete primitive past before nDelta. Whole fields belonging to disjoint deterministic slabs are independent, despite spatial overlap within a slab.

The same one-slab marginal argument also works at a common stopping time for the joint primitive filtration by the Poisson strong Markov property, if genuinely needed. No claim is made for an anticipating start time chosen using future marks. The theorem only needs its fixed deterministic grid.

Events at deterministic slab endpoints have probability zero; a fixed half-open convention handles definitions. The slow certificate finishes by the endpoint, while fast-word exclusion bounds all intermediate times and pre-event limits.

## 5. Union and exact quantifier order

The three flags need not be mutually independent. Their union has probability at most

2b^4 exp(((s+4)log8-C/2)b)
+ b^4(35 kappa Delta)^m/m!
+ 6sigma((2R+5)b+3)^4 Delta,

which is (B).

For the canonical recipe choose s=1, C=10log8+2, and fixed R>=ceil(280eC)+10. The slow exponent is exactly -b. These choices fix the coarse rule phi, connectivity k=4R+4 and packet dependence graph, before b is chosen. The imported HT threshold p_0 therefore depends on this fixed rule and k, not on b.

Choose any fixed p_* in (0,min(p_0,1/2)). Our self-contained domination replacement allows

delta_*=(p_*/2)^(D+1),  D=(4(R+3)+1)^4-1.

Choose a finite integer b>=4 large enough that
2b^4 exp(-b)<=delta_*/3
and b^4 2^(-floor(Rb/2))<=delta_*/3.
Such b exists because each exponential beats its polynomial prefactor. Finally set

sigma_0/kappa = delta_* / [18 C b ((2R+5)b+3)^4] > 0.

Then sigma<=sigma_0 makes the noise term <=delta_*/3. Hence the whole marginal is <=delta_*. All selected quantities are independent of L and T. Delta rescales as 1/kappa and sigma_0 scales as kappa. Only afterward take compatible L=bM with M sufficiently large for injective guards and the torus replay inequalities.

There is no circular choice: phi and its HT threshold are fixed before increasing b; the flag dependence degree stays fixed in coarse units; the physical rate is selected last. The recipe establishes a positive existence threshold even though p_0 is not quantitatively evaluated and the successive constants can be impractically poor. It establishes no usable rate, hardware feasibility, or noisy-decoder threshold.



