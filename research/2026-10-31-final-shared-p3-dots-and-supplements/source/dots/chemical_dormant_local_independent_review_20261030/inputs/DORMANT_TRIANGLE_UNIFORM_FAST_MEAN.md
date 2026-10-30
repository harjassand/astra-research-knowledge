# Uniform fast mean away from the dormant D=0 face
Status: personal derivation, unreviewed. Conserved fast/clearing fiber only, not full connector recurrence.

Residual chain:2A'<->A'+D<->C+D, fixed positive rates; killing at k_D(A')_2. Write a=A', c=C, d=D, n=a+c+d. Active means an enabled residual source; fast activity is invariant. Let J=floor(n^(1/8)), K=floor(n^(1/4)). The preserved complex-path lemma gives a crude uniform polynomial mean Cn^M on every active state, so all suprema below are finite without an assumed mixing law.

## 1. Small positive D and the dormant feedback
The proof of SEEDED_D_EXIT_KERNEL_CANDIDATE.md is uniform for initial1<=d<=J if its upper stop is changed to d>=2J. Its low/high-A bounds use only d<=2J. Reaching2J requires at least J D-creating events, whose number before killing is geometrically bounded because creation and killing share propensity(a)_2. Hence, writing M_small for the full clearing mean supremum over1<=d<=J and M_0 over active d=0,

    M_small<=C n^-1/2+C n^-1/8 M_0+Cn^M exp(-cJ).

At active d=0, a>=2. The first event is either clearing with fixed probability p>0 or D creation, which enters d=1; its mean time is <=C. Thus M_0<=C+(1-p)M_small. Solving gives M_0<=C and M_small<=Cn^-1/8.

## 2. An earned growth coordinate near the D-dominant corner
Put R=a+c and S=a+eta c, where eta<1 is sufficiently close to1. Active states have R>=1, and R cannot reach0 under fast reactions. The linear-in-D channels have S jumps +1, -(1-eta), +(1-eta), respectively. Their logarithmic drift is bounded below by

    d/S [c_1 a-C_1(1-eta)a+c_2(1-eta)c]>=c d,

after choosing eta. The2A'->A'+D channel decreases S by1 and contributes at worst -CR. Therefore Q log S>=c'n whenever R<=epsilon n, with epsilon sufficiently small. At fixed large M, stopping the underlying FAST chain when R first reaches2M sqrt(n) gives mean hitting time <=C log(n)/n by bounded stopped Dynkin. Adding clearing only shortens this stage. No stationary A/C fraction is assumed.

## 3. A bounded killed corrector after the reserve has grown
For R>=M sqrt(n), d>=J, use

    w=1+beta c/R,   1<=w<=1+beta.

The2A'->A'+D channel contributes at most C beta(a)_2/R. The A'D->2A' channel decreases c/R. The remaining pair contributes exactly

    beta d [k_forward a/R-k_reverse c/R].

If a<=epsilon R, this is <=-c beta d; the positive2A' contribution is absorbed by a fraction of the clearing killing term for large R. If a>epsilon R, clearing rate(a)_2>=cR^2 dominates the possible O(d) positive linear contribution because R^2>=M^2 n>=M^2 d. Choose M large. The killed generator thus satisfies

    (Q-k_D(a)_2)w<=-c d<=-cJ.

Stop at clearing, d<J, or R<M sqrt(n). Assigning zero at these terminal boundaries only improves the inequality, so the actual mean stage time is <=C/J.

## 4. Crossing the two reserve regions without an assumed barrier
Enter the high stage from R>=2M sqrt(n). The only fast reaction that decreases the UNWEIGHTED R is2A'->A'+D. Before clearing its count has a geometric tail. Thus reaching R<M sqrt(n) before clearing has probability <=exp(-c sqrt(n)). At this exceptional exit the crude polynomial full-fiber mean pays the continuation; its product is negligible. A d<J exit lands at d=J-1 and is covered by M_small.

Any initial state with d>=J and R<2M sqrt(n) first uses the logarithmic growth stage; any initial state with larger R starts directly in the high stage. Hence

    sup_active,d>=J E tau
       <=C log(n)/n+C/J+M_small+Cn^M exp(-c sqrt(n))
       <=C n^-1/8.

Together with section1,

    sup_active,d>=1 E tau<=Cn^-1/8,
    sup_active,d=0 E tau<=C.

## 5. Uniform probability of returning to the dormant face
Starting with d=1, stop at clearing, d=0 or d>=J. The seeded exit estimate gives probability of d=0 at most Cn^-1/8, and the upper exit has probability exp(-cJ), after which its chance of eventually hitting0 is at most1. Thus P_d=1(hit d=0 before clearing)<=Cn^-1/8. From any d>=1, a path to0 must first visit1; strong Markov gives the same bound uniformly over every active positive-D composition.

These are actual fast-fiber means and return probabilities. They do not by themselves control the physical connector's non-small dormant return kernel or prove full network recurrence.
