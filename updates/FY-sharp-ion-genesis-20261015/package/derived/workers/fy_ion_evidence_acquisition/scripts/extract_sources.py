"""Read original PDF and XLSX sources without modifying their bytes.
Extracted full text and cell maps are local working evidence, not publication files.
"""
import json
import pathlib
import posixpath
import zipfile
import xml.etree.ElementTree as ET

from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / 'raw_originals'
PRIVATE = ROOT / 'analysis' / 'private_extractions'
PRIVATE.mkdir(parents=True, exist_ok=True)
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p': 'http://schemas.openxmlformats.org/package/2006/relationships'}

for path in RAW.glob('*.pdf'):
    if not path.read_bytes().startswith(b'%PDF'):
        print(json.dumps({'file':path.name, 'status':'NOT_A_PDF'}))
        continue
    reader = PdfReader(path)
    (PRIVATE / (path.stem + '.txt')).write_text('\n\n'.join(f'===== PDF PAGE {i+1} =====\n' + (page.extract_text() or '') for i,page in enumerate(reader.pages)))
    print(json.dumps({'file':path.name,'pages':len(reader.pages),'metadata':str(reader.metadata)}))

for path in RAW.glob('*.xlsx'):
    book = {'source_file':path.name,'sheets':[]}
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS):
                strings.append(''.join(t.text or '' for t in si.iterfind('.//s:t',NS)))
        rels = {r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')).findall('p:Relationship',NS)}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',NS):
            target = rels[sheet.attrib['{'+NS['r']+'}id']]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl',target))
            tree = ET.fromstring(z.read(target))
            cells = {}
            for c in tree.findall('.//s:sheetData/s:row/s:c',NS):
                v = c.find('s:v',NS)
                value = v.text if v is not None else None
                typ = c.attrib.get('t')
                if typ == 's' and value is not None:
                    value = strings[int(value)]
                elif typ == 'inlineStr':
                    value = ''.join(t.text or '' for t in c.iterfind('.//s:t',NS))
                elif value is not None and typ not in ['str','e','b']:
                    try: value = float(value)
                    except ValueError: pass
                formula = c.find('s:f',NS)
                if value is not None or formula is not None:
                    cells[c.attrib['r']] = {'v':value, **({'formula':formula.text,'formula_attrs':formula.attrib} if formula is not None else {})}
            dim = tree.find('s:dimension',NS)
            s = {'name':sheet.attrib['name'],'state':sheet.attrib.get('state','visible'), 'dimension':dim.attrib.get('ref') if dim is not None else None, 'cells':cells}
            book['sheets'].append(s)
            labels = [[k,v] for k,v in cells.items() if isinstance(v['v'],str)]
            first_rows = dict(list((k,v) for k,v in cells.items() if int(''.join(ch for ch in k if ch.isdigit()))<=7)[:16])
            print(json.dumps({'file':path.name,'sheet':s['name'],'dimension':s['dimension'],'cell_count':len(cells),'formula_count':sum('formula' in c for c in cells.values()),'first_rows':first_rows,'labels':labels[:20]},ensure_ascii=False))
    (PRIVATE / (path.stem + '_cells.json')).write_text(json.dumps(book,ensure_ascii=False))
