# Recoverable-response-class localization audit

## Verdict

The localization and composition with the mirrored one-sided selector check out under four exact conditions:

1. The tested label $c$ is sampled offline from the ORIGINAL tested prior $\mu_C$, independently of fresh live inputs and the source resource.
2. The Alice row $\alpha$ is an actual orthogonal record of her complete instrument (or a deterministic function of its retained fine records); Bob's checked row $\gamma$ and all live fine outputs are likewise retained.
3. The predicate factors exactly through $k=f_c(\alpha)$, or any failure is null under the complete ORIGINAL preselection output law.
4. The decoder error $e$ is averaged over the complete ORIGINAL preselection law, before either global event or localized event.

Bob's POVM $D_{k\mid c,Y_J}$ is local: it uses the shared offline $c$, Bob's own fresh input $Y_J$, and his actual premeasurement system. Its Lüders isometry followed by Bob's original complete instrument and the factorized acceptance test is one physical Bob-local event. The fresh reverse channel $\mu(x\mid y)$ is unchanged, so the mirrored one-sided theorem applies with the same shared seed included as input-independent shared randomness.

## Coherent localization comparison

Fix $c,Y_J$ and purify the source. After Alice's complete instrument, write the actual dilated state
$$
|\Psi\rangle=\sum_{\alpha,a_J}|\alpha,a_J\rangle_A|\omega_{\alpha,a_J}\rangle_{RB},
$$
with subnormalized residual vectors. Orthogonality of the retained Alice records is essential. Let $k_0=f_c(\alpha)$ and let $D_{k\mid c,Y_J}$ be Bob's complete POVM; complete any sub-POVM with a default guess outcome. Bob physically applies the local isometry
$$
U_D=\sum_k|k\rangle_K\otimes\sqrt{D_{k\mid c,Y_J}},
\qquad U_D^*U_D=I,
$$
retains $K$, then runs his original complete fine instrument. He accepts using $\widehat\theta_c(k,\gamma)$. This sequence uses no fresh Alice input or Alice record and leaves Alice's instrument unchanged and complete.

The ideal comparison vector copies the true row class only from Alice's orthogonal record:
$$
|\Psi_{\rm id}\rangle
=\sum_{\alpha,a_J}|\alpha,a_J\rangle_A|f_c(\alpha)\rangle_K
   |\omega_{\alpha,a_J}\rangle_{RB}.
$$
This is not a physical operation. In one row block the squared difference is
$$
\begin{aligned}
\left\|\sum_k|k\rangle\sqrt{D_k}|\omega\rangle
      -|k_0\rangle|\omega\rangle\right\|^2
&=2\|\omega\|^2-2\langle\omega|\sqrt{D_{k_0}}|\omega\rangle\\
&\le2\big(\|\omega\|^2-\langle\omega|D_{k_0}|\omega\rangle\big),
\end{aligned}
$$
using $\sqrt D\ge D$ for $0\le D\le I$. Orthogonal row/fine-record blocks sum, as do classical input blocks with their ORIGINAL prior weights. Therefore
$$
\|\Psi_{\rm act}-\Psi_{\rm id}\|^2\le2e,
\quad
e=\mathbb E_{\mu_C\mu_J,\ \text{complete preselection source}}
   [1-D_{f_c(\alpha)\mid c,Y_J}].
$$
This is an unconditional decoder error before either event. Replacing it with error conditioned on the original joint event is invalid because postselection can amplify error.

Let $W_{Y_J}$ be Bob's Stinespring isometry for the original full fine instrument, and let $\Pi_{\widehat\theta}$ accept exactly when $\widehat\theta_c(k,\gamma)=1$. The same contraction
$$
C=\Pi_{\widehat\theta}(I_K\otimes W_{Y_J})
$$
acts on both vectors. If
$$
\theta_c(\alpha,\gamma)=\widehat\theta_c(f_c(\alpha),\gamma)
$$
on every supported complete-source row/output block, then $C|\Psi_{\rm id}\rangle$ is exactly the ORIGINAL accepted fine-instrument vector (with an ideal $K$ copy that can be discarded). For original and localized event masses $p,p'$ this gives
$$
|\sqrt{p'}-\sqrt p|\le\sqrt{2e}.
$$
For the live-loss effect $0\le L\le I$, with original and localized selected mean losses $\alpha,\alpha'$,
$$
\sqrt{p'\alpha'}=\|\sqrt L\,C|\Psi_{\rm act}\rangle\|
 \le\sqrt{p\alpha}+\sqrt{2e}.
$$
These are unnormalized amplitude bounds; they do not by themselves bound a conditional table when $p$ is small. If the predicate factorization is only source-null, the nullity must be certified under the full original preselection output law, not only after selection. A nonzero mismatch mass $\eta$ requires an added $\sqrt\eta$ amplitude allowance.

## Mirrored one-sided selector composition

Package Bob's sequence (POVM $D$, original instrument, final local check) as one complete full-string Bob instrument with a Bob-local success sub-POVM. Alice's original complete instrument is untouched. Treat $c\sim\mu_C$ as a shared classical seed sampled before fresh $J$ inputs; because $C$ and $J$ are disjoint coordinate sets in the iid-pair source, $c$ is independent of the fresh pairs. The event may reweight $c$ and $Y_J$, but by Bob locality and completeness of Alice's instrument it cannot reweight $X_J$ conditioned on $(Y_J,c)$. Hence the reverse channel remains $\prod_{i\in J}\mu(x_i\mid y_i)$ after the Bob-local event. Thus the mirrored one-sided theorem applies with
$$
\mu(x\mid y)=\delta\nu(x)+(1-\delta)\kappa(x\mid y),\qquad\delta>0,
$$
on the $m=|J|$ live coordinates, and with the same-model base gap $\epsilon$.

For $t=\sqrt{2e/p}<1$, the amplitude bounds imply
$$
\sqrt{p'}\ge\sqrt p(1-t),\qquad
\sqrt{\alpha'}\le\frac{\sqrt\alpha+t}{1-t},\qquad
\ln\frac1{p'}\le\ln\frac1p-2\ln(1-t).
$$
The mirrored selector therefore yields
$$
\boxed{\displaystyle
\epsilon\le
\left[
\frac{\sqrt\alpha+t}{1-t}
+\sqrt{\frac{\ln(1/p)-2\ln(1-t)}{\delta m}}
\right]^2.}
$$
Equivalently, before substituting the lower bound on $p'$,
$$
\epsilon\le
\left[
\sqrt{\frac{p\alpha}{p'}}
+\sqrt{\frac{2e}{p'}}
+\sqrt{\frac{\ln(1/p')}{\delta m}}
\right]^2.
$$
At $e=0$ and exact/source-null factorization, $p'=p$ and the accepted original fine law is preserved exactly. The decoder and its entire input-dependent POVM family still need to be supplied; no low-$\ln(1/p)/m$ bound implies small $e/p$, and no efficient acquisition or representation bound follows.

## Failure boundaries

- Sampling $c$ from the posterior after the original event would use an event-dependent seed, not the original tested prior. It invalidates the stated preselection error average and can leak tested outcomes into a fresh-round strategy.
- If $\alpha$ is a hidden or nonorthogonal decomposition rather than a checked classical instrument record, the ideal-copy vector is not an available orthogonal-block comparison.
- If $D$ depends on fresh Alice input or outcome, Bob's localization is not local.
- If $\widehat\theta$ fails to reproduce $\theta$ on supported complete-source blocks, the comparison contains an additional predicate-mismatch term.
- A source-null mismatch or $e=0$ preserves the original accepted fine law; a rowwise or postselected small error alone does not.

