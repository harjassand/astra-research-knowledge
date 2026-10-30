# Binding correction: the native-profile relative entropy is a sum

30 October 2026. Root's actual receiving read found a displayed-formula
transcription error in equation (20) of
SINGLE_FILE_CONTACT_CONTROLS_NATIVE_DENSITY.md, SHA256

b0101449c47336f52ca40d040fdc0a0541dc8ea01867110196f79af49186dd94

The original bytes remain unchanged and are also snapshotted in
receiving_review. The correct functional in (20) is

\[
\mathcal V(\rho_*)=
\int_0^1
\left[
\rho_*(x)\log\frac{\rho_*(x)}{\rho}
+(1-\rho_*(x))\log\frac{1-\rho_*(x)}{1-\rho}
\right]\,dx.
\]

The plus sign between the two Bernoulli terms was missing in the original
display. They are added, not multiplied. This correction is binding for
equations (20)--(21), the positive density-preparation cost, and the role
summary. The binomial-counting proof and the stated Pinsker lower bound
already use this sum. No stationary-law, physical-current or operating-work
identity changes. No new fixture was required.

