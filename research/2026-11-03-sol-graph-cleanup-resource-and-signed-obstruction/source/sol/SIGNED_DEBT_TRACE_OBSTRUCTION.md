# The paid finite trace is not yet a return: an exact signed-debt witness

Keep JOINT_NORMAL_RESOURCE_CAP.md at its actual scope. Its complete
population/clock operator must not be silently turned into recurrence.
The following exact family forces the next missing operation.

Take all block constants1 and any positive core constants (core cannot
fire before this particular trace absorbs). Start at

    x_n=(3,1,n,0,0,n), n>=2.

Use the actual normal-resource trace from that file and its physical
receiver Z=15+M-m(A)-m(D), m=(0,2,4,7,7,...). Here Z_in=2n+12.
Its entire continuing state set has only FIVE states:

    S0=(3,1,n,0,0,n),       Z-Z_in=0;
    S1=(4,2,n+1,0,0,n),     Z-Z_in=3;
    S2=(1,0,n-1,0,0,n),     Z-Z_in=1;
    S3=(2,1,n-1,0,0,n),     Z-Z_in=1;
    S4=(3,2,n,0,0,n),       Z-Z_in=1.

The continuing transitions are respectively I2,I3,I0,I2,I3. The last
I3 absorbs successfully at both anchors zero. A peer input is an actual
failure at ANY state; it is not omitted or continued for free.

The complete genuine rates are

| State | I0 | I1 | I2 | I3 | II0 |
|---|---:|---:|---:|---:|---:|
| S0 | 1 | 3 | 6n | 0 | 1 |
| S1 | 1 | 8 | 24(n+1) | 48n(n+1) | 1 |
| S2 | 1 | 0 | 0 | 0 | 1 |
| S3 | 1 | 2 | 2(n-1) | 0 | 1 |
| S4 | 1 | 6 | 12n | 12n(n-1) | 1 |

All other raw hazards are zero until absorption. Every possible absorbed
output has Z_out-Z_in in {0,1,2,3,4,5,6}; none has a negative value.
In particular S3's own I0/I1 failures have increment0; S2's peer input
has increment1. All terms of the table are retained.

Finite backward substitution proves

    Z_out>=Z_in on EVERY path,
    E(Z_out-Z_in)->1,
    E physical_time ->1/2,
    P(both-anchor-zero success)->1/2.                   (1)

Therefore this trace cannot pay physical return at ANY increasing
function of Z, even after rescaling it or replacing Z^2 by a larger power.
This is not transience: it refutes this stop/receiver pairing, including
its use on a signed packet debt. A later actual stop or a different
receiving geometry may repay it.

The positive-majority progress theorem avoids this family because B-C is
negative. The finite resource cap still applies and earns all moments of
this complete trace; neither fact supplies the missing negative-sign
joint repayment.

The actual next requirement is to receive this debt and its peer-input
branch in one common physical return construction, or to prove a
normalized invariant law. Assigning a receiving law to the peer branch,
calling the finite matrix itself inward, or demanding exponential return
would all evade rather than solve that requirement.

check_signed_trace_obstruction.py computes (1) by exact rational
backward substitution and symbolic limits. The other finite probes in
results/resource_trace_probes.json preserve the actual whole normal trace,
including the 134-state neutral borrowing example. Their scope is
diagnostic, not an all-family recurrence claim.
