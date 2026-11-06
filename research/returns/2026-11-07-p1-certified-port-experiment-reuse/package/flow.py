"""Exact polynomial trajectory checker, adapted with credit from the retained
port_reuse/verified_flow.py. Parallel positive-residue memory replaces its
series recurrence. All numerical paths remain untrusted proposals.
"""
from fractions import Fraction as Q
from exact import require,dyadic as round_dyadic,sqrt_up as sqrt_upper,spectral_bound,encode

def padd(a,b):
    c=[Q(0)]*max(len(a),len(b))
    for i,x in enumerate(a):c[i]+=x
    for i,x in enumerate(b):c[i]+=x
    while len(c)>1 and c[-1]==0:c.pop()
    return c


def pscale(a,b):
    return [x*b for x in a]


def pmul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    while len(c)>1 and c[-1]==0:c.pop()
    return c


def load_from_spec(spec,r):
    """Manifest syntax proves monotonicity by construction.

    phi(y) = sum weight*v*(v.y) + sum weight*v*(v.y)^3,
    with nonnegative rational weights. Both are gradients of convex
    nonnegative quadratic/quartic polynomials and vanish at zero.
    """
    terms=[]
    for row in spec:
        degree=row['degree'];weight=Q(row['weight']);v=list(map(Q,row['direction']))
        require(degree in (1,3) and weight>=0 and len(v)==r)
        terms.append((degree,weight,v))
    return terms


def sparse(matrix):
    return [[(j,x) for j,x in enumerate(row) if x] for row in matrix]


def build(components,attachment):
    """Only acquired models enter this source-independent composition."""
    r=sum(model['r'] for model in components);q=attachment.get('dimension',0)
    require(isinstance(q,int) and q>=0)
    R=r+q;dimension=R+sum(model['r']*len(model['poles']) for model in components)
    damping=list(map(Q,attachment.get('damping',[])))
    require(len(damping)==q and all(v>0 for v in damping))
    J=[list(map(Q,row)) for row in attachment.get('skew',[[0]*R for _ in range(R)])]
    require(len(J)==R and all(len(row)==R for row in J))
    require(all(J[i][j]==-J[j][i] for i in range(R) for j in range(R)))
    matrix=[[Q(0)]*dimension for _ in range(dimension)]
    groups=[list(range(R))];weights=[];offset=0;state=R
    for model in components:
        rr=model['r'];A=[list(map(Q,row)) for row in model['A']]
        for i in range(rr):
            for j in range(rr):matrix[offset+i][offset+j]-=A[i][j]
        for pole0,residue in zip(model['poles'],model['residues']):
            pole=Q(pole0);residue=[list(map(Q,row)) for row in residue]
            for i in range(rr):
                matrix[state+i][state+i]=-pole
                matrix[state+i][offset+i]=1
                for j in range(rr):matrix[offset+i][state+j]=residue[i][j]
            groups.append(list(range(state,state+rr)))
            weights.append(spectral_bound(residue)/pole)
            state+=rr
        offset+=rr
    require(state==dimension)
    for i,v in enumerate(damping):matrix[r+i][r+i]-=v
    for i in range(R):
        for j in range(R):matrix[i][j]-=J[i][j]
    alpha=min([Q(model['a']) for model in components]+damping)
    error=max(Q(model['certificate']['operator_error']) for model in components)
    return matrix,R,alpha,error,groups,weights


def certify(components,attachment,path,initial_bounds):
    matrix,R,alpha,error,groups,weights=build(components,attachment)
    cert=residual_certificate(matrix,path,R,groups)
    norms=[sqrt_upper(Q(v)) for v in cert['squared_residual_bounds']]
    numerical=norms[0]+sum((w*n for w,n in zip(weights,norms[1:])),Q(0))
    observed_norm=sqrt_upper(Q(cert['observed_L2_squared_bound']))
    Delta=numerical+error*observed_norm
    rho=sqrt_upper(sum((Q(v)**2 for v in initial_bounds),Q(0)),64)
    cert.update(encode({'effective_numerical_residual_L2':numerical,
        'source_uncertainty_contribution_L2':error*observed_norm,
        'combined_residual_L2':Delta,'coercivity':alpha,
        'initial_state_radius':rho,'operator_error':error,
        'uniform_observed_error_radius':Delta*sqrt_upper(1/(2*alpha))+rho,
        'observed_L2_error_radius':Delta/alpha+rho*sqrt_upper(1/(2*alpha)),
        'additional_source_calls':0,'model_dimension':len(matrix),
        'future_attachment_dimension':attachment.get('dimension',0),
        'observed_dimension':R,'components':len(components)}))
    return cert


def field(L,load,r,x,u):
    out=[sum((value*x[j] for j,value in row),Q(0)) for row in L]
    for degree,weight,v in load:
        s=sum((v[j]*x[j] for j in range(r)),Q(0))
        value=weight*s**degree
        for i in range(r):out[i]-=v[i]*value
    for i in range(r):out[i]+=u[i]
    return out


def float_field(L,load,r,x,u):
    out=[sum(value*x[j] for j,value in row) for row in L]
    for degree,weight,v in load:
        value=weight*sum(v[j]*x[j] for j in range(r))**degree
        for i in range(r):out[i]-=v[i]*value
    for i in range(r):out[i]+=u[i]
    return out


def propose_path(matrix,load_spec,r,segments,steps_per_unit=64,node_bits=44):
    """Untrusted finite numerical proposal; every interval is checked later."""
    d=len(matrix);L=sparse(matrix);Lf=[[(j,float(x)) for j,x in row] for row in L]
    load=load_from_spec(load_spec,r)
    lf=[(degree,float(weight),list(map(float,v))) for degree,weight,v in load]
    x=[0.0]*d;time=Q(0);pieces=[];evaluations=0
    for row in segments:
        length=Q(row['duration']);u=list(map(Q,row['input']))
        require(length>0 and len(u)==r)
        raw=length*steps_per_unit
        steps=max(1,-(-raw.numerator//raw.denominator));h=length/steps;hf=float(h)
        uf=list(map(float,u));nodes=[]
        start=[round_dyadic(Q.from_float(v),node_bits) for v in x]
        nodes.append([str(v) for v in start])
        for _ in range(steps):
            f1=float_field(Lf,lf,r,x,uf)
            f2=float_field(Lf,lf,r,[v+hf*w/2 for v,w in zip(x,f1)],uf)
            f3=float_field(Lf,lf,r,[v+hf*w/2 for v,w in zip(x,f2)],uf)
            f4=float_field(Lf,lf,r,[v+hf*w for v,w in zip(x,f3)],uf)
            x=[v+hf*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(x,f1,f2,f3,f4)]
            evaluations+=4
            nodes.append([str(round_dyadic(Q.from_float(v),node_bits)) for v in x])
        pieces.append({'start_time':str(time),'step':str(h),'input':[str(v) for v in u],
                       'nodes':nodes})
        time+=length
    return {'dimension':d,'observed':r,'load':load_spec,'pieces':pieces,
            'horizon':str(time),'node_bits':node_bits,
            'proposal_field_evaluations':evaluations}


def residual_certificate(matrix,path,r,groups):
    """Exact L2 upper bounds by polynomial coefficient absolute sums.

    Each group is a list of residual coordinates. Returns the rational
    integral bound for its squared Euclidean residual norm. A cubic
    Hermite segment is continuous, with derivatives from the actual
    rational vector field. Forcing switches are exact segment boundaries.
    """
    d=len(matrix);require(path['dimension']==d and path['observed']==r)
    L=sparse(matrix);load=load_from_spec(path['load'],r)
    squared=[Q(0) for _ in groups];port_norm2=Q(0);elapsed=Q(0)
    previous=[Q(0)]*d;intervals=0;max_bits=0
    for part in path['pieces']:
        require(Q(part['start_time'])==elapsed)
        h=Q(part['step']);require(h>0)
        u=list(map(Q,part['input']));nodes=[list(map(Q,row)) for row in part['nodes']]
        require(nodes and nodes[0]==previous and all(len(row)==d for row in nodes))
        for left,right in zip(nodes,nodes[1:]):
            f0=field(L,load,r,left,u);f1=field(L,load,r,right,u)
            polys=[]
            for x,y,a,b in zip(left,right,f0,f1):
                polys.append([x,h*a,3*(y-x)-h*(2*a+b),-2*(y-x)+h*(a+b)])
            rhs=[]
            for row in L:
                poly=[Q(0)]
                for j,value in row:poly=padd(poly,pscale(polys[j],value))
                rhs.append(poly)
            for degree,weight,v in load:
                dot=[Q(0)]
                for j in range(r):dot=padd(dot,pscale(polys[j],v[j]))
                term=dot if degree==1 else pmul(pmul(dot,dot),dot)
                for i in range(r):rhs[i]=padd(rhs[i],pscale(term,-weight*v[i]))
            for i in range(r):rhs[i]=padd(rhs[i],[u[i]])
            bounds=[]
            for poly,F in zip(polys,rhs):
                derivative=[Q(i)*poly[i]/h for i in range(1,len(poly))]
                residual=padd(derivative,pscale(F,Q(-1)))
                bound=sum(map(abs,residual),Q(0));bounds.append(bound)
                max_bits=max(max_bits,*(max(abs(x.numerator).bit_length(),x.denominator.bit_length())
                                        for x in residual))
            for index,group in enumerate(groups):
                squared[index]+=h*sum((bounds[i]**2 for i in group),Q(0))
            port_norm2+=h*sum((sum(map(abs,polys[i]),Q(0))**2 for i in range(r)),Q(0))
            intervals+=1
        elapsed+=h*(len(nodes)-1);previous=nodes[-1]
    require(elapsed==Q(path['horizon']))
    return {'squared_residual_bounds':[str(x) for x in squared],
            'observed_L2_squared_bound':str(port_norm2),'intervals':intervals,
            'max_residual_coefficient_bits':max_bits,
            'terminal_observed':[str(x) for x in previous[:r]]}


