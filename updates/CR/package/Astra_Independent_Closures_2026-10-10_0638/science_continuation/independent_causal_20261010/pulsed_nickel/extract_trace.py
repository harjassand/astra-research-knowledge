import zipfile,xml.etree.ElementTree as ET,json,sys
from pathlib import Path
from io import BytesIO
import numpy as np
p=Path(__file__).parent
ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z=zipfile.ZipFile(p/'DataCat.zip'); x=zipfile.ZipFile(BytesIO(z.read('DataCat/All Electrolysis traces.xlsx')))
for sn in [int(v) for v in sys.argv[1:]]:
 rows=[]
 for _,el in ET.iterparse(x.open(f'xl/worksheets/sheet{sn}.xml'),events=('end',)):
  if el.tag !=ns+'row':continue
  r=np.full(6,np.nan)
  for c in el.findall(ns+'c'):
   v=c.find(ns+'v')
   if v is not None and c.attrib.get('t','n')=='n':
    col=''.join(k for k in c.attrib['r'] if k.isalpha());ix=0
    for k in col:ix=ix*26+ord(k)-64
    if ix<=6:
     try:r[ix-1]=float(v.text)
     except:pass
  rows.append(r);el.clear()
 a=np.array(rows);np.save(p/f'trace_sheet{sn}.npy',a)
 print('sheet',sn,a.shape)
 print(a[:8]);print(a[-4:])
