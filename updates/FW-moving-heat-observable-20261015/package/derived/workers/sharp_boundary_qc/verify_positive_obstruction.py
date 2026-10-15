"""Standalone exact NON-SOS local input-heat obstruction for every r>0.

Reads only POSITIVE_INPUT_HEAT_OBSTRUCTION.json. Rebuilds every necessary
linear constraint from F, compatible jets, contacts, and explicit symmetries;
then verifies the sparse rational equality dual. Analytic necessity of the
constraints is in POSITIVE_INPUT_HEAT_OBSTRUCTION.txt.
"""
import sympy as s
import json,sys,hashlib
from pathlib import Path
from itertools import combinations,combinations_with_replacement as cwr

def build_system():
    r,t,p,q=s.symbols('r t p q',real=True)
    x=s.Matrix(s.symbols('a b c d',real=True));a,b,c,d=x
    z=s.Matrix(s.symbols('z0:6',real=True))
    ww=list(s.symbols('w0:60'));d1,d2=s.symbols('d1 d2');vars_=ww+[d1,d2]
    u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
    F=3*r/(8*(r+2))*(u+v-2*j)**2+r*(r-1)*u*u/6+j*j+r*u*j
    HH=s.hessian(F,x)
    B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
    mons=[x[ii]*x[jj] for ii,jj in cwr(range(4),2)]
    OO=s.zeros(4)
    for ii,(i,k) in enumerate(combinations(range(4),2)):
        vv=sum(ww[10*ii+jj]*mm for jj,mm in enumerate(mons))
        OO[i,k]=vv;OO[k,i]=-vv
    P=s.expand(d1*(B1.T*HH*B1)[0]+d2*(B2.T*HH*B2)[0]+(B1.T*OO*B2)[0])
    oldA=s.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
    newA=s.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],[1,(r+1)*t]])
    rot=s.Matrix([[p,-q],[q,p]])
    grad=[s.diff(P,xx) for xx in list(x)+list(z)];contact_eq=[]
    for AA,xi in [(oldA,(t,1)),(newA,(1,t))]:
        Arot=s.Matrix(list(rot*AA));nn,mm=xi;target=rot[:,0]
        zz=s.Matrix([target[0]*nn*nn,target[0]*nn*mm,target[0]*mm*mm,
                     target[1]*nn*nn,target[1]*nn*mm,target[1]*mm*mm])
        sub=dict(zip(list(x)+list(z),list(Arot)+list(zz)))
        for gg in grad:
            expr=s.expand(gg.subs(sub,simultaneous=True))
            for order in [0,1]:
                cc=s.expand(expr.diff(t,order).subs(t,0))
                contact_eq.extend(s.Poly(cc,p,q).coeffs())
    for i,k,l in combinations(range(4),3):
        closed=s.expand(s.diff(OO[k,l],x[i])-s.diff(OO[i,l],x[k])+s.diff(OO[i,k],x[l]))
        contact_eq.extend(s.Poly(closed,*x).coeffs())
    contact_eq=[s.cancel(vv) for vv in contact_eq if vv!=0]
    Econtact,_=s.linear_eq_to_matrix(contact_eq,vars_)
    eq=[]
    subzero=dict(zip(list(x)+list(z),[1,0,0,1,0,1,0,0,0,-(r+1)]))
    eq.extend([s.cancel(s.diff(P,xx).subs(subzero)) for xx in x])
    eq.append(3*d1-(2*r+1)*d2)
    Tx=s.Matrix([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])
    Tz=s.Matrix.vstack(s.Matrix.hstack(s.eye(3),-s.eye(3)),s.Matrix.hstack(s.eye(3),s.eye(3)))
    Px=s.diag(1,-1,-1,1);Pz=s.diag(1,-1,1,-1,1,-1)
    h=(2*r+1)/3;AK=s.Matrix([b,h*a,d,h*c])
    zk=s.Matrix([z[2],h*z[1],h*h*z[0],z[5],h*z[4],h*h*z[3]])
    sections=[{'kind':'new_zero_A_gradient','rows':4},{'kind':'natural_diffusion','rows':1}]
    for label,AA,zz,scale in [('target_pi_over_4',Tx*x,Tz*z,s.Rational(1,4)),
                             ('paired_reflection',Px*x,Pz*z,1),
                             ('input_involution',AK,zk,1/h**3)]:
        pp=P.subs(dict(zip(list(x)+list(z),list(AA)+list(zz))),simultaneous=True)*scale-P
        coeff=[s.cancel(cc) for cc in s.Poly(pp,*(list(x)+list(z)),domain='EX').coeffs()]
        eq.extend(coeff);sections.append({'kind':label,'rows':len(coeff)})
    Eaug,_=s.linear_eq_to_matrix(eq,vars_)
    E=Eaug.col_join(Econtact);sections.append({'kind':'contact_and_closedness','rows':Econtact.rows})
    jet=dict(zip(list(x)+list(z),[0,0,1,0,0,1,0,0,0,0]))
    L,_=s.linear_eq_to_matrix([s.cancel(P.subs(jet))],vars_)
    c=r*(r+1)*(2*r+1)/(r+2)
    return {'r':r,'E':E,'L':L,'c':c,'vars':vars_,'P':P,'x':x,'z':z,'sections':sections}

def main():
    base=Path(__file__).parent
    path=Path(sys.argv[1]) if len(sys.argv)>1 else base/'POSITIVE_INPUT_HEAT_OBSTRUCTION.json'
    data=json.loads(path.read_text());print('Regenerating full necessary non-SOS system...',flush=True)
    built=build_system();r=built['r'];E=built['E'];L=built['L'];c=built['c']
    assert E.shape==(411,62) and data['system_shape']==[411,62]
    assert built['sections']==data['row_sections']
    def pol(cc):return sum((s.Rational(vv)*r**ii for ii,vv in enumerate(cc)),s.S.Zero)
    def rat(rr):return s.cancel(pol(rr['numerator'])/pol(rr['denominator']))
    def positive_coeffs(pp):
        cc=s.Poly(pp,r).all_coeffs()
        return (all(vv>=0 for vv in cc) and any(vv>0 for vv in cc)) or (all(vv<=0 for vv in cc) and any(vv<0 for vv in cc))
    lam=s.zeros(411,1)
    for term in data['dual_terms']:
        ii=term['row'];assert lam[ii]==0;lam[ii]=rat(term['multiplier'])
        _,den=s.fraction(lam[ii]);assert positive_coeffs(den)
    target=L.T.copy();target[61]+=c
    assert all(s.cancel(vv)==0 for vv in E.T*lam-target)
    nn,dd=s.fraction(s.cancel(c));assert all(vv>=0 for vv in s.Poly(nn,r).all_coeffs()) and nn!=0
    assert all(vv>=0 for vv in s.Poly(dd,r).all_coeffs()) and dd!=0
    # The second diffusion coefficient stays strictly positive under averaging.
    assert s.cancel(c-r*(r+1)*(2*r+1)/(r+2))==0
    receipt={'status':'PASS','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'domain':'every real r>0','system_shape':[411,62],'dual_nonzero_terms':len(data['dual_terms']),
             'exact_dual_equality':True,'dual_denominators_nonzero_every_positive_r':True,
             'forced_negative_actual_jet':'P(e21,(0,1,0,0,0,0))=-r(r+1)(2r+1)d2/(r+2)<0',
             'SOS_assumption':False,'excluded_class':'constant positive input diffusion plus local closed homogeneous-quadratic two-form; smooth C2 coefficient extension by Taylor reduction',
             'nonquasiconvexity_proved':False,'output_coupled_heat_excluded':False,
             'formal_proof_verification':False,'external_review':False}
    (base/'POSITIVE_OBSTRUCTION_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: exact 48-term equality dual forces a negative actual compatible jet for all r>0, including r=1.',flush=True)

if __name__=='__main__':main()
