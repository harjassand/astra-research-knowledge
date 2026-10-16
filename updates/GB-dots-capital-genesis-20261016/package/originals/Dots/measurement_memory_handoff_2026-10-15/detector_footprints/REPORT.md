# Exact complete detectors for the acquired [[33,1,4]] code

2026-10-15. All check/qubit indices below are zero-based. This is exact matrix algebra, not a noisy-circuit simulation or hardware feasibility result.

## Main result

A single check's support A is correctable, but measuring only that check does not eliminate all nonstabilizer Pauli operators supported in A. Among the existing 40 checks:

| Target A | Number of targets | Minimum detector checks | Minimum union D of detector data supports | Correctable minimum detector sets |
|---|---:|---:|---:|---:|
| Weight-4 check support | 32 | 7 | 14 qubits | 64 of 128 per target |
| Weight-5 check support | 8 | 9 | 18 qubits | 0 of 7,200 per target |

The weight-5 targets are X8–X11 and Z0,Z1,Z18,Z19. Each weight-4 target has 108 distinct minimum-set unions, 58 correctable. Each weight-5 target has 2,733 distinct unions, none correctable. Exhaustive enumeration covers 61,696 minimum sets and 25,320 target/union pairs. A valid logical witness is stored for every uncorrectable union.

The 14/18 minima optimize union size over ALL sufficient subsets of the existing checks, not merely over the examples chosen here: every sufficient subset contains a restricted-row basis, and removing extra detectors cannot enlarge its union. The same argument shows that no larger sufficient detector set can rescue correctability for a weight-5 target. These minima do not cover synthesizing other stabilizer products as different physical measurements.

There is NO nonempty self-contained region D for this code satisfying the same full-Pauli, zero-good-support certificate with all detector supports contained in D. This is a limitation of this certificate, not an impossibility theorem for noisy QEC.

## Exact criterion and minimality proof

Work modulo Pauli phases. Let R_X and R_Z be the check row spaces, each rank 16. For any A, define local stabilizer dimensions

s_X(A) = 16 − rank(H_X restricted to A-complement),
s_Z(A) = 16 − rank(H_Z restricted to A-complement).

For a selected subset G of existing checks, the dimension of supported Paulis centralizing G is

2|A| − rank(G_X restricted to A) − rank(G_Z restricted to A).

All local stabilizers already lie in that centralizer. Consequently the required inclusion

Pauli(A) intersect Centralizer(G) ⊆ phase S_code

holds exactly when this dimension equals s_X(A)+s_Z(A). Because A is correctable, using all checks already achieves equality. Therefore G is sufficient exactly when its restricted X rows span the full restricted H_X row space and its restricted Z rows span the full restricted H_Z row space. This is the direct sum of two binary linear matroids. Minimum cardinality is the sum of their ranks, achieved by any pair of bases.

For an X-check weight-w target, ranks are (w,w−1); for a Z-check target, (w−1,w). Thus minimum count is 2w−1. Exhaustively enumerating combinations of the nonzero restricted rows lists every minimum set. For weight 4, the basis counts are 16×8; for weight 5, 160×45, with the type order exchanged for Z targets.

For each expanded D, exact correctability is tested using

logical_X_dimension(D) = |D| − rank(H_Z restricted to D) − s_X(D),
logical_Z_dimension(D) = |D| − rank(H_X restricted to D) − s_Z(D).

Both must vanish. This covers mixed Paulis: any logical X(x)Z(z) has a nontrivial pure component on the same support. Logical witnesses are commuting vectors outside the relevant stabilizer row space. The script independently checks both properties; it first uses weight-4 logicals when available, otherwise finds a witness by nullspace elimination. A returned larger witness is not claimed minimum-weight.

## Explicit smallest detector reservations

Target X0 has A={0,4,8,16}. A minimum complete set is

G_X={X0,X2,X4,X12}, G_Z={Z2,Z6,Z10}.

Its union is D={0,2,4,6,8,9,10,12,16,18,20,25,27,29}, of size 14, and D is correctable. Correctability of D does not mean these same seven checks are complete on D. They are complete only on the original four-qubit A.

An equally small but uncorrectable choice replaces X4 by X16, retaining the other six checks. Its D={0,4,6,8,9,10,12,16,17,18,25,27,29,31} contains Z logical {8,9,16,17}.

Target X8 has A={0,1,24,25,27}. A minimum complete set is

G_X={X0,X1,X8,X10,X12}, G_Z={Z0,Z2,Z3,Z6}.

Its minimum-size union is D={0,1,2,4,5,6,8,9,10,11,16,17,18,24,25,27,29,31}, of size 18. It contains Z logical {8,9,16,17}. Every other sufficient existing-check choice also has uncorrectable union, by exhaustive minimum-basis enumeration and monotonicity.

For Z0, a minimum union uses G_X={X0,X2,X4,X8}, G_Z={Z0,Z2,Z4,Z10,Z12}, and contains X logical {8,10,12,14}. The full per-target lists and examples are in results.json.

## Why fully noisy support closure cannot succeed here

### General dimension obstruction

Suppose all measured stabilizer detectors G are supported entirely in D and the same inclusion is required on all Pauli(D). Put d=|D|, r=rank(G), and s=rank(S_code intersect Pauli(D)). Then r≤s≤d because these are commuting Pauli spaces. Centralizer dimension is 2d−r, so completeness requires

2d−r ≤ s ≤ d, with r≤d.

Necessarily r=s=d. Thus the code fixes a unique pure stabilizer state on D and factors across D versus its complement. Ordinary entanglement-bearing memory regions cannot meet this condition. This argument permits arbitrary code stabilizer detectors, not merely the supplied 40 rows.

### Code-specific exact no-factor certificate

There is a simpler independently checkable certificate ruling out every nonempty D here. Any original stabilizer h restricted to D centralizes G: every g is supported in D, so its commutation with h|D equals its commutation with h. Completeness would therefore make every h|D itself a code stabilizer. In particular, all restricted original X/Z checks must commute:

for every x in HX and z in HZ, (x AND z) dot indicator(D) = 0 over GF(2).

There are 112 nonempty X/Z intersections, all of size two. Their incidence matrix has rank 32 on 33 vertices. Equivalently, the graph joining each such pair is connected. The only indicators satisfying these equal-membership constraints are the empty and full set. Full D is impossible because the code has k=1 and nontrivial logical operators. Therefore no nonempty self-contained complete detector region exists.

Starting from a weight-4 check support, propagating these necessary fixed-point equality constraints yields region sizes 4→15→31→33; from a weight-5 support, 5→25→33. These are NECESSARY fixed-point closures, not a measurement protocol or a claim that any actual chosen detector expansion has those intermediate supports.

For a concrete detector-expansion example, the minimum correctable X0 construction above expands 4→14. Completing detectors again on that 14-qubit footprint with an explicitly stored greedy row basis expands to 28 qubits with both X and Z logical dimensions one. The exact basis and witnesses are in results.json. This illustrative path is not the no-go proof; the connected-overlap certificate covers all choices.

## Meaning for the unread-measurement theorem

The theorem's A is the entire weak-noise/error footprint being certified, whereas D here is the union of physical DATA supports touched by its chosen detector measurements. Even D excludes ancillary qubits, resets, couplers, transport, and duration. Those require a real circuit specification.

With an A-only weak perturbation, the 7/9 exact syndrome checks certify the required local-centralizer premise. But that application treats detector backaction as the stipulated exact full-joint pinching, with fresh isolated reservoirs and no feedback, and must account for detector support/time in the geometric reservation. Ignoring readout does not idealize measurement backaction or remove these resources.

If arbitrary detector faults instead enlarge the perturbation footprint to D, the A-only result is insufficient. Weight-5 detector unions already contain logicals. Weight-4 detector unions can be correctable, but that alone does not make the selected G complete on D. Repeating the same full-Pauli, zero-good-support closure cannot yield a nonempty self-contained region in this code.

This does not say only physically noiseless detectors could ever work. It says the current A-only proof requires its exact boundary-channel assumption or a separate justified treatment of additional faults. Flagged circuits, separately charged measurement-fault events, restricted physical fault sets, or good sectors allowed to retain correctable errors could change the theorem. None is supplied or validated by these matrices. No hardware feasibility, time/rate, threshold, or experimental logical-error claim is made.

## Reproduction and provenance

Run `python check_complete_detectors.py` (or supply a matrix-directory argument) with standard-library Python. No author software, packages, or network execution is used. The script reads only the two acquired matrices and writes its own results beside itself.

The matrices were previously matched entry-for-entry to Appendix B of the primary paper: https://arxiv.org/html/2408.08865v2#A2 . Source matrices are checks-as-rows (20×33 each).

SHA-256:
- HX_33.json: c3b1a7b92ff093559c439a34b4cad34d1ed6e61e80fc0166570667baa89d39a4
- HZ_33.json: 8698befcf87017ff96b2e9a07dfd89e14a636d1d80c2bc50e6a85d49fd4eb830

Artifacts: check_complete_detectors.py; results.json (40 targets, exact minima, examples, closure chains); all_minimum_detector_unions.json (25,320 exact union/witness certificates). The small explore.py was an initial own exploratory calculation and is not required for reproduction.
