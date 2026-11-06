"""Exact optimal experiments for a monotone constitutive-law family.

Unknown g has global secants in [m,L], m>0, and finite interval data.
The task is the equilibrium g^{-1}(forcing). A query returns a dyadic
force report with physical error delta and rounding error <=2^{-p}/2.
Every history is checked against one stationary law. All arithmetic is
rational. The finite experiment catalogue and all branches are charged.

The envelope formulas are the retained N1039 optimal-recovery mechanism.
The game recursion is ordinary finite-horizon minimax dynamic programming.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product


def require(condition, message='Invalid input or certificate'):
    if not condition:
        raise ValueError(message)


def floor(x):
    x=Q(x)
    return x.numerator//x.denominator


def ceil(x):
    return -floor(-Q(x))


def normalize(samples):
    rows={}
    for x,lo,hi in samples:
        x,lo,hi=Q(x),Q(lo),Q(hi)
        if x in rows:
            lo=max(lo,rows[x][0]);hi=min(hi,rows[x][1])
        if lo>hi:
            return None
        rows[x]=(lo,hi)
    return tuple((x,*rows[x]) for x in sorted(rows))


def envelope(m,L,samples,x,endpoint):
    x=Q(x);D=L-m
    if endpoint=='lower':
        return m*x+max(lo-m*z-D*max(z-x,Q(0)) for z,lo,_ in samples)
    require(endpoint=='upper')
    return m*x+min(hi-m*z+D*max(x-z,Q(0)) for z,_,hi in samples)


def feasible(m,L,samples):
    return samples is not None and bool(samples) and all(
        envelope(m,L,samples,x,'lower')<=hi for x,_,hi in samples)


def root_range(m,L,samples,forcing):
    """Exact attained range of g^{-1}(forcing) over the whole family."""
    u=Q(forcing)
    lower=max(x+(u-hi)/(m if u<=hi else L) for x,_,hi in samples)
    upper=min(x+(u-lo)/(L if u<=lo else m) for x,lo,_ in samples)
    require(lower<=upper,'Inconsistent root interval')
    return lower,upper


def potential(m,L,samples,x,endpoint):
    """Exact integral of an extremal piecewise-affine law from 0 to x.

    Includes all cone breakpoints and all possible line intersections;
    trapezoidal integration on this refinement is exact.
    """
    x=Q(x);a,b=sorted((Q(0),x))
    breaks={a,b}; lines=[]
    for z,lo,hi in samples:
        value=lo if endpoint=='lower' else hi
        breaks.add(z)
        lines.extend([(m,value-m*z),(L,value-L*z)])
    for i,(s,c) in enumerate(lines):
        for t,d in lines[:i]:
            if s!=t:
                breaks.add((d-c)/(s-t))
    cuts=sorted(t for t in breaks if a<=t<=b)
    total=sum(((right-left)*(envelope(m,L,samples,left,endpoint)+
                              envelope(m,L,samples,right,endpoint))/2
               for left,right in zip(cuts,cuts[1:])),Q(0))
    return total if x>=0 else -total


class ExperimentGame:
    def __init__(self,spec):
        self.spec=spec
        self.m,self.L=map(Q,spec['slopes'])
        self.delta=Q(spec['physical_error'])
        self.forcing=Q(spec['forcing'])
        self.budget=spec['budget']
        require(0<self.m<=self.L and self.delta>=0)
        require(isinstance(self.budget,int) and self.budget>=0)
        self.initial=normalize(spec['prior_data'])
        require(feasible(self.m,self.L,self.initial),'Inconsistent prior data')
        self.actions=[]
        for row in spec['experiments']:
            x=Q(row['x']);p=row['precision_bits'];cost=row.get('cost',1)
            require(isinstance(p,int) and p>=0 and isinstance(cost,int) and cost>=1)
            self.actions.append((x,p,cost))
        self.nodes=[];self.cache={}
        self.edge_count=0

    def responses(self,samples,action):
        x,p,_=self.actions[action];q=Q(1,1<<p);eta=self.delta+q/2
        lo=envelope(self.m,self.L,samples,x,'lower')
        hi=envelope(self.m,self.L,samples,x,'upper')
        answers=[]
        for j in range(ceil((lo-eta)/q),floor((hi+eta)/q)+1):
            y=j*q
            child=normalize(samples+((x,y-eta,y+eta),))
            if feasible(self.m,self.L,child):
                answers.append((y,child))
        require(bool(answers),'A valid source must permit at least one report')
        return answers

    def solve_node(self,samples,budget):
        key=(samples,budget)
        if key in self.cache:
            return self.cache[key]
        idx=len(self.nodes);self.cache[key]=idx;self.nodes.append(None)
        lower,upper=root_range(self.m,self.L,samples,self.forcing)
        stop=(upper-lower)/2;best=stop;chosen=None;branches=[]
        for a,(_,_,cost) in enumerate(self.actions):
            if cost>budget:
                continue
            children=[]
            for y,child in self.responses(samples,a):
                k=self.solve_node(child,budget-cost)
                children.append({'report':str(y),'child':k})
                self.edge_count+=1
            worst=max(Q(self.nodes[v['child']]['value']) for v in children)
            branches.append({'action':a,'worst_value':str(worst),'children':children})
            if worst<best:
                best=worst;chosen=a
        self.nodes[idx]={'budget':budget,'data':[[str(t) for t in row] for row in samples],
                         'root_interval':[str(lower),str(upper)],'stop_value':str(stop),
                         'value':str(best),'chosen_action':chosen,'actions':branches}
        return idx

    def solve(self):
        root=self.solve_node(self.initial,self.budget)
        node_id=root;trace=[]
        while self.nodes[node_id]['chosen_action'] is not None:
            node=self.nodes[node_id]
            branch=next(a for a in node['actions'] if a['action']==node['chosen_action'])
            edge=max(branch['children'],key=lambda e:Q(self.nodes[e['child']]['value']))
            trace.append({'node':node_id,'action':branch['action'],**edge})
            node_id=edge['child']
        leaf=self.nodes[node_id]
        lo,hi=map(Q,leaf['root_interval'])
        return {'input':self.spec,'root':root,'value':self.nodes[root]['value'],
                'nodes':self.nodes,'counts':{'unique_states':len(self.nodes),
                                          'stored_response_edges':self.edge_count},
                'worst_case_witness':{
                    'trace':trace,'leaf':node_id,'shared_data':leaf['data'],
                    'lower_root_source':'upper envelope','upper_root_source':'lower envelope',
                    'root_values':[str(lo),str(hi)],'separation':str(hi-lo)}}

    def fixed_schedule_value(self,schedule):
        """Worst radius of a fixed, nonadaptive sequence of catalogue actions."""
        require(sum(self.actions[a][2] for a in schedule)<=self.budget)
        @lru_cache(None)
        def recur(samples,j):
            if j==len(schedule):
                lo,hi=root_range(self.m,self.L,samples,self.forcing)
                return (hi-lo)/2
            return max(recur(child,j+1) for _,child in self.responses(samples,schedule[j]))
        return recur(self.initial,0)

    def best_fixed_schedule(self):
        best=(root_range(self.m,self.L,self.initial,self.forcing)[1]-
              root_range(self.m,self.L,self.initial,self.forcing)[0])/2
        selected=()
        mincost=min((a[2] for a in self.actions),default=self.budget+1)
        for n in range(1,self.budget//mincost+1):
            for schedule in product(range(len(self.actions)),repeat=n):
                if sum(self.actions[a][2] for a in schedule)>self.budget:
                    continue
                value=self.fixed_schedule_value(schedule)
                if value<best:
                    best=value;selected=schedule
        return {'value':str(best),'schedule':list(selected)}


def verify_game(spec,certificate):
    """Verify every allowed action and response, including alternatives.

    This checks a minimax optimality certificate, not only one policy's
    performance. Exact rational feasibility and inverse-envelope formulas
    are the small mathematical kernel. No assertion is disabled by -O.
    """
    require(certificate['input']==spec,'Certificate input mismatch')
    game=ExperimentGame(spec);nodes=certificate['nodes'];seen=set()
    def check(idx,samples,budget):
        require(isinstance(idx,int) and 0<=idx<len(nodes),'Invalid child reference')
        node=nodes[idx]
        require(node['budget']==budget)
        require(node['data']==[[str(t) for t in row] for row in samples])
        if idx in seen:
            return Q(node['value'])
        lo,hi=root_range(game.m,game.L,samples,game.forcing)
        stop=(hi-lo)/2
        require(node['root_interval']==[str(lo),str(hi)])
        require(Q(node['stop_value'])==stop)
        expected=[a for a,v in enumerate(game.actions) if v[2]<=budget]
        require([a['action'] for a in node['actions']]==expected,'Missing experiment alternative')
        values={}
        for branch in node['actions']:
            a=branch['action'];responses=game.responses(samples,a)
            require([e['report'] for e in branch['children']]==[str(y) for y,_ in responses],
                    'Missing or altered feasible response')
            childvalues=[check(edge['child'],child,budget-game.actions[a][2])
                         for edge,(_,child) in zip(branch['children'],responses)]
            values[a]=max(childvalues)
            require(Q(branch['worst_value'])==values[a])
        value=min([stop]+list(values.values()))
        require(Q(node['value'])==value,'Incorrect minimax value')
        chosen=node['chosen_action']
        require((chosen is None and value==stop) or (chosen in values and values[chosen]==value),
                'Chosen action is not optimal')
        seen.add(idx)
        return value
    value=check(certificate['root'],game.initial,game.budget)
    require(Q(certificate['value'])==value)
    witness=certificate['worst_case_witness'];current=certificate['root']
    for edge in witness['trace']:
        require(edge['node']==current)
        node=nodes[current];require(edge['action']==node['chosen_action'])
        branch=next(a for a in node['actions'] if a['action']==edge['action'])
        require({'report':edge['report'],'child':edge['child']} in branch['children'])
        require(Q(nodes[edge['child']]['value'])==Q(node['value']))
        current=edge['child']
    require(current==witness['leaf'] and nodes[current]['chosen_action'] is None)
    require(witness['shared_data']==nodes[current]['data'])
    require(witness['root_values']==nodes[current]['root_interval'])
    require(Q(witness['separation'])==2*value)
    return {'verified_nodes':len(seen),'value':str(value),'all_experiment_alternatives_checked':True}
