# Ordinary quantum capacity: independent construction and exact unresolved boundary

**Whole-question outcome: unresolved.** I have neither constructed the requested total additive-1/4 evaluator nor proved that it cannot exist. The complete constructions below are an exact rational finite-block evaluator, a quantitative equivalence between the requested evaluator and a dimension-only effective truncation, and a countermodel that excludes a particular inference from strong converses. None is substituted for the requested resolution.

This is the initial independent construction by r1. I deliberately read the common question, accepted N675's quantified statement, and the two supplied completed predecessor responses. I did not access another pilot constructor's developing work or a lead solution. A public-source search incidentally returned Harjas's already published N684 capacity/distillation page. Local memory supplied an older reminder that the ordinary and assisted questions differ; the current originals, rather than an older unreviewed label in memory, govern the accepted premises. No missing predecessor PDF/ZIP was recovered or assumed available.

## 1. A rational-only finite-block operation

Put

\[
q_n(N)=\frac1n\max_\rho I_c(\rho,N^{\otimes n}),\qquad
Q(N)=\sup_n q_n(N).
\]

For the promised input encoding, every q_n is uniformly computable to certified additive precision. Here is an explicit operation that requires neither an optimization oracle nor algebraic Kraus factors.

Let a=dim A, b=dim B, d=a^n, c=b^n. Form the normalized rational Choi matrix of N^n by tensoring and regrouping its input and output indices. For a nonzero complex rational d-by-d matrix T, use

\[
\rho_T=TT^*/s,\quad s=\operatorname{Tr}(TT^*),\quad
|\psi_T\rangle=s^{-1/2}\sum_{i,r}T_{ir}|r\rangle_R|i\rangle_A.
\]

The density matrix of this purification is rational even though its displayed vector need not be. The output on RB is exactly

\[
\Omega_{rb,r'b'}=
\frac d{s}\sum_{i,j}T_{ir}\overline{T_{jr'}}
(J_{N^n})_{(i,b),(j,b')}.
\]

The factor d comes from the normalized Choi convention. Both Omega_RB and Omega_B are rational density matrices. Since the true channel dilation and the input purification together are pure,

\[
I_c(\rho_T,N^n)=S(\Omega_B)-S(\Omega_{RB}).
\]

Thus no independently supplied environmental map is used.

### Entropy with rational arithmetic

For a D-dimensional density matrix sigma define

\[
P_m(\sigma)=\sum_{k=1}^m
\frac{\operatorname{Tr}[\sigma(I-\sigma)^k]}k.
\]

The scalar expansion of -x log x gives

\[
0\le S_{\rm nats}(\sigma)-P_m(\sigma)\le \frac D{m+1}.
\tag{1}
\]

To verify the tail, for x>0,

\[
x\sum_{k=m+1}^\infty\frac{(1-x)^k}k
\le \frac{x}{m+1}\frac{(1-x)^{m+1}}x
\le\frac1{m+1}.
\]

The x=0 term is zero. Summing over D eigenvalues proves (1), including singular states.

The expansion

\[
\ln2=2\sum_{j=0}^{K-1}\frac{3^{-(2j+1)}}{2j+1}+r_K,
\quad 0<r_K\le\frac9{4(2K+1)3^{2K+1}}
\]

supplies positive rational brackets ell<=ln2<=u. Consequently

\[
P_m/u\le S_{\rm bits}(\sigma)
\le [P_m+D/(m+1)]/\ell.
\tag{2}
\]

All terms in (2) are computed by rational matrix multiplication, trace, and integer arithmetic. No minimum-eigenvalue promise or hidden condition number is required.

### A complete finite input net and its cost

Take every matrix T=P/H, where each real and imaginary entry of the integer matrix P lies in {-H,...,H}, except the zero matrix. For every input state rho, round sqrt(rho) entrywise to this grid. Its Frobenius error is at most d/H. If d/H<=tau/2, normalization changes the associated pure vector by at most tau; the trace distance of the pure states, and of either channel output, is then at most tau.

For trace distance tau<=1/2, entropy continuity gives

\[
|I_c(\rho,N^n)-I_c(\rho_T,N^n)|/n
\le \tau(\log_2 a+2\log_2 b)+8\sqrt\tau/n.
\tag{3}
\]

For completeness, the loose bound used here is h_2(t)<=4 sqrt(t). It follows from -t ln t<=sqrt(t), -(1-t)ln(1-t)<=t, and ln2>1/2. The usual entropy-continuity estimate then gives (3), using output dimensions c and dc.

For desired normalized error epsilon>0, let

\[
C=\lceil\log_2a\rceil+2\lceil\log_2b\rceil,
\quad u_0=\min\{1/4,\epsilon/[16(C+8)]\},
\quad \tau=u_0^2,
\quad H=\lceil 2d/\tau\rceil.
\]

Then the right side of (3) is at most u_0(C+8)<=epsilon/16. The number of Gram factors inspected is exactly

\[
(2H+1)^{2d^2}-1.
\tag{4}
\]

Set eta=n epsilon/8, use m>=8dc/eta, and take an ln2 bracket of width at most eta/(16dc). Each output-entropy interval has width at most eta/2: the polynomial tail contributes at most eta/4 and the ln2 bracket at most eta/4. The resulting coherent-information interval has width at most eta. Maximize its lower and upper endpoints separately over the finite net, divide by n, and add epsilon/16 to the upper endpoint for (3). The interval contains q_n and has width less than epsilon.

This proves termination of the finite operation with an explicit mathematical error guarantee.

For an input Choi matrix of common-denominator bit length B, the tensor matrix has (ab)^(2n) entries of bit length O(nB+n log a), and its literal construction uses O(n(dc)^2) rational scalar operations. The largest density matrix evaluated above has dimension dc=(ab)^n. The literal algorithm performs the number of evaluations in (4); one evaluation uses O(d^4 c^2+m (dc)^3) rational scalar operations, including forming the purification output and naive dense entropy-polynomial multiplication. The common denominator of an output density matrix has bit length O(nB+log s), where s is the integer squared norm of P and log s=O(log d+log H). A conservative bound for intermediate entropy-arithmetic bit length is O(m[nB+log s+log m+log(dc)]). These costs are enormous but finite and effective. Acquisition consists of the input matrix itself; no witnessing code, reference, strategy, package, or external service is an input to this operation.

The executable `rational_block.py` implements this construction, including complex rational arithmetic, tensor regrouping, the complete Gram-net loop and the entropy intervals. Its full net is not claimed executed. Already for a=b=2, n=1, epsilon=1/4, the conservative parameters are H=1,982,464, m=1,024, and the net count has 53 decimal digits.

## 2. The exact remaining evaluator operation is a recursive uniform cutoff

The following equivalence gives a different representation of the whole question. It is a proof of equivalence, not a construction of either equivalent object.

**Theorem.** The following assertions are equivalent on the common input contract.

1. There is a total additive-1/4 evaluator for Q on rational valid Choi inputs.
2. There is a total arbitrary-accuracy evaluator on those inputs.
3. There is a total computable function F(a,b,epsilon), depending only on the two dimensions and rational epsilon>0, such that

   Q(N)-q_F(a,b,epsilon)(N)<=epsilon

   for every a-to-b channel, including channels with nonrational entries.

4. There is a total computable instance-dependent sufficient blocklength on rational inputs, with an arbitrary requested accuracy.

The nonrational channels in assertion 3 are a mathematical quantifier, not a claim that they are supplied by exact finite rational descriptions.

### Fixed error and arbitrary error

Q(N^k)=kQ(N). Tensor powers of a rational normalized Choi matrix are rational normalized Choi matrices. Calling the putative fixed-error evaluator on N^k and dividing its answer by k gives error at most 1/(4k). To achieve error delta, take k>=1/(4 delta).

The amplified input has input/output dimensions a^k,b^k and (ab)^(2k) entries; its entry bit lengths grow linearly with k times the original common-denominator size. This is an actual explicit input expansion. No efficient reduction is asserted.

### A common continuity modulus for all blocklengths

Write delta=(1/2)||N-M||_diamond. Replacing one channel use at a time and keeping the purification R of the common input gives

\[
|q_n(N)-q_n(M)|\le g_b(\delta),\quad
|Q(N)-Q(M)|\le g_b(\delta),
\]

where

\[
g_b(\delta)=4\delta\log_2b+
2(1+\delta)h_2(\delta/(1+\delta)).
\tag{5}
\]

Here is a direct justification. In one replacement the marginal on R and all output sites except the replaced B_i is unchanged. The change in coherent information is therefore the difference of the changes in S(B_i|B_others) and S(B_i|R B_others). For states at trace distance delta, the conditional-entropy mixing argument gives a bound 2 delta log b+(1+delta)h_2(delta/(1+delta)) for each term. Summing n replacements and dividing by n proves (5). The bound survives maximization and a supremum over n.

For delta=t^2<=1, a useful entirely explicit upper bound is

\[
g_b(\delta)\le (4\lceil\log_2 b\rceil+12)t.
\tag{6}
\]

Thus a rational delta sufficient for any required continuity error is computably selectable.

### An effective rational net of all channels with fixed dimensions

This net does not assume a capacity evaluator. Let D=ab and J_0=I_D/D. For a target Choi trace-norm net radius r>0, shrink every valid J to

\[
J'=(1-\lambda)J+\lambda J_0,\quad \lambda=r/8.
\]

For r<=1, the least eigenvalue of J' is at least lambda/D and ||J-J'||_1<=2 lambda. Round J' to a Hermitian rational grid matrix K with entry magnitude error at most h. Project back to the trace-preserving affine space using

\[
K'=K-[\operatorname{Tr}_B K-I_A/a]\otimes I_B/b.
\]

If h<=lambda/(4D^2), then ||K'-J'||_infinity<=2Dh<=lambda/(2D). Hence K' is positive, has the correct partial trace, and

\[
\|K'-J\|_1\le 2\lambda+2D^2h<r.
\]

Enumerate all bounded grid matrices and retain those whose projected matrices are positive. Positivity is decidable exactly using rational principal minors. This is a finite rational valid-channel net. Since ||N-M||_diamond<=a||J_N-J_M||_1, taking r=2 delta/a supplies a delta-net in half diamond norm. Its size and rational denominator bounds depend computably only on a,b,delta. No code or large auxiliary state is acquired by constructing this net.

### From a total evaluator to a dimension-only cutoff

Fix a,b,epsilon. Select delta so g_b(delta)<=epsilon/8 and construct the preceding finite rational channel net {M_j}. Use the putative evaluator, with the tensor amplification above, to obtain v_j satisfying

\[
|v_j-Q(M_j)|\le\epsilon/32.
\]

For t=0,1,..., compute certified lower bounds L_j,t on q_(2^t)(M_j) with error at most epsilon/32, using Section 1. Stop when

\[
L_{j,t}>v_j-\epsilon/8\qquad\hbox{for every }j.
\tag{7}
\]

This stopping test is rational and decidable. It eventually succeeds: q_(2^t)(M_j) increases to Q(M_j), while the threshold in (7) is at most Q(M_j)-3 epsilon/32. The finite evaluation's lower error is at most epsilon/32.

At the successful n=2^t, each net channel obeys q_n(M_j)>Q(M_j)-5 epsilon/32. For an arbitrary channel N, choose a net channel at distance delta. Apply (5) twice to obtain

\[
q_n(N)>Q(N)-5\epsilon/32-2\epsilon/8
>Q(N)-\epsilon.
\]

This constructs F from the assumed evaluator. The evaluator calls, the rational channel net, the finite-block searches, and their huge dimension/precision costs are all explicit finite operations. The proof does not presume a code-search convergence modulus in order to find F.

Conversely, a computable F and the finite operation in Section 1 immediately give a total Q evaluator. An instance-dependent cutoff is equivalent by the same argument, or by searching q_n after obtaining an arbitrarily precise capacity value. This proves all four assertions equivalent.

### Why compactness alone stops short

For every fixed a,b,epsilon a finite dimension-only cutoff does exist. The functions q_(2^t) are continuous, increase to Q, and have the common modulus (5) on a compact channel space. A finite-cover argument, equivalently Dini's theorem, gives uniform convergence. The unconstructed operation is selecting these cutoffs by one total algorithm across a,b,epsilon. The argument above shows that making that selection effective would already resolve the requested question positively.

Cubitt et al.'s 2015 result excludes one blocklength working independently of channel dimensions; it does not say that this dimension-dependent cutoff cannot be computable. The accepted N675 helper/reference obstruction does not supply that missing ordinary-channel claim.

## 3. Semidecidability and exact threshold quantifiers

Section 1 gives a uniform computable increasing rational sequence L_s(N) converging to Q(N): at stage s combine all certified lower bounds already obtained for n<=s with precision at most 1/s, keeping the maximum and zero. Therefore

\[
Q(N)>r\ \Longleftrightarrow\ \exists s\,[L_s(N)>r],
\]

and Q(N)<=r is a universal computable predicate. Equality boundaries require the additional precision quantifier:

\[
Q(N)\ge r\ \Longleftrightarrow\
\forall k\ \exists s\,[L_s(N)>r-2^{-k}],
\]

\[
Q(N)<r\ \Longleftrightarrow\
\exists k\ \forall s\,[L_s(N)\le r-2^{-k}].
\]

These statements concern explicit rational channel inputs, with approximate finite-block optimization performed by the operation above. They do not require deciding exact equalities between entropy maxima and rational numbers. In particular, a promise Q>=u versus Q<=v with u>v has a search that halts in the upper branch. It does not have a constructed search that halts in the lower branch. This is compatible with either computability answer.

## 4. A fully effective strong converse does not select the cutoff

The new general strong converses were checked as a possible positive route. Their capacity/Renyi quantities still involve regularization. More generally, even an effective, all-blocklength exponential strong converse is not by itself a convergence-modulus theorem.

Here is a precise countermodel to that inference, not a constructed quantum channel. For a machine z, simulate it for n steps and define

\[
a_n(z)=
\begin{cases}
\max(0,n-T),&\text{if it first halts at time }T\le n,\\
0,&\text{otherwise}.
\end{cases}
\]

This is uniformly computable, 0<=a_n<=n, superadditive, and has increments in {0,1}. Its limiting normalized rate is C(z)=1 if z halts and 0 otherwise. Put

\[
f_n(z,R)=2^{-\max\{0,nR-a_n(z)\}}.
\]

Every finite f_n is computable. Below C, f_n eventually equals one. Above C, for every n,

\[
f_n(z,R)\le2^{-n(R-C(z))}.
\]

Thus the strong-converse exponent is explicitly at least the rate gap, with no non-effective starting blocklength. Product-code consistency also holds, since superadditivity gives f_(n+m)(R)>=f_n(R)f_m(R). Nevertheless C is the halting indicator and no effective truncation exists. To turn this into the desired negative theorem one would have to realize such a family as actual finite rational memoryless channels. I have not constructed that operation.

## 5. Attempts at the negative direction and their exact remaining issue

I considered reductions through the accepted source-defined defect V(E,F), the completed symmetric-helper capacity Q_ss, channel potentials, and stationary input processes. The accepted N675 theorem is used at its stated generic variable-dimensional rational positive-POVM scope; its proof is not reopened. It supplies a computable positive defect margin in the halting branch and zero in the other branch. The completed N1677 ordinary physical complement and assisted rate construction are credited at their actual scope.

That margin alone does not yet give a computable lower bound on the ordinary rate. A finite reference of unknown dimension can be transported through the constructed ordinary channel in a finite block, but the achieved rate can have an unknown denominator. A search for a positive coherent-information block then supplies only the semidecision in Section 3. It does not make the no-case terminate.

The stationary-memory representation does remove an unknown finite reference size from *boundary* costs. However, its emitted receiver and environment histories implement actual lossy channels on the memory. Replacing those histories by untouched copies of the virtual reference changes the entropy terms. The supplied predecessor identifies a signed history remainder with no established lower bound, and includes an explicit extensive correction. I found no argument that controls that remainder for the N675 hard family. A fast averaged memory mixer is not, by itself, a recovery map available to both outputs; a record-conditioned unitary trajectory does not imply reference transmission.

I also examined whether computing Q on every finite helper extension would compute Q_ss. It yields a computable sequence of finite-helper values only under the assumed Q evaluator. Its supremum still has no effective helper cutoff, exactly the issue ruled out by the accepted assisted theorem. A computable supremum's finite terms need not give a computable supremum; no contradiction follows. Topological uniform positivity at fixed main dimensions similarly does not supply an effective minimum positive ordinary rate across the hard family.

The explicit circuit/QMA construction of Bhattacharyya--Mehta--Zhao v3 was checked against the requested input encoding. It gives computational hardness with a constant ordinary-capacity gap, while its undecidability construction uses a restricted assisted zero-error resource. Its QMA result is compatible with the finite algorithm in Section 1 because no running-time promise is made here. Circuit-to-matrix expansion must be charged and does not prove nonexistence of an unrestricted-time evaluator.

No failed attempt above is promoted to an obstruction for all ordinary codes. No stationary catalyst, untouched reference, free quantum wire, postselection, or assisted rate has been silently included in Q.

## 6. Executed work and source limits

The standard-library exact-arithmetic fixture run of `rational_block.py` completed in approximately 0.36 seconds of tool wall time. It certified intervals containing coherent information 1, 0, 0, 1/2, and -1 for a maximally mixed qubit through identity, dephasing, half-erasure, quarter-erasure, and full-erasure channels, respectively. Exact tensor-regrouping equality was checked for two identity uses. A nonreal Gram factor passed exact trace, purity and Hermiticity checks. These checks test implementation conventions; the general finite-net guarantee is the proof above. The astronomical exhaustive net, an encoded halting instance, a capacity upper-bound hierarchy, and an end-to-end main-question solution were not executed or obtained.

Only r1's directory was written. No package was installed, no paid/API service or physical experiment was used, no source-transfer hold was bypassed, and no shared integration, predecessor or memory file was changed. Model compute usage is not inferred from elapsed wall time and remains under the lead's account-wide guard.

Governing local originals read in place:

- `repo/updates/DG/package/channel_order_undecidability/EXTRACTED_TEXT.txt`, Sections 1 and 11--14, with `repo/knowledge/current/packets/N675.json`'s current acceptance.
- `repo/research/2026-11-03-p1-symmetric-assistance-return/source/p1/COMPLETE_VISIBLE_RESPONSE.txt`.
- `repo/research/2026-11-03-p1-ordinary-capacity-resource-interface/source/p1/COMPLETE_VISIBLE_RESPONSE.txt`.

Here `repo` is the read-only path supplied in COMMON_QUESTION.md. The offered missing PDF/ZIP packages remain unavailable and unused.

Public primary-source checks:

- Bhattacharyya--Mehta--Zhao, [arXiv:2601.22471v3](https://arxiv.org/html/2601.22471v3): the ordinary constant-gap QMA result and restricted assisted zero-error result are distinct. The ordinary computability question is explicitly not resolved there.
- Cubitt et al., [arXiv:1408.5115](https://arxiv.org/abs/1408.5115), [Nature Communications 6, 6739](https://doi.org/10.1038/ncomms7739): no fixed detection block works uniformly over all channel dimensions. No noncomputable convergence modulus is imported.
- Smith--Smolin--Winter, [quant-ph/0607039](https://arxiv.org/abs/quant-ph/0607039): the symmetric helper is an additional resource; bounding its dimension is a separate evaluation issue.
- Cheng--Tomamichel, [arXiv:2609.08998](https://arxiv.org/abs/2609.08998), and Tomamichel's [account of the two strong-converse proofs](https://marcotom.info/the-tale-of-two-proofs-of-the-strong-converse/): the Renyi comparison is still regularized. Section 4 above is an independent logical countermodel, not a claim made by these authors.
- Khabbazi Oskouei--Mancini, [arXiv:1608.07730v3](https://arxiv.org/html/1608.07730): the paper explicitly defines recursive approximability as convergence of a computable sequence, without a computable precision-to-stage modulus. Its universal semidensity representation does not supply the requested evaluator.

I also inspected the primary qutrit-incapacity paper [arXiv:2607.24693v1](https://arxiv.org/html/2607.24693v1) and the potential-capacities primary abstract [arXiv:1505.00907](https://arxiv.org/abs/1505.00907). Neither was used as a premise in the constructions above. Discovery snippets, catalogue status, and unacquired attachments are not theorems in this argument.

The whole question therefore remains open after this independent attempt. The concrete unresolved operation in the positive representation is a recursive uniform cutoff F; in the attempted negative representations it is an actual ordinary-rate gap or an equivalent memoryless-channel realization. The bounded pilot does not supply either operation by assumption.
