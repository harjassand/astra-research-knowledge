# Independent cycle-flow normalization check

This supplements the earlier pending mechanism note. It uses the same precise
bundled cycle, not a stationary distribution for the fixed-mass internal fiber.

Let T be the first core event from a seeded state, except that a last-seed death is
followed by its A-zero wait and restoring immigration. Write u,d,z for the up,
down,zero probabilities. The number B_T of physical immigrations during the cycle,
**including its terminal endpoint**, is exactly one on up or zero and zero on down.
Thus `E_x B_T=u(x)+z(x)`.

The physical immigration process has constant rate lambda. Optional stopping its
compensated counting process at `T intersect [0,m]` gives
`E_x B_(T wedge m)=lambda E_x(T wedge m)`. Both sides pass to their limits by
monotone convergence; the previously established integrable cycle bound suffices.
Consequently

```
lambda E_x T=u(x)+z(x) <=1
```

pointwise. There is also a direct pathwise bound: let J be the next physical
immigration time. An up cycle ends at J, a down cycle ends before J, and a zero
cycle waits at A=0 until J. Therefore `T<=J` and `E_x T<=1/lambda` without any
conditional independence assertion about the pre-extinction and post-extinction
waits. Suppression of seed loss is not involved.

For a stationary embedded law nu, its already-proved exponential moment integrates
N. Since total-count increments are +1,-1,0, stationarity gives `nu(u)=nu(d)`.
Together with u+d+z=1,

```
lambda E_nu T=nu(u+z)=(1+nu(z))/2,
1/(2lambda)<=E_nu T<=1/lambda.
```

The lower bound is **stationary-average only**, not a pointwise holding-time bound.
For example an A-only state with large A has mean cycle time
`1/(lambda+mu A)<1/(2lambda)`. The upper bound is pointwise.

Within a cycle, except at its terminal endpoint, N never exceeds its starting
value. An endpoint birth is included in B_T but has zero duration in the occupation
integral; these conventions are consistent. Hence

```
E_nu integral_0^T t^N(s) ds <=(1/lambda)nu(t^N),
pi_cont(t^N)<=2 nu(t^N).
```

The older `H=1/mu+1/lambda` conditional bound, Jensen denominator, and
`2lambda H nu(t^N)` flow bound remain valid conservative comparators. The sharper
bound does not require acquiring nu, nu(z), a fiber law, or a different sampled
kernel. It uses only the already-earned stationarity identity and the fixed-rate
immigration clock.

The independently solved killed-fiber systems verify the pointwise identity
`lambda E_xT=p_up+p_loss` exactly in all 285 tested states. Their four right-hand
sides include both p_up and the physical seeded duration: these satisfy
`p_up=lambda*h_seed` by the same killed matrix. These finite exact checks do not
stand in for the ordinary all-state compensator/pathwise proof.
