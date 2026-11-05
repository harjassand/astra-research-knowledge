# Primary comparisons for the universal passive response construction

These are comparison notes, not a claim of exhaustive novelty search. The theorem's contribution must be evaluated as its complete physical operation and quantifiers. Classical linear response, passive realization, nonparametric identification, handling unknown initial state, and learning without mixing already have substantial literature.

## Unknown initial state is not a new subject

A. E. Pearson, *Finite time interval linear system identification without initial state estimation*, Automatica 12(6), 577-587 (1976), DOI:
https://doi.org/10.1016/0005-1098(76)90039-X

The primary abstract gives a finite-interval deterministic least-squares construction for a class of differential systems that avoids estimating the initial state. It treats certain unknown disturbances as free differential-equation responses and requires independence of data functions and derivatives for uniqueness. Therefore avoiding initial-state reconstruction by itself is not a novelty claim available to this programme.

## Learning without a mixing-time factor is established

M. Simchowitz, H. Mania, S. Tu, M. I. Jordan, B. Recht, *Learning Without Mixing: Towards A Sharp Analysis of Linear System Identification*, COLT 2018:
https://proceedings.mlr.press/v75/simchowitz18a.html
https://proceedings.mlr.press/v75/simchowitz18a/simchowitz18a.pdf

This paper gives nearly minimax ordinary least-squares guarantees for linear dynamical systems and replaces standard mixing arguments by a dependent-data small-ball analysis. Its initial state-space model has finite observed state dimension; later related work also treats partial observation. Claims that this new construction is the first finite-sample identification without mixing would be false.

## Simulation accuracy from bounded noisy data is established

*Set Membership identification of linear systems with guaranteed simulation accuracy* (2020):
https://arxiv.org/abs/2001.07628

The primary abstract describes finite sampled data with bounded measurement noise, estimation of noise and decay bounds, stable identified models and both input-output/state-space structures. It is a serious comparator for any broad claim about certified acquired simulation. The exact governing assumptions should be inspected in the full paper when making a detailed rate comparison.

## Passive reduction and physical structure

The earlier completed scalar bridge already compares Bockius et al.'s extended Markov realizations, Lang--Lu's GLE identification/perturbation analysis, and accepted Astra N1688. Those comparisons remain part of this result. The new construction uses a different target: the full measured step response at a permanently loaded physical port, with randomized initialization of the unknown retained state. It should not be presented as a new exponential-compression rate or an improvement of stochastic GLE guarantees.

## Precisely supported distinction

The constructed operation is uniform over a supplied LTI passive class with a known observable dissipation inequality and finite total energy, without a supplied finite hidden order, hidden relaxation gap or ready-made zero-state preparation. A permanent known trap supplies coercivity and a finite actuator interface. The random quiet-window event, finite-box step acquisition, metrology/force budgets and finite response evaluation are joined explicitly.

That is a specific theorem to compare, not a blanket claim that ordinary system identification cannot handle unknown initial conditions, slow mixing, passive structure or simulation error. No historical priority is established by the present search.
