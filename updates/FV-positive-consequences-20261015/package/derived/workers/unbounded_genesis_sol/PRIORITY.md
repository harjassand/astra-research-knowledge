# Primary-source comparison and scope

Checked 2026-10-15. Exact priority of the radius theorem remains **UNKNOWN**. Searches that found no exact predecessor do not establish novelty.

The mathematical contract under review is one scalar probability law satisfying
\[
\widehat M(s,t)=\widehat\nu(s,t)e^{i(sA+tB)}
\]
for every real Fourier parameter and every state, for the full infinite separated-block pair. It is stronger than separately specifying noisy coordinate marginals.

1. **R. F. V. Anderson, Weyl calculus; W. J. Ricker (1997).** Ricker's [The Weyl functional calculus and two-by-two selfadjoint matrices](https://doi.org/10.1017/S0004972700033980), Bull. Austral. Math. Soc. 55, 321-325, was acquired in full. Printed pp. 322 and 324 were also visually inspected. Page 322 attributes a sphere formula to Anderson 1969, Theorem 4.1; pp. 323-324 derive the derivative of the projected sphere measure. Thus the disk kernel and distributional derivative mechanism in Section 2 of PROOF.md are established machinery, independently reconstructed here. Ricker's theorem concerns order zero versus commutativity for a finite matrix pair. It does not state a common scalar regularizer, infinite-gap coupling criterion, or an exact exponential-moment radius.

2. **R. Schwonnek and R. F. Werner (2020).** [The Wigner distribution of arbitrary observables](https://arxiv.org/html/1802.08342), J. Math. Phys. 61, 082103, was acquired in full HTML. Read Sections II, III.2, III.8 and IV.2, plus the concluding discussion. The definition explicitly starts with bounded operators. The paper treats Fourier ordering, compact support, positivity, nearly commuting pairs, and the qubit disk singularity. Its final discussion lists unbounded and infinite-dimensional analysis as further work. It supplies close finite-block context, not the infinite-family radius classification proved here.

3. **R. Sabbagh, O. Movilla Miangolarra, H. Hezari and T. T. Georgiou (2025).** [Particle approximations of Wigner distributions for arbitrary observables](https://arxiv.org/html/2409.19206), Phys. Rev. Research 7, 013102, was acquired in full preprint HTML; the [published primary record](https://doi.org/10.1103/PhysRevResearch.7.013102) was checked. Its standing setup is finite dimensional, and its principal results construct signed discrete approximations to the Weyl distribution using symmetrized orderings. This does not decide existence of a single positive scalar regularizer across unbounded energy gaps.

4. **Anderson's original papers.** The [1970 publisher abstract](https://www.sciencedirect.com/science/article/pii/0022123670900509) was checked: its stated results concern connected support and order-zero/commutativity. Full original 1969/1970 articles were not acquired in this worker. The Ricker attribution is primary evidence for the sphere mechanism, but is not a substitute for a complete theorem-by-theorem review of Anderson's originals.

Relevant prior internal capital was inspected at the specified Git pin: the FU arbitrary convex moment-domain proof and FU weighted noncompact proof. Neither is a premise of this result. Their norm-interior interface does not directly cover the whole unbounded tuple here. This comparison is an assessment of applicability, not a claim that no stronger external theorem exists.

Known pieces are Weyl ordering, Pauli/sphere kernels, analytic-element terminology, slow radial potentials, Schur complements and direct-sum POVMs. The candidate contribution is the matching **sufficiency** for the exponential-gap obstruction: a common smooth radial strictly log-concave law with exact open moment ball, including its critical radius, on an infinite noncommuting family. It neither claims a new kernel nor presents ordinary phase-space Gaussian smoothing as new.

Source bytes and hashes are in sources/ACQUISITION.json. The older PDF and visual review images are preserved under sources/. Finite symbolic checks establish their displayed arithmetic scope; they are not external review or formal proof. No historical first-result claim, efficient compiler, information advantage or physical implementation follows.
