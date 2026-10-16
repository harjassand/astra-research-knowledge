# Faithful qubit-reference MMSE reversal for three Pauli outputs

## Certified result

A qubit reference suffices for the requested channel family and q=1/5. The target prepares sigma_i=(I+(3/5)P_i)/2, i=X,Y,Z. The source reveals the classical input with probability 1/5 and otherwise erases it. A finite, faithful binary encoding and an explicit fixed target receiver achieve

source optimal MMSE - target fixed-receiver risk
=8360352958858328928696700289758492365162202649
 /1602805342290558616614381584839931820000000000000
approximately 0.005216075051827943, strictly above 1/200.

The target receiver acts on dimension 4 (output qubit times reference qubit), rather than dimension 6 in the previous three-level-reference fixture. This is an achieved resource tradeoff, not a global optimum or a general memory lower-bound theorem.

The ordinary scalar-reference SLD threshold for this target is 9/50<1/5, so the reversal genuinely requires quantum reference information relative to the ordinary scalar experiment. The ordinary RLD threshold 9/41 exceeds 1/5 and must not be substituted for the SLD/MMSE threshold.

## Explicit normalized physical states

Labels theta=+1 and -1 are equally likely. Each state is block diagonal in the three-valued classical input; the three blocks are qubit matrices. Divide every matrix below by 10000.

For theta=+1:

rho_+,1 = [[2955,559+1469i],[559-1469i,911]],
rho_+,2 = [[4267,298-2382i],[298+2382i,1377]],
rho_+,3 = [[271,92-204i],[92+204i,219]].

For theta=-1:

rho_-,1 = [[445,94-46i],[94+46i,46]],
rho_-,2 = [[5052,306-1668i],[306+1668i,591]],
rho_-,3 = [[367,535-883i],[535+883i,3499]].

Each full state has trace one. Exact leading-principal-minor tests prove every block eigenvalue is strictly above 1/1000 and strictly below 3/5. Thus both full states are faithful with condition number below 600. These are explicit conditioning margins, not an experimental perturbation-robustness guarantee.

The reference marginals are UNEQUAL:

rho_+,ref=[[7493,949-1117i],[949+1117i,2507]]/10000,
rho_-,ref=[[5864,935-2597i],[935+2597i,4136]]/10000.

The reference alone carries label information, and its contribution is retained in the source calculation. No erased-reference term is dropped.

## Fixed target receiver

In output-qubit tensor reference-qubit basis, measure the spectral decomposition of the following Hermitian observable L and report its eigenvalue as the estimator of theta. All entries are divided by 10000:

L = [[1709, -270+1263i, 1140+1076i, -682+1336i],
     [-270-1263i, -4178, 1274-1316i, 1329-1077i],
     [1140-1076i, 1274+1316i, 1550, 298+1698i],
     [-682-1336i, 1329+1077i, 298-1698i, 920]].

This is a fixed rational-complex receiver, not asserted to be exactly optimal. Its spectral measurement uses at most four outcomes. Its approximately optimized precursor had eigenvalues near -0.52369, -0.01281, 0.01303, 0.52365; the exact certificate uses the displayed rational matrix, not those rounded spectral values.

## Exact source optimum and target risk

Define B_i=(rho_+,i+rho_-,i)/2 and H_i=(rho_+,i-rho_-,i)/2. Let W=sum B_i and K=sum H_i. The SLD convention is B L+L B=2H and g_B(H)=Tr H L.

For a qubit block, writing B=b_0 I+B_0 and H=h_0 I+H_0 with traceless B_0,H_0, the exact SLD is

l_0=[b_0 h_0-Tr(B_0 H_0)/2]/[b_0^2-Tr(B_0^2)/2],
L_B=l_0 I+(H_0-l_0 B_0)/b_0.

This gives the input and reference costs exactly:

sum_i g_(B_i)(H_i)
=7138379179024706109709259158259/22452248015302534651358382180000,

g_W(K)=43227124794193/892341237500000.

The source optimal explained variance is

G_source=(1/5)sum_i g_(B_i)(H_i)+(4/5)g_W(K)
=512602730891287968831734845584555808011773
 /5008766694657995676919942452624786937500000.

For target baseline A=sum_i sigma_i tensor B_i and target tangent J=sum_i sigma_i tensor H_i, the displayed fixed receiver has explained-risk reduction

G_target,fixed=2Tr J L-Tr A L^2
=2151143651639/20000000000000.

Therefore target fixed-receiver risk is exactly 1-G_target,fixed, approximately 0.89244281741805. The source's optimum is 1-G_source, approximately 0.897658892469878. Their difference is the positive fraction stated above. Since the source is optimized, this certifies a decision reversal even if the target receiver is not globally optimal.

## Preparation, measurement, and calibration accounting

- Prepare the specified two classical-input/reference states: a three-symbol classical register and one qubit reference, full input dimension 6. The states are separable across the classical/quantum cut but require controlled, generally noncommuting reference preparations.
- The target receiver receives two qubits in a four-dimensional joint space and performs the fixed observable's spectral measurement. This is a mathematical joint-measurement requirement, not a claim about a specific gate set or apparatus.
- The erasure receiver receives a four-valued classical reveal-or-erase register and the reference qubit, total direct-sum dimension 8. Its optimal observable consists of the three qubit SLD observables L_(B_i)(H_i) on reveal and L_W(K) on erase.
- The receiver calibration must match the displayed preparation and target observable. The certificate does not include state preparation, tomography, measurement synthesis, calibration error, detector loss, or drift.
- A four-dimensional joint analyzer may simplify integration relative to the prior six-dimensional example, but neither example by itself entails a two-photon entangling gate. No unsupported hardware implementation or architecture advantage is asserted.

The new fixture has a smaller achieved risk gap and a weaker certified eigenvalue floor than the previous qutrit-reference example, while using lower reference and joint-receiver dimension. These are concrete achieved properties, not an optimization frontier or matched claim of overall experimental superiority.

## Reproduction and scope

The exact state and fixed observable matrices are in checks/fixture.json and checks/receiver.json. checks/verify_fixed_receiver.py reconstructs every trace, state positivity margin, source optimum including its erased-reference term, fixed target risk, and positive gap. It compares the result with checks/FIXED_RECEIVER_CERTIFICATE.json. The target receiver is not claimed exactly optimal, and neither the input encoding nor achieved memory/gap tradeoff is claimed globally optimal.
