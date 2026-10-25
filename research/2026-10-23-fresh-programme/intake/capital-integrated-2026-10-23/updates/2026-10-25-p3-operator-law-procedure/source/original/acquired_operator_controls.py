"""Independent sources and exact falsification/transfer controls.

Run: python acquired_operator_controls.py
No physical measurements, downloaded datasets, or recovered historical code.
The learner sees only a linear action/transpose API; this file also owns the
separate source-coordinate reference used AFTER the artifact is frozen.
"""
from fractions import Fraction as F
from collections import Counter
import json
from pathlib import Path
import random
import time

from acquired_operator_calculus import (
    acquire_relation, AcquiredCalculus, ColumnBasis, DefectModule, Program,
    encode, eye, matrix_rank, mm, mv, transpose, zeros,
)

ROOT = Path(__file__).resolve().parent


class RationalScramble:
    def __init__(self,n,seed):
        self.n = n
        rng = random.Random(seed)
        self.permutation = list(range(n))
        rng.shuffle(self.permutation)
        self.reflectors = [[F(rng.choice((-1,1))) for _ in range(n)] for _ in range(2)]

    def reflect(self,vector,v):
        a = 2*sum((x*y for x,y in zip(vector,v)),F(0))/self.n
        return [x-a*y for x,y in zip(vector,v)]

    def forward(self,vector):
        for v in self.reflectors:
            vector = self.reflect(vector,v)
        return [vector[i] for i in self.permutation]

    def backward(self,vector):
        unpermuted = [F(0)]*self.n
        for j,i in enumerate(self.permutation):
            unpermuted[i] = vector[j]
        for v in reversed(self.reflectors):
            unpermuted = self.reflect(unpermuted,v)
        return unpermuted


class MatrixFreeSource:
    def __init__(self,n,kind='derivative',seed=10,a=F(7,3),b=F(1)):
        self.n,self.kind,self.a,self.b = n,kind,F(a),F(b)
        self.scramble = RationalScramble(n,seed)
        self.counts = Counter()
        rng = random.Random(seed+901)
        if kind=='generic':
            self.dense = {s:[[F(rng.randrange(-2,3)) for _ in range(n)] for _ in range(n)] for s in ('A','B')}

    def derivative(self,v,trans=False):
        if not trans:
            return [F(i+1)*v[i+1] for i in range(self.n-1)]+[F(0)]
        return [F(0)]+[F(i)*v[i-1] for i in range(1,self.n)]

    def base_apply(self,symbol,v,trans=False):
        if self.kind=='generic':
            return mv(transpose(self.dense[symbol]) if trans else self.dense[symbol],v)
        if self.kind=='central_difference':
            if symbol=='B':
                return [i*x for i,x in enumerate(v)]
            sign = -1 if trans else 1
            return [sign*((v[i+1] if i+1<self.n else 0)-(v[i-1] if i else 0))/2 for i in range(self.n)]
        if self.kind=='fermion':
            result = [F(0)]*self.n
            lower = (symbol=='A') != trans
            for j in range(0,self.n,2):
                result[j if lower else j+1] = (self.a if symbol=='A' else self.b)*v[j+1 if lower else j]
            return result
        if self.kind=='chebyshev':
            if symbol=='A':
                out = [F(0)]*self.n
                sums = [F(0),F(0)]
                if not trans:
                    for i in reversed(range(self.n)):
                        out[i] = (1 if i==0 else 2)*sums[1-i%2]
                        sums[i%2] += i*v[i]
                else:
                    for j in range(self.n):
                        out[j] = j*sums[1-j%2]
                        sums[j%2] += (1 if j==0 else 2)*v[j]
                return [self.a*x for x in out]
            out = [F(0)]*self.n
            if not trans:
                out[1] += v[0]
                for j in range(1,self.n):
                    out[j-1] += v[j]/2
                    if j+1<self.n:
                        out[j+1] += v[j]/2
            else:
                out[0] = v[1]
                for j in range(1,self.n):
                    out[j] = (v[j-1]+(v[j+1] if j+1<self.n else 0))/2
            return [self.b*x for x in out]
        if symbol=='A':
            if self.kind=='q_derivative':
                # A standard q-difference source at q=2. The learner is not
                # told q, nor that a q-commutation relation should exist.
                if not trans:
                    value = [(2**(i+1)-1)*v[i+1] for i in range(self.n-1)]+[F(0)]
                else:
                    value = [F(0)]+[(2**i-1)*v[i-1] for i in range(1,self.n)]
                return [self.a*x for x in value]
            value = self.derivative(v,trans)
            if self.kind=='kinetic':
                value = self.derivative(value,trans)
            return [self.a*x for x in value]
        if symbol=='B':
            value = (list(v[1:])+[F(0)]) if trans else ([F(0)]+list(v[:-1]))
            return [self.b*x for x in value]
        raise ValueError(symbol)

    def apply(self,symbol,v,transpose=False):
        self.counts[symbol+('T' if transpose else '')] += 1
        native = self.scramble.backward(v)
        response = self.base_apply(symbol,native,transpose)
        return self.scramble.forward(response)

    def snapshot(self):
        total = sum(self.counts.values())
        return {'primitive_action_calls':total, 'returned_field_elements':total*self.n,
                'by_primitive':dict(self.counts)}


class CommutatorLift:
    """Expose K=[A,B],B using ONLY the underlying source action APIs."""
    def __init__(self,source):
        self.source,self.n = source,source.n

    def apply(self,symbol,v,transpose=False):
        if symbol=='B':
            return self.source.apply('B',v,transpose)
        if not transpose:
            ab = self.source.apply('A',self.source.apply('B',v))
            ba = self.source.apply('B',self.source.apply('A',v))
        else:
            ab = self.source.apply('B',self.source.apply('A',v,True),True)
            ba = self.source.apply('A',self.source.apply('B',v,True),True)
        return [x-y for x,y in zip(ab,ba)]

    def base_apply(self,symbol,v,transpose=False):
        if symbol=='B':
            return self.source.base_apply('B',v,transpose)
        if not transpose:
            ab = self.source.base_apply('A',self.source.base_apply('B',v))
            ba = self.source.base_apply('B',self.source.base_apply('A',v))
        else:
            ab = self.source.base_apply('B',self.source.base_apply('A',v,True),True)
            ba = self.source.base_apply('A',self.source.base_apply('B',v,True),True)
        return [x-y for x,y in zip(ab,ba)]


def apply_word(base,word,v):
    for symbol in reversed(word):
        v = base.base_apply(symbol,v)
    return v


def apply_normal(base,normal,v):
    result = [F(0)]*base.n
    for (i,j),c in normal.items():
        y = apply_word(base,'B'*i+'A'*j,v)
        result = [x+c*z for x,z in zip(result,y)]
    return result


def apply_circuit(base,nodes,v,output=-1):
    # Compile each DAG node to a native reference application. The memo caches
    # expression closures, not answers for a different input vector.
    functions = []
    for node in nodes:
        op = node['op']
        if op in ('A','B'):
            functions.append(lambda x,s=op:base.base_apply(s,x))
        elif op=='scalar':
            functions.append(lambda x,c=F(node['value']):[c*y for y in x])
        elif op=='scale':
            f,c = functions[node['arg']],F(node['value'])
            functions.append(lambda x,f=f,c=c:[c*y for y in f(x)])
        elif op=='add':
            f,g = functions[node['left']],functions[node['right']]
            functions.append(lambda x,f=f,g=g:[a+b for a,b in zip(f(x),g(x))])
        elif op=='mul':
            f,g = functions[node['left']],functions[node['right']]
            functions.append(lambda x,f=f,g=g:f(g(x)))
        else:
            raise ValueError(op)
    return functions[output](v)


def in_source_coordinates(calculus,source):
    left = transpose([source.scramble.backward(v) for v in calculus.left.basis.columns],source.n)
    right = transpose([source.scramble.backward(v) for v in calculus.right.basis.columns],source.n)
    return left,right


def exact_relation_reference(source,api,relation):
    if relation['status']!='ACQUIRED':
        return False
    # The all-input check runs independently in source coordinates; it never
    # changes or supplies data to the learner.
    left = transpose([source.scramble.backward(v) for v in transpose(relation['U'])],source.n)
    right = transpose([source.scramble.backward(v) for v in transpose(relation['V'])],source.n)
    candidate = mm(left,transpose(right)) if relation['rank'] else zeros(source.n,source.n)
    for j in range(source.n):
        e = [F(i==j) for i in range(source.n)]
        ab = api.base_apply('A',api.base_apply('B',e))
        ba = api.base_apply('B',api.base_apply('A',e))
        native = [x-relation['sigma']*y-relation['c']*z for x,y,z in zip(ab,ba,e)]
        if native != [candidate[i][j] for i in range(source.n)]:
            return False
    return True


def all_input_program_check(calculus,source,base,program,reference_apply,bases):
    left,right = bases
    predicted = mm(mm(left,program.correction),transpose(right)) if calculus.rank else zeros(source.n,source.n)
    for j in range(source.n):
        e = [F(i==j) for i in range(source.n)]
        truth = reference_apply(e)
        normal = apply_normal(base,program.normal,e)
        delta = [x-y for x,y in zip(truth,normal)]
        if delta != [predicted[i][j] for i in range(source.n)]:
            raise AssertionError(f'all-input correction failed at basis column {j}')
    return matrix_rank(program.correction)


def random_dag(rng,cap):
    # Fixed grammar, new coefficients and topology AFTER acquisition.
    nodes = [{'op':'A'},{'op':'B'},{'op':'scalar','value':1}]
    degrees = [1,1,0]
    for _ in range(14):
        choice = rng.choice(('add','mul','scale'))
        if choice=='scale':
            i = rng.randrange(len(nodes))
            nodes.append({'op':'scale','arg':i,'value':rng.choice((-5,-3,-1,2,4,7))})
            degrees.append(degrees[i])
        elif choice=='add':
            i,j = rng.randrange(len(nodes)),rng.randrange(len(nodes))
            nodes.append({'op':'add','left':i,'right':j})
            degrees.append(max(degrees[i],degrees[j]))
        else:
            possibilities = [(i,j) for i in range(len(nodes)) for j in range(len(nodes))
                             if degrees[i]+degrees[j]<=cap]
            i,j = rng.choice(possibilities)
            nodes.append({'op':'mul','left':i,'right':j})
            degrees.append(degrees[i]+degrees[j])
    # Ensure the output contains a nontrivial order-sensitive held-out factor.
    nodes += [{'op':'mul','left':0,'right':1},
              {'op':'add','left':len(nodes)-1,'right':len(nodes)}]
    return nodes


def new_program_workload(calculus,source,base,count=12,seed=9001):
    rng = random.Random(seed)
    bases = in_source_coordinates(calculus,source)
    checks,nonzero,ranks = 0,0,[]
    held_out = []
    # Words are sampled only after the serialized artifact has been loaded.
    words = ['AB','AABB','ABABAB','AAAABBBB','BAAABBAB']
    words = [w for w in words if len(w)<=calculus.degree_cap]
    words += [''.join(rng.choice('AB') for _ in range(rng.randrange(2,calculus.degree_cap+1)))
              for _ in range(count)]
    for word in words:
        p = calculus.word(word)
        rank = all_input_program_check(calculus,source,base,p,
                                      lambda v,w=word:apply_word(base,w,v),bases)
        checks += 1
        nonzero += bool(rank)
        ranks.append(rank)
        held_out.append({'kind':'word','word':word,'correction_rank':rank})
    for _ in range(count):
        dag = random_dag(rng,calculus.degree_cap)
        p = calculus.circuit(dag)
        rank = all_input_program_check(calculus,source,base,p,
                                      lambda v,n=dag:apply_circuit(base,n,v),bases)
        checks += 1
        nonzero += bool(rank)
        ranks.append(rank)
        held_out.append({'kind':'DAG','nodes':dag,'correction_rank':rank,'degree':p.degree})
    return {'programs_checked':checks, 'all_input_columns_checked':checks*source.n,
            'nonzero_boundary_corrections':nonzero, 'max_correction_rank':max(ranks),
            'normalization_steps':calculus.normalization_steps,
            'word_cache_entries':len(calculus.word_cache), 'held_out_programs':held_out}


def ideal_blind_spot(n):
    source = MatrixFreeSource(n,a=1)
    passed = 0
    for j in range(n-1):
        e = [F(i==j) for i in range(n)]
        delta = [x-y-z for x,y,z in zip(
            source.base_apply('A',source.base_apply('B',e)),
            source.base_apply('B',source.base_apply('A',e)),e)]
        passed += not any(delta)
    top = [F(i==n-1) for i in range(n)]
    defect = [x-y-z for x,y,z in zip(
        source.base_apply('A',source.base_apply('B',top)),
        source.base_apply('B',source.base_apply('A',top)),top)]
    return {'restricted_basis_probes_that_miss_defect':passed,
            'top_basis_defect':encode(defect), 'global_ideal_law_false':any(defect),
            'associative_algebra_dimension_by_matrix_unit_proof':n*n}


def run_main():
    started = time.perf_counter()
    source = MatrixFreeSource(64,a=F(7,3),seed=182)
    relation = acquire_relation(source,rank_budget=1,seed=824)
    assert relation['status']=='ACQUIRED'
    after_relation = source.snapshot()
    assert exact_relation_reference(source,source,relation)
    calculus = AcquiredCalculus.acquire_modules(source,relation,degree_cap=8)
    after_modules = source.snapshot()
    artifact_path = ROOT/'acquired_operator_calculus_retained.json'
    artifact_path.write_text(json.dumps(calculus.dump(),indent=2)+'\n')
    # Genuine reuse from an object with no source pointer and no old query answers.
    retained = AcquiredCalculus.load(json.loads(artifact_path.read_text()))
    assert retained.left.api is None and retained.right.api is None
    new_tasks = new_program_workload(retained,source,source)
    assert source.snapshot()==after_modules
    # Specific-pair cancellation can enlarge the domain beyond the common one.
    commutator = retained.add(retained.word('AB'),retained.scale(retained.word('BA'),-1))
    comparison = retained.compare(commutator,retained.scalar(relation['c']))
    assert comparison['rank']==1
    result = {
        'kind':'new exact computational controls; no physical data',
        'native_dimension':source.n, 'degree_cap':8,
        'learned_sigma':relation['sigma'],'learned_c':str(relation['c']),
        'learned_defect_rank':relation['rank'],
        'relation_all_input_reference_check':True,
        'after_relation_acquisition':after_relation,'after_module_acquisition':after_modules,
        'reuse_native_calls':0,
        'left_dimension_profile':retained.left.dimension_profile(),
        'right_dimension_profile':retained.right.dimension_profile(),
        'common_protected_input_dimension':source.n-retained.right.dim,
        'basic_commutator_protected_input_dimension':comparison['valid_input_dimension'],
        'independent_dense_tomography_primitive_calls':2*source.n,
        'tomography_retained_matrix_entries':2*source.n**2,
        'native_vector_width':source.n,
        'certificate':encode(relation['certificate']),
        'new_tasks':new_tasks,'restricted_excitation_failure':ideal_blind_spot(source.n),
        'wall_seconds':time.perf_counter()-started,
    }
    # Deliberately off-class numerical stencil and generic operators.
    controls = []
    for kind in ('central_difference','generic'):
        bad = MatrixFreeSource(17,kind=kind,seed=404)
        got = acquire_relation(bad,rank_budget=1,seed=227,sketch_attempts=1)
        assert got['status']=='UNKNOWN'
        controls.append({'source':kind,'result':encode(got),'cost':bad.snapshot()})
    result['failed_applicability_controls'] = controls
    (ROOT/'acquired_operator_calculus_results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('new_tasks','restricted_excitation_failure','failed_applicability_controls')},indent=2))
    print(json.dumps({'held_out':{k:v for k,v in new_tasks.items() if k!='held_out_programs'},
                      'off_class_statuses':[x['result']['status'] for x in controls]},indent=2))


def run_new_primitive():
    """A supplied kinetic operator fails; a commutator macro obtains a calculus.

    Declared macro grammar: either use A,B directly, or replace A by [A,B].
    The grammar, rank budget, and source linearity are NOT learned.
    """
    started = time.perf_counter()
    source = MatrixFreeSource(96,kind='kinetic',seed=928,a=F(3,2),b=F(2,3))
    direct = acquire_relation(source,rank_budget=2,seed=911,sketch_attempts=1)
    assert direct['status']=='UNKNOWN'
    direct_cost = source.snapshot()
    lifted = CommutatorLift(source)
    relation = acquire_relation(lifted,rank_budget=2,seed=912,sketch_attempts=1)
    assert relation['status']=='ACQUIRED'
    after_relation = source.snapshot()
    assert exact_relation_reference(source,lifted,relation)
    calculus = AcquiredCalculus.acquire_modules(lifted,relation,degree_cap=7)
    after_modules = source.snapshot()
    artifact_path = ROOT/'acquired_kinetic_calculus_retained.json'
    artifact_path.write_text(json.dumps(calculus.dump(),indent=2)+'\n')
    retained = AcquiredCalculus.load(json.loads(artifact_path.read_text()))
    workload = new_program_workload(retained,source,lifted,count=8,seed=293)
    assert source.snapshot()==after_modules
    # A consequential task family: derive the commutator derivative of each new
    # polynomial f(B), and obtain all finite-boundary corrections.
    polynomial_queries = []
    rng = random.Random(320)
    bases = in_source_coordinates(retained,source)
    for degree in (2,3,4,5,6):
        coefficients = [F(rng.randrange(-7,8)) for _ in range(degree+1)]
        coefficients[-1] = F(degree+2)
        lhs = retained.scalar(0)
        derivative = retained.scalar(0)
        for j,c in enumerate(coefficients):
            lhs = retained.add(lhs,retained.scale(retained.word('A'+'B'*j),c))
            lhs = retained.add(lhs,retained.scale(retained.word('B'*j+'A'),-c))
            if j:
                derivative = retained.add(derivative,retained.scale(retained.word('B'*(j-1)),c*j*relation['c']))
        comparison = retained.compare(lhs,derivative)
        assert comparison['status']=='EXACT_DIFFERENCE'
        difference = retained.add(lhs,retained.scale(derivative,-1))
        assert not difference.normal
        def native(v):
            result = [F(0)]*source.n
            for j,c in enumerate(coefficients):
                ab = apply_word(lifted,'A'+'B'*j,v)
                ba = apply_word(lifted,'B'*j+'A',v)
                dv = apply_word(lifted,'B'*(j-1),v) if j else [F(0)]*source.n
                result = [x+c*(a-b-j*relation['c']*d) for x,a,b,d in zip(result,ab,ba,dv)]
            return result
        rank = all_input_program_check(retained,source,lifted,difference,native,bases)
        polynomial_queries.append({'coefficients':encode(coefficients),'degree':degree,
                                   'exact_correction_rank':rank,
                                   'valid_input_dimension':source.n-rank})
    assert source.snapshot()==after_modules
    result = {'kind':'new mathematical source and new acquired primitive; no physical data',
              'n':source.n,'original_source_primitives':['kinetic operator','coordinate multiplication'],
              'declared_macro_search':['A,B','[A,B],B'],
              'direct_attempt':encode(direct),'after_direct_failure':direct_cost,
              'acquired_macro':'K=[A,B]', 'learned_relation':'K B - B K = c I + U V^T',
              'learned_c':str(relation['c']),'learned_rank':relation['rank'],
              'all_input_relation_reference_check':True,
              'after_relation_acquisition':after_relation,'after_module_acquisition':after_modules,
              'reuse_native_calls':0,'left_dimension_profile':retained.left.dimension_profile(),
              'right_dimension_profile':retained.right.dimension_profile(),
              'protected_input_dimension':source.n-retained.right.dim,
              'tomography_primitive_calls':2*source.n,
              'new_tasks':workload,'new_polynomial_derivative_queries':polynomial_queries,
              'wall_seconds':time.perf_counter()-started}
    (ROOT/'acquired_kinetic_calculus_results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('new_tasks','direct_attempt')},indent=2))


def run_noncommutative_control():
    # The second search sign really matters: an exact anticommutation source.
    source = MatrixFreeSource(20,kind='fermion',seed=187,a=F(5,2),b=F(4,3))
    relation = acquire_relation(source,rank_budget=0,seed=880,sketch_attempts=1)
    assert relation['status']=='ACQUIRED' and relation['sigma']==-1 and relation['rank']==0
    assert exact_relation_reference(source,source,relation)
    calculus = AcquiredCalculus.acquire_modules(source,relation,degree_cap=8)
    before = source.snapshot()
    # Here normal-ordering is global; there are no defect-module vectors.
    for w in ('AB','ABA','AABB','ABABAB','AAAABBBB'):
        p = calculus.word(w)
        for e in eye(source.n):
            assert apply_word(source,w,e)==apply_normal(source,p.normal,e)
    assert source.snapshot()==before
    # The native source also has A^2=0. The learned single relation is a sound
    # but incomplete native equality oracle, and correctly returns UNKNOWN.
    extra_identity = calculus.compare(calculus.word('AA'),calculus.scalar(0))
    assert extra_identity['status']=='UNKNOWN'
    result = {'learned_sigma':relation['sigma'],'learned_c':str(relation['c']),
              'learned_rank':relation['rank'],'cost':source.snapshot(),
              'rejected_search_log':relation['search_log'],
              'additional_native_identity_A_squared_zero':True,
              'single_law_evaluator_result':extra_identity}
    (ROOT/'acquired_operator_anticommutation_control.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps(encode(result),indent=2))


def native_polynomial(api,coefficients,v):
    coefficients = [F(c) for c in coefficients]
    value = [coefficients[-1]*x for x in v]
    for c in reversed(coefficients[:-1]):
        value = [x+c*y for x,y in zip(api.apply('B',value),v)]
    return value


def run_spectral_transfer_and_synthesis():
    """New discretization, new native law acquisition, new compiled procedures."""
    started = time.perf_counter()
    source = MatrixFreeSource(40,kind='chebyshev',seed=882,a=1,b=1)
    # Reusing an old instance's factors would be invalid. Reacquisition is paid.
    relation = acquire_relation(source,rank_budget=1,seed=764,sketch_attempts=1)
    assert relation['status']=='ACQUIRED'
    assert exact_relation_reference(source,source,relation)
    after_relation = source.snapshot()
    calculus = AcquiredCalculus.acquire_modules(source,relation,degree_cap=8)
    after_acquisition = source.snapshot()
    artifact = ROOT/'acquired_spectral_calculus_retained.json'
    artifact.write_text(json.dumps(calculus.dump(),indent=2)+'\n')
    retained = AcquiredCalculus.load(json.loads(artifact.read_text()))
    new_tasks = new_program_workload(retained,source,source,count=6,seed=567)
    assert source.snapshot()==after_acquisition
    rng = random.Random(992)
    procedures,executions = [],[]
    for degree in (2,4,7):
        coefficients = [F(rng.randrange(-4,5)) for _ in range(degree)]+[F(3)]
        before = source.snapshot()
        procedure = retained.synthesize_polynomial_commutator(coefficients)
        assert source.snapshot()==before
        # New inputs include an arbitrary mixed vector and the native top mode,
        # which exposes a correction missed by a low-degree-only evaluator.
        inputs = [[F(rng.randrange(-3,4)) for _ in range(source.n)],
                  source.scramble.forward([F(j==source.n-1) for j in range(source.n)])]
        for index,v in enumerate(inputs):
            before_optimized = source.snapshot()['primitive_action_calls']
            y = procedure.execute(source,v)
            optimized_calls = source.snapshot()['primitive_action_calls']-before_optimized
            before_reference = source.snapshot()['primitive_action_calls']
            first = source.apply('A',native_polynomial(source,coefficients,v))
            second = native_polynomial(source,coefficients,source.apply('A',v))
            native = [a-b for a,b in zip(first,second)]
            direct_calls = source.snapshot()['primitive_action_calls']-before_reference
            assert y==native
            # The correction's norm is descriptive, not a numerical certificate.
            ideal = native_polynomial(source,procedure.normal_polynomial,v)
            corrections = [a-b for a,b in zip(y,ideal)]
            executions.append({'degree':degree,'input':index,
                               'compiled_primitive_calls':optimized_calls,
                               'direct_primitive_calls':direct_calls,
                               'exact_output_equal':True,
                               'ideal_without_defect_failed':any(corrections)})
        # All-input check on the new compiled procedure in addition to execution.
        for j in range(source.n):
            e = [F(i==j) for i in range(source.n)]
            lhs = [F(0)]*source.n
            for k,c in enumerate(coefficients):
                a = apply_word(source,'A'+'B'*k,e)
                b = apply_word(source,'B'*k+'A',e)
                lhs = [x+c*(aa-bb) for x,aa,bb in zip(lhs,a,b)]
            normal = apply_normal(source,{(i,0):c for i,c in enumerate(procedure.normal_polynomial)},e)
            x = source.scramble.forward(e)
            correction = mv(procedure.correction_left,mv(transpose(procedure.correction_right),x))
            predicted = [a+b for a,b in zip(normal,source.scramble.backward(correction))]
            assert lhs==predicted
        procedures.append(procedure.dump())
    # Source interpretation failure: projected physical x^2 multiplication is
    # NOT the square of projected coordinate multiplication. For the top mode,
    # the omitted intermediate T_n mode returns a quarter of T_{n-1}.
    top = [F(i==source.n-1) for i in range(source.n)]
    projected_square = apply_word(source,'BB',top)
    true_projected_x_squared = list(projected_square)
    true_projected_x_squared[-1] += F(1,4)
    assert true_projected_x_squared!=projected_square
    result = {'source':'coefficient-truncated Chebyshev differentiation and multiplication',
              'n':source.n,'degree_cap':8,'learned_c':str(relation['c']),
              'learned_rank':relation['rank'],
              'after_relation_acquisition':after_relation,
              'after_module_acquisition':after_acquisition,
              'new_program_synthesis_native_calls':0,
              'left_dimension_profile':retained.left.dimension_profile(),
              'right_dimension_profile':retained.right.dimension_profile(),
              'common_protected_input_dimension':source.n-retained.right.dim,
              'tomography_primitive_calls':2*source.n,
              'new_tasks':new_tasks,'new_procedure_executions':executions,
              'projection_interface_failure':{'P_x_squared_P_not_equal_P_x_P_squared':True,
                 'top_mode_difference':'1/4 times top mode',
                 'scope':'compiler target is f(B); no projected physical-potential contract inferred'},
              'wall_seconds':time.perf_counter()-started}
    (ROOT/'acquired_spectral_procedures.json').write_text(json.dumps(procedures,indent=2)+'\n')
    (ROOT/'acquired_spectral_calculus_results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='new_tasks'},indent=2))


if __name__=='__main__':
    run_main()
    run_new_primitive()
    run_noncommutative_control()
    run_spectral_transfer_and_synthesis()
