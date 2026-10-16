"""Independent formulas and measurements; no acquired code is executed."""
import math,json,hashlib,pathlib,openpyxl
root=pathlib.Path(__file__).parent
w=openpyxl.load_workbook(root/'final_Fig2.xlsx',read_only=True,data_only=True)
s=w['Figure 2 b']; X0,S0=[s.cell(10,c).value/100 for c in (3,4)];X1,S1=[s.cell(11,c).value/100 for c in (3,4)]
rho=(X1*(1/S1-1))/(X0*(1/S0-1));h=10.;d=.1;P=h+d;D=h-P*rho
out={'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.suffix in ['.xlsx','.pdf']},'final':{'rho':rho,'D_beta_zero':D,'net_ethylene_per_Ain':X1*(2-1/S1)},'preprint_rounded':{'rho':(.810*(1/.805-1))/(.808*(1/.477-1))},'countermodels':[]}
for mu in [.04,.01,.001,.00001,.0000001]:
 v=math.exp(-mu*h);L=-math.expm1(-mu*h)/mu;z=D/L
 if z>=1:continue
 u=(1-z)/(1-z*v);lam=-math.log(u)/d;q=u*v
 iso=(1-u)*L;cond=z*(-math.expm1(-mu*P))*L
 assert abs((h-z*L)/P-rho)<1e-14
 # Independent explicit pulse versus same-duration sham endpoints:
 before=z*v;executed=1-(1-before)*u;omitted=before*math.exp(-mu*d)
 assert abs((executed-omitted)*L-cond)<1e-12
 # Minimal equal-window recovery observable: recover mu and conditioning q.
 tau=100.;J0=z*(-math.expm1(-mu*tau))/mu;J1=J0*math.exp(-mu*tau)
 recovered=-math.log(J1/J0)/tau
 assert abs(recovered-mu)<1e-15
 out['countermodels'].append({'mu':mu,'lambda':lam,'z':z,'mean':(h-z*L)/P,'isolated_10s':iso,'conditioned_10s':cond,'conditioning_e_fold_cycles':-1/math.log(q),'positive_recovery_e_fold_s':1/mu,'recovery_mu_from_equal_windows':recovered})
(root/'independent_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
