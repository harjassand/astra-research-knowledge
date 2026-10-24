# Exact ratio one does not preserve a nonzero information budget

24 October 2026. New receiving use of standard channel-information bounds to interpret the exact coefficient families. The capacity bounds themselves are established prior science, not inventions here.

## Classical transmitted channel with quantum side information

Let X be the classical channel input, Y its output under K, U a message, and R arbitrary quantum side information. The Markov property Y independent of UR given X and the chain rule imply
I(U:Y|R)<=I(X:Y|R)=H(Y|R)-H(Y|X)<=I(X:Y)<=C(K).
This holds for the actual cq state, not a classical replacement for R. If U and R are initially independent, I(U:YR)=I(U:Y|R), so the same ceiling applies to total information about the new message available to the receiver.

For the n-symbol complement channel K(y|x)=1/(n-1) when y!=x,
C(K)=log n-log(n-1),
because each row has entropy log(n-1) and uniform input maximizes output entropy.

Yet the new exact complete and conditional relative-entropy coefficients equal ONE at this negative reset endpoint. The ordinary and single-ensemble cq MI coefficients equal1/(n-1). These facts are compatible: conditional fraction-retention near one can occur only at small enough absolute message information. The capacity ceiling tends to zero as n grows. Increasing the alphabet does not create a finite-rate almost-noiseless channel.

## Quantum transmitted channel

For any channel N:A→B, I(U:B|R)<=I(UR:B). Every extension UR of the channel input can be obtained by a channel on a purification of its A marginal. Data processing therefore bounds this by
C_E(N)=max_a I(A':B)_(id tensor N)(psi_a),
the standard entanglement-assisted channel mutual information. Hence imposing I(U:A|R)>=delta>0 yields the safe ratio ceiling
min{eta_conditional(N), C_E(N)/delta}.
It is an upper bound, not an assertion that the coefficient maximizer and capacity maximizer are compatible.

For the d-dimensional negative-endpoint depolarizing channel lambda=-1/(d^2-1), irreducible unitary covariance and concavity of channel mutual information make the maximally mixed input optimal. Its normalized Choi state is (I-Phi_d)/(d^2-1). Thus
C_E=2log d-log(d^2-1)=log[d^2/(d^2-1)],
while the complete and conditional coefficient is one. The capacity ceiling is O(d^-2). This is a sharp illustration of the distinction between a ratio supremum and a task carrying a fixed amount of new information.

For d2, the finite balanced CMI witness in complement_balanced_interval.json has input .00751934nats, output .00456634nats and ratio .60728. It is well below the standard absolute ceiling log(4/3)≈.287682nats. Its gain is in incremental-information contraction, not a communication-capacity violation.

## Provenance and limits

The single-letter entanglement-assisted capacity framework is Bennett–Shor–Smolin–Thapliyal, https://arxiv.org/abs/quant-ph/0106052. Classical symmetric-channel capacity and the chain-rule bounds above are ordinary comparators. No hardware preparation, decoded-rate demonstration, free entanglement, energy saving, or historical novelty is claimed. The useful consequence here is choosing an information contract that cannot be gamed by vanishing signals or expanding unused reference space.
