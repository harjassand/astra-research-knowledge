# Unbounded seed phases and uniform seeded reset estimates

30 October 2026. Working extensions, not independently reviewed.

## 1. The dormant Green pays an exponential phase budget

The proof of DORMANT_GREEN_NONBALANCED_V2.md applies with

`W_(theta,lambda,alpha)=exp(theta r+lambda B)(1+A)^-alpha`

for every fixed lambda>=0. In its high-A blocks, clearing decreases B and low approaches have bounded B; high activations/immigrations incur only fixed factors exp(lambda(q-1)) and exp(lambda), and remain rare after increasing A0. In the finite-A/high-B leading kernel, the three nonseed endpoints decrease B or leave it EXACTLY unchanged. Thus its weighted powers retain the same geometric factor 1-p. Intermediate and error endpoints have bounded B overshoots, and their O(1/B0) error coefficient remains arbitrarily small. Finite-corner reference rewards have all required exponential A/B moments under product Poisson.

Hence the actual terminal seed law from section B=q pays ANY fixed exp(lambda B_seed) factor while preserving the incoming inverse-A profile. The seed phase is not bounded or discarded.

The same reasoning applies to `(1+r)^j exp(theta r+lambda B) f_alpha(A)`, killed on r<=r0, for any fixed real j. Raise r0 so its residual factor is increasing. Leading head r decrements remain favorable; bounded positive shifts have bounded multipliers; finite A/B corners have r=C+O(1), so their normalized constants are uniform in C. This supplies the polynomial residual enlargements used below without differentiating an already constructed potential.

## 2. The seeded episode has a 1/n time/reset scale

For positive-D input, the s=a0-1 resolvent extension gives

`(b)_q T_+ <= C x^(1-a0)/(x^3+nd) <= C/n`.

For every p>2, the same drift with s=p-2 pays dormant-entry reward f_p:

`V_p=E[f_p(A_out); dormant entrance] <= C x^(2-p)/(x^3+nd)`.

In particular V_m<=C/n and V_(m-1)<=C/n. The full local dormant continuation has time bound C f_m/(b)_q and A-occupation bound C f_(m-1)/(b)_q by the power-spending proof. Therefore the COMPLETE first-connector episode from positive D has

`(b)_q T_full<=C/n`.

For its occupation, if a0>2 take resolvent exponent s=a0-2 to get `(b)_q U_+<=C/n`. If a0=2, take s=1/2: because A<=n+a0, the operational occupation integrand 1/(A-1) is at most C n^(1/2) x^(-3/2). This gives `(b)_q U_+<=C n^-1/2`. Add the dormant continuation using V_(m-1)<=C/n. Uniformly for all a0>=2,

`(b)_q U_full<=C n^-1/2`.

The clearing compensator has bounded integrand `(A)_m f_m(A-m)`. Hence its ACTUAL clearing-output sublaw satisfies

`E[f_m(A_out); clearing first] <= C (b)_q T_full <= C/n`.

These estimates require positive D at input and B>=q; they deliberately do not assert a vanishing mean for an initially dormant state.

## 3. How much initial positive-D occupation is later dormant?

The occupation accumulated after first d=0 entry is at most `C V_(m-1)/(b)_q`. Compare with the reviewed lower U_+ and the displayed V_p:

`U_after_first_dormant <= C x^-1 U_+`.

Thus for large incoming A, first-connector activations occurring in later dormant intervals are a vanishing fraction of the actual activation occupation. For small incoming A their absolute contribution is O(1/[n(b)_q]). This matters when paying the negative activation margin; it cannot be inferred from the probability of ever visiting D=0.

## 4. Finite-grade dormant kernel

For any fixed inverse exponent s and any fixed rare degree j, truncate the dormant phase counters once degree j is reached. Give degree 1 to noncompulsory low immigration, m-1 to high activation, and m to high immigration. The seed-interrupted proof, with its marked generating function and half-A stopping, now proves

`E[exp(theta r_out+lambda B_out) f_s(A_out); accumulated degree>=j] <= C_(s,j) exp(theta r_in+lambda B_in) f_(s+j)(A_in)`

when begun at the section; analogous marked input/output entries retain the phase and counter. Before the half-A stop, f_s(output)<=C A_in^-s and the marked coefficient bound spends j powers. At the half-A stop, use the alpha=s phase-weighted Green with the actual entrance law and its exponentially small TILTED block weight. Bounded incoming A is covered by the actual finite-head Green. Only finitely many degrees are used; there is no assumption that C_(s,j) stays controlled as j->infinity.

These are the needed graded incoming-law bounds for following a seed through an unbounded phase. They do not by themselves prove the whole section kernel or recurrence.
