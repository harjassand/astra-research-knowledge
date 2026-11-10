ROOT MATHEMATICAL COMPOSITION: SYMMETRIZED NOMINAL LYAPUNOV CONTROL PAYS ACTUAL FIRING ACTIVITY
10 November 2026 Brisbane. A general nominal sufficient lemma, not existence of its Lyapunov function for every network. It extends the reversible ground-state composition to the correct virtual symmetrisation, while retaining the physical graph and costs.

Let Q be a nonexplosive countable-state nominal CTMC with strictly positive invariant probability pi on its actual class. Let a(x)>0 be its total labelled firing rate, including zero-change channels if any, and assume pi(a)<infinity. Define the stationary adjoint off-diagonal rates
 qstar(x,y)=pi(y)*q(y,x)/pi(x),
and Qs=(Q+Qstar)/2. Keep each zero-change labelled channel at its original rate. Stationarity gives sum_(y!=x)qstar(x,y)=sum_(y!=x)q(x,y), so Qs has exactly the SAME total labelled activity a(x). It is reversible for pi and
 E_pi,Qs(f,f)=E_pi,Q(f,f)
by swapping x,y in the stationary-flow sum. These are algebraic identities, not an assumption that Q itself is reversible or that a perturbed chain preserves pi.

SUFFICIENT LEMMA. Suppose the ORIGINAL Q has the accepted physical Poincare inequality Var_pi(f)<=g E_pi,Q(f,f). Suppose there is a positive proof function H and set C such that
 Qs H/H<=-ell*a outside C,
 Qs H/H<=a everywhere,
 a<=A_C on C,
with computable bounds ell^-1,A_C,g. Then
 sum pi*a*(f-pi f)^2
 <=[ell^-1+A_C*(1+ell^-1)*g]*E_pi,Q(f,f).
Proof: use the reversible ground-state inequality for Qs on f-pi f. The outside contribution is at least ell times its activity-weighted variance, the inside contribution is bounded below by -A_C Var_pi(f), and Qs has the same Dirichlet form as Q. Add the inside activity variance and invoke the original physical gap. Clipping/Fatou give the natural form-domain extension. Polynomial numerical-parameter bounds and polynomial binary evaluation of ell^-1,A_C,g imply the corresponding computable polynomial activity-gap bound.

The HYPOTHESIS is drift for Qs, not merely drift for Q. A one-sided Lyapunov estimate for the original nonreversible generator is not silently sufficient. Qs and its extra transitions are used only to prove an inequality of the ORIGINAL Q; no virtual rate or edge is emitted by the physical compiler and no virtual event is substituted for a charged physical firing.

EXACT MASS-ACTION FORMULA WITHOUT A NORMALISER OR CLASS ORACLE. For the actual conditional-Poisson target pi_lambda(x) proportional to lambda^x/x!, an original labelled channel y+w->z+w with rate coefficient kappa has adjoint channel
 z+w -> y+w, coefficient kappa_star=kappa*lambda^(y-z).
Indeed at x>=z+w,
 [pi(x+y-z)/pi(x)]*kappa*(x+y-z)^falling(y+w)
 =kappa*lambda^(y-z)*x^falling(z+w).
The conditioning normaliser cancels exactly, including rare classes. The exponent y-z is fixed and independent of catalyst w. The virtual adjoint/symmetrized coefficients are ordinary rational expressions with fixed input exponents. Weak reversibility and graph preservation ensure that these endpoint populations already lie in the same actual class via original return paths; no new ACTUAL communicating class or reachability oracle is supplied. Virtual reverse edges need not be legal physical edges and remain proof devices.

Thus a designer may investigate graded confinement of the explicit nominal symmetrisation while retaining the original physical realisation. Its weighted inequality, if proved with the required bounds, is exactly the nominal criterion used in136C for all physical independent-rate errors. Whether such a graded construction and Lyapunov bound exist for every fixed weakly reversible R remains OPEN. The old uniform-menu trapping clock still fails the criterion; symmetrisation does not repair a bottleneck already present in a reversible example.

SOURCE/OVERLAP. This is an algebraic composition with the accepted nominal physical gap and136C activity criterion, not a second proof of the full robustness theorem. The reversible lemma in ROOT_POLYNOMIAL_ACTIVITY_GAP_ALL_ACTIVITIES_TRAP_20261110.txt10526/SHA0d15f1849b5e4f0ce80bd87ad585654c31b64940f63cf83b57c972e667aaae22 remains valid as written; this note specifies the additional Qs-drift hypothesis that permits nonreversible use. The latter note's complete all-activity graded trapping example is unchanged. No unread primary source, held transfer, free stationary-density oracle, new physical species/model/resource or source/access workaround is used. Current scientists retain their full questions and autonomy; all known/unknown holds and existing team/cadence/resource protections apply.
