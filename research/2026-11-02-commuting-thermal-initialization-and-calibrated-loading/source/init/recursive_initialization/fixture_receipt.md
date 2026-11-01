# Actual local recognizer and full-stencil trace tests

2026-11-01. Executed exact integer GF(2) fixtures; no mocked syndrome constraints.

## 1. Exhaustive one-square Bell RX ell3

`actual_rx_recognizer_fixture.py` retains all19 qubits and12 Z checks of the actual one-square replacement. The syndrome image has rank11.

All4096 possible syndrome strings were tested: exactly2048 accepted and2048 rejected, matching global image membership for every input. All accepted reconstruction identities, intermediate weight nonincrease and parent halving checks passed.

The implemented full-input/full-output-stencil circuit has41 gates,135 host objects, maximum host degree26. Its2071 isolated accepting-component replays all reproduce exactly the original component's marked objects AND wire values, and are globally valid syndromes. There are24 accepting inputs with two genuinely separate components. Maximum observed trace-size/syndrome-weight ratio is51.

This explicitly exercises cancellation gates rather than marking only nonzero outputs.

Results: `actual_rx_recognizer_fixture_results.json`.

## 2. Main [[5,1,2]] seed RX ell3

`actual_main_seed_recognizer_test.py` uses the actual Eq.108 seed, with60 fine qubits and38 Z checks, syndrome image rank35.

All local primitive tables were exhaustively built and checked: both Cx tables have256 entries; the four corner-Q tables have8 entries each, and the central-Q table has32. Every locally solvable input has a correction satisfying the source outgoing-weight bound. This fixture includes nontrivial Q-gadget cycle constraints absent from the single-square case.

6039 syndrome strings were tested, including3000 generated-valid inputs,3000 arbitrary inputs, zero, and every singleton check syndrome. Localflags plus diagonal/finite-parent verification agree with global image membership on all tested inputs. Of the3000 arbitrary inputs,378 accepted and2622 rejected. Every accepted correction reconstructs the original syndrome exactly; intermediate nonincrease and RX halving pass.

Results: `actual_main_seed_recognizer_results.json`.

## Scope of fixtures

These fixtures validate the local RX recognition/compiler mechanism and the abstract trace splitting on a concrete replacement. Their finite bottom decoders are fixtures, NOT replacements for the matched §5.1.1 level-2 terminal decoder required by the full memory theorem. The all-level binding proof explicitly preserves that O(ell^4) terminal macro-gate and its established correction choices. No noisy physical loader is tested here.
