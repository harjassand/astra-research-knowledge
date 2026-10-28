# Raw-image mechanical-query investigation

Start with RESULT.md. The general operation is in PROOF.md; the improved
difference-image estimator and its precise variance scope are in
DIFFERENCE_RECEIVER.md. LITERATURE.md preserves the strong ordinary methods
that supplied much of the machinery.

The actual public input is data/MS_Images_H015.zip. It is a rectangular-jet
image record, not an annular torque record. DATA_RECEIPT.json and
DATA_MOMENTS.json preserve the executed finite-pixel query. The empirical
normalizer is negative, so there is no normalized physical output.

To replay the complete pixel computation, with NumPy and Pillow available:

```sh
producer-workspace/python3 producer-workspace/consume_images.py
```

To replay only the saved-record covariance and rational variance arithmetic:

```sh
python3 producer-workspace/replay_record.py
```

The original pixel run completed the scientific output files and then hit a
display-only KeyError. EXECUTION_NOTE.md preserves that fact and the guard
correction without inventing a rerun. COST_SCOPE.json, source/data acquisition
receipts and SOURCE_STATE.json retain costs, the incomplete Neal PDF and the
unused Cambridge fallback.

No physical experiment or qualified torque estimate was acquired. No priority,
general-purpose blur invention, practical advantage or completed civilization
level capability is claimed. The internal mathematical construction and the
native admission failure are both retained.
