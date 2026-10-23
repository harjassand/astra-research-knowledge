"""Shared full-history BSC-HMM filter and exact finite-horizon belief planner.

No fixture truth is imported. Both acquired estimators and the separately
labelled evaluator oracle use these identical routines. Finite arithmetic is
floating point; this is exact tree enumeration, not a formal numeric proof.
"""
from dataclasses import dataclass
import math


@dataclass
class Model:
    eta: float
    lambdas: tuple
    initial_prior_plus: float = 0.5


def observe_prior(prior_mean, eta, y):
    denominator = 1+eta*y*prior_mean
    if denominator <= 0:
        raise ValueError('Observed history has zero probability under candidate model')
    return (prior_mean+eta*y)/denominator


def predict_and_update(posterior_mean, model, action, y):
    predicted = model.lambdas[action]*posterior_mean
    probability = (1+model.eta*y*predicted)/2
    updated = observe_prior(predicted, model.eta, y)
    return probability, updated


def filter_history(actions, obs, model):
    m = observe_prior(2*model.initial_prior_plus-1, model.eta, int(obs[0]))
    log_likelihood = math.log((1+model.eta*int(obs[0])*
                               (2*model.initial_prior_plus-1))/2)
    for action,y in zip(actions,obs[1:]):
        p,m = predict_and_update(m,model,int(action),int(y))
        log_likelihood += math.log(p)
    return m,log_likelihood


def reward(objective, previous, current, action):
    cost = objective['action1_cost']
    if objective['name'] == 'positive_output':
        raw = (1+current)/2-cost*action
    elif objective['name'] == 'observed_switches':
        raw = (1-previous*current)/2-cost*action
    else:
        raise ValueError(objective['name'])
    # The normalized per-step reward lies in [0,1]. All computation and
    # physical step costs are charged separately from this synthetic utility.
    value = (raw+cost)/(1+cost)
    assert -1e-12 <= value <= 1+1e-12
    return value


def optimal_tree(model, posterior_mean, previous, objective, horizon=None):
    h = objective['horizon'] if horizon is None else horizon
    if h == 0:
        return 0.0,None,1
    best = None
    nodes = 1
    for action in (0,1):
        total = 0.0
        children = {}
        for y in (-1,1):
            probability,updated = predict_and_update(posterior_mean,model,action,y)
            continuation,child,subnodes = optimal_tree(model,updated,y,objective,h-1)
            nodes += subnodes
            total += probability*(reward(objective,previous,y,action)+continuation)
            children[y] = child
        if best is None or total > best[0]:
            best = (total,{'action':action,'children':children})
    return best[0],best[1],nodes


def evaluate_tree(tree, truth_model, truth_posterior, previous, objective):
    if tree is None:
        return 0.0
    action = tree['action']
    total = 0.0
    for y in (-1,1):
        probability,updated = predict_and_update(truth_posterior,truth_model,action,y)
        total += probability*(reward(objective,previous,y,action)+
                              evaluate_tree(tree['children'][y],truth_model,updated,y,objective))
    return total


def constant_tree(action,h):
    if h == 0:
        return None
    child = constant_tree(action,h-1)
    return {'action':action,'children':{-1:child,1:child}}
