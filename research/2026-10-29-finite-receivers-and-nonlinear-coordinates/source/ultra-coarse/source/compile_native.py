"""Read the actual pinned kmcos RuO2 catalog; no fitted rates/generator.

This is an independent catalog consumer, not execution of kmcos/Fortran.
It preserves every process and periodic local condition/action. Primitive
mass/thermochemistry conventions are explicit in MODEL.json.
"""
import ast,configparser,hashlib,json,math,re,time
from pathlib import Path

HERE=Path(__file__).resolve().parent


def arithmetic(expr,env):
    t=ast.parse(expr,mode='eval')
    allowed=(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Add,ast.Sub,ast.Mult,ast.Div,
             ast.Pow,ast.USub,ast.UAdd,ast.Load,ast.Constant,ast.Name,ast.Call)
    assert all(isinstance(n,allowed) for n in ast.walk(t))
    assert all(not isinstance(n,ast.Call) or isinstance(n.func,ast.Name) and
               n.func.id in ('sqrt','exp') for n in ast.walk(t))
    return eval(compile(t,'catalog arithmetic','eval'),{'__builtins__':{}},env)


def main():
    tic=time.perf_counter()
    raw=(HERE/'source_entry/CO_oxidation.ini').read_text()
    cp=configparser.ConfigParser(interpolation=None);cp.optionxform=str;cp.read_string(raw)
    env=dict(pi=math.pi,h=6.62606957e-34,eV=1.602176565e-19,
             kboltzmann=1.3806488e-23,umass=1.660538921e-27,
             angstrom=1e-10,bar=1e5,sqrt=math.sqrt,exp=math.exp,
             m_CO=28.010,m_O2=31.998)
    # Source species.py uses G(T)=1000*(H(T)-H(0))-T*S(T), then
    # linearly interpolates G, NOT S and H separately.
    jmol=1.03642e-5
    co400=(1000*(2.976+8.671)-400*206.238)*jmol
    co500=(1000*(5.931+8.671)-500*212.831)*jmol
    mu0co=(co400+co500)/2
    mu0o=(1000*(4.543+8.683)-450*217.445)*jmol
    for sec in cp.sections():
        if sec.startswith('Parameter '):
            n=sec.split(' ',1)[1]
            env[n]=arithmetic(cp[sec]['value'],env)
    env.update(T=450.,p_COgas=1e-5,p_O2gas=1e-5)
    env['beta']=1/(env['kboltzmann']*env['T'])
    env['mu_COgas']=mu0co+8.6173324e-5*env['T']*math.log(env['p_COgas'])
    env['mu_O2gas']=mu0o+8.6173324e-5*env['T']*math.log(env['p_O2gas'])
    site={'bridge':0,'cus':1};sp={'empty':0,'CO':1,'O':2}
    processes=[]
    def parse(s):
        out=[]
        for z in s.split(' + '):
            m=re.fullmatch(r'(empty|CO|O)@(bridge|cus)(?:\.\(([-\d, ]+)\))?',z.strip())
            assert m,z
            off=(0,0,0) if m[3] is None else tuple(int(x) for x in m[3].split(','))
            assert off[2]==0
            out.append([site[m[2]],off[0],off[1],sp[m[1]]])
        return out
    for sec in cp.sections():
        if not sec.startswith('Process '):continue
        name=sec.split(' ',1)[1];v=cp[sec]
        group=1 if name.startswith('CO_adsorption') else 2 if name.startswith('O2_adsorption') else 0
        processes.append(dict(name=name,rate=arithmetic(v['rate_constant'],env),
                    group=group,conditions=parse(v['conditions']),actions=parse(v['actions']),
                    reaction=name.startswith('React_')))
    assert len(processes)==36
    # The actual native controls are adsorption-rate multipliers. In the
    # intended ideal-gas pressure model these equal pressure multipliers.
    # Source hardcoded kB/eV differs slightly from its CODATA ratio; keep
    # that tiny literal pressure/desorption discrepancy explicit, not hidden.
    d=1-env['eV']/env['kboltzmann']*8.6173324e-5
    nx=ny=4;M=2*nx*ny
    lco=nx*ny*sum(p['rate'] for p in processes if p['group']==1)
    lo=nx*ny*sum(p['rate'] for p in processes if p['group']==2)
    horizon=4/(lco+lo)
    des_bound=nx*ny*sum(p['rate'] for p in processes if 'desorption' in p['name'])
    # For pressure multipliers >=.8, |log a|<=1/4 and
    # |a**d-1|<=|d|/2 (since |d|/4<<1).
    pressure_bias=horizon*des_bound*abs(d)/2
    model=dict(catalog_sha256=hashlib.sha256(raw.encode()).hexdigest(),
       repository='kmcos/kmcos',revision='4442009d73032cbe39f8201370ad6d8927c7be4c',
       path='examples/CO_oxidation.ini',native_processes=processes,nx=nx,ny=ny,sites=M,
       T_kelvin=450,p_CO_bar=1e-5,p_O2_bar=1e-5,horizon_seconds=horizon,
       gas_activity_upper={'CO':lco,'O2':lo,'total_times_horizon':4},
       conventions={'mass_CO_amu':28.010,'mass_O2_amu':31.998,
          'mass_scope':'declared modern atomic-mass convention; upstream ASE dependency is unpinned',
          'NIST_source_urls':['https://janaf.nist.gov/tables/C-093.txt','https://janaf.nist.gov/tables/O-029.txt'],
          'NIST_rows_scope':'selected web-read thermochemical rows; direct NIST byte download returned403',
          'mu0_CO_eV':mu0co,'mu0_O2_eV':mu0o,'chemical_potential_rule':'literal pinned species.py interpolation and kB/eV constant'},
       intervention_scope='scale ONLY CO/O2 adsorption groups; genuine available computational process-rate intervention, not a measured physical pressure actuator',
       literal_pressure_desorption_exponent=d,
       literal_pressure_difference_TV_proposal=pressure_bias,
       literal_pressure_difference_scope='analytic coupling formula; float display, not a certified physical model-error bound',
       reset_scope='independent clean-surface starts in the computational consumer only; no experimental regeneration or stationary law granted',
       compile_seconds=time.perf_counter()-tic)
    (HERE/'MODEL.json').write_text(json.dumps(model,indent=2)+'\n')
    # Flatten all local events for the standalone C++ consumer.
    lines=[f'{nx} {ny} {len(processes)} {horizon:.17g}']
    for p in processes:
        assert len(p['conditions'])==len(p['actions'])<=2
        lines.append(f"{p['rate']:.17g} {p['group']} {int(p['reaction'])} {len(p['conditions'])}")
        for c,a in zip(p['conditions'],p['actions']):
            assert c[:3]==a[:3]
            lines.append(' '.join(map(str,c+a[3:])))
    (HERE/'NATIVE_INPUT.txt').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'processes':len(processes),'sites':M,'seconds':model['compile_seconds'],
           'horizon':horizon,'gas_activity':lco+lo,'pressure_discrepancy':pressure_bias}))


if __name__=='__main__':main()
