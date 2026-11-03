# A compatible signed zero-peer return, including mixed signs

Author continuation of NATIVE_SIGNED_RETURN_THEOREM.md and the earned
SOURCE_CONDITIONED_CORE_SWITCH.md. This expands the actual outgoing
operation, not just the definition of its receiving quantity. All statements
below use the SAME current angular receiver Vhat_ang on their stated
zero-gate subregions. Full recurrence remains unproved.

Use the notation and accepted raw w,Sscale=sC,c0 from P1's
angular_gated_global_receiver_bridge.md. Write S_hidden for B+C+E+F and

    Gate(x): Psi(x)-S_hidden(x)>=10(w+5).                (1)

For every stop below, at most10 block events occur, except the last
pointwise operation which uses just one. Both S_hidden and Psi are
core-invariant; one block event changes their difference by at most w+5
in the adverse direction. Thus (1) makes V_ang=V on EVERY actual branch
and full corner halo. Any corner value used is therefore the REAL
F0_ang=F0, not an assumed output law.

## 1. An empty active minority: all peers and all high anchors

Take

    A=a>=3, B=0, C>=max(a+2,R), D=0,

with E,F arbitrary and Gate(x). Stop at the first actual reaction. Core
is truly disabled. There are only the two constant source0 hazards.
The active own input has Delta Psi=-w+2, while the peer input has
Delta Psi<=3 for EVERY hidden peer state and either residual sign.
With p=alpha0/B0,

    E Delta Psi<=p(-w+2)+(1-p)*3=3-p(w+1)<=-5.          (2)

The last bound uses the actual raw w>=4+8B0/b0. Every output is outside
the double-low corner because the original active anchor stays>=3.
The g-anchor terms vanish at input and each actual output: the own gap
dominates its anchor, and a newly born peer anchor1 has h_peer>=1.
Physical time is exactly1/B0 and one noncore event is paid.

Consequently for raw R sufficiently large this is a coefficient-one
Vhat_ang return, with a positive linear-in-M surplus. It does not require
the peer to be pinned or empty AFTER its input: that actual landing is
received immediately.

## 2. A one-molecule minority above anchor4: all peer signs and inventories

Now B=1,C-1>=max(a+2,R), D=0, a>=5; E,F are again arbitrary and Gate(x).
Run until a wrong block event OR the actual I2,I3 prefix completes.
On its successful prefix, the physical landing is

    (a-2,0,C-1,0,E,F),

still with active anchor>=3. Append the first-input operation from
section1. Every wrong event is retained at its real output. No core can
fire before the final peer input because its anchor is zero throughout.

Direct raw factorial division gives I2 then I3 with probability
1-O_raw(1/(C-1)), uniformly in a>=5 and in E,F. Each of these two letters
lowers Psi by1. The appended input has mean gain at most (2). Thus

    E Delta Psi<=-7+O_raw(1/(C-1)),
    J_nc<=3, E time<=3/B0.                              (3)

All g terms remain zero even on the rare wrong-source halo. The squared
workload identity therefore gives the actual common Vhat_ang return
with a linear surplus for R large. This is an UNBOUNDED-active-anchor
operation, not a finite-head fixture.

## 3. The anchor4 terminal-to-corner interface

Take a=4,B=1,C-1>=R,D=0. If the actual I2,I3 prefix succeeds, it lands at

    z=(2,0,C-1,0,E,F) in the double-low corner.

Receive z by its actual F0_ang value. There are at most3 further block
events before its first anchor3. Two cases are earned:

### 3a. Negative peer, unrestricted minority and hot ratio

If F-E>=R, the first own input at z exits the corner with gain -w+2.
A peer input has gain <=-w+2 and leaves one anchor2 and one anchor1.
Apart from the O(1/R) anchor2-source1 event, at most one phase1-source1
can occur, so that latter corner has mean gain<=w+2+O_raw(w/R).
The same constant input race therefore gives

    E_z Delta Psi_corner
        <=p(-w+2)+(1-p)*4+O_raw(w/R)
         =4-p(w+2)+O_raw(w/R)<=-3                     (4)

for R large. Neither E nor the gap ratio is bounded. The I2,I3 prefix
already gave -2 units. Its rare wrong paths have bounded workload
increment and probability O(1/R). Thus the complete actual corner-valued
operation is inward in Vhat_ang.

### 3b. Positive peer, unrestricted minority

If E-F>=R, the first peer input at z has gain +3. At its actual landing
(2,0,C-1,1,E+1,F), source1 at the negative anchor2 is rare O(1/R), by
its exact ratio to source2. A source0 at the positive active peer is
also rare O(1/R), because its source1 hazard is at least cR everywhere.
On all remaining paths, either the negative anchor's source2 exits with
gain<=2, or the positive peer's source1 followed by source1/source2 has
gain -5/-2. Interleavings with a negative input only decrease the gain.
The mean at this landing is consequently <=2+O_raw(w/R). Hence

    E_z Delta Psi_corner
        <=p(-w+2)+(1-p)*5+O_raw(w/R)
         =5-p(w+3)+O_raw(w/R)<=-2.                    (5)

The same completed prefix proves a genuine mixed-sign return, with NO
minority bound in this anchor4 case, subject to Gate(x). All real core
landings and all corner interruptions are included.

## 4. Anchor3: complete negative peer and a mixed activation cone

For a=3,B=1,D=0 and negative gaps C-1,F-E large, the full all-minority
return is NATIVE_SIGNED_RETURN_THEOREM.md. Its exact source-conditioned
switch bound receives the corner's second phase1-source1 branch. Gate(x)
attaches it to Vhat_ang, including arbitrary E and majority ratios.

There is also a true MIXED-sign operation. Put

    n=min(C-1,E-F), F<=eps*n, n>=n0.                    (6)

The constants eps>0,n0 are acquired from the raw list. Both majority
scales and F can diverge. This condition automatically implies Gate(x)
for n large and eps small; it is not a fixed peer inventory.

Use the SAME complete five-state trace and append the ACTUAL corner at
every low-low output. Its two main outputs have gains

    y0=(0,0,C-2,0,E,F): -w-2,
    yp=(1,0,C-1,1,E+1,F): +1,                         (7)

with probabilities p,1-p up to O_raw(1/n). Rare trace outputs are all
included, with bounded workload change and actual corner values.

From y0, the real mixed-sign corner obeys

    E Delta Psi_corner(y0)<=4+O_raw(w/n).              (8)

To verify (8), stop/account for the rare negative anchor2-source1 using
lambda1/lambda2<=C/n, and for any extra positive-peer source0 at positive
anchor using lambda0/lambda1<=C/n. Their genuine counts are bounded by5.
On every other path, ordinary normal phase motion has workload changes
0,3,2-or--1,1 in the positive port, and
0,-w+2-or--w-1,2-or--1,1 in the negative port. At first corner exit their
sum is at most4. An extra negative source0 only reduces this bound; an
extra positive source1 at anchor2 is exactly3 units better than source2.
No core path changes Psi or these parity identities.

From yp, a stronger mixed bound is earned:

    E Delta Psi_corner(yp)<=-2+C_raw,w*(F+3)/n.         (9)

Here is the actual population-controlled argument. Before corner exit,
B_negative+F_positive<=F_initial+3: this sum is CORE-INVARIANT and changes
by at most1 per growth. The positive peer's source1 hazard is >=c n at
anchors1 or2. Thus the probability of a negative-port phase1-source1
(the ONLY +w phase1 event) is <=C(F+3)/n: before the peer's first source1
compare the two source hazards; after that source1 compare with its
still-enabled positive-peer source1/source2 exit. The expected number of
those peer events is<=2. This is an actual compensator comparison over
the moving inventories, not a received neighboring profile.

Positive-peer extra source0 and negative anchor2-source1 remain rare
O(1/n). On every other path, either the negative port takes source0 then
its odd-minority source2 (gain<=-w+1), or the positive peer takes source1
then source1/source2 (gain -5/-2). Any interleaving retained negative
input makes the result smaller. This proves (9), with every conservative
landing and competing path included.

Combining (7)--(9) gives the WHOLE actual workload bound

    E Delta Psi_total
       <=p(-w-2+4)+(1-p)(1-2)+C_raw,w*(F+3)/n
        =-1-p(w-3)+C_raw,w*(F+3)/n.                  (10)

Choose eps after the fixed raw constants, then n0. The right side is
strictly negative, uniformly throughout (6). At most10 noncore events
and physical mean<=10/B0 pay the square and count rewards exactly as in
the negative-peer theorem. The result is a coefficient-one common
Vhat_ang physical return with a positive linear surplus.

## 5. A direct raw zero-peer sector: ANY minority, ANY peer, either own sign

There is an additional generator operation with no activation truncation.
Take

    A>=6, D=0,
    |B-C|>=max(A+2,R_star), Gate(x),                    (11)

with E,F arbitrary. The accepted per-port mixed-sign table from P1's
global_receiver_fusion_positive_cone.md proves, for large raw R_star,

    L_own Psi<=-q_own/4.                               (12)

For a positive own residual, q_own>=3 alpha1 R_star; for a negative
residual with minority>=1, q_own>=6 alpha2(R_star+1). Enlarge R_star so
q_own>=32 beta0 in these fast cases. The peer's only live input has gain
at most3, giving

    L Psi<=-q_nc/8.                                    (13)

In the remaining slow case (negative own residual and B=0), only own
source0 and peer source0 exist. The stronger -w+2 own gain and the raw
choice w>=4+8B0/b0 prove (13) directly.

All one-jump g terms vanish, by the two-unit own residual margin and the
fact that the peer's new anchor1 has h>=1. No one-jump destination enters
the corner: a terminal from A>=6 leaves A>=3. Gate(x) makes the angular
term zero at the input and every neighbor. Thus the FULL raw generator
has, for further enlarged R_star,

    L Vhat_ang
       <=Sscale*(-(Psi+c0)/4+(w+1)^2)*q_nc
       <=-1-q_nc.                                    (14)

The actual FIRST reaction is a noncore reaction because D=0, and its
complete physical/count receiving law follows from (14). No competing
peer channel or future core landing is assigned a free value. This
sector includes mixed signs, separated scales and unrestricted minority
populations, and it meets the other admitted regions in ONE receiver.

## 6. Compatibility and honest remaining domain

Each statement above receives every actual corner or peer output at
Vhat_ang and contains at least one genuine event. They may be added to
P1's physical-time switching menu without a new matching assumption.
The unrestricted native negative theorem outside Gate(x) is retained
only for the previous Vhat; it is NOT silently fused into the angular
receiver near balance.

The remaining complement still includes two active peers at entry,
ready terminal-to-corner states at anchors3..5 in the nonzero angular
region, mixed anchor3 activation with a large relative minority, and
intermediate signed debt patterns not covered by the actual stops above.
Neither the normal-resource finite matrix nor a workload defined on those
states proves their outgoing sign. Full six-species recurrence and the
broader weak-reversibility principle remain open.

The mechanism earned here is the source-conditioned conservative switch
plus actual corner receipt, complemented by raw source-hazard matching.
It develops the signed obstruction into real negative AND mixed return
operations while preserving the correct physical clock and common output.
