"""Rational residual certificates for later nonlinear port interventions.

Floating RK4 only proposes nodes. A rational cubic Hermite path is built
from rounded nodes and exact vector-field slopes. Its polynomial residual
is bounded with exact arithmetic. The model error and residual are then
converted to a guarantee for the actual compatible source by the energy
inequality in RESULT.txt. No new native source observations are needed.
"""
from fractions import Fraction as Q
from memory import require,round_dyadic,sqrt_upper,row_norm,decode_matrix,reduced_matrix


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


def attachment_data(model,attachment):
    r=len(model['A']);q=attachment.get('dimension',0)
    require(isinstance(q,int) and q>=0)
    R=r+q;a=Q(model['contract']['a'])
    damping=list(map(Q,attachment.get('damping',[])))
    require(len(damping)==q and all(x>0 for x in damping))
    J=decode_matrix(attachment.get('skew',[["0"]*R for _ in range(R)]))
    require(len(J)==R and all(len(row)==R for row in J))
    require(all(J[i][j]==-J[j][i] for i in range(R) for j in range(R)))
    alpha=min([a]+damping)
    return r,q,R,damping,J,alpha


def build_emulator(model,attachment):
    r,q,R,damping,J,alpha=attachment_data(model,attachment)
    old=reduced_matrix(model);d=len(old)+q
    L=[[Q(0)]*d for _ in range(d)]
    index=lambda i:i if i<r else i+q
    for i,row in enumerate(old):
        for j,v in enumerate(row):L[index(i)][index(j)]=v
    for i,v in enumerate(damping):L[r+i][r+i]-=v
    for i in range(R):
        for j in range(R):L[i][j]-=J[i][j]
    return L,R,alpha


def build_full(H,model,attachment):
    r,q,R,damping,J,alpha=attachment_data(model,attachment)
    ports=model['contract']['ports'];hidden=[i for i in range(len(H)) if i not in ports]
    order=ports+hidden;index=lambda i:i if i<r else i+q
    d=len(H)+q;L=[[Q(0)]*d for _ in range(d)]
    for i,source_i in enumerate(order):
        for j,source_j in enumerate(order):L[index(i)][index(j)]=-H[source_i][source_j]
    for i,v in enumerate(damping):L[r+i][r+i]-=v
    for i in range(R):
        for j in range(R):L[i][j]-=J[i][j]
    return L,R,alpha


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


def certify_reduced(model,path,attachment):
    L,R,a=build_emulator(model,attachment)
    r=len(model['A']);k=len(model['moments'])
    groups=[list(range(R))]+[list(range(R+r*j,R+r*(j+1))) for j in range(k)]
    cert=residual_certificate(L,path,R,groups)
    norms=[sqrt_upper(Q(v)) for v in cert['squared_residual_bounds']]
    c=Q(model['contract']['c'])
    Mnorm=[row_norm(decode_matrix(M)) for M in model['moments']]
    effective=norms[0]
    for j in range(k):effective+=Mnorm[j]*sum(norms[1:j+2],Q(0))/c
    y_norm=sqrt_upper(Q(cert['observed_L2_squared_bound']))
    error=Q(model['contract']['operator_error'])
    residual=effective+error*y_norm
    # 1/sqrt(2a) is enclosed ABOVE by sqrt(1/(2a)).
    sup_radius=residual*sqrt_upper(1/(2*a))
    cert.update({'effective_emulator_residual_L2':str(effective),
                 'source_port_residual_L2':str(residual),
                 'coercivity':str(a),
                 'uniform_observed_error_radius':str(sup_radius),
                 'observed_L2_error_radius':str(residual/a),
                 'additional_native_calls':0})
    return cert


def certify_full(matrix,path,r,a):
    cert=residual_certificate(matrix,path,r,[list(range(len(matrix)))])
    residual=sqrt_upper(Q(cert['squared_residual_bounds'][0]))
    cert['uniform_state_error_radius']=str(residual*sqrt_upper(1/(2*Q(a))))
    return cert
