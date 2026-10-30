"""Replay assigned scientific artifacts without modifying their source copies."""
import sys
sys.dont_write_bytecode = True
import importlib.util
from pathlib import Path
from contextlib import redirect_stdout
import json

BASE = Path('producer-workspace/control')
OUT = Path(__file__).resolve().parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def replay(name, fn):
    with (OUT / (name + '.txt')).open('w') as stream, redirect_stdout(stream):
        fn()
    print(name + ': PASS', flush=True)

def b1_checkpoint():
    m = load('check_construction', BASE/'block1/checkpoint/check_construction.py')
    m.exact_certificate()
    s = load('b1_checkpoint_schedule', BASE/'block1/checkpoint/schedule.py')
    s.display(s.make_plan('0.1'))
replay('block1_checkpoint', b1_checkpoint)

def b1_7144():
    m = load('b1_7144_checks', BASE/'block1/result_7144d77/checks.py')
    m.exact_word_checks(); m.moment_certificate(); m.constructive_upper_bound()
    s = load('b1_7144_schedule', BASE/'block1/result_7144d77/phase_schedule.py')
    s.display(s.make_plan('0.01'))
replay('block1_7144d77', b1_7144)

def b1_bc():
    # Its archived parent-relative helper path no longer resolves. Inject only
    # the helper from the explicitly assigned checkpoint; do not follow paths
    # into any original run or unrelated source tree.
    m = load('b1_bc_checks', BASE/'block1/result_bc63f86/check_barrier.py')
    w = m.degree_five_word(); m.exact_word_certificate(w)
    p = m.profiles(w); m.exact_noise_commutant(); m.diagnostic(w,p)
replay('block1_bc63f86', b1_bc)

def b1_ea():
    s = load('schedule', BASE/'block1/result_ea8db7e/schedule.py')
    m = load('b1_ea_checks', BASE/'block1/result_ea8db7e/check.py')
    print(json.dumps({'exact':m.exact_cycle_certificate(),
                      'scalar':m.scalar_diagnostics(),
                      'resources':s.resources()}, indent=2))
replay('block1_ea8db7e', b1_ea)

def b2_807():
    load('pauli_series', BASE/'block2/result_80767e8/pauli_series.py')
    m = load('b2_807_exact', BASE/'block2/result_80767e8/high_order_barrier.py')
    m.main()
    n = load('b2_807_moments', BASE/'block2/result_80767e8/macro_moment_barrier.py')
    n.main()
replay('block2_80767e8', b2_807)

def b2_969_safe():
    m = load('exact_degree5', BASE/'block2/result_969cae3/exact_degree5.py')
    m.D = OUT
    m.main()
    p = BASE/'block2/result_969cae3/finite_certificate.py'
    source = p.read_text().replace('D=Path(__file__).resolve().parent', 'D=Path('+repr(str(OUT))+')')
    exec(compile(source, str(p), 'exec'), {'__file__':str(p),'__name__':'review_finite_certificate'})
    c = load('b2_969_channel', BASE/'block2/result_969cae3/channel_checks.py')
    c.D = OUT
    c.main()
replay('block2_969cae3', b2_969_safe)

def b2_d97():
    m = load('b2_d97_checks', BASE/'block2/result_d97a506/check_barrier.py')
    result = m.exact_checks()
    # Exact certificates are the proof-bearing artifacts. Long floating-point
    # powers with known drift are deliberately unnecessary for this replay.
    result = {k:v for k,v in result.items() if k not in ('profile','bath_h')}
    print(json.dumps(result, indent=2))
replay('block2_d97a506', b2_d97)
