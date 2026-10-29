"""Exact random choices from positive integer circuit weights.

The input is an actual finite nonnegative-integer +/* DAG.  This module does
not acquire such a DAG from an arbitrary counting problem.  No subtraction,
floating-point operation, expanded huge count, or count oracle is used by the
sampler.  Integer exponents are binary-encoded; significant bits are rounded
outwards.  Sampling is exact under independent fair RNG bits and terminates
almost surely, with expected polynomial work at the supplied circuit scope.
"""
from dataclasses import dataclass
import random


def _natural(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(label + ' must be a nonnegative integer')
    return value


@dataclass(frozen=True)
class Dyadic:
    """The exact nonnegative value mantissa * 2**exponent, not expanded."""
    mantissa: int
    exponent: int

    def __post_init__(self):
        _natural(self.mantissa, 'dyadic mantissa')
        if type(self.exponent) is not int:
            raise ValueError('dyadic exponent must be an integer')

    def form(self):
        return dict(mantissa=self.mantissa, exponent=self.exponent)


ZERO = Dyadic(0, 0)


def _canonical(mantissa, exponent):
    if not mantissa:
        return ZERO
    trailing = (mantissa & -mantissa).bit_length() - 1
    return Dyadic(mantissa >> trailing, exponent + trailing)


def round_dyadic(mantissa, exponent, precision, upward=False):
    """Directed rounding to at most precision significant bits."""
    _natural(mantissa, 'mantissa')
    if type(exponent) is not int or type(precision) is not int or precision < 2:
        raise ValueError('integer exponent and precision at least two required')
    if not mantissa:
        return ZERO
    shift = max(0, mantissa.bit_length() - precision)
    if shift:
        rounded = mantissa >> shift
        if upward and (rounded << shift) != mantissa:
            rounded += 1
        mantissa = rounded
        exponent += shift
        if mantissa.bit_length() > precision:
            # A carry to exactly 2**precision; this division is exact.
            mantissa >>= 1
            exponent += 1
    return _canonical(mantissa, exponent)


def compare_dyadic(left, right):
    """Exact comparison, without aligning an enormous exponent gap."""
    if not left.mantissa or not right.mantissa:
        return (left.mantissa > right.mantissa) - (left.mantissa < right.mantissa)
    lh = left.mantissa.bit_length() + left.exponent
    rh = right.mantissa.bit_length() + right.exponent
    if lh != rh:
        return (lh > rh) - (lh < rh)
    # Equal leading positions bound this shift by the mantissa bit lengths.
    if left.exponent >= right.exponent:
        a, b = left.mantissa << (left.exponent-right.exponent), right.mantissa
    else:
        a, b = left.mantissa, right.mantissa << (right.exponent-left.exponent)
    return (a > b) - (a < b)


def scale_dyadic(value, integer):
    _natural(integer, 'exact dyadic scale')
    return _canonical(value.mantissa * integer, value.exponent)


def _on_grid(value, grid_exponent, upward):
    if not value.mantissa:
        return 0
    shift = value.exponent - grid_exponent
    if shift >= 0:
        return value.mantissa << shift
    shift = -shift
    if shift >= value.mantissa.bit_length():
        return int(upward)
    result = value.mantissa >> shift
    return result + int(upward and (result << shift) != value.mantissa)


def add_dyadic(left, right, precision, upward=False):
    if not left.mantissa:
        return round_dyadic(right.mantissa, right.exponent, precision, upward)
    if not right.mantissa:
        return round_dyadic(left.mantissa, left.exponent, precision, upward)
    height = max(left.mantissa.bit_length()+left.exponent,
                 right.mantissa.bit_length()+right.exponent)
    grid = height - precision
    # Each grid conversion has at most precision+1 materialized bits even
    # when the difference between input exponents is astronomically large.
    total = _on_grid(left, grid, upward) + _on_grid(right, grid, upward)
    return round_dyadic(total, grid, precision, upward)


def multiply_dyadic(left, right, precision, upward=False):
    return round_dyadic(left.mantissa*right.mantissa,
                        left.exponent+right.exponent, precision, upward)


class ExpansionLimit(ValueError):
    """A conservative intermediate/output bit allowance was exceeded."""


class SamplingPrecisionLimit(ValueError):
    """The exact decision remains unresolved at the explicit random-bit cap."""


class PositiveIntegerCircuit:
    """Hash-consed, acyclic nonnegative-integer arithmetic.

    Rounding budgets describe an unfolded error recurrence, not the number of
    physically processed gates. They have polynomial binary length even when
    their numeric values and the output's bit length are exponential.
    """
    def __init__(self):
        self.nodes = []
        self.zero_flags = []
        self.rounding_budgets = []
        self.bit_bounds = []
        self._interned = {}
        self._interval_cache = {}
        self.stats = dict(interval_gate_evaluations=0, exact_gate_evaluations=0,
                          random_bits=0, exact_choices=0, max_random_bits_per_choice=0,
                          max_mantissa_bits=0, max_exponent_bits=0,
                          max_requested_precision=0, largest_materialized_count_bits=0,
                          cancellation_used=False, expanded_count_in_sampling=False)
        self.zero = self.constant(0)
        self.one = self.constant(1)

    def _index(self, node):
        if type(node) is not int or not 0 <= node < len(self.nodes):
            raise ValueError('actual existing arithmetic-node index required')
        return node

    def constant(self, value):
        _natural(value, 'literal nonnegative integer constant')
        descriptor = ('constant', value)
        if descriptor in self._interned:
            return self._interned[descriptor]
        index = len(self.nodes)
        self._interned[descriptor] = index
        self.nodes.append(descriptor)
        self.zero_flags.append(value == 0)
        self.rounding_budgets.append(1)
        self.bit_bounds.append(value.bit_length())
        return index

    def _binary(self, op, left, right):
        self._index(left); self._index(right)
        if op == 'add':
            if self.zero_flags[left]: return right
            if self.zero_flags[right]: return left
        else:
            if self.zero_flags[left] or self.zero_flags[right]: return self.zero
            if left == self.one: return right
            if right == self.one: return left
        if right < left: left, right = right, left
        descriptor = (op, left, right)
        if descriptor in self._interned:
            return self._interned[descriptor]
        index = len(self.nodes)
        self._interned[descriptor] = index
        self.nodes.append(descriptor)
        self.zero_flags.append(False)
        a, b = self.rounding_budgets[left], self.rounding_budgets[right]
        self.rounding_budgets.append(max(a,b)+1 if op == 'add' else a+b+1)
        a, b = self.bit_bounds[left], self.bit_bounds[right]
        self.bit_bounds.append(max(a,b)+1 if op == 'add' else a+b)
        return index

    def add(self, left, right):
        return self._binary('add', left, right)

    def multiply(self, left, right):
        return self._binary('multiply', left, right)

    def total(self, nodes):
        level = list(nodes)
        for node in level: self._index(node)
        if not level: return self.zero
        while len(level) > 1:
            level = [self.add(level[i], level[i+1]) if i+1<len(level) else level[i]
                     for i in range(0,len(level),2)]
        return level[0]

    def power(self, node, exponent):
        self._index(node); _natural(exponent, 'power exponent')
        result = self.one
        while exponent:
            if exponent & 1: result = self.multiply(result, node)
            exponent >>= 1
            if exponent: node = self.multiply(node, node)
        return result

    def interval(self, node, precision):
        self._index(node)
        if type(precision) is not int or precision < 2:
            raise ValueError('precision must be an integer at least two')
        values = self._interval_cache.setdefault(precision, [])
        self.stats['max_requested_precision'] = max(self.stats['max_requested_precision'], precision)
        for i in range(len(values), node+1):
            entry = self.nodes[i]
            if entry[0] == 'constant':
                lower = round_dyadic(entry[1], 0, precision, False)
                upper = round_dyadic(entry[1], 0, precision, True)
            else:
                al, au = values[entry[1]]; bl, bu = values[entry[2]]
                operation = add_dyadic if entry[0] == 'add' else multiply_dyadic
                lower = operation(al, bl, precision, False)
                upper = operation(au, bu, precision, True)
            if compare_dyadic(lower, upper) > 0:
                raise AssertionError('directed interval inverted')
            if self.zero_flags[i] != (lower.mantissa == 0):
                raise AssertionError('positive circuit lost its exact zero information')
            values.append((lower,upper))
            self.stats['interval_gate_evaluations'] += 1
            self.stats['max_mantissa_bits'] = max(self.stats['max_mantissa_bits'],
                lower.mantissa.bit_length(), upper.mantissa.bit_length())
            self.stats['max_exponent_bits'] = max(self.stats['max_exponent_bits'],
                abs(lower.exponent).bit_length(), abs(upper.exponent).bit_length())
        return values[node]

    def decide_prefix(self, left, right, prefix, bits):
        """Return 0/1 only if the entire uniform dyadic cell is certified.

        The desired probability of 0 is left/(left+right). Return None when
        more fair bits and precision are necessary. This operation samples no
        bits itself, permitting independent complete finite-prefix checks.
        """
        self._index(left); self._index(right)
        _natural(bits,'uniform prefix length'); _natural(prefix,'uniform prefix')
        if prefix >= (1 << bits): raise ValueError('prefix exceeds its stated length')
        if self.zero_flags[left] and self.zero_flags[right]:
            raise ValueError('a zero total weight has no probability distribution')
        if self.zero_flags[left]: return 1
        if self.zero_flags[right]: return 0
        budget = max(self.rounding_budgets[left], self.rounding_budgets[right])
        precision = bits + budget.bit_length() + 10
        al, au = self.interval(left, precision)
        bl, bu = self.interval(right, precision)
        scale = 1 << bits
        # upper(U)*upper(B) <= (1-upper(U))*lower(A)
        if compare_dyadic(scale_dyadic(bu,prefix+1),
                          scale_dyadic(al,scale-prefix-1)) <= 0:
            return 0
        # lower(U)*lower(B) >= (1-lower(U))*upper(A)
        if compare_dyadic(scale_dyadic(bl,prefix),
                          scale_dyadic(au,scale-prefix)) >= 0:
            return 1
        return None

    def choose(self, left, right, rng=None, maximum_random_bits=None):
        """An exact Bernoulli choice; no finite fixed-precision approximation."""
        if maximum_random_bits is not None:
            _natural(maximum_random_bits, 'explicit random-bit allowance')
        rng = random.SystemRandom() if rng is None else rng
        prefix = bits = 0
        while True:
            result = self.decide_prefix(left, right, prefix, bits)
            if result is not None:
                self.stats['exact_choices'] += 1
                self.stats['max_random_bits_per_choice'] = max(
                    self.stats['max_random_bits_per_choice'], bits)
                return result
            if maximum_random_bits is not None and bits >= maximum_random_bits:
                raise SamplingPrecisionLimit('exact random comparison is still unresolved')
            bit = rng.getrandbits(1)
            if type(bit) is not int or bit not in (0,1):
                raise ValueError('RNG must supply actual fair bits')
            prefix = (prefix << 1) | bit
            bits += 1
            self.stats['random_bits'] += 1

    def choose_many(self, weights, rng=None):
        """A balanced positive-sum tree over the actual supplied weights."""
        weights = tuple(weights)
        if not weights: raise ValueError('nonempty category list required')
        for node in weights: self._index(node)
        tree = [(node, i, None) for i,node in enumerate(weights)]
        while len(tree)>1:
            tree = [(self.add(tree[i][0],tree[i+1][0]),tree[i],tree[i+1])
                    if i+1<len(tree) else tree[i] for i in range(0,len(tree),2)]
        current = tree[0]
        if self.zero_flags[current[0]]: raise ValueError('all categories have zero weight')
        while current[2] is not None:
            choice = self.choose(current[1][0],current[2][0],rng)
            current = current[1+choice]
        return current[1]

    def expand(self, root, maximum_intermediate_bits=1000000):
        """Separate exact integer output, with a conservative explicit guard."""
        self._index(root)
        if maximum_intermediate_bits is not None:
            _natural(maximum_intermediate_bits,'expanded integer bit allowance')
        needed=set(); stack=[root]
        while stack:
            node=stack.pop()
            if node in needed: continue
            needed.add(node)
            entry=self.nodes[node]
            if entry[0]!='constant': stack.extend(entry[1:])
        if maximum_intermediate_bits is not None and any(
                self.bit_bounds[node]>maximum_intermediate_bits for node in needed):
            raise ExpansionLimit('conservative intermediate bit bound exceeds allowance')
        values={}
        for node in sorted(needed):
            entry=self.nodes[node]
            value=(entry[1] if entry[0]=='constant' else
                   values[entry[1]]+values[entry[2]] if entry[0]=='add' else
                   values[entry[1]]*values[entry[2]])
            values[node]=value
            self.stats['exact_gate_evaluations']+=1
            self.stats['largest_materialized_count_bits']=max(
                self.stats['largest_materialized_count_bits'],value.bit_length())
        return values[root]

    def form(self, root):
        self._index(root)
        return dict(representation='nonnegative_integer_plus_times_DAG',root=root,
            allocated_nodes=len(self.nodes),zero=self.zero_flags[root],
            conservative_expanded_bit_bound=self.bit_bounds[root],
            rounding_budget_binary_bits=self.rounding_budgets[root].bit_length(),
            integer_value_materialized=False)
