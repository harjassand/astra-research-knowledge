# Synthetic contraction fixture

This is an exposed architecture fixture, not an invention, research discovery,
measured device, independently reproduced simulation or performance trial.

For supplied exact rational state x_0 = 1 and supplied recurrence x_(k+1) = x_k/2,
induction gives x_k = 2^(-k). Therefore four updates reach error at most 1/16.
This internally reconstructed elementary identity applies only to this recurrence.
The script uses exact rational arithmetic; it does not estimate an unknown rate.

A fixed ten-step reference uses ten updates. An equally informed stopping control
uses four, exactly as the candidate. No algorithmic advantage over that control
is demonstrated. Update counts omit acquisition, checking, representation growth,
wall time and energy. Those quantities are unknown, not measured zero.

The proposed computational implementation is a termination scheduler for a toy
solver. An independent software benchmark would test matched accuracy and total
acquisition, checking and execution costs on preregistered cases. No such benchmark
has run. A useful general solver would additionally need to acquire a certified
contraction bound through its permitted input interface. This acquisition problem
is a reverse handoff to theory; the supplied bound does not solve it.

No claim about physical controller stability, manufacturability, energy savings
or real-world best-known performance follows from this fixture.
