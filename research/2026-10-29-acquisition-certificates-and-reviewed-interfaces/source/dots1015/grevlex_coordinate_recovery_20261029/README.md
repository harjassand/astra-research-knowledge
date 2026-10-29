# No-local-optimizer feasible-candidate recovery: executed diagnostic

This is a separate continuation of the frozen grevlex value oracle. It does not modify that packet. It addresses the fallback case where an ordinary local optimizer fails to produce a useful feasible upper bound.

## Executed results

`check_adjugate_coordinates.py` computes the field-linear matrices and the weighted adjugate traces N_j(t)=tr[M_j adj(tI−M_lambda)] over three primes. If p(t)=t^40+c39t^39+...+c0, set B0=I and Bk=L B(k−1)+c(40−k) I. Then adj(tI−L)=sum(k=0..39)t^(39−k) Bk. All three finite-field identities M_j p′(L)1=N_j(L)1 pass. This is a modular diagnostic, not an exact rational identity proof.

`reconstruct_coordinate_candidates.py` reconstructs three rational degree≤39 numerator candidates after336 primes/7814 modulus bits in12.76s. Maximum numerator/denominator heights are3452/3769 bits. A fresh prime agrees. These are still candidates: no rigorous height bound or direct exact quotient identity is supplied for these numerator polynomials.

Nevertheless, they are useful as an untrusted candidate finder. `recover_feasible_candidate.py` isolates the least root of the already exactly verified value polynomial to width2^-100, evaluates N_j/p′ at its rational midpoint, and obtains chart coordinates approximately(1.0000005608256,1.00000033203075,1.00000028459786). It constructs an exactly rational unit quaternion by stereographic rounding, verifies its norm and evaluates the original quartic exactly. This gives a certified original-objective global gap1.190011164703136e−5 <1e−4 in2.11s, without invoking any local optimizer. The exact feasibility/upper bound is independent of whether the provisional coordinate identities are correct. The lower bound is inherited from the reviewed grevlex value polynomial and re-isolated exactly. This is a valid instance certificate, not a theorem that the untrusted finder succeeds on all inputs.

The stored `feasible_candidate_certificate.json` contains the rational unit quaternion and exact upper/lower/gap. No SOS positivity shortcut or known minimizing vector is fed to this finder.

## Failed double-precision left-eigenvector route

`check_left_eigenvector_numeric.py` tests a materially different representation: the evaluation left eigenvector of M_lambda. Direct binary64 construction is badly conditioned here: estimated condition number of M_Q is1.75e32. It selects a spurious nearby complex eigenvalue and has normalized residual5.5e−4; the inferred coordinates are wrong. These data are retained explicitly as a failed numerical implementation. They do not refute the exact left-eigenvector method. A rational/interval high-precision solve with an inverse perturbation bound would be needed to certify that method; it is not supplied here.

## Reproduction and dependencies

Run the three scripts `check_adjugate_coordinates.py`, `reconstruct_coordinate_candidates.py`, `recover_feasible_candidate.py`, with OPENBLAS_NUM_THREADS=1 if desired. They import the frozen grevlex packet at `producer-workspace/grevlex_value_oracle_20261029`; this is an explicit dependency, not a hidden shape/FGLM import. The fourth numerical diagnostic is optional. Inputs are the received exact quartic, its grevlex coordinate matrices and its exact value polynomial. No stationary coordinate representation from the old fixed-z shape is used.

Established adjugate/trace/CRT methods are not claimed as novel. The new evidence is execution on this retained diagnostic and an exact useful output checked independently of the uncertain finder.
