"""Acquire a rank-one law from an unlabelled finite operator-word library.

This is minors modeling/direct linearization of MinRank, a known algebraic
technique. The research use here is matrix-free acquisition, an observed
uniqueness gate, independent all-input residual certification, and transfer to
the defect calculus. No efficient general MinRank solver is claimed.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import random
import time

from acquired_operator_calculus import (
    AcquiredCalculus, ColumnBasis, encode, inverse, mm, mv, random_vector,
    relation_action, transpose,
)

WORDS = ('','A','B','AA','AB','BA','BB')


class WordSketch:
    """One acquired interaction record shared by competing representations."""
    def __init__(self,api,seed=0,sketch_size=8,sample_size=257):
        self.api,self.n = api,api.n
        self.rng = random.Random(seed)
        self.sketch_size,self.sample_size = sketch_size,sample_size
        self.omega = [random_vector(self.rng,self.n,sample_size) for _ in range(sketch_size)]
        self.left = [random_vector(self.rng,self.n,sample_size) for _ in range(sketch_size)]
        self.responses = [{'':v} for v in self.omega]
        self.compressed = {}
        self.ensure(WORDS)

    def ensure(self,words):
        for w in sorted(set(words),key=len):
            if w not in self.compressed:
                if w:
                    self.ensure((w[1:],))
                    for response in self.responses:
                        response[w] = self.api.apply(w[0],response[w[1:]])
                self.compressed[w] = mm(self.left,transpose([r[w] for r in self.responses]))

    def dump(self):
        return encode({'n':self.n,'sketch_size':self.sketch_size,
                       'right_probe_columns':self.omega,'left_projection_rows':self.left,
                       'native_word_responses':self.responses,
                       'compressed_word_matrices':self.compressed,
                       'scope':'actual structural acquisition data, shared across representation attempts'})


def nullspace_of_rows(rowbasis):
    free = [i for i in range(rowbasis.n) if i not in rowbasis.pivots]
    result = []
    for j in free:
        value = [F(0)]*rowbasis.n
        value[j] = F(1)
        for pivot,row in reversed(list(zip(rowbasis.pivots,rowbasis.echelon))):
            value[pivot] = -sum((x*y for i,(x,y) in enumerate(zip(row,value)) if i!=pivot),F(0))
        result.append(value)
    return result


def word_responses(api,words,v):
    responses = {'':v}
    for word in sorted(words,key=len):
        if word and word not in responses:
            # Any omitted suffix is a temporary computational subexpression.
            suffix = word[1:]
            if suffix not in responses:
                responses.update(word_responses(api,(suffix,),v))
            responses[word] = api.apply(word[0],responses[suffix])
    return responses


def discover_quadratic_rank_one(api,*,seed=0,sketch_size=8,sample_size=257,checks=4,sketch=None):
    """Return acquired q-Weyl relation, an unsupported law, or UNKNOWN.

    Inputs are a complexity-limited WORD library and rank-one budget, not a
    proposed commutator. If the quadratic-minor coefficient system has a
    one-dimensional kernel, its decomposable point is the only possible
    nonzero rank<=1 law in this word library, up to scalar. This uniqueness
    conclusion is deterministic from exact observations. Existence of the
    lifted native law is separately checked on fresh vectors.
    """
    n,d = api.n,len(WORDS)
    if sketch_size>n:
        raise ValueError('sketch size exceeds native dimension')
    sketch = sketch or WordSketch(api,seed,sketch_size,sample_size)
    rng = sketch.rng  # Continue the stream: validation must NOT replay probes.
    sketch_size,sample_size = sketch.sketch_size,sketch.sample_size
    compressed = [sketch.compressed[w] for w in WORDS]
    monomials = [(i,j) for i in range(d) for j in range(i,d)]
    rows = ColumnBasis(len(monomials))
    used = 0
    # The query sketch is reused for every equation; no native calls occur in
    # this symbolic loop. Do not stop at nullity one until every minor agrees.
    for a,b in combinations(range(sketch_size),2):
        for x,y in combinations(range(sketch_size),2):
            row = []
            for i,j in monomials:
                value = compressed[i][a][x]*compressed[j][b][y]-compressed[i][a][y]*compressed[j][b][x]
                if i!=j:
                    value += compressed[j][a][x]*compressed[i][b][y]-compressed[j][a][y]*compressed[i][b][x]
                row.append(value)
            rows.add(row)
            used += 1
            if len(rows)==len(monomials):
                return {'status':'NO_RANK_ONE_LAW_IN_LIBRARY','words':WORDS,
                        'minor_coefficient_rank':len(rows),'lifted_dimension':len(monomials),
                        'minors_processed':used,
                        'reason':'full coefficient rank excludes every nonzero Veronese point'}
    kernel = nullspace_of_rows(rows)
    if len(kernel)!=1:
        return {'status':'UNKNOWN','words':WORDS,'minor_coefficient_rank':len(rows),
                'lifted_dimension':len(monomials),'minors_processed':used,
                'kernel_dimension':len(kernel),
                'reason':'linearization does not isolate one projective law; not a nonexistence conclusion'}
    z = kernel[0]
    tensor = [[F(0) for _ in range(d)] for _ in range(d)]
    for (i,j),value in zip(monomials,z):
        tensor[i][j]=tensor[j][i]=value
    pivot = next((i for i in range(d) if tensor[i][i]),None)
    if pivot is None:
        return {'status':'NO_RANK_ONE_LAW_IN_LIBRARY','reason':'unique lifted point has no nonzero square coordinate'}
    theta = [tensor[i][pivot]/tensor[pivot][pivot] for i in range(d)]
    if any(tensor[i][j]!=tensor[pivot][pivot]*theta[i]*theta[j] for i in range(d) for j in range(d)):
        return {'status':'NO_RANK_ONE_LAW_IN_LIBRARY','reason':'unique lifted point is not decomposable'}
    raw = dict(zip(WORDS,theta))
    info = {'words':WORDS,'coefficients':encode(raw),'minor_coefficient_rank':len(rows),
            'lifted_dimension':len(monomials),'minors_processed':used,
            'unique_rank_at_most_one_candidate_in_library':True,
            'uniqueness_scope':'fixed word library; conditional existence validated separately'}
    if not raw['AB'] or any(raw[w] for w in ('A','B','AA','BB')):
        return {'status':'LAW_CANDIDATE_OUTSIDE_EXECUTOR',**info}
    q,c = -raw['BA']/raw['AB'],-raw['']/raw['AB']
    # No sign/parameter candidate was supplied: both q and c came from minors.
    image = ColumnBasis(n)
    for _ in range(3):
        image.add(relation_action(api,q,random_vector(rng,n,sample_size),c))
        if len(image)>1:
            return {'status':'UNKNOWN','reason':'compressed law failed native rank test',**info}
    u = image.matrix()
    rank = len(image)
    if rank:
        i = image.pivots[0]
        e = [F(j==i) for j in range(n)]
        native_row = relation_action(api,q,e,c,True)
        vt = [[x/u[i][0] for x in native_row]]
        v = transpose(vt)
    else:
        v = [[] for _ in range(n)]
    for _ in range(checks):
        z = random_vector(rng,n,sample_size)
        actual = relation_action(api,q,z,c)
        candidate = mv(u,mv(transpose(v),z)) if rank else [F(0)]*n
        if actual!=candidate:
            return {'status':'UNKNOWN','reason':'fresh native all-input identity check failed',**info}
    return {'status':'ACQUIRED','n':n,'sigma':q,'c':c,'rank':rank,'U':u,'V':v,
            'law_discovery':info,'certificate':{'kind':'fresh exact linear identity test',
              'sample_size':sample_size,'fresh_checks':checks,'candidate_bound':1,
              'false_accept_probability_bound':F(1,sample_size**checks),
              'per_new_program_confidence_charge':0}}


def run_discovery_controls():
    from acquired_operator_controls import MatrixFreeSource,exact_relation_reference,new_program_workload
    root = Path(__file__).resolve().parent
    results = []
    for kind,n,seed in [('derivative',32,104),('chebyshev',32,105),('q_derivative',32,106),('fermion',20,107),('generic',17,108)]:
        started = time.perf_counter()
        source = MatrixFreeSource(n,kind=kind,seed=seed,a=F(7,3),b=F(1))
        relation = discover_quadratic_rank_one(source,seed=seed+300)
        after_discovery = source.snapshot()
        result = {'source':kind,'n':n,'status':relation['status'],
                  'after_discovery':after_discovery,
                  'discovery':encode({k:v for k,v in relation.items() if k not in ('U','V')}),
                  'wall_seconds_discovery':time.perf_counter()-started}
        if relation['status']=='ACQUIRED':
            assert exact_relation_reference(source,source,relation)
            calculus = AcquiredCalculus.acquire_modules(source,relation,degree_cap=6)
            path = root/f'acquired_discovered_{kind}_retained.json'
            path.write_text(json.dumps(calculus.dump(),indent=2)+'\n')
            retained = AcquiredCalculus.load(json.loads(path.read_text()))
            before = source.snapshot()
            workload = new_program_workload(retained,source,source,count=3,seed=seed+800)
            assert before==source.snapshot()
            result['after_modules'] = before
            result['new_tasks'] = workload
            result['all_input_native_relation_confirmed'] = True
        results.append(result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('discovery','new_tasks')},indent=2),flush=True)
    (root/'acquired_relation_discovery_results.json').write_text(json.dumps(results,indent=2)+'\n')


def run_acquired_q_procedure():
    """Reuse an already acquired object; do not rerun its training experiment."""
    from acquired_operator_calculus import CompiledCommutator
    from acquired_operator_controls import MatrixFreeSource,native_polynomial,apply_word,apply_normal
    root = Path(__file__).resolve().parent
    data = json.loads((root/'acquired_discovered_q_derivative_retained.json').read_text())
    calculus = AcquiredCalculus.load(data)
    source = MatrixFreeSource(32,kind='q_derivative',seed=106,a=F(7,3),b=1)
    coefficients = [F(3),F(-2),F(5),F(0),F(-7),F(4)]
    procedure = calculus.synthesize_twisted_polynomial_derivation(coefficients)
    assert source.snapshot()['primitive_action_calls']==0
    path = root/'acquired_q_derivation_procedure.json'
    path.write_text(json.dumps(procedure.dump(),indent=2)+'\n')
    frozen = CompiledCommutator.load(json.loads(path.read_text()))
    # All-input validation in an independent reference coordinate system.
    for j in range(source.n):
        e = [F(i==j) for i in range(source.n)]
        actual = [F(0)]*source.n
        for k,c in enumerate(coefficients):
            ab = apply_word(source,'A'+'B'*k,e)
            ba = apply_word(source,'B'*k+'A',e)
            actual = [x+c*(a-frozen.twist**k*b) for x,a,b in zip(actual,ab,ba)]
        normal = apply_normal(source,{(i,0):c for i,c in enumerate(frozen.normal_polynomial)},e)
        correction = mv(frozen.correction_left,mv(transpose(frozen.correction_right),source.scramble.forward(e)))
        predicted = [a+b for a,b in zip(normal,source.scramble.backward(correction))]
        assert actual==predicted
    assert source.snapshot()['primitive_action_calls']==0
    v = [F((j*13)%11-5) for j in range(source.n)]
    output = frozen.execute(source,v)
    compiled_calls = source.snapshot()['primitive_action_calls']
    first = source.apply('A',native_polynomial(source,coefficients,v))
    second = native_polynomial(source,[c*frozen.twist**j for j,c in enumerate(coefficients)],source.apply('A',v))
    direct_calls = source.snapshot()['primitive_action_calls']-compiled_calls
    assert output==[a-b for a,b in zip(first,second)]
    result = {'source':'q-difference operator with q unlabelled during discovery',
              'acquired_q':str(calculus.sigma),'acquired_c':str(calculus.c),
              'new_polynomial':encode(coefficients),
              'generated_normal_coefficients':encode(frozen.normal_polynomial),
              'correction_rank':frozen.rank,'all_input_reference_columns':source.n,
              'synthesis_native_calls':0,'compiled_execution_calls':compiled_calls,
              'direct_execution_calls':direct_calls,'exact_execution_equal':True,
              'relation_acquisition_reused_from_saved_object':True}
    (root/'acquired_q_derivation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


class FiniteOperatorAlgebra:
    """A retained faithful multiplication table when native closure is small.

    This is the conventional finite-algebra alternative. It is deliberately
    given the same observations and retention rights as the defect learner.
    """
    def __init__(self,words,actions,zero_identities,certificate):
        self.words = words
        self.actions = actions
        self.zero_identities = zero_identities
        self.certificate = certificate
        self.dim = len(words)
        if not words or words[0]!='':
            raise ValueError('unit must be the first basis word')

    def word(self,word):
        coefficients = [F(i==0) for i in range(self.dim)]
        for symbol in reversed(word):
            coefficients = mv(self.actions[symbol],coefficients)
        return coefficients

    def multiply(self,p,q):
        result = [F(0)]*self.dim
        for word,c in zip(self.words,p):
            if c:
                part = q
                for symbol in reversed(word):
                    part = mv(self.actions[symbol],part)
                result = [x+c*y for x,y in zip(result,part)]
        return result

    def circuit(self,nodes):
        values = []
        for node in nodes:
            op = node['op']
            if op in ('A','B'):
                value = self.word(op)
            elif op=='scalar':
                value = [F(node['value'])*F(i==0) for i in range(self.dim)]
            elif op=='scale':
                value = [F(node['value'])*x for x in values[node['arg']]]
            elif op=='add':
                value = [x+y for x,y in zip(values[node['left']],values[node['right']])]
            elif op=='mul':
                value = self.multiply(values[node['left']],values[node['right']])
            else:
                raise ValueError(op)
            values.append(value)
        return values[-1]

    def dump(self):
        return encode({'kind':'acquired faithful finite operator algebra',
                       'basis_words':self.words,'generator_left_actions':self.actions,
                       'complete_zero_identity_space_in_quadratic_library':self.zero_identities,
                       'certificate':self.certificate,
                       'scope':'all finite polynomial circuits in the same native primitives'})

    @classmethod
    def load(cls,data):
        return cls(data['basis_words'],
                   {s:[[F(x) for x in row] for row in matrix] for s,matrix in data['generator_left_actions'].items()},
                   data['complete_zero_identity_space_in_quadratic_library'],data['certificate'])


def acquire_small_algebra(api,*,dimension_budget=4,seed=0,sketch_size=8,sample_size=257,checks=4,sketch=None):
    """Learn native word-span closure and check ALL closure relations jointly."""
    n,d = api.n,len(WORDS)
    sketch = sketch or WordSketch(api,seed,sketch_size,sample_size)
    rng = sketch.rng
    sketch_size,sample_size = sketch.sketch_size,sketch.sample_size
    compressed = sketch.compressed
    basis = ColumnBasis(sketch_size**2)
    basis_words = []
    for w in WORDS:
        flat = [x for row in compressed[w] for x in row]
        added,_ = basis.add(flat)
        if added:
            basis_words.append(w)
            if len(basis)>dimension_budget:
                return {'status':'UNKNOWN','reason':'observed native algebra dimension exceeds budget',
                        'observed_independent_words':basis_words}
    needed = sorted(set(WORDS)|{s+w for s in ('A','B') for w in basis_words},key=len)
    sketch.ensure(needed)
    representations = {}
    for w in needed:
        try:
            representations[w] = basis.coordinates([x for row in compressed[w] for x in row])
        except ValueError:
            return {'status':'UNKNOWN','reason':'native left-generator closure exceeds acquired word span',
                    'outside_word':w,'basis_words':basis_words}
    # These fresh tests jointly certify all fitted generator multiplication
    # relations. A single incorrect stacked linear residual passes with <=1/q
    # per new vector, regardless of the number of relations in the stack.
    for _ in range(checks):
        z = random_vector(rng,n,sample_size)
        native = word_responses(api,needed,z)
        for s in ('A','B'):
            for w in basis_words:
                coefficients = representations[s+w]
                expected = [sum((c*native[b][i] for c,b in zip(coefficients,basis_words)),F(0)) for i in range(n)]
                if native[s+w]!=expected:
                    return {'status':'UNKNOWN','reason':'fresh native closure certificate failed'}
    linear_constraints = ColumnBasis(d)
    for a in range(sketch_size):
        for b in range(sketch_size):
            linear_constraints.add([compressed[w][a][b] for w in WORDS])
    zero_space = [dict(zip(WORDS,v)) for v in nullspace_of_rows(linear_constraints)]
    actions = {s:transpose([representations[s+w] for w in basis_words]) for s in ('A','B')}
    return FiniteOperatorAlgebra(basis_words,actions,zero_space,
        {'false_accept_probability_bound':F(1,sample_size**checks),
         'sample_size':sample_size,'fresh_stacked_checks':checks,
         'observed_basis_independence':'deterministic from the exact compressed responses',
         'per_new_program_confidence_charge':0})


def run_nonunique_repair():
    from acquired_operator_controls import MatrixFreeSource,random_dag,apply_circuit,apply_word
    root = Path(__file__).resolve().parent
    source = MatrixFreeSource(20,kind='fermion',seed=107,a=F(7,3),b=1)
    got = acquire_small_algebra(source,dimension_budget=4,seed=707)
    assert isinstance(got,FiniteOperatorAlgebra)
    after = source.snapshot()
    path = root/'acquired_finite_algebra_retained.json'
    path.write_text(json.dumps(got.dump(),indent=2)+'\n')
    retained = FiniteOperatorAlgebra.load(json.loads(path.read_text()))
    rng = random.Random(908)
    checks = 0
    for _ in range(10):
        nodes = random_dag(rng,10)
        value = retained.circuit(nodes)
        for j in range(source.n):
            e = [F(i==j) for i in range(source.n)]
            actual = apply_circuit(source,nodes,e)
            predicted = [F(0)]*source.n
            for w,c in zip(retained.words,value):
                response = apply_word(source,w,e)
                predicted = [x+c*y for x,y in zip(predicted,response)]
            assert actual==predicted
        checks += 1
    assert source.snapshot()==after
    # Complete native equality: the previously unrecognized A^2=0 is now
    # acquired, and four independent basis operators make the evaluator faithful.
    assert not any(retained.word('AA')) and not any(retained.word('BB'))
    hard = MatrixFreeSource(20,kind='derivative',seed=110,a=1)
    failed = acquire_small_algebra(hard,dimension_budget=4,seed=708)
    assert isinstance(failed,dict) and failed['status']=='UNKNOWN'
    result = {'previous_failure':'rank-one-law uniqueness gate was inconclusive',
              'replacement':'acquired complete finite algebra',
              'dimension':retained.dim,'basis_words':retained.words,
              'zero_identity_space_dimension':len(retained.zero_identities),
              'acquisition_cost':after,'reuse_native_calls':0,
              'new_DAGs_all_input_checked':checks,'all_input_columns':checks*source.n,
              'now_certifies_A_squared_zero':True,
              'certificate':encode(retained.certificate),
              'derivative_control':failed,'derivative_control_cost':hard.snapshot(),
              'dense_tomography_primitive_calls':2*source.n}
    (root/'acquired_finite_algebra_results.json').write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps(encode(result),indent=2))


def acquire_reusable_reasoner(api,*,seed=0,degree_cap=6,algebra_budget=4):
    """Choose a learned representation using one retained observation record.

    The small-algebra path has arbitrary circuit-degree scope. The defect path
    has bounded-degree correction scope. Returning neither is permitted.
    This wrapper does not choose its route using a source-family label.
    """
    sketch = WordSketch(api,seed=seed)
    small = acquire_small_algebra(api,dimension_budget=algebra_budget,sketch=sketch)
    if isinstance(small,FiniteOperatorAlgebra):
        return {'status':'ACQUIRED','representation':'finite_algebra','object':small,
                'shared_sketch':sketch,'earlier_attempts':[],
                'overall_false_accept_bound':F(1,257**4)}
    law = discover_quadratic_rank_one(api,sketch=sketch)
    if law['status']=='ACQUIRED':
        calculus = AcquiredCalculus.acquire_modules(api,law,degree_cap)
        return {'status':'ACQUIRED','representation':'defect_calculus','object':calculus,
                'shared_sketch':sketch,'earlier_attempts':[small],
                'overall_false_accept_bound':F(2,257**4)}
    return {'status':'UNKNOWN','representation':None,'object':None,
            'shared_sketch':sketch,'earlier_attempts':[small,law],
            'overall_false_accept_bound':F(2,257**4)}


def run_shared_probe_learner():
    from acquired_operator_controls import MatrixFreeSource,new_program_workload,random_dag,apply_word,apply_circuit
    root = Path(__file__).resolve().parent
    outcomes = []
    for kind,n,seed in [('q_derivative',32,202),('fermion',20,203),('generic',17,204)]:
        source = MatrixFreeSource(n,kind=kind,seed=seed,a=F(7,3),b=1)
        got = acquire_reusable_reasoner(source,seed=seed+600)
        cost = source.snapshot()
        output = {'source':kind,'status':got['status'],'chosen_representation':got['representation'],
                  'paid_native_cost':cost,'earlier_attempts':encode(got['earlier_attempts']),
                  'overall_false_accept_bound':str(got['overall_false_accept_bound']),
                  'quadratic_native_probes_shared_not_repeated':True}
        if got['object'] is not None:
            path = root/f'acquired_reusable_{kind}.json'
            path.write_text(json.dumps(got['object'].dump(),indent=2)+'\n')
            if got['representation']=='defect_calculus':
                retained = AcquiredCalculus.load(json.loads(path.read_text()))
                workload = new_program_workload(retained,source,source,count=3,seed=308)
                output['new_programs_all_input_checked'] = workload['programs_checked']
                output['acquired_q'] = str(retained.sigma)
            else:
                retained = FiniteOperatorAlgebra.load(json.loads(path.read_text()))
                rng = random.Random(309)
                for _ in range(5):
                    nodes = random_dag(rng,12)
                    coefficients = retained.circuit(nodes)
                    for j in range(n):
                        e = [F(i==j) for i in range(n)]
                        truth = apply_circuit(source,nodes,e)
                        predicted = [F(0)]*n
                        for w,c in zip(retained.words,coefficients):
                            predicted = [x+c*y for x,y in zip(predicted,apply_word(source,w,e))]
                        assert truth==predicted
                output['new_programs_all_input_checked'] = 5
            assert source.snapshot()==cost
            output['new_program_native_calls'] = 0
        # Preserve one actual shared acquisition record, not just its score.
        if kind=='q_derivative':
            (root/'acquired_shared_operator_probes.json').write_text(json.dumps(got['shared_sketch'].dump(),indent=2)+'\n')
        outcomes.append(output)
        print(json.dumps(output,indent=2),flush=True)
    (root/'acquired_reusable_learner_results.json').write_text(json.dumps(outcomes,indent=2)+'\n')


if __name__=='__main__':
    run_discovery_controls()
    run_acquired_q_procedure()
    run_nonunique_repair()
    run_shared_probe_learner()
