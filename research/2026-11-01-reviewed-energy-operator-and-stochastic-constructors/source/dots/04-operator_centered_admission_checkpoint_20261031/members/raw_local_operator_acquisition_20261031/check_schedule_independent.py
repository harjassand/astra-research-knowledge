import copy,json
import receive_operator_schedule as r
import test_operator_schedule as t
import test_operator_certificate as core
checks=[]
def ck(n,b):assert b,n;checks.append(n)
s=t.fixture();rec=r.acquire(s)
def leaves(v,p=()):
    if type(v) is dict:
        for k,x in v.items():yield from leaves(x,p+(k,))
    elif type(v) is list:
        for k,x in enumerate(v):yield from leaves(x,p+(k,))
    elif type(v) is int:yield p,v
for p,v in leaves(rec):
    for val in (bool(v),float(v)):
        z=copy.deepcopy(rec);d=z
        for k in p[:-1]:d=d[k]
        d[p[-1]]=val
        ck('alias '+str(p)+str(type(val)),not r.verify_certificate(s,z))
# Adding the identical Pauli with opposite physical source matrix must NOT
# induce an invalid cancellation of its positive norm envelope.
z=copy.deepcopy(s); cp=copy.deepcopy(z['operator_spec']['couplings'][0]);cp['id']='negative copy'
import acquire_operator_certificate as a
cp['source_matrix']=a.encmat(-a.matrix(cp['source_matrix'],3));z['operator_spec']['couplings'].append(cp)
z['operator_certificate']=a.acquire(z['operator_spec']);rz=r.acquire(z)
ck('norm triangle not physical cancellation',rz['parameters']['coupling_c_upper']==[2,1])
# Removing all actual couplings leaves a valid zero-charge drift certificate;
# control-only receiving must not divide by zero.
z=copy.deepcopy(s);z['operator_spec']['couplings']=[];z['operator_certificate']=a.acquire(z['operator_spec']);rz=r.acquire(z)
ck('zero coupling direct branch',rz['parameters']['coupling_c_upper']==[0,1] and rz['status']=='PASS')
# Full-rank raw identity bypass remains refused despite a previously valid cert.
z=copy.deepcopy(s);z['operator_spec']['couplings'][0]['source_matrix']=a.encmat(__import__('sympy').eye(3))
ck('raw fullrank cannot bypass wrapper',not r.verify_admitted(z,rec))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'known-model composition, not hardware or gate backend'},indent=2))
