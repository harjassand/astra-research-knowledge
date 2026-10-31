# Other openings and why they were not promoted

## A reusable excursion / resolvent calculus

Desired power: learn from one physical trajectory, then answer later
first-passage, boundary-value, occupation, and Feynman-Kac potential queries.
Recording a first-return excursion from boundary i to boundary j with its
duration and occupation marks gives a renewal kernel K_theta and a reward
vector b_theta. The boundary response is (I-K_theta)^(-1)b_theta. Killing gives
a contraction; finite parameter nets give a simultaneous confidence event for
later adaptive query choices. Natural visits can supply row samples through
the strong Markov property, without restarting the experiment.

This is a useful construction but not a strong surviving new operation. Exact
milestoning already makes the renewal-kernel reduction; trace processes give
Schur complements; ordinary generator estimation and numerical resolvents are
fair same-data comparators. Successor representations and reward-free
reinforcement learning already formalize acquiring a reusable object before
the reward is specified. Adding common concentration does not establish a new
capability.

Further problems are concrete. A finite archive of continuous excursion marks
does not approximate the full path law in total variation merely because its
finite-dimensional means are accurate. Boundary-visit quotas do not imply a
polynomial physical acquisition time. Rare traps can be invisible to a short
trajectory while dominating undiscounted passage-time means. Supplying a
mixing bound, return-time cap, generative sampler, or reset would hide rather
than solve those acquisition problems.

Primary comparisons:

- Juan M. Bello-Rivas and Ron Elber, *Exact milestoning* (2015):
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4352169/
- David Aristoff, Juan M. Bello-Rivas, and Ron Elber, *A mathematical framework
  for Exact Milestoning* (2016):
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4879838/
- Eric Vanden-Eijnden and collaborators, *On the assumptions underlying
  milestoning* (2008): https://pmc.ncbi.nlm.nih.gov/articles/PMC2646510/
- Chi Jin, Akshay Krishnamurthy, Max Simchowitz, and Tiancheng Yu,
  *Reward-Free Exploration for Reinforcement Learning*, ICML 2020:
  https://proceedings.mlr.press/v119/jin20d.html
- Andrew Wagenmaker, Yifang Chen, Max Simchowitz, Simon Du, and Kevin Jamieson,
  *Reward-Free RL is No Harder Than Reward-Aware RL in Linear Markov Decision
  Processes*, ICML 2022:
  https://proceedings.mlr.press/v162/wagenmaker22b.html

## A reusable algebraic execution representation

Desired power: learn a common algebra, symmetry, or integrable coordinate
system and use it for an entire family of later calculations. This is more
substantial than a predictor because it changes how the calculation executes.
If uncertainty is entirely in a common conjugating unitary U, then replacing
U by U_hat incurs a uniform O(||U-U_hat||) error in every word U W U^dagger,
regardless of word length. By contrast, uncertainty in the intrinsic spectrum
cannot usually be confined to a one-time coordinate error: a phase error dtheta
becomes order one at time of order 1/dtheta.

The ordinary routes are strong. Numerical simultaneous block diagonalization
uses the commutant of the generated matrix algebra; Pauli anticommutation
graphs can reveal exact free-fermion structure through line-graph recognition;
Clifford and low-resource quantum process learning can acquire corresponding
representations. Unknown sector weights and observables remain important:
solving each free-fermion symmetry sector does not automatically make summing
over exponentially many sectors efficient, and a compact Clifford-times-product
state description does not make every measurement distribution easy to sample.

The paired drifting source in the companion note was the strongest concrete
construction reached here. It earns a decoder and a polynomial acquisition
bound, while honestly retaining the same-data published algorithm and the
unheralded-noise failure. It is not offered as a replacement for the parent's
selected research construction.
