#!/usr/bin/env python3
"""Evaluator-only simulated plant. Learner receives serialized shot counts.

Each action prepares the VISIBLE qubit, lets an unknown joint unitary act,
and measures/discards the visible qubit. A hidden memory qubit persists.
Repeated episode starts are a supplied, counted full-process reset resource.
This is not acquired laboratory data. Private matrices are never serialized
to the learner's calibration data.
"""
import math
import numpy as np

_I = np.eye(2, dtype=complex)
_X = np.array([[0,1],[1,0]],complex)
_Y = np.array([[0,-1j],[1j,0]],complex)
_Z = np.diag([1,-1]).astype(complex)


def _rotation(pauli, angle):
    return math.cos(angle)*np.eye(pauli.shape[0])-1j*math.sin(angle)*pauli


class ShotPlant:
    number_actions = 4
    number_outcomes = 2
    observable_rank_upper_bound = 4  # Architecture; no latent operator supplied.

    def __init__(self, seed=146071):
        self.rng = np.random.default_rng(seed)
        u = np.kron(_I,_rotation(_Y,0.31)@_rotation(_Z,-0.21))
        for p, angle in [(np.kron(_X,_X),0.59),(np.kron(_Y,_Y),0.37),(np.kron(_Z,_Z),0.43)]:
            u = u@_rotation(p,angle)
        u = u@np.kron(_rotation(_X,0.17),_I)
        preparations = [np.array([1,0]),np.array([0,1]),
                        np.array([1,1])/math.sqrt(2),np.array([1,1j])/math.sqrt(2)]
        z = np.eye(2,dtype=complex)
        x = np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
        y = np.array([[1,1],[1j,-1j]],complex)/math.sqrt(2)
        measurement_bases = [z,x,y,z]
        self._kraus = {}
        tensor = u.reshape(2,2,2,2)
        for a in range(4):
            for o in range(2):
                self._kraus[a,o] = np.einsum('s,seuf,u->ef',measurement_bases[a][:,o].conj(),tensor,preparations[a])
            completeness = sum(self._kraus[a,o].conj().T@self._kraus[a,o] for o in range(2))
            assert np.max(np.abs(completeness-_I)) < 1e-12
        self._initial = (_I+0.21*_X-0.28*_Y+0.34*_Z)/2
        self.reset_episodes = 0
        self.primitive_interventions = 0

    def episode_counts(self, actions, shots):
        """N legal repeated episodes; multinomial batching is a simulator speedup.

        Only integer outcome counts are returned, never exact expectations.
        The ledger charges every represented shot, reset and intervention.
        """
        leaves = [self._initial]
        for a in actions:
            if not 0 <= a < self.number_actions:
                raise ValueError('Illegal action')
            leaves = [self._kraus[a,o]@rho@self._kraus[a,o].conj().T for rho in leaves for o in range(2)]
        probabilities = np.array([np.trace(rho).real for rho in leaves])
        probabilities /= probabilities.sum()
        counts = self.rng.multinomial(shots,probabilities)
        self.reset_episodes += int(shots)
        self.primitive_interventions += int(shots)*len(actions)
        return counts.tolist()

    def _advance_batch(self, states, a):
        candidates = [self._kraus[a,o]@states@self._kraus[a,o].conj().T for o in range(2)]
        p0 = np.trace(candidates[0],axis1=1,axis2=2).real
        outcomes = (self.rng.random(len(states)) >= p0).astype(int)
        result = np.where(outcomes[:,None,None] == 0,candidates[0],candidates[1])
        masses = np.trace(result,axis1=1,axis2=2).real
        result /= masses[:,None,None]
        self.primitive_interventions += len(states)
        return result,outcomes

    def controller_experiment(self, shots, abort_probability, continuation_action=2):
        """Legal adaptive episodes and continuation, returning only aggregate counts."""
        states = np.repeat(self._initial[None,:,:],shots,axis=0)
        self.reset_episodes += shots
        states,succeeded,lengths = self.controller_states(states,abort_probability)
        states,test_outcomes = self._advance_batch(states,continuation_action)
        return {
            'shots':shots,'successes':int(succeeded.sum()),
            'success_and_test1':int(np.sum(succeeded & (test_outcomes == 1))),
            'abort_and_test1':int(np.sum(~succeeded & (test_outcomes == 1))),
            'total_primitive_calls_before_test':int(lengths.sum()),
            'maximum_primitive_calls_before_test':int(lengths.max()),
        }

    def controller_states(self, states, abort_probability):
        number = len(states)
        control = np.zeros(number,dtype=int)
        alive = np.ones(number,dtype=bool)
        success = np.zeros(number,dtype=bool)
        lengths = np.zeros(number,dtype=int)
        for _ in range(10000):
            indices = np.flatnonzero(alive)
            if not len(indices):
                break
            aborted = indices[self.rng.random(len(indices)) < abort_probability]
            alive[aborted] = False
            old_control = control.copy()
            for c,a in [(0,0),(1,3)]:
                indices = np.flatnonzero(alive & (old_control == c))
                if not len(indices):
                    continue
                updated,outcomes = self._advance_batch(states[indices],a)
                states[indices] = updated
                lengths[indices] += 1
                finished = np.zeros(len(indices),dtype=bool) if c == 0 else outcomes == 0
                success[indices[finished]] = True
                alive[indices[finished]] = False
                control[indices] = outcomes
        else:
            raise RuntimeError('Clock tail exceeded simulator cap')
        return states,success,lengths

    def repeated_controller_experiment(self, shots, abort_probability, continuation_action=2):
        states = np.repeat(self._initial[None,:,:],shots,axis=0)
        self.reset_episodes += shots
        states,success1,length1 = self.controller_states(states,abort_probability)
        # Reuse the physical hidden memory after both success and abort. Only
        # the two-state classical controller is reinitialized.
        states,success2,length2 = self.controller_states(states,abort_probability)
        _,test = self._advance_batch(states,continuation_action)
        both = success1 & success2
        return {'shots':shots,'both_successes':int(both.sum()),
                'both_success_and_test1':int(np.sum(both & (test == 1))),
                'total_primitive_calls':int(length1.sum()+length2.sum()+shots)}

    def reset_word_experiment(self, word, repeats, shots, continuation_action=2):
        # Two legally prepared history ensembles, followed by the SAME word.
        states0 = np.repeat(self._initial[None,:,:],shots,axis=0)
        states1 = states0.copy()
        self.reset_episodes += 2*shots
        states0,_ = self._advance_batch(states0,0)
        states1,_ = self._advance_batch(states1,3)
        for _ in range(repeats):
            for a in word:
                states0,_ = self._advance_batch(states0,a)
                states1,_ = self._advance_batch(states1,a)
        _,o0 = self._advance_batch(states0,continuation_action)
        _,o1 = self._advance_batch(states1,continuation_action)
        return {'shots_each':shots,'history0_test1':int(o0.sum()),'history1_test1':int(o1.sum())}

    def evaluator_joint_probability(self, actions, outcomes):
        # Evaluation only. This method is not exposed to/imported by learner.
        state = self._initial
        for a,o in zip(actions,outcomes):
            if o is None:
                state = sum(self._kraus[a,b]@state@self._kraus[a,b].conj().T for b in range(2))
            else:
                state = self._kraus[a,o]@state@self._kraus[a,o].conj().T
        return float(np.trace(state).real)

    def macro_counts(self, preparation, shots, abort_probability,
                     future_action=None, maximum_calls=128):
        """Count-only batching of a LEGAL capped adaptive operation.

        Exact private propagation generates the sampling distribution; only
        integer counts and total physical-call cost are returned. This is the
        adaptive analogue of episode_counts, not an expectation oracle. The
        cap aborts while retaining memory. It changes the unbounded target by
        at most (1-delta)^maximum_calls in each terminal test probability.
        Multinomial categories retain call length, so the ledger charges an
        actual sampled integer number of represented native interventions.
        """
        state = self._initial
        for a in preparation:
            state = sum(self._kraus[a,o]@state@self._kraus[a,o].conj().T for o in range(2))
        terminal = []
        current = [state,np.zeros((2,2),complex)]
        gamma = 1-abort_probability
        def record(label,length,rho):
            if future_action is None:
                terminal.append((label,length,None,float(np.trace(rho).real)))
            else:
                for outcome in range(2):
                    k = self._kraus[future_action,outcome]
                    probability = float(np.trace(k@rho@k.conj().T).real)
                    terminal.append((label,length,outcome,probability))
        for length in range(maximum_calls+1):
            if length == maximum_calls:
                record('abort',length,current[0]+current[1])
                break
            record('abort',length,abort_probability*(current[0]+current[1]))
            continuing = [np.zeros((2,2),complex),np.zeros((2,2),complex)]
            for c,a in [(0,0),(1,3)]:
                for o in range(2):
                    k = self._kraus[a,o]
                    updated = gamma*k@current[c]@k.conj().T
                    if c == 1 and o == 0:
                        record('success',length+1,updated)
                    else:
                        continuing[o] += updated
            current = continuing
        probabilities = np.array([max(t[3],0) for t in terminal])
        assert abs(probabilities.sum()-1) < 1e-11
        probabilities /= probabilities.sum()
        counts = self.rng.multinomial(shots,probabilities)
        native_calls = sum(t[1]*int(count) for t,count in zip(terminal,counts))
        self.reset_episodes += int(shots)
        self.primitive_interventions += int(native_calls+shots*(len(preparation)+(future_action is not None)))
        labels = {}
        for (label,length,outcome,_),count in zip(terminal,counts):
            key = label if outcome is None else f'{label},{outcome}'
            labels[key] = labels.get(key,0)+int(count)
        return {'preparation':list(preparation),'future_action':future_action,
                'shots':int(shots),'counts':labels,'sampled_macro_native_calls':native_calls,
                'maximum_calls':maximum_calls,'abort_probability':abort_probability}
