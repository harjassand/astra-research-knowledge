# A fully explicit common-stationary planning obstruction

## Status and intended use

This is an ordinary self-contained proof derived during the branch investigation. It is **not** claimed historically novel and is not a civilisation-changing result. It rules out an attractive but invalid shortcut: exact low-dimensional, positive, uniformly mixing predictive dynamics do not by themselves provide precision-efficient exact planning. The qualification about precision is essential.

## Theorem

Unless P = NP, there is no algorithm polynomial in the binary description length of an explicitly supplied family of rational, strictly positive, 4-by-4 doubly stochastic transition matrices that solves the following terminal open-loop planning problem exactly:

* all transitions share the uniform stationary distribution;
* every transition entry is at least 3/16;
* there are two allowed transitions at each of n stages;
* the initial distribution and terminal reward vector are fixed rational vectors, independent of the integer PARTITION instance;
* choose one transition per stage to maximize expected terminal reward.

Consequently, polynomial dependence only on log(1/epsilon), instead of 1/epsilon or a stronger structural parameter, cannot generally yield additive-epsilon optimal planning for this family.

## Construction

Start from positive integers a_1,...,a_n, supplied in binary. PARTITION asks whether signs sigma_i in {-1,+1} exist with sum_i sigma_i a_i = 0.

Let

```
B = [[ 1, 0, 0],
     [ 0, 1, 0],
     [ 0, 0, 1],
     [-1,-1,-1]],

C = [[ 3,-1,-1,-1],
     [-1, 3,-1,-1],
     [-1,-1, 3,-1]] / 4.
```

Then CB=I_3, C1_4=0, and 1_4^T B=0. Let J=1_4 1_4^T/4 and u=1_4/4.

For an integer a, define

```
A(a) = [[1, 0, 0],
        [a, 1, 0],
        [a*a, 2*a, 1]].
```

It sends (1,s,s^2)^T to (1,s+a,(s+a)^2)^T.

Calculate

```
M = max(1, max over i, sigma, j, k of abs((B A(sigma*a_i) C)[j,k]))
alpha = 1/(16*M)
P_i^sigma = J + alpha * B A(sigma*a_i) C.
```

All these rational numbers have polynomial binary encoding length. Every entry of P_i^sigma lies in [3/16,5/16]. Because 1^T B=0 and C1=0, each P_i^sigma is doubly stochastic, with common stationary distribution u.

Fix beta=1/8 and

```
p_0 = u + beta*B*(1,0,0)^T = (3/8, 1/4, 1/4, 1/8)^T.
g = C^T*(0,0,1)^T = (-1/4,-1/4,3/4,-1/4)^T.
r = (3/4)*1_4 - g = (1,1,0,1)^T.
```

The reward r is a fixed vector in [0,1]^4.

## Exact evolution and proof

Since JB=0, Cu=0, and CB=I, for any v,

```
P_i^sigma (u + t Bv) = u + t*alpha*B*A(sigma*a_i)*v.
```

Induction yields

```
p_n = u + beta*alpha^n*B*(1,S,S^2)^T,
S = sum_i sigma_i*a_i.
```

Furthermore, g^T u=0 and g^T B=(0,0,1), so

```
r^T p_n = 3/4 - beta*alpha^n*S^2.
```

Therefore the maximum possible terminal reward is exactly 3/4 if and only if the PARTITION instance is positive. Constructing the matrices and the fixed start/report is polynomial work. This proves exact planning NP-hardness.

If the PARTITION instance is negative, |S|>=1 for every sign choice, so every reward is at most 3/4-beta*alpha^n. Set epsilon=beta*alpha^n/3. Its binary encoding length is polynomial in the instance description. An epsilon-optimal policy (or an epsilon-accurate optimal value) distinguishes the two cases. Thus a general running-time bound polynomial in the input length and log(1/epsilon) would imply P=NP.

## What the result does and does not say

It grants the entire exact predictive model before planning. Hence it is stronger than an acquisition lower bound: even zero acquisition cost and exact retained dynamics do not eliminate this planning obstruction.

It does not establish hardness at fixed error, or at inverse-polynomial epsilon. Its hard signal is beta*alpha^n. Indeed, the uniform mixing contracts away the controlled signal. A method polynomial in 1/epsilon can legitimately be exponential in the integer-instance input length here. It would be wrong to market this as robust constant-accuracy hardness.

The theorem concerns stage-dependent binary action sets. It is a standard finite-horizon open-loop planning interface. Stationary action constraints would need a separate clock/state construction; that is not silently supplied.

## Strong existing positive machinery that must be retained

* Alegre, Bazzan, and da Silva (ICML 2022), **Optimistic Linear Support and Successor Features as a Basis for Optimal Policy Transfer**: https://proceedings.mlr.press/v162/alegre22a.html . This already connects linear-reward transfer to convex coverage sets and constructs a policy set for optimal transfer. A newly proposed policy-hull learner is not automatically a new foundational mechanism.
* Mhammedi, Foster, and Rakhlin, **Efficient Model-Free Exploration in Low-Rank MDPs** (arXiv:2307.03997): https://arxiv.org/abs/2307.03997 . Need inspect exact learning-oracle interface before claiming an unconditional polynomial algorithm.
* Huang, Li, Liang, and Yang (ICML 2026), **Breaking the Computational Barrier: Provably Efficient Actor-Critic for Low-Rank MDPs**: https://proceedings.mlr.press/v306/huang26x.html ; https://arxiv.org/abs/2605.01242 . The abstract explicitly targets computationally expensive planning/optimization oracles via supervised learning. Its assumptions must be fetched before claiming it settles arbitrary low-rank planning.

## Scientific implication

A learned predictive representation and a learned planning operation are different assets. A proposed mechanism should expose the operation that optimizes over the reachable response set, charge how it is acquired, and state its precision dependence. Positivity and a common stationary state do not substitute for that operation.
