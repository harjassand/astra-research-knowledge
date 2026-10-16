"""Original harmless synthetic byte streams; no pickle serializer/deserializer."""
import pathlib, sys, unittest, json, struct
from unittest import mock
import safe_reader as r
BASE=pathlib.Path('/workspace/shared/stm_control_logs')
NAMES=('00000.npy','01500.npy','02920.npy')
def stream(body):return b'\x80\x03'+body+b'.'
def global_(name):return b'c'+name.replace(' ','\n').encode()+b'\n'
def dtype(dt='f8',endian='<'):
    g=r.Node('global','numpy dtype');n=r.Node('reduce',(g,(dt,False,True)));n.state=(3,endian,None,None,None,-1,-1,63 if dt=='O8' else 0);return n
def array(shape=(1,),data=struct.pack('<d',2.0),dt=None):
    n=r.Node('reduce',(r.Node('global','numpy.core.multiarray _reconstruct'),(r.Node('global','numpy ndarray'),(0,),b'b')));n.state=(1,shape,dt or dtype(),False,data);return n
class Tests(unittest.TestCase):
    def test_inert_known_reduce(self):
        # A known GLOBAL with invalid arguments must be rejected, never called.
        with mock.patch('builtins.__import__',side_effect=AssertionError('import attempted')):
            with self.assertRaises(r.ReaderError):r.parse_pickle(stream(global_('numpy.core.multiarray scalar')+b')R'))
    def test_unknown_callback(self):
        with mock.patch('os.system',side_effect=AssertionError('callback invoked')):
            with self.assertRaises(r.ReaderError):r.parse_pickle(stream(global_('os system')+b')R'))
    def test_memo_identity(self):
        v=r.parse_pickle(stream(b']q\x00(]q\x01h\x01e'));self.assertIs(v[0],v[1])
    def test_cycle(self):
        with self.assertRaisesRegex(r.ReaderError,'Cyclic'):r.parse_pickle(stream(b']q\x00h\x00a'))
    def test_malformed_streams(self):
        for body in [b'R',b'\x93',b'Pbad\n',b'h\x00',b'j\xff\xff\xff\xff',b']q\x00q\x00',b'}(K\x01K\x02u',b'}(X\x01\x00\x00\x00ku',b'K\x01K\x02',b']b',b'\x80\x03N']:
            with self.subTest(body=body),self.assertRaises(r.ReaderError):r.parse_pickle(stream(body))
    def test_trailing_and_protocol(self):
        for b in [stream(b'N')+b'junk',b'\x80\x04N.',b'N.']:
            with self.assertRaises(r.ReaderError):r.parse_pickle(b)
    def test_bounds(self):
        for name,limit,payload in [('MAX_OPS',2,stream(b'NN')),('MAX_MEMO',1,stream(b']q\x01')),('MAX_STACK',1,stream(b'NN')),('MAX_ITEMS',1,stream(b'](NNe')),('MAX_DEPTH',2,stream(b'(((Nttt'))]:
            with self.subTest(name=name),mock.patch.object(r,name,limit),self.assertRaises(r.ReaderError):r.parse_pickle(payload)
        with mock.patch.object(r,'MAX_FILE',2),self.assertRaises(r.ReaderError):r.parse_pickle(stream(b'N'))
    def test_deep_graph(self):
        with self.assertRaises(r.ReaderError):r.parse_pickle(stream(b'N'+b'\x85'*70))
    def test_alias_depth(self):
        x=[];root=[x]
        for _ in range(65):x=[x]
        root.append(x)
        with self.assertRaises(r.ReaderError):r.validate(root)
    def test_dtype_array_guards(self):
        bad=[array(dt=dtype('i8')),array(dt=dtype('f8','>')),array(shape=(2,)),array(shape=(r.MAX_ARRAY+1,)),array(shape=(True,)),array(data=struct.pack('<d',float('nan'))),array(dt=dtype('b1','|'),data=b'\x02'),array(shape=(1,)*9),array(shape=(0,),data=b'x'),array(dt=dtype('O8','|'),data=[{}])]
        for x in bad:
            with self.subTest(x=x.state[:3]),self.assertRaises(r.ReaderError):r.validate(x)
    def test_header_guards(self):
        for h in [b"{'descr':'|O','shape':(1,),'fortran_order':False}",b"{'descr':'<f8','shape':(),'fortran_order':False}",b"__import__('os')",b"{}"]:
            with self.assertRaises(r.ReaderError):r.parse_bytes(b'\x93NUMPY\x01\x00'+len(h).to_bytes(2,'little')+h+stream(b'N'))
    def test_three_diagnostics_match_old_summary(self):
        old=json.loads((BASE/'sample_decoded_summary.json').read_text());self.assertEqual(set(old),set(NAMES))
        for name in NAMES:
            p=BASE/'acquired/training_data_and_model_parameters/training_data'/name
            root=r.parse(p);self.assertEqual(json.loads(json.dumps(r.decode(root))),old[name])
            d=root.state[4][0];prev=d['episode_start_info']
            for info in d['transitions']['info']:
                curr=info['img_info'];self.assertIs(curr['img_forward'],curr['img_forward']);prev=curr
            self.assertIs(d['episode_end_info']['img_forward'],prev['img_forward'])
if __name__=='__main__':unittest.main(verbosity=2)
