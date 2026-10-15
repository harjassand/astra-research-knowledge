"""Small exact checks for the separate non-strict critical-storage note.
No full heat-Gram replay and no analytic formalization is claimed.
"""
from pathlib import Path
import hashlib,json
import sympy as S

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
WORK=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-direction-transport-20261015')
CERT=ROOT/'workers/nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json'
data=json.loads(CERT.read_text())
records=[]


def zero(expr):
    assert S.expand(expr)==0,expr


def passed(name,**details):
    records.append(dict(name=name,status='PASS',**details))
    print('PASS:',name,flush=True)


a,b,c,d=S.symbols('a b c d',real=True)
z=[a,b,c,d]
omega=S.zeros(4)
mon=data['quadratic_coefficient_order']
for (i,j),row in zip(data['omega_pair_order'],data['omega_coefficients']):
    val=sum(S.Rational(co)*z[p]*z[q]for co,(p,q)in zip(row,mon))
    omega[i,j]=val
    omega[j,i]=-val
alpha=S.Matrix([sum(z[j]*omega[j,i]for j in range(4))/4 for i in range(4)])
for i in range(4):
    for j in range(i+1,4):
        zero(S.diff(alpha[j],z[i])-S.diff(alpha[i],z[j])-omega[i,j])
passed('actual rational heat form has the stated global primitive')

restriction=S.expand(omega[0,2].subs({b:0,d:0}))
zero(restriction-(S.Rational(788811,20000)*a*a+S.Rational(98601,2500)*c*c))
y=S.symbols('y',real=True)
loop=S.Matrix([S.cos(y),0,S.sin(y),0])
line=(alpha.subs(dict(zip(z,list(loop))),simultaneous=True)).dot(loop.diff(y))
value=S.simplify(S.integrate(S.expand_trig(line),(y,0,2*S.pi))/(2*S.pi))
assert value==S.Rational(1577619,160000)
loop_reverse=S.Matrix([S.cos(y),0,-S.sin(y),0])
reverse_line=alpha.subs(dict(zip(z,list(loop_reverse))),simultaneous=True).dot(loop_reverse.diff(y))
reverse_value=S.simplify(S.integrate(S.expand_trig(reverse_line),(y,0,2*S.pi))/(2*S.pi))
assert reverse_value==-value
assert alpha.subs({a:0,b:0,c:0,d:0})==S.zeros(4,1)
passed('same-zero-profile normal jets have distinct gauge-invariant circulations',
       positive=str(value),zero='0',negative=str(reverse_value))

u=a*a+c*c
v=b*b+d*d
j=a*d-b*c
G=3*(u+v-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
t,eps=S.symbols('t epsilon',real=True)
line_G=S.expand(G.subs({a:1,b:t,c:0,d:1}))
line_H=(2+t*t)**2
zero(line_G-(-S.Rational(1,24)+3*t**4))
zero(S.diff(line_G-eps*line_H,t,2).subs(t,0)+8*eps)
passed('positive strict bulk subtraction is excluded by exact acoustic zero')

r=S.symbols('r',real=True)
unit=S.integrate((1+r*r)**2,(r,0,1))
double=2*S.integrate((S.Rational(1,4)+r*r)**2,(r,0,1))
assert unit==S.Rational(28,15)
assert double==S.Rational(103,120)<unit
passed('fixed-return action bound need not be a dominating storage',
       unit_return=str(unit),double_width_return=str(double))

frozen=OUT/'WORKER_MANIFEST.json'
manifest=json.loads(frozen.read_text())
for name,record in manifest['files'].items():
    actual=hashlib.sha256((OUT/name).read_bytes()).hexdigest()
    assert actual==record['sha256'],(name,actual,record['sha256'])
sources=[CERT,
    WORK/'updates/FR-capital-mining-20261015/synthesis/external_machinery/HEAT_TO_CRITICAL_TRACE.md',
    ROOT/'root/G_HEAT_IMPLICATION_AND_COMPATIBILITY.md',
    ROOT/'workers/adversarial_operation/G_HEAT_REVIEW.md',
    ROOT/'workers/nonlinear_qc/G_QUASICONVEXITY_PROOF.md']
local=[OUT/'G_CRITICAL_STORAGE_SCOPE.md',Path(__file__).resolve()]
receipt={'status':'PASS','groups':len(records),'records':records,
    'source_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in sources},
    'local_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in local},
    'read_scopes':{'FR HEAT_TO_CRITICAL_TRACE.md':'lines1-245, especially37-215',
                   'root G_HEAT_IMPLICATION_AND_COMPATIBILITY.md':'full',
                   'adversarial G_HEAT_REVIEW.md':'full',
                   'G_EXACT_HEAT_CERTIFICATE.json':'ordering and omega coefficient fields, then primitive reconstruction only',
                   'G_QUASICONVEXITY_PROOF.md':'lines45-132'},
    'frozen_manifest_sha256':hashlib.sha256(frozen.read_bytes()).hexdigest(),
    'frozen_inventory_unchanged':True,
    'analytic_scope':'new finite required-supply and short-connector continuity proofs not formalized by these checks',
    'heat_scope':'uses supplied independently reconstructed all-background QC premise; no full heat-Gram replay here',
    'historical_novelty':'UNKNOWN','external_correctness':'UNKNOWN'}
(OUT/'G_CRITICAL_STORAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'{len(records)} exact check groups passed; frozen inventory unchanged.',flush=True)
