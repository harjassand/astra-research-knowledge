ASTRA: LEARNING REUSABLE CONTROL FROM NOISY SPARSE EXPERIMENTS
1 November 2026

Read Astra_Reusable_Control_20261101.pdf first. The complete scientific record
is in this archive; there is no claim that it has been published to GitHub.

PRIOR SOURCE PIN
https://github.com/harjassand/astra-research-knowledge
51ce47ce39f976517d60e2f87bbe280b651f6056
Only this corpus was used for prior Astra research. Accepted premises retain
their actual conditions. Source paths and exact hashes are in SOURCE_BINDINGS.json.

MAIN PROOFS
work/physical/NOISY_ACQUISITION_PROOF.md
  Positive-rational finite noisy acquisition, precise constants, cost and priors.
work/control/CONTROL_CONSUMER_PROOF.md
  General offline convex decision consumer, exact task certificates, acquisition
  from bounded sensors, noise lower bound and executed results.
work/comparators/RESISTOR_NETWORK_LOWER_BOUND.md
  Literal positive-conductance circuit twins and matching experiment-order law.
work/comparators/INTERVENTION_ORDER_LOWER_BOUND.md
  Inherited dark-path lower bound, quantified asymptotics, single-bright cycle,
  conventional comparisons and quantum alternative screening.
work/comparators/PAIR_BLIND_CONTINUOUS_REGRET.md
  Additional five-control continuous-decision obstruction; its finite remainder
  makes the displayed bound informative only at high total strength.
work/physical/PASSIVE_NETWORK_BINDING.md
  General ideal-circuit supplier, warranted scale and physical costs.

SCOPE THAT MUST TRAVEL WITH THE RESULT
The exact physical source family, fixedness, positive dose language, correct
scalar intervals and future constraint/oracle access are inputs. They are not
learned merely by fitting. The factorial law concerns simultaneous experiment
support, not total settings. Generic uniform budgets can be enormous. The
three-control example retains full rational degree and demonstrates task-local
regret certificates; it does not establish tiny uniform error, a hardware
performance gain, large-system scalability or historical novelty.

MAIN EXECUTED EXAMPLE
work/control/network_results/
  Four-node ideal resistor emulator,84 source settings including shared noisy
  baseline,14 retained coefficient variables,32 exact LP-dual certificates,
  four future tasks and zero additional source readings.
work/learning/independent_network_control_validation.json
  Independent exact check using only scalar/current records, public specs and
  saved duals. Certificate validity PASS. Two of the four original2e-5 normalized
  regret targets were MISSED; their actual upper bounds remain valid.
work/control/results/
  Separate earlier singular-Gram emulator; preserve its different source scope.

REPRODUCE EXACT CHECKS (Python standard library only)
Run from the extracted archive root:

python work/learning/validate_control_certificates.py --data work/control/network_results --output work/learning/replayed_network_validation.json
python work/learning/validate_control_certificates.py
python work/learning/check_rational_norming.py
python work/comparators/check_resistor_network_lower_bound.py
python work/comparators/check_intervention_lower_bound.py
python work/control/budget_bounds.py

GENERATE NEW FITS/PROPOSALS (requires numpy and scipy)
python work/control/control_demo.py --fixture network
python work/control/control_demo.py --fixture gram

The numerical solvers only propose fits, actions and duals. Saved certificates
are validated with exact fractions. Different numerical library versions may
propose different certificates; the archived exact checker needs no optimizer.
The source matrices are used only in emulation and separate truth diagnostics,
never as learner/certifier inputs. The independent validator does not import
the generating program or read its source-truth report.

INDEPENDENT SCOPE RECORDS
work/learning/independent_noisy_rational_review.md
work/learning/control_certificate_review.md
work/learning/network_control_review.md
work/physical/CONSUMER_REVIEW.md
These are substantive internal challenges, not external or formal validation.

PRIMARY RESEARCH
The report and main proof credit interval-rational approximation (Salazar Celis,
Cuyt and Verdonk2007), rational interpolation error (Cuyt and Yang2010), modern
positive-denominator rational fits (Chok and Vasil), linear-fractional
programming (Charnes and Cooper1962), and known-model convex network design
(Ghosh, Boyd and Saberi2008). External manuscripts are not republished here.

USEFUL FAILURES PRESERVED
1. Prior rare-event resolvent accuracy does not give multiplicative survival
   accuracy: exponential lifetimes can have close resolvents but unbounded
   survival ratios over long horizons.
2. Generic no-reset quantum formulations did not beat strong existing machinery.
3. Nonphysical rational fits need not be concave; source concavity must be used
   through a valid value-oracle or derivative certificate.
4. One-at-a-time and pair tests can miss a real joint response.
5. Moderate-q uniform sufficient budgets are impractical, although actual
   task-specific LP certificates can be much tighter.
6. Shared baseline error caused two initial numerical target misses, retained
   without tuning the source data or replacing the target.

The PDF source is included. Build it with xelatex twice if desired. The provided
PDF has been rendered and visually checked. All local sources and programs
needed for the reported claims are included; no private data service is needed
for replay of the exact checks.
