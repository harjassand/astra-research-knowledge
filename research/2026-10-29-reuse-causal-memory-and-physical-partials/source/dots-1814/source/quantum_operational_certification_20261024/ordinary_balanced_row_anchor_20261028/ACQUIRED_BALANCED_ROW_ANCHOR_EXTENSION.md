# Acquiring the balanced row anchor from ordinary counts

28 October 2026. New construction candidate; independent receiving pending. This is a separate extension of the received exact rank-one row theorem, whose source and receipt remain unchanged. It removes the SUPPLIED LOCATION of the balanced anchor, not the actual known receiver basis, exact row-rank-one structure, or quantitative existence promise. It does not use the separately pending near-rank-one extension.

## 1. Interface and result

Use all physical and comparator conventions of `BALANCED_RANK_ONE_ROW_ANCHOR_ACQUISITION.md`: a stationary reset source, known linear four-real-coordinate encoder, an ACTUALLY AVAILABLE known k-dimensional output register/basis, ordinary six-state loss-state preparations T_x on d=2k coordinates, and unrestricted full-CPTP recovery. Every T_x is the actual normalized positive loss density, with

    ell(x,C)=(3/2)Tr(C^T T_x), 0<=C<=2I.

The exact row promise is

    (T_x)_ii=lambda_i (u_i^T x)^2,
    sum_i lambda_i u_i u_i^T=I_4, sum_i lambda_i=4.

Zero rows are allowed; all nonzero masses and real unit directions are unknown. A valid loss-state rank bound r<=d is supplied as in the received theorem, for example r=min(d,3R) from encoded Choi rank R. The output basis is not obtained by a generic unknown random compression, which need not preserve this promise.

Replace the supplied anchor by the following weaker information:

**Existence promise.** A rational number 0<kappa<=1/4 is known, and there exists an UNKNOWN x_* in S^3 such that

    |u_i^T x_*|^2>=kappa                         (1)

for every nonzero row. No algorithmic access to x_* is supplied. This is not a good-code or low-loss promise. There is still no minimum row mass or source spectral floor.

For 0<gamma,epsilon<=1, the construction below has ideal expected Bell loss

    E ell_selected <=(1+gamma/2)ell_star+epsilon/64,     (2)

where ell_star is the optimum over the entire declared encoder sphere and all CPTP decoders. One subsequently used privately framed payload, with one paid whole-process implementation discrepancy at most epsilon/2, has actual unhalved complete error at most

    min{2,(1+gamma)Delta_star+epsilon}, Delta_star=2ell_star.

The deterministic source cap is

    O_tilde((d+dr)/(kappa gamma epsilon))+1
       <=O_tilde(k^2/(kappa gamma epsilon))+1.          (3)

The count pilot uses the same 20 distinct ordinary settings as the received theorem. Only ONE additional encoder setting is selected adaptively and queried as a quantum state bank. All encoder nets below are classical processing, not physical query menus. Equally informed conventional protocols may implement this same learner with the same receiver resources.

## 2. Count pilot and high-count retention

Use the received finite fourth design: four axes each with probability 1/12, and the 16 sign vectors (±1,±1,±1,±1)/2 each with probability 1/24. Its actual ordinary records (x,i) satisfy

    Pr(i)=lambda_i/4,
    E[xx^T | i]=(I_4+2u_i u_i^T)/6.                  (4)

Let beta_t=beta_q=epsilon/256, and choose an integer

    L>=max{1,log(64d/beta_t)},
    N=ceil[2^43 d L/(kappa gamma epsilon)],
    T=ceil[2^18 L/kappa].                            (5)

Take exactly N pilot calls, including all outcomes. At each row with actual count n_i>256L, compute the same finite rational top unit vector v_i and observed-gap certificate as in the received theorem; its numerical vector error is at most sqrt(L/N)/100. Keep row i only when n_i>=T and its certificate passes. Call the retained set I. No row below this threshold is divided by its observed count or inferred to have zero mass.

The received conditional-moment and binomial proof gives a single event G_t, of probability at least 1-beta_t, on which:

1. Every high-count row passes the gap certificate and has projective error e_i=sin^2 angle(u_i,v_i)<=256L/n_i. For low-count rows set the accounting error e_i=1.
2. If N lambda_i/4>=8L, then n_i>=N lambda_i/8.
3. The weighted direction bound is sum_i lambda_i e_i<=4096 dL/N.

These are conditional-on-realized-label-sequence concentration statements, not replacements of rare actual counts by their expectations. Their proof and finite eigensolver are imported from the unchanged received source and independent receipt.

On G_t, every retained row satisfies e_i<=kappa/1024, so an optimally signed representative obeys

    min_{s=±1}||s v_i-u_i||<=sqrt(2e_i)<sqrt(kappa)/16.  (6)

The sign is only for the proof; the algorithm never needs it. Also the total discarded selector mass Lambda=sum_{i not in I}lambda_i obeys

    Lambda<=8dT/N<=2^22 dL/(kappa N).                   (7)

Indeed a discarded row with Nlambda_i/4>=8L has lambda_i<=8n_i/N<8T/N. Each remaining row has lambda_i<32L/N<=8T/N. The last bound uses T<=2^19L/kappa, which includes the integer ceiling. Thus rare and missing rows are explicitly paid, not assumed absent.

## 3. Finite search for an acquired anchor

Build a rational sphere net of chord radius at most sqrt(kappa)/16. One explicit construction is as follows. Choose a power-of-two M with M^2 kappa>=4096, minimal with that property. In each of eight signed-coordinate stereographic charts, enumerate the three rational parameters t_j in [-1,1] on the mesh 1/M and use

    q(t)=(2t_1,2t_2,2t_3,1-||t||^2)/(1+||t||^2),

with the chart's coordinate permutation and sign. Every vector is exactly rational and unit. A point of S^3 has a signed dominant coordinate at least 1/2; the corresponding inverse parameters are in [-2/3,2/3]^3. Rounding them changes their norm by at most sqrt(3)/(2M), while the chart map is 2-Lipschitz. Thus this finite grid covers S^3 to radius at most sqrt(3)/M<sqrt(kappa)/16. Its size is O(kappa^(-3/2)), with polynomial bit length. The search has no dependence on an exponentially large numerical coordinate range.

Choose the first grid point x_0 satisfying all of the exact rational inequalities

    |v_i^T x_0|^2>=9kappa/16, i in I.                 (8)

If none exists, or a required certificate fails, take a fixed physical fallback policy. On G_t such a search succeeds: a grid point within sqrt(kappa)/16 of x_* has every retained estimated overlap at least

    sqrt(kappa)-sqrt(kappa)/16-sqrt(kappa)/16
      =7sqrt(kappa)/8>3sqrt(kappa)/4.

Any selected x_0 then has true retained overlaps at least

    |u_i^T x_0|>=3sqrt(kappa)/4-sqrt(kappa)/16
       =11sqrt(kappa)/16>sqrt(kappa)/2.                (9)

Thus the acquired anchor is genuinely kappa/4-balanced on the retained rows. The existence promise need not be algorithmically certified from finite data. The guarantee is conditional on that model promise and G_t. A bad record still returns a physical fallback; no success probability is divided out.

## 4. Dropping rare rows is a task-risk approximation, not a deployed measurement

Let P be the known diagonal projector onto the retained coordinates of the loss-state register. It is used in the proof and in forming a positive predictor; no measurement of the payload output in this basis is imposed.

For any actual purification Psi_x of T_x,

    ||Psi_x-P Psi_x||^2=Tr[(I-P)T_x]
       =sum_{i not in I}lambda_i(u_i^T x)^2<=Lambda.    (10)

Consequently every full-CPTP decoder satisfies the uniform root-loss comparison

    |sqrt(ell(x,C))-sqrt((3/2)Tr(C^T P T_x P))|
       <=sqrt(3Lambda).                              (11)

This uses the actual positive quadratic loss functional and its norm at most 3. In particular it retains and pays ALL lost cross-block coherences by a purification norm; it does not replace the source by an uncharged pinched channel. P acts on the auxiliary loss-state representation and need not define a legal payload decoder operation.

The exact positive-polynomial quotient from the received theorem applies to the retained principal submatrix. Define, only on I,

    r_i(x)=(u_i^T x)/(u_i^T x_0),
    shat_i=v_i/(v_i^T x_0), rhat_i(x)=shat_i^T x,

and put rhat_i(x)=0 outside I. With R_x supported on I,

    P T_x P=R_x P T_x0 P R_x.                         (12)

Every used estimated denominator has magnitude at least 3sqrt(kappa)/4, and ||Rhat_x||<=2/sqrt(kappa) on every record passing (8). The true retained denominator is nonzero by (9). The sign ambiguity of v_i cancels in the ratio.

Write a=u_i^T x_0, b=v_i^T x_0 and w_i=lambda_i a^2. Align v_i's sign only for the proof. Then

    w_i ||v_i/b-u_i/a||^2
      =lambda_i ||a v_i-bu_i||^2/b^2
      <=8lambda_i e_i/b^2
      <=16lambda_i e_i/kappa.

The first inequality uses ||a v_i-bu_i||<=2||v_i-u_i|| and ||v_i-u_i||^2<=2e_i. Thus uniformly over every x,

    sum_{i in I}w_i |rhat_i(x)-r_i(x)|^2
      <=2^16 dL/(kappa N)=:E_row.                    (13)

The improved denominator in (8) is what avoids a second balance loss in this bound. Neither (7) nor (13) divides by lambda_i.

## 5. One fresh actual anchor bank and a compatible root bound

After the pilot and anchor choice have been frozen, acquire exactly n_0 fresh actual copies of T_x0 in the SAME known physical output basis. Set

    m=kappa gamma epsilon/2^22,
    D_0=nextpow2(dr),
    n_0=ceil[(80D_0/m)log(12D_0/beta_q)].              (14)

The received ordinary Bures query returns a physical density tau with root fidelity f(T_x0,tau)>=1-m except probability beta_q, conditional on every fixed pilot history. Uniformity of the actual rank bound and this conditional guarantee justify averaging over the data-selected anchor; a mixture of iid banks is not replaced by the tensor power of its average.

Define

    T_hat_x=Rhat_x tau Rhat_x.                        (15)

It is positive and quadratic in real x, but is not asserted normalized, TP, or a valid source Choi completion. One purification of the ACTUAL T_x0, projected to its retained rows and multiplied by R_x, purifies (12) simultaneously for all encoders. A single Uhlmann alignment of tau with that same anchor, followed by Rhat_x, gives uniform full-decoder error

    |sqrt(ell(x,C))-sqrt(ell_hat(x,C))|
      <=sqrt(3Lambda)+sqrt(3E_row)+sqrt(24m/kappa)
      =:delta.                                      (16)

This is one compatible acquired anchor, not independently aligned changing-encoder purifications. Equations (5), (7), (13), and (14) give

    delta^2<=9Lambda+9E_row+72m/kappa
      <=gamma epsilon/32768.                        (17)

The triangle step in (16) is purely for the actual same decoder C, including arbitrary cross-coordinate coherence.

## 6. Finite full-decoder optimization and all-history error

For every physical C, the surrogate ell_hat(x,C) is a nonnegative real quadratic bounded by 12/kappa. The known objective H_x=(3/2)T_hat_x^T has both trace and operator norm at most 6/kappa. Apply the received full-CPTP known-coefficient SDP/control contract with coefficient bound b=6/kappa, not its old constant-loss bound. A rational encoder net with squared chord radius h_opt^2<=kappa nu_opt/48, and SDP/repair error at most nu_opt/2, gives a physical pair within nu_opt of the continuous surrogate optimum. Use

    nu_opt<=gamma epsilon/131072.                    (18)

As in the received proof, at a joint continuous optimum the fixed-decoder quadratic is stationary in x, so the net loss is quadratic in h_opt. This net is not physically sampled. Positive prediction does not require a fabricated valid-channel completion; only the selected decoder must be CPTP on every record.

On the simultaneous pilot and fresh-bank good event,

    sqrt(ell_selected)<=sqrt(ell_star)+2delta+sqrt(nu_opt)
      <=sqrt(ell_star)+3sqrt(gamma epsilon/32768).

Young's inequality with gamma/2, using gamma<=1, gives

    ell_selected<=(1+gamma/2)ell_star+27epsilon/32768
      <(1+gamma/2)ell_star+epsilon/512.

The combined statistical bad mass is at most epsilon/128, and actual Bell loss of any returned physical policy is at most one. This proves (2) with slack. No unconditional estimate is promoted to a fixed-record certificate.

The deterministic horizon for one payload is H=N+n_0+1. All pilot settings, rational anchor arithmetic, the classical anchor search, fresh collective receiver bank, finite estimator, encoder/decoder optimization, memory, physical decoder compilation, and private framing are paid. Implement the 24-slot ideal distribution with bounded bits as in the independent receipt; its whole-pilot error and every finite control error fit one predetermined whole-process discrepancy epsilon/2. If search or numerical certification fails, pad any unused bank calls with a fixed ordinary setting, return the declared physical fallback, and preserve the fixed cap. No expected stopping time or free postselected success resource is used.

## 7. Scope and exact governing dependencies

The received base source is `BALANCED_RANK_ONE_ROW_ANCHOR_ACQUISITION.md`, SHA-256 `421f3fdabfaff88e924346795f7d7aa63014549cb335db4b1c884abfdfe97083`. Its independent receipt is `BALANCED_ROW_ANCHOR_INDEPENDENT_RECEIPT.md`, SHA-256 `a0abe7399f33b68f48e2633cb7baf11d301408678304cc89d66d318118679895`, with JSON receipt `66be88a3cedd8f54154a4173731b575d3c132ca6df418a7a1819b5cae34a6a27`. Its ordinary loss preparation, Bures query, finite full-CPTP SDP and private-framed comparator imports are unchanged and are not re-proved here.

The new obligations are high-count retention, a data-acquired balanced anchor, the discarded-mass coherent task bound, and conditional composition of the later state bank. The known basis and exact rank-one diagonal promise are still substantive. No noisy-data certificate of those exact promises, free frame acquisition, source eigenvalue floor, useful logical seed, protected input reference, or coherent encoder selector is added. The result is not an improvement of the generic unstructured k^4 theorem without further promises; kappa may deteriorate with dimension. The independently pending approximate-row extension is not used. A multi-payload substitution can be made only with its full retained-history/complete-process budget stated separately.
