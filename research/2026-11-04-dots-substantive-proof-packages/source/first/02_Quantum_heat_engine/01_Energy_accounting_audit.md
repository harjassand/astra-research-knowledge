# Thermal-contact audit of a periodically driven chiral conductor

**Finding:** A standard, exactly unitary finite-band realization of the scattering topology in Ryu et al. has positive AC input power. It reproduces charge pumping but not the inference that zero mean photon exchange per incident energy implies zero total input power. This is a narrow model/accounting result, not a new engine or a blanket claim that every result of the paper is wrong.

Target: S. Ryu et al., Nature Communications **13**, 2512 (2022), https://doi.org/10.1038/s41467-022-30039-7 . Equations and supplement: https://arxiv.org/html/2104.11149v3 . No authors or third parties have been contacted.

## 1. Assumptions and measured quantities

1. Three normal, noninteracting fermionic contacts L1, L2, R supply independent grand-canonical incoming states. Both left contacts have the same temperature and DC chemical potential; R may differ. This matches the paper's thermal distributions deep in each reservoir and SI XII's initially independent contact potentials.
2. A classical periodic voltage generates a phase converter U on the outgoing L1 stream and its inverse on the stream entering L1, exactly as in SI S46. Reservoir absorption thermalizes outgoing particles; it is not a coherent return loop.
3. A static, energy-conserving resonant scatterer connects the streams. There is one transport channel per stream. Parasitic circuit losses are ignored, favoring the proposed engine.
4. Heat into contact alpha is Q_alpha=(1/h) integral dE (E-mu_alpha)[g_alpha(E)-f_alpha(E)], evaluated at that contact's reference after all entry conversions. With particle currents positive into contacts, electrical output is P_e=sum_alpha mu_alpha J_N,alpha. Total drive input is P_AC=sum_alpha Q_alpha+P_e. A time-dependent change of gauge must retain voltage-current work.

An overall constant shift of every energy, including band edge, resonance and chemical potentials, changes none of these heat or power results. Negative numerical energies merely place zero at the resonance; they do not assume physical states below the chosen finite band bottom.

## 2. The finite Fermi-edge term

For a phase drive, let p_n=|a_n|^2, delta=hbar*Omega, and g(E)=sum_n p_n f(E-n*delta). For a thermal Fermi function with a deep filled sea,

integral [f(E-d)-f(E)] dE = d,

integral (E-mu)[f(E-d)-f(E)] dE = d^2/2.

These are convergent differences, obtained by differentiating in d and using the normalized, centered distribution -f'(E). Thus sum_n n*p_n=0 gives zero excess particle flux, but

J_ex = delta^2 sum_n n^2 p_n/(2h) = e^2 average(V_ac^2)/(2h) > 0.

Reversing the phase changes the sign of n, not n squared. Applied to an independently thermal stream, it produces another positive J_ex. It cancels energy only when applied to the original coherent driven state, which S46 does not route back to it.

The paper's Eq.10/S47 instead sums n*p_n at each incoming energy and obtains zero. With a physical lower band edge, however, only propagating outgoing energies are allowed and amplitudes near the edge must be modified consistently with unitarity. With an unbounded filled sea, separated energy integrals diverge and shifting their limits can discard the finite term above. Merely truncating sidebands is not a valid repair because it destroys unitarity.

## 3. Exactly unitary finite-band construction

Use a finite energy ladder E_m=(m-N/2)*delta+epsilon, m=0,...,N-1, and integrate epsilon over one Floquet zone. For the paper's S30 pulse define s=Omega*w, r=exp(-s). Its phase, up to an irrelevant constant sign, is

a(t)=(1-r*exp(i*Omega*t))/(1-r*exp(-i*Omega*t)).

Define the Hermitian matrix K with K_mm=0 and K_mn=-i*r^|m-n|/(m-n) for m!=n. Set U=exp(i*K). U is exactly unitary at every finite N. Far from the boundaries its coefficients tend to S30; the boundaries automatically acquire the corrections needed for a real finite band.

Let S0 be the static three-contact matrix with nonzero blocks S0_L1,L2=I, S0_L2,L1=r_st(E), S0_L2,R=t_st(E), S0_R,L1=t_st(E), S0_R,R=r_st(E). Choose r_st=E/(E+i*Gamma/2), t_st=-i*Gamma/2/(E+i*Gamma/2). Then

S = diag(U-dagger,I,I) S0 diag(U,I,I)

is exactly unitary and has S46's interior scattering topology. For F=diag(f_L1,f_L2,f_R), outgoing occupations are the diagonal of S F S-dagger.

All sums are finite, so the two total-energy computations are algebraically identical:

sum_i E_i[(S F S-dagger)_ii-F_ii]
= sum_ij (E_i-E_j)|S_ij|^2 F_jj.

No rearrangement of divergent integrals occurs. The nonzero incoming-energy result resides in the boundary-corrected matrix elements that the unrestricted mean-n argument neglects. The result converges as the band edges recede.

## 4. One numerical counterexample using the paper's waveform

Use Gamma as the resonance full width at half maximum. Set delta/Gamma=1, s=0.1*pi, kB*T_L/Gamma=.2625, kB*T_R/Gamma=.2375, average mu/Gamma=1. The paper's linear-response load prescription gives delta_mu/Gamma=.331021682. Its exact pulse probabilities are p_-1=q, p_n=(1-q)^2*q^n for n>=0, q=exp(-2s); sum n^2*p_n=2.287136002.

All powers below are in Gamma^2/h:

- Gross DC output: .038256581.
- Paper zero-input accounting: hot heat -.167733188, nominal efficiency .228079970, compared with Carnot .095238095.
- Physical heat into L1: 1.143568001; into L2: .975834813; into R: .129476608.
- Full source input: 2.287136002.
- Net output after source input: -2.248879421. The hot contacts together receive, rather than supply, heat.

The outgoing-distribution calculation and exact finite-unitary calculation agree to about 1e-13 at N=128. N=64,96,128 gives source input 2.2871359788, 2.2871360019021, 2.2871360019034. Unitarity defect is below 9e-16. Zero drive restores AC input below 1e-14. Halving the energy grid spacing changes gross output by less than 7e-16. Directly optimizing gross DC output changes it only to .038302668, not the conclusion. Even charging only the forward channel's J_ex leaves negative net output.

## 5. Independent thermodynamic check

For thermal f and any occupation g, the Bernoulli relative entropy obeys exactly

kB[sigma(g)-sigma(f)] = (E-mu)(g-f)/T - kB*D(g||f).

Therefore the occupation-Shannon entropy flux minus physical Clausius heat flux is nonpositive. The paper's positive difference cannot simultaneously use the same modes, references and heat definition. This algebraic check does not assume that occupation-Shannon entropy equals the full coherent von Neumann entropy.

## 6. Strongest caveats and unresolved points

- An AC contact's local heat and laboratory energy differ by work terms. A different consistent gauge can redistribute those terms. Our construction includes the entry inverse phase before computing contact heat; a microscopic contact/circuit derivation remains worthwhile to verify the intended experimental boundary.
- The finite-ladder exponential is one controlled, unitary ultraviolet completion. It is not a unique microscopic Hamiltonian for every possible quantum Hall gate. Its agreement with convergent Fermi-edge differences and standard voltage-contact power is the relevant evidence.
- A prepared nonthermal input, coherent return loop, or extra work/entropy resource could permit a different resource comparison. None is included in the independent thermal inputs and topology audited here. Common drive phase alone does not create the necessary return-state correlation.
- This does not refute charge pumping, every plotted curve, or all nonthermal-engine advantages. The numerical example reconstructs the stated model and load prescription; it is not a digitization of a figure.
- Targeted searches found no accessible correction/comment identifying this edge issue, but were not exhaustive and establish no novelty or priority. No external publication or contact is authorized or undertaken.

Primary checks: Moskalets and Buttiker, PRB **66**, 205320 (2002), propagating-sideband restrictions, https://arxiv.org/html/cond-mat/0208356 ; Battista et al., PRB **90**, 085418 (2014), outgoing energy and contact voltage-work accounting, https://doi.org/10.1103/PhysRevB.90.085418 .

Reproduction: check_paper_model.py, check_paper_unitary_band.py and corresponding JSON outputs in this directory. CONTACT_AND_PRIORITY_CHECK.md preserves contact interpretation, source locations and search limits. ASSESSMENT.md contains earlier analytic and numerical adversarial checks.
