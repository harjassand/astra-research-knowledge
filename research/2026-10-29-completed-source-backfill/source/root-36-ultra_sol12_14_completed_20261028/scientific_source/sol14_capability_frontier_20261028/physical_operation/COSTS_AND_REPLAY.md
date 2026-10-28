# Source, resource and replay contract

## Exact target

Input: contaminated solid aluminum feed, a paid liquid-Ga intermediary and ionic-liquid electrorefining apparatus, with a qualified common-regime activity/kinetic/transport model.

Desired output: continually replenished and harvested useful Al at declared purity, yield, throughput and full-cycle cost, rather than one finite dissolved-Al charge.

What was acquired: a model construction, an independently solved ordinary BVP control, explicit countermodel purity/flux thresholds, current source navigation, primary literature observations and a failed capability claim. No material specimen or measured operating regime was acquired.

## Source acquisition

The public Astra HEAD was verified at intake and pinned to 97970d87d04c7b0c932c69d3403b155d844acfc6. The task-first interface, technology navigation and canonical current metadata were fetched into sources/. Their exact byte hashes are in sources/ACQUISITION.json. A focused metadata search for electrorefining, aluminum scrap and liquid gallium produced no exact current-record match; this is not a novelty clearance.

A few material capability records were inspected as navigation leads. No Fe/CNT mobility, optical lattice-repair law, old powder-volume theorem, thermal result or quantum result was imported as an Al-process input. External and old science roots remained read-only.

Primary source observations and unacquired regimes are in sources/PRIMARY_INPUTS.json. The 2003 ordinary-process PDF was acquired from the journal's DOI service and its text extracted locally. Its PDF hash is recorded in sources/primary/receipts.json. The 1999 Ga study was read through its author-institution abstract. Full underlying potential/activity/temperature conventions were not acquired.

One attempted 1999 PDF download returned a browser-validation HTML page. It was identified by its missing PDF signature and was not counted as a paper; only the failed acquisition receipt is retained. The publisher full-text routes for the 2020 and 2026 papers were unavailable, so primary publisher abstracts/search-visible passages were used at their actual scope. A separate 2008 primary abstract was read; its PDF fetch timed out. No paywall was bypassed, access bought or experimental action taken.

## Numerical inputs versus acquired observations

The program makes its hybrid nature explicit. It does not certify common-medium Ga and Al diffusivities, concentration standards, activity coefficients or temperature transfer. Metal-host diffusivity/concentration, geometry, viscosity, rotation, dilute trace-species approximation, reversible Ga interface and absorbing collector are supplied parameters.

The numerical Ga purity gates are design choices. They are not claimed universal alloy specifications. The Al-complex single-species transport expression is not a fully coupled electrolyte limit. Levich scaling is an ordinary transport model granted to both routes, not a demonstrated hydrodynamic law for a supported rotating liquid-Ga film.

Actual source kinetics can rescue or worsen a model prediction. In particular, Ga(III)/Ga(I) rates measured on tungsten or carbon cannot pay the missing Ga(I)/liquid-metal rate. This distinction is central to the stopping decision.

## Equally informed ordinary controls

- The direct solid-anode alternative receives qualified surface renewal, electrolyte stirring, cathode optimization and the same information. It is not forced to operate with an arbitrarily passive anode.
- A generic numerical Nernst–Planck BVP is solved with the same finite kinetic boundary conditions, confirming the closed transport expression.
- The stronger ordinary hydrodynamic comparator uses species-dependent diffusivity scaling. Its correction improves the new candidate and changes the 1 ppm window. Both results are retained.
- Constant potential is the matched control for the supplied pulsed-potential/Tafel model. Its conditional Jensen result does not apply automatically to acoustic surface renewal or to a changing material interface.
- The ordinary literature comparison charges its own recovery, heat, ultrasound/stirring, residue, bath lifetime and product costs. No full-cycle superiority is awarded merely from reported cell energy.

## Complete resource boundary

The liquid-host route owes the Ga inventory and preparation, feed activation/contact, stable supports/wetting, pumping or rotation, ionic-liquid manufacture/purification/loss, containment, reference calibration, power, heating, feed and product assays, residue handling, Ga recovery, cathode harvesting and failed material. Continuous output beyond preload and host lifetime are required.

The active-area/host extrapolations are explicit scenarios, not industrial lower bounds. No free arbitrarily thin stable film, fast Al supply from real dirty scrap, invariant bath, pure cathode or indefinitely reusable Ga is assumed as an acquired capability.

Available primary observations support laboratory electrorefining; usable industrial material yield, component properties, dynamic purity tails, energy per saleable kilogram and equipment economics remain unknown here.

## Computation and replay

No packages were installed. The existing sol8 Python environment supplies NumPy and SciPy. Source-PDF text extraction used the existing bundled pypdf runtime. The scientific calculation is small local CPU work, approximately 0.02–0.04 s in the recorded runs; it is not a general speed advantage or an experimental acquisition cost.

From the workspace root:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol14_capability_frontier_20261028/physical_operation/code/redox_transport.py

Outputs are confined to this owned folder. The JSON retains every supplied model parameter, both transport comparisons, the BVP errors, rescue thresholds, finite inventory and decision. Replay can change elapsed-time metadata; freeze a new manifest after an intentional rerun.

The producer-authored code/freeze_receipt.py consumes the saved outputs, checks the source hashes and Levich correction, then writes the final receipt and manifest. It is a replay/provenance consumer, not an independent scientific review.

No agents or new worker contexts were spawned. No goals, automation, paid compute, purchases, public writes, Capital edits, outreach, biological engineering or physical actions were performed. Earlier sol9–sol12 results remain frozen.
