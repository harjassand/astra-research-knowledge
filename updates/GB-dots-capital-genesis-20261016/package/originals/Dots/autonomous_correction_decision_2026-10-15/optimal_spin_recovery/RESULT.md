# Exact Gaussian single-interval recovery ceiling for the Li four-level code

## Scope and result

This is an analytic result for one explicitly stipulated noise model, not a reconstruction of the measured hardware channel or a demonstrated improvement. The channel is N_v(rho)_{mn}=exp[-v(m-n)^2/2] rho_{mn}, with m=(-3/2,-1/2,1/2,3/2), from theta~N(0,v). No gate, reset, timing, leakage, drift, or estimation costs are included. Persistent theta across cycles must be integrated outside the full conditional trajectory, not replaced by repeated applications of this averaged map.

The code and error states were checked directly against the downloaded Extended_data_Fig6.py: L0=(1/2,0,sqrt(3)/2,0), L1=(0,sqrt(3)/2,0,1/2), E0=(-sqrt(3)/2,0,1/2,0), E1=(0,-1/2,0,sqrt(3)/2). Its published ideal recovery maps each Lj to itself and Ej to Lj using separate Kraus operators.

Let x=exp(-v/2). Among ALL CPTP recovery maps from dimension four to the logical qubit,

F_e,opt = (1+f)/2,
f = sqrt(21x^2-6x^10+x^18)/4.

Among ALL such maps that additionally fix the entire codespace exactly, including every logical superposition,

F_e,dark = (1+r)/2,
r = (9x-x^9)/8.

The published ideal recovery attains the second optimum. Thus a requirement that the entire code be an exactly preserved dark subspace eliminates the proposed recovery improvement for this model.

## Global analytic certificate, unrestricted recovery

Write the two disjoint physical supports as H0=span{|−3/2>,|+1/2>} and H1=span{|−1/2>,|+3/2>}. The encoded noise maps |0><0| to A on H0, |1><1| to B on H1, and |0><1| to C:H1→H0, where Tr A=Tr B=1 and

C = (1/4) [[sqrt(3)x, x^9], [3x, sqrt(3)x]].

For any CPTP R,
4 F_e(R N V) = <0|R(A)|0> + <1|R(B)|1> + 2 Re <0|R(C)|1>.

Each population term is at most one. Let W be ANY Stinespring isometry for R and W_j=(<j| tensor I)W. Each W_j is a contraction. Then the off-diagonal term is Tr(W_0 C W_1†), whose magnitude is at most ||C||_1, by trace-norm/operator-norm duality and ||W_1†W_0||∞≤1. Hence F_e≤(1+||C||_1)/2. This covers unrestricted CPTP maps, not merely a chosen ansatz.

To attain it, choose a unitary polar factor U in C=U|C|, extend any singular polar factor to a unitary, and define an isometry on the direct sum by W|h0>=|0> tensor |h0>, W|h1>=|1> tensor U|h1>. Trace out the two-dimensional environment. The population terms equal one and the coherence is Tr(CU†)=||C||_1. Thus the upper bound is sharp. For a 2×2 C, ||C||_1²=Tr(C†C)+2|det C|. Here det C=3x²(1−x^8)/16≥0, giving the displayed expression. This inequality plus saturating recovery is a global optimality certificate without reliance on a numerical SDP.

## Explicit optimal Kraus operators and missing operation

In the respective syndrome bases (L0,E0) and (L1,E1), the same crossblock is

M = x/16 [[15+y, −sqrt(3)(1−y)], [sqrt(3)(1−y), 3(1−y)]], y=x^8.

Set t=atan[sqrt(3)(1−y)/(9−y)], taking 0≤t≤atan(sqrt(3)/9). One exact optimal decoder has Kraus operators

K0=|0><L0| + |1>(cos(t)<L1|−sin(t)<E1|),
K1=|0><E0| + |1>(sin(t)<L1|+cos(t)<E1|).

Their completeness sum is I4. Appending the encoding isometry gives a recovery back into the physical codespace. Equivalently, rotate the L1/E1 syndrome basis coherently by a noise-dependent angle, then apply the existing syndrome-discarding ideal recovery. A balanced realization splits opposite half-angle rotations between H0 and H1.

This is an explicitly realizable abstract CPTP map, but a new physical implementation is NOT demonstrated. The missing ingredient is calibrated coherent, logical-branch-dependent code/error mixing before syndrome erasure, while retaining the needed phase. Merely retuning the error-to-code dissipative jump while preserving every code state cannot attain this bound.

For the tuned recovery applied to a completely noiseless code input, logical coherence is cos(t), so its entanglement infidelity is (1−cos(t))/2. It does not fix the code for any finite v>0. At strong dephasing, t approaches 0.1901256 rad (10.89 degrees), with noiseless-input infidelity about 0.00900975. At the degenerate fully dephased limit x=0 many optimum maps exist, including the dark map; the preceding angle statement describes this particular continuous family.

## Why exact code fixing changes the global optimum

Suppose R(V rho V†)=rho for EVERY logical rho. Every Stinespring dilation must have W Lj=|j> tensor |e> for a common environment state e. This follows by purity of the output on basis states and preservation of their superposition. Orthogonality of W applied to the code and its orthogonal complement then forces W Ej into logical tensor e-perp. Consequently R(P_L X P_E)=R(P_E X P_L)=0 for every X. The channel can only apply the fixed ideal decoding to the code block and an arbitrary CPTP decoder to the two-dimensional error block.

The crossblock M above has code-code entry a=x(15+y)/16 and error-error entry b=3x(1−y)/16≥0. Both noisy logical populations have error probability q=3(1−x^4)/8. The error decoder's two correct population terms are each at most q, and its error coherence factor has modulus at most one. Together with the fixed code terms, 4F_e≤2+2(a+b). Equality is reached by Ej→|j> isometrically. Since a+b=r, the published ideal decoder is globally optimal within the entire exact-code-fixing class. This proof does not assume the decoder preserves the disjoint physical supports in advance.

The condition is stronger than preserving only L0 and L1 populations. A map could preserve those two basis states while dephasing superpositions; it would not meet the full dark-subspace condition used here.

## Size of the opportunity, before all physical costs

The exact comparison is f²−r²=3x²(1−x^8)²/64. Thus strict improvement exists in the stipulated unrestricted model for 0<v<infinity, but it is small.

- The exact global maximum of (F_e,opt−F_e,ideal) occurs at y*=(19−2sqrt(85))/9, v*=−log(y*)/4≈0.6938543641. Its value is y*^(1/8)[2sqrt(y*²−6y*+21)+y*−9]/16≈0.00646610384, or 0.6466 percentage points of entanglement fidelity. To certify this, differentiate g(y)=y^(1/8)[2sqrt(q)+y−9]/16, q=y²−6y+21. The derivative has the sign of 3(y−1)[6y−14+3sqrt(q)]. Its only interior zero follows from 27y²−114y+7=0; the other root is outside [0,1]. Both endpoint gaps are zero, proving the stated global maximum. The other maximum locations below are numerical checks, not symbolic certificates.
- At that point F_e,opt≈0.90131969 versus F_e,ideal≈0.89485359.
- The coherence ratio f/r is at most 2sqrt(21)/9≈1.01835015. To verify, put y=x^8 and differentiate 4(21−6y+y²)/(9−y)²; its derivative is 48(y−1)/(9−y)^3≤0 on [0,1]. The ratio maximum is a limit as v→infinity, where both coherences vanish.
- The best adjacent-Zeeman physical pair under this same free dephasing has coherence x. The ceiling f/x≤sqrt(21)/4≈1.14564392 is a coherence ratio, not a lifetime or fidelity ratio. The unrestricted maximum absolute entanglement-fidelity gap over that unprotected pair is numerically about 0.04853172, at v≈0.57379671. The published ideal decoder reaches about 0.04221309 maximum gap at v≈0.54930614.
- For average qubit gate fidelity, use F_avg=(2F_e+1)/3; absolute improvements are 2/3 of the entanglement-fidelity improvements.
- Small-v expansions: f=1−3v²/4+109v⁴/32+O(v⁵), while r=1−9v²/8+15v³/8−273v⁴/128+O(v⁵). Thus unrestricted optimal entanglement infidelity begins at 3v²/8, versus 9v²/16 for the code-fixing ideal map. Their difference starts at 3v²/16. This is a leading-order error reduction of one third, not a large absolute-fidelity gain.

These ceilings cannot establish advantage against echo, dynamical decoupling, better encodings, or optimized physical controls. Those baseline implementations and their costs have not been executed here.

## Optional mirror-encoding family, independently checked

For L0=sqrt(u)|−3/2>+sqrt(1−u)|+1/2>, L1=sqrt(1−u)|−1/2>+sqrt(u)|+3/2>, 0≤u≤1:

f_u²=x²[1+2u(1−y)−u²(1−y)(3+y)].

For 0<v<infinity its unrestricted optimum occurs at u=1/(3+y), with f_family=2x/sqrt(3+y). This changes the encoding with the noise variance and does not claim optimality over all encodings.

For exact-code-fixing recovery, the code-code coherence is x[1−u²(1−y)] and the error-error coherence is x u(1−u)(1−y), which is nonnegative. The same constrained proof gives r_dark,u=x[1+u(1−2u)(1−y)]. Its maximum over this mirror family is u=1/4, independent of finite positive variance. The actual Li code is therefore already the optimum in this restricted encoding family with exact code fixing. At v=0 all encodings tie.

## Prior art and novelty boundary

The operational family is standard channel-adapted optimal recovery, with a polar-decomposition trace-norm alignment. No operation-family or algorithmic novelty is claimed. Fletcher, Shor and Win explicitly optimize entanglement fidelity for a fixed encoding and noise channel via semidefinite programming: https://arxiv.org/abs/quant-ph/0606035 (Phys. Rev. A 75, 012338, 2007). Reimpell and Werner's earlier iterative optimization explicitly allows schemes not perfectly correcting any selected syndrome: https://arxiv.org/abs/quant-ph/0307138 (Phys. Rev. Lett. 94, 080501, 2005). These primary abstracts were retrieved and checked. The derivation here is a small closed-form specialization and a constraint diagnosis; a comprehensive literature search for this exact four-level formula has not been performed.

## Reproducibility

check.py verifies the trace-norm identity, exact difference of squared coherences, encoding-family stationary point, Kraus completeness, and entanglement fidelities evaluated directly from the full 4×4 Gaussian channel for ten variances. checks.json holds outputs and numerical optimizations. Original published files were read without modification. Numerical optimization is explicitly distinguished from the analytic global recovery certificate.
