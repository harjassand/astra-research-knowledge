import unittest, json, math
from fractions import Fraction as F
from unittest.mock import patch
from pathlib import Path
from certified_clock import *

ROOT=Path(__file__).resolve().parent

def independent_log_bounds(num,den,terms=95):
    # Independent exact-Fraction series; no fixed-point helper is reused.
    assert 1<=F(num,den)<=2
    z=F(num-den,num+den)
    ans=2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)),F())
    tail=2*z**(2*terms+1)/F(2*terms+1)/(1-z*z)
    return ans,ans+tail

def negative_log_bounds(num,den):
    e=den.bit_length()-num.bit_length()
    if num*(1<<e)<den:e+=1
    lo,hi=independent_log_bounds(num*(1<<e),den)
    l2,h2=independent_log_bounds(2,1)
    return e*l2-hi,e*h2-lo

def solve(A,b):
    A=[list(row)+[y] for row,y in zip(A,b)];n=len(b)
    for i in range(n):
        k=next(k for k in range(i,n) if A[k][i]);A[i],A[k]=A[k],A[i]
        z=A[i][i];A[i]=[x/z for x in A[i]]
        for j in range(n):
            if j!=i:
                z=A[j][i];A[j]=[x-z*y for x,y in zip(A[j],A[i])]
    return [r[-1] for r in A]

class CertifiedClockTests(unittest.TestCase):
    def setUp(self):self.B=default_budget()
    def test_exact_budget(self):
        B=self.B;r=B.report()
        self.assertEqual(B.q,F(1,65536));self.assertEqual(B.R,(4800,6900,8100,8775))
        self.assertEqual(B.b,94);self.assertEqual(B.P,126)
        self.assertLess(F(r['failure_bounds']['total']),B.delta)
        self.assertLess(F(r['failure_bounds']['total']),self.B.delta/4)
    def test_independent_exact_log_enclosures(self):
        B=self.B;c=ExpCells(B);D=1<<B.b
        first=ceil(B.a*D);last=((1-B.a)*D).numerator//((1-B.a)*D).denominator-1
        ks=[first,first+1,D//8,D//4,D//3,D//2,D//2+1,3*D//4,last-1,last]
        for k in ks:
            point,lo,hi=c.cell_from_integer(k)
            # All ideal U in [k/D,(k+1)/D] are covered.
            elo,_=negative_log_bounds(k+1,D);_,ehi=negative_log_bounds(k,D)
            self.assertLessEqual(F(lo,c.F),elo)
            self.assertGreaterEqual(F(hi,c.F),ehi)
            self.assertLessEqual(lo,point);self.assertLessEqual(point,hi)
    def test_invalid_inputs_rejected(self):
        bad=[((.125,'1/16'),(1,2)),(('0','1/2'),(1,2)),(('1','1/2'),(1,2)),(('1/2','1/2'),(0,2)),(('1/3','1/2'),(1,2)),(('1/2',),(1,2))]
        for p,r in bad:
            with self.assertRaises((TypeError,ValueError)):Budget(p,r)
    def test_injected_bit_source_and_contract(self):
        bank=BitCallbackBank(lambda label: lambda k: 0)
        r=acquire(self.B,tape_bank=bank)
        self.assertEqual(r['failure'],'uniform_endpoint')
        self.assertEqual(r['execution_source'],'caller-supplied bit callbacks')
        with self.assertRaises(ValueError):BitCallbackTape(lambda k:1<<k).getbits(3)
        with self.assertRaises(ValueError):acquire(self.B)
        with self.assertRaises(ValueError):acquire(self.B,tape_bank=bank,reference=True)
    def test_sort_keeps_pairs(self):
        B=Budget(('1/16','1/8'),('2','1'))
        self.assertEqual(B.p,(F(1,8),F(1,16)))
    def test_endpoint_cells_fail_closed(self):
        c=ExpCells(self.B)
        for k in [0,(1<<self.B.b)-1]:
            with self.assertRaisesRegex(AcquisitionFailure,'uniform_endpoint'):c.cell_from_integer(k)
        with patch.object(CounterTape,'getbits',return_value=0):
            r=acquire(self.B,'forced-endpoint')
        self.assertEqual(r['output'],'0');self.assertEqual(r['failure'],'uniform_endpoint')
    def test_ambiguous_poisson_not_guessed(self):
        class Stub:
            def draw(self,tape):return 15,10,20
        with self.assertRaisesRegex(AcquisitionFailure,'ambiguity'):poisson_count(Stub(),None,F(15),F(16),5)
    def test_count_cap_not_ignored(self):
        class Stub:
            def draw(self,tape):return 1,1,1
        with self.assertRaisesRegex(AcquisitionFailure,'cap'):poisson_count(Stub(),None,F(100),F(100),5)
    def test_zero_atom_preserved_on_certified_tape(self):
        B=self.B;D=1<<B.b;k=D-ceil(B.a*D)-2
        def bits(tape,count):return k if tape.key.endswith(b'\x00W') else D//2
        with patch.object(CounterTape,'getbits',bits):r=acquire(B,'forced-zero',reference=True)
        self.assertIsNone(r['failure']);self.assertEqual(r['output'],'0')
        self.assertEqual(r['same_tape_reference']['exact_H_interval'],['0','0'])
        self.assertTrue(r['same_tape_reference']['within_requested_epsilon_for_every_tape_extension'])
    def test_mismatched_reference_evidence_rejected(self):
        B=self.B;D=1<<B.b;k=D-ceil(B.a*D)-2
        def bits(tape,count):return k if tape.key.endswith(b'\x00W') else D//2
        class BadBank(TapeBank):
            def evidence(self):
                x=super().evidence()
                if '0/exact_marks' in x:x['0/exact_marks']['generated_block_sha256']='deliberate mismatch'
                return x
        with patch.object(CounterTape,'getbits',bits):
            with self.assertRaisesRegex(ValueError,'replay evidence mismatch'):
                acquire(B,tape_bank=TapeBank('same'),reference=True,reference_tape_bank=BadBank('same'))
    def test_recorded_replay_and_small_stream_identity(self):
        old=json.loads((ROOT/'REPLAY_RESULTS.json').read_text())['run'];r=acquire(self.B,old['seed'])
        for k in ('output','failure','strata','main_exponential_cells','main_bits','main_tape_evidence'):self.assertEqual(r[k],old[k])
        self.assertTrue(any(s['branch']=='compressed' for s in old['strata']))
        ref=old['same_tape_reference'];self.assertTrue(ref['within_requested_epsilon_for_every_tape_extension'])
        for s in old['strata']:
            if s['branch']=='small':
                for role in ('arrivals','exact_marks'):
                    label=f"{s['index']}/{role}"
                    self.assertEqual(old['main_tape_evidence'][label],ref['tape_evidence'][label])
    def test_extreme_rarity_replay_stays_bounded(self):
        doc=json.loads((ROOT/'EXTREME_RARITY_RESULTS.json').read_text());old=doc['run']
        B=Budget((F(1,1<<50),)*4,(1,2,4,8));r=acquire(B,old['seed'])
        self.assertEqual(B.q,F(1,1<<200));self.assertEqual(r['output'],old['output'])
        self.assertEqual(r['main_exponential_cells'],29401)
        self.assertTrue(all(s['branch']=='compressed' for s in r['strata']))
        self.assertNotIn('same_tape_reference',r)
    def test_display_overflow_does_not_break_exact_output(self):
        B=Budget((F(1,1<<2000),),(1,));r=acquire(B,'audit-overflow-display')
        self.assertIsNone(r['failure']);self.assertIsNone(r['output_float_display_only'])
        self.assertGreater(F(r['output']),F(1<<1024))
    def test_decimal_conversion_limit_uses_exact_hex(self):
        B=Budget((F(1,1<<20000),),(1,));r=acquire(B,'audit-hex-output')
        self.assertIsNone(r['failure']);self.assertTrue(r['output'].startswith('0x'))
        self.assertGreater(exact_fraction(r['output']),F(1<<19000))
        self.assertEqual(exact_fraction(rational_text(B.q)),B.q)
    def test_os_prefix_exact_replay(self):
        old=json.loads((ROOT/'OS_ACQUISITION_RESULTS.json').read_text())['run']
        r=acquire(self.B,tape_bank=PrefixReplayBank(ROOT/'OS_PREFIX'))
        for k in ('output','failure','strata','main_exponential_cells','main_bits','main_tape_evidence'):
            self.assertEqual(r[k],old[k])
        self.assertEqual(r['main_exponential_cells'],14769)
    def test_os_prefix_tamper_and_exhaustion_rejected(self):
        import tempfile
        manifest=json.loads((ROOT/'OS_PREFIX'/'manifest.json').read_text())
        row=manifest['streams']['W'];data=bytearray((ROOT/'OS_PREFIX'/row['file']).read_bytes());data[0]^=1
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d);(directory/'manifest.json').write_text(json.dumps(manifest))
            (directory/row['file']).write_bytes(data)
            with self.assertRaisesRegex(ValueError,'hash mismatch'):PrefixReplayBank(directory).stream('W')
        with self.assertRaisesRegex(ValueError,'exceeds recorded'):
            PrefixReplayTape('x',b'0'*32,1).getbits(2)
    def test_brown_laplace_matches_exact_killed_generator(self):
        B=self.B;n=B.n;N=1<<n;Q=[[F() for _ in range(N)] for _ in range(N)]
        pi=[]
        for x in range(N):
            pi.append(math.prod(1-B.p[i] if (x>>i)&1 else B.p[i] for i in range(n)))
            for i in range(n):
                rate=B.rates[i]*(B.p[i] if (x>>i)&1 else 1-B.p[i]);Q[x][x^(1<<i)]+=rate;Q[x][x]-=rate
        for s in [F(1,16),F(1),F(16)]:
            A=[[(s if x==y else 0)-Q[x][y] for y in range(1,N)] for x in range(1,N)]
            f=solve(A,[Q[x][0] for x in range(1,N)])
            chain=pi[0]+sum((pi[x]*f[x-1] for x in range(1,N)),F())
            R=F()
            for mask in range(1,N):
                prob=math.prod(1-B.p[i] if (mask>>i)&1 else B.p[i] for i in range(n))
                rate=sum((B.rates[i] for i in range(n) if (mask>>i)&1),F())
                R+=prob/(s+rate)
            self.assertEqual(chain,B.q/(B.q+s*R))

if __name__=='__main__':unittest.main(verbosity=2)
