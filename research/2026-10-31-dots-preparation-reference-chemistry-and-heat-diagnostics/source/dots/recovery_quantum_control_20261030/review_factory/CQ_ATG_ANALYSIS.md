# Joint record/output ATG memory: exact local checks, distance and a confinement obstruction

30 October 2026. New working derivation, not independently reviewed. It neither imports the original Tanner drift nor proves a native memory threshold.

## 1. Actual primary interface

The ATG graph uses alternating X/Z check layers and vertical data connections. Its bulk X measurements leave local parity constraints and record-dependent boundary stabilizers; the encoded Bell correlations involve longer products. These identities are given in Section 3.2, equations 9–16 of [Bergamaschi and Liu, arXiv:2411.04405v1](https://arxiv.org/html/2411.04405v1). Their preparation theorem concerns local stochastic circuit noise and classical feedforward, not the sustained native memory proposed here.

Keep each measured bit as a physical classical register R, using Z_R eigenvalue (-1)^r. Let the code have H_X H_Z^T=0. Odd layers carry Z checks, even layers X checks; unmeasured boundaries are data layers 1 and 2T+1.

The following commuting CQ checks have bounded weight and bounded incidence:

- For a Z check c and even t, the record parity at check locations (c,t-1),(c,t+1), together with data-record locations (i,t) for i in c.
- For an X check c and interior odd t, the corresponding record parity through the adjacent even check layers.
- Bottom boundary: Z_c on DATA times Z_R(c,1), and X_c on DATA times Z_R(c,2).
- Top boundary: Z_c times Z_R(c,2T+1), and X_c times Z_R(c,2T).

A check of base weight w gives bulk weight w+2 or boundary weight w+1. LDPC incidence stays bounded independently of n,T. The ideal post-measurement joint CQ state satisfies all these checks with eigenvalue +1, even when its boundary-only Pauli frame is extensive. Thus there really IS a zero-syndrome starting interface for a NEW joint record/output memory. Its local check potential is not the original single-block Tanner potential.

Long record-dependent Bell-logical relations select a particular protected target inside this local-check space. Their nonlocality is not by itself an objection: logical information in an ordinary code is likewise not fixed by its local checks.

## 2. Explicit sector syndrome matrix

Consider the sector detecting Z errors on boundary DATA. Put H=H_X. There are T+1 data-error vectors d_0,...,d_T in F_2^n: d_0 and d_T are the boundary Z masks, while interior d_j are bit flips in the raw data records at odd layer 2j+1. Let m_1,...,m_T in F_2^{m_X} be flips in check records at even layers 2j.

The violated local CQ checks are exactly

    r_0 = H d_0 + m_1,
    r_j = H d_j + m_j + m_(j+1),  1<=j<T,
    r_T = H d_T + m_T.

Equivalently H_ext = [I_(T+1) tensor H | partial_path tensor I_checks].

The sector detecting X errors uses H_Z and the same formula with T+2 data slices and T+1 check-record edges: its interior data flips are at even layers, with boundary X masks at the endpoints. These are exact binary Pauli/record-flip equations, including actual boundary signs. They are not a new decoding guarantee.

## 3. Local transport gauge and protected logical class

For each temporal edge j and base qubit i, the transformation

    d_(j-1) += e_i,   d_j += e_i,   m_j += H e_i

has zero extended syndrome and weight at most 2+D, where D is the base column-weight bound. It is an actual local transport relation. In the graph-state representation it comes from a graph generator on the intervening data vertex: after recording its X measurement, the unused phase on that classical record is irrelevant. At a boundary, the corresponding factor is the correct X or Z DATA Pauli. These transformations preserve the ideal joint CQ target, rather than demanding an already-computed dense boundary frame.

For any zero-syndrome extended error, summing all rows gives

    H v=0,   v=sum_j d_j.

Transport all d_j to one endpoint using the preceding moves. The zero-syndrome equations force the accompanying m_j to cancel. The remaining error is precisely v on that endpoint. If C_opp is the opposite-type stabilizer row space, the protected relative logical class is

    [v] in ker(H)/C_opp.

Adding opposite-type stabilizers at a slice does not alter this class. Conversely, the local transports and those stabilizers generate every zero-syndrome error with trivial protected class. This is an error-equivalence statement for the known Bell target with classical gauge records, not automatically an unknown-input subsystem theorem for arbitrary coherent record states.

If the base sector distance is d=minimum{|v|:v in ker(H)\C_opp}, the corresponding protected distance of this extended error model is EXACTLY d. Indeed |v|<=sum_j |d_j|<=total error support, and placing a minimum logical v on one boundary achieves d. Thus temporal records need not reduce protected distance merely because logical correlations have long representatives.

## 4. Why the old linear energy confinement fails

Distance alone does not give a drift or a barrier. Let b be a check-space vector. Put d_j=0 and m_j=b on EVERY temporal edge. This vertical record string has local syndrome b at each boundary and zero at every interior check. For singleton b=e_c, it violates only two local checks, independently of T.

Define fill_H(b)=min{|z|:Hz=b}, with infinity if no preimage exists. Any extended error with this same syndrome obeys, at every temporal edge j,

    m_j = b + H(sum_(ell<j) d_ell).

Therefore either some m_j=0, forcing total data support at least fill_H(b), or all T edge vectors are nonzero, forcing record support at least T. Consequently the minimum support of ANY error with these same local check violations satisfies

    reduced_support >= min(T, fill_H(b)).

This lower bound already minimizes over all syndrome-preserving transformations, hence also over the narrower target-preserving gauge. The original string provides upper bound T; two endpoint fills provide upper bound 2 fill_H(b) when finite.

A constant local check-count energy is therefore not uniformly linear in reduced error support when the temporal length and filling cost grow. The obstruction is structural, not a poor decoder choice.

## 5. A hard singleton exists for a nontrivial large-distance CSS sector

Suppose H has full row rank, maximum column weight D>0, and ker(H)/C_opp has a nonzero class of distance d. Choose a minimum preimage z_c of each singleton e_c and form the right inverse R with those columns. Let F=max_c |z_c|.

For each physical coordinate i,

    w_i=e_i+R H e_i

lies in ker(H), with |w_i|<=1+D F. If 1+D F<d, every w_i belongs to C_opp by the definition of sector distance. For any nontrivial logical vector v in ker(H), however,

    sum_(i:v_i=1) w_i = v + R H v = v,

which would put v in C_opp, a contradiction. Hence some singleton has

    fill_H(e_c) >= (d-1)/D.

For linearly growing sector distance and fixed D, the vertical string gives reduced support Omega(min(T,d)) while its local check-count energy remains two. With redundant H, any singleton outside im(H) gives the even simpler lower bound T directly.

This demonstrates why the native theorem's old size-independent linear confinement estimate cannot simply be asserted for the natural spacetime CQ checks. It does NOT rule out a Peierls/cluster analysis, a different energy/potential, a genuinely nonlocal decoding algorithm, protected auxiliary records, or a redesigned higher-dimensional/classical memory.

## 6. Actual next proof obligation

The joint CQ initialization resolves one honest obstacle: the factory output starts in the new local-check zero sector without dense feedforward. The outstanding task is now a memory theorem for the explicit extended syndrome matrices and their record/data error channels. It must handle the low-energy vertical strings, protect the logical class, construct actual bounded-rate corrections and record refresh, and bound continuous joint-bath noise and the eventual readout/feedforward interval.

A factory's one-time clustering theorem is not this sustained-memory theorem. Likewise, the existence of local gauge transport moves is not a native noisy correction law. The derivation supplies a concrete object on which a new law can be built, while exhibiting the precise reason the old Tanner drift does not transfer.

## 7. Executable finite checks

`check_cq_extended.py/json` builds the explicit extended matrix for path-sector examples, verifies every local transport column has zero syndrome, and exhaustively finds minimum-support representatives of the two-endpoint vertical-string syndrome for nine small n,T cases. This verifies the finite algebra, not the general confinement proof or a good Tanner-family decoder. In particular n=6,T=4 has only two violated checks but exact minimum same-syndrome support four.
