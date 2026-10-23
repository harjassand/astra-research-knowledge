# Independent targeted review: tempered-screen source binding

Reviewer: `/root/safeguarded_mh_mechanism`.
Scientific date: 22 October 2026, Australia/Brisbane.
Review completion UTC: 2026-10-21T16:29:14.785531+00:00

## Reviewed source

- File: `TEMPERED_SCREEN.md`
- Bytes: 14197
- SHA256: `fa0d12398f3b2bbcaa417a591ab70b8ea33e76c4a940b6976c76018fe833f06c`

The separately accepted main source `SAFE_LOCAL_THEOREM.md` remains unchanged
at SHA256 `ad80cb6a4ec919585182ff0fc5210da6643bd9a3378264dace262b6715e9d3da`.

## Verdict

**Theorems 3 and 4, and the nonsharp quantitative consequence (4.3), pass
this internal targeted review under their stated contracts.** No substantive
mathematical gap was found. Historical originality and external acceptance
are not established by this review.

I read the complete actual source, independently checked the proof steps
listed below, and checked the one display correction in the final bytes.
No numerical calculation or trajectory was needed or executed for this
extension. The mechanism notes are in `tempered_screen_challenge.md`.

## Checked obligations

1. Finite positive pi,q; fixed symmetric stochastic Q; fixed K>0,
   0<alpha<1, eta in the stated intervals; proposal initialization;
   fixed kernel throughout each run. Support size may vary in the
   supremum. The arbitrary-measurable-space scope of the main theorem
   is not silently attributed to this tempered construction.
2. Product acceptance reversibility and its monotonicity in eta.
   The Holder pair-sum proof of qL_eta(A)<=q(A)+q(A)^eta uses the
   correct column-sum consequence of symmetric stochastic Q.
3. The power bound is setwise rather than a measure inequality.
   Layer cake and Jensen rigorously propagate it through Markov
   kernels; D_j and r_j follow the displayed recursion.
4. First-hit submeasure domination and its propagation against the
   invariant probability pi retain all later returns to the low set.
   No stopped-law independence or deterministic-time substitution is
   invoked.
5. Density truncation constructs a probability bounded by (V+1)q;
   TV error is at most delta_s, and its extra low-set mass is explicitly
   charged. It is an analysis device, not an unimplemented reset.
6. For every fixed eta>0, the order of choosing fixed h,s,V and then
   sending t to infinity gives uniform zero floor. The final limit
   over the intermediate tolerance is justified; the constants may
   be extremely large.
7. In the near-one interval eta>theta_K, s=ceil(v log log n), the
   r_s lower bound, truncation exponent, first-hit survival exponent,
   propagated-hit bound, B/R choices, core multiplier and high-tail
   coefficient all have the stated uniform orders.
8. Choosing v=zeta/kappa for 0<zeta<min(1,kappa/ell) in the same
   construction gives the nonsharp O(log^-zeta n) risk bound for
   every fixed eta in (0,1), and the stated exponential sufficient
   mixing-time bound. This does not prove a sharp lower rate.
9. Q=I gives the same admitted two-state exact lower family as in
   the main theorem. The matching coefficient and its explicit
   monotone uniform inversion apply within the sufficient interval.
10. The eta=0 floor is inherited legitimately: the old lower family
    already uses positive finite pi,q and a fixed symmetric Q, while
    its old general reversible-kernel upper bound covers this subclass.

## Correction made before final binding

The first version of Section 5 wrote an exact equality
`A^2/t=exp(2(log n)^z)/t` despite A=V+1. I requested its correction to
`A^2/t=exp(2(log n)^z+o(1))/t`, which is present in the above bound source.
This did not change any conclusion; the correction makes the displayed
identity accurate. No failed scientific branch was concealed by it.

## Limits retained

The eta threshold is sufficient, not necessary. The sharp coefficient
for 0<eta<=theta_K remains open. Divergence of the linear domination
ratio is not itself an adverse mixing lower bound. More accepted local
proposals do not prove proposal-start TV dominance or an end-to-end
speedup. Pure IMH already has coefficient K. The full ideal-real error
contract, target normalizer cancellation and actual q access remain
explicit. No new population KL certificate is inferred from observations.

Review resources were direct mathematical inspection and communication.
No new diagnostic execution or external intervention occurred for this
source binding; the original main-theorem diagnostic costs stay separate.
