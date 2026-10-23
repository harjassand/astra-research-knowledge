# Independent challenge: exact depth law and the compression tail

Reviewer: `/root/stopping_literature`. Date: 21 October 2026.

## Verdict and scope

The proposed critical-input depth law is correct as an exact bounded-observable identity. It includes the exceptional vacuum transition and is valid for every normal initial bath state, with arbitrary coherence. The product-averaged depth is a reflected lazy symmetric random walk. A uniform terminal-depth bound stronger than the requested bound follows without a bath-diagonality assumption.

The type-domination step is valid, provided it is applied to the actual whole-block positive map. The conditioned type input need not itself generate a Markov depth process. For arbitrary normal initializers, their uncontrolled tails must be handled by a direct initialization trace-distance comparison before applying the polynomial type-probability penalty.

This review proves those statements. It does not certify the owner's subsequent code-existence/decoder construction or claim a new capacity converse. No literature search or numerical experiment was needed for this algebraic challenge.

## 1. Exact model and adjoint bath channel

Use the exact two-seed Fock coordinates

\[
E=\mathbb C^2\otimes\mathcal F(\mathbb C^2),\qquad
P_0=I_2\otimes|\emptyset\rangle\langle\emptyset|,
\]

with creation operators \(S_a=I_2\otimes L_a\), \(a=1,2\), and vacuum seed swap

\[
R=X\otimes|\emptyset\rangle\langle\emptyset|.
\]

Let \(L\) denote the word-length operator, independent of the seed coordinate. The exact unitary and its coherent family are

\[
U=\begin{pmatrix}
R&S_1&S_2\\
S_1^*&0&0\\
S_2^*&0&0
\end{pmatrix},\qquad
V_s=\alpha U+i\beta I,
\quad \alpha=\cos s,\quad\beta=\sin s.
\]

The relations used below are

\[
S_a^*S_b=\delta_{ab}I,\quad
\sum_{a=1}^2 S_aS_a^*=I-P_0,\quad
R^*=R,\quad R^2=P_0.
\]

For a diagonal external input

\[
\eta_q=\operatorname{diag}\left(q,\frac{1-q}{2},\frac{1-q}{2}\right),
\quad 0\le q\le1,
\]

define the normal bath channel

\[
\Phi_{s,q}(\tau)
=\operatorname{Tr}_{A}\bigl[V_s(\eta_q\otimes\tau)V_s^*\bigr].
\]

For every bounded bath operator \(F\), expansion of \(V_s^*(I\otimes F)V_s\) gives

\[
\begin{split}
\Phi_{s,q}^*(F)
={}&\beta^2F
+\alpha^2\left[
q\left(RFR+\sum_{a=1}^2S_aFS_a^*\right)
+\frac{1-q}{2}\sum_{a=1}^2S_a^*FS_a
\right]\\
&+i\alpha\beta q[R,F].
\end{split}
\tag{1}
\]

In particular, the coherent term has not been dropped by treating the device as a mixture. It vanishes below for a specific operator reason.

## 2. Closure of every bounded depth observable

Let \(f:\mathbb N_0\to\mathbb C\) be bounded. The following are exact bounded-operator identities:

\[
[R,f(L)]=0,\qquad Rf(L)R=f(0)P_0,
\]

\[
S_a^*f(L)S_a=f(L+1),
\]

\[
\sum_{a=1}^2S_af(L)S_a^*
=f((L-1)_+)(I-P_0).
\]

The first identity holds because \(R\) only exchanges the two length-zero vectors. The creation identity follows on each word basis vector. For the last identity, a nonempty word has exactly one top symbol, whereas both adjoints annihilate the vacuum. Thus the missing vacuum value is supplied precisely by \(Rf(L)R\). Substitution into (1) yields

\[
\boxed{
\Phi_{s,q}^*f(L)
=\beta^2 f(L)
+\alpha^2\bigl[(1-q)f(L+1)+qf((L-1)_+)\bigr].
}
\tag{2}
\]

At the critical input \(q=1/2\), this is exactly

\[
\boxed{
\Phi_{s,1/2}^*f(L)
=\beta^2 f(L)
+\frac{\alpha^2}{2}\left[f(L+1)+f((L-1)_+)\right].
}
\tag{3}
\]

No commutation of the initial state with \(L\), \(R\), or the creation operators was used. The invariant algebra of bounded functions of \(L\) is sufficient: iterating (2), then pairing with any normal bath state, gives the same expectations as the classical kernel. Coherences between words, heights, or seed sectors cannot contribute additional terms to these expectations. This statement concerns the depth marginal; the complete bath state can remain coherent.

For a product external input \(\eta_q^{\otimes n}\) independent of the initial bath, tracing all outgoing ports gives \(\Phi_{s,q}^n(\tau)\). The one-time depth marginal therefore equals that of

\[
Y_{j+1}=\max\{0,Y_j+X_{j+1}\},
\tag{4}
\]

where the independent increments obey

\[
\Pr(X_j=+1)=\alpha^2(1-q),\quad
\Pr(X_j=-1)=\alpha^2q,\quad
\Pr(X_j=0)=\beta^2.
\tag{5}
\]

The initial distribution is \(\Pr(Y_0=\ell)=\operatorname{Tr}(\tau\,1_{\{\ell\}}(L))\). At the vacuum, a downward step remains at zero. No intermediate measurement of the bath is required to obtain this classical representation of its marginals.

## 3. Uniform critical tail bound

Assume \(q=1/2\), \(n\ge1\), and the initial bath state is supported at depths at most \(a\ge0\). This means \(\tau=P_{\le a}\tau P_{\le a}\); arbitrary coherence inside this subspace is allowed.

Couple every process to the same increments. The map \(y\mapsto\max(0,y+x)\) is increasing and one-Lipschitz. Hence

\[
Y_n^{\ell}\le \ell+Y_n^0\le a+Y_n^0
\qquad(0\le\ell\le a).
\tag{6}
\]

Let \(S_k=X_1+\cdots+X_k\), \(S_0=0\). Iterating (4) from zero gives

\[
Y_n^0=\max_{0\le j\le n}(S_n-S_j).
\tag{7}
\]

Reversing the independent, identically distributed increments preserves their joint distribution. Consequently

\[
Y_n^0\overset{d}=\max_{0\le k\le n} S_k.
\tag{8}
\]

For \(\lambda\ge0\),

\[
\mathbb E e^{\lambda X_1}
=\beta^2+\alpha^2\cosh\lambda
\le e^{\lambda^2/2}.
\]

Here \(\cosh\lambda\le e^{\lambda^2/2}\) follows term by term from \((2m)!\ge 2^m m!\). Thus \(e^{\lambda S_k-k\lambda^2/2}\) is a nonnegative supermartingale. Stop it at the first crossing of \(b\) or at time \(n\). Bounded optional stopping gives

\[
\Pr\left(\max_{k\le n}S_k\ge b\right)
\le e^{-\lambda b+n\lambda^2/2}.
\]

Taking \(\lambda=b/n\) and using (6)–(8) proves, for every \(b\ge0\),

\[
\boxed{
\operatorname{Tr}\!\left[
1_{(a+b,\infty)}(L)\,\Phi_{s,1/2}^n(\tau)
\right]
\le e^{-b^2/(2n)}.
}
\tag{9}
\]

The requested weaker bound \(4e^{-b^2/(8n)}\) follows immediately. Equation (9) is uniform in \(s\), the seed sector, and the coherences of the supported initial state. It includes the identity endpoint \(\alpha=0\), where the actual overflow probability is zero.

## 4. What type domination establishes, and what it does not

Take even \(n\) and let \(\Pi_n\) project onto external words with exactly \(n/2\) zero symbols. Each of the remaining positions can contain either 1 or 2. Set

\[
D_n=\binom n{n/2}2^{n/2},\qquad
\sigma_n=\Pi_n/D_n.
\]

Every such word has probability \(2^{-3n/2}\) under \(\eta_{1/2}^{\otimes n}\). Therefore

\[
p_n=\operatorname{Tr}(\Pi_n\eta_{1/2}^{\otimes n})
=\binom n{n/2}2^{-n}=\Theta(n^{-1/2}),
\]

and the exact positive-operator inequality is

\[
\sigma_n\le p_n^{-1}\eta_{1/2}^{\otimes n}.
\tag{10}
\]

For a fixed bath state \(\tau\), evolving all \(n\) inputs through the actual device and tracing the outgoing ports is a positive linear map of the external input. Apply that map to (10), then pair with the positive final-depth overflow projection. If \(\tau\) is supported at depths at most \(a\), (9) gives

\[
\boxed{
\Pr_{\sigma_n,\tau}(L_n>a+b)
\le p_n^{-1}e^{-b^2/(2n)}.
}
\tag{11}
\]

This is an average over the normalized type input, sufficient for a later expurgation argument. It is not a claim that every vector in the type subspace already has small overflow, nor a claim that its depth process remains Markov after conditioning on the type.

For example, choosing initial cutoff \(a_n=\lfloor n^{1/4}\rfloor\) and terminal cutoff \(H_n=\lfloor n^{3/4}\rfloor\) makes the right side of (11), with \(b=H_n-a_n\), decay as \(O(\sqrt n\,e^{-\Theta(\sqrt n)})\). The terminal coordinate projection has rank

\[
\operatorname{rank}P_{\le H_n}
=2\sum_{j=0}^{H_n}2^j
=2(2^{H_n+1}-1)=2^{o(n)}.
\]

### Arbitrary normal initializers

For a general normal \(\tau\), define the comparison state

\[
\tau_a=\frac{P_{\le a}\tau P_{\le a}}
{\operatorname{Tr}(P_{\le a}\tau)}.
\]

For sufficiently large \(a\) its denominator is nonzero. Normality gives \(\operatorname{Tr}(P_{\le a}\tau)\to1\), and purification followed by normalized projection gives

\[
\|\tau-\tau_a\|_1
\le 2\sqrt{1-\operatorname{Tr}(P_{\le a}\tau)}.
\tag{12}
\]

The induced complete external channels satisfy, at every horizon,

\[
\|\mathcal N_{\tau}^{(n)}-\mathcal N_{\tau_a}^{(n)}\|_\diamond
\le\|\tau-\tau_a\|_1.
\tag{13}
\]

This is full trace/diamond norm. It follows by tensoring the bath-state difference with an arbitrary input/reference state, applying the same whole-block unitary, and tracing inaccessible registers. There is no horizon factor.

Apply (11) to \(\tau_{a_n}\), and carry (12)–(13) separately. No rate of decay of the original normal bath tail is assumed. In particular, multiplying that original uncontrolled tail by \(p_n^{-1}\) before separating the initialization comparison could invalidate the argument. The varying comparison state is used in a proof of codes for the one actual fixed initializer; it does not authorize physically reinitializing the bath at each horizon.

## 5. Optional limited obstruction for input bias below the critical value

Fix \(q<1/2\) and \(\alpha\ne0\). The unreflected increments in (5) have strictly positive mean

\[
\mu=\alpha^2(1-2q)>0.
\]

For every starting depth \(\ell\ge0\), reflection only raises the position, so

\[
Y_n^{\ell}\ge\ell+S_n\ge S_n.
\tag{14}
\]

For completeness, a centered variable supported in an interval of length two has log moment-generating function at most \(\lambda^2/2\): its log moment-generating function has zero value and derivative at zero, and second derivative equal to the variance under an exponential tilt, which is at most one. Applying Chernoff's bound to the sum of the centered increments yields, when \(h<\mu n\),

\[
\Pr(S_n\le h)
\le\exp\left[-\frac{(\mu n-h)^2}{2n}\right].
\]

Together with (2), (4) and (14), this proves for every normal initializer, without an initial moment bound,

\[
\boxed{
\operatorname{Tr}\!\left[
P_{\le h}\Phi_{s,q}^n(\tau)
\right]
\le\exp\left[-\frac{(\mu n-h)^2}{2n}\right].
}
\tag{15}
\]

Hence for any \(h_n=o(n)\), the low-depth mass tends to zero, and for sufficiently large \(n\) it is at most \(e^{-\mu^2n/8}\). The case \(\alpha=0\) is excluded: it has no positive drift and keeps the bath fixed.

This closes only the particular strategy of obtaining high average mass in a sublinear-depth coordinate projection under this fixed biased product input. It does not exclude another input family, a different compressible environment subspace, recovery that tolerates an extensive environment, or a rate above \(3/2\). It is not a capacity converse.

## 6. Challenge outcome and observed resources

No algebraic error was found in the critical depth-law premise. The vacuum swap contributes exactly the reflecting boundary term; the coherent interference term vanishes on length observables for a stated commutator reason. Type domination survives the coherent bath, with the limitations identified in Section 4.

Work performed: direct bounded-operator calculation, explicit classical coupling and exponential-supermartingale proof, complete positive-map verification of the type inequality, and a separate biased-input obstruction. No simulation, new source retrieval, additional subagent, or measured runtime-intensive computation was used. The owner retains the main universal compression and coding construction.
