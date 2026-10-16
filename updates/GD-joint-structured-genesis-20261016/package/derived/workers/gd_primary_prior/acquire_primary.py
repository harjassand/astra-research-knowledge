"""Read-only primary-source retrieval. No acquired code is executed."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, urllib.request, urllib.error

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'acquired_excluded_from_publication'
SOURCES = [
 ('redheffer_1953.pdf', 'https://msp.org/pjm/1953/3-4/pjm-v3-n4-p11-s.pdf'),
 ('dryanov_qazi_rahman_2002.pdf', 'https://citeseerx.ist.psu.edu/document?doi=64975efc67f88c13dbebba9f18fff6b52e64eb3f&repid=rep1&type=pdf'),
 ('albert_bradlyn_fraas_jiang_1512.08079v4.pdf', 'https://arxiv.org/pdf/1512.08079v4'),
 ('vacchini_1906.00693v1.pdf', 'https://arxiv.org/pdf/1906.00693v1'),
 ('aniello_1002.3507v1.pdf', 'https://arxiv.org/pdf/1002.3507v1'),
 ('shang_franca_2604.18533v2.pdf', 'https://arxiv.org/pdf/2604.18533v2'),
 ('ht_2212.08437v2.pdf', 'https://arxiv.org/pdf/2212.08437v2'),
 ('temmel_1105.1683v3.pdf', 'https://arxiv.org/pdf/1105.1683v3'),
 ('lss_official.pdf', 'https://projecteuclid.org/journals/annals-of-probability/volume-25/issue-1/Domination-by-product-measures/10.1214/aop/1024404279.pdf'),
 ('lss_legacy.pdf', 'https://projecteuclid.org/download/pdf_1/euclid.aop/1024404279'),
 ('schonmann_papers.html', 'https://www.math.ucla.edu/~rhs/papers.html'),
 ('hormander_landing.html', 'https://www.mscand.dk/article/view/10421'),
]

def get(item):
    name,url=item
    row={'requested_url':url,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (read-only research source retrieval)'}), timeout=35) as r:
            data=r.read();row.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
        valid_pdf = data.startswith(b'%PDF')
        if name.endswith('.pdf') and not valid_pdf:
            name += '.failed_html'
        out=DEST/name;out.write_bytes(data)
        row.update(path=str(out.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pdf_magic=valid_pdf)
        if valid_pdf:
            from pypdf import PdfReader
            doc=PdfReader(out)
            txt=out.with_suffix('.txt')
            txt.write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n'+page.extract_text() for i,page in enumerate(doc.pages)),encoding='utf-8')
            row.update(pdf_pages=len(doc.pages),text_path=str(txt.relative_to(ROOT)),text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
    except Exception as e:
        row.update(error=f'{type(e).__name__}: {e}')
    return row

if __name__=='__main__':
    DEST.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        rows=list(ex.map(get,SOURCES))
    (DEST/'ACQUISITION.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in row.items() if k in ('path','bytes','pdf_pages','error','content_type')} for row in rows],indent=2))
