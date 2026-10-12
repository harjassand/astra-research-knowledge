"""Synthetic assay. The optimiser is NOT passed adjacency, state labels, or rates.
Only the benchmark truth-checker accesses the hidden model.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numba import njit
from flux_design import Summary

@njit(cache=True)
def _sample(adj, destinations, reward, rates, bg_rate, rho, samples, seed):
    np.random.seed(seed)
    k=len(rates);degree=adj.shape[1]
    source_counts=np.zeros(k,np.int64)
    control_counts=np.zeros(k,np.int64)
    reward_sum=0;total_time=0.;background_events=0;control_events=0;max_controls=0
    for episode in range(samples):
        state=np.random.randint(k)  # reproducible reset law: uniform over active sources
        episode_controls=0
        while True:
            rate=rates[state] if state<k else 0.
            total=bg_rate+rho+rate
            total_time+=-np.log(max(np.random.random(),1e-300))/total
            pick=np.random.random()*total
            if pick<rho:
                if state<k: source_counts[state]+=1
                reward_sum+=reward[state]
                if episode_controls>max_controls:max_controls=episode_controls
                break
            elif pick<rho+bg_rate:
                state=adj[state,np.random.randint(degree)]
                background_events+=1
            else:
                control_counts[state]+=1;control_events+=1;episode_controls+=1
                state=destinations[state]
    return source_counts,reward_sum,control_counts,total_time,background_events,control_events,max_controls

@dataclass
class HiddenInstance:
    adjacency: np.ndarray
    destinations: np.ndarray
    reward: np.ndarray
    background_rate: float
    reset_rate: float

    @property
    def channels(self):return len(self.destinations)

    def assay(self,rates,samples:int,seed:int)->Summary:
        rates=np.asarray(rates,float)
        if rates.shape!=(self.channels,) or np.any(rates<0) or not np.all(np.isfinite(rates)):
            raise ValueError('Invalid rates.')
        if samples<1:raise ValueError('Positive sample count required.')
        x=_sample(self.adjacency,self.destinations,self.reward,rates,self.background_rate,
                  self.reset_rate,samples,seed)
        return Summary(int(samples),x[0].tolist(),int(x[1]),x[2].tolist(),float(x[3]),int(x[4]),int(x[5]),int(x[6]))


def generate_instance(states:int,channels:int,seed:int,degree:int=4,background_rate:float=1.,reset_rate:float=1.):
    if states<=channels+1 or channels<1 or degree<1:raise ValueError('Invalid dimensions.')
    rng=np.random.default_rng(seed)
    adjacency=rng.integers(0,states,size=(states,degree),dtype=np.int64)
    adjacency[:,0]=(np.arange(states)+1)%states # irreducible background ring
    destinations=rng.integers(channels,states,size=channels,dtype=np.int64)
    reward=rng.integers(0,2,size=states,dtype=np.int64)
    return HiddenInstance(adjacency,destinations,reward,background_rate,reset_rate)
