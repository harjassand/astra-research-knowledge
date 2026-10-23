# Exact stack representation, bath-overlap kernel, and two finite-block identities

Constructor: `/root/feedback_incorporation`  
Date: 21 October 2026  
Parent construction remains with `/root`. This contribution does not repeat the feedback audit or the parent's new height-code argument.

## Main results and limits

1. The actual rooted tree, including its port-0 exception, is exactly a two-seed binary Fock space. A finite normal-form algebra computes every coherent block amplitude and its final-bath overlaps.
2. Projecting a colored-Dyck input block onto the ideal Dyck output space gives **an exact bath-returning filter** `T_m(s) tensor I_E`. Every entry has an explicit color-matching formula. This is not a trace-preserving code by itself.
3. There is a genuine coherent interference identity: `T_m` has norm `alpha^2` for every m, attained on an explicitly constructed `(m+1)`-dimensional subspace. Its success probability `alpha^4` is independent of m. The subspace has polynomial dimension, so this construction alone gives zero asymptotic rate.
4. A fixed two-call input code and an explicit receiver decoder simulate a qubit erasure channel with probability `alpha^2 beta^2` on **all joint logical-bath inputs**. Repeated packets yield the product erasure channel at the chosen reduced logical interface without resetting the bath. All physical output/syndrome registers remain accounted for; the complete enlarged output process is not claimed to be IID.
5. The perturbed interaction is not locally unitary equivalent to U when `alpha beta != 0`: their operator Schmidt ranks are six and five. This excludes a one-use local gauge shortcut, not more general block equivalences or capacity identities.

Here `alpha=cos(s)`, `beta=sin(s)`, and `alpha^2+beta^2=1`. The written identities hold for all real s; the requested scientific question fixes a nonzero s in the small positive interval. No conclusion above establishes a reliable rate exceeding 3/2.

## 1. Exact two-seed Fock space, with the root retained

Let `F` be the Hilbert space with orthonormal basis all finite words over `{1,2}`, including the empty word `empty`. Let `L_a |w> = |a w>` be left creation. Put

`P = |empty><empty|`, `L_a* L_b = delta_ab I`,

`L_1 L_1* + L_2 L_2* = I-P`.

The physical bath is unitarily identified with `C^2_seed tensor F`. Seed 0 is the original root. Seed 1 is its port-0 child. To encode any other vertex, take the path from its seed using labels 1 and 2 and write the labels in reverse chronological order, so the most recently traversed downward edge is the leftmost letter. Every original vertex occurs once. The original root's port-0 edge switches the seeds at the empty word.

Define on the bath

`S_a = I_seed tensor L_a`,

`R = X_seed tensor P`,

`Q = I_seed tensor P`.

Then

`R*=R`, `R^2=Q`, `R S_a=0`, `S_a* R=0`,

`S_a* S_b=delta_ab I`, `sum_a S_a S_a*=I-Q`.

The physical unitary is exactly

`U = |0><0| tensor R + sum_(a=1,2) (|0><a| tensor S_a + |a><0| tensor S_a*)`.

For input a=1,2 it pushes a and outputs 0. For input 0 at a nonempty word it pops its first letter and outputs that letter. For input 0 at either seed vacuum it switches seeds and outputs 0. Thus the special root and its port-0 child are both treated correctly. The relations also give `U*=U` and `U^2=I` directly.

For the stipulated stationary initializer, every vertex at word depth k above either seed has weight `(1/3)(1/6)^k`. Hence

`tau_pi = (I_seed/2) tensor tau_F`,

`tau_F = (2/3) sum_w (1/6)^|w| |w><w|`.

This is exactly the supplied normal state, not a substitute boundary condition or a truncated tree. In particular the two seeds have equal weight. The depth used here differs by one from original distance from the root on the seed-1 component.

## 2. Exact coherent amplitudes and normal forms

Let `B_yx = <y|V_s|x>`, an operator on the bath. The only nonzero entries are

`B_00 = alpha R + i beta I`,

`B_0a = alpha S_a`, `B_a0 = alpha S_a*`, `B_aa=i beta I`, for a=1,2.

For any input word x and output word y of length n,

`A_yx = B_(y_n,x_n) ... B_(y_1,x_1)`.

The chronological order is essential. For an arbitrary normal initial density tau, the reduced block channel satisfies

`<y|N_s^tau(|x><x'|)|y'> = Tr[tau A_(y',x')* A_(y,x)]`.

Thus final-bath overlaps are retained before summing histories. Replacing these products by independent history probabilities would change the channel.

Every finite product lies in the finite linear span of

`F_uv = I_seed tensor L_u L_v*`,

`K_uv = X_seed tensor |u><v|`.

The finite matrix units with even seed parity are already in this span because

`I_seed tensor |u><v| = F_uv - sum_(a=1,2) F_(u a,v a)`.

The following multiplication rules suffice. Words are concatenated in the displayed order.

- If `x=v w`, then `F_uv F_xy = F_(u w,y)`.
- If `v=x w`, then `F_uv F_xy = F_(u,y w)`.
- If neither word is a prefix of the other, that product is zero. When equal, use the common empty-w result once.
- `F_uv K_xy = K_(u w,y)` when `x=v w`, and zero otherwise.
- `K_uv F_xy = K_(u,y w)` when `v=x w`, and zero otherwise.
- `K_uv K_xy = delta_(v,x) [F_uy - sum_a F_(u a,y a)]`.

Adjoints exchange u and v. These rules keep the rank-two boundary exactly; they do not discard rare visits to it.

### Closed stationary overlap kernel

Write `theta=1/6`. The trace rules are

`Tr(tau_pi F_uv) = delta_(u,v) theta^|u|`,

`Tr(tau_pi K_uv) = 0`.

They follow by summing the geometric mass of every prefix cylinder. Therefore the general channel matrix element above can be evaluated by a finite normal-form multiplication, with no infinite cutoff. In more explicit Gram form:

`Tr(tau_pi F_uv* F_xy)` is

- `theta^|y|` if `x=u w` and `y=v w`;
- `theta^|v|` if `u=x w` and `v=y w`;
- zero otherwise,

again counting the coincident empty-w case once. Furthermore,

`Tr(tau_pi F_uv* K_xy)=0`,

`Tr(tau_pi K_uv* K_xy)=delta_(u,x) delta_(v,y) (1-2theta) theta^|v|`.

The F terms are not generally orthogonal. Their nonzero cross overlaps are precisely a place where a path-count or incoherent-history simplification loses information. Odd and even seed-flip sectors are orthogonal only after taking the stipulated equal-seed stationary trace; arbitrary coherent tau need not have that simplification.

## 3. Balanced input/output projection is an exact bath-returning filter

Let `C_m` denote the span of all binary-colored Dyck words of length 2m, and let F(w) be the inherited ideal output word: pushes output 0 and pops output their matched push colors. Let `J_m` and `J'_m` be the input and ideal-output inclusions of that same abstract word basis. Define

`T_m(s) tensor I_E = (J'_m* tensor I_E) W_s^(2m) (J_m tensor I_E)`.

The right side really is scalar on E; this is the claim to prove.

Take input w and ideal output F(z), with both w and z colored Dyck words. At each position:

- Input push and z-push force `alpha S_a`.
- Input pop and z-pop force `alpha S_b*`.
- Input push and z-pop force `i beta I`, and their nonzero colors must agree.
- Input pop and z-push nominally allow `alpha R+i beta I`.

Let `H_w(j),H_z(j)` be the nonnegative Dyck heights after j positions. The relative bath height of the forced move history is

`h(j) = [H_w(j)+H_z(j)]/2`.

This is an integer, nonnegative, and ends at zero. At a possible R position, w is about to pop. Its pre-step height is at least one; the two pre-step heights have the same parity. Their sum is therefore at least two, so `h >= 1`. The previously created stack is nonempty and R annihilates that term. Similarly every forced pop closes an edge opened within the block and never reads the initializer. These statements include both seed vacua.

Only one move/stay selection can survive for this pair of words. Apply the forced pushes and pops to a finite color stack, and also require every simultaneous nonzero input/output color to match. If a color test fails, `T_m[z,w]=0`. Otherwise let 2r be the number of forced moves. Then

`T_m[z,w] = (-1)^(m-r) alpha^(2r) beta^(2m-2r)`.

All forced moves cancel to `I_E`, proving the operator identity for arbitrary bath vectors and, by linearity, arbitrary bath states and external entanglement. The construction is a finite exact filter. Its outcome probability can depend on the logical input, so it is not legitimate to normalize each accepted input separately and call that a deterministic code.

### Four-call example

For m=2, order the abstract input basis by separate pairs `P(a,b)=(a,0,b,0)` and nested pairs `N(a,b)=(a,b,0,0)`. In this basis, with the same ordering for ideal outputs,

`T_2 = alpha^4 I_8 - alpha^2 beta^2 X`,

`X = [[0, SWAP], [I_4, 0]]`.

X is unitary and `X^4=I`. On symmetric colors it has eigenvalues +1 and -1, each of multiplicity three. On the antisymmetric color line it has eigenvalues +i and -i. The largest singular value of `T_2` is `alpha^2`, with multiplicity three when `alpha beta != 0` away from the degenerate endpoints. In contrast, retaining only the all-move contribution would give the scalar `alpha^4`; the improvement is genuine interference.

## 4. Exact dark-pair identity and a polynomial protected subspace

For a unit color vector `c=c_1|1>+c_2|2>`, put

`S_c=c_1 S_1+c_2 S_2`,

`chi_c=(|0,c>-|c,0>)/sqrt(2)`.

Then `S_c* S_c=I`. On every bath vector psi,

`(U_1+U_2)(chi_c tensor S_c psi)=0`,

`U_2 U_1(chi_c tensor S_c psi)=-chi_c tensor S_c psi`.

These follow directly from `R S_c=0` and `S_a* S_c=c_a I`: the cross terms are proportional to `|c,c>-|c,c>` and cancel. Therefore

`V_(s,2) V_(s,1)(chi_c tensor S_c psi)=-chi_c tensor S_c psi`

for every s. The pair is exactly dark to this coherent perturbation once the stack has the matching color on top.

Consider the length-2m input vector

`|c> tensor chi_c^(tensor(m-1)) tensor |0>`.

Every basis word occurring in it is Dyck. In the balanced-output event, the first slot must move and pushes `S_c`, giving amplitude alpha. Every internal pair acts by the preceding identity and leaves that stack unchanged. The last slot must move and pops the color, giving the second alpha. The internal signs agree with the ideal F identification. Consequently T_m acts as `alpha^2 I` on the span of these vectors.

The map from m color qubits into the physical word space sends the first color to the first port, each remaining color through the linear isometry `c -> chi_c`, and appends a final 0. Restricting this isometry to `Sym^m(C^2)` gives exactly the span in question. Its dimension is m+1; the powers `c^(tensor m)` span that symmetric subspace. This proves the dimension and the operator identity for arbitrary superpositions, rather than just product color vectors.

Conversely every Dyck input starts with a push and every ideal Dyck output starts with 0, so the first projected interaction has norm |alpha|. Every input ends with 0 and every ideal output ends with a nonzero color, so the last projected interaction also has norm |alpha|. The intervening device is unitary and all remaining projections are contractions. Thus

`||T_m|| <= alpha^2`.

The explicit symmetric-color subspace saturates it. Hence `||T_m||=alpha^2` for all m. Its accepted event has probability `alpha^4` and returns the bath exactly, but its `(m+1)` logical dimension has zero asymptotic rate per 2m forward calls. I have not proved that it exhausts the maximal-singular subspace for general m. Exact checks at m=1,2,3 give dimensions 2,3,4 at the specified rational test point only.

## 5. Exact two-call erasure-channel simulation on all joint inputs

Encode a color qubit a=1,2 into the two physical input ports as `|a,0>`. Direct expansion gives

`W_s^(2)(|a,0> tensor psi)`

`= alpha^2 |0,a> tensor psi`

`  + i alpha beta |0,0> tensor S_a psi`

`  + i alpha beta sum_(b=1,2) |a,b> tensor S_b* psi`

`  + |a,0> tensor (i alpha beta R-beta^2 I) psi`.

There are no omitted root terms. Define a receiver output isometry with a four-dimensional syndrome F:

- `|0,a> -> |a>_Q |0>_F`;
- `|a,0> -> |a>_Q |1>_F`;
- `|a,1> -> |a>_Q |2>_F`;
- `|a,2> -> |a>_Q |3>_F`;
- `|0,0> -> |e>_Q |0>_F`, where e is an orthogonal erasure symbol.

It is an isometry because the nine physical output basis vectors have distinct images. Also record/dephase the binary good-versus-erasure flag in an explicit classical receiver register C. This step is needed to make the following reduced erasure channel statement hold for arbitrary coherent bath inputs; it is a local receiver instrument, not a bath measurement.

Let `r=alpha^2 beta^2`, and define

`M = alpha^2 |0>_F tensor I`

`    + |1>_F tensor (i alpha beta R-beta^2 I)`

`    + i alpha beta sum_(b=1,2) |b+1>_F tensor S_b*`,

`T = sum_(a=1,2) S_a <a|`.

The exact decoded branches are

`good: I_L tensor M`,

`erasure: i alpha beta |e>_Q |0>_F tensor T`.

Using the stack relations,

`M* M = [alpha^4+beta^4+alpha^2 beta^2] I = (1-r) I`,

`T* T = I_(L tensor E)`.

In the first identity the cross terms in `(i alpha beta R-beta^2 I)* (i alpha beta R-beta^2 I)` cancel, while `R^2+sum_b S_b S_b*=I`. These are identities on the **whole bath**, not expectations in its stationary state.

Let rho be any joint trace-class state on `A tensor L tensor E`, with A an arbitrary reference containing any other logical packets or previous laboratory systems. After this decoder, and after tracing the bath, syndrome, and unused record when defining the chosen logical port,

`Tr_(E,F,C) decoded(rho) = (id_A tensor Er_r)(Tr_E rho)`,

where

`Er_r(X) = (1-r) X + r Tr(X) |e><e|`

and the first term is embedded in the color-qubit subspace of Q. To prove the equality, test the good branch against any observable on A and L and use `M* M=(1-r)I`; it gives `(1-r)Tr_E rho`. The erasure branch gives `r Tr_(L,E)rho` by `T*T=I`. The retained flag record removes cross terms. Thus no initial product assumption between L and E is used in the one-block identity.

This proves a reusable reduced-port simulation: apply it successively to packets on the same bath, with the same fixed encoding and decoding. The identity remains valid when A includes all other packets and prior retained outputs, so induction (or backward propagation of observables) gives the product erasure channel at the selected logical interfaces. The flag probabilities are IID Bernoulli(r), even though the physical bath and syndromes may have memory. Standard protocols that use only those logical outputs and flags can therefore be run without a bath reset.

### Resource and claim boundary

Every simulated qubit channel uses exactly two forward qutrit calls. The four-dimensional syndrome and binary measurement record are external receiver registers and are retained/accounted for. Ignoring them in the chosen logical interface is an explicit local decoding choice; they are not hidden bath cells. The erasure branch stores the lost qubit in the bath through T. The good branch can also change the bath through M. No terminal bath return is asserted for this full two-call erasure simulation when s is nonzero.

The complete enlarged physical output process, including all syndrome information, is not claimed to equal an IID erasure channel. Reusing those extra registers for a different decoder could exploit additional information. The result is an exact simulation under the stated interface, not a converse for the original device and not a capacity gain above 3/2.

## 6. A precise obstruction to local gauge equivalence

The five reservoir operators `R,S_1,S_2,S_1*,S_2*` are linearly independent, as are their five port matrix coefficients. Thus the algebraic operator Schmidt rank of U across port versus bath is five.

For `alpha beta != 0`, V_s adds the independent reservoir operator I with independent port coefficient `I_3`. The six port coefficients `|0><0|,|0><1|,|0><2|,|1><0|,|2><0|,I_3` are independent. On the bath, R has odd seed parity; the S and adjoint S operators change word length by opposite signs; I preserves length and seed. Orthogonality of the creation ranges finishes their independence. Hence the operator Schmidt rank of V_s is six.

Pre- and postmultiplication by local port/bath unitaries act invertibly on the two operator factors and preserve this rank. Therefore no such one-use local unitary equivalence transforms V_s to U at nonzero alpha beta. This argument does not exclude time-dependent block encodings, generalized process simulations, or equality of their communication capacities.

## 7. Executable evidence and resources

The standard-library file `representation/exact_representation.py` implements Gaussian-rational coefficients, the infinite-bath normal-form multiplication, the stationary trace kernel, block amplitudes, the balanced-word formula, and exact rational small-matrix ranks. Run from the packet root or adjust the script path:

`python representation/exact_representation.py --output representation/replay.json`

The replay uses the exact small-angle point

`alpha=4194303/4194305`, `beta=4096/4194305`,

which obeys `alpha^2+beta^2=1` and `0<beta<=1/512`. It checks the stack/root identities, one-use unitarity, all two-slot code amplitudes, good-branch normalization, dark-pair identities for exact real and complex color vectors, and every balanced input/output pair for m=1,2,3. A separate exact rational spectral diagnostic at `beta^2=2^-20` gives maximal-singular-subspace dimensions 2,3,4 for those three blocks. That finite observation is not promoted to an exhaustive all-m theorem.

The recorded replay passed without a finite bath truncation. Observed script body time was approximately 0.1044 seconds, peak resident memory 11,904 KiB on Linux, Python 3.12.14. The complete values are in `representation/replay.json`. These are replay costs, not the cost of finding or checking the mathematical constructions. Model/search energy and total monetary cost are not exposed and are not estimated.

An exploratory attempt to use SymPy found it unavailable in both the default and primary Python runtimes. No package was installed. The final implementation uses only the standard library. No old capacity replay, outside compute service, purchase, outreach, or public posting occurred.

The written operator identities, not the finite check count, establish the universal claims. Historical novelty and external certification remain unassessed. The parent's stronger height-code construction is distinct and has not been duplicated here.
