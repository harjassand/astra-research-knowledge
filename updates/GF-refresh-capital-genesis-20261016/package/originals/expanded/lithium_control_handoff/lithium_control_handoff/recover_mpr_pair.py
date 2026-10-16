"""Narrow independent MPR reader. No acquired code imported/executed.
Layout cross-reference: echemdata/galvani BioLogic.py. New v0 IDs are u16
at byte6 (not the reference parser's lossy odd-byte slicing).
"""
from pathlib import Path
import struct,json,hashlib
import numpy as np
import openpyxl
ROOT=Path(__file__).resolve().parent
BASE=ROOT/'figure 04/analysis/EC-LAB/pulsed for ultralow conc/LFPC-duo-pulased'
FILES={'CC':'Ch1-20251103-LFPC-duo-179,6mg, non-pulsed method_C01.mpr','P4-8':'Ch1-20251107-LFPC-duo-179,6mg, pulsed method-4s discharge 8s rest_C01.mpr'}
DT=np.dtype([('flags','u1'),('Ns','<u2'),('time_s','<f8'),('dq_mAh','<f8'),('Q_mAh','<f8'),('control','<f4'),('Ewe_V','<f4'),('range','<u2'),('Qcharge_discharge_mAh','<f8'),('halfcycle','<u4')])
def parse(p):
 d=p.read_bytes();assert d.startswith(b'BIO-LOGIC MODULAR FILE\x1a');pos=52
 while pos<len(d):
  assert d[pos:pos+6]==b'MODULE';h=pos+6
  assert d[h+35:h+39]==b'\xff'*4
  length,version=struct.unpack_from('<II',d,h+39);x=d[h+59:h+59+length]
  if d[h:h+10]==b'VMP data  ':
   n,nc=struct.unpack_from('<IB',x);ids=struct.unpack_from('<'+str(nc)+'H',x,6)
   assert version==0 and ids==(1,2,3,21,31,65,131,4,7,13,5,6,39,467,468)
   assert len(x)==1007+n*DT.itemsize
   a=np.frombuffer(x,DT,offset=1007).copy()
  pos=h+59+length
 return a
if __name__=='__main__':
 for label,name in FILES.items():
  a=parse(BASE/name);print(label,a.dtype,len(a));print(a[:10]);print('END',a[-6:]);print('Ns',np.unique(a['Ns'],return_counts=True));print('modes',np.unique(a['flags']&3,return_counts=True))
  np.savetxt(ROOT/(label+'_decoded.csv'),np.column_stack([a[n] for n in a.dtype.names]),delimiter=',',header=','.join(a.dtype.names),comments='')
