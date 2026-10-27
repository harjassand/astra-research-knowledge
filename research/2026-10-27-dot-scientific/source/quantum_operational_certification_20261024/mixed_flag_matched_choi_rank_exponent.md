# Matched quadratic flag-rank exponent in the full-Choi-program model

2026-10-27. Constructive upper proof candidate, independent receipt requested. The quadratic Choi lower bound is independently received; the adaptive physical-query lower bound remains only linear in rank.

## Family and exact bands

Let E_U(rho)=U(rho tensor I_r/r)U* on B=C3 tensor Cr, with unknown U. Its normalized Choi state is J_U=P/r, where

 P=sum_(k=1)^r |Phi_(U,k)><Phi_(U,k)|,
 |Phi_(U,k)>=(1/sqrt3)sum_a |a>_A U|a,k>.

The output marginal is I_(3r)/(3r), so

 omega=I_(9r)/(9r), H=J-3omega=P/r-I_(9r)/(3r).

The positive band is exactly P, with eigenvalue2/(3r); its complement has eigenvalue-1/(3r).

For the nine qutrit Weyls W_j on A define P_j=(W_j tensor I)P(W_j* tensor I). Their basis vectors satisfy

 <Phi_(U,k)|(W_j*W_l tensor I)|Phi_(U,m)>
 =delta_(k,m) Tr(W_j*W_l)/3
 =delta_(k,m)delta_(j,l).

Thus the nine rank-r bands are mutually orthogonal and sum to the identity on A tensor B. This is an exact statement, not an approximate Gram argument or a hidden flag-basis oracle.

## 1. Ideal full inverse from band measurement

Prepare the normalized receiver Bell pair between its logical output R and A. Measure the nine bands sequentially (retaining data after rejection), and apply the known Bell correction for the first accepted label. Since the bands partition the whole space, ideal erasure never occurs.

Let V_k:C3->B map |a> to U|a,k>. A rank-one component of label j has physical Bell-contraction Kraus operator, after the known correction,

 K_(j,k)=V_k*/3.

Tracing out the measured A,B registers sums over the orthogonal k components; no physical flag measurement or classical knowledge of k is needed. Each corrected accepted label therefore implements

 rho_B ->(1/9)sum_k V_k* rho_B V_k.

Summing all nine labels gives the CPTP map

 D_U(rho_B)=Tr_flag[U* rho_B U].                      (1)

In particular D_U composed E_U=id_3 exactly. Equation(1) holds on arbitrary B inputs, not just the promised encoded state. Coherence within each rank-r band must be preserved until the measured registers are discarded; the programmable implementation below uses coherent uncomputation for that reason.

## 2. Explicit consumed-program implementation

T=(J+3omega)/4 and omega are obtained from ordinary labelled mixed training, or from one full Choi copy each by known local processing. Rotating T on A implements each H_j=4T_j-6omega. No flag or eigenbasis is supplied.

Fix0<zeta<=1. Set

 eta=(zeta/100)²,
 M=2^m the least power of two at least768r,
 R=ceil log_2(1/eta),
 S=9R pi(M-1).

For each label use R coherent finite-QPE runs for exp[i pi(H_j+I)/2], accepting phase estimates in[1/4+1/(12r),3/4). Both eigenvalues are separated from the decision boundaries by at least1/(12r). Copy the majority decision and uncompute all QPE work. Then measure the decision, retaining A,B on rejection. Negative-time uncomputation uses fresh mixed samples and negative angles.

The complete exact-evolution retained-data binary instrument for each band differs from its Lueders measurement by at most4sqrt(eta). This is the underlying retained-data construction proved in the received arbitrary-rank filter, rather than merely its final erased-rejection corollary.

The controlled forward times are(pi/2)2^a, with opposite reverse times. Their total absolute sum across all labels is S. Simulate time t with

 N_t=ceil[512 |t| S/zeta]

signed rounds, angles4t/N_t,-6t/N_t. The received controlled signed-pair error256t²/N_t gives total simulation error at most zeta/2. The nine ideal classifier errors sum to at most36sqrt(eta)=0.36zeta. Sequential complete-instrument telescoping, correction and discarding therefore give total unhalved diamond error below zeta from(1).

The training cap is

 n_train<=1024 S²/zeta+36Rm.                         (2)

Each signed round consumes two mixed programs; the final term counts ceilings for forward/reverse times. The original noisy data call is additional. The raw output dimension is3r, but the program sample cost is quadratic in r, up to the displayed accuracy/logarithmic factors.

## 3. Scoped matched exponent

The independently received theorem `mixed_flag_quadratic_choi_program_lower_bound.md` gives Omega(r²) full Choi programs for any fixed nontrivial complete inverse accuracy. Equation(2) gives O(r²) times logarithmic/accuracy factors in that SAME full-Choi-program model. Thus the rank exponent is matched there.

The upper implementation is also available through ordinary mixed-sample physical training. However, the received lower bound against arbitrary bounded adaptive physical queries is only Omega(r), from latent-flag collision. A quadratic adaptive-query lower bound is not inferred from the Choi result.

No optimal accuracy exponent, reusable learned decoder, mixed-success entropy theorem, or general unknown-channel inverse claim is made. This is the exactly reversible uniform mixed-flag family, with its explicit positive gap and exact band partition.
