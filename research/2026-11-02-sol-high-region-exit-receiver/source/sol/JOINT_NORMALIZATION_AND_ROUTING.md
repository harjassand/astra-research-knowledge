# Joint normalization: exact assets and the remaining composition problem

Author derivation. This is not a completed recurrence proof. The completed
predecessor directories remain unchanged.

For block i write a_i for its anchor, r_i=B_i-C_i, t_i=min(B_i,C_i),
o_i=t_i mod 2, and

    k_i=|r_i|+ceil(t_i/2),
    h_i=|r_i|+3t_i/2+o_i/2,
    f_i=a_i-h_i,    g_i=max(f_i,0),    K=sum_i k_i.

These variables are acquired directly from the four source complexes
0, AB, 2A+B+C, 3A+2B+2C. A conservative pair transfer changes donor h by-3
and recipient h by+3, and preserves K exactly. Also k_i<=h_i<=3k_i.
Consequently total population is at most sum_i g_i+7K. The function

    sum_i eta_i g_i^2+C(K+c)^2                         (J1)

is proper for all positive eta_i,C,c. Properness alone is not a return law.

## High-anchor maximal-source normalization

While every participating anchor is at least3, choose the terminal source
when t>=2, source2 when t=1, source1 when t=0 and r>0, and source0 otherwise.
Every chosen block step preserves f_i exactly. A terminal reduces K by1.
An activation step with nonzero r and the source2 preparation preserve K.
Only source0 at r=t=0 introduces a new unit of K. Every core step preserves
the sum of the f_i, but transports three units between individual f_i.

For a normalization without additional empty inputs, while the anchors stay
at least3 and the hidden inventories are drained completely, direct count
identities give

    #activation0/1=sum|r_i|,
    #source2=sum|r_i|+sum o_i,
    #terminal=sum t_i/2+sum|r_i|+sum o_i/2,
    delta(sum a_i)=-sum|r_i|-3sum t_i/2-sum o_i/2.

The core may interleave arbitrarily. These are path-count identities, not a
claim that the displayed policy is the full actual process or that it drains
before an anchor reaches2.

## A real failure when low anchors are admitted

The finite graph in normal_form_graph.py overapproximates arbitrary peer
supplies. Its unbounded negative-pair-difference warning has an actual
two-block realization. Start

    (A,B,C,D,E,F)=(1,2,c,1,2,2), c>=2.

Take I1, I2, core I->II, I2, I3, core II->I. The successive states are

    (2,2,c+1,1,2,2), (3,3,c+2,1,2,2),
    (3,1,c,1,4,4),   (4,2,c+1,1,4,4),
    (1,0,c-1,1,4,4), (1,2,c+1,1,2,2).

All channels have strictly positive raw rates, and all chosen block sources
are maximal enabled sources at that moment. The path can be repeated and
pumps C. It does not prove transience: every competing raw path still has to
be paid. It does disprove deterministic boundedness of this normal policy.
The same example shows why high-anchor normalization cannot simply be
continued through its low-anchor boundary.

## A global core-charge inequality above the donor activation threshold

Let Q=sum eta_i g_i^2 and consider a directed core transfer i->j, with
rate kappa_ij a_i a_j u_i, u_i=(B_i)_2(C_i)_2. Its change satisfies

    delta Q<=6 eta_i g_i-6 eta_j g_j+9(eta_i+eta_j).     (J2)

If this is positive, then g_j<=C_eta(a_i+1). Hence

    a_j<=g_j+h_j<=C_eta(a_i+K+1).

The positive generator contribution of that transfer is therefore at most

    C_raw a_i^2(a_i+K+1)u_i.                           (J3)

If a_i>=3, its own terminal has rate alpha_i3(a_i)_3 u_i and leaves g_i
unchanged while reducing K by1. Since (a_i)_3>=2a_i^3/9 and K>=1 when
u_i>0, a sufficiently large fixed C in (J1) pays (J3) from at most half of
that terminal's negative C(K+c)^2 generator contribution. Sum over finitely
many core ports and choose C once. This works for arbitrary hidden counts,
pair differences and other anchors. It is a raw-source inequality, not an
assumed favorable core transport law. It does NOT pay core moves whose donor
anchor is1 or2, nor all nonterminal block moves.

## Routing of a ready packet

For two ports at fixed anchors a,d>=3 the transfer/terminal ratios are

    q_I=2d/[alpha_3(a-1)(a-2)],
    q_II=a/[beta_3(d-1)(d-2)].

The two-hop product is O(1/(ad)), even when one first transfer is almost
certain. Thus one must analyze the joint service path rather than require
each donor terminal to beat every transfer.

More generally, on a fixed finite port graph with all anchors>=L, a transfer
to a port whose anchor is no larger than the donor has probability <=C/L
relative to terminal service. A strictly increasing-anchor path visits at
most the number of ports. Thus the routing chain of one ready packet has a
uniform geometric bound in blocks of that many service events, for L large.
This statement freezes the anchors only for its stated finite routing chain;
an actual chemical episode must also pay anchor changes and every competing
growth reaction. No infinite-rate limit is used or asserted.

## Axis geometry changes the receiver decision

Starting on the double anchor axis (a,0,0,d,0,0), a normal I preparation,
transfer to II and II terminal can return at (a+3,0,0,d-3,0,0).
The total anchor is unchanged. Its squared sum therefore cannot value the
equalization. A weighted sum eta_1 a^2+eta_2 d^2 can.

At large fixed anchors, the leading one-packet transfer intensities are

    c_1 d/a^2, c_2 a/d^2,
    c_1=2alpha_0/alpha_3, c_2=beta_0/beta_3.

Their leading quadratic transfer drift is nonpositive if
eta_2/eta_1=(c_1/c_2)^(1/3). This is a leading-order diagnostic, not a
uniform all-path estimate. Growth interruptions, finite-jump terms, multiple
packets and the low-anchor receiving boundary remain obligations.

A simpler globally defined candidate that preserves every actual core step
exactly is total_population^2+gamma(A-rD)^2 with r=(c_1/c_2)^(1/3), plus
acquired low-source profiles if needed. It can value a completed anchor
transfer while allowing the physical preparation debt to be repaid later.
No choice of gamma or full output contract has yet been proved successful.

The present new leverage is the joint routing/core-charge structure. The
remaining operation is an actual return construction that pays the low-anchor
boundary and all interrupted preparations at the same proper receiver.
