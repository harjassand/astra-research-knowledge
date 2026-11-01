# Primary-source comparison notes

All prior Astra content was bound to revision
`51ce47ce39f976517d60e2f87bbe280b651f6056`. These wider primary sources were
retrieved in this turn. Citation IDs are supplied to the parent for navigation;
the parent must reopen any source it cites in the final answer.

1. David Aldous and James Allen Fill, *Reversible Markov Chains and Random
   Walks on Graphs*, Chapter 3, Section 3.7.2, Proposition 3.41.
   https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html
   Exact stationary mean hitting-time variational formula for general A,
   including the optimizer 1-E_x tau_A/E_pi tau_A. Read lines 148--156.
   Web refs `turn17view2`, `turn20view0`.

2. A. Bianchi and A. Gaudilliere, *Metastable states, quasi-stationary
   distributions and soft measures*, Stochastic Processes and their
   Applications 126 (2016), 1622--1680, DOI 10.1016/j.spa.2015.11.015.
   https://arxiv.org/pdf/1103.1143
   Definition 2.8 introduces soft capacities using dangling conductances
   and a killed-process interpretation. Read PDF pages 8--9.
   Web refs `turn17view0`, `turn18view0`.

3. A. Bianchi, A. Gaudilliere and P. Milanesi, *On soft capacities,
   quasi-stationary distributions and the pathwise approach to metastability*,
   Journal of Statistical Physics 181 (2020), 1052--1086,
   DOI 10.1007/s10955-020-02618-9.
   https://arxiv.org/pdf/1807.11233
   Section 2.3, Definition 2.9, Eq. (21), admits overlapping sets.
   Taking R=A, S=whole space, kappa=infinity, lambda=s recovers the
   screened Dirichlet functional in the reversible construction exactly.
   Its objective is metastability asymptotics, not plainly the current
   fully paid finite statistical algorithm. Web refs `turn17view1`,
   `turn18view2`, `turn20view1`.

4. A. Gaudilliere and C. Landim, *A Dirichlet principle for non reversible
   Markov chains and some recurrence theorems*, Probab. Theory Relat.
   Fields (2014), preprint https://arxiv.org/pdf/1111.2445 .
   General nonreversible capacity, adjoint hitting potentials and
   variational principles are established machinery. Definitions and
   identities (2.3)--(2.6) were read. Web ref `turn29view0`.

5. L.-J. Huang and Y.-H. Mao, *Variational principles of hitting times for
   non-reversible Markov chains*, J. Math. Anal. Appl. 468 (2018).
   Primary author slides:
   https://math0.bnu.edu.cn/probab/Workshop2018/Lectures/July%2016-afternoon/6-Huang.pdf
   Search output explicitly states a nonreversible variational formula for
   E_pi tau_A using both primal and adjoint mean potentials. Full paper was
   not acquired in this branch. Web ref `turn29search39`.

6. J. Loper, G. Zhou and S. Geman, *Capacities and efficient computation
   of first-passage probabilities*, Phys. Rev. E 102, 023304 (2020),
   DOI 10.1103/PhysRevE.102.023304.
   https://journals.aps.org/pre/abstract/10.1103/PhysRevE.102.023304
   Explicit strong comparator: local simulations around rare targets
   estimate long-time first-passage probabilities. The requested output
   is target choice probabilities rather than the exact stationary-start
   mean considered here. Abstract/search metadata were acquired; a full
   theorem-by-theorem comparison remains necessary before priority claims.
   Web refs `turn21search0`, `turn21search24`.

7. M. Baudel, A. Guyader and T. Lelievre, *On the Hill relation and the
   mean reaction time for metastable processes*, SPA (2023),
   https://arxiv.org/abs/2008.09790 and author's full paper
   https://perso.lpsm.paris/~aguyader/files/papers/bgl.pdf .
   Strong comparator for source-sink flux, entrance distributions and
   bias from replacing the correct entrance law by quasi-stationary laws.
   Introduction and Theorem 5.6 were subsequently read. That theorem
   controls relative bias using quasi-stationary relaxation and one-step
   escape quantities, rather than plainly giving the present stationary
   start screening comparison. Full theorem comparison remains unfinished.
   Web refs `turn21academia25`, `turn21search26`, `turn33view2`, `turn35view1`.

8. D. Aldous, *Probability Approximations via the Poisson Clumping
   Heuristic*, Chapter B, especially B17--B19, B29--B31.
   https://www.stat.berkeley.edu/~aldous/Book2/book.pdf
   This is the most direct older computational idea. It uses the stationary
   outward-flux exit law and the short-term probability f_A of not returning
   to A to estimate E_pi tau_A approximately as 1/(J f_A). B19d writes
   the corrected rate as sum_y flux(A,y) f_A(y). The treatment includes
   coarse sets and nonreversible queueing examples. The heuristic already
   identifies the target-boundary recrossing correction and local simulation
   opportunity; merely using that correction is not new. Read lines
   2011--2044, 2169--2183, 2542--2575. Web refs `turn39view0`, `turn40view0`.

9. P. Mathieu, *Hitting times and spectral gap inequalities*,
   Ann. Inst. Henri Poincare Probab. Statist. 33(4) (1997), 437--465.
   https://www.numdam.org/item/AIHPB_1997__33_4_437_0.pdf
   Explicitly permits non-symmetric processes; uses Laplace equilibrium
   potentials and gap/Dirichlet energy bounds to control hitting-time
   transforms and exponential approximation. Section IV, Proposition 6,
   pages455--456; Theorem7 page459. Those formulas required screenshots
   because OCR omitted math. Web ref `turn44view0`, screenshot refs
   `turn46view0` through `turn46view3`. This is close prior machinery;
   it was not found to state the exact present finite nonrev CDF bound.

10. P. Flajolet and R. Sedgewick, *Analytic Combinatorics*, TheoremIX.5.
    Author-hosted source https://algo.inria.fr/flajolet/Publications/book.pdf
    Targeted retrieval explicitly gives the smoothing constants 1/pi
    for the integral over [-T,T] and 24||G'||_infinity/(pi T), citing
    Feller volumeII,p538. Search ref `turn47search27` and author-site
    Princeton copy `turn41search5`. Full PDF open exceeded service size
    limit, but the exact theorem was retrieved by targeted search.

11. Aldous--Fill, Chapter3 section3.5.4, Proposition3.23.
    https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S5.html
    For reversible chains, stationary hitting-time CDF is uniformly
    within tau_rel/E_pi tau_A of the exponential with the same mean.
    That is stronger than the O(delta log(1/delta)) general nonreversible
    Fourier certificate in its reversible subcase. Web ref `turn43search2`.

## Scope of originality presently supportable

Do not claim invention of capacity, soft killing, adjoint potential theory,
reactive flux, the flux-weighted short-term no-return correction, local
target simulations, or learning local Markov rates.
The current candidate addition is the particular finite, gap-relative
two-sided nonreversible screening comparison, its direct positive
recrossing realization, its lower success probability, and the complete
composition with acquired reversible/directed-cycle parameter uncertainty.
No exact prior match was found in this bounded search, which is not proof
of historical novelty. No general physical or computational advantage
over all equally informed ordinary algorithms has been established.
