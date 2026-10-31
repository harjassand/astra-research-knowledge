# Activity cost with coherent local source creation

Status: root resource addendum candidate, unreviewed. This counts the specified Markov guard loss/injection jumps, not heat/power, all microscopic bath events, or coherent simulation work. It does not replace the selected-fault proof.

Let N=sum_i n_i. The source has loss rates lambda_i>=lambda>0, injection a_i<=a, number-conserving hopping, and arbitrary real number-preserving terms. At cell i let c_i bound the norm of the TOTAL off-diagonal (P_i to Q_i) Hamiltonian block, including any admitted source creation by the system. Intended system evolution and number-preserving source terms do not change N. All bounds are uniform over actual source/system/reference states.

## Mean cost

The source-creating Hamiltonian obeys

    |Tr rho i[K_i,n_i]|<=2 c_i sqrt(Tr rho n_i)
                       <=(lambda_i/2)Tr rho n_i+2c_i^2/lambda_i.

Write J_- and J_+ for cumulative loss and injection jumps. The exact expectation balance and the preceding inequality yield

    E J_+ <= T sum_i a_i,
    E J_- <=2 E N(0)+2T sum_i a_i+4T sum_i c_i^2/lambda_i,
    E(J_-+J_+) <=2 E N(0)+3T sum_i a_i+4T sum_i c_i^2/lambda_i.

Time-dependent coefficients can be integrated in these expressions using actual uniform bounds. In the fixed-diffusion convention c_i=sqrt(lambda)b_i with common loss, the coherent contribution is4T sum_i b_i^2. It is not a squared norm of the sum of all couplings and does not grow with the rapid rate solely because the rate is rapid.

## Canonical-count exponential moment

For u>0 choose W=exp(2u N) and tilt BOTH loss and injection jump counts by exp(u). Loss contributes

    -lambda_i(1-exp(-u)) n_i W.

Injection is bounded by a_i(exp(3u)-1)W. The similarity-transformed Hamiltonian commutator has off-diagonal norm at most2c_i sinh(u). The2x2 operator inequality

    [[0,X^dagger],[X,0]] <= A I+d Q,
    A=||X||^2/d,

follows by Schur complement (with the zero-X case taken separately). Taking d=lambda_i(1-exp(-u)) absorbs the loss contribution and leaves

    tilted_G^dagger(W) <= B(u) W,
    B(u)=sum_i [a_i(exp(3u)-1)
       +4c_i^2 sinh(u)^2/(lambda_i(1-exp(-u)))].

Since W>=I, positive tilted evolution gives

    E exp[u(J_-+J_+)]
      <=Tr(exp(2uN)rho0) exp[T B(u)].

This is an operator-counting argument, not a classical-occupation-path assumption. Source/system correlations and coherent number-conserving transport are retained. The Markov-field initialization and specified jump representation remain binding. Extra spectator events are not counted by this formula.

## What this does and does not buy

The mean and exponential bounds can price native jump activity while the clamped-weight theorem separately prices logical fault amplitudes. A high cooling bandwidth is still an actual hardware resource. If injection a_i rises proportionally with loss lambda_i, the injection cost rises accordingly; fixed activation is not a free physical knob. No thermodynamic energy is inferred from the number operator without a separate physical identification.

A small jump budget alone cannot certify a useful computation. An arbitrary source-number-preserving PP logical error could cause no source jumps at all; the main fault theorem excludes it or demands an additional unprotected-error budget. Conversely coherent source-creating interactions retain a nonzero diffusion-scale logical disturbance when c_i scales as sqrt(lambda). This note does not erase that disturbance or solve full-source coherent simulation.
