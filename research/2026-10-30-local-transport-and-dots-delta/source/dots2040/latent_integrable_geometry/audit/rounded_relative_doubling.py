"""Hostile, NONCERTIFIED rounded-section relative-doubling experiments.

Fixed genuine genus-two periodic Toda curve from a=(1,2,3), b=(0,1,-1).
Exact rational rounded matrix/kernel/norm polynomial and exact rational root
isolation; analytic point evaluation, matching, projection, and Abel integration
are high precision numerical checks, not certificates. No producer imports.
"""
from pathlib import Path
import argparse,hashlib,json,math,time,traceback
import sympy as s
import mpmath as mp
import numpy as np
from scipy.optimize import linear_sum_assignment

ROOT=Path(__file__).resolve().parents[1]
x,t=s.symbols('x t');g=2;mp.mp.dps=110
F=s.Poly((x**3-15*x+8)**2-144,x,domain=s.QQ)
FDESC=[int(c) for c in F.all_coeffs()]
def rational_mp(v):
    v=s.Rational(v);return mp.mpf(int(v.p))/int(v.q)
def sym_complex(v):
    a,b=s.expand_complex(v).as_real_imag();return mp.mpc(rational_mp(a),rational_mp(b))
def polyvalue(P,z):return mp.polyval([rational_mp(c) for c in P.all_coeffs()],z)
def bitmax(values):
    return max((max(abs(int(s.Rational(v).p)).bit_length(),int(s.Rational(v).q).bit_length()) for v in values),default=0)
def outnum(v):
    if isinstance(v,mp.mpc):return {'re':mp.nstr(v.real,35),'im':mp.nstr(v.imag,35)}
    return mp.nstr(v,35)

def exact_roots(P,bits):
    """All roots, including multiplicity; each midpoint has rational isolator."""
    roots=[]
    for factor,multiplicity in P.sqf_list()[1]:
        reals,complexes=factor.intervals(eps=s.Rational(1,2**bits),all=True)
        for (a,b),m in reals:
            roots.append((rational_mp((a+b)/2),multiplicity*m))
        for (a,b),m in complexes:
            roots.append(((sym_complex(a)+sym_complex(b))/2,multiplicity*m))
    assert sum(m for _,m in roots)==P.degree()
    return roots

EDGES=sorted([a for a,m in exact_roots(F,320)])
def point(j,theta):
    lo,hi=EDGES[2*j+1:2*j+3];c=(lo+hi)/2;r=(hi-lo)/2
    xx=c+r*mp.cos(theta)
    excluded=mp.fprod(xx-e for k,e in enumerate(EDGES) if k not in [2*j+1,2*j+2])
    yy=r*mp.sin(theta)*mp.sqrt(-excluded)
    return {'x':xx,'y':yy,'gap':j,'theta':theta%(2*mp.pi),'infinity':False}
def angle_of(P,j):
    lo,hi=EDGES[2*j+1:2*j+3];c=(lo+hi)/2;r=(hi-lo)/2;xx,yy=P['x'],P['y']
    excluded=mp.fprod(xx-e for k,e in enumerate(EDGES) if k not in [2*j+1,2*j+2])
    return -1j*mp.log((xx-c)/r+1j*yy/(r*mp.sqrt(-excluded)))
def angular_distance(a,b):
    d=a-b;return mp.sqrt((mp.fmod(d.real+mp.pi,2*mp.pi)-mp.pi)**2+d.imag**2)
def circular_distance(a,b):return abs(mp.atan2(mp.sin(a-b),mp.cos(a-b)))
def perturb_angles(original,eps):
    result=[];displacements=[]
    for a in original:
        for k in [0,2,-2,4,-4,6,-6]:
            candidate=(a+k*eps)%(2*mp.pi)
            if all(circular_distance(candidate,b)>=eps for b in result):break
        else:raise RuntimeError('angle separation construction failed')
        result.append(candidate);displacements.append(circular_distance(candidate,a))
    return result,displacements

_integral_cache={}
def abel_point(j,theta):
    theta=mp.mpf(theta)%(2*mp.pi);key=(j,mp.nstr(theta,115))
    if key in _integral_cache:return _integral_cache[key]
    lo,hi=EDGES[2*j+1:2*j+3];c=(lo+hi)/2;r=(hi-lo)/2
    def integrand(u,k):
        xx=c+r*mp.cos(u)
        excluded=mp.fprod(xx-e for l,e in enumerate(EDGES) if l not in [2*j+1,2*j+2])
        return -xx**k/mp.sqrt(-excluded)
    cuts=[mp.mpf(0)]+([mp.pi] if theta>mp.pi else [])+[theta]
    v=mp.matrix([mp.quad(lambda u:integrand(u,k),cuts) for k in range(g)])
    _integral_cache[key]=v;return v
def abel_period(j):
    lo,hi=EDGES[2*j+1:2*j+3];c=(lo+hi)/2;r=(hi-lo)/2
    def f(u,k):
        xx=c+r*mp.cos(u)
        excluded=mp.fprod(xx-e for l,e in enumerate(EDGES) if l not in [2*j+1,2*j+2])
        return -xx**k/mp.sqrt(-excluded)
    return mp.matrix([mp.quad(lambda u:f(u,k),[0,mp.pi,2*mp.pi]) for k in range(g)])
PERIODS=mp.matrix(g,g)
for jj in range(g):PERIODS[:,jj]=abel_period(jj)
def sumabel(angles):return sum((abel_point(j,a) for j,a in enumerate(angles)),mp.zeros(g,1))
def mod_period(v):
    coeff=mp.lu_solve(PERIODS,v);integers=mp.matrix([mp.nint(c) for c in coeff])
    rem=v-PERIODS*integers
    return {'residual_norm':outnum(mp.norm(rem)),'period_coordinate_residual':outnum(mp.norm(coeff-integers)),
            'removed_period_integers':[int(v) for v in integers]}

def section_zeros(A,B,bits):
    common=s.gcd(A,B).monic();Ar=A.exquo(common);Br=B.exquo(common)
    R=(Ar*Ar-F*Br*Br);zeros=[]
    def add(xx,yy,m,kind):
        for _ in range(m):zeros.append({'x':xx,'y':yy,'infinity':False,'kind':kind})
    # Common x-factors put zeros on BOTH sheets, doubled at a branchpoint.
    for fac,m in common.sqf_list()[1]:
        branch=s.gcd(fac,F);ordinary=fac.exquo(branch)
        for xx,mr in exact_roots(branch,bits):add(xx,mp.mpf(0),2*m*mr,'common_branch')
        for xx,mr in exact_roots(ordinary,bits):
            yy=mp.sqrt(polyvalue(F,xx));add(xx,yy,m*mr,'common_plus');add(xx,-yy,m*mr,'common_minus')
    branch=s.gcd(R,F);ordinary=R.exquo(branch)
    for xx,m in exact_roots(branch,bits):add(xx,mp.mpf(0),m,'section_branch')
    for xx,m in exact_roots(ordinary,bits):
        yy=mp.sqrt(polyvalue(F,xx));plus=abs(polyvalue(Ar,xx)+yy*polyvalue(Br,xx));minus=abs(polyvalue(Ar,xx)-yy*polyvalue(Br,xx))
        add(xx,yy if plus<=minus else -yy,m,'ordinary_section')
    # Zeros at each infinity of the SECTION, even if f has fewer actual poles.
    Frev=s.expand(t**(2*g+2)*F.as_expr().subs(x,1/t));sq=s.series(s.sqrt(Frev),t,0,4*g+1).removeO()
    infinity_orders=[]
    for sign in [1,-1]:
        series=s.Poly(s.expand(t**(2*g)*A.as_expr().subs(x,1/t)+sign*t**(g-1)*B.as_expr().subs(x,1/t)*sq),t)
        order=next((k for k in range(4*g+1) if series.nth(k)!=0),None)
        if order is None:raise RuntimeError('infinity order exceeds section degree')
        infinity_orders.append(order)
        for _ in range(order):zeros.append({'infinity':True,'sheet':sign,'kind':'infinity'})
    assert len(zeros)==4*g, ('section degree count',len(zeros),A,B)
    return zeros,{'common_factor_degree':common.degree(),'reduced_norm_degree':R.degree(),
                  'infinity_orders':infinity_orders,'norm_coefficient_bits':bitmax((A*A-F*B*B).all_coeffs())}

def run_case(name,D0,D,qbits,epsbits,perturb=True,kernel_choice=0):
    start=time.perf_counter();eps=mp.mpf(2)**(-epsbits);points=[];perturbation=mp.zeros(g,1)
    separation=mp.inf;maxdisplacement=mp.mpf(0)
    for j in range(g):
        old=[D[j],D[j],(-D0[j])%(2*mp.pi)]
        angles,disp=perturb_angles(old,eps) if perturb else (old,[mp.mpf(0)]*3)
        separation=min(separation,*[circular_distance(angles[k],angles[l]) for k in range(3) for l in range(k)])
        maxdisplacement=max(maxdisplacement,*disp)
        for oldtheta,theta in zip(old,angles):
            points.append(point(j,theta))
            # Use the short local lift across angle zero, not an artificial
            # full-period jump in the fundamental-interval Abel integral.
            delta=mp.atan2(mp.sin(theta-oldtheta),mp.cos(theta-oldtheta))
            winding=mp.nint((theta-oldtheta-delta)/(2*mp.pi))
            perturbation+=abel_point(j,theta)-abel_point(j,oldtheta)-winding*PERIODS[:,j]
    result={'name':name,'qbits':qbits,'epsbits':epsbits,'perturbed':perturb,'kernel_choice':kernel_choice,
            'input_min_angle_separation':outnum(separation),'max_angle_displacement':outnum(maxdisplacement),
            'D0_angles':list(map(outnum,D0)),'D_angles':list(map(outnum,D)),
            'abel_perturbation_norm':outnum(mp.norm(perturbation))}
    rows=[];true_rows=[]
    for P in points:
        xx,yy=P['x'],P['y'];row=[xx**k for k in range(2*g+1)]+[yy*xx**k for k in range(g)]
        true_rows.append(row);rows.append([int(mp.nint(v*2**qbits)) for v in row])
    M=s.Matrix(rows);kernel_start=time.perf_counter();basis=M.nullspace();assert basis
    v=basis[0] if kernel_choice==0 else sum(((j+1)*b for j,b in enumerate(basis)),s.zeros(3*g+1,1))
    vmax=max(abs(a) for a in v);v=v/vmax;assert M*v==s.zeros(3*g,1)
    result.update({'rounded_rank':3*g+1-len(basis),'nullity':len(basis),'matrix_entry_bits':bitmax(M),
                   'kernel_coefficient_bits':bitmax(v),'kernel_seconds':time.perf_counter()-kernel_start})
    residual=max(abs(sum(row[j]*rational_mp(v[j]) for j in range(3*g+1))) for row in true_rows)
    bound=mp.mpf(3*g+1)*mp.mpf(2)**(-qbits-1)
    result.update({'max_input_section_residual':outnum(residual),'rounding_residual_bound':outnum(bound),
                   'residual_within_rounding_bound':bool(residual<=bound*(1+mp.mpf('1e-40')))})
    A=s.Poly(sum(v[k]*x**k for k in range(2*g+1)),x,domain=s.QQ)
    B=s.Poly(sum(v[2*g+1+k]*x**k for k in range(g)),x,domain=s.QQ)
    result['section_A']=list(map(str,reversed(A.all_coeffs())))
    result['section_B']=list(map(str,reversed(B.all_coeffs())))
    root_start=time.perf_counter();zeros,metadata=section_zeros(A,B,qbits+100)
    result.update(metadata);result['root_isolation_seconds']=time.perf_counter()-root_start
    # Minimum-cost injective matching of six inputs to eight section zeros.
    costs=np.full((3*g,4*g),1e100);anglecache={}
    for i,P in enumerate(points):
        for k,Z in enumerate(zeros):
            if Z['infinity']:continue
            try:
                ang=angle_of(Z,P['gap']);anglecache[i,k]=ang
                costs[i,k]=min(1e99,float(angular_distance(ang,mp.mpc(P['theta']))))
            except (ValueError,ZeroDivisionError):pass
    ii,kk=linear_sum_assignment(costs);assert len(ii)==3*g
    maxmatch=max(costs[i,k] for i,k in zip(ii,kk));matched=set(map(int,kk));remaining=[Z for k,Z in enumerate(zeros) if k not in matched]
    result.update({'matching_max_angle_distance':str(maxmatch),
      'matching_below_quarter_input_separation':bool(perturb and maxmatch<float(separation/4)),
      'matched_zero_kinds':[zeros[k]['kind'] for k in kk],
      'remaining_zero_kinds':[P['kind'] for P in remaining]})
    # Assign residual involutes to distinct physical ovals, then project the
    # complex signed angle to its real part. Record, rather than hide, failures.
    if any(P['infinity'] for P in remaining):
        result['status']='RESIDUAL_INFINITY';result['total_seconds']=time.perf_counter()-start;return result
    E=[dict(P,y=-P['y']) for P in remaining];pcost=np.zeros((g,g));angles={}
    for j in range(g):
        lo,hi=EDGES[2*j+1:2*j+3]
        for k,P in enumerate(E):
            try:
                ang=angle_of(P,j);angles[j,k]=ang
                # Height of local complex angle plus distance of x from gap.
                outdist=max(mp.mpf(0),lo-P['x'].real,P['x'].real-hi)/(hi-lo)
                pcost[j,k]=min(1e99,float(abs(ang.imag)+outdist))
            except (ValueError,ZeroDivisionError):pcost[j,k]=1e100
    ji,ki=linear_sum_assignment(pcost);projected=[None]*g;collars=[];movement=[]
    for j,k in zip(ji,ki):
        ang=angles[j,k];theta=ang.real%(2*mp.pi);projected[j]=theta;collars.append(abs(ang.imag))
        P=point(j,theta);movement.append(abs(P['x']-E[k]['x'])+abs(P['y']-E[k]['y']))
    result.update({'output_one_point_per_gap':bool(all(pcost[j,k]<0.1 for j,k in zip(ji,ki))),
      'max_complex_angle_height':outnum(max(collars)),'projection_max_xy_movement':outnum(max(movement)),
      'projected_output_angles':list(map(outnum,projected))})
    r=sumabel(projected)-2*sumabel(D)+sumabel(D0)
    result['abel_original_relative_residual']=mod_period(r)
    result['abel_perturbed_section_residual']=mod_period(r-perturbation)
    result['status']='CHECKED_NOT_CERTIFIED';result['total_seconds']=time.perf_counter()-start
    return result

def cases():
    base=[mp.mpf('.7'),mp.mpf('2.0')]
    return {
      'generic':(base,[mp.mpf('1.3'),mp.mpf('4.5')]),
      'branch_edges':([mp.mpf(0),mp.pi],[mp.pi,mp.mpf(0)]),
      'branch_triple':([mp.mpf(0),mp.pi],[mp.mpf(0),mp.pi]),
      'exact_conjugate':(base,[(-a)%(2*mp.pi) for a in base]),
      'near_conjugate':(base,[(-a+mp.mpf(2)**-40)%(2*mp.pi) for a in base]),
      'exact_identity':(base,list(base)),
      'near_identity':(base,[a+mp.mpf(2)**-40 for a in base]),
      'near_branch_collision':([mp.mpf(2)**-40,mp.pi+mp.mpf(2)**-40],[mp.mpf(0),mp.pi])}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--names',default='generic');ap.add_argument('--qbits',default='32,64,128')
    ap.add_argument('--epsbits',type=int,default=12);ap.add_argument('--naive',action='store_true');ap.add_argument('--kernel-choice',type=int,default=0)
    ap.add_argument('--output',default='rounded_relative_doubling_results.json');args=ap.parse_args()
    output=Path(__file__).with_name(args.output);results=[]
    header={'warning':'Noncertified experiment; rational root isolation does not certify analytic evaluation/matching/projection/Abel error.',
            'F':str(F.as_expr()),'edges':list(map(outnum,EDGES)),
            'real_period_matrix':[[outnum(PERIODS[i,j]) for j in range(g)] for i in range(g)],
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for name in args.names.split(','):
        D0,D=cases()[name]
        for q in map(int,args.qbits.split(',')):
            try:result=run_case(name,D0,D,q,args.epsbits,not args.naive,args.kernel_choice)
            except Exception as exc:result={'name':name,'qbits':q,'epsbits':args.epsbits,'perturbed':not args.naive,
                'status':'EXCEPTION','error':repr(exc),'traceback':traceback.format_exc()}
            results.append(result);output.write_text(json.dumps(dict(header,results=results),indent=2))
            print(json.dumps({k:v for k,v in result.items() if k not in ['section_A','section_B','traceback']},indent=2),flush=True)
    return 0
if __name__=='__main__':main()
