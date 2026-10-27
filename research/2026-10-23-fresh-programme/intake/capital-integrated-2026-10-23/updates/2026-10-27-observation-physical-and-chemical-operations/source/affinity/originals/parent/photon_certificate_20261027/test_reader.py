"""NONPHYSICAL deterministic software fixtures. No IID/Poisson source is claimed.

Positive output branch coverage is arithmetic only. These chosen fixtures do
not acquire the premises of their conditional statistical interpretation.
"""
import copy,hashlib,io,json,time,unittest
from fractions import Fraction as F
from pathlib import Path
import photon_certificate as pc
ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'header.example.json').read_text())
TINY=[json.loads(x) for x in (ROOT/'NONPHYSICAL_TINY.jsonl').read_text().splitlines()][1:]
EXPECTED=list(map(F,('0','-1/8','3/8','0','5/16','1/16','1/8','1/16')))

def lines(h,bs):
    yield (json.dumps(h,separators=(',',':'))+'\n').encode()
    for b in bs:yield (json.dumps(b,separators=(',',':'))+'\n').encode()

def result(h=None,bs=None):return pc.certify(lines(h or BASE,bs or TINY))

def empty_block(index):return {'kind':'block','index':index,**{k:[{'count':0,'phasors':[]},{'count':0,'phasors':[]}] for k in ('bright_a','bright_b','dark')}}

class ReaderTests(unittest.TestCase):
    def test_independent_tiny_features_and_unbiased_variance(self):
        f,_,totals,cut=pc.block(TINY[0],0,[4,4]);self.assertEqual(f,EXPECTED);self.assertEqual(totals,[4,4]);self.assertFalse(cut)
        z,_,totals,cut=pc.block(TINY[1],1,[4,4]);self.assertEqual(z,[0]*8);self.assertEqual(totals,[5,4]);self.assertTrue(cut)
        d=result();self.assertEqual(list(map(F,d['exact_sums'])),EXPECTED)
        self.assertEqual(list(map(F,d['exact_squared_sums'])),[v*v for v in EXPECTED])
        c=d['confidence_construction'];self.assertEqual(list(map(F,c['empirical_means'])),[v/2 for v in EXPECTED])
        self.assertEqual(list(map(F,c['unbiased_variances'])),[v*v/2 for v in EXPECTED])
        self.assertEqual(d['blocks']['clipped_whole'],1);self.assertEqual(d['confidence_lower'],'49/50')
        self.assertEqual(d['observed_max_block_counts_diagnostic_only'],[5,4]);self.assertFalse(d['observed_maxima_were_used_as_caps'])
        self.assertEqual(d['header']['lambda_on'],['1','1']);self.assertEqual(d['status'],'UNKNOWN')
    def test_channel_swap_and_conjugation(self):
        b=copy.deepcopy(TINY[0])
        for key in ('bright_a','bright_b','dark'):b[key].reverse()
        f=pc.block(b,0,[4,4])[0]
        self.assertEqual(f,[*EXPECTED[2:4],*EXPECTED[:2],EXPECTED[5],EXPECTED[4],EXPECTED[6],-EXPECTED[7]])
    def test_independent_channel_phase_cancels_in_product(self):
        b=copy.deepcopy(TINY[0]);phase=(F(3,5),F(4,5))
        # Direct independent rational rotation, not the reader's cmul.
        for key in ('bright_a','bright_b','dark'):
            for z in b[key][0]['phasors']:
                a,c=map(F,z);z[:]=[str(F(3,5)*a-F(4,5)*c),str(F(4,5)*a+F(3,5)*c)]
        f=pc.block(b,0,[4,4])[0]
        g=pc.affinity_geometry([(f[0],f[1]),(f[2],f[3])],[F(0)]*2,(f[6],f[7]),F(0),[f[4],f[5]],[F(0)]*2,32)
        # Hand oracle: original P=(1/8+i/16)*(i/8)*(3/8).
        self.assertEqual(F(g['geometry']['product_imaginary_abs']),F(3,512))
    def test_clipped_events_are_still_validated(self):
        b=copy.deepcopy(TINY);b[1]['dark'][0]['phasors'][1]=[2,0]
        with self.assertRaisesRegex(pc.InputError,'norm>1'):result(bs=b)
        b=copy.deepcopy(TINY);b[1]['dark'][0]['count']=3
        with self.assertRaisesRegex(pc.InputError,'count/phasor'):result(bs=b)
    def test_fixed_N_and_indices(self):
        bad=[TINY[:1],TINY+[empty_block(2)]]
        wrong=copy.deepcopy(TINY);wrong[1]['index']=0;bad.append(wrong)
        for bs in bad:
            with self.subTest(bs=len(bs)),self.assertRaises(pc.InputError):result(bs=bs)
        with self.assertRaises(pc.InputError):pc.certify(iter(list(lines(BASE,TINY))+[b'\n']))
        h=copy.deepcopy(BASE);h['N']=1
        with self.assertRaises(pc.InputError):result(h=h)
    def test_malformed_nonfinite_and_duplicate(self):
        encoded=json.dumps(BASE)
        with self.assertRaises(pc.InputError):pc.parse_json((encoded[:-1]+',"N":2}').encode(),'test')
        for token in (b'NaN',b'Infinity',b'-Infinity',b'0.5'):
            with self.assertRaises(pc.InputError):pc.parse_json(b'{"x":'+token+b'}','test')
        with self.assertRaises(pc.InputError):pc.parse_json(b'\xff','test')
        with self.assertRaises(pc.InputError):pc.parse_json(b'{','test')
        for value in ('NaN','Infinity','1/0',True):
            h=copy.deepcopy(BASE);h['eta']=value
            with self.subTest(value=value),self.assertRaises(pc.InputError):result(h=h)
    def test_budget_and_header_semantics(self):
        for change in ({'budget_scope':'PER_RECORD'},{'alpha_stat':'0'},{'alpha_stat':'1'},{'alpha_other_total':{'bad':'-1/2'}},{'alpha_other_total':{'bad':'1'}},{'cutoffs':[0,4]},{'lambda_on':['-1','1']},{'N':True}):
            h=copy.deepcopy(BASE);h.update(change)
            with self.subTest(change=change),self.assertRaises(pc.InputError):result(h=h)
        h=copy.deepcopy(BASE);h['analysis']['frequency_cycles_per_time']='NaN'
        with self.assertRaises(pc.InputError):result(h=h)
    def test_exact_sqrt_and_log_enclosures(self):
        vals=[F(0),F(1),F(2),F(2,3),F(10**100,7),F(1,10**100),F(1234567,987654321)]
        for x in vals:
            for bits in (1,8,32,64):
                lo,hi=pc.sqrt_bounds(x,bits);self.assertLessEqual(lo*lo,x);self.assertGreaterEqual(hi*hi,x)
                if x:self.assertGreater(lo,0)
        for x in (F(1),F(2),F(3200),F(32*10**9,7)):
            h=pc.log_upper(x);self.assertEqual(h.denominator,1);self.assertGreaterEqual(2**int(h),x)
            if h:self.assertLess(2**(int(h)-1),x)
    def test_independent_tail_oracle(self):
        # Read-only external TEST oracle. The inference module never reads it.
        oracle=ROOT/'TEST_ONLY_POISSON_ORACLE.json';d=json.loads(oracle.read_text())
        tails,_=pc.poisson_tails(F(80),144)
        for k in (143,144,145):self.assertGreaterEqual(tails[k],F(d['tail_intervals'][str(k)]['upper']))
        h=copy.deepcopy(BASE);h['cutoffs']=[144,144];h['lambda_on']=['40','40'];h['lambda_dark']=['0','0']
        tm,td,to,_=pc.bias_bounds(h);ours=[tm[0],td[0],to]
        for got,needed in zip(ours,d['K144_upper_mean_diag_cross_bias']):self.assertGreaterEqual(got,F(needed))
        zero,_=pc.poisson_tails(F(0),1);self.assertEqual(zero,{2:F(0),1:F(0),0:F(1)})
        loose,_=pc.poisson_tails(F(10),1);self.assertEqual(loose,{2:F(1),1:F(1),0:F(1)})
    def test_UNKNOWN_and_inconsistent_geometry(self):
        d=result(bs=[empty_block(0),empty_block(1)]);self.assertEqual(d['status'],'UNKNOWN');self.assertIsNone(d['affinity_lower'])
        d=pc.affinity_geometry([(F(1),F(0))]*2,[F(0)]*2,(F(0),F(2)),F(0),[F(1)]*2,[F(0)]*2,32)
        self.assertEqual(d['status'],'UNKNOWN');self.assertIn('inconsistent_radius_squared_ge_one',d['reasons'])
    def test_deterministic_NONPHYSICAL_positive_software_path(self):
        h=copy.deepcopy(BASE);h['N']=4096;h['cutoffs']=[2,2];h['lambda_on']=['1/200','1/200'];h['lambda_dark']=['0','0']
        def blocks():
            for i in range(h['N']):
                b=empty_block(i);b['bright_a']=[{'count':1,'phasors':[[1,0]]},{'count':1,'phasors':[[0,1]]}];b['bright_b'][1]={'count':1,'phasors':[[1,0]]};yield b
        d=pc.certify(lines(h,blocks()));self.assertEqual(d['status'],'CONDITIONAL_LOWER_BOUND')
        self.assertEqual(d['data_kind'],'NONPHYSICAL_SOFTWARE_TEST');self.assertFalse(d['physical_experiment_acquired_or_qualified']);self.assertFalse(d['precommitment_verified'])
        r2=F(d['radius_squared_lower']);A2=F(d['affinity_squared_lower']);lo=F(d['affinity_lower'])
        self.assertTrue(0<r2<1);self.assertEqual(A2,36*r2/(1-r2));self.assertTrue(0<lo and lo*lo<=A2)
        (ROOT/'NONPHYSICAL_POSITIVE_SOFTWARE_RESULT.json').write_text(json.dumps(d,indent=2)+'\n')
    def test_API_EOF_sentinel_and_malformed_text(self):
        valid=list(lines(BASE,TINY))
        for entries in ([*valid,None,json.dumps(empty_block(2)).encode()],
                        [valid[0],None,*valid[1:]], [None,*valid], [*valid,7]):
            with self.subTest(entries=len(entries)),self.assertRaises(pc.InputError):pc.certify(iter(entries))
        with self.assertRaises(pc.InputError):pc.certify(iter(["\ud800"]))
    def test_input_digest(self):
        data=b''.join(lines(BASE,TINY));d=pc.certify(io.BytesIO(data))
        self.assertEqual(d['received_stream_sha256'],hashlib.sha256(data).hexdigest());self.assertEqual(d['received_bytes'],len(data))

if __name__=='__main__':unittest.main()
