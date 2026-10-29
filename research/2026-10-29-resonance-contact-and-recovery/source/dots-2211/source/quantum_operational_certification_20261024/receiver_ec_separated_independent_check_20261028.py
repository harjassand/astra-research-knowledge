from pathlib import Path
import json,hashlib
D=Path(__file__).parent
src=D/'contractive_syndrome_reuse_independent_check_20261028.py';ctx={'__file__':str(src)}
exec(compile(src.read_text().split('for t in range(1,9):')[0],str(src),'exec'),ctx)
globals().update({k:v for k,v in ctx.items() if not k.startswith('__')})
D=Path(__file__).parent
T=P;S=P;G=s.zeros(16);bound=s.Integer(0);g=s.Integer(0);rows=[];rho=s.Integer(1);last=None
for t in range(1,9):
 a=s.Rational(1,40+t);b=s.Rational(1,51+2*t)
 F=superop([rot(kron(Z,X),a)*k for k in reset]);N=superop([rot(kron(Z,X),b)])
 e=2*sn(a);n=2*sn(b);bt=(1-cos2(a)*cos2(b))/2
 oldS,oldG=S,G;T=clean(F*N*T);S=clean(P*T);G=clean(Q*T)
 assert eq(G,Q*(F-P)*N*(oldS+oldG))
 assert eq(P*F*N*oldG,P*(F-P)*N*oldG+P*(N-s.eye(16))*oldG)
 if t==1:rho=cos2(b)
 else:rho*=(cs(last)*cs(b)-sn(last)*sn(b))**2-(sn(last)*cs(b)+cs(last)*sn(b))**2
 err=(1-rho*cos2(a))/2
 assert eq(S,(1-err)*P+err*superop([kron(Z,I)])*P)
 bound+=bt+(n+e)*g/2;g=2*e*(1+g)
 assert err<=bound
 rows.append({'T':t,'true_half_diamond':float(err),'separated_bound':float(bound),'e':float(e),'n':float(n)});last=a
files=['receiver_ec_separated_reuse_20261028.md','receiver_ec_separated_independent_check_20261028.py',src.name]
out={'status':'PASS_EXACT_SEPARATED_COHERENT_FEEDBACK_RECURRENCE','rounds':rows,'sha256':{f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files}}
(D/'receiver_ec_separated_independent_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
