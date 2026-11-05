"""Render the complete plain-text research record as a paginated PDF."""
from pathlib import Path
from html import escape
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    NextPageTemplate, Image, KeepTogether,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output/pdf/autonomous_catalysis_research.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
FONTS = Path('/usr/share/fonts/truetype/dejavu')
for name, file in [('Body','DejaVuSerif.ttf'),('Bold','DejaVuSans-Bold.ttf'),
                   ('Sans','DejaVuSans.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))

ink = colors.HexColor('#172738')
blue = colors.HexColor('#234E69')
muted = colors.HexColor('#5E6E79')
styles = {
 'title': ParagraphStyle('title',fontName='Bold',fontSize=23,leading=28,textColor=ink,spaceAfter=16),
 'subtitle': ParagraphStyle('subtitle',fontName='Sans',fontSize=9.5,leading=14,textColor=muted,spaceAfter=17),
 'h1': ParagraphStyle('h1',fontName='Bold',fontSize=14.1,leading=19,textColor=blue,spaceBefore=18,spaceAfter=10,keepWithNext=True),
 'h2': ParagraphStyle('h2',fontName='Bold',fontSize=11.5,leading=16,textColor=ink,spaceBefore=13,spaceAfter=7,keepWithNext=True),
 'body': ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=14.5,textColor=ink,spaceAfter=9,splitLongWords=True,allowWidows=False,allowOrphans=False),
 'eq': ParagraphStyle('eq',fontName='Mono',fontSize=8.9,leading=13.3,textColor=blue,backColor=colors.HexColor('#F0F5F8'),borderPadding=9,spaceBefore=3,spaceAfter=12,leftIndent=8,rightIndent=8,splitLongWords=True),
 'ref': ParagraphStyle('ref',fontName='Sans',fontSize=8.3,leading=12,textColor=ink,spaceAfter=9,splitLongWords=True),
 'caption': ParagraphStyle('caption',fontName='Sans',fontSize=9.5,leading=14,textColor=ink,spaceAfter=10),
}

class ReportDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in ('h1','h2'):
            title = flowable.getPlainText()
            key = 's'+str(self.seq.nextf('section'))
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0 if flowable.style.name=='h1' else 1,closed=False)

def page(canvas,doc):
    w,h=canvas._pagesize
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D3DEE6'))
    canvas.line(48,h-34,w-48,h-34)
    canvas.setFont('Sans',7.6);canvas.setFillColor(muted)
    canvas.drawString(48,h-25,'AUTONOMOUS REACTION-ENERGY RECYCLING  •  RESEARCH RECORD')
    canvas.line(48,38,w-48,38)
    canvas.drawString(48,25,'Conditional constructions • Physical endpoint unresolved • 4 November 2026')
    canvas.drawRightString(w-48,25,str(doc.page))
    canvas.restoreState()

w,h=A4
doc=ReportDoc(str(OUT),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=48,bottomMargin=50,
             title='Autonomous reaction-energy recycling: complete constructions and unresolved endpoint',
             author='ChatGPT research collaboration',subject='Independent scientific constructions and reproducible catalytic kinetics')
doc.addPageTemplates([
 PageTemplate(id='portrait',frames=[Frame(48,50,w-96,h-98,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page),
 PageTemplate(id='landscape',pagesize=landscape(A4),frames=[Frame(48,50,h-96,w-98,id='figure',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page),
])

def rich(s):
    # Preserve literal mathematical signs, then make actual source URLs clickable.
    parts=re.split(r'(https?://[^\s]+)',s)
    out=[]
    for part in parts:
        if part.startswith(('https://','http://')):
            url=part.rstrip('.,;')
            tail=part[len(url):]
            out.append('<link href="'+escape(url,quote=True)+'" color="#235F84">'+escape(url)+'</link>'+escape(tail))
        else:out.append(escape(part))
    return ''.join(out)

story=[]
reference=False
for idx,block in enumerate((ROOT/'next_science/research_report.txt').read_text().split('\n\n')):
    block=block.strip()
    if not block:continue
    if block.startswith('# '):
        story.append(Paragraph(rich(block[2:]),styles['title']))
    elif block.startswith('## '):
        if block.startswith('## References'):
            reference=True;story.append(PageBreak())
        story.append(Paragraph(rich(block[3:]),styles['h1']))
    elif block.startswith('### '):
        story.append(Paragraph(rich(block[4:]),styles['h2']))
    elif block.startswith('>'):
        lines=[x[1:].lstrip() if x.startswith('>') else x for x in block.splitlines()]
        story.append(Paragraph('<br/>'.join(escape(x) for x in lines),styles['eq']))
    elif idx==1:
        story.append(Paragraph(rich(block),styles['subtitle']))
    else:
        story.append(Paragraph(rich(block).replace('\n','<br/>'),styles['ref' if reference else 'body']))

story.extend([NextPageTemplate('landscape'),PageBreak(),
              Paragraph('Figure: evidence and conditional whole-cycle limits',styles['h1'])])
imgpath=ROOT/'next_science/root_construction/catalysis/full_cycle_evidence.png'
from PIL import Image as PILImage
iw,ih=PILImage.open(imgpath).size
dw=h-96
story.append(Image(str(imgpath),width=dw,height=dw*ih/iw))
story.append(Spacer(1,10))
story.append(Paragraph('The left panel digitizes the source supporting information; its error scale represents image extraction, not experimental confidence. The other panels are model calculations under explicit waveform, cycle, and donor-budget assumptions. They are not fits to the material and do not exclude reversible or correlated mechanisms outside that class. Complete scripts and input attribution are included in the accompanying archive.',styles['caption']))
doc.build(story)
print(OUT)
