# Active force-port experiments need not identify hidden dissipation

This independent companion gives an exact identification criterion and a minimal fully controllable/observable Langevin counterexample. Its complete [standalone construction and proof](package/companions/active_port_nonidentifiability.txt) is retained as a separate result from [mixed-bath quantum acquisition](README.md). It is a completed obstruction within its stated isothermal linear class, not a newly useful engine, an experimental demonstration or a historical-priority determination. No blanket inheritance of the main quantum proof audit is claimed.

## Observations, controls and exact criterion

All coordinates are even under time reversal; units have `k_B T=1`. Consider the stationary overdamped diffusion

```text
dX=[A X+D C^T u]dt+sqrt(2D)dW,
Y=C X,
D=-(A Sigma+Sigma A^T)/2 > 0.
```

`A` is known and stable, `(C,A)` is observable, `Sigma>0` is the stationary covariance and `u` is a true mechanical force conjugate to the observed positions. Allowed controls use the entire past output and independent randomness, with a well-posed causal solution. They cannot reset/measure hidden coordinates, change native mobility or access the hidden drive's supply. Each device starts stationary.

For two admissible stationary covariances differing by symmetric `Z`, the complete stationary Gaussian output laws **and** force-response kernels agree exactly iff

```text
Z C^T=0,
Z A^T C^T=0.
```

Output covariance is `C exp(At)Sigma C^T`, response is `C exp(At)D C^T`; known-drift observability gives necessity. The input/output identity `Y=Y0+H*u` then couples both devices using the same uncontrolled output path and controller seed. Every well-posed adaptive nonlinear force protocol has the same transcript, stopping decisions and observed work distribution. Unlimited exposure, bandwidth or precision at those same ports does not distinguish the models.

Complete covariance/mobility identification is possible precisely when `span{range(C^T),range(A^T C^T)}=R^n`. With `r` independent position/force ports, `n>2r` necessarily leaves an ambiguity despite ordinary dynamic controllability and observability. This is a parameter-identification criterion for the known-drift model; it does not say that every thermodynamic functional needs every parameter.

## Connected three-coordinate equilibrium mimic

Let `K=[[2,-1,0],[-1,2,-1],[0,-1,2]]`, `A=-K`, and observe/force coordinate one, `C=[1,0,0]`. For `0<=t<sqrt(5)-2`, set

```text
D_t=[[1,0,0],[0,1,t],[0,t,1-4t]],
Sigma_t=K^-1-2t e3 e3^T.
```

The drift input is always `e1 u` because `D_t e1=e1`. Deterministic controllability and observability are full rank, with determinant one; the native dynamics form a connected chain. Yet every stationary controlled transcript through that port equals the equilibrium `t=0` law, while entropy production is

```text
sigma(t)=4t^2/(1-4t-t^2).
```

It is zero at equilibrium, positive for every `t>0` and diverges at the boundary. Every member before the boundary is stable and strictly elliptic. The general companion proves the same construction for a symmetric positive `K` and a direction invisible to both `C` and `CK`; its closed-form entropy production makes the ambiguity explicit.

Unbounded dissipation across this class requires an increasingly singular mobility and divergent native-force matrix `-D^-1 K`. It is not an unbounded effect at fixed total hardware budget or accessible free energy. Equilibrium versus positive dissipation already remains ambiguous for small bounded perturbations. A quantitative hidden mobility/force bound is additional information and can restrict the upper range.

Observing coordinate three resolves its variance. Passively observing coordinates one and two while forcing only coordinate one still leaves this family identical; applying a true conjugate force at coordinate two changes its drift response and resolves the parameter. Known full-state resets can expose transients. Those are specific additional ports, not stronger processing of the unchanged data.

Since the same full data law occurs at zero and arbitrarily large entropy production, no procedure can uniformly give a finite upper confidence endpoint with nontrivial coverage over this unrestricted class. This does not deny accessible work: its distribution through the unchanged force/position port is also identical. Port-accessible work and total internal dissipation are different targets here.

The supplied note reports NumPy sanity checks of the algebraic formulas, Lyapunov equation, covariance equality and determinant; no physical experiment or new Capital calculation was performed. Hidden dissipation under partial observation, fluctuation-response methods, waiting-time lower bounds and linear-diffusion entropy-production formulas are established prior machinery. The exact adaptive conjugate-force ambiguity and known-drift span criterion are retained without a global novelty claim. [Full prior-art discussion](package/companions/active_port_nonidentifiability.txt), [selection record](package/SELECTION_RECORD.txt), [original provenance](SOURCES.json).
