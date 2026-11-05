# Literature and second boundary-repair review

Date: 2026-11-05. Independent internal review. No external verification or novelty claim. The earlier proper-parent proof was not modified.

## Results

- The asymmetric one-species PVBS repair coefficient calculation is correct on the whole four-dimensional local code, including arbitrary reference entanglement.
- Tensor-product and local-kernel-equivalent extensions preserve the needed repair structure, provided each factor already has a verified reference-safe repair and uniform open gap.
- Native multispecies PVBS must not be assigned the exact full spectral gap merely from its one-particle mass formula.
- A separate explicit three-state interaction below has unique product bulk, exact periodic gap 1/5, and an exponentially closing open gap. Thus even adding a positive periodic gap to the weak-parent promise does not imply the uniform open-gap input used by the proposed proof. This construction is not a counterexample to LTI completeness.

## Primary literature checked

1. Bachmann and Nachtergaele, *Product Vacua with Boundary States and the Classification of Gapped Phases*, arXiv:1212.3718v3: https://arxiv.org/pdf/1212.3718 . Eqs. (2.1)-(2.2) define the NN projectors. Proposition 2.1 establishes uniform full open-chain gaps when every lambda_i differs from 1. The open ground space has dimension 2^s once the chain can accommodate the s species. Proposition 2.8 and Eq. (2.20) describe the product bulk limit and exponential edge localization; Lemma 2.9 gives an exact ground-vector interval-splitting formula. The sharp mass-gap statement following Proposition 2.1 is expressly restricted to one-particle sectors, not the entire native multispecies Hamiltonian.
2. Fernandez-Gonzalez, Schuch, Wolf, Cirac, Perez-Garcia, *Frustration Free Gapless Hamiltonians for Matrix Product States*, arXiv:1210.6613v2: https://arxiv.org/pdf/1210.6613 . Section 5 constructs gapless weak-parent/uncle models with injective-MPS thermodynamic ground states. This disproves an inference of an open gap from unique injective-MPS bulk data alone; it does not disprove LTI convergence.
3. Targeted searches did not identify a primary-source, one-dimensional, unique-MPS example with positive periodic gap but closing open gap before the direct construction below was derived. The 2D PVBS gapless-edge results do not settle that 1D question. This is a search limitation, not a nonexistence or novelty claim.

## Whole-code asymmetric PVBS coefficient check

For 0<lambda<1 let Psi_L=sum_(x=1)^L lambda^(x-1)|x>, n_L=||Psi_L||, and V_L encode the orthonormal vacuum and Psi_L/n_L. The actual Stinespring map discards the left buffer into its environment, decodes the right buffer, and reencodes the retained qubit using V_(2ell), in physical cyclic order R,L. CP complement/reset branches vanish on the local ground code P.

Set

    alpha=n_ell/n_(ell+1),  beta=lambda^ell/n_(ell+1),
    delta^2=[lambda^2(n_ell-n_(2ell))^2+lambda^(4ell+2)]/n_(ell+1)^2.

The left code-one vector decomposes as

    alpha (Psi_ell/n_ell) tensor |0> + beta Omega_ell tensor |1>.

The right code-one vector, with its untouched neighbor first, is

    [|1> tensor Omega_ell
       + lambda n_ell |0> tensor(Psi_ell/n_ell)]/n_(ell+1).

The ideal right image is Psi_(2ell+2)/n_(ell+1), on untouched-right-neighbor,R,L,untouched-left-neighbor. Its difference from the actual image consists of the joined-mode norm difference lambda(n_ell-n_(2ell)) and the last-neighbor tail lambda^(2ell+1). These are orthogonal, giving delta^2.

For orthonormal input columns (00,10,01,11), squared actual-minus-ideal errors are respectively

    0, beta^2, delta^2, alpha^2 delta^2+beta^2.

The two last-column contributions are orthogonal because their discarded-left environments are the normalized particle vector and the vacuum. The actual right factor has norm one. Hence exactly

    ||(K-K0)P||_F^2 = 2beta^2+(1+alpha^2)delta^2,
    ||(K-K0)P||^2 <= this quantity = O(lambda^(2ell)).

The ideal image is in the full cyclic-region open ground space, tensored with the environment. This verifies an operator/code-subspace estimate, not merely selected-state clustering. Reflection treats lambda>1 using lambda^-1.

Exact finite-buffer erasure to the periodic vacuum is impossible: the normalized open edge state retains a nonzero core occupation under every boundary-only CPTP operation. Its core occupation tends to lambda^(2ell) for a long chain. This is consistent with, and requires, a nonzero exponentially small energetic error.

## Extensions and scope

For a fixed number of layers, h_ref=sum_j a_j h_j, a_j>0, has tensor-product finite ground spaces. Tensoring the reference-safe channels and their ideal comparison maps gives the same exponential estimate by a finite telescoping product bound. Mixed left-/right-binding PVBS species on separate on-site factors cause no problem. Proper injective-MPS-parent factors can be included if their separate repair theorem is accepted.

If h>=0 has exactly ker h=ker h_ref, finite dimensionality gives c h_ref<=h<=C h_ref with 0<c<=C<infinity. All finite open and periodic kernels are unchanged, and the open gap is at least c times the reference gap. The channel and ideal images still annihilate the relevant actual local terms; use the actual norm M=||h|| in the seam estimates. Excited sectors may now interact, so the actual gap is not asserted to equal the decoupled reference gap.

Kernel equality directly fixes all finite-volume kernels and infinite zero-energy frustration-free states. For the strongest C*-algebraic meaning of infinite ground-state uniqueness, retain the intended uniqueness promise explicitly unless an additional identification theorem is provided. The new example below avoids this ambiguity by equality of infinite dynamics with a strict product parent.

## Explicit 1D positive-periodic-gap / closing-open-gap example

This is a direct calculation, not a claim that a cited paper contains the model.

At each site use {|0>,|a>,|b>}. Put q=1/2, lambda_a=q, lambda_b=q^-1, and

    phi_s=(|0s>-lambda_s|s0>)/sqrt(1+lambda_s^2),
    h=|phi_a><phi_a|+|phi_b><phi_b|
        +sum_(s,t in {a,b}) |st><st|.

The six summands have orthogonal ranges, so h is a rank-six projector. It is translation invariant, NN, positive and FF.

### Open kernel and vanishing gap

The open N-site kernel is exactly the span of

    Omega_N,
    Psi_a,N=sum_(x=1)^N q^(x-1)|a_x>,
    Psi_b,N=sum_(x=1)^N q^(N-x)|b_x>.

Indeed, the hopping constraints fix the one-particle amplitude ratios. Every configuration containing at least two particles can be transported through intervening vacancies to an adjacent occupied pair; its amplitude must then vanish because all occupied pairs are forbidden. Thus the kernel dimension is exactly three for N>=2.

Define the orthogonal, normalized two-particle trial vector

    chi_N=Z_N^-1/2 sum_(1<=x<y<=N) q^(x-1+N-y)|a_x b_y>,
    Z_N=sum_(k=0)^(N-2)(k+1)q^(2k).

Every vacuum-particle hopping projector annihilates chi_N. Only adjacent occupied pairs contribute, giving the exact Rayleigh quotient

    <chi_N,H_N^open chi_N>
       =(N-1)q^(2N-4)/Z_N.

Since chi_N is orthogonal to the entire zero-energy space, the positive open gap is at most this exponentially vanishing expression.

### Exact periodic gap and unique product bulk

Let X=diag(0,-3/10,3/10), number=diag(0,1,1), and

    h'=h-X tensor I+I tensor X.

A direct local block calculation gives

    h' >= (1/10)(number tensor I+I tensor number).

For reproducibility, the nine eigenvalues of the difference are

    0,0,0,1/5,4/5,4/5,4/5,4/5,7/5.

Also ker h'=span{|00>}, so h' is a strict product-parent interaction. The coboundary cancels exactly on periodic chains and in infinite-chain dynamics: commutators with any fixed local observable see no endpoint term for sufficiently long intervals. Thus h and h' have the same unique product bulk ground state, while their open spectra differ.

On every periodic N>=3 chain,

    H_N^per(h)=H_N^per(h') >= (1/5)Npart
        >=(1/5)(I-|Omega_N><Omega_N|).

Either uniform one-particle vector attains energy 1/5. Therefore the periodic ground is uniquely Omega_N and gap_per(N)=1/5 exactly.

### Verification and interpretation

`check_boundary_gap_counterexample.py` independently constructs h and h', checks the local inequality, computes full dense spectra for N=3,...,7, and verifies the exact trial-energy expression. Results are in `boundary_gap_counterexample_results.json`. Observed open gaps are approximately 0.2, 0.0550096, 0.0164688, 0.00502067, 0.00151643; periodic gaps are 0.2 throughout. These checks corroborate the algebra, not replace it.

The example defeats a proposed reduction of all positive-periodic-gap weak parents to a uniform-open-gap hypothesis. It does not defeat the existing proper-parent proof, the verified PVBS erasure theorem, or general LTI completeness. The interaction is a periodic/infinite coboundary modification of a strict product parent, suggesting that coboundary robustness of the unrestricted hierarchy is a useful distinct target.

## Gapless periodic branch

For any unrestricted NN LTI dual at level n>=3, positivity gives

    0 <= Tr rho(H_open)^2 <= (n-1)v+2M,

and hence gamma_n>=-2M/(n-1). Combined with gamma_n<=gap_per(N) for N>=2n, this implies gamma_n->0 whenever liminf_(N->infinity)gap_per(N)=0, without an MPS or open-gap assumption. It does not solve arbitrary positive-gap weak parents.

## Follow-on audit: fixed-site reset with a coercive coboundary

The investigator subsequently proposed a stronger argument covering the preceding closing-open-gap example. I checked the following version.

Assume h>=0, h|00>=0, M=||h||, and there are a Hermitian onsite X, a fixed block length k>=2, and c>0 such that

    B_k := sum_(i=1)^(k-1) h_(i,i+1) + X_1-X_k
        >= c(I-|0^k><0^k|).

This block assumption is enough; it is not necessary to assume the individual shifted two-site term is positive. Full LTI gives Tr rho B_k=k-1 on every translated k-site block, since every local h moment is one and the onsite boundary expectation telescopes to zero.

Reset only physical sites 1 and n to vacuum, leaving the entire core unchanged. Put P=Pi_vac^[1,k] Pi_vac^[n-k+1,n], with n>=2k. The periodic boundary contribution after reset has only two active seam terms, each norm <=M. For F=Phi*(H_boundary^2), ||F||<=4M^2 and PFP=0. Positivity implies FP=PF=0, hence

    F <= 4M^2(I-P)
      <= (4M^2/c)(B_k,left+B_k,right),
    Tr rho F <= K := 8M^2(k-1)/c.

No global open-ground compression or bound on Tr rho occurs. The unchanged core has m_c=n-3 bonds, so

    Tr Phi(rho)H_core=m_c,
    Tr Phi(rho)H_core^2 <= m_c v+2M.

The same Hilbert-Schmidt triangle and finite periodic spectral inequality yield

    Delta_n m_c <= [sqrt(m_c gamma_n+2M)+sqrt(K)]^2.

Together with gamma_n<=2M, this gives the explicit comparison

    Delta_n-gamma_n
      <= [2M+2sqrt((2M m_c+2M)K)+K]/m_c = O(n^-1/2).

For n>=max(4,2k) all supports and positive core length are valid. The earlier conservative factor-2 domination also works. The key point is that the LTI coboundary cancellation controls the repair cost without an original uniform open gap. The three-state example has k=2,c=1/10.

## Native multispecies PVBS also has such a finite-block coboundary

This is a direct algebraic extension, not a quoted literature theorem about LTI.

Use the native s-species PVBS projector interaction with lambda_i>0 and lambda_i!=1 for every species. Its phases can be arbitrary as in the source. Put

    alpha_i=lambda_i^2/(1+lambda_i^2),
    Y_0=0,  Y_i=alpha_i-1/2,
    h'=h-Y tensor I+I tensor Y.

The vacuum/species i block has diagonal entries 1/2 and offdiagonal magnitude t_i=lambda_i/(1+lambda_i^2). Its eigenvalues 1/2 +/- t_i are strictly positive.

On the occupied |ij>,|ji> block set x=lambda_i^2,y=lambda_j^2 and

    delta=(y-x)/((1+x)(1+y)).

The original rank-one projector has diagonal x/(x+y),y/(x+y), and offdiagonal magnitude sqrt(xy)/(x+y). The shifted diagonal adds delta,-delta. Therefore the shifted block has trace one and determinant

    delta[(y-x)/(x+y)-delta]
      = (y-x)^2(1+xy) / [(1+x)^2(1+y)^2(x+y)] >= 0.

It is strictly positive when lambda_i!=lambda_j. For equal parameters, the original one-dimensional exchange kernel remains. Same-species |ii> has energy one. Consequently h'>=0, and its local kernel consists only of |00> together with the equal-parameter exchange vectors.

If all lambda_i are distinct, ker h'=span{|00>}, giving k=2. In general let r be the largest number of species sharing the same lambda value; k=r+1 suffices (and k=s+1 always suffices). To see this, a zero-energy basis coefficient cannot contain a vacuum/occupied interface, nor adjacent occupied labels with different lambda values. Thus a nonvacuum word must be entirely occupied by one equal-lambda group. The exchange relations permit every adjacent transposition of distinct species with a nonzero phase. A word longer than the group size has a repeated species; moving the repetitions adjacent forces its amplitude to zero by the |ii> penalty. Hence the k-site h' Hamiltonian has uniquely the product vacuum as kernel.

Finite dimensionality then gives c>0 with

    H_k^open(h') >= c(I-|0^k><0^k|).

Since H_k^open(h')=H_k^open(h)-Y_1+Y_k, this is the fixed-block hypothesis with X=-Y. The fixed-site reset argument therefore covers all native finite-species PVBS models with noncritical parameters, including repeated anisotropies and arbitrary exchange phases. It does not require guessing their exact full gaps or applying the asymmetric erasure separately to interacting species.

### Strong infinite-ground-state uniqueness for the three-state example

For completeness, the strict-parent comparison identifies the full locally stable infinite ground-state set, not only FF states. Let omega be any ground state for h'. A finite interval reset to vacuum is a local CPTP variation; the ground-state condition implies that its energy change is nonnegative. Its two newly exposed boundary terms have norm at most 2||h'|| in total, so the original internal energy is uniformly bounded by that constant. Since h'>=(1/10)(n_left+n_right), the sum of omega(n_x) over all x in Z is finite. In particular omega(n_x)->0 at either infinity. The post-reset boundary energies are at most ||h'|| times the occupation expectations of the two untouched exterior neighbor sites, because the corresponding compressed positive operator annihilates their vacuum. Taking interval endpoints to infinity therefore shows that every fixed internal h' expectation vanishes. The same local coercivity forces omega(n_x)=0 for every x, so omega is the product vacuum. Since h and h' have identical infinite dynamics, this also proves strong bulk uniqueness for h.

The latest computational supplement for the native multispecies coboundary is `check_native_pvbs_coboundary.py` with output `native_pvbs_coboundary_results.json`. It checks five choices, random exchange phases, repeated anisotropies, and the predicted fixed-block unique vacuum kernels. These are finite checks supporting the analytic block-kernel argument.

## Final review verdict (2026-11-05)

I read the completed `COBOUNDARY_REPAIR.md` and `PVBS_EXTENSION.md` after the investigator's fixed-block and full-input reset checks. I found no remaining algebraic gap in the stated nearest-neighbor unrestricted results. In particular:

- The strict-product coboundary assumptions force the onsite X to preserve the vacuum ray, so the asserted shifted vacuum kernel and periodic uniqueness are consistent.
- The sharper K0=4M^2(k-1)/c is valid. The periodic seam annihilates the reset output before the square is evaluated; (A+B)^2<=2(A^2+B^2), followed by vacuum compression of each h^2, gives the whole-input operator bound 2M^2(n_2+n_(n-1)). Full LTI controls both occupations by (k-1)/c. There is no hidden trace bound or open-gap assumption.
- The original native PVBS phase/ratio convention was rechecked directly against arXiv:1212.3718v3, Eqs. (2.1), (2.2), and (2.11). The determinant and equal-lambda kernel proof use those exact signs. `NATIVE_PVBS_EXTENSION.md` now gives a separate complete proof and the five random-phase block checks.
- The single-species asymmetric channel remains independently valid for kernel-equivalent interactions. Its larger tensor-layer extension is appropriately distinguished from the separate native-multispecies coboundary argument.
- The closing-open-gap qutrit example is not an LTI counterexample; the direct repair covers it. Its simple two-particle trial indeed has H_open^2/H_open quotient one, not its exponentially small Rayleigh energy.
- The notes appropriately avoid general weak-parent completeness, restricted-Y completeness, external verification, and novelty claims. The infinite-ground-state wording for the qutrit example is supported by the local-reset uniqueness argument above.

One cosmetic correction was sent to the investigator: the approximate N=6 and N=7 open gaps in the evidence paragraph should match the saved full spectra, 0.0050206654 and 0.0015164292. This does not affect any bound or proof.
