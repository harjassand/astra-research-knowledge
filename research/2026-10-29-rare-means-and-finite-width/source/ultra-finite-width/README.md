# Fixed-coupling nonlinear eta-background impurity receiver

Governing result: `PROOF.md`, with honest prior/capability disposition in
`PRIOR_AND_DECISION.md`. Root whole intake is recorded separately.

At the supplied ideal 4x4 open Hubbard source U/J=8, density one,
epsilon/J=.05 and time10/J, the physical source density excess lies in

    [-0.28709904883586866, -0.28619395337614108].

The exact two-particle linear response is separated by at least .0084303.
The nonlinear run used 328257 amplitudes, 2160 matvecs and10.7655s of
propagation. No laboratory state, experiment or generic thermal-state
closure was acquired.

Commands (use the repository sol8 solver-runtime Python):

    python check_native.py
    python native.py --nx 4 --ny 4 --cutoff 3 --out PREDICTION.json
    python compare_linear.py
    python receive_result.py

The receipts are frozen; rerun into a separate destination if necessary.
`check_native.py` independently reconstructs finite CAR/eta/native signs;
`receive_result.py` performs exact final interval composition without
repeating propagation. Float displays are not authoritative in place of
the scalar rational upper bounds.

The generic operation is already available from known eta symmetry and
bounded-source Dyson/Fock truncation. The branch is DEPRIORITIZED as a
new foundational capability. Its positive output is a restricted
nonlinear prediction and a transparent return-path error theorem; the
generic finite-width/resonance problem remains open here. The exact
extensive-source binomial counter prevents a fixed-defect promotion.
