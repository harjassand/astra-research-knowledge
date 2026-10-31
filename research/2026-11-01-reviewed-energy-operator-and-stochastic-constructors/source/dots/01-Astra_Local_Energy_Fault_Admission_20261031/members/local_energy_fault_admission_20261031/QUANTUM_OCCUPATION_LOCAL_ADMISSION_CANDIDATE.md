# Local fault admission from loss, bounded injection and coherent transport

31 October 2026. New receiving construction, **unreviewed**. This is not a new threshold theorem, a fixed-diffusion elimination result, or a hardware demonstration. It supplies an inclusive fault-AMPLITUDE bound for a restricted microscopic model. The ordinary non-Markovian threshold machinery is the intended consumer.

## 1. Actual model and resource contract

There are finitely many source qubits indexed by a graph V. Write n_i=|1><1|_i and sigma_i^- = |0><1|_i. Their generator contains

- loss jumps sqrt(lambda) sigma_i^-, lambda>0;
- continuing injection jumps sqrt(a_i) sigma_i^+, 0<=a_i<=a;
- coherent hopping Hamiltonian lambda H_hop, with
  H_hop=sum_{unordered {i,j}} (J_ij sigma_i^+ sigma_j^- + conjugate(J_ij) sigma_j^+ sigma_i^-).

Let B_ij=|J_ij| for an edge, B_ii=0, so B is symmetric. Require its acquired row sums d_i<=beta<1/2. Put gamma=1-2 beta>0. An additional acquired source Hamiltonian diagonal in the occupation basis may remain ON with arbitrary strength: it commutes with every weight below. Its actual implementation is still paid. Hopping, loss, injection and ALL unselected system interactions stay ON throughout the proof. No bath reset, stationary state, diagonal source state or classical source trajectory is assumed. The reservoir dilation is that of this supplied bounded Lindblad model; a different unknown microscopic reservoir is not thereby certified. Initial finite source/system/reference correlations can be arbitrary. The Markov loss/injection reservoir fields have the initialized input required by the specified Lindblad dilation (equivalently independent vacuum fields for the displayed jumps). Arbitrary correlated incoming fields are NOT included.

An actual finite circuit schedule consists of elementary locations l with time interval I_l, |I_l|<=tau, an intended source-independent gate on a bounded system patch, and a set D_l of at most g source indices. A source index belongs to at most one active location at any time. The location's unwanted Hamiltonian is

  K_l(t)=sqrt(lambda) sum_{i in D_l} n_i tensor A_{li}(t) + Delta_l(t),

where A_{li} is Hermitian, acts on that location's system patch (and any legitimate retained classical control register), and ||A_{li}(t)||<=b. The optional Delta_l is source-independent Hermitian implementation error with integral_{I_l}||Delta_l(t)||dt<=epsilon_ctl. All terms are supported on the declared location patch on the system side. The intended gate generator can have large norm; its action, routing, duration and implementation remain paid. The proof does not turn a promised unitary into a physical gate. Idle sites need actual locations too.

Source-independent intended operations commute with every weight used below. Exact source-independent instruments can be coherently dilated with their outcome/garbage records retained. A fixed schedule with coherent feed-forward fits if the same support, b, tau and epsilon_ctl bounds hold on every branch. Arbitrary source controls, source-dependent reset rates, coherent creation of source excitations, unbounded fanout, and overlapping assignments violating the one-active-location condition are not admitted here.

The model is NOT the fixed-diffusion source of earlier sections of the campaign: injection a is a physical rate independent of lambda. The mean occupation is small for rapid loss. If injection scales with lambda, the bound below deteriorates explicitly and does not claim to erase a nonzero leading dissipator. The n_i A_i interaction is dark-annihilating and does not itself create source energy. It can nevertheless have noncommuting system operators and quantum backaction on coherently transported source excitations.

## 2. Selected fault amplitudes, not invented fault probabilities

Use the canonical jump-history Stinespring dilation of the full source Lindblad evolution, retaining all jump times/colors privately. Include intended system gates and their reference/record registers. For each selected set S of k locations introduce a complex parameter z_l multiplying K_l only at l in S; unselected unwanted interactions remain at their actual real value one. Let W(z) denote the resulting (generally nonisometric) jump-history operator. Physical real settings yield the actual isometry.

All spaces are finite dimensional before the ordinary continuum jump-record dilation. For finite total time and fixed finite source/system registers, the no-jump propagators and the jump-history direct sum converge normally on compact complex z sets; equivalently this is the bounded-coefficient quantum-trajectory construction. This makes W an entire operator-valued function. It is NOT a normalized postselected state and is not asserted CPTP for complex z.

Define

  E(S) = product_{l in S} (evaluation at z_l=1 - evaluation at z_l=0) W(z).

Expansion of the Hamiltonian Dyson series says exactly that E(S) is the sum of fault amplitudes with at least one insertion from every selected location; other locations are unrestricted. Removing a location removes its system-coupling/error Hamiltonian only, not source hopping, loss, injection or any other gate. This is the inclusive amplitude object used in ordinary local non-Markovian fault tolerance. Its norm is operator norm on the complete finite system/source input with those reservoir fields initialized, unchanged by adjoining a reference. It is not the norm of an arbitrary full-unitary extension on unrestricted field inputs. The usual inclusive-amplitude/linearity receiving must be read in this initialized-isometry form; no non-Markovian-loss-reservoir extension is claimed.

## 3. A local operator weight with all exterior interactions present

For nonnegative u_i<=1 define

  V_u=product_i (I+u_i n_i).

All factors commute. V_u acts as identity on the system and its records. Each real unwanted interaction n_i A_{li}, every intended system Hamiltonian and every source-independent control commutes with V_u.

The loss adjoint is exactly

  D[sigma_i^-]^dagger(V_u)=-u_i n_i V_u/(1+u_i).

Injection obeys

  D[sigma_i^+]^dagger(V_u)=u_i(1-n_i)V_u <= u_i V_u.

For one hopping edge, on its one-excitation block the commutator i[H_ij,V_u] has off-diagonal magnitude |J_ij||u_i-u_j| V_rest. Its other blocks vanish. Therefore the OPERATOR inequality

  i[H_ij,V_u] <= |J_ij|(u_i+u_j)
       [n_i V_u/(1+u_i)+n_j V_u/(1+u_j)]

holds: on the one-excitation block the right side is the scalar |J_ij|(u_i+u_j)V_rest, and on the double-excitation block it is nonnegative. No stochastic interpretation of coherent hopping is used.

For |z_l|<=R, the imaginary part of a selected coupling contributes to the nonunitary norm evolution at most

  2 R sqrt(lambda) b sum_{i in D_l} n_i V_u.

Put r=2Rb/sqrt(lambda), and let v_i(t)=r when i belongs to an active selected location, zero otherwise. The extra control error contributes the scalar 2R||Delta_l(t)|| V_u. Real parts, including arbitrarily large real outside interactions, still commute with V_u and cause no additional weight growth.

Choose V(t) backward from V(T)=I. In rescaled backward time s=lambda(T-t), its coefficients satisfy

  dot u_i=-u_i+d_i u_i+sum_j B_ij u_j+v_i(1+u_i),  u_i(0)=0,

with v read at the corresponding reversed physical time. Set r=gamma/4. At a first component reaching u_i=1, the derivative is at most -1+2 beta+2r=-gamma/2<0. Hence 0<=u_i<=1. Define A=-I+diag(d)+B. Since A is Metzler and its row AND column sums are <=-gamma,

  u(s) <= 2 integral_0^s exp[A(s-v)] v(v) dv,
  ||exp(A t)||_1 <= exp(-gamma t).

This is an ordinary finite-dimensional comparison inequality, with constants independent of |V|.

Returning to forward physical time, (partial_t + tilted-adjoint-generator)V(t) is bounded above by

  [a sum_i u_i(t)+2R sum_{selected active l}||Delta_l(t)||] V(t).

The terms containing n_i V/(1+u_i) cancel or are nonpositive by construction. This inequality is valid with all hopping edges and all real system interactions ON.

## 4. The simultaneous selected-history estimate

Let k=|S|. At every time there are at most gk selected source indices and their total selected space-time volume is at most gk tau. The preceding convolution gives

  sum_i u_i(0) <= (2r/gamma) gk,
  integral_0^T sum_i u_i(t)dt <= (2r/gamma) gk tau.

The first inequality uses the terminal-time convolution; the second uses Fubini and the decaying column sum. It is independent of the total computation duration outside selected locations, including arbitrary gaps between them.

Since V(0)<=exp(sum_i u_i(0)) I, V(T)=I, integration of the weighted nonunitary evolution yields

  ||W(z)||^2 <= exp{ C k + 2R epsilon_ctl k },
  C=(2rg/gamma)(1+a tau).

One way to make this completely explicit is to evolve a positive input by the jump-history non-TP map with complex Hamiltonian. Its weighted trace derivative satisfies the preceding scalar inequality; taking the supremum over positive inputs is exactly the squared operator norm of W(z). Reference inputs obey the same inequality because the weight is tensored with identity. No reduced-state trace bound is substituted for this dilation norm.

For r=gamma/4, C=g(1+a tau)/2. The certificate prices initial arbitrary excitations through the first term and continuing physical injection through a tau. It does not assume an empty bath or omit warm inputs.

## 5. Cauchy extraction gives the threshold premise

For a one-variable analytic operator F,

  F(1)-F(0)=(1/(2 pi i)) integral_{|z|=R} F(z)/[z(z-1)] dz,

where R>1. Applying this separately in all selected variables yields

  ||E(S)|| <= [ exp(C/2+R epsilon_ctl)/(R-1) ]^k.       (1)

Thus an actual dimension-independent local amplitude strength is

  eta = exp(C/2+R epsilon_ctl)/(R-1).

For epsilon_ctl=0 choose R=gamma sqrt(lambda)/(8b), provided R>1. If R>=2,

  eta <= [16 b/(gamma sqrt(lambda))] exp[g(1+a tau)/4]. (2)

When b=0 the source-dependent interaction is absent and the usual direct control-error bound applies; do not divide by b. With a nonzero acquired control-error bound choose

  R=min(gamma sqrt(lambda)/(8b), 1/(2 epsilon_ctl)),

provided this is >=2. The same proof uses r=2Rb/sqrt(lambda)<=gamma/4 and the larger displayed C as a safe upper bound. It gives an explicit bound of order b/sqrt(lambda)+epsilon_ctl with paid constants. If R<2, (1) remains usable whenever R>1, but no small-noise claim follows automatically. If no admissible R exists, report non-admission rather than infer a threshold.

The bound is on inclusive amplitudes, not a positive p^k fault probability. Ordinary non-Markovian amplitude-threshold receivers apply under their actual gadget/input/control premises. A separate physical Pauli twirl may convert suitable disjoint-window cases to CP fault effects; that operation is unnecessary for (1) and is not smuggled into this theorem. In particular imperfect key pulses do not disappear: they are part of the actual gate/control-error budget.

## 6. Why this is a genuine local admission rather than a one-point moment argument

The contour is applied to the full selected Stinespring amplitude. Its k-dependent bound comes from the selected space-time potential in the operator weight, so it includes simultaneous and temporally separated selected faults with a persistent quantum source. One excitation may coherently visit many patches; all such histories are included in the hopping commutator estimate. No product of marginal fault probabilities, no global trace-distance estimate, no stationary covariance and no independent-source assumption supplies the result.

There is also no exterior-volume factor: the logarithm of the tilted norm is bounded by a decaying convolution of the selected potential. Both row and column control are load-bearing. Arbitrary high-degree transport, unbounded source-to-system fanout, shared arbitrary-strength source Hamiltonians, and source-creating sqrt(lambda) interactions are outside the theorem.

## 7. Acquisition, execution, and ordinary competitors

Acquisition consists of the actual graph/local hopping and loss/injection bounds, local A access/norm certificates, a complete location assignment and its actual gate schedule, and epsilon_ctl where used. For a supplied bounded-degree explicit graph these bounds can be checked with polynomial local arithmetic, not an exponential source-state table. A known homogeneous finite program can provide a uniform family certificate; unknown couplings cannot be inferred for free from a few samples. Rate calibration and statistical confidence are additional tasks. Physical implementation of a large lambda, low a, and the required control Hamiltonians is not furnished by this mathematical certificate.

For example beta=1/4, g=2, a tau=1, b=1 gives C=2, R=sqrt(lambda)/16, and exact eta=e/(sqrt(lambda)/16-1) when epsilon_ctl=0. At lambda=10^12 this is approximately 4.35e-5. This is an illustrative sufficient amplitude parameter, NOT a numerical fault-tolerance threshold or a practical hardware operating point. The actual chosen fault-tolerant construction and its overhead must be supplied. A generic raw-norm admission would see coupling sqrt(lambda) rather than the small occupation exposure, and can fail in the same parameter range.

The strongest ordinary comparison is not an independent-noise straw model. AGP's local non-Markovian fault amplitudes and AKP's shared-bath spatial bounds already receive a bound such as (1); their threshold, recovery and input machinery should be used directly. Existing randomization, decoupling and physical cooling methods receive the same source and control information. This construction's possible contribution is the specific microscopic local admission, not a new threshold or a new randomized-compiling method. Its ordinary components are a positive product weight, loss-versus-transport comparison, a jump-history dilation and complex-analytic fault extraction. No historical novelty claim is made.

The fixed-diffusion quantum apparatus problem remains open here: off-diagonal injection interactions of order sqrt(lambda) would add source-energy terms to this weight inequality. They can produce a nonzero effective dissipator, which must be the intended operation, be transparently encoded/corrected, or be paid as leading noise. Replacing a by a lambda-dependent rate in (1) is honest but generally destroys the useful admission. A global return gap or a one-point energy bound alone is not enough to repair this.

## 8. Source comparison and scope of reads

Primary threshold references:
- Aliferis, Gottesman, Preskill, quant-ph/0504218v3, Section 11: local inclusive operator-amplitude condition and shared-bath receiving. https://arxiv.org/html/quant-ph/0504218v3
- Aharonov, Kitaev, Preskill, quant-ph/0510231: fault tolerance with long-range correlated Hamiltonian noise. https://preskill.caltech.edu/pubs/preskill-2006-long-range.pdf
- Winick et al., 2212.07500v1, Sections III.2–III.4: non-Markovian randomized compiling, environment-retaining Pauli structure and key-dependent failure boundaries. https://arxiv.org/html/2212.07500v1

Accessible Astra sources read separately:
- N951 FINITE_CONTROL_COMPILER.md, SHA cb0a668684fa9d7160f77d471fd143d027a1a52a76e3feeaa73e677e241cdbda: disjoint-window shared-bath Pauli effect and finite-control signed-path bridge, under actual integrated interaction/control bounds.
- N1467 CP_CAVITY_LOCAL_FAULT_BRIDGE.md, SHA cd254da562171a38028ca942b3dfbaa85abc5477b464c5defc465c93a488f27f, and FAULT_CLASS_AND_GADGET_RECEIVING.md, SHA 9576281ca42a4cd0979b3d049b93a7aca84ecc52ac133ef6c72f852f281241b3: CP-cavity signed inclusive maps and disjoint gadget receiver under bounded incident complete norms.
- N1483 08_STANDARD_FT_SUPEROPERATOR_RECEIVING.md, SHA 751b5452f3bea9bbe31a9d833b569a144b45977d8503931c7f6dcc3aa37da7fc: ordinary scheduled code/gadget receiving, actual reset/gate preparation and signed good-map trace-defect reasoning.

Those are existing governing capital, not newly proved here; their internal review scopes remain their own. The exact latest P2 commutator-admission card has not been located, and this note does not assign it a fabricated locator or claim to supersede it. A source-based novelty comparison would require inspecting that exact statement.
