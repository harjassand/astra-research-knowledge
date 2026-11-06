"""Certified acquisition of a reusable port memory model.

Unknown H has symmetric part >=a I and norm <=b. The symmetric special
case has a faster certified expansion. Known coordinate ports are fixed
before acquisition. The learner receives quantized full-vector
actions on unit-norm rational inputs. It does not receive H's entries.
All native reports, internal rounding and arithmetic are charged.

The construction uses a normalized Neumann/exponential expansion, not
unverified moment fitting. Theory and full costs are in RESULT.txt.
"""
from fractions import Fraction as Q
from math import isqrt


def require(ok,message='Invalid input or certificate'):
    if not ok:
        raise ValueError(message)


def round_dyadic(x,p):
    """Nearest dyadic; deterministic upward choice at an exact tie."""
    x=Q(x)*(1<<p)
    return Q((2*x.numerator+x.denominator)//(2*x.denominator),1<<p)


def sqrt_upper(x,p=48):
    x=Q(x);require(x>=0)
    scaled=(x.numerator<<(2*p))//x.denominator
    j=isqrt(scaled)
    y=Q(j,1<<p)
    if y*y<x:
        y=Q(j+1,1<<p)
    require(y*y>=x)
    return y


def sym(matrix):
    return [[(matrix[i][j]+matrix[j][i])/2 for j in range(len(matrix))]
            for i in range(len(matrix))]


def row_norm(matrix):
    rows=max((sum(map(abs,row),Q(0)) for row in matrix),default=Q(0))
    columns=max((sum((abs(row[j]) for row in matrix),Q(0))
                 for j in range(len(matrix[0]) if matrix else 0)),default=Q(0))
    return max(rows,columns)  # >=sqrt(||M||_1 ||M||_infinity)>=||M||_2


def encode_matrix(matrix):
    return [[str(x) for x in row] for row in matrix]


def decode_matrix(matrix):
    return [[Q(x) for x in row] for row in matrix]


def plan(n,ports,a,b,tolerance,structure='symmetric'):
    a,b,tolerance=map(Q,(a,b,tolerance))
    require(isinstance(n,int) and n>0 and 0<a<=b and tolerance>0)
    require(bool(ports) and len(set(ports))==len(ports))
    require(all(isinstance(i,int) and 0<=i<n for i in ports))
    require(structure in ('symmetric','accretive'))
    r=len(ports)
    if structure=='symmetric':c=(a+b)/2;rho=(b-a)/(b+a)
    else:c=b*b/a;rho=1-a*a/(2*b*b)
    target=min(tolerance,a/4)
    if a==b:
        return {'n':n,'ports':list(ports),'a':str(a),'b':str(b),'c':str(c),
                'rho':'0','target':str(target),'k':0,'precision_bits':0,
                'action_error':'0','state_error_bound':'0','moment_error_bound':'0',
                'tail_error':'0','data_error':'0','operator_error':'0','native_calls':0}
    hidden=n-r
    tail=b*b/(c*(1-rho)) if hidden else Q(0);k=0
    while tail>target/2:
        tail*=rho;k+=1
    Cw=(1+1/b)+(1+2/c)/(1-rho)
    Cdata=r+Q(k*r)*b/c*(b*Cw+2)
    allowed=min(1/(2*Cw),target/(2*Cdata))
    p=0
    while Q(n,1<<(p+1))>allowed:
        p+=1
    eta=Q(n,1<<(p+1));ew=eta*Cw
    em=r*b*eta*(b*Cw+2)
    data=r*eta+Q(k)*em/c
    require(ew<=Q(1,2) and tail+data<=target)
    result={'n':n,'ports':list(ports),'a':str(a),'b':str(b),'c':str(c),
            'rho':str(rho),'target':str(target),'k':k,'precision_bits':p,
            'action_error':str(eta),'state_error_bound':str(ew),
            'moment_error_bound':str(em),'tail_error':str(tail),
            'data_error':str(data),'operator_error':str(tail+data),
            'native_calls':r*(k+1)}
    if structure!='symmetric':result['structure']=structure
    return result


def acquire(action,n,ports,a,b,tolerance,structure='symmetric'):
    """action(q,p) -> n rational reports. No source matrix is passed."""
    contract=plan(n,ports,a,b,tolerance,structure)
    a,b,c=Q(a),Q(b),Q(contract['c']);r=len(ports)
    hidden=[i for i in range(n) if i not in ports]
    p=contract['precision_bits'];history=[]
    if a==b:
        A=[[a if i==j else Q(0) for j in range(r)] for i in range(r)]
        return {'contract':contract,'A':encode_matrix(A),'moments':[],
                'history':[],'state_dimension':r,'coefficient_count':r*r}
    def call(q):
        require(len(q)==n and sum((x*x for x in q),Q(0))<=1,'Query exceeds unit norm')
        response=list(map(Q,action(q,p)))
        require(len(response)==n)
        require(all((x*(1<<p)).denominator==1 for x in response),'Non-dyadic report')
        history.append({'query':[str(x) for x in q],
                        'report':[str(x) for x in response]})
        return response
    columns=[];states=[]
    for i in ports:
        q=[Q(0)]*n;q[i]=Q(1);y=call(q)
        columns.append([y[j] for j in ports])
        states.append([round_dyadic(y[j]/b,p) for j in hidden])
    A=[[columns[j][i] for j in range(r)] for i in range(r)]
    if structure=='symmetric':A=sym(A)
    moments=[]
    for _ in range(contract['k']):
        mcols=[];following=[]
        for state in states:
            q=[Q(0)]*n
            for j,value in zip(hidden,state):q[j]=value/2
            y=call(q)
            mcols.append([2*b*y[j] for j in ports])
            following.append([round_dyadic(value-2*y[j]/c,p)
                              for j,value in zip(hidden,state)])
        M=[[mcols[j][i] for j in range(r)] for i in range(r)]
        moments.append(sym(M) if structure=='symmetric' else M)
        states=following
    require(len(history)==contract['native_calls'])
    return {'contract':contract,'A':encode_matrix(A),
            'moments':[encode_matrix(M) for M in moments],
            'history':history,'state_dimension':r*(contract['k']+1),
            'coefficient_count':r*r*(contract['k']+1)}


def replay_acquisition(record):
    """Replay the learner from its complete response history.

    This checks the query generation, norm constraints and returned
    representation. Native-action error validity is an explicit instrument
    premise, checked separately for the concrete software source.
    """
    contract=record['contract'];history=record['history'];cursor=0
    def action(q,p):
        nonlocal cursor
        require(cursor<len(history),'Missing report')
        row=history[cursor];cursor+=1
        require([str(x) for x in q]==row['query'],'Changed acquisition query')
        require(p==contract['precision_bits'])
        return row['report']
    rebuilt=acquire(action,contract['n'],contract['ports'],contract['a'],
                    contract['b'],contract['target'],contract.get('structure','symmetric'))
    require(cursor==len(history) and rebuilt==record,'Acquisition replay mismatch')
    return {'native_calls':cursor,'returned_scalars':cursor*contract['n'],
            'operator_error':contract['operator_error'],
            'state_dimension':record['state_dimension']}


def compact(record):
    """Online representation; the separately charged audit log is retained."""
    return {key:record[key] for key in ['contract','A','moments','state_dimension','coefficient_count']}


def reduced_matrix(model):
    A=decode_matrix(model['A']);Ms=[decode_matrix(M) for M in model['moments']]
    r=len(A);k=len(Ms);c=Q(model['contract']['c']);d=r*(k+1)
    # Linear part in x' = L x - port phi(y) + port u.
    L=[[Q(0) for _ in range(d)] for _ in range(d)]
    for i in range(r):
        for j in range(r):L[i][j]=-A[i][j]
    for ell,M in enumerate(Ms):
        for i in range(r):
            for j in range(r):L[i][r*(ell+1)+j]=M[i][j]
        for i in range(r):
            index=r*(ell+1)+i;L[index][index]=-c
            L[index][r*ell+i]=Q(1) if ell==0 else c
    return L
