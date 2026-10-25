"""Exact, matrix-free acquisition of a defective operator calculus.

New implementation, 2026-10-25. Standard-library only. Native sources are not
implemented in this module. A source supplies n and apply('A'|'B', vector,
transpose=False). Linearity, exact rational answers, and transpose access are
assumptions, not conclusions of testing.

The retained JSON contains actual relation factors, module bases, and module
actions. Loading it does not require a native source. All later circuit
evaluation is native-query free within the retained degree cap.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import OrderedDict
from fractions import Fraction as F
from math import comb
import random


def zeros(m, n):
    return [[F(0) for _ in range(n)] for _ in range(m)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a, width=None):
    if not a:
        return [[] for _ in range(width or 0)]
    return [list(x) for x in zip(*a)]


def mv(a, v):
    return [sum((x*y for x, y in zip(row, v) if x and y), F(0)) for row in a]


def mm(a, b):
    nr = len(a)
    nc = len(b[0]) if b else 0
    out = zeros(nr, nc)
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x*y
    return out


def madd(a, b, scale=F(1)):
    return [[x+scale*y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def mscale(a, c):
    return [[c*x for x in row] for row in a]


def inverse(a):
    n = len(a)
    aug = [[F(x) for x in row] + eye(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if aug[i][j]), None)
        if p is None:
            raise ValueError('singular')
        aug[j], aug[p] = aug[p], aug[j]
        v = aug[j][j]
        aug[j] = [x/v for x in aug[j]]
        for i in range(n):
            if i != j and aug[i][j]:
                v = aug[i][j]
                aug[i] = [x-v*y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


class ColumnBasis:
    """Incremental exact independent columns, retaining their original values."""
    def __init__(self, n):
        self.n = n
        self.columns = []
        self.pivots = []
        self.echelon = []
        self.transforms = []

    def reduce(self, v):
        residual = [F(x) for x in v]
        coefficients = [F(0)]*len(self.columns)
        for p, e, transform in zip(self.pivots, self.echelon, self.transforms):
            value = residual[p]
            if value:
                residual = [x-value*y for x, y in zip(residual, e)]
                for j, y in enumerate(transform):
                    coefficients[j] += value*y
        return residual, coefficients

    def add(self, v):
        residual, coefficients = self.reduce(v)
        pivot = next((i for i, x in enumerate(residual) if x), None)
        if pivot is None:
            return False, coefficients
        z = residual[pivot]
        self.columns.append([F(x) for x in v])
        self.pivots.append(pivot)
        self.echelon.append([x/z for x in residual])
        self.transforms.append([-x/z for x in coefficients] + [1/z])
        return True, [F(0)]*(len(self.columns)-1)+[F(1)]

    def coordinates(self, v):
        residual, coefficients = self.reduce(v)
        if any(residual):
            raise ValueError('vector outside retained span')
        return coefficients

    def matrix(self):
        return transpose(self.columns, self.n)

    def __len__(self):
        return len(self.columns)


def matrix_rank(a):
    if not a or not a[0]:
        return 0
    basis = ColumnBasis(len(a))
    for col in transpose(a):
        basis.add(col)
    return len(basis)


def poly_trim(p):
    p = list(p)
    while len(p)>1 and not p[-1]:
        p.pop()
    return p


def poly_derivative(p):
    return [i*p[i] for i in range(1, len(p))] or [F(0)]


def poly_remainder(a, b):
    a, b = poly_trim(a), poly_trim(b)
    while len(a)>=len(b) and any(a):
        shift = len(a)-len(b)
        q = a[-1]/b[-1]
        for i, x in enumerate(b):
            a[shift+i] -= q*x
        a = poly_trim(a)
    return a


def poly_gcd(a, b):
    a, b = poly_trim(a), poly_trim(b)
    while any(b):
        a, b = b, poly_remainder(a, b)
    return [x/a[-1] for x in a]


def charpoly(a):
    """Faddeev-LeVerrier over Q; result has increasing powers."""
    n = len(a)
    current = eye(n)
    descending = [F(1)]
    for k in range(1, n+1):
        product = mm(a, current)
        c = -sum((product[i][i] for i in range(n)), F(0))/k
        descending.append(c)
        for i in range(n):
            product[i][i] += c
        current = product
    return list(reversed(descending))


def scalar_from_pencil(h, rank_budget):
    p = charpoly(h)
    g, derivative = p, p
    for _ in range(rank_budget):
        derivative = poly_derivative(derivative)
        g = poly_gcd(g, derivative)
    degree = len(g)-1
    if degree < 1:
        return None
    c = -g[-2]/(degree*g[-1])
    expected = [F(comb(degree, j))*(-c)**(degree-j) for j in range(degree+1)]
    return c if g == expected else None


def relation_action(api, sigma, v, c=F(0), transpose_action=False):
    if not transpose_action:
        ab = api.apply('A', api.apply('B', v))
        ba = api.apply('B', api.apply('A', v))
    else:
        ab = api.apply('B', api.apply('A', v, True), True)
        ba = api.apply('A', api.apply('B', v, True), True)
    return [x-sigma*y-c*z for x, y, z in zip(ab, ba, v)]


def random_vector(rng, n, sample_size):
    return [F(rng.randrange(sample_size)) for _ in range(n)]


def acquire_relation(api, rank_budget=1, signs=(1, -1), *, seed=0,
                     sample_size=257, checks=4, sketch_attempts=2,
                     oversampling=2):
    """Obtain AB-sigma BA=cI+UV^T, or UNKNOWN.

    At most len(signs)*sketch_attempts candidate validations. Given exact
    linear APIs, chance of ever accepting an incorrect relation is at most
    that number times sample_size**(-checks). All validation vectors are fresh.
    Discovery may return UNKNOWN even on a member of the search class.
    """
    n, r = api.n, rank_budget
    if r < 0 or n <= 2*r:
        raise ValueError('need nonnegative rank budget and n>2r')
    rng = random.Random(seed)
    logs = []
    k = 2*r+1
    for sigma in signs:
        for attempt in range(sketch_attempts):
            omega_columns = [random_vector(rng, n, sample_size) for _ in range(k)]
            omega = transpose(omega_columns)
            compression = [random_vector(rng, n, sample_size) for _ in range(k)]
            nmat = mm(compression, omega)
            try:
                ninv = inverse(nmat)
            except ValueError:
                logs.append({'sigma': sigma, 'attempt': attempt, 'reason':'singular pencil input'})
                continue
            responses = [relation_action(api, sigma, v) for v in omega_columns]
            h = mm(ninv, mm(compression, transpose(responses)))
            c = scalar_from_pencil(h, r)
            if c is None:
                logs.append({'sigma':sigma, 'attempt':attempt, 'reason':'no repeated scalar root'})
                continue
            image = ColumnBasis(n)
            for _ in range(r+oversampling):
                image.add(relation_action(api, sigma, random_vector(rng, n, sample_size), c))
                if len(image)>r:
                    break
            if len(image)>r:
                logs.append({'sigma':sigma, 'attempt':attempt, 'c':str(c), 'reason':'rank budget exceeded'})
                continue
            u = image.matrix()
            rr = len(image)
            if rr:
                # Row pivots are obtained by a column basis of U^T.
                rowbasis = ColumnBasis(rr)
                selected = []
                for i, row in enumerate(u):
                    added, _ = rowbasis.add(row)
                    if added:
                        selected.append(i)
                    if len(selected)==rr:
                        break
                residual_rows = []
                for i in selected:
                    e = [F(j==i) for j in range(n)]
                    residual_rows.append(relation_action(api, sigma, e, c, True))
                vt = mm(inverse([u[i] for i in selected]), residual_rows)
                v = transpose(vt)
            else:
                v = [[] for _ in range(n)]
            accepted = True
            for check in range(checks):
                z = random_vector(rng, n, sample_size)
                actual = relation_action(api, sigma, z, c)
                predicted = mv(u, mv(transpose(v, n), z)) if rr else [F(0)]*n
                if actual != predicted:
                    accepted = False
                    logs.append({'sigma':sigma, 'attempt':attempt, 'c':str(c),
                                 'reason':'fresh all-input identity check failed', 'check':check})
                    break
            if accepted:
                return {'status':'ACQUIRED', 'n':n, 'sigma':sigma, 'c':c,
                        'rank':rr, 'U':u, 'V':v, 'search_log':logs,
                        'certificate':{'kind':'exact linear identity, randomized acquisition',
                          'sample_size':sample_size, 'fresh_checks':checks,
                          'candidate_bound':len(signs)*sketch_attempts,
                          'false_accept_probability_bound':F(len(signs)*sketch_attempts, sample_size**checks),
                          'per_new_program_confidence_charge':0}}
    return {'status':'UNKNOWN', 'n':n, 'rank_budget':r, 'search_log':logs}


class DefectModule:
    """Rank-compressed, degree-filtered block Krylov module.

    Each accepted basis vector is queried at most once per native primitive.
    This is a strong retaining baseline, not a claimed new Krylov algorithm.
    """
    def __init__(self, api, seeds, transpose_action=False):
        self.api = api
        self.n = api.n
        self.transpose_action = transpose_action
        self.seeds = seeds
        self.basis = ColumnBasis(self.n)
        self.degrees = []
        self.actions = {}
        self.depth = 0
        for col in transpose(seeds, self.n):
            added, _ = self.basis.add(col)
            if added:
                self.degrees.append(0)

    def extend(self, depth):
        if self.api is None:
            raise ValueError('loaded module has no native access; cannot extend')
        i = 0
        while i<len(self.basis):
            if self.degrees[i]<depth:
                for symbol in ('A','B'):
                    key = (symbol,i)
                    if key not in self.actions:
                        result = self.api.apply(symbol, self.basis.columns[i], self.transpose_action)
                        added, coordinates = self.basis.add(result)
                        if added:
                            self.degrees.append(self.degrees[i]+1)
                        self.actions[key] = coordinates
            i += 1
        self.depth = max(self.depth, depth)
        return self

    @property
    def dim(self):
        return len(self.basis)

    def seed_coordinates(self):
        columns = [self.basis.coordinates(col) for col in transpose(self.seeds, self.n)]
        return transpose(columns, self.dim)

    def apply_coordinates(self, symbol, coefficients):
        width = len(coefficients[0]) if coefficients else 0
        result = zeros(self.dim, width)
        for j, row in enumerate(coefficients):
            if any(row):
                if (symbol,j) not in self.actions:
                    raise ValueError('program exceeds acquired filtered module')
                action = self.actions[(symbol,j)]
                for i, value in enumerate(action):
                    if value:
                        for t, x in enumerate(row):
                            if x:
                                result[i][t] += value*x
        return result

    def word_coordinates(self, word):
        result = self.seed_coordinates()
        # A left word acts right-to-left; a row word acts left-to-right.
        order = word if self.transpose_action else reversed(word)
        for symbol in order:
            result = self.apply_coordinates(symbol, result)
        return result

    def dimension_profile(self):
        return [sum(d<=k for d in self.degrees) for k in range(self.depth+1)]

    def dump(self):
        return {'n':self.n, 'transpose':self.transpose_action,
                'seeds':encode(self.seeds), 'basis_columns':encode(self.basis.columns),
                'degrees':self.degrees, 'depth':self.depth,
                'actions':{f'{s}:{i}':encode(v) for (s,i),v in self.actions.items()}}

    @classmethod
    def load(cls, data):
        obj = cls.__new__(cls)
        obj.api = None
        obj.n = data['n']
        obj.transpose_action = data['transpose']
        obj.seeds = decode_matrix(data['seeds'])
        obj.basis = ColumnBasis(obj.n)
        for col in data['basis_columns']:
            added, _ = obj.basis.add([F(x) for x in col])
            if not added:
                raise ValueError('retained basis is not independent')
        obj.degrees = data['degrees']
        obj.depth = data['depth']
        obj.actions = {}
        for key, values in data['actions'].items():
            symbol, i = key.split(':')
            obj.actions[(symbol,int(i))] = [F(x) for x in values]
        return obj


@dataclass
class Program:
    normal: dict
    correction: list
    degree: int


class AcquiredCalculus:
    def __init__(self, relation, left, right, degree_cap):
        self.relation, self.left, self.right = relation, left, right
        self.n, self.rank = relation['n'], relation['rank']
        self.sigma, self.c = F(relation['sigma']), F(relation['c'])
        self.degree_cap = degree_cap
        self.dl, self.dr = left.dim, right.dim
        self.pairing = mm(transpose(right.basis.matrix(), self.n), left.basis.matrix())
        # Reuse of arbitrarily many programs must not accumulate their entire
        # history. This arithmetic cache is bounded polynomially in the cap.
        self.word_cache = OrderedDict()
        self.word_cache_limit = max(32,4*(degree_cap+1)**2)
        self.left_word_cache = {}
        self.right_word_cache = {}
        self.normalization_steps = 0

    @classmethod
    def acquire_modules(cls, api, relation, degree_cap):
        if relation['status']!='ACQUIRED' or degree_cap<2:
            raise ValueError('need an acquired relation and degree cap >=2')
        left = DefectModule(api, relation['U']).extend(degree_cap-2)
        right = DefectModule(api, relation['V'], True).extend(degree_cap-2)
        return cls(relation, left, right, degree_cap)

    def empty_correction(self):
        return zeros(self.dl, self.dr)

    def scalar(self, value):
        value = F(value)
        return Program({(0,0):value} if value else {}, self.empty_correction(), 0)

    def scale(self, p, value):
        value = F(value)
        return Program({key:value*x for key,x in p.normal.items() if value*x},
                       mscale(p.correction,value), p.degree)

    def add(self, p, q):
        normal = dict(p.normal)
        for key, value in q.normal.items():
            normal[key] = normal.get(key,F(0))+value
            if not normal[key]:
                del normal[key]
        return Program(normal, madd(p.correction,q.correction), max(p.degree,q.degree))

    def _seed_word(self, side, word):
        cache = self.left_word_cache if side=='left' else self.right_word_cache
        module = self.left if side=='left' else self.right
        if word not in cache:
            cache[word] = module.word_coordinates(word)
        return cache[word]

    def prepend(self, symbol, p):
        if p.degree+1>self.degree_cap:
            raise ValueError('program degree exceeds retained cap')
        normal = {}
        correction = self.left.apply_coordinates(symbol,p.correction)
        def put(key, value):
            normal[key] = normal.get(key,F(0))+value
            if not normal[key]:
                del normal[key]
        for (i,j), value in p.normal.items():
            if symbol=='B':
                put((i+1,j),value)
            elif symbol=='A':
                put((i,j+1),value*self.sigma**i)
                if i:
                    put((i-1,j),value*self.c*sum(self.sigma**t for t in range(i)))
                if self.rank:
                    for t in range(i):
                        l = self._seed_word('left','B'*t)
                        r = self._seed_word('right','B'*(i-1-t)+'A'*j)
                        correction = madd(correction,mm(l,transpose(r)),value*self.sigma**t)
            else:
                raise ValueError('unknown primitive')
        self.normalization_steps += 1
        return Program(normal,correction,p.degree+1)

    def word(self, word):
        if word not in self.word_cache:
            p = self.scalar(1)
            for symbol in reversed(word):
                p = self.prepend(symbol,p)
            self.word_cache[word] = p
            while len(self.word_cache)>self.word_cache_limit:
                self.word_cache.popitem(last=False)
        self.word_cache.move_to_end(word)
        return self.word_cache[word]

    def _left_normal_action(self, normal, correction):
        result = self.empty_correction()
        for (i,j), value in normal.items():
            current = correction
            for symbol in reversed('B'*i+'A'*j):
                current = self.left.apply_coordinates(symbol,current)
            result = madd(result,current,value)
        return result

    def _right_normal_action(self, correction, normal):
        result = self.empty_correction()
        for (i,j), value in normal.items():
            current = transpose(correction, self.dr)
            for symbol in 'B'*i+'A'*j:
                current = self.right.apply_coordinates(symbol,current)
            result = madd(result,transpose(current,self.dl),value)
        return result

    def multiply(self, p, q):
        degree = p.degree+q.degree
        if degree>self.degree_cap:
            raise ValueError('circuit degree exceeds retained cap')
        result = self.scalar(0)
        for (i,j), x in p.normal.items():
            for (k,l), y in q.normal.items():
                ordered_product = self.word('B'*i+'A'*j+'B'*k+'A'*l)
                result = self.add(result,self.scale(ordered_product,x*y))
        result.correction = madd(result.correction,self._left_normal_action(p.normal,q.correction))
        result.correction = madd(result.correction,self._right_normal_action(p.correction,q.normal))
        result.correction = madd(result.correction,mm(mm(p.correction,self.pairing),q.correction))
        result.degree = degree
        return result

    def circuit(self, instructions, output=-1):
        """Evaluate a DAG without expanding it into its input word list."""
        values = []
        for node in instructions:
            op = node['op']
            if op in ('A','B'):
                value = self.word(op)
            elif op=='scalar':
                value = self.scalar(node['value'])
            elif op=='scale':
                value = self.scale(values[node['arg']],node['value'])
            elif op=='add':
                value = self.add(values[node['left']],values[node['right']])
            elif op=='mul':
                value = self.multiply(values[node['left']],values[node['right']])
            else:
                raise ValueError('unknown circuit operation')
            values.append(value)
        return values[output]

    def normal_program(self, normal):
        result = self.scalar(0)
        for (i,j), value in normal.items():
            result = self.add(result,self.scale(self.word('B'*i+'A'*j),value))
        return result

    def correction_action(self, correction, v):
        if not self.rank:
            return [F(0)]*self.n
        return mv(self.left.basis.matrix(),mv(correction,mv(transpose(self.right.basis.matrix()),v)))

    def compare(self, p, q):
        difference = self.add(p,self.scale(q,-1))
        if difference.normal:
            return {'status':'UNKNOWN', 'reason':'different ideal normal forms; extra native identities may exist'}
        rank = matrix_rank(difference.correction)
        return {'status':'EXACT_DIFFERENCE', 'rank':rank,
                'native_equal':rank==0, 'valid_input_dimension':self.n-rank,
                'correction':difference.correction}

    def synthesize_polynomial_commutator(self, coefficients):
        """Compile [A,f(B)] into c f'(B) plus an exact low-rank correction.

        f is a NEW polynomial of the native B operator. It is not implicitly
        a Galerkin projection of multiplication by a physical function.
        Synthesis uses no native calls. Execution below uses B but never A.
        """
        if self.sigma != 1:
            raise ValueError('this procedure uses the commutator law')
        return self.synthesize_twisted_polynomial_derivation(coefficients)

    def synthesize_twisted_polynomial_derivation(self, coefficients):
        """Compile A f(B)-f(qB) A using the ACQUIRED scalar q.

        The normal term is c sum_j [j]_q f_j B^(j-1). The same executor
        therefore specializes to ordinary, signed, or q-difference calculus
        according to the acquired relation, with finite-native defects retained.
        """
        coefficients = [F(x) for x in coefficients]
        while len(coefficients)>1 and not coefficients[-1]:
            coefficients.pop()
        if len(coefficients)>self.degree_cap:
            raise ValueError('polynomial commutator exceeds acquired degree')
        target = self.scalar(0)
        for j,c in enumerate(coefficients):
            if c:
                target = self.add(target,self.scale(self.word('A'+'B'*j),c))
                target = self.add(target,self.scale(self.word('B'*j+'A'),-c*self.sigma**j))
        derivative = [self.c*sum(self.sigma**t for t in range(j))*coefficients[j]
                      for j in range(1,len(coefficients))] or [F(0)]
        expected = {(i,0):c for i,c in enumerate(derivative) if c}
        if target.normal != expected:
            raise AssertionError('symbolic derivative normalization failed')
        factors = rank_factorization(target.correction)
        if factors is None:
            left,right = [[] for _ in range(self.n)],[[] for _ in range(self.n)]
        else:
            f,g = factors
            left = mm(self.left.basis.matrix(),f)
            right = mm(self.right.basis.matrix(),transpose(g))
        return CompiledCommutator(coefficients,derivative,left,right,self.n,self.sigma)

    def dump(self):
        return {'kind':'acquired defective operator calculus',
                'relation':encode(self.relation), 'degree_cap':self.degree_cap,
                'left':self.left.dump(), 'right':self.right.dump(),
                'protected_domain':{'dimension':self.n-self.dr,
                                    'constraint':'right.basis_columns times input = 0'}}

    @classmethod
    def load(cls, data):
        relation = dict(data['relation'])
        relation['c'] = F(relation['c'])
        relation['sigma'] = F(relation['sigma'])
        relation['U'], relation['V'] = decode_matrix(relation['U']),decode_matrix(relation['V'])
        return cls(relation,DefectModule.load(data['left']),DefectModule.load(data['right']),data['degree_cap'])


def encode(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,list):
        return [encode(x) for x in value]
    if isinstance(value,tuple):
        return [encode(x) for x in value]
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    return value


def decode_matrix(value):
    return [[F(x) for x in row] for row in value]


def rank_factorization(a):
    """Exact small matrix factorization a=F G, with independent factors."""
    if not a or not a[0]:
        return None
    basis = ColumnBasis(len(a))
    for col in transpose(a):
        basis.add(col)
    if not len(basis):
        return None
    f = basis.matrix()
    g = transpose([basis.coordinates(col) for col in transpose(a)])
    return f,g


@dataclass
class CompiledCommutator:
    target_polynomial: list
    normal_polynomial: list
    correction_left: list
    correction_right: list
    n: int
    twist: F = F(1)

    @property
    def rank(self):
        return len(self.correction_left[0])

    def execute(self,api,v):
        p = list(self.normal_polynomial)
        while len(p)>1 and not p[-1]:
            p.pop()
        value = [p[-1]*x for x in v]
        for c in reversed(p[:-1]):
            value = [x+c*y for x,y in zip(api.apply('B',value),v)]
        if self.rank:
            correction = mv(self.correction_left,mv(transpose(self.correction_right),v))
            value = [x+y for x,y in zip(value,correction)]
        return value

    def dump(self):
        return encode({'target':'A f(B)-f(q B) A', 'q':self.twist, 'n':self.n,
                       'f_coefficients_in_increasing_powers':self.target_polynomial,
                       'normal_polynomial_coefficients':self.normal_polynomial,
                       'correction_left':self.correction_left,
                       'correction_right':self.correction_right,
                       'correction_rank':self.rank,
                       'uncorrected_valid_domain_dimension':self.n-self.rank,
                       'validity':'conditional on the retained native relation; all input vectors'})

    @classmethod
    def load(cls,data):
        return cls([F(x) for x in data['f_coefficients_in_increasing_powers']],
                   [F(x) for x in data['normal_polynomial_coefficients']],
                   decode_matrix(data['correction_left']),decode_matrix(data['correction_right']),
                   data['n'],F(data.get('q',1)))
