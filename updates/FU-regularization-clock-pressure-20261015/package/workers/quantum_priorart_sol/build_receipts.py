from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from pypdf import PdfReader

base=Path(__file__).resolve().parent
src=base/"sources"
profiles=[
("husimi_1940","Some Formal Properties of the Density Matrix",
 "Kôdi Husimi","https://www.jstage.jst.go.jp/article/ppmsj1919/22/4/22_4_264/_pdf","https://doi.org/10.11429/ppmsj1919.22.4_264",
 ["Original printed pp.277-279 (PDF pp.14-16): Sec.5, Eqs.(5.1),(5.5),(5.6), wave-packet positive expectation and Gauss/Fourier smoothing, visually inspected"]),
("schwonnek_werner_1802.08342","The Wigner distribution of n arbitrary observables",
 "René Schwonnek; Reinhard F. Werner","https://arxiv.org/pdf/1802.08342","https://doi.org/10.1063/1.5140632",
 ["PDF pp.2-5: characteristic/moment definitions, graphical regularization, Proposition 1 support proof, Proposition 2 positivity proof",
  "PDF p.14: Eqs.(51)-(55), exact Pauli triple shell-derivative distribution"]),
("dammeier_schwonnek_werner_1505.00049","Uncertainty relations for angular momentum",
 "Lars Dammeier; René Schwonnek; Reinhard F. Werner","https://arxiv.org/pdf/1505.00049","https://doi.org/10.1088/1367-2630/17/9/093046",
 ["PDF pp.20-22: all-direction output contract, calibration and metric error, Lemma 9 proof",
  "PDF pp.23-24: Lemma 10 proof and general covariant POVM classification Eqs.(109)-(111)",
  "PDF pp.25-27: Lemma 11, Eq.(118), Theorem 12 and proof reduction"]),
("barchielli_gregoratti_1912.09758","Entropic measurement uncertainty relations for all the infinite components of a spin vector",
 "Alberto Barchielli; Matteo Gregoratti","https://arxiv.org/pdf/1912.09758",None,
 ["PDF pp.3-8: sphere POVMs and directional discretization, Theorem 1",
  "PDF pp.9-10: noise and compatibility distinctions",
  "PDF pp.17-18: Theorem 4 spin-half optimum and classical-noise interpretation"]),
("appleby_quant-ph9911021","Optimal Measurements of Spin Direction",
 "D. M. Appleby","https://arxiv.org/pdf/quant-ph/9911021","https://doi.org/10.1023/A:1003712030966",
 ["PDF pp.8-11: Sec.5, isotropic retrodictively optimal coherent POVM, Eq.(36), and spin-direction first moments"]),
("dariano_macchiavello_sacchi_quant-ph0007062","Joint measurements via quantum cloning",
 "G. M. D'Ariano; C. Macchiavello; M. F. Sacchi","https://arxiv.org/pdf/quant-ph/0007062","https://doi.org/10.1088/1464-4266/3/2/305",
 ["PDF pp.1-3: clone coordinate POVM, unbiased rescaling, coherent measurement Eqs.(13)-(17)"]),
("sabbagh_miangolarra_georgiou_2505.00245","On a time-resolved interpretation of the Husimi function",
 "Ralph Sabbagh; Olga Movilla Miangolarra; Tryphon T. Georgiou","https://arxiv.org/pdf/2505.00245",None,
 ["All 4 pages: general Gaussian-semigroup positive representation, general non-convolution kernel, explicit Pauli normalization and kernel"]),
("sabbagh_et_al_2409.19206","Particle approximations of Wigner distributions for n arbitrary observables",
 "Ralph Sabbagh; Olga Movilla Miangolarra; Hamid Hezari; Tryphon T. Georgiou","https://arxiv.org/pdf/2409.19206","https://doi.org/10.1103/PhysRevResearch.7.013102",
 ["Definitions and signed-measure statements",
  "PDF pp.7-8: Proposition 4 principal-axis marginal proof, Proposition 5 convergence proof, Proposition 6 smoothed uniform convergence proof",
  "Pauli examples"]),
("massar_quant-ph0703036","Uncertainty Relations for Positive Operator Valued Measures",
 "Serge Massar","https://arxiv.org/pdf/quant-ph/0703036","https://doi.org/10.1103/PhysRevA.76.042114",
 ["PDF pp.2-4: uncertainty operator positivity, qubit examples, weak unbiasedness distinction Eqs.(9)-(12)"]),
("ghai_sharma_ghosh_2306.07917","Negativity of Wigner distribution function as a measure of incompatibility",
 "Jatin Ghai; Gautam Sharma; Sibasish Ghosh","https://arxiv.org/pdf/2306.07917",None,
 ["PDF pp.1-3: Wigner definition, graphical Gaussian regularization, noisy-operator/eigenprojector setup"]),
]
def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()
def record_file(path):
 return {"path":str(path.relative_to(base)),"bytes":path.stat().st_size,"sha256":digest(path)}
records=[]
for stem,title,authors,url,doi,read in profiles:
 pdf=src/(stem+".pdf")
 assert pdf.read_bytes().startswith(b"%PDF"), stem
 txt=pdf.with_suffix(".txt")
 # Text is a derivative, not an immutable acquired source; remove embedded NULs.
 text=txt.read_text().replace("\x00","")
 txt.write_text(text)
 r={"title":title,"authors":authors,"download_url":url,"doi":doi,
    "pdf":record_file(pdf),"pages":len(PdfReader(pdf).pages),
    "extraction":record_file(txt),"proof_sections_inspected":read,
    "format":"Original primary research preprint PDF; downloaded bytes pinned by SHA256",
    "visual_check_pages":[]}
 for png in src.glob(stem+"_page*.png"):
  r["visual_check_pages"].append(record_file(png))
 records.append(r)
gates=[
 {"title":"The Weyl functional calculus","authors":"Robert F. V. Anderson","year":1969,
  "doi":"https://doi.org/10.1016/0022-1236(69)90013-5",
  "primary_url":"https://www.sciencedirect.com/science/article/pii/0022123669900135",
  "attempted_pdf_url":"https://www.sciencedirect.com/science/article/pii/0022123669900135/pdfft",
  "access":"Full PDF request HTTP 403; bibliographic metadata only. No full-text clearance."},
 {"title":"On the Weyl functional calculus","authors":"Robert F. V. Anderson","year":1970,
  "doi":"https://doi.org/10.1016/0022-1236(70)90050-9",
  "primary_url":"https://www.sciencedirect.com/science/article/pii/0022123670900509",
  "attempted_pdf_url":"https://www.sciencedirect.com/science/article/pii/0022123670900509/pdfft",
  "access":"Primary publisher abstract obtained; full PDF request HTTP 403. No full-text clearance."},
 {"title":"Joint Wigner distribution for spin-1/2 particles","authors":"Leon Cohen; Marlan O. Scully","year":1986,
  "doi":"https://doi.org/10.1007/BF01882690",
  "primary_url":"https://link.springer.com/article/10.1007/BF01882690",
  "access":"Primary publisher abstract obtained; subscription full text unavailable. No full-text clearance."},
 {"title":"Quasi-probability distribution for spin-1/2 particles","authors":"C. Chandler; L. Cohen; C. Lee; M. Scully; K. Wódkiewicz","year":1992,
  "doi":"https://doi.org/10.1007/BF01889685",
  "primary_url":"https://link.springer.com/article/10.1007/BF01889685",
  "access":"Primary publisher abstract and references obtained; subscription full text unavailable. No full-text clearance."},
 {"title":"Towards a new uncertainty principle: quantum measurement noise","authors":"Hans Martens; Willem M. de Muynck","year":1991,
  "doi":"https://doi.org/10.1016/0375-9601(91)91015-6",
  "primary_url":"https://www.sciencedirect.com/science/article/abs/pii/0375960191910156",
  "attempted_pdf_url":"https://citeseerx.ist.psu.edu/document?doi=5d4708ca3ec5fb6370f2513d9cbf366a9dc26c8f&repid=rep1&type=pdf",
  "access":"Primary abstract obtained; located PDF index link failed, curl 404 / web 403. No full-text clearance."},
 {"title":"Unsharp reality and joint measurements for spin observables","authors":"Paul Busch","year":1986,
  "doi":"https://doi.org/10.1103/PhysRevD.33.2253",
  "primary_url":"https://journals.aps.org/prd/abstract/10.1103/PhysRevD.33.2253",
  "attempted_pdf_url":"https://journals.aps.org/prd/pdf/10.1103/PhysRevD.33.2253",
  "access":"Primary publisher abstract obtained; PDF inaccessible/subscription. No full-text clearance."},
]
report={"recorded_at_utc":datetime.now(timezone.utc).isoformat(),
        "input":{"path":"../../sources/regularization_pasted.txt",
                 "sha256":digest(base.parent.parent/"sources"/"regularization_pasted.txt"),
                 "role":"Producer claim data, not certification"},
        "downloaded_primary_pdfs":records,"historical_full_text_gates":gates,
        "notes":["Unversioned arXiv download URLs are resolved by actual pinned PDF bytes; hashes establish identity, not validity.",
                 "PNG receipts record visual inspections of mathematical formulas.",
                 "No failed PDF is counted as acquired."]}
(base/"SOURCE_RECEIPTS.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
print(json.dumps({"downloaded_primary_pdfs":len(records),"historical_full_text_gates":len(gates),"all_pdf_headers_valid":True},indent=2))
