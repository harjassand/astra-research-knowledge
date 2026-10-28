# Actual execution, including the presentation error

The full pixel consumer completed and wrote DATA_RECEIPT.json and
DATA_MOMENTS.json before its final display raised a KeyError. The display had
assumed a positive empirical normalizer and tried to print an optional
normalized-output key. The actual normalizer is negative, so that key correctly
did not exist. This was an avoidable display bug, not a lost image computation.
The guard was corrected in consume_images.py. The original source run was not
repeated merely to obtain a zero exit status; its3.194323-second computation
and failed final display are retained as the actual history.

The separate replay_record.py uses the saved integer moments and an O(n^2)
pair-difference covariance identity. It does not import the consumer and does
not claim independently to decode all pixels or verify the image-to-moment
stage. RECORD_REPLAY.json records its actual result and cost.

The source HTTP ZIP retrieval is public read-only acquisition. ZIP CRCs are
checked on all500 member reads; the whole archive SHA256 is recorded. These
are transport checks, not a validation of the Poisson, radial-PSF, aperture,
finite-lag or hydrodynamic model. No physical experiment was performed.
