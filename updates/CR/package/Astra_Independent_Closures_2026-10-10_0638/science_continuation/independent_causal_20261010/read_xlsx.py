import zipfile,xml.etree.ElementTree as E
from io import BytesIO
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def parse(b):
 x=zipfile.ZipFile(BytesIO(b));ss=[]
 if 'xl/sharedStrings.xml' in x.namelist():
  ss=[''.join(t.text or '' for t in si.findall('.//m:t',ns)) for si in E.fromstring(x.read('xl/sharedStrings.xml')).findall('m:si',ns)]
 result={}
 for s in x.namelist():
  if s.startswith('xl/worksheets/sheet') and s.endswith('.xml'):
   rows=[]
   for row in E.fromstring(x.read(s)).findall('.//m:row',ns):
    d={}
    for c in row.findall('m:c',ns):
     v=c.find('m:v',ns)
     val=v.text if v is not None else None
     if val is not None and c.attrib.get('t')=='s':val=ss[int(val)]
     elif c.attrib.get('t')=='inlineStr':val=''.join(n.text or '' for n in c.findall('.//m:t',ns))
     if val is not None:d[c.attrib['r']]=val
    rows.append(d)
   result[s]=rows
 return result
if __name__=='__main__':
 from pathlib import Path
 p=Path(__file__).parent;z=zipfile.ZipFile(p/'raw_data.zip')
 for n in ['Data Files for Figshare/Excel/Manuscript/Fig. 2.xlsx','Data Files for Figshare/Excel/Manuscript/Fig. 1(b).xlsx']:
  print(n)
  for s,rs in parse(z.read(n)).items():
   print(s)
   for row in rs[:15]:print(row)
