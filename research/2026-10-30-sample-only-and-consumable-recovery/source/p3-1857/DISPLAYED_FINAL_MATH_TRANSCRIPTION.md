# Normally displayed final: deterministic text/formula projection

Visible-only report, not acquired theorem, code or review originals. Each KaTeX formula uses its original TeX annotation, with duplicate rendered glyphs omitted. Raw visible HTML/text and private DOM remain preserved separately.

ChatGPT said:ChatGPT
The strongest new result is a working theorem for verifying noncommuting quantum control certificates from local calibration. It replaces a whole-system operator calculation with a finite-neighbourhood calculation, while controlling how calibration error affects the resulting guarantee.
The earlier bounded-retention theorem is now saved, independently reviewed internally, and accompanied by executed finite-shot code. The previous experiments remain preserved as reported continuity; their old files were absent from this executor, so I have not represented them as recovered or rerun.
1. The central mechanism
I changed the target from stationary-state reconstruction to certifying cumulative recorded outcomes of a live quantum device under adaptive control.
For an available physical instrument with outcome maps  $\mathcal M_{a,y}$ , recorded reward  $r_{a,y}$ , and a positive operator  $F$ , define $Q_{a,\lambda}(F)
=\sum_y e^{\lambda r_{a,y}}\mathcal M_{a,y}^{*}(F).$
If every allowed action satisfies $Q_{a,\lambda}(F)\le \eta_a F,$
then the observed cumulative reward  $S_t$  obeys $\Pr\!\left[
\exists t:\;
\lambda S_t-\sum_{j<t}\log\eta_{a_j}
\ge \log B_0+\log(1/\delta)
\right]\le\delta,$
where  $B_0\ge \operatorname{Tr}(F\rho_0)/\lambda_{\min}(F)$ .
This is an anytime probability bound, including data-dependent stopping. It permits classical feedback, entangled plant states and passive references. The instruments must include their measurement disturbance and associated physical operations. Holding noise needs its own modeled contribution.
The controller never has to measure  $F$  or reconstruct the conditional quantum state. Deployment continues to use the live calibrated instruments.
Risk-sensitive quantum control, operator Bellman inequalities and quantum martingale arguments have substantial predecessors. I used those constructions as machinery; I am not claiming their invention. arxiv.org+2
The stronger step: noncommuting potentials
The first construction used commuting local potentials. The ordinary robust-SDP comparator contained it, so I continued to the obstruction that mattered: a general noncommuting extensive potential appears to require a global matrix calculation.
Let $F=e^H,\qquad H=\sum_X h_X,$
with terms on at most  $k$  sites and $\sup_i\sum_{X\ni i}\|h_X\|\le J,\qquad (k-1)J<1.$
For an action supported on  $s$  sites, imaginary-time dressing of its local Kraus operators gives a controlled approximation inside a radius- $R$  neighbourhood. The resulting bound is $\|A-\widehat A_R\|
\le
4d_S e^{\lambda r_{\max}}C\,T_{R+1}
+
d_S\xi\!\left(e^{\lambda r_{\max}}C^2-1\right),$
where:
$A=F^{-1/2}Q_{a,\lambda}(F)F^{-1/2}$ ;
$\widehat A_R$  uses the finite neighbourhood and the learned local instrument;
$\xi$  bounds the local normalized Choi error;
$C=(1-(k-1)J)^{-s/(k-1)}$ ;
$T_{R+1}$  is an explicit exponentially decaying commutator-series tail.
Neither error term contains the total Hilbert-space dimension. Exact trace preservation is essential to the centered calibration term. When  $H=\lambda V$ , that term is  $O(\lambda\xi)$ , avoiding an artificial  $1/\lambda$  loss in the mean-rate limit.
Imaginary-time locality itself is established research. The new working construction here is its explicit use in an unknown-instrument calibration and adaptive-control certificate, with the constants and enabling interface carried through. Phys. Rev. Research
On a bounded-growth one-dimensional lattice, radius  $O(\log(1/\epsilon))$  gives polynomial classical patch computation in  $1/\epsilon$ , at fixed local constants. Higher-dimensional dense patch computation can cost $\exp\!\bigl(O(\log^D(1/\epsilon))\bigr).$
Bounded interaction size alone does not guarantee small neighbourhoods.
The theorem and signed-Choi calibration argument passed the completed internal mathematical and code review.
2. What actually ran
InvestigationExecuted resultScope
Bounded-retention learningAt the same 1.8 million modeled source calls, RMS trace error was 0.0879 for one-call probes, 0.0236 for 32-call probes, and 0.0524 for 400-call probesFinite-shot qubit implementation; excessive holding loses
Unknown-device control certificate14,680,064 calibration calls produced the bounds belowLocal instrument data, including holding noise
Noncommuting locality22,020,096 local process probes; a seven-site patch certified a nine-site example with normalized tilted eigenvalue at most 1.31937, versus the hidden exact value 1.27504Full-chain matrices were used only to score the finite check
Population-only ambiguityTwo instruments gave identical population-probe records but different coherent bounds: 1.30384 versus 1.34307; input-coherence calibration certified 1.34745An exact information blind spot, with an executed finite-shot remedy
All observations were synthetic. Aggregate-count sampling is distinguished from explicit trajectories and matrix calculations in the files. The numerical certificates use floating-point eigensolves; interval verification remains open.
A completed physical control operation
The reference operation charges a cell until a native jump flag appears, then harvests an excitation. Holding survival is  $v$ , and charge probability is  $c$ . The flag, harvest readout, fresh work bit and holding interval are explicit resources.
Its exact optimal mean delivery rate is $\mu=\frac{cv}{1+c}.$
The optimal controller is classical. The operator proof additionally bounds the permitted coherent and entangled strategies.
For the unknown-device calibration at  $c=.62,\;v=.93$ , the numerical implementation of the 99% simultaneous confidence construction gave $\mathbb E S_T^{\rm controller}
\ge 0.323812\,T-0.574142,$
and, for every allowed policy, $\mathbb E S_T\le 0.361357\,T.$
The reference optimum is  $0.355926$  per call.
The same archive gives the fixed post-calibration anytime boundary $S_t\le 0.364626\,t+46.0517$
with operating failure probability  $0.01$ ; adding calibration failure gives at most  $0.02$  total.
The main calibration also requires 7,340,032 fresh harvest work bits. Raw counts, input/outcome ordering, fitted effects and confidence radii are saved, so the reusable data record is concrete.
A useful failure remains: the jump-only controller can stall after an off-model excitation when holding becomes nearly perfect. Its robust lower certificate becomes expensive as  $v\to1$ . Extra sensing or timed resets would change the interface and must be charged.
3. What the ordinary alternatives defeated
The comparisons changed the attack rather than merely accompanying it.
Structured stationary transport: ordinary resistance estimation stayed near 130,000 source calls from 32 to 131,072 sites. A small global mixing gap did not create an advantage for retained-history reconstruction.
Mean and risk-sensitive Bellman compilation: ordinary local tomography plus robust optimization contains the initial compiler and exactly solves the transparent charge/harvest reference. Mortimer’s stationary-observable SDP work provides a relevant known-generator representation; the unknown-device acquisition cannot be supplied for free. arxiv.org
Broader retention architectures: the complementary coherent-interrogation experiment obtained a real improvement over one-call acquisition under good holding, with its phase-localization pilot paid. Poor holding removed that benefit. It does not establish superiority to optimized entangled parallel estimation. arxiv.org
Unrestricted stationary-sector certification: the saved hidden-sector obstruction requires  $\Omega(d)$  calls even with adaptive quantum memory and intermediate controls. Supplied locality and addressability are therefore substantive resources.
The noncommuting theorem supplies a quantitative verification layer that the ordinary method can also use. No source advantage over that fully informed comparator has been established.
4. Current boundary of the result
The completed advance is a constructive route from local physical calibration to global adaptive-trajectory guarantees, including noncommuting certificate potentials.
Its remaining limitations are consequential:
useful potentials and controllers may be difficult to find;
a general initial-potential contribution remains extensive;
local support, addressability and a memoryless instrument interface are supplied guarantees;
physical idle evolution must be included;
the present conservative confidence bounds require millions of calls;
no optimized hard many-body controller or hardware advantage has been demonstrated.
These are working theorems with completed internal reviews and runnable evidence. Priority and external acceptance remain open.
Saved proofs and runnable work
STATUS.md — complete checkpoint, comparisons, costs and execution distinctions.
STATUS.mdDocumentOpen file   noncommuting_risk_locality.mdDocumentOpen filecheck_noncommuting_locality.pyCodeOpen file6 more
