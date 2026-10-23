Conditional actual-circuit material-response exclusion (calculation16)

Actual input: coupled_bound/actual_voltage_path.csv, SHA256 in JSON, 961
samples, period8.048358436ms. Both bank voltages include3ms thermal holds,
the solved LC exchanges and finite30us corrections. No thermal route or
independent waveform was optimized here. Areas are ONE ten-film-bank area;
the average of both bank fullcycle losses equals pair-halfcycle normalization.

Same positive T-independent LTI Debye+DC spectrum for both banks, fitted to
the source initially uncharged voltage-step current at348.15K from1–10ms,
within declared±2pixel current uncertainty:

 SAME-SPECTRUM numerical minimum128.910969J/m2 perbankfullcycle; DC=0.
 401/801/1201/1601tau grids agree128.910970/128.910969/128.910969/128.910968.
 Half/twice/fourtimes uncertainty gives130.09784/126.66020/122.84729J/m2.
 Each branch state is periodic; reset residual<8.3e-13V. This is resistor
 loss with recovered capacitor state, not gross charging input.

ANALYTICAL ALL-TAU LOWER BOUND:108.116555J/m2 perbankfullcycle.
For any positive Debye spectrum and nonnegative DC conductance, at source
time t*>=P/(2pi):

 E_cycle >= [I_step(t*)/V_step] * integral(V-mean(V))^2 dt.

Proof: for each nonzero Fourier harmonic, set z=t*/tau and a=omega*t*>=1.
The derivative of log[exp(z)/(1+z^2/a^2)] is1-2z/(a^2+z^2)>=0. Hence
omega^2*tau^2/(1+omega^2*tau^2)>=exp(-t*/tau). Apply Parseval to exact
periodic RC dissipation, sum positive branches; DC obeys an even stronger
bound. No finite tau grid or assumption of a nonzero DC floor is required.
Actualpath ACvariance integral=.9314853071V^2s perbank. Source t*=1.286307ms
gives lowercurrent8.485207uA, omega1*t*=1.004193. Electrode area pi*(.1mm)^2;
multiply by10layers and divide byarea after applying the perdevice bound.

Candidate favorable gross=.162702J/pairhalf; unallocated matched-TE margin
=.025607J/pairhalf. The full source FE reversible rectangle is1.103311J/bank
for one monotone0<->23.27V excursion with T confined338..348K. Thus this LTI
response class cannot power the supplied cycle, even before other losses;
the all-tau bound also exceeds that caloric rectangle by98times. This is NOT
a measured cyclic-material loss bound, nor a conclusion about other trained,
nonlinear, thermal-history-dependent responses.

CAPACITANCE CONSISTENCY:
Loss-minimizing fit needs extraCeq=.176437F/m2 perfilm, extra equilibrium
stepcharge4.10569C/m2. The MINIMUM extraCeq over all compatible fits, allowing
DC, is.0283956F/m2 (stepcharge.660765C/m2); that minC fit loses179.084J/m2 on
this actualcycle. The source10kHz branch-average stepcharge is.376069C/m2,
secant.0161611F/m2. Therefore additive branches cannot leave the claimed
equilibrium G/Q(V) unchanged. However sourceqref is NOT measured equilibrium:
the optimum slowbranches add only1.65e-6F/m2 apparent parallelC at10kHz and
can be nearly invisible to that highfrequency curve. The sourcecurve alone
does not establish an equilibrium-capacitance contradiction. A physical
total model would require explicit internal states and refitted background,
with heat/charge feedback; the supplied reversible envelope is not that model.

The initially-zero step assumption is decisive and unverified: source
conditioning, instrumentation, domains, traps, thermal transients and trained
periodic state are not separated by the one trace. Do not substitute this
conditional class exclusion for an experimentally supported FE no-go.

Files: actual_cycle.py; actual_cycle_results.json; actual_run_log.json.
Replay from workspace: work/atomistic6/env/bin/python
work/electrical16/material/relaxation/actual_cycle.py
