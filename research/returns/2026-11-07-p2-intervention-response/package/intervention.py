"""Finite intervention prediction and certified value-only design.

All arithmetic outside the explicitly bounded elementary-function enclosures
uses fractions.Fraction. A reader supplies calibrated scalar energy records;
it is not a unit-cost oracle. See RESEARCH_REPORT.txt for the hypotheses and
the full acquisition/cost contract. No physical measurement is performed here.
"""
from fractions import Fraction as Q
from itertools import product
from math import prod
import json

def qtree(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,dict): return {str(k):qtree(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [qtree(v) for v in x]
    return x

def dyadic_below(x):
    """Largest power of two <= x, for 0<x<=1."""
    x=Q(x)
    if not 0<x<=1: raise ValueError("Expected 0<x<=1")
    y=Q(1)
    while y>x: y/=2
    return y

def round_dyadic(x,bits):
    scale=1<<bits
    n=(2*x.numerator*scale+x.denominator)//(2*x.denominator)
    return Q(n,scale)

def precision_for(radius):
    bits=0
    while Q(1,1<<bits)>radius: bits+=1
    return bits

def atan_interval(den,bits):
    x=Q(1,den); power=x; total=Q(0); sign=1; k=0
    tol=Q(1,1<<(bits+12))
    while True:
        term=sign*power/(2*k+1)
        updated=total+term
        if abs(term)<tol:
            return min(total,updated),max(total,updated)
        total=updated; power*=x*x; sign=-sign; k+=1

def pi_interval(bits):
    a=atan_interval(5,bits); b=atan_interval(239,bits)
    return 16*a[0]-4*b[1],16*a[1]-4*b[0]

def cos_approx(x,tolerance):
    """Rational midpoint and rigorous Taylor remainder for real |x|<=4."""
    assert abs(x)<=4
    total=Q(1); term=Q(1); k=0
    while True:
        k+=1
        term=-term*x*x/((2*k-1)*(2*k))
        if abs(term)<=tolerance:
            # total is the Taylor polynomial of degree 2k-2.
            # The degree 2k-1 Taylor polynomial is the same; remainder <=|term|.
            return total,abs(term)
        total+=term

def cheb_nodes(n,delta):
    """Rational nodes q_j with certified |q_j-cos((2j+1)pi/(2n))|<=delta."""
    bits=precision_for(delta)+8
    p=pi_interval(bits+8)
    pm=(p[0]+p[1])/2; pr=(p[1]-p[0])/2
    nodes=[]; errors=[]
    for j in range(n):
        factor=Q(2*j+1,2*n)
        cm,cr=cos_approx(factor*pm,Q(1,1<<(bits+4)))
        node=round_dyadic(cm,bits)
        node=max(Q(-1),min(Q(1),node))
        err=cr+factor*pr+Q(1,1<<(bits+1))
        assert err<=delta
        nodes.append(node); errors.append(err)
    return nodes,errors,bits

def cheb_values(x,n):
    out=[Q(1)]
    if n>1: out.append(Q(x))
    for j in range(2,n): out.append(2*x*out[-1]-out[-2])
    return out

def energy_tensor(reader,theta,d,tensor_radius):
    """Reconstruct a symmetric tensor from d(d+1)/2 scalar energies."""
    scalar_radius=Q(tensor_radius,2*d)
    diagonal=[]; de=[]; records=[]
    for i in range(d):
        e=[Q(0)]*d; e[i]=Q(1)
        rec=reader(theta,e,scalar_radius)
        assert rec["error"]<=scalar_radius
        diagonal.append(rec["mid"]); de.append(rec["error"]); records.append(rec)
    mat=[[Q(0) for _ in range(d)] for _ in range(d)]
    errs=[[Q(0) for _ in range(d)] for _ in range(d)]
    for i in range(d): mat[i][i]=diagonal[i]; errs[i][i]=de[i]
    for i in range(d):
        for j in range(i+1,d):
            e=[Q(0)]*d; e[i]=e[j]=Q(1)
            rec=reader(theta,e,scalar_radius)
            assert rec["error"]<=scalar_radius
            val=(rec["mid"]-diagonal[i]-diagonal[j])/2
            err=(rec["error"]+de[i]+de[j])/2
            mat[i][j]=mat[j][i]=val; errs[i][j]=errs[j][i]=err
            records.append(rec)
    op_error=max(sum(row) for row in errs)
    assert op_error<=tensor_radius
    return mat,op_error,records

def choose_predictor_parameters(k,r,U,epsilon,rho=None):
    k=int(k); r,U,epsilon=map(Q,(r,U,epsilon))
    if k<1 or not 0<r<1 or U<=0 or epsilon<=0:
        raise ValueError("Invalid predictor contract")
    if rho is None:
        s=Q(1)
        while s*s>1-r: s/=2
        rho=1+s
    rho=Q(rho)
    chi=(rho+1/rho)/2
    assert rho>1 and r*chi<1
    B=U/(1-r*chi)
    n=1
    while Q(2**(k+1)*k)*B*rho**(-n)/(1-1/rho)**k>epsilon/3:
        n+=1
    trunc=Q(2**(k+1)*k)*B*rho**(-n)/(1-1/rho)**k
    gain=(2*n)**k
    B0=(1+r)*U
    Ly=r*(1+r)*U/(1-r)
    nu=epsilon/(12*gain)
    delta_target=min(Q(1,100*n*n),epsilon/(12*gain*(Ly+B0*k*n*n)))
    delta=Q(1,1<<precision_for(delta_target))
    return dict(k=k,r=r,U=U,epsilon=epsilon,rho=rho,B=B,n=n,
                truncation=trunc,noise_gain=gain,B0=B0,Ly=Ly,
                tensor_radius=nu,node_radius=delta)

def compile_predictor(reader,k,d,r,U,epsilon,rho=None,max_nodes=None):
    pars=choose_predictor_parameters(k,r,U,epsilon,rho)
    n=pars["n"]; N=n**k
    if max_nodes is not None and N>max_nodes:
        raise RuntimeError("Declared acquisition cap exceeded; no impossibility inferred")
    nodes,node_errors,bits=cheb_nodes(n,pars["node_radius"])
    basis=[cheb_values(x,n) for x in nodes]
    indices=list(product(range(n),repeat=k))
    data={}; acquisitions=[]; maximum_node_error=Q(0)
    for ix in indices:
        theta=[Q(r)*nodes[j] for j in ix]
        mat,err,records=energy_tensor(reader,theta,d,pars["tensor_radius"])
        maximum_node_error=max(maximum_node_error,err)
        data[ix]=[mat[i][j] for i in range(d) for j in range(d)]
        acquisitions.append(dict(index=ix,theta=theta,records=records,
                                 tensor_error=err))
    # Separable exact tensor transform, O(k n^(k+1) d^2) rational operations.
    for axis in range(k):
        updated={}
        for other in product(range(n),repeat=k-1):
            for nu in range(n):
                acc=[Q(0)]*(d*d)
                for j in range(n):
                    old_ix=list(other); old_ix.insert(axis,j); old_ix=tuple(old_ix)
                    weight=basis[j][nu]
                    vals=data[old_ix]
                    for a in range(d*d): acc[a]+=weight*vals[a]
                factor=Q(1 if nu==0 else 2,n)
                new_ix=list(other); new_ix.insert(axis,nu)
                updated[tuple(new_ix)]=[factor*x for x in acc]
        data=updated
    total_bound=pars["truncation"]+pars["noise_gain"]*(
        maximum_node_error+
        (pars["Ly"]+pars["B0"]*k*n*n)*pars["node_radius"])
    assert total_bound<=epsilon
    coefficient_bits=max(max(abs(x.numerator).bit_length(),x.denominator.bit_length())
                         for values in data.values() for x in values)
    return dict(parameters=pars,d=d,nodes=nodes,node_error_bounds=node_errors,
                node_bits=bits,coefficients=data,acquisitions=acquisitions,
                uniform_operator_error=total_bound,
                maximum_coefficient_bits=coefficient_bits)

def evaluate_predictor(model,theta):
    pars=model["parameters"]; k=pars["k"]; n=pars["n"]; r=pars["r"]; d=model["d"]
    theta=list(map(Q,theta))
    if len(theta)!=k or any(abs(t)>r for t in theta):
        raise ValueError("Query outside the certified control box")
    v=[cheb_values(t/r,n) for t in theta]
    out=[Q(0)]*(d*d)
    for ix,coefs in model["coefficients"].items():
        weight=prod(v[j][ix[j]] for j in range(k))
        for a in range(d*d): out[a]+=weight*coefs[a]
    return [out[i*d:(i+1)*d] for i in range(d)]

def read_predictor(path):
    """Load the saved rational polynomial without invoking its source reader."""
    with open(path) as handle: model=json.load(handle)
    model["parameters"]={key:(Q(value) if isinstance(value,str) else value)
                          for key,value in model["parameters"].items()}
    model["coefficients"]={
        tuple(int(x.strip()) for x in key.strip("()").split(",") if x.strip()):
            [Q(x) for x in values]
        for key,values in model["coefficients"].items()}
    model["uniform_operator_error"]=Q(model["uniform_operator_error"])
    return model

def certified_design(reader,vertices,e,r,S,epsilon,price=None,max_iterations=None):
    """Value-only conditional-gradient design with an explicit global gap.

    S is a supplied upper bound on the baseline energy for loading e.
    vertices are explicitly supplied rational controls in [-r,r]^k.
    The reader's scalar error includes every acquisition/actuation error.
    """
    V=[list(map(Q,v)) for v in vertices]; e=list(map(Q,e))
    if not V: raise ValueError("Empty vertex list")
    k=len(V[0]); q=len(V); r,S,eps=map(Q,(r,S,epsilon))
    if k<1 or not 0<r<1 or S<0 or eps<=0: raise ValueError("Invalid design contract")
    if any(len(v)!=k or any(abs(x)>r for x in v) for v in V):
        raise ValueError("Vertices outside certified domain")
    price=list(map(Q,price or [0]*k))
    if len(price)!=k: raise ValueError("Price dimension mismatch")
    diam=max((max(v[j] for v in V)-min(v[j] for v in V) for j in range(k)),default=Q(0))
    C=2*(1+r)*S*diam*diam/(1-r)**2
    Ct=max(C,eps)
    h=eps/(8*Ct); nu=eps*h/64
    pcost=[sum(price[j]*v[j] for j in range(k)) for v in V]
    range_bound=2*r*S+max(pcost)-min(pcost)
    lipschitz=(1+r)*S/(1-r)+sum(abs(x) for x in price)
    rounding_scale=lipschitz*diam*max(0,q-1)
    weight_bits=precision_for(eps*eps/(32*Ct*rounding_scale)) if rounding_scale else 0
    weight_denominator=1<<weight_bits
    rounding_loss=rounding_scale/weight_denominator
    assert rounding_loss<=eps*eps/(32*Ct)
    maximum_updates=int(16*Ct*range_bound/(eps*eps))+1
    theta=V[0][:]
    weights=[Q(i==0) for i in range(q)]
    transcript=[]
    for iteration in range(maximum_updates+2):
        if max_iterations is not None and iteration>=max_iterations:
            raise RuntimeError("Declared execution cap reached before certification")
        rec0=reader(theta,e,nu)
        assert rec0["error"]<=nu
        val0=rec0["mid"]-sum(price[j]*theta[j] for j in range(k))
        probes=[]; secants=[]
        for v in V:
            point=[(1-h)*theta[j]+h*v[j] for j in range(k)]
            rec=reader(point,e,nu)
            assert rec["error"]<=nu
            val=rec["mid"]-sum(price[j]*point[j] for j in range(k))
            secants.append((val-val0)/h)
            probes.append(rec)
        top=max(secants); i=secants.index(top)
        gap_upper=top+2*nu/h+C*h/2
        row=dict(iteration=iteration,theta=theta[:],baseline=rec0,probes=probes,
                 secants=secants,gap_upper=gap_upper)
        transcript.append(row)
        if gap_upper<=eps:
            return dict(theta=theta,weights=weights,vertices=V,loading=e,
                        price=price,r=r,baseline_energy_bound=S,
                        value_interval=[val0-nu,val0+nu],
                        optimum_interval=[val0-nu,val0+nu+max(Q(0),gap_upper)],
                        gap_upper=gap_upper,epsilon=eps,curvature=C,
                        h=h,reading_radius=nu,range_bound=range_bound,
                        lipschitz=lipschitz,diameter=diam,
                        curvature_envelope=Ct,weight_bits=weight_bits,
                        rounding_objective_loss_bound=rounding_loss,
                        a_priori_update_bound=maximum_updates,
                        updates=iteration,transcript=transcript,
                        maximum_control_bits=max(
                            max(abs(x.numerator).bit_length(),x.denominator.bit_length())
                            for item in transcript
                            for rec in [item["baseline"]]+item["probes"]
                            for x in rec["theta"]))
        lower_direction=top-2*nu/h
        assert lower_direction>=7*eps/8
        step=dyadic_below(min(Q(1),lower_direction/Ct))
        row["vertex"]=i; row["step"]=step
        raw_weights=[(1-step)*w+step*Q(j==i) for j,w in enumerate(weights)]
        # Round within the simplex: move every discarded fraction to vertex 0.
        weights=[Q(0)]+[Q((w*weight_denominator).__floor__(),weight_denominator)
                         for w in raw_weights[1:]]
        weights[0]=1-sum(weights[1:])
        assert all(w>=0 for w in weights) and sum(weights)==1
        theta=[sum(weights[j]*V[j][a] for j in range(q)) for a in range(k)]
    raise AssertionError("Valid contract contradicts proved progress bound")

def affine_coefficient_name(exact_module,base_name,direction_names,theta):
    """Paid construction of a valid coefficient name at an actual rational control."""
    theta=list(map(Q,theta))
    if len(theta)!=len(direction_names): raise ValueError("Control count mismatch")
    def name(n):
        s=n; multiplier=1+sum(abs(t) for t in theta)
        while multiplier*Q(1,1<<s)>Q(1,1<<n): s+=1
        fields=[base_name(s)]+[f(s) for f in direction_names]
        d=fields[0].d; level=max(f.level for f in fields)
        if any(f.d!=d for f in fields): raise ValueError("Dimension mismatch")
        weights=[Q(1)]+theta; vals={}
        for ix in product(range(1<<level),repeat=d):
            x=[Q(2*j+1,2*(1<<level)) for j in ix]
            arrays=[f.at(x) for f in fields]
            vals[ix]=[[sum(w*a[i][j] for w,a in zip(weights,arrays))
                       for j in range(d)] for i in range(d)]
        err=sum(abs(w)*f.error for w,f in zip(weights,fields))
        assert err<=Q(1,1<<n)
        return exact_module.StepField(d,level,vals,err)
    return name

def represented_name_reader(exact_module,base_name,direction_names,tau,M,r,
                            max_stages=None):
    """A concrete numerical acquisition path; every predecessor solve is paid."""
    records=[]
    def read(theta,e,radius):
        name=affine_coefficient_name(exact_module,base_name,direction_names,theta)
        field_tolerance=Q(1)
        while field_tolerance*field_tolerance>2*radius: field_tolerance/=2
        cert=exact_module.certified_solve(
            name,Q(tau)*(1-Q(r)),Q(M),e,field_tolerance,max_stages=max_stages)
        rec=dict(theta=list(theta),loading=list(e),
                 mid=(cert["lower"]+cert["upper"])/2,error=cert["gap"]/2,
                 stage=cert["stage"],mesh_level=cert["mesh_level"],
                 primal_dimension=cert["primal_dimension"],
                 dual_dimension=cert["dual_dimension"])
        assert rec["error"]<=radius
        records.append(rec)
        return rec
    return read,records

def reciprocal_sqrt_under(x,relative_error):
    """Rational t with 1-relative_error <= t*sqrt(x) <= 1, x>0.

    Only rational comparisons and bisection are used. All generated powers
    of two and bisection operations are paid finite computation.
    """
    x=Q(x); rel=Q(relative_error)
    assert x>0 and 0<rel<1
    upper=Q(1)
    while upper*upper<x: upper*=2
    while (upper/2)**2>=x: upper/=2
    lower=upper/2
    while upper-lower>rel*lower:
        middle=(lower+upper)/2
        if middle*middle<=x: lower=middle
        else: upper=middle
    return 1/upper

def rounded_ellipsoid_update(center,shape,normal,beta,center_bits,shape_bits):
    """Contain the central half-ellipsoid using a bounded rational update.

    The retained side is normal.(x-center)<=0. The report proves containment,
    volume decrease and polynomial bit bounds, including both roundings.
    """
    m=len(center); assert m>=2
    u=[sum(shape[i][j]*normal[j] for j in range(m)) for i in range(m)]
    quadratic=sum(normal[i]*u[i] for i in range(m))
    assert quadratic>0
    t=reciprocal_sqrt_under(quadratic,m*beta)
    new_center=[round_dyadic(center[i]-t*u[i]/(m+1),center_bits) for i in range(m)]
    factor=Q(m*m,m*m-1)
    inflated=[[(1+2*beta)**2*factor*(shape[i][j]-Q(2,m+1)*u[i]*u[j]/quadratic)
               for j in range(m)] for i in range(m)]
    new_shape=[[round_dyadic(inflated[i][j],shape_bits)+
                (Q(m,1<<shape_bits) if i==j else 0)
                for j in range(m)] for i in range(m)]
    return new_center,new_shape

def ellipsoid_design(reader,vertices,e,r,S,epsilon,price=None,
                     force_volume_certificate=False):
    """Polynomial-record global design from calibrated values, no cut oracle.

    The explicit vertex list is lifted to a full-dimensional simplex.
    All physical probes remain in its convex hull. At most (q+1)*N scalar
    records are used, N=4*q*(q-1)*(B+1); B is the proved logarithmic accuracy
    budget. q=1 uses one record. No coefficient reconstruction is performed.
    """
    V=[list(map(Q,v)) for v in vertices]; e=list(map(Q,e))
    if not V: raise ValueError("Empty vertex list")
    q=len(V); m=q-1; k=len(V[0]); r,S,eps=map(Q,(r,S,epsilon))
    if k<1 or not 0<r<1 or S<0 or eps<=0: raise ValueError("Invalid design contract")
    if any(len(v)!=k or any(abs(t)>r for t in v) for v in V):
        raise ValueError("Invalid control vertices")
    price=list(map(Q,price or [0]*k))
    if len(price)!=k: raise ValueError("Price dimension mismatch")
    diam=max((max(v[j] for v in V)-min(v[j] for v in V) for j in range(k)),default=Q(0))
    eta=eps/2
    C=2*(1+r)*S*diam*diam/(1-r)**2; Ct=max(C,eta)
    h=eta/(16*Ct); nu=eta*h/256
    Ltheta=(1+r)*S/(1-r)+sum(abs(x) for x in price)
    L=max(Ltheta*diam*m,eta)
    ball_radius=eta/(16*q*q*L)
    B=precision_for(ball_radius)
    N=4*m*(m+1)*(B+1) if m else 1
    beta=Q(1,64*m*(m+1)) if m>=2 else Q(0)
    center_bits=precision_for(beta*Q(1,1<<N)/m) if m>=2 else N+2
    shape_bits=precision_for(beta*Q(1,1<<(2*N))/(2*m)) if m>=2 else N+2
    record_bits=precision_for(nu/2)
    actuation_scale=Ltheta*diam*max(0,q-1)
    actuation_bits=precision_for(nu/(4*actuation_scale)) if actuation_scale else 0
    actuation_denominator=1<<actuation_bits
    actuation_loss=actuation_scale/actuation_denominator
    assert actuation_loss<=nu/4
    records=[]; transcript=[]; best=None
    def acquire(weights):
        theta=[sum(weights[i]*V[i][j] for i in range(q)) for j in range(k)]
        actuated_weights=[Q(0)]+[
            Q((w*actuation_denominator).__floor__(),actuation_denominator)
            for w in weights[1:]]
        actuated_weights[0]=1-sum(actuated_weights[1:])
        actual=[sum(actuated_weights[i]*V[i][j] for i in range(q)) for j in range(k)]
        raw=reader(actual,e,nu/4)
        assert raw["error"]<=nu/4
        actual_mid=raw["mid"]-sum(price[j]*actual[j] for j in range(k))
        mid=round_dyadic(actual_mid,record_bits)
        error=raw["error"]+Q(1,1<<(record_bits+1))+actuation_loss
        assert error<=nu
        rec=dict(theta=theta,actuated_theta=actual,actuated_weights=actuated_weights,
                 energy_record=raw,objective_mid=mid,objective_error=error)
        records.append(rec)
        return rec
    def finish(reason,point,record,gap,iteration,center,shape):
        gap=gap+actuation_loss
        assert gap<=eps
        return dict(theta=record["actuated_theta"],nominal_theta=point,
                    reason=reason,epsilon=eps,internal_accuracy=eta,gap_upper=gap,
                    value_interval=[record["objective_mid"]-nu,record["objective_mid"]+nu],
                    optimum_interval=[record["objective_mid"]-nu,record["objective_mid"]+nu+gap],
                    vertices=V,loading=e,price=price,r=r,baseline_energy_bound=S,
                    diameter=diam,curvature=C,curvature_envelope=Ct,h=h,reading_radius=nu,
                    objective_lipschitz=Ltheta,lifted_lipschitz=L,near_optimal_ball_radius=ball_radius,
                    logarithmic_radius_bits=B,maximum_iterations=N,iterations=iteration,
                    beta=beta,center_bits=center_bits,shape_bits=shape_bits,record_bits=record_bits,
                    actuation_bits=actuation_bits,actuation_objective_loss_bound=actuation_loss,
                    source_reading_radius=nu/4,
                    records=records,transcript=transcript,final_center=center,final_shape=shape,
                    maximum_control_bits=max(
                        max(abs(x.numerator).bit_length(),x.denominator.bit_length())
                        for rec in records for x in rec["actuated_theta"]))
    if m==0:
        rec=acquire([Q(1)])
        return finish("single feasible vertex",V[0],rec,Q(0),0,[],[])
    center=[Q(0)]*m
    shape=[[Q(i==j) for j in range(m)] for i in range(m)]
    interval=[Q(-1),Q(1)]
    for iteration in range(N):
        row=dict(iteration=iteration,center=center[:],shape=[a[:] for a in shape])
        transcript.append(row)
        negative=next((i for i,x in enumerate(center) if x<0),None)
        if negative is not None:
            normal=[Q(-int(i==negative)) for i in range(m)]
            row["kind"]="simplex coordinate cut"
        elif sum(center)>1:
            normal=[Q(1)]*m
            row["kind"]="simplex sum cut"
        else:
            weights=center+[1-sum(center)]
            theta=[sum(weights[i]*V[i][j] for i in range(q)) for j in range(k)]
            rec0=acquire(weights); index0=len(records)-1
            if best is None or rec0["objective_mid"]>best[1]["objective_mid"]:
                best=(theta[:],rec0)
            secants=[]; probe_indices=[]
            for j in range(q):
                probe_weights=[(1-h)*w+h*Q(i==j) for i,w in enumerate(weights)]
                rec=acquire(probe_weights); probe_indices.append(len(records)-1)
                secants.append((rec["objective_mid"]-rec0["objective_mid"])/h)
            gap=max(secants)+2*nu/h+C*h/2
            gradient=[secants[i]-secants[-1] for i in range(m)]
            row.update(kind="measured objective cut",theta=theta,
                       record_index=index0,probe_indices=probe_indices,
                       secants=secants,gradient=gradient,gap_upper=gap)
            if (gap<=eta and not force_volume_certificate) or not any(gradient):
                assert gap<=eta
                return finish("measured global gap",theta,rec0,max(Q(0),gap),iteration+1,center,shape)
            normal=[-g for g in gradient]
        row["cut_normal"]=normal
        if m==1:
            if normal[0]>0: interval[1]=center[0]
            else: interval[0]=center[0]
            center=[(interval[0]+interval[1])/2]
            shape=[[(interval[1]-interval[0])**2/4]]
        else:
            center,shape=rounded_ellipsoid_update(center,shape,normal,beta,center_bits,shape_bits)
    assert best is not None
    return finish("rounded ellipsoid volume bound",best[0],best[1],eta,N,center,shape)

def finite_quadratic_reader(base,directions,ports):
    """Construct paid records for an explicitly listed rational quadratic form.

    Coordinates 0..ports-1 are imposed; remaining coordinates minimize the
    positive quadratic energy. SPD/relative-actuation promises are part of
    the caller's contract. Gaussian elimination is implemented here; no
    external linear-system oracle or hidden state is used.
    """
    base=[[Q(x) for x in row] for row in base]
    directions=[[[Q(x) for x in row] for row in a] for a in directions]
    size=len(base); records=[]
    assert 1<=ports<=size and all(len(row)==size for row in base)
    def solve(matrix,rhs):
        n=len(rhs); aug=[row[:]+[v] for row,v in zip(matrix,rhs)]
        for j in range(n):
            pivot=next(i for i in range(j,n) if aug[i][j])
            aug[j],aug[pivot]=aug[pivot],aug[j]
            v=aug[j][j]; aug[j]=[x/v for x in aug[j]]
            for i in range(n):
                if i!=j:
                    v=aug[i][j]; aug[i]=[a-v*b for a,b in zip(aug[i],aug[j])]
        return [row[-1] for row in aug]
    def read(theta,e,radius):
        assert len(theta)==len(directions) and len(e)==ports
        mat=[[base[i][j]+sum(Q(t)*a[i][j] for t,a in zip(theta,directions))
              for j in range(size)] for i in range(size)]
        internal=[row[ports:] for row in mat[ports:]]
        rhs=[-sum(mat[i][j]*Q(e[j]) for j in range(ports)) for i in range(ports,size)]
        state=list(map(Q,e))+solve(internal,rhs)
        energy=sum(state[i]*mat[i][j]*state[j] for i in range(size) for j in range(size))
        bits=precision_for(radius)+1; mid=round_dyadic(energy,bits)
        rec=dict(theta=list(theta),loading=list(e),mid=mid,error=Q(1,1<<(bits+1)),
                 explicit_matrix_dimension=size,free_coordinates=size-ports,
                 source="explicit rational quadratic form and Gaussian elimination")
        assert abs(mid-energy)<=rec["error"]<=radius
        records.append(rec); return rec
    return read,records

