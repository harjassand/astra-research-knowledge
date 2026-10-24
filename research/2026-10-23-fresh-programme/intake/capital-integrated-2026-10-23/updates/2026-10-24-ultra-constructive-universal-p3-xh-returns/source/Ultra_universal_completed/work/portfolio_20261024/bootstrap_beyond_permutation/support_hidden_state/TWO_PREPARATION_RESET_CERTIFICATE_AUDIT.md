# Audit: two-preparation rank-two reset certificate

Scope: audits the sharper two-preparation construction supplied in the
current task. It is distinct from the earlier general OOM/LP analysis in
`RESET_CERTIFICATE_AUDIT.md`. The result is an observable-behaviour reset
certificate under a full rank-two controlled action/outcome interface; it
does not claim to reset a latent physical state or return to the original
initializer.

## Completeness from two actual preparations

Let the empty continuation be normalized to probability one, let (G) be a
binary future event, and use predictive coordinates
\[
 x=(1,p),\qquad p=\Pr(G).
\]
Assume the rank of the **full controlled action/outcome Hankel space** is at
most two. If two actually prepared states have (p_0\ne p_1), the two rows
\((1,p_0),(1,p_1)\) are linearly independent, so the rank is exactly two
and they span the entire predictive row space. This is a completeness proof,
not a latent-state reconstruction.

For every legal finite future adaptive-event test (E), its probability is
linear in predictive coordinates and hence has the form
\[
 f_E(p)=a_E+b_Ep.
\]
Because it is an event probability, (f_E(p_i)\in[0,1]) for (i=0,1).
Writing (g=p_1-p_0\ne0),
\[
 |b_E|=\frac{|f_E(p_1)-f_E(p_0)|}{|g|}\le\frac1{|g|}.
\]
This bound uses the two *actual* preparations and the fact that the test is
bounded. It does not assume all points between (p_0,p_1) are reachable.
For any physical input state, (p\in[0,1]), so its distance from the
reference preparation is at most one.

## Nonselective mixture theorem

For a fixed nonselective macro word (u), the induced map on the complete
rank-two predictive space is affine:
\[
 p\longmapsto b_u+d_up.
\]
The affine property follows because the macro is a fixed trace-preserving
controlled operation with all internal outcomes averaged; its action on
unnormalized predictive functionals is linear, and normalization fixes the
first coordinate. For the measured event (G), its contrast between the two
actual preparations is exactly
\[
 \Delta_u=f_G(S_u(p_1))-f_G(S_u(p_0))=d_u g.
\]
For a fresh private random choice of macro, independent of the incoming
history, with fixed probabilities \(\lambda_u\ge0,\sum_u\lambda_u=1\),
the averaged map has slope
\[
 d=\sum_u\lambda_ud_u=\frac{\sum_u\lambda_u\Delta_u}{g}.
\]
Let (S\) denote that averaged operation and take the target to be the
*actual* state (S(\rho_0)), where ρ₀ is one of the reproducible
preparations. For every physical input (p\in[0,1]) and every legal future
event (E),
\[
 |f_E(S(p))-f_E(S(p_0))|
 =|b_Ed(p-p_0)|
 \le\frac{|\sum_u\lambda_u\Delta_u|}{|g|^2}.
\]
Thus the stated denominator is (g^2\), not (g\): one factor converts the
measured G-contrast to the macro slope, and the second bounds the slope of
an arbitrary future event. The same inequality holds for every finite
adaptive future event in the promised full action/outcome continuation
space. Taking the supremum over events gives a total-variation bound on
future behavior **provided those event tests are in that full space**.
It is uniform over all reachable histories because every physical history
has a coordinate (p\in[0,1]).

The exact result depends on nonselectivity: the complete macro must be a
trace-preserving operation, with failure/death branches retained as outcomes
or included in the physical state. If the macro is conditioned on a success
record or on survival, normalized predictive updates need not be affine. A
history-dependent stopping/abort event can also leak information unless
completion time and all side channels are fixed independently of the
internal outcomes. The private key and withheld outcomes are essential to
the stated observation interface.

## Finite-frequency certificate

Suppose every raw probability frequency used for the two preparations and
for every predeclared macro (u\in U) is within (w) of its true value on
one simultaneous confidence event. Set
\[
 \widehat g=\widehat p_1-\widehat p_0,\qquad
 \widehat\Delta_u=\widehat q_{1,u}-\widehat q_{0,u},\qquad
 g_{\rm low}=|\widehat g|-2w.
\]
Then \,\(|g|\ge g_{\rm low}\), and
\(|\Delta_u-\widehat\Delta_u|\le2w\). For any data-dependent
\(\lambda\) on the simplex, simultaneous coverage over the whole
predeclared library gives
\[
 \left|\sum_u\lambda_u\Delta_u\right|
 \le\left|\sum_u\lambda_u\widehat\Delta_u\right|+2w.
\]
Consequently, if (g_{\rm low}>0\),
\[
 \epsilon_{\rm beh}\le
 \frac{|\sum_u\lambda_u\widehat\Delta_u|+2w}{g_{\rm low}^2}
 +2\rho_{\rm mix},
\]
where \(\rho_{\rm mix}\) bounds total-variation distance between the intended and implemented word-choice laws. The factor 2 covers both preparations; validate the implemented law directly to set this term to zero. Adaptive choice of λ is safe only
because the frequency error event covers every predeclared (u); a
post-selection library requires fresh validation or a uniform bound over
that larger library. For finite-bit implementation, either use exactly
sampleable dyadic weights and validate that implemented mixture, or include
the implementation-law error explicitly; changing a word-choice law by
total variation rho can change a two-preparation contrast by up to 2rho.
Keep all support words at the same completion time and hide the fresh key.
For Bernoulli outcomes, (N\) predeclared settings,
and (n\) independent trials per setting, Hoeffding gives the simultaneous
radius
\[
 w=\sqrt{\frac{\log(2N/\alpha)}{2n}}
\]
with failure probability at most α. If \(g_{\rm low}\) is small, the
certificate correctly becomes weak; rank two alone does not provide a gap.
If the fitted contrast is zero, then achieving target ε requires roughly
\(w\lesssim \epsilon g_{\rm low}^2/2\), so the validation repetitions scale
as \(O(g^{-4}\epsilon^{-2}\log(N/\alpha))\) in the small-error regime.

All of these frequencies must be measured from actual reproducible starts.
An estimate of the contrast after (u) requires both preparations,
execution of (u), and measurement of (G). Charge both initializer calls,
word durations, measurement, and validation. Equal macro completion times
avoid a timing leak. Any amortization against the expensive initializer is
separate. The target is (S(\rho_0)), not ρ₀; if the downstream
objective requires the original state, this certificate does not meet it.

## Sharp interface counterexample: revealing the private key

Take a binary hidden state with (p\in\{0,1\}), event (G) equal to the
state bit, and two nonselective words: identity (I:p\mapsto p) and flip
\(X:p\mapsto1-p). Let the two actual preparations have (p_0=0,p_1=1),
so (g=1). Their contrasts are \(\Delta_I=1\) and \(\Delta_X=-1\).
The equal mixture has \(\sum\lambda\Delta=0\) and maps every physical
predictive state to (p=1/2): it is an exact reset when only the averaged
post-word behaviour is visible.

If the selected word key is disclosed, the *joint* future interface is not
reset. Starting from (p=0), the joint (key, next G outcome) is
\((I,0)) or \((X,1)); starting from (p=1), it is \((I,1)) or
\((X,0)). These distributions have total-variation distance one. Thus
“private key/outcomes withheld” is a mathematical assumption about the
observer, not an implementation detail that can be dropped. If the key is
revealed after the fact, the observer can condition on it and the averaged
contrast certificate no longer describes that enlarged interface.

A second boundary is postselection. For a filter that succeeds with
probability (\epsilon\) on state 0 and probability one on state 1, the
conditional update is
\[
 p\longmapsto\frac{p}{p+\epsilon(1-p)},
\]
which is nonlinear in (p). Contrasts of the normalized success branch do
not determine the nonselective map; success probability and failure/abort
records must remain part of the tested outcome interface. The stated proof
avoids this by requiring nonselective words, withheld internal outcomes,
and fixed completion time.

## Verdict

Under the literal rank-two full-interface, nonselective, private-key,
fixed-completion assumptions, the algebraic all-history/all-finite-event
bound is valid, with the exact (g^{-2}) scaling and the stated raw-frequency
robustification. Its main acquisition gate is obtaining a confidence lower
bound on the true gap (g); small (g) makes certification costly or
vacuous. The result does not provide a reset word, guarantee a low-cost
positive mixture exists, return the original initialization, or account for
the total amortized benefit.
