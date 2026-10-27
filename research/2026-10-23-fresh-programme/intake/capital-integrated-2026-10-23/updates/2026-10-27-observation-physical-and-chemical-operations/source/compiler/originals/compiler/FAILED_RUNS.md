# Failed work retained separately from successful certificates

- Initial numerical acquisition used existing retained SciPy/NumPy. Its H03
  answer q=0 was exactly reconstructed; the separately constructed positive
  nondegraded example gave q=3/40. No numerical residual was treated as proof.
- First SymPy exact-backend adapter assumed every returned scalar had .p/.q;
  native Python integer zeros caused two AttributeError terminations before
  either new output certificate was written. Fraction(str(value)) repaired
  scalar decoding. Those failed processes count as failed setup/work, not
  mathematical negatives.
- More seriously, SymPy1.14.0 solvers.simplex.linprog returned objective0 and
  point[0,1,0] for the exact constraints of K=I_2,L=[1,1]. The point violates
  U_(1,0)<=K_(1,0)=0. The independent verifier rejected the candidate before
  acceptance. failed_sympy_backend_repro.py retains the exact minimal call;
  SYMPY_FAILED_OUTPUT.json records its result. This was a failed exact
  acquisition backend, not a theorem counterexample or an accepted certificate.
- Final acquisition replaces that backend with a standard-library rational
  simplex using Bland's anti-cycling rule, from the supplied feasible
  U=0,v=0 slack basis. Final independent primal/dual checks pass. The backend
  is ordinary optimization, not a new solver or a polynomial-runtime claim.

Research/source-discovery total time, software-provisioning before this
continuation, and all failed-work aggregate CPU/wall time were not instrumented
and remain UNKNOWN. FINAL_REPLAY.json separately measures the final selected
fresh processes; it is not a discovery-cost or total-scientific-effort measure.
The numerical-proposal timing fields exclude startup, imports and discovery.

- The first final replay's new forced-query runtime check hardcoded output2
  from the initial optimal table. Bland simplex selected the equally optimal
  table with the last two output rows swapped (K has identical such rows),
  whose queried raw0 outputs1. This was a stale expected-table test value,
  not a channel-law failure. The test now checks the compiled residual and
  callback/cost, and the displayed final table was reconciled with its file.
  The two separately valid rational optima remain preserved.
