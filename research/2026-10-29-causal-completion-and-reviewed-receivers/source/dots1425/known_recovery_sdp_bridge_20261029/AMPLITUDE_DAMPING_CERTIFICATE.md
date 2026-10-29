# Exact known-channel SDP witness: Petz need not be the optimum
2026-10-29. Supporting calculation, not a new recovery-optimization method. Primary predecessor: Fletcher–Shor–Win, *Optimum Quantum Error Recovery using Semidefinite Programming*, quant-ph/0606035, https://arxiv.org/abs/quant-ph/0606035 .

For qubit amplitude damping with K0=diag(1,a), K1=[[0,b],[0,0]], a,b>=0, a²+b²=1, the identity decoder has entanglement fidelity(1+a)²/4. It is optimal, as the following matching dual certificate proves.

Use column-vectorized recovery Choi J with Tr_output J=I_2. Its objective matrix is W=sum_l vec(K_l†)vec(K_l†)†/4. Thus W has nonzero entries W00=1/4, W03=W30=a/4, W33=a²/4 and W11=b²/4. The dual minimizes TrY subjectY tensor I_2>=W. Choose Y=diag((1+a)/4,a(1+a)/4). Its residual has a2×2 block(a/4)[[1,-1],[-1,1]] on coordinates0,3, scalar(1+a-b²)/4>=0 on coordinate1, and scalar a(1+a)/4>=0 on coordinate2. Therefore it is PSD. TrY=(1+a)²/4 matches the identity primal value exactly.

For a>0 and the maximally mixed reference, the Petz Kraus operators are L0=diag(1/sqrt(2-a²),1), L1=[[0,0],[b/sqrt(2-a²),0]]. Its composite entanglement fidelity is
 [(a+1/sqrt(2-a²))²+b^4/(2-a²)]/4.
At a=4/5,b=3/5 all source Kraus entries and optimal primal/dual certificates are rational; the Petz value is algebraic and strictly below the optimum81/100. This is a useful fixture for a physical learned-channel optimal-recovery upgrade, not an objection to the accepted squared-optimum Petz theorem.

No claim that a floating numerical solver has certified the optimum is needed here: the displayed rational primal/dual matrices certify it analytically.
