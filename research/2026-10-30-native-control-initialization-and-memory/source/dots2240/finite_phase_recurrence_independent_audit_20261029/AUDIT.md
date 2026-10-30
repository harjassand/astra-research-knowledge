# Independent hostile audit: one-count / finite-mode chemical recurrence
2026-10-29. Reviewed complete source bytes listed in SOURCE_SHA256.txt. No publication or novelty claim.

## Verdict and scope
I find the three supplied arguments mathematically sound under their exact finite one-hot-mode contract. Together they prove nonexplosion and positive recurrence of every communicating class, and finiteness of every exponential count moment of each class's invariant probability. This is an independent reconstruction of the proof, not acceptance based on other reviewers' agreement or finite simulations.

The theorem is not the arbitrary-dimensional weakly reversible chemical recurrence conjecture. Neither an arbitrary projection to one coordinate nor a fluctuating infinite internal background is covered. It does cover the advertised one unbounded count with a finite weakly reversible mode-labelled complex graph, without a uniform mixing gap or time-scale separation.

No concrete proof defect was found. Below I give the critical derivations and the boundary and tail details that must remain attached to the result.

## 1. Tree exponents and the invariant alternative
For every sufficiently large real count, each projected mode edge rate is a polynomial with positive leading coefficient. Irreducibility makes every rooted tree sum nonzero and positive; its leading terms cannot cancel. Taking beta_j=deg(tau_j)-max deg(tau) therefore gives the asserted stationary asymptotic. Fixed finite shifts of the argument leave both leading degree and coefficient unchanged. This validates reusing the same beta after changing to r=x+beta_j.

Finite mode stationarity cancels the added beta increment exactly, not asymptotically. If all residual increments delta are zero, r is an exact state-space invariant, including boundary transitions. Each fixed-r class contains at most one count per mode and hence at most m states. All such finite classes are closed by the return-path argument below; positive recurrence, nonexplosion and exponential moments are immediate.

If some delta is nonzero, weak reversibility guarantees a downward edge. For the frozen drift, the highest source height among nonhorizontal edges cannot have an upward outgoing edge: its complex return path would have a nonhorizontal downward crossing with still higher source height. Thus every maximal contributing term is negative, with no leading cancellation. Negative heights/exponents are harmless. This correctly proves the frozen sign, while not by itself proving actual recurrence.

## 2. Fixed-tilt matrix: signs and strictness
The weighted identity is exact because mode stationarity cancels sum F_e(u_k^2-u_j^2). Self-mode jumps contribute zero to its untilted Dirichlet term, but their tilt term remains, as required.

For downward tilt t in (0,1), the contribution equals

  -t F (u_k-u_j)^2/2 -(1-t)F(u_j^2+u_k^2)/2.

For upward t=1+b, expanding u_j u_k=u_k^2+(u_j-u_k)u_k and applying b|d u_k|<=d^2/4+b^2 u_k^2 gives exactly the claimed negative one-quarter Dirichlet term plus (b+b^2)F u_k^2. No sign reversal or missing factor is present.

For an upward edge from height h, stop a complex return path at its first vertex of height <=h. Every source on the stopped path has height >=h+1, and its final edge is downward. Therefore each relevant flux dominates the original upward flux by a factor of order at least r. Telescoping the mode values to the final edge's source uses only the preceding path differences, and the final downward sink controls that last value. Repeated modes and same-mode reactions do not break this estimate. With finitely many upward edges, all burdens are absorbed for a finite common threshold; fixed large tilts merely worsen that threshold.

The retained energy vanishes only on vectors constant on the connected projected mode graph. A downward sink then forces that constant to zero. Thus the symmetric part of P G is strictly negative definite even when its least eigenvalue approaches zero with r. For any complex eigenvector, splitting into real/imaginary parts proves Re(lambda)<0. Consequently the Metzler semigroup integral gives a nonnegative inverse of -G, and the transposed inverse applied to 1 is strictly positive (already its small-time integrand is positive). No uniform spectral margin is assumed or needed.

## 3. Exact adjoint lift and shift slack
G has polynomial entries; its inverse entries are rational functions with real coefficients (rational coefficients for the specified rational rates/tilts). Eventual positivity implies a positive leading asymptotic c r^d for each v_j, so every fixed-shift ratio tends to 1, including when d is negative.

An incoming reaction with increment delta starts at r-delta. Its incoming mass is exactly exp(-theta r) exp(theta delta) v_j(r-delta) lambda_e(r-delta). Multiplicative slack exp(eta|delta|)>1 dominates the finite-shift ratio for each nonzero delta at sufficiently large r. For delta=0 the two arguments are identical, so horizontal rates require no approximation at all. This is the essential repair of the naive variable-corrector problem; arbitrarily fast horizontal transitions generate no shift error.

Subtracting the exact outgoing loss yields L*mu<=exp(-theta r)G^T v=-exp(-theta r). Boundary infeasibility and the arbitrary low-state extension affect only finitely many states because all increments and mode offsets are bounded. Exponential decay times a positive rational function ensures both sum mu and sum mu q are finite. Thus every infinite sum used later is justified by nonnegativity or finite absolute total mass, rather than formal cancellation of divergent quantities.

## 4. Closed classes, including boundaries
For an enabled edge from (a,j) to (b,k) at count x>=a, set z=x-a>=0. Following a directed complex return path produces successive states with counts z+a_path and the corresponding modes. Every step is enabled because z>=0. The path returns to the original state. Thus every state transition has an enabled state-level return path, and every communicating class is closed, even at small counts. One cannot replace weak reversibility by mere irreducibility of the projected mode graph in this step.

After deleting null state transitions, every nonabsorbing state has 0<q<infinity. Absorbing singletons are already settled. If an entire nonabsorbing class missed K, summing the strict adjoint inequality over that closed class would contradict conservation of the finite measure nu=mu q under the stochastic embedded kernel. Hence it meets K. This also implies only finitely many nonabsorbing classes in a non-invariant projected component, although the proof does not need that corollary.

## 5. Embedded recurrence and nonexplosion: complete argument
Let A=Gamma intersect K and C=Gamma minus K. The dual inequality gives

  nu_C >= nu_C P_CC + nu_A P_AC.

Iteration yields nu_A P_AC sum_{n>=0}P_CC^n <=nu_C. Since each nu_a>0 and A is finite, the expected number of consecutive C visits after leaving any a in A is finite. An infinite excursion would contribute infinite occupation, so every such excursion returns almost surely. Direct transitions within A take one step and create no difficulty.

The successive-visit chain on finite A is irreducible: any state-level path between A states can be compressed at its A visits, and all excursions return. Its expected number of successive visits to hit a specified a is finite. Expected original jump counts between successive A visits are uniformly finite because A is finite. Thus a has finite expected embedded return time; irreducibility then establishes positive recurrence of the entire embedded class. This does not assume continuous-time nonexplosion in advance: the embedded stochastic kernel is defined independently of holding times.

The recurrent embedded path visits a fixed finite-rate state infinitely often almost surely. Conditional on that path, its holding times at that state are independent identically distributed exponentials with a positive finite mean. Their sum diverges almost surely, ruling out finite-time explosion. This also handles arbitrary initial states in the class by irreducible recurrence.

Every positive falling factorial at an integer state is at least 1. Hence q>=min_e kappa_e for nonabsorbing states, after restricting to the finite reaction list and ignoring null transitions. The mean physical holding time is uniformly bounded above. Finite expected embedded return steps therefore give finite expected physical return time. The direction of this bound is correct; no upper bound on rates is required.

## 6. Tail domination made explicit
Choose a regeneration state a in A. Let g_i be its expected embedded occupation counts before return. The expected numbers g_i for i in finite A are finite, so choose c=max_{i in A}g_i/nu_i. By excursion decomposition,

  g_C=g_A P_AC sum_{n>=0}P_CC^n <=c nu_C,

and g_A<=c nu_A. Therefore the invariant embedded occupation measure is dominated by a constant times nu on the entire class. Dividing occupation at state i by q_i gives continuous-time occupation, dominated by c mu_i. Its total mass is positive and finite; normalizing preserves domination up to another class-dependent constant. This supplies the detail omitted by the source's brief 'use the excursion Green bound' sentence.

For any desired exponential moment exponent s>0, run the construction with theta>s and 0<eta<theta. Then exp(s x)mu(x,j) is summable because r=x+beta_j and the remaining factor has only polynomial growth. The class's invariant probability is unique, so separate choices of theta prove all exponential moments of the same probability. There is no requirement that the constants be uniform in theta or that one envelope simultaneously work for every theta.

## 7. Broader opening that is justified, and one that is not
A useful rigorous corollary is available when an original network has one unrestricted species X and all other species are confined to a finite closed internal state set S (for example by fixed internal conservation totals). Replace each internal population vector z in S by a mode. For every original reaction a X+y -> b X+y', and every feasible z>=y in S, insert the lifted edge (a,z)->(b,z-y+y') with rate constant kappa (z)_y. This is a finite network of the required form.

Weak reversibility lifts: along an original complex return path, hold the residual internal population z-y fixed. Every intermediate internal state is nonnegative and belongs to the same closed set S, so all lifted return edges exist. The theorem therefore applies to this finite-background family, including non-one-hot original internal chemistry, provided S is indeed closed and finite. Constants and mode count may grow badly with the supplied conservation totals.

This does not justify freezing an internal population that is not conserved, replacing an infinite background by a finite truncation, reducing arbitrary multidimensional weakly reversible networks, or treating coupled unbounded species as one count without an exact state-space/rate-preserving lift. Those remain genuine broader problems.

## Exact-version and presentation qualifications
- Acceptance binds the three SHA-256 source versions in SOURCE_SHA256.txt. Changes to the tilted slack, path stopping rule, reset of residual coordinate, or embedded-measure inequality need rereview.
- A consolidated theorem statement should explicitly include arbitrary fixed positive rate constants, fixed finite graph, integer nonnegative source/product counts, exact one-hot mode constraint, and weak reversibility of the full complex graph.
- The invariant case is handled separately; finite classes have class-dependent moment constants, not a uniform bound over all invariant levels.
- This is proof validation, not a literature/novelty search or an external referee endorsement. No numerical screen is used as evidence for the general theorem.
