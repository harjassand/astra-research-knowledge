# Three-call blocks suffice for coherent sector acquisition

24 October2026(local),w64. NEW refinement of frozen309a506... . The original coherent-sector construction remains unchanged and sufficient. This proof replaces its drain/long-reset classifier by a fixed input100 block and derives a native depth-process concentration bound. New full fresh criticism PENDING. No generic Markov or coherent-uncomputation novelty is claimed.

## TC1. Exact native outcome instruments, no bath-state oracle

For a fixed seed-X sector x and arbitrary word input, send the two-call program10. Let J=x|empty><empty| in this sector. With the CORRECT Y=i(|10><01|-|01><10|), its hypothetical measured +/- Kraus operators are

    K_+=[(a+i b)I+alpha beta J]/sqrt2,
    K_-=[(a-i b)I-alpha beta J]/sqrt2,

and the Y0 instrument has THREE distinct Kraus operators

    i alpha beta S1, i alpha beta S1*, i alpha beta S2*.

These follow by retaining all output patterns01,10,00,11,12 of the actual two native V calls. In particular the zero subspace is not replaced by a coherent sum of its orthogonal output Kraus operators.

K_+,K_- are word diagonal. Every other Kraus operator is a partial injection of words. The same holds for the vacuum reset Kraus operators alpha J+i beta I and alpha S_j*. Therefore initial off-diagonal WORD operators never contribute to the trace of any outcome sequence: the entire classifier POVM is word diagonal. Its diagonal entries depend only on initial DEPTH, because each nonempty word has exactly one possible top-color pop. Hence its worst error on the whole depth<=H quantum subspace and arbitrary references is exactly the worst error of the corresponding classical depth process over h0=0,...,H. This equivalence is only for the hypothetical outcome probabilities; the actual classifier circuit keeps every port coherent.

Put m=2a^(3/2)beta. The two-call probe has probabilities

    at root: Pr(Y=+1/-1)=[1-ab +/-x m]/2;
             Y0 pushes1 with probability ab;
    nonroot: Pr(Y=+1)=Pr(Y=-1)=(a^2+b^2)/2;
             Y0 pushes1 with probability ab,
             Y0 pops its top color with probability ab.

Now append ONE physical vacuum call after every probe. This is exactly the fixed three-port input100 block. The conditional signal before block k obeys

    E[Y_k|history]=x m 1_(h_k=0).                  (TC1)

All three physical calls are retained coherently for later C* reversal.

## TC2. An exact workload representation

Let iid Z_k take values+1,-1 with probability ab each and0 otherwise. Let iid B_k be Bernoulli(a), independent of Z_k. The full post-block depth transition is exactly

    h_(k+1)=max(0,h_k+W_k), W_k=Z_k-B_k.           (TC2)

At root the fictitious Z=-1 event is folded into stayingroot. Its Y signal can be coupled within those folded outcomes so that the root biased probabilities above remain exact. At nonroot Z=+1/-1 are the two Y0 push/pop paths. This constructs the correct JOINT Y/depth law while W_k remains iid and independent of the previous history. W and Y in the SAME block need not be independent; the proof never assumes that.

Here W is bounded in[-2,1], E[W]=-a, and

    q=Pr(W<=-1)=ab+a(1-2ab)=a(a+2b^2)>0.           (TC3)

Thus the constant reset creates negative depth drift; there is no need to approximate independent root probes with a new log-long reset after each sample.

## TC3. Explicit concentration of root visits

Take r>=4H/a. Hoeffding for the bounded iid W gives

    Pr[sum W_k>-ar/2]<=exp(-a^2 r/18).             (TC4)

Write R_k=-(h_k+W_k)_- for the nonnegative reflection increment. The pathwise identity h_r=h0+sum W+sum R, h_r>=0, implies on the complement of(TC4) that sum R>=ar/4. Since R_k<=2 1_(h_k<=1), the number K of visits to{0,1} is at least ar/8.

Define T_k=1_(h_k<=1)1_(W_k<=-1). Its conditional expectation is q1_(h_k<=1). The martingale sum[T_k-q1_(h_k<=1)] has increments bounded by1. Azuma therefore gives

    Pr[K>=ar/8 AND sum T_k<qar/16]
         <=exp(-q^2 a^2 r/512).                   (TC5)

Every T_k=1 ensures h_(k+1)=0. Counting the final endpoint once at most gives N0=sum_(k=0)^(r-1)1_(h_k=0)>=sum T_k-1. If additionally r>=32/(qa), then except for(TC4),(TC5),

    N0>=qar/32.                                   (TC6)

The signal martingale sum[xY_k-m1_(h_k=0)] has increments bounded by2. On(TC6), classifying the sign incorrectly requires a downward deviation of at least mqar/32. Another Azuma bound gives exp[-m^2 q^2 a^2 r/8192]. Combining all three events, their last exponent being smallest, yields the UNIFORM quantum-classifier error

    eta<=3exp[-m^2 q^2 a^2 r/8192],
    r>=max(4H/a,32/(qa)).                          (TC7)

Tie assignment is arbitrary; the bound covers the larger event x sumY<=0. Every ingredient is a bound on the exact outcome law, which was shown word/depth diagonal. No measurement of the unknown word or seed is implemented in the actual quantum protocol.

Consequently r=O_beta[H+ln(1/eta)+1] three-call blocks suffice. All constants in(TC7) are explicit and can be VERY conservative, especially near endpoints. It is not a small finite-budget claim.

## TC4. Substitute into the clean coherent oracle and word factory

Use the SAME reversible local majority B and C*BC construction as309a. Its operator error is still bounded by

    2sqrt(eta)+L delta_inv+e_B, now L=3r.

Acquire C* by the full-two-sector positive-forward-power inverse. This gives clean X_s XOR, with arbitrary initial label and all ancillas returned, using

    O_beta[(H+ln(1/zeta)+1)^2/zeta] native calls    (TC8)

and the same order of coherent quantum returns for oracle operator allowance zeta. The seed-preserving unknown-word factory then has the corresponding improved bound O_beta[(H+ln(1/epsilon)+1)^2/epsilon], with the exact same complete target and error accounting as309a. Known beta remains supplied/calibrated; the seed/purifier remains unknown and preserved. No arbitrary chosen seed state is prepared.

## TC5. A concrete exact-arithmetic special parameter certificate

At beta=1/2,a=3/4,b=1/4, each three-call depth/counter transition lies in Q(sqrt3) with denominator128. In sector+, at root the Y+/- transitions to root have numerators52+/-24sqrt3; Y0 transitions to depths0,1 have numerators18,6. At nonroot, each Y+/- transition decrements depth or stays with numerators30,10; the Y0 push paths have numerators18,6, and the Y0 pop paths have numerators18,6 except at depth1 where they coalesce into root numerator24. All stated numerators share denominator128.

An exact integer-pair dynamic program can therefore propagate the joint score/depth probabilities for r blocks, verify normalization at EVERY block and compare the exact wrong-label probability to a rational threshold using integer outward brackets for sqrt3. Sector- probabilities are the sign mirror of sector+; including score0 gives a conservative certificate for both. The POVM's depth-diagonal form makes a check over h0=0,...,H sufficient for arbitrary quantum/reference inputs.

At this same parameter, V^3=iI on the FULL native space. Two actual forward V calls implement iV*, with one common sector-independent phase. Thus a clean oracle uses exactly L+2L=9r forward calls and quantum returns, up to a harmless common global phase. The total seed-preserving factory count using two such oracles is18r+T, with18r backward qutrit returns. This is an ideal-model finite-operation certificate, not a hardware calibration claim. Phase/compiler/native errors remain added by their actual invocation counts.

three_call_classifier_exact.py and its exact certificate are the intended finite evidence; new native comparisons must verify the depth/counter kernel against full two-seed sparse circuits before a receipt is claimed. Exact arithmetic certifies its finite Markov polynomial, not historical novelty or physical attainability. The generic coherent-classification/control ideas remain prior; special native priority UNKNOWN; mission NOT_ACHIEVED.
