# Integer implementation of the spectral-test sample budget
2026-10-29. Additive author clarification; no accepted files changed.

Let M=2^b be the QPE resolution and s the odd repetition count. Each controlled evolution is exp(i*pi*2^j*tau), j=0,...,b-1. Replace its time by the rational upper bound u_j=4*2^j and let U=4s(M-1). For each occurrence use
 n_j=ceil(u_j)+ceil(32*u_j*U/delta_inst)
fresh samples. Then n_j>=|t_j| and 32*t_j^2/n_j <= delta_inst*u_j/U. Summing over all occurrences yields at most delta_inst diamond simulation error. This is an exact integer policy using rational delta_inst, with no hidden transcendental rounding decision. It uses at most U+32U^2/delta_inst+2sb samples. Known rotations by multiples of pi remain explicitly synthesized controls with a separate summed channel-error budget.

For the composition theorem, split the declared instrument budget between DME and known-gate synthesis (for example half each); substitute delta_inst/2 into the above sample policy. The total implementation still obeys the declared delta_inst bound, increasing only the numerical sample constant.
