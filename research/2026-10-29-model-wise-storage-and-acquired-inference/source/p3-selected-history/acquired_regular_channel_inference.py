"""Regular-event inference after an actually acquired quadratic noise law.

Counts are positive integer DAGs; exact short observation samples use certified
lazy random choices without expanding these counts. Full original tapes still
execute every actual transition and pay their full output cost. DFA geometry
is the supplied event query, not supplied hidden source structure.
"""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import random
import time
from acquired_quadratic_noise_erasure import AcquiredQuadraticNoiseErasure
from positive_count_circuit_sampling import PositiveIntegerCircuit,Dyadic,ExpansionLimit

PINS={
    'acquired_quadratic_noise_erasure.py':'889e9ce8f5ec06f584548897db6944b6f1521dcd6378edefcf52d9ca2362fdc5',
    'positive_count_circuit_sampling.py':'881137934f131b1a61c07c0f3b5bb6e9f117e149600a2600cc549c4a038cfeb4',
    'query_directed_initial_history.py':'a2b987087e239c4ca788cc596128236752a2313245f3304e39816b2f17d23de4'}


def _natural(n,label):
    if type(n) is not int or n<0: raise ValueError(label+' must be a nonnegative integer')
    return n


def _word(n,bits,label):
    _natural(n,label)
    if n.bit_length()>bits: raise ValueError(label+' exceeds its original dimension')
    return n


def _pins():
    here=Path(__file__).resolve().parent
    for name,digest in PINS.items():
        if sha256((here/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('frozen dependency changed: '+name)


class BinaryDFA:
    """An explicit deterministic event automaton, with no path multiplicity."""
    def __init__(self,transitions,start,accepting):
        if not isinstance(transitions,(list,tuple)) or not transitions:
            raise ValueError('nonempty explicit deterministic transition table required')
        size=len(transitions); rows=[]
        for row in transitions:
            if not isinstance(row,(list,tuple)) or len(row)!=2:
                raise ValueError('exactly one successor per binary label required')
            if any(type(q) is not int or not 0<=q<size for q in row):
                raise ValueError('every successor must be one actual DFA state')
            rows.append(tuple(row))
        if type(start) is not int or not 0<=start<size:
            raise ValueError('actual DFA start required')
        accepting=tuple(accepting)
        if any(type(q) is not int or not 0<=q<size for q in accepting):
            raise ValueError('actual accepting DFA states required')
        self.transitions=tuple(rows); self.start=start
        self.accepting=frozenset(accepting); self.size=size

    def accepts(self,word):
        state=self.start
        for bit in word:
            _word(bit,1,'observation bit'); state=self.transitions[state][bit]
        return state in self.accepting


class AcquiredRegularChannelEvent:
    def __init__(self,channel,automaton,horizon,initial_state=None):
        started=time.perf_counter(); _pins()
        if type(channel) is not AcquiredQuadraticNoiseErasure or not channel.admitted:
            raise ValueError('the frozen, actually acquired quadratic channel is required')
        if type(automaton) is not BinaryDFA:
            raise ValueError('validated explicit deterministic event automaton required')
        _natural(horizon,'actual horizon')
        if initial_state is not None: _word(initial_state,channel.state_bits,'actual initial state')
        self.channel,self.automaton,self.horizon=channel,automaton,horizon
        self.initial_state=initial_state
        self.original_noise_bits=channel.noise_bits*horizon
        self.circuit=PositiveIntegerCircuit(); c=self.circuit; d=automaton.size
        self.noise_nodes=tuple(c.constant(n) for n in channel.channel_counts)
        self.identity=tuple(tuple(c.one if i==j else c.zero for j in range(d)) for i in range(d))
        rows=[]
        for i in range(d):
            row=[c.zero]*d
            for bit in (0,1):
                j=automaton.transitions[i][bit]
                row[j]=c.add(row[j],self.noise_nodes[bit])
            rows.append(tuple(row))
        self.transfer=tuple(rows)
        self._squares=[self.transfer]; self._power_cache={0:self.identity,1:self.transfer}
        self._continuations={}; self._restricted={}
        self.stats=dict(original_noise_bits=self.original_noise_bits,horizon=horizon,
            supplied_hidden_channel=False,supplied_event_DFA=True,
            acquired_channel_stats=channel.stats,matrix_compositions=0,
            row_matrix_products=0,short_observation_samples=0,
            full_original_tape_samples=0,full_original_tape_witnesses=0,
            actual_transitions_for_short_samples=0,
            initial_law_needed_for_observation_prediction=False,
            full_history_rank_unrank_implemented=False)
        self.count_node=self.restricted_count_node(())
        self.empty=c.zero_flags[self.count_node]
        self.stats['construction_seconds']=time.perf_counter()-started

    @classmethod
    def from_raw(cls,transition,state_bits,observation,automaton,horizon,initial_state=None,*,width_limit=None):
        channel=AcquiredQuadraticNoiseErasure(transition,state_bits,observation,width_limit=width_limit)
        return cls(channel,automaton,horizon,initial_state)

    def _matrix_product(self,left,right):
        c=self.circuit; d=self.automaton.size
        self.stats['matrix_compositions']+=1
        return tuple(tuple(c.total(c.multiply(left[i][k],right[k][j])
            for k in range(d) if not c.zero_flags[left[i][k]] and not c.zero_flags[right[k][j]])
            for j in range(d)) for i in range(d))

    def _row_product(self,row,matrix):
        c=self.circuit; d=self.automaton.size
        self.stats['row_matrix_products']+=1
        return tuple(c.total(c.multiply(row[i],matrix[i][j]) for i in range(d)
            if not c.zero_flags[row[i]] and not c.zero_flags[matrix[i][j]]) for j in range(d))

    def _power(self,exponent):
        _natural(exponent,'matrix power')
        if exponent in self._power_cache: return self._power_cache[exponent]
        while len(self._squares)<exponent.bit_length():
            self._squares.append(self._matrix_product(self._squares[-1],self._squares[-1]))
        result=self.identity; remaining=exponent; bit=0
        while remaining:
            if remaining&1: result=self._matrix_product(result,self._squares[bit])
            remaining>>=1; bit+=1
        self._power_cache[exponent]=result
        return result

    def _constraints(self,constraints):
        if isinstance(constraints,dict): constraints=constraints.items()
        result={}; conflict=False
        for position,bit in constraints:
            _natural(position,'actual observation position'); _word(bit,1,'requested observation bit')
            if position>=self.horizon: raise ValueError('observation position exceeds horizon')
            if position in result and result[position]!=bit: conflict=True
            result[position]=bit
        return tuple(sorted(result.items())),conflict

    def restricted_count_node(self,constraints):
        """Counts original tapes under DFA evidence and actual label restrictions."""
        key,conflict=self._constraints(constraints); c=self.circuit
        if conflict: return c.zero
        if key in self._restricted: return self._restricted[key]
        d=self.automaton.size; row=tuple(c.one if i==self.automaton.start else c.zero for i in range(d))
        cursor=0
        for position,bit in key:
            row=self._row_product(row,self._power(position-cursor))
            following=[c.zero]*d
            for state,value in enumerate(row):
                target=self.automaton.transitions[state][bit]
                following[target]=c.add(following[target],c.multiply(value,self.noise_nodes[bit]))
            row=tuple(following); cursor=position+1
        row=self._row_product(row,self._power(self.horizon-cursor))
        result=c.total(row[q] for q in self.automaton.accepting)
        self._restricted[key]=result
        return result

    def count_form(self):
        result=self.circuit.form(self.count_node)
        result.update(original_noise_bits=self.original_noise_bits,horizon=self.horizon)
        return result

    def count(self,maximum_intermediate_bits=1000000):
        return self.circuit.expand(self.count_node,maximum_intermediate_bits)

    def probability(self,maximum_output_bits=1000000):
        if maximum_output_bits is not None:
            _natural(maximum_output_bits,'probability output allowance')
            if self.original_noise_bits+1>maximum_output_bits:
                raise ExpansionLimit('expanded probability denominator exceeds allowance')
        return Fraction(self.count(maximum_output_bits),1<<self.original_noise_bits)

    def probability_bounds(self,significant_precision=64):
        """Certified dyadic bounds with binary exponents, not expanded rationals."""
        lo,hi=self.circuit.interval(self.count_node,significant_precision)
        return (Dyadic(lo.mantissa,lo.exponent-self.original_noise_bits),
                Dyadic(hi.mantissa,hi.exponent-self.original_noise_bits))

    def sample_selected(self,positions,rng=None):
        """Exact joint requested observation bits; never a distant original-noise sample."""
        positions=tuple(positions)
        for position in positions:
            _natural(position,'requested observation position')
            if position>=self.horizon: raise ValueError('position outside actual horizon')
        if self.empty: return None
        rng=random.SystemRandom() if rng is None else rng
        constraints={}
        for position in sorted(set(positions)):
            weights=tuple(self.restricted_count_node(tuple(constraints.items())+((position,bit),))
                          for bit in (0,1))
            constraints[position]=self.circuit.choose(*weights,rng=rng)
        self.stats['short_observation_samples']+=1
        return tuple(constraints[position] for position in positions)

    def _continuation(self,state,remaining):
        key=(state,remaining)
        if key not in self._continuations:
            power=self._power(remaining)
            self._continuations[key]=self.circuit.total(power[state][q] for q in self.automaton.accepting)
        return self._continuations[key]

    def _full(self,rng,maximum_steps,actual_initial):
        if maximum_steps is not None:
            _natural(maximum_steps,'full output step allowance')
            if self.horizon>maximum_steps:
                raise ExpansionLimit('full original tape exceeds explicit step allowance')
        if self.empty: return None
        if not self.horizon: return ()
        if actual_initial is None:
            if self.channel.state_bits: raise ValueError('actual hidden initial state required for original tape')
            actual_initial=0
        _word(actual_initial,self.channel.state_bits,'actual original initial state')
        state=actual_initial; control=self.automaton.start; tape=[]; c=self.circuit
        for step in range(self.horizon):
            remaining=self.horizon-step-1
            weights=tuple(c.multiply(self.noise_nodes[bit],
                self._continuation(self.automaton.transitions[control][bit],remaining)) for bit in (0,1))
            if rng is None:
                bit=next((b for b in (0,1) if not c.zero_flags[weights[b]]),None)
                if bit is None: raise AssertionError('positive continuation lost its witness')
                ticket=0
            else:
                bit=c.choose(*weights,rng=rng)
                ticket=rng.randrange(self.channel.channel_counts[bit])
            noise,state=self.channel._decode_local(state,bit,ticket)
            tape.append(noise); control=self.automaton.transitions[control][bit]
        if control not in self.automaton.accepting: raise AssertionError('decoded original tape violates event')
        return tuple(tape)

    def witness(self,maximum_steps=100000):
        result=self._full(None,maximum_steps,self.initial_state)
        if result is not None: self.stats['full_original_tape_witnesses']+=1
        return result

    def sample(self,rng=None,maximum_steps=100000):
        rng=random.SystemRandom() if rng is None else rng
        result=self._full(rng,maximum_steps,self.initial_state)
        if result is not None: self.stats['full_original_tape_samples']+=1
        return result

    def raw_initialization(self,program):
        return RegularChannelInitialSource(self,program)


class RegularChannelInitialSource:
    """All original raw-initializer seeds remain posterior-uniform for future-only evidence."""
    def __init__(self,event,program):
        from query_directed_initial_history import LiteralVectorCircuit
        self.event=event; self.initialization=LiteralVectorCircuit(program)
        if self.initialization.output_bits!=event.channel.state_bits:
            raise ValueError('raw initializer must output the actual microscopic state')
        self.initial_bits=self.initialization.bits
        c=event.circuit
        self.joint_count_node=c.multiply(c.power(c.constant(2),self.initial_bits),event.count_node)
        self.stats=dict(initializer_syntax=self.initialization.stats,
            original_initial_bits=self.initial_bits,supplied_initial_law=False,
            initializer_semantically_compiled=False,posterior_initial_evaluations=0)

    def count_form(self):
        result=self.event.circuit.form(self.joint_count_node)
        result.update(original_initial_bits=self.initial_bits,
                      original_dynamic_noise_bits=self.event.original_noise_bits)
        return result

    def count(self,maximum_intermediate_bits=1000000):
        return self.event.circuit.expand(self.joint_count_node,maximum_intermediate_bits)

    def posterior_count_form(self):
        return dict(zero=self.event.empty,power_of_two=None if self.event.empty else self.initial_bits)

    def sample_initial(self,rng=None):
        if self.event.empty: return None
        rng=random.SystemRandom() if rng is None else rng
        return rng.getrandbits(self.initial_bits)

    def witness_initial(self):
        return None if self.event.empty else 0

    def sample(self,rng=None,maximum_steps=100000):
        if self.event.empty: return None
        rng=random.SystemRandom() if rng is None else rng
        original=self.sample_initial(rng)
        state=self.initialization.execute(original)
        return original,self.event._full(rng,maximum_steps,state)

    def witness(self,maximum_steps=100000):
        if self.event.empty: return None
        state=self.initialization.execute(0)
        return 0,self.event._full(None,maximum_steps,state)
