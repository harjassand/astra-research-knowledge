# A noise-adapted source-unknown Choi-discriminant receiver

2026-10-27. New construction and analytic guarantee, pending independent receipt. This trades a weaker p/9 throughput and initially larger training cost for a stronger entropy-tolerance regime. It does not replace the independently received quadratic-training raw-code receiver.

Let E(rho)=p V rho V*+q Tr(rho)tau, p>=p0>0, p+q=1, with arbitrary finite-dimensional coherent reset tau. Set
 epsilon_ent=sqrt[5(p+3q)Delta].
Assume epsilon_ent<=p/25. There is an explicit source-unknown receiver using only ordinary discarded-label T/omega mixed programs, known qutrit operations and controlled SWAPs whose complete unhalved diamond distance from

 (p/9 id, (1-p/9) erasure)

is at most

 zeta +4sqrt[(25/2)p epsilon_ent]+(25/3)epsilon_ent,     (1)

for any chosen0<zeta<=1. The positive-rate operation is charged, not a normalized accepted-only comparison. Its explicit training count is below. The source promise and entropy condition are not verified by this construction.

## 1. An actual reset-sensitive discriminant

Let J be the normalized source Choi state and omega=I3/3 tensor E(I3/3). From ordinary labelled training, J=4T-3omega. Define

 H=J-3omega=4T-6omega
  =p Phi_V-(p/3)Q-(2q/3)I3 tensor tau,
 Q=I3 tensor VV*.

H is a rank-one positive update of a negative semidefinite operator, so it has at most one positive eigenvalue. Also -I<=H<=I. Unlike J-omega, H deliberately retains a negative reset penalty: its positive eigenvector suppresses noise rather than merely identifying the original isometry ray.

## 2. A known-source polar witness pays the positive eigenvector

This section constructs only an ANALYTIC witness, not a gate granted to the source-unknown learner. Put d=p/3,Y=q tau/3. The received entropy-only polar theorem provides the smallest positive eigenvalue lambda3 of dP-Y, where P=VV*, and the quantity
 e=3(d-lambda3)<=5epsilon_ent.
Our assumption implies e<=p/5, so there are three positive eigenvalues. Let Pplus be the corresponding rank-three positive spectral projection,
 M=V*Pplus V,
 Jiso=Pplus V M^(-1/2).
The received polar lemma gives p(1-lambda_min M)<=e. The isometry Jiso has range Pplus, and its normalized Choi vector Phi_Jiso satisfies

 |<Phi_V,Phi_Jiso>|^2=(Tr sqrt(M)/3)^2>=1-e/p.

Moreover, compressing dP-Y>=lambda3 on Pplus gives

 Tr[Jiso*Y Jiso]<=d Tr M-3lambda3<=e.

Its Q expectation is at most1. Therefore its Rayleigh value for H is at least

 p-e-p/3-(2/3)e=2p/3-5e/3.

Consequently H has a UNIQUE positive eigenvalue lambda obeying

 lambda>=2p/3-5e/3>=p/3.                              (2)

Let chi be its normalized eigenvector. Since Q>=Phi_V, the eigenvalue identity yields BOTH

 1-|<Phi_V,chi>|^2 <=5e/(2p)<=25epsilon_ent/(2p),       (3)
 q<chi|I3 tensor tau|chi> <=5e/2<=25epsilon_ent/2.      (4)

To see(3), H<=pPhi_V-(p/3)Q implies lambda<=(2p/3)|<Phi_V,chi>|^2. For(4), write the noise term separately and use |<Phi_V,chi>|^2<=1. These are actual spectral statements for the original source, including noncommuting noise.

## 3. Ideal positive-eigenvector operation

Prepare a known local Bell pair |Phi3>_OC and project C together with the received datum onto |chi><chi|. Keep logical O on acceptance and erase otherwise. If chi were Phi_V, this is exactly the received V*/3 success Kraus operator and yields ideal success p/9 on the genuine source branch.

For arbitrary chi, the complete rank-one-projector instrument differs from the Phi_V projector instrument by at most4sqrt[1-|<Phi_V,chi>|^2] in unhalved diamond norm. This follows directly by expanding the two accepted maps and paying the erased rejection effect. After the local Bell preparation/postprocessing, the genuine encoded data branch of weight p therefore costs at most

 4sqrt[(5/2)p e].

For a reset datum, the actual accepted mass is

 b_chi=(q/3)<chi|I3 tensor tau|chi> <=5e/6.

The complete reset-vs-erasure deviation is2b_chi<=5e/3. Thus the IDEAL chi receiver has complete original-source error at most

 4sqrt[(5/2)p e]+5e/3
 <=4sqrt[(25/2)p epsilon_ent]+25epsilon_ent/3.          (5)

This receiver does not assert input-independent acceptance or a deterministic inverse. No unknown positive spectral projector is yet assumed available; the next section acquires it.

## 4. Explicit acquisition from ordinary mixed programs

Use finite QPE on
 U=exp[i pi(H+I)/2].
Its phase for eigenvalue a is(a+1)/4 in[0,1/2]. All nonpositive eigenvalues have phase at most1/4; the unique positive one has phase at least1/4+p0/12 by(2). Classify a phase estimate as accepted if it lies in
 [1/4+p0/24, 3/4).
Circular estimation error less than delta_phase=p0/24 is sufficient for correct classification, including wrap at zero.

Choose
 eta=(zeta/16)^2,
 M=2^m the least power of two with M>=768/p0,
 r=ceil(log2(1/eta)),
 t_a=(pi/2)2^a, a=0,...,m-1,
 S=r pi(M-1)/2.

The already received finite QPE tail proof applies because M delta_phase>=32. Each run has error at most1/16; r repeats and majority give error at most eta on every eigenspace. The rank-one accepted-coherence argument then gives full accepted-plus-erased instrument error at most8sqrt(eta)=zeta/2 for exact evolutions.

For each controlled time t use
 N_t=ceil[512tS/zeta]
rounds with one T collision of angle+4t/N_t and one omega collision of angle-6t/N_t. Each consumes two ordinary training channel calls. A controlled partial-SWAP collision with angle h differs from its ideal controlled density evolution by at most4h^2 in diamond norm: both share the first-order generator and each second-order integral remainder is at most2h^2. In one signed round these two errors total at most208(t/N_t)^2. The two ideal controlled evolutions differ from their joint-generator evolution by at most48(t/N_t)^2, using the commutator bound for generators4T and-6omega. Thus the full controlled H evolution error is at most256t^2/N_t.

Summing the allocated errors gives zeta/2. Therefore the actually implemented complete chi-projector receiver differs from the ideal one by at most zeta, proving(1). Its consumed-training budget is

 n_train=2r sum_a N_(t_a)
        <=1024S^2/zeta+2rm,                           (6)

plus one data call. All randomness is discarded, and training is independent of the data/reference conditional on one fixed memoryless source. No purified program access, inverse channel unitary, or classical source description is supplied.

## 5. The stronger-noise versus cost tradeoff

If one wants relative complete error at most nu p, take zeta=nu p0/2. The first term is then at most nu p/2. A sufficient condition is epsilon_ent<=nu^2 p/10000 (for0<nu<=1), which also implies the gap premise. Equation(1) then gives total error less than nu p. Equivalently a sufficient original entropy threshold is of order nu^4 p^2, rather than the order-p^3 raw-code-overlap threshold at fixed relative accuracy.

The generic acquisition count(6) in this relative regime scales as p0^-3 times accuracy/logarithmic factors, not p0^-2. No matching sample-exponent claim is made here. The ideal success rate is p/9, so a relative error appreciably smaller than that rate is needed for a useful accepted capability. The exact and near-erasure quadratic-training receiver remains preferable when its stronger overlap/entropy promise holds.

## 6. Stronger resolvent receiving: no square-root code-amplitude loss

The actual discriminant structure gives a stronger guarantee than(1), with the SAME physical protocol and training count:

 complete error <=zeta+30epsilon_ent.                  (7)

The earlier(1) remains a valid independent coarse bound. To prove(7), write

 D_B=(p/3)P+(2q/3)tau,
 H=pPhi_V-I3 tensor D_B,
 R=(lambda I+D_B)^(-1).

The unique positive eigenvector has phase chosen so that

 chi=C(I3 tensor R)Phi_V, C>0,
 (p/3)Tr(V*RV)=1.

The second identity is the rank-one secular equation. Set

 t=(2p/3-lambda)/p,
 f=|<Phi_V,chi>|^2,
 G=p V*R V.

Then0<=t<=5e/(3p)<=1/3 and Tr G=3. Normalization and the secular equation give C=p sqrt(f). Also D_B>=(p/3)P, so inverse order gives

 G<=I/(1-t).

The trace constraint consequently gives every eigenvalue of G between3-2/(1-t) and1/(1-t), hence

 ||G-I||<=2t/(1-t).

Equation(3), or directly lambda<=(2p/3)f, gives f>=1-3t/2 and therefore1-sqrt(f)<=3t/2. The actual Bell-contraction Kraus operator on genuine code data is

 A=K_chi V=(C/3)V*RV=sqrt(f)G/3.

Crucially A is POSITIVE Hermitian, not merely a vector-close arbitrary matrix. Thus

 ||A-I/3|| <=[2t/(1-t)+3t/2]/3 <=3t/2,
 ||A||<=1/[3(1-t)]<=1/2.

The accepted CP-map difference from rho/9 is at most

 (||A||+1/3)||A-I/3|| <=5t/4

in diamond norm. Paying erased rejection doubles this to at most5t/2. The genuine code branch of the original source therefore costs at most(5/2)pt.

The exact eigenvalue identity separately gives

 q<chi|I3 tensor tau|chi> <=p-3lambda/2=(3/2)pt.

Its accepted reset mass is at mostpt/2, so its complete reset-vs-erasure cost is at mostpt. Summing,

 ideal chi-receiver error <=(7/2)pt
                          <=35e/6
                          <=(175/6)epsilon_ent
                          <=30epsilon_ent.

The learned spectral instrument adds at most zeta, proving(7). No additional logical compensation or unknown Gram-matrix gate is needed; the positive resolvent structure supplies the linear amplitude estimate directly.

For a requested relative error0<nu<=1, choose zeta=nu p0/2 and assume epsilon_ent<=nu p/60. The complete error is then at most nu p. This premise automatically implies epsilon_ent<=p/25, and is equivalent to the sufficient original entropy threshold

 Delta<=nu^2 p^2/[18000(p+3q)].

Thus the physically specified source-unknown operation now reaches the same square-root entropy ERROR SCALE as the known-source polar construction, at its explicitly weaker p/9 identity throughput and initially p0^-3 relative-training cost. The joint resource/noise/throughput frontier is not claimed optimal.
