# Independent review: source-feedback extension

Reviewed `pilot_reconstruction/FEEDBACK_DERIVATION.md` and executed `pilot_reconstruction/feedback_check.py` successfully. The exact rational arithmetic and finite fixed-N balance assertions pass. No empirical source-response parameter has been identified by this calculation.

## Verdict

The derivation and the three affine examples are correct as a logical non-identification argument. A single baseline measurement of epsilon, A, R and Q does not identify the derivative of the source map or the response to a finite absorber change. The extension goes beyond the fixed-source/survival example without incorrectly interpreting a gain greater than one as a survival probability.

The strongest defensible conclusion is: **the baseline and proposed capture fraction alone do not establish the sign of whole-loop productivity change within the unrestricted source-response class.** This is not evidence that the actual plasma source has positive recycle stimulation, or that an actual 90% absorber worsens production. A physical restriction on source response could restore a sign conclusion; it must be established, not presumed.

## Algebra and numbers checked

With R=(1-epsilon)A, A=f(R), Q=epsilon A, define D=1-(1-epsilon)f'(R). Implicit differentiation at D nonzero gives

A'=-A f'/D,
Q'=A(1-f')/D.

Therefore, for A>0 and D>0, Q' is positive, zero or negative according as f' is below, equal to or above one. This conclusion requires the same f under the intervention and specified other controls. If absorber replacement changes independent source controls, the total derivative includes those changes; they cannot be hidden in a scalar fixed-f formula.

For f(R)=c+gR and c=1-.35g, the three examples share epsilon=.65, A=1, R=.35, Q=.65:

- g=0: c=1; upgraded Q=.9; fixed-power SEC ratio=13/18.
- g=1: c=.65; upgraded Q=.65; SEC ratio=1.
- g=1.5: c=.475; upgraded A=19/34 and Q=171/340; SEC ratio=221/171, approximately 1.29240.

The last model admits the exact decomposition A=R+S(R), S(R)=.475+.5R. Thus survival is one, not 1.5, and the additional response is fresh formation. At baseline S=.65; at the upgraded steady state S=171/340. Fresh formation remains positive at every nonnegative R. This provides a nitrogen-balanced mathematical map; positivity alone does not validate its kinetics, heat balance, energy efficiency or achievable operating domain. All values are normalized logical examples, not proposed apparatus performance.

## One necessary stability qualification

D>0 alone is not sufficient for stability of the discrete pass map A_next=f((1-epsilon)A). Its local stability criterion is

|(1-epsilon)f'(R)|<1.

Large negative slopes can have D>0 while violating this criterion. If the document's wording means an independently stable branch that also has D>0, it is valid, but should explicitly distinguish these statements. For all three affine examples, 0<=g<=1.5 and .65<=epsilon<=.90 give 0<=(1-epsilon)g<=.525<1. Hence they are stable throughout the full interpolation interval, not merely at both endpoints. Actual delayed/multistate plant dynamics need not have this scalar pass stability criterion.

The code checks g(1-epsilon)<1 rather than its absolute value; that is sufficient for the three explicitly nonnegative gains used. An absolute-value assertion would be safer if the example set is later generalized. The comment claiming the finite-difference sign matches the derivative is correct here; adding an explicit assertion would make the check executable rather than only documented.

## Scope of inventory and energy tests

The 12-pass recurrence conserves new fixed nitrogen exactly as product + destroyed/lost nitrogen + final retained inventory, with initial inventory zero. The terminal inventory has not yet passed through another survival/destruction step, correctly matching the chosen terminal boundary. This is a discrete mass-balance demonstration, not a dynamic fit or a physical 12-pass runtime forecast. Unequal initial inventory requires adding initial retained nitrogen to the input side. Acid held in columns must be assigned to product or inventory once, not both.

For fixed complete electric power, SEC ratios are inverse product ratios. If power changes, the logarithmic derivative E'/E-Q'/Q is correct. For a finite practical comparison, integrated energy per equal specified product, with measured initial/final inventory and thermal/pressure reset state, is needed. Improved capture may also change circulation time, pressure drop, plasma throughput or source composition. A dimensionless per-pass model must not silently be read as a comparison at unchanged production per hour.

## What measurement closes the claim

A local controlled return perturbation identifies only a local derivative. To predict the finite .65-to-.90 intervention, determine the source response over the traversed return interval and establish that other state variables and the source map remain applicable, or perform the actual matched paired complete-operation comparison. Under these affine examples the required interval runs from baseline R=.35 to the respective upgraded return, not just an infinitesimal neighborhood around .35.

Paired inlet/outlet fixed-N molar flows can identify the net source map without resolving every microscopic formation/destruction pathway. A multivariable response is needed if O2/Ar fraction, humidity, temperature, pressure, total flow or quench history change. Measuring the direct full-operation product and energy response can settle practical ranking without a scalar source-map model. The derivative result is elementary feedback algebra, not a new physical theorem or a substitute for those measurements.
