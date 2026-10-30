# Finite-response active recorder: a useful construction with a bad work scaling

30 October 2026. Root's follow-on attack. This is a separate continuous
material model, not an undeclared sensor for two-dimensional exclusion.
The physical-mechanism role subsequently proposed a stronger passive
follower. Preserve this failed efficiency route and its exact scope.

## 1. Physical equations and initial information

There are d=N² native coordinates, grouped into N rows of N for the
displayed displacement. The unperturbed reference is underdamped Langevin:

\[
 dX_i=V_i ds,\qquad
 dV_i=(-\partial_iU_N(X)-\gamma_iV_i)ds+\sqrt{2\gamma_i}\,dW_i.
                                                               \tag{1}
\]

U_N is an unknown smooth periodic interaction with a normalizable canonical
law; unknown fixed gamma_i lie in a bounded positive interval. The actual
reference initializer is canonical, or has density ceiling exp(CN²)
relative to it and the independent pointer initial laws below. Conditional
claims require the same ceiling and fresh sources after conditioning on
the retained record. A known canonical formula is not an uncharged sampler.

Attach a memory Y with energy Y²/2 and an actuator c with energy Mc²/2:

\[
\begin{aligned}
 dV_i&=(-\partial_iU_N-\gamma_iV_i-gY_i+c_i)ds
                                  +\sqrt{2\gamma_i}\,dW_i,\\
 dY_i&=gV_i ds,\\
 dc_i&=[-(c_i-gY_i)/\tau-V_i/M]ds
                                  +\sqrt{2/(M\tau)}\,dB_i.  \tag{2}
\end{aligned}
\]

Tau>0 is fixed. W,B are actual independent local bath sources. Initially
Y_i~N(0,1), c_i~N(0,1/M) independently and unread; exact costly matching
c_i=gY_i is not assumed. The -V_i/M term is the reciprocal reaction of the
native force +c_i. The +gY_i/tau actuator term is a **powered unilateral
operation**. It needs a local amplifier or another actual supplier, with
its response, loading, noise, range and power. Calling it active does not
construct that supplier. These equations retain native inertia and a white
Langevin bath; they are not the earlier finite-bath cell or a hard cutoff.

The internal pointer obeys exactly Y_i(s)=Y_i(0)+g[X_i(s)-X_i(0)]. Put

\[
 g²=H_N/N²,\quad M=N^4/H_N²,\quad H_N\to\infty,\quad H_N=o(N).
                                                               \tag{3}
\]

Then the row estimate sum_i Y_i/g differs from the actual row displacement
by the same initial offset at every time. Its normalized per-row variance
is 1/(NH_N), and its spatial root-mean-square error has tail

\[
 \Pr\{[N^{-1}\sum_y|\widehat A_y/N²-A_y/N²|²]^{1/2}>\epsilon\}
 \le\exp[CN²+C'N-c\epsilon²N²H_N].                           \tag{4}
\]

The exp(CN²) factor permits the stated warm initializer. This describes an
internal physical pointer. Final reading, common held timestamps,
communication, and Eulerian row attribution when particles change rows
remain separate operations. No noiseless output port has been derived.

## 2. A native-law comparison that does not learn the interaction

R_i=c_i-gY_i obeys

\[
 dR_i=[-R_i/\tau-(g²+1/M)V_i]ds+\sqrt{2/(M\tau)}\,dB_i.       \tag{5}
\]

This is weak memory friction and small colored force, not exact microscopic
noninvasiveness. Let Q be the unperturbed native law with the same recorder
equations evaluated along it, and P the actual law (2), to T_N=N²T_0.
This comparison is a calculation on path measures, not a copied specimen.
Girsanov gives

\[
 Z=dP/dQ=\exp(\mathcal M-\mathcal Q/2),\quad
 \mathcal M=\sum_i\int R_i(2\gamma_i)^{-1/2}dW_i,\quad
 \mathcal Q=\sum_i\int R_i²/(2\gamma_i)ds.                    \tag{6}
\]

Localize first. The bounds below supply Novikov and remove the stopping.
With a=g²+1/M and delta=tau a, convolution Young gives

\[
 \mathcal Q\le C[\tau\|R(0)\|²+
            \delta²\int\|V\|²ds+\int\|G\|²ds],              \tag{7}
\]

where G is zero-initial OU noise with covariance at most I/M. Under the
canonical comparison V has standard Gaussian marginal at each time, even
though times and coordinates can be dynamically dependent. Jensen in time
therefore gives

\[
 E\exp[b\int_0^{T_N}\|V\|²ds]\le(1-2bT_N)^{-d/2}.          \tag{8}
\]

The corresponding bound for G uses covariance 1/M. R(0) has covariance aI.
Holder separates the three terms; a warm initial density adds exp(CN²).
For |p|<=cN/H_N, (3) and (7)--(8) imply

\[
 \log E_Qe^{Cp²\mathcal Q}\le C_0N²+C_1p²(H_N²+H_N).         \tag{9}
\]

The small-coefficient conditions are p²a=O(1),
p²delta²T_N=O(1), and p²T_N/M=O(1). The exponential martingale and
Cauchy--Schwarz yield E_Q Z^p <= [E_Q exp((2p²-p)mathcal Q)]^(1/2)
for p outside (0,1); inside that interval use concavity. Thus for
p_N=cN/H_N->infinity,

\[
 {\log E_QZ^{p_N}\over p_NN²}\to0,\qquad
 {\log E_QZ^{1-p_N}\over p_NN²}\to0.                          \tag{10}
\]

Holder bounds P(A) by Q(A)^(1-1/p_N) times exp[o(N²)], and conversely
bounds Q(A) using E_P Z^(-p_N)=E_Q Z^(1-p_N). Hence every warranted
speed-N² LDP for a native path observable transfers with the **same rate**.
Exponential tightness transfers too. The native LDP is a separate input;
the recorder need not know U_N or gamma_i. Its own actual g, tau and M
still require implementation and calibration.

This comparison is weaker than the main theorem's exact native isolation.
It proves no total-variation or central-limit statement. The broad unknown
potential scope of (10) must not be substituted for a source martingale
bound in a controller theorem without a separate receiving argument.

## 3. Exact energy ledger and the failed scaling

For E=U_N+sum_i(V_i²+Y_i²+Mc_i²)/2, reciprocal powers cancel and

\[
 dE=dW_{act}+\sum_i\gamma_i(1-V_i²)ds
                 +\sum_i(1-Mc_i²)ds/\tau+d\mathcal N_s,
 \quad dW_{act}=(Mg/\tau)\sum_iY_ic_i ds.                    \tag{11}
\]

The pointer energy is only part of the cost. The actuator continually
dissipates Mc²/tau while tracking gY. No energy-recovery or electronics
overhead has been removed by writing a signed work identity.

For the free native example U=0, (V,R) is a two-dimensional stable OU
process with matrix [[-gamma,1],[-a,-1/tau]]. Its displacement diffusion is

\[
 D_{eff}={\gamma+\tau/M\over[\gamma+\tau(g²+1/M)]²}
                   \longrightarrow1/\gamma.                \tag{12}
\]

The stable rates stay bounded away from zero. Direct integration of their
covariances gives E(Yc)(s)=2g³D_eff s+O(g), uniformly for bounded positive
gamma, and

\[
 EW_{act}^{one}(T_N)=Mg^4D_{eff}T_N²/\tau+O(Mg²T_N).
\]

Since Mg^4=1, the d=N²-coordinate apparatus has

\[
 EW_{act}^{total}={T_0²\over\tau}
       [N^{-2}\sum_i\gamma_i^{-1}+o(1)]N^6,
 \qquad E\sum_iY_i(T_N)²=O(N²H_N).                           \tag{13}
\]

Its input work is order N^6 although useful pointer energy is only order
N²H_N. This is an explicit bad architecture, not a universal sensing
lower bound. Equation (13) is not extended to interacting U without its
displacement/correlation estimates. Preparation, finite-range operation,
pointer export and logic are additional resources.

## 4. The earlier passive attempt was too narrow

A damped reciprocal memory dY=(gV-lambda Y)ds+sqrt(2lambda Theta)dB has
the direct estimator
(Y_T-Y_0+lambda integral Y)/g = Delta X +sqrt(2lambda Theta)B_T/g.
For N probes per row its spatial precision exponent at T=N² is of order
N²[g²/(lambda Theta)], while its added low-frequency friction is
g²/lambda. At fixed Theta that particular transducer cannot both remove
its backaction and achieve a super-volume exponent by weakening g.

This does **not** exclude a reciprocal follower with an additional moving
pointer. The complementary role found exactly that alternative: keep the
spring extension bounded while a real pointer follows gX. Its error is an
endpoint displacement instead of accumulated bath noise. That mechanism
invalidates any attempted general no-go inference from the simple damped
memory and is the selected next construction. It also shows why a joint
Girsanov cost including unobserved probe noise can be misleading when the
physical task concerns the native marginal law.

## 5. Primary comparison and scope

Jun--Bechhoefer's feedback traps retain real update and observation delay:
https://arxiv.org/pdf/1212.4588. Zheng et al.'s implemented one-way electrical
coupling uses an inverting amplifier with negligible input loading or an
additional buffer: https://arxiv.org/pdf/2011.10993, Section 2. That actual
construction does not supply arbitrary volume-scale noise/loading accuracy.
Dechant--Lutz, *Fundamental limits on nonequilibrium sensing* (2025),
https://pmc.ncbi.nlm.nih.gov/articles/PMC12635388/, already analyze
nonreciprocal sensing and low-frequency precision at finite dissipation.
Their examples are another reason not to promote (13) to a general bound.

No priority is claimed for amplification, compensation or Girsanov transfer.
The paid model, likelihood proof and costly failure are retained as useful
machinery; they do not establish a manufactured recorder or a total-work
advantage. The passive follower and the emitted-mark receiver are serious
alternatives with different actual physical interfaces.
