# Raw coverability words give an actual polynomial shell clock

This is an acquired ordinary-method construction toward the full recurrence target. It is not advertised as a new coverability algorithm, historical novelty, or a completed weighted recurrence argument.

## 1. Exact finite acquisition from the raw list

For a reaction y->y' and an upward target basis vector b, the least enabling predecessor that can reach a state >=b in one firing is

    pre_(y->y')(b)=y+(b-y')_+.

Start from the finite target antichain B0. Repeatedly add all such predecessors and remove every vector dominated by another basis vector. The increasing upward-closed reachability sets stabilize by Dickson's lemma. Every new basis vector carries its actual reaction followed by the previously acquired witness word. This is the standard exact backward coverability construction; no finite-state truncation or guessed reachability oracle is used. Its actual antichain/bit cost is paid, with no efficient bound claimed here.

The fixed point B recognizes U=Pre*(up B0) exactly. Let L be the maximum stored word length, increased to one if needed. For EVERY x in U a dominated basis vector supplies a word of at most L enabled actual reactions leading to the target. Monotonicity of enabling preserves that word under a nonnegative translation. The word may change ANY inventory; none is frozen or reset.

For a weakly reversible raw list, U is forward invariant. If x in U makes a physical jump to z, a translated complex return path takes z back to x, and then the existing word reaches the target. Thus every actual competing jump that has not already hit the target leaves a state with an acquired word. This is the exact role of weak reversibility here.

## 2. The physical clock on a moving shell

Let N=|x|_1 at the attempt's start. Stop at the upward target or at exit from the actual shell N/2<=|X|_1<=2N. Write

    D=max_e |y_e|_1,
    kmin=min_e k_e>0,
    S=sum_e k_e,
    qmax(N)=S max(1,2N)^D,
    delta0(N)=min(1,kmin/qmax(N)),
    delta(N)=delta0(N)^L.

While unstopped, an available witness edge has rate >=kmin because enabled falling-factorial products are positive integers. Total physical activity is <=qmax(N). Thus the conditional chance of following a chosen witness word for at most L jumps is >=delta(N). If that word exits the shell first, the stopped attempt has already ended. After any other block of L jumps, forward invariance of U supplies another acquired word. Hence the number of blocks before the stopping time is dominated by a geometric law with success probability delta(N).

At every unstopped state an enabled witness edge gives total rate >=kmin. Actual holding times have mean <=1/kmin; counting jumps as time would be incorrect. Consequently

    E_x tau <= L/[kmin delta(N)],
    E_x J_tau <= L/delta(N).                              (1)

Both are explicit polynomials in N for the fixed raw network and acquired finite witness set. Competing transitions, moving hidden coordinates and shell exits are included in tau. This is not a stationary fiber or a spectral-gap statement.

The same construction pays tails. Since the embedded path and independent unit exponential holding variables can be sampled separately for fixed autonomous rates, each block duration is dominated by a sum of L independent exponentials of rate kmin. For 0<s<kmin put M(s)=(kmin/(kmin-s))^L. Restarting at failed blocks gives

    E_x exp(s tau) <= M(s)/[1-(1-delta(N))M(s)]             (2)

whenever the denominator is positive. For example s=kmin delta(N)/(4L) works. The jump-count analogue follows by geometric blocks. For any nonnegative actual running reward bounded on the shell by Fmax(N), (1) gives E integral_0^tau F(X_s) ds<=Fmax(N)L/[kmin delta(N)]. No normalized tilted law is used.

If the start is centered in a shell wide enough to contain every state of its acquired word, the first block also gives a quantitative lower bound delta(N) for reaching the target before shell exit. This lower bound need not be close to one.

## 3. Why this is not yet a recurrence proof

The target may be the banked fixed-width bulk, but classes with conserved small pools may never cover it. They must be handled rather than silently discarded. Even on bulk-coverable classes, a shell stop can be an outward exit. A polynomial attempt clock and a probability N^(-P) of hitting the bulk do NOT establish a finite global return time: successive outward exits still need a compatible inward weighted renewal inequality. A polynomial-clock argument that omits this obligation would not complete the programme.

The genuine next diagnostic is therefore the weighted exit operator, with physical time and the chosen bulk return reward carried together. The exact word construction earns its local clock and accessibility inputs. It does not supply the sign of that operator.
