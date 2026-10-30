# Why geometric seed counts do not alone extend the collective Green theorem

30 October 2026. Exact abstract counterexample to a tempting extension; not a counterexample to the accepted chemical family.

Start with n target labels, n divisible by m. Killing has rate kappa(A)_m. A competing seed event has rate c kappa(A)_m and deletes m target labels. All other rank progress/safe/bounded-noise rules are harmless (all surviving labels already have rank0). There are no births. At each effective mark the seed probability is rho=c/(1+c)<1, independently of the current count as long as A>=m.

With probability rho^(n/m)>0, all n/m marks are seeds and no kill occurs. Then A=0 and both rates vanish forever. Thus the killing time tau has P(tau=infinity)>0 and E tau=infinity, despite the exact geometric bound

    P(number of seeds before kill >=j)<=rho^j

for every feasible j (and the usual interpretation on extinction). Every finite-n sample path has finitely many jumps; nonexplosion is not the issue.

A ghost-label extension can still give excellent finite-horizon forcing on the event of few deletions. It CANNOT convert an exponentially unlikely extinction branch into a finite expected killing time without a separately earned finite-head/replenishment return bound. Consequently the fixed-n hypothesis in COLLECTIVE_KILLED_GREEN.md is not cosmetic, and the incoming-grade completion must not be silently combined with geometric seed accounting to claim a whole episode.

In the actual open chemical architecture immigration and restoration may supply such a return, but their time, source and graded output costs must be paid using the existing genuine head mechanisms or newly proved replacements. This note neither denies those prior proofs nor imports them into a new collective module.
