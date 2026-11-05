"""Build the noisy thermal-interface research report; proofs and checks live beside it."""
from pathlib import Path
import hashlib, html, json, sys, re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
)
from PIL import Image as PILImage
from matplotlib.mathtext import math_to_image
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "dejavuserif"
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent / "deliverables"
OUT.mkdir(exist_ok=True)
TMP = ROOT / "equations"
TMP.mkdir(exist_ok=True)
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
FONT = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in (
    ("DSerif", "DejaVuSerif.ttf"), ("DSerif-Bold", "DejaVuSerif-Bold.ttf"),
    ("DSans", "DejaVuSans.ttf"), ("DSans-Bold", "DejaVuSans-Bold.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT / filename)))
for family in ("DSerif", "DSans"):
    pdfmetrics.registerFontFamily(
        family, normal=family, bold=family+"-Bold",
        italic=family, boldItalic=family+"-Bold"
    )
INK = colors.HexColor("#172D3D")
TEAL = colors.HexColor("#247A82")
MUTED = colors.HexColor("#586973")
PALE = colors.HexColor("#EDF4F5")
WIDTH = A4[0] - 96
styles = {
    "body": ParagraphStyle("body", fontName="DSerif", fontSize=10.3,
                           leading=15.4, spaceAfter=8, textColor=INK),
    "small": ParagraphStyle("small", fontName="DSerif", fontSize=9.1,
                            leading=13.2, spaceAfter=6, textColor=INK),
    "caption": ParagraphStyle("caption", fontName="DSans", fontSize=8.6,
                              leading=12, spaceAfter=8, textColor=MUTED),
    "h1": ParagraphStyle("h1", fontName="DSans-Bold", fontSize=18.5,
                         leading=24, spaceAfter=14, textColor=INK),
    "h2": ParagraphStyle("h2", fontName="DSans-Bold", fontSize=11.7,
                         leading=15.7, spaceBefore=8, spaceAfter=7, textColor=TEAL),
    "title": ParagraphStyle("title", fontName="DSans-Bold", fontSize=27,
                            leading=33, spaceAfter=18, textColor=INK),
    "label": ParagraphStyle("label", fontName="DSans-Bold", fontSize=9,
                            leading=13, spaceAfter=12, textColor=TEAL),
    "table": ParagraphStyle("table", fontName="DSerif", fontSize=8.8,
                            leading=12.5, spaceAfter=0, textColor=INK),
}
story, plain = [], []
def p(text, style="body"):
    rendered = text.replace("ℓ", '<font name="DSans">ℓ</font>')
    story.append(Paragraph(rendered, styles[style]))
    plain.append(text)
def h(text):
    p(text, "h2")
def page(title):
    if story:
        story.append(PageBreak())
    p(title, "h1")
def eq(tex, fontsize=13):
    tex = " ".join(tex.split())
    tex = re.sub(r"\\le(?![A-Za-z])", r"\\leq", tex)
    tex = re.sub(r"\\ge(?![A-Za-z])", r"\\geq", tex)
    tex = re.sub(r"\\ne(?![A-Za-z])", r"\\neq", tex)
    def fractions(s):
        result, i = "", 0
        while i < len(s):
            if s[i] == "{" and (i == 0 or s[i-1] != "\\"):
                j, depth = i+1, 1
                while j < len(s) and depth:
                    if s[j] == "{" and s[j-1] != "\\": depth += 1
                    if s[j] == "}" and s[j-1] != "\\": depth -= 1
                    j += 1
                inside = fractions(s[i+1:j-1])
                k, level, split = 0, 0, None
                while k < len(inside):
                    if inside[k] == "{" and (k == 0 or inside[k-1] != "\\"): level += 1
                    if inside[k] == "}" and (k == 0 or inside[k-1] != "\\"): level -= 1
                    if level == 0 and inside.startswith("\\over", k): split = k; break
                    k += 1
                if split is not None:
                    inside = "\\frac{"+inside[:split]+"}{"+inside[split+5:]+"}"
                result += "{"+inside+"}"
                i = j
            else:
                result += s[i]
                i += 1
        return result
    tex = fractions(tex)
    tex = re.sub(r"\\mathbb\s+([A-Za-z])", r"\\mathbb{\1}", tex)
    tex = re.sub(r"\\(mathcal|overline)\s+([A-Za-z])", r"\\\1{\2}", tex)
    tex = re.sub(r"\\sqrt([0-9])", r"\\sqrt{\1}", tex)
    tex = tex.replace(r"\mathbf1", r"\mathbf{1}")
    tex = re.sub(r"\\frac([0-9])([0-9])", r"\\frac{\1}{\2}", tex)
    tex = re.sub(r"\}([0-9])", r"}{\1}", tex)
    key = hashlib.sha256((str(fontsize)+tex).encode()).hexdigest()[:15]
    f = TMP / (key + ".png")
    if not f.exists():
        math_to_image("$" + tex + "$", str(f), dpi=240,
                      format="png", color="#172D3D")
    with PILImage.open(f) as im:
        w, ht = im.size
    width = min(WIDTH, w * fontsize / 10 * 72 / 240)
    image = Image(str(f), width=width, height=ht*width/w)
    image.hAlign = "CENTER"
    story.extend([Spacer(1, 3), image, Spacer(1, 10)])
    plain.append("MATH: " + tex)
def table(rows, widths):
    data = [[Paragraph(c, styles["table"]) for c in row] for row in rows]
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0,0), (-1,0), PALE),
        ("LINEBELOW", (0,0), (-1,0), .7, TEAL),
        ("LINEBELOW", (0,1), (-1,-1), .3, colors.HexColor("#D8E0E4")),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
        ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.extend([t, Spacer(1, 9)])
    plain.extend(" | ".join(row) for row in rows)
def link(url, label):
    return '<link href="%s" color="#247A82">%s</link>' % (
        html.escape(url, quote=True), html.escape(label)
    )

def figure(path, maxheight=340, caption=None):
    with PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(WIDTH / iw, maxheight / ih)
    pic = Image(str(path), width=iw*scale, height=ih*scale)
    pic.hAlign = "CENTER"
    story.extend([Spacer(1, 5), pic, Spacer(1, 7)])
    if caption:
        p(caption, "caption")

def theorem(label, text):
    p("<b>" + label + ".</b> " + text)

# The artifact-operation marker was run once before this file was authored.

# 1
p("ASTRA RESEARCH / CONSTRUCTIVE RESOLUTION / 5 NOVEMBER 2026", "label")
p("A noisy interface to a long-lived thermal quantum register", "title")
p("Fixed component error, constructive thermal precompensation, and a reference-preserving write-hold-read operation", "h2")
p("<b>Result.</b> Within a specified noisy-circuit architecture and the accepted commuting-Hamiltonian / Pauli-Davies holding contract, a fixed nonzero component error rate supports commissioning, unknown-input loading, long passive holding, useful protected access, refresh, and noisy local delivery. The accuracy of each elementary control location need not shrink with memory size or requested duration.")
p("The construction prepares a positive, efficiently sampled inverse-noise syndrome law. Actual terminal noise maps that law to the Gibbs syndrome marginal, while a prefix argument protects the unknown logical state. A noisy classical regenerator removes the old syndrome-history dependence that otherwise prevents an independent endpoint-noise description. An anytime-read argument handles adaptive access without assuming a Gibbs marginal at a stopping time.")
h("The operational consequence")
p("The register tolerates a prescribed interval with every active quantum controller disabled, while its static protective Hamiltonian and stipulated thermal environment remain present. In an explicitly common bath, every noninteracting holding Hamiltonian loses accurate unknown-qubit storage after a constant-length blackout, regardless of gaps, cooling or code size. The zero-Hamiltonian case becomes entanglement breaking. This establishes a control-availability capability, with no total-energy or total-spacetime advantage claimed.")
h("What remains supplied and what is paid")
p("The holding bath, positive commuting couplings, suitable fabrication and a paid nonlocal active fabric remain model assumptions. No finite-speed, bounded-density three-dimensional processor is inferred. Noisy gates, controllers, waits, routing, sampling, coefficient acquisition, reset and raw ports are inside the operation. The unavoidable raw-port error is O(p); protected interior error can be made arbitrarily small. The sufficient constants are severely unfavorable.")
p("This report proves the new bridges. Accepted source compilation, thermal loading, passive-time coupling and earlier results are used at their earned scopes. Accompanying proof notes and executable finite checks make the construction inspectable. The finite checks are not a BDL device or lifetime simulation.", "small")

# 2
page("1. Model, interfaces and accepted inputs")
p("Let N be the physical memory size and m the number of commuting checks. A decoder frame identifies each valid syndrome sector with a fixed logical system. The valid syndrome space L is a binary linear subspace. A local Pauli translates a syndrome within L and may induce a logical Pauli. An unstable syndrome is one on which an elementary physical Pauli can act nontrivially on the protected logical system.")
eq(r"\pi(s)=Z^{-1}e^{-\sum_{a=1}^{m}\lambda_a s_a},\quad s\in L,\qquad \lambda_a=\beta J_a>0.")
table([
 ["Input or resource", "Precise scope used"],
 ["Accepted history compiler", "Bounded-degree history representation, E(γ) ≥ a|γ|, polynomial frame evaluation, and an instability witness of size L*(N) = Ω(N^η)."],
 ["Accepted holding theorem", "Energy-resolved local Pauli Davies jumps, bounded rate Γ, Gibbs syndrome stationarity, and logical-jump probability controlled by unstable mass."],
 ["Active primitive model", "Independent state-independent stochastic Pauli faults of fixed strength p at bounded-arity gates, preparations, measurements and idles; fixed schedules and disjoint fresh factory faults."],
 ["Classical controls", "Boolean arithmetic and scheduling use the same noisy protected gate scheme. Final raw controls use the regenerator proved below."],
 ["Architecture", "Paid nonlocal active links with specified clock time, fault law and cost; a constant-size terminal cell per memory site; synchronized final arrivals."],
 ["Physical access", "Paid local exchange and stable coupler switching. The explicit acquisition route also requires selective isolation of actual check couplers."],
], [135, WIDTH-135])
p("We use half-diamond error d⋄(Φ,Ψ) = ½‖Φ−Ψ‖⋄ and classical total variation. Channel statements allow arbitrary logical references and retained external records. Fine internal Bell, controller and pool transcripts are reset where required, with their cost included.")
p("The fully commissioned instance uses §16's single unknown stationary Pauli law Λ at all specified wire and measurement cuts: all reset, readout, template and record-capture faults are determined by Λ, with no extra unknown SPAM channel. Selective-check calibration is paid. Broader known independent laws are covered by the circuit lemmas; idle ratios do not identify arbitrary unknown gate-dependent faults. Stationarity, the bath and fabrication class remain substantive contracts against which finite tests cannot exclude arbitrary drift.", "small")

# 3
page("2. Complete operation and its guarantee")
theorem("Theorem A: fixed-rate thermal-register operation", "Fix the preceding contracts, a sufficiently low fixed temperature, and bounded check incidence and coupling strength. There is p* &gt; 0 independent of N, requested duration and requested interior accuracy. For p &lt; p*, finite noisy circuits commission and load an unknown reference-entangled logical input, hold it passively, perform protected work and refresh, and deliver a local raw output.")
p("For each offered source j, declare a deterministic cap T<sub>j</sub> on that source's intrinsic passive time. Let R bound source/access opportunities, including rejected or selectively considered candidates, and T = ΣT<sub>j</sub>. For ordinary sequential use, R is proportional to writes and reads. With a fixed Peierls slack incorporated into b<sub>N</sub>, the campaign bound has the form")
eq(r"d_\diamond\le Cn_{\rm raw}p+\epsilon_{\rm total}+C(RNq+\Gamma NT)b_N,\qquad b_N\le C'e^{-cN^\eta}.")
p("Here n<sub>raw</sub> counts unknown logical raw entries and deliveries, and q = O(p) is the calibrated physical-memory endpoint strength. The unabsorbed anytime-read bound contains Nq(1+ΓNT<sub>j</sub>) times the sharper instability tail; the proof earns the displayed slack absorption. The term ε<sub>total</sub> pays protected computation, regeneration, source/numerical approximation, coefficient uncertainty and acquisition failure. Encoded internal reuse does not repay a logical raw port; physical release and reacquisition do.")
h("The actual sequence")
p("Commission component laws and couplings. Compute the effective endpoint Pauli law for the chosen schedule. Sample the positive preimage μ = K<sup>−1</sup>π. Inject the unknown qubit through a noisy protected input interface and run the accepted thermal encoder for that sample. Export its N outputs using independent Bell resources, regenerated byproducts and synchronized local descents. Actual terminal noise produces the Gibbs syndrome marginal. Engage the holding Hamiltonian. To read, begin all local raw-to-protected injections together, apply the protected decoder, perform useful logical work, and deliver or reload a fresh compensated background.")
p("The source error is paid once per prepared source. A finite independent source stream can be commissioned with one total variation budget. Adaptive holds and reads are controlled by source-specific intrinsic-time caps, not by an unjustified claim of equilibrium at a stopping time. If only a total exposure cap is supplied across adaptive refreshes, a conservative extra factor for the number of reset opportunities is retained unless a sharper allocation is proved.", "small")

# 4
page("3. One noisy code for quantum and classical work")
p("A generic fault-tolerant output theorem leaves correctable syndrome systems. They may correlate across blocks and with records. Replacing them immediately by independent Pauli noise would be false. We first construct compatible noisy interfaces and local-stochastic fanout, then erase that dependence.")
h("A same-code measurement-free precursor")
p("Use Aharonov and Ben-Or's measurement-free scheme [1], including coherent syndrome processing, noisy preparation, idle and discard. The finite native set includes NOT, CNOT, phase, controlled-Z, H, Toffoli and SWAP. An explicit conservative base code comes from RM(5,11), of length 2048, dimension 1024 and distance 64. It is self-dual and doubly even. Puncturing one coordinate and taking the dual inclusion gives a one-qubit CSS code of length 2047 and distance at least 63, correcting 31 errors.")
p("Self-duality follows because products of degree-at-most-five evaluation monomials have degree below eleven and zero binary sum; dimension is half the length. The decomposition f(x,t)=g(x)+th(x) proves the distance induction. Generator weights divisible by four and even pairwise overlaps prove doubly-evenness. All these constants are fixed and very large.")
p("AB procedures have spread at most four; a gate preceded by correction has conservative spread sixteen, inside this correction margin. Let A bound the native locations in a fixed rectangle. Mark two or more bad child rectangles as a recursive bad tag. With a = A(A−1)/2,")
eq(r"p_{r+1}\le ap_r^2,\qquad p_r\le p(ap)^{2^r-1},\qquad \sum_{r\ge0}p_r\le2p\quad(ap\le1/2).")
p("For G protected locations, choose the level so Gp<sub>r</sub> fits its budget. AB's correction-stage validity accommodates arbitrary incoming density matrices. Logical correctness is asserted only for the specified sparse-correctable incoming class. Those deviations form the syndrome subsystem of a many-to-one code; they are not declared absent.")
p("CFG's code-independent algebra [2] then applies: an exact logical unitary factors from the syndrome; pure logical preparation factors; exact destructive logical measurement traces the consumed syndrome. These facts follow from purity and Stinespring uniqueness. We do not import CFG's ideal classical controller. The same AB code and noisy primitives implement the Boolean arithmetic, fanout and adjacent-level interfaces here.", "small")

# 5
page("4. Interfaces and correlated classical leaves")
h("Adjacent-level quantum interfaces")
p("Fix finite target circuits for base-code encoding and coherent recovery followed by inverse encoding. Implement a level-r to level-(r+1) stage by simulating that encoder with level-r rectangles and finishing with correction; reverse the construction for descent. This is CFG's adjacent-level construction [2], instantiated in the same measurement-free representation. The encoder and decoder are circuit descriptions, not ideal physical devices.")
p("Let g bound the rectangles in one stage. Off an input-independent bad-fault tag of probability at most gp<sub>r</sub>, the stage is logically correct for every allowed incoming syndrome. The fixed code margin corrects the sparse bad-child set. Complete descent therefore has a bad tag satisfying")
eq(r"q_{\rm out}\le g\sum_{r=0}^{r_{\max}-1}p_r\le2gp.")
p("The analogous upward interface preserves an unknown reference-entangled raw input except for O(p) encoded logical boundary noise. Its final high-level leakage can be reduced arbitrarily. No bare output waits while a growing classical decoder finishes: waiting is protected at the current level and counted.")
h("Protected fanout produces local-stochastic leaves")
p("Prepare independent encoded Bell resources A<sub>i</sub>B<sub>i</sub>. Perform a protected logical Bell-basis unitary on incoming data D<sub>i</sub> and A<sub>i</sub>. Copy each resulting logical Z bit into M fresh encoded zero blocks by a protected CNOT tree. Discard consumed D,A registers. No fanout or old-controller gate touches B.")
p("Replace bad high-level paths in a channel hybrid by their exact logical counterparts, paying ε<sub>FT</sub> without conditioning on global success. Conditional on Bell bit b, the logical pool is |b⟩<sup>⊗M</sup>. Its syndromes can correlate arbitrarily with one another, B and old records. Descend and measure its M copies using disjoint future faults. Wrong copies lie inside independent local bad tags, hence")
eq(r"\Pr[S\subseteq W]\le q_c^{|S|},\qquad q_c\le(2g+1)p.")
p("The bound is uniform in the full incoming syndrome/reference state. It is a local-stochastic law, not a product-error claim. Copying a single already corrupted raw bit would violate it by producing a macroscopic error with constant probability. Protected fanout must precede raw descent.")

# 6
page("5. Static noisy regeneration: theorem")
theorem("Theorem B: history-independent raw classical export", "Let M = 3<sup>L</sup> raw leaves equal b XOR E<sub>j</sub>, with local-stochastic error support of strength q<sub>c</sub>. The bit and errors may correlate with arbitrary quantum references. Use a fixed ternary majority tree. Every wire has fresh independent flip probability at most e; every complement-covariant voter has an independent faulty-macro tag of probability at most v. Put p<sub>c</sub> = max(q<sub>c</sub>,e,v) ≤ 1/100.")
eq(r"d_\diamond({\rm actual\ root},{\rm fresh\ BSC\ root})\le q_c(21p_c)^L.")
p("The comparison output is b XOR Z, where Z is independent of all old references and records, with crossover at most 2p<sub>c</sub>. Independent reference trees give independent errors even if actual leaf pools were correlated. For k output bits, the joint replacement cost is at most kq<sub>c</sub>(21p<sub>c</sub>)<sup>L</sup>.")
h("A finite noisy voter with the required symmetry")
p("Apply CNOT a→b, CNOT a→c, and a Toffoli with controls b,c and target a. Keep a and discard the others. Its ideal output is")
eq(r"a\oplus(a\oplus b)(a\oplus c)=ab\oplus ac\oplus bc={\rm maj}(a,b,c).")
p("For every fixed intervening bit-flip pattern, complementing all inputs preserves the transformed Toffoli controls and complements its target. Thus the noisy truth table is exactly complement covariant in the stipulated Pauli/bit-flip model. Its macro-fault probability is bounded by the sum of its finite gate and idle fault probabilities. Another decomposition must establish the same covariance or impose it with a local constant-depth complement twirl; it cannot simply presume it.")
h("The resource tradeoff")
p("Depth L = O(log(k/ε)) suppresses dependence on old history to ε, using 3<sup>L</sup> leaves and O(3<sup>L</sup>) gates and links. The remaining raw bit error stays O(p). This polynomial pool cost can dominate the processor's usual polylogarithmic threshold overhead. The fixed tree is reusable with fresh faults and paid preparation/reset. It needs no ideal mutable routing network.")

# 7
page("6. Mixed local-stochastic proof")
p("Couple the actual tree to a reference tree whose leaves are all b, using the same fresh wire and voter faults. These exact reference leaves exist only in the proof. Let D mean actual/reference disagreement and U mean that either process is wrong relative to b. For disjoint sets A,B of level-ℓ nodes, maintain")
eq(r"\Pr[D_A=1,\ U_B=1]\le d_\ell^{|A|}u_\ell^{|B|},\qquad d_0=u_0=q_c.")
p("A shared wire flip cannot create D and changes the U bound to at most u+e. A correct majority is wrong only if two children are wrong. Majority outputs disagree only if a child disagrees and a distinct child is erroneous in at least one process: six ordered witnesses suffice. A faulty voter can disagree only if an input differs, because both executions use the same truth table. Thus")
eq(r"u_{\ell+1}\le v+3(u_\ell+e)^2,\qquad d_{\ell+1}\le[3v+6(u_\ell+e)]d_\ell.")
p("For several parent events, expand their witness unions. Different parents use disjoint children and fresh fault variables. Apply the mixed bound to the disjoint D and U witness sets and multiply fresh tag probabilities. Summing witnesses gives the same product-form bound for every disjoint A,B. Initial leaf-error independence was never used.")
eq(r"\bar u=2p_c,\quad v+3(\bar u+e)^2\le p_c+27p_c^2\le2p_c,")
eq(r"3v+6(\bar u+e)\le21p_c<1,\qquad d_L\le q_c(21p_c)^L.")
p("The reference subtrees use independent fresh faults. Complement covariance makes their error independent of b. For a majority-plus-output-flip voter, r<sub>0</sub>=0 and r<sub>ℓ+1</sub>=v+(1−2v)[3z<sup>2</sup>−2z<sup>3</sup>], with z=e+(1−2e)r<sub>ℓ</sub>. A finite complement-covariant truth table gives an equally explicit recursion. The preceding bound implies r<sub>L</sub>≤2p<sub>c</sub>.")
p("For quantum records, attach each initial classical error label to its conditional reference state. The coupled executions retain the same state whenever output bits agree. Half trace distance is bounded by the mismatch mass. Supremizing over references proves the channel/instrument guarantee. It preserves unconditional records; postselection on a rare record incurs its usual acceptance-probability cost.", "small")

# 8
page("7. Bell export and simultaneous raw arrival")
p("A complete descent can expose an old correlated syndrome at the output. Applying Bell corrections through that old coherent controller can transfer the same dependence into a fresh B syndrome. We therefore defer every correction until the final raw cell.")
p("Run separate trees for the Bell bits. B retains its unresolved frame on an independent protected wait/descent path. Destructive logical Bell measurement traces the old D,A syndromes. After discarding the fine pool gauges and internal transcripts, the comparison B gauge has its independent resource marginal; no independence is claimed against those still-retained fine systems. Tree replacement makes the final bit errors independent of B and old external history. The comparison instrument, with a CPTP encoding map V<sub>B</sub>, is")
eq(r"\rho\longmapsto {1\over4}\sum_b |b\rangle\langle b|\otimes\mathcal V_B(P_b\rho P_b^\dagger\otimes\tau_B).")
p("Let E<sub>i</sub> be the independent B-side logical wait/descent channel with its resource syndrome, O(p)-close to identity. Let Q<sub>tree,i</sub> be regenerated-bit Pauli noise and Q<sub>term,i</sub> be final-gate Pauli noise. Uniform Bell labels themselves implement the exact Pauli twirl:")
eq(r"K_i=Q_{{\rm term},i}\circ Q_{{\rm tree},i}\circ {1\over4}\sum_b\mathcal P_b^{-1}\circ E_i\circ\mathcal P_b.")
p("Each K<sub>i</sub> is an exact Pauli channel in the comparison; independent resources give their product. A Clifford-only controller is unnecessary, and there is no additional ideal twirl seed. Protected hybrids and 2N tree replacements cost ε<sub>FT</sub>+2Nq<sub>c</sub>(21p<sub>c</sub>)<sup>L</sup> in half-diamond distance.")
h("Clock synchronization is an interface requirement")
p("The classical roots and B's raw quantum output arrive at the same predetermined clock. Run their terminal paths in parallel; pad only while information is protected. Execute two always-scheduled native gates: CNOT from the regenerated X bit to B, then controlled-Z from the Z bit. This needs no ideal classical gate-selection device. Those gates, local SWAP and modeled switching exposure take bounded time and belong to K<sub>i</sub>. An early raw bit cannot wait through a growing descent at no cost.")
p("Discard the two byproduct controls and reset internal pool and Bell transcripts at paid cost. No signalling preserves the independent B marginal, while regenerated controls prevent old gauges from re-entering it. All pre-existing external records remain. This product-noise export, rather than an assumed product form of residual FT syndromes, supplies thermal precompensation.", "small")

# 9
page("8. A positive inverse-noise thermal source")
p("At most w checks touch one site, and each check touches at most d sites. Join sites sharing a check; the resulting graph has degree D≤w(d−1). A local Pauli channel K<sub>i</sub> acts on syndromes by commuting translations T<sub>i,a</sub>. Its nonidentity probability is at most q&lt;1/4. Fourier eigenvalues on the four-element Pauli group are at least 1−2q. Therefore")
eq(r"K_i^{-1}=b_{i,0}\left(I+\sum_{a\ne0}r_{i,a}T_{i,a}\right),\quad b_{i,0}\ge1,\quad\sum_{a\ne0}|r_{i,a}|\le{2q\over1-2q}\le4q.")
p("One proof is the Neumann series for K<sub>i</sub>−I, whose coefficient ℓ<sub>1</sub> norm is at most 2q; the identity coefficient is the average inverse Fourier eigenvalue and is at least one. A nonfaithful representation on the syndrome subspace causes no problem: map this full-group inverse to its translation representation.")
theorem("Theorem C: uniform positive preimages", "At fixed β and bounded incidence and coupling strength, sufficiently small q&gt;0 makes μ<sub>I</sub> = (∏<sub>i∈I</sub>K<sub>i</sub><sup>−1</sup>)π a strictly positive probability law for every set I, uniformly in N and the syndrome constraints. The theorem supplies a constructive local expansion and a polynomial sampler for the accepted history family.")
h("Signed connected-noise polymers")
p("For a connected site set C, sum all its nonidentity local labels:")
eq(r"z_C(s)=\sum_{a_i\ne0}\left(\prod_{i\in C}r_{i,a_i}\right){g(s+\sum_{i\in C}v_{i,a_i})\over g(s)},\qquad |z_C(s)|\le\theta^{|C|},")
eq(r"\theta={2q\over1-2q}e^{w\lambda_{\max}}.")
p("Nonadjacent components touch disjoint checks, so their energy ratios factor. The inverse law is exactly a signed hard-core polymer partition function:")
eq(r"{\mu_I(s)\over\pi(s)}=\left(\prod_{i\in I}b_{i,0}\right)Z_I(s).")
p("All inverses preserve total mass, so normalization is already one. Positivity is the central issue: coefficients can be negative, and a naive total-variation perturbation would grow with N. The next page establishes positivity without that extensive loss.")

# 10
page("9. Zero-free expansion and local influence")
p("Use the conservative condition θ≤[32e<sup>3</sup>(D+1)]<sup>−1</sup>. Scale every nonidentity r coefficient by a complex number z. On |z|≤2, activities are bounded by (2θ)<sup>|C|</sup>. Connected sets of size k through a fixed site number at most [e(D+1)]<sup>k−1</sup>. A convenient size-tilted rooted bound at z=1 is")
eq(r"U={e^2\theta\over1-e^3(D+1)\theta}.")
p("For a polymer C, all incompatible polymers meet its closed neighborhood. Their size-tilted activity sum is at most (D+1)|C|U&lt;|C|. The same inequality with room to spare holds at |z|≤2. The Kotecký-Preiss expansion [5] therefore converges absolutely with an extra exponential total-order margin, and its logarithm is analytic and zero-free throughout that disk.")
p("Along the real path z=0 to z=1, Z<sub>I</sub>(s) is real and begins at one. Since it never vanishes, it is positive. This proves every μ<sub>I</sub> is a probability law, uniformly in I, N and s. The connected-island method is closely related to the forward small-time Gibbs analysis of van Enter et al. [6]; the required use here is its signed inverse and all-prefix consequences.")
h("Local rather than global sensitivity")
p("Write Ψ<sub>I</sub>(s)=log Z<sub>I</sub>(s)=Σ<sub>A</sub>Φ<sub>A</sub>(s). If s,s′ differ on check set S, only clusters touching at most d|S| neighboring sites can change. Root the absolute cluster sum there. The exponential total-order margin also pays the number of check coordinates touched by a cluster. Uniformly over I and ambient check assignments,")
eq(r"|\Psi_I(s)-\Psi_I(s')|\le2dU|S|=\kappa|S|,")
eq(r"\sum_{A:\,A\ {\rm touches}\ S}\sup_s|\Phi_A(s)|\,|{\rm supp}_{\rm checks}A|\le wdU|S|.")
p("For the second inequality, a cluster of total order r touches at most wr checks; weight r by its available exponential tilt and apply the rooted KP estimate. These weighted bounds control how one history polymer influences another. A pointwise bound on μ/π alone would not suffice: that ratio can still vary exponentially with Nq.")

# 11
page("10. Polynomial evaluation of the correction")
p("Positivity is not an algorithm. We need to evaluate Ψ differences with a total error budget compatible with a polynomial-length sampler. Let P<sub>I</sub>(z;s) denote the exact signed subset polynomial obtained by scaling every nonidentity local coefficient by z. It factors over disconnected induced site components, and P<sub>I</sub>(1;s)=Z<sub>I</sub>(s). For any finite site set C, define the formal-series Möbius coefficient")
eq(r"f_C(z)=\sum_{B\subseteq C}(-1)^{|C-B|}\log P_B(z).")
p("Möbius inversion expresses log P<sub>I</sub> as the sum of f<sub>C</sub> over C⊆I. Factorization makes f<sub>C</sub> vanish for disconnected C. Every nonzero monomial in f<sub>C</sub> must involve every site of C; hence its first possible degree is |C|. Therefore the logarithm through degree ℓ can be computed by enumerating only connected site sets of size at most ℓ.")
p("There are N exp(O(ℓ)) such sets at bounded degree. For each, enumerate its subsets and at most four local Pauli labels per site, form P<sub>B</sub>, and take formal logarithms through degree ℓ. The per-set arithmetic is exp(O(ℓ)) with polynomial bit complexity. Energies and probabilities are evaluated to the finite precision required by the final budget.")
h("A uniform truncation error")
p("The zero-free disk |z|≤2 supplies a branch of log P<sub>I</sub> bounded by O(N) there, using the convergent cluster bound. Cauchy's coefficient estimate gives a geometric Taylor tail at z=1. Thus")
eq(r"\ell_{\rm noise}=O(\log(N/\delta))\quad\Longrightarrow\quad|\widehat\Psi_I(s)-\Psi_I(s)|\le\delta.")
p("The total runtime N exp(O(ℓ<sub>noise</sub>)) is polynomial at fixed graph degree and fixed physical parameters. The same algorithm handles all inverse subsets I and forward-noise versions. It does not enumerate the exponentially many full syndrome strings.")
p("If the sampler runs t updates, evaluate its transition probabilities to total variation error at most ε/(2t) each. Stepwise coupling adds at most ε/2. This pays numerical evaluation explicitly. Rejecting full Gibbs samples using sup(μ/π) would instead permit exponential rejection cost; that shortcut is not used.")
p("The method is a finite, checkable construction of the signed correction. It does not claim optimized exponents or practical runtime for the BDL family.", "small")

# 12
page("11. Sampling the softly interacting history gas")
p("Augment the accepted bounded-degree history graph by joining check variables affected by one physical site. Its degree Δ′ remains bounded. Enlarging adjacency only merges valid components, so E(γ)≥a|γ| persists by addition. The accepted nonzero-base witness still forces a component of size L*(N). A compatible polymer collection X now has weight")
eq(r"W(X)=e^{-\beta\sum_{\gamma\in X}E(\gamma)+\Psi_I(s(X))}.")
p("Deleting one polymer changes Ψ by at most κ|γ|. Set b=βa−κ, c<sub>h</sub>=(alphabet size−1)max(2,Δ′)<sup>2</sup>, and x=c<sub>h</sub>e<sup>−b</sup>. Deletion is injective, so a specified polymer has inclusion probability at most e<sup>−b|γ|</sup>. Counting connected assignments yields")
eq(r"\Pr[\exists |\gamma|>\ell]\le {M x^{\ell+1}\over1-x},\qquad \Pr[{\rm unstable}]\le {B x^{L_*(N)}\over1-x}.")
p("Here M counts history variables and B counts fixed base variables. Enumerate the K polymers of size at most ℓ and update one uniformly by its exact conditional heat bath. Its insertion odds depend on the whole current configuration through Ψ, so this is not the old factorized-polymer chain.")
h("Weighted path coupling proves rapid mixing")
p("Use distance Σ|γ| over differing occupancies. Adjacent configurations differ by ξ. Updating ξ removes the disagreement. Hard incompatibility creates expected weighted disagreement at most (Δ′+1)|ξ|U<sub>h</sub>. For compatible γ, the log-odds difference is at most four times the cluster terms touching both γ and ξ. Interchange sums and apply the weighted rooted bound to obtain soft influence at most 4wdU|ξ|U<sub>h</sub>, where")
eq(r"U_h={x\over(1-x)^2},\qquad [\Delta'+1+4wdU]U_h\le{1\over2}.")
p("The Bernoulli probability as a function of log odds has derivative at most the odds, already bounded by e<sup>−b|γ|</sup>. This earns both influence bounds. The expected distance contracts by 1−1/(2K); ordinary path coupling extends it to all configurations. Starting empty, distance to stationarity is at most M, so")
eq(r"t_{\rm mix}=O(K\log(M/\epsilon)),\qquad \ell=O(\log(M/\epsilon)).")
p("Bounded-degree enumeration and the preceding evaluator make the sampler polynomial, including truncation, mixing and arithmetic error. No unproved positive sampler or exponential rejection step is hidden in commissioning.", "small")

# 13
page("12. Explicit threshold and endpoint prefixes")
p("The existence of a size-independent threshold can be stated without hiding the competing low-temperature and control requirements. Choose β to satisfy the accepted holding theorem and")
eq(r"c_he^{-\beta a}\le {1\over32(\Delta'+1)}.")
p("With λ<sub>max</sub>=βJ<sub>max</sub>, define")
eq(r"\theta_0=\min\left\{{1\over32e^3(D+1)},{1\over64wd}\right\},\quad q_0=\min\left\{{1\over8},{\theta_0\over4}e^{-w\beta J_{\max}}\right\}.")
p("For q≤q<sub>0</sub>, θ≤θ<sub>0</sub>, U≤8θ, κ≤1/(4w), and 4wdU≤½. Therefore x≤e<sup>1/4</sup>/[32(Δ′+1)] and the sampler's influence bound is below ½. Choose the elementary rate p small enough for the AB recursion, classical-tree condition and effective q≤q<sub>0</sub>. Every condition is independent of N, duration and requested ε. These are sufficient mathematical constants, not practical threshold estimates.")
h("Compensated writes protect the logical input")
p("Start from μ<sub>all</sub>. Apply the independent physical endpoint errors one site at a time. After the noise on sites J, the syndrome law is exactly μ<sub>complement J</sub>. Every prefix has the same unstable-tail bound b<sub>0,N</sub>=Bx<sup>L*(N)</sup>/(1−x). A Pauli at a stable syndrome has trivial logical action in the protected decoder frame. Thus")
eq(r"\Pr[{\rm logical\ write\ discrepancy}]\le Nq\,b_{0,N}.")
p("The final syndrome marginal is exactly π. The source and all noise labels are coupled identically between the actual and ideal logical processes; only rare nonidentity logical actions are removed. This is a half-diamond bound against arbitrary references, not merely an average fidelity estimate. Subsequent channel contractivity preserves the once-paid discrepancy.")
h("Forward prefixes for read injection")
p("Independent raw-to-protected interfaces give product input channels. Protected Pauli seeds can be prepared while the memory remains in its counted passive hold; regenerated raw versions apply the pre-twirl at capture, and protected inverse seeds act after injection. This earns product Pauli noise, with all seed and waiting costs included. The forward polymer proof bounds every K<sub>J</sub>π. Deterministic read error is at most Nq b<sub>0,N</sub>. Adaptive capture requires the next page's hitting argument; its syndrome marginal need not be Gibbs.", "small")

# 14
page("13. Adaptive reads, retained seeds and reuse")
h("An anytime-read lemma")
p("Presample the independent read Pauli labels F for a fixed padded read template, independently of the bath trajectory. Let A<sub>F</sub> be the set of initial syndromes for which some nonidentity read Pauli encounters an unstable syndrome after its preceding prefix. The forward-prefix bound and a union bound give")
eq(r"\mathbb E_F\pi(A_F)\le Nq\,b_{0,N}.")
p("For a stationary continuous-time syndrome chain X with total exit rate at most r<sub>max</sub>≤CΓN and any fixed set A, hitting A by time T requires either starting in A or an entry jump. Stationarity equates total inward and outward flux, hence")
eq(r"\Pr[\exists t\le T:X_t\in A]\le\pi(A)+T\sum_{x\notin A,y\in A}\pi(x)Q(x,y)\le(1+r_{\max}T)\pi(A).")
p("Averaging over F bounds every adaptive read time τ≤T, even when τ uses retained syndrome records:")
eq(r"\Pr[{\rm logical\ read\ discrepancy\ at}\ \tau]\le Nq(1+C\Gamma NT)b_{0,N}.")
p("The presampling is a coupling of actual independent future faults. It requires a fixed noise template; choosing a new physical noise law after inspecting records would need its own argument. The proof does not assert equilibrium at τ and does not condition on a rare successful record.")
h("Campaign accounting and the exact record extension")
p("Keep the original compensated seed s, endpoint labels F and resulting syndrome s′=s+δF in the ideal comparison. The retained seed has law μ and can correlate with s′. Do not replace it with an independent π-labelled record. Logical inputs and references may themselves depend on s. The syndrome marginal at the start of each intrinsic passive path is π, which suffices for stationary-path coupling.")
p("For source-specific caps, write/read prefix terms and holding jumps give C[R Nq+ΓNT(1+Nq)]b<sub>0,N</sub>, where T is the sum of the declared caps. Choose a fixed slack x&lt;x<sub>1</sub>&lt;1 and b<sub>N</sub>=C x<sub>1</sub><sup>L*(N)</sup>. Since a polynomial times (x/x<sub>1</sub>)<sup>L*(N)</sup> is bounded, (1+Nq)b<sub>0,N</sub>≤C′b<sub>N</sub>. This earns Theorem A, with worse fixed constants and exponent.")
p("A source stream's joint approximation error is paid once. Each refresh still pays its preparation and allocated caps. Rejection or selection based on retained seeds is covered by a union over all offered candidates; the selected source is not assigned a Gibbs marginal for free. Accepted syndrome-preserving reuse remains separate: noisy decode/work/reload consumes the old background.", "small")

# 15
page("14. Full Gibbs preparation and free energy")
p("For a uniform logical subsystem, every endpoint logical Pauli is immaterial. Exact syndrome compensation therefore produces the full quantum Gibbs state exactly in the ideal comparison. Finite sampling, arithmetic, acquisition and implementation errors give the corresponding finite-ε trace-distance guarantee. This is a mixed-state preparation statement; it does not upgrade the separate coherent thermofield-double construction to a fixed-noise raw output.")
h("A quadratic excess free-energy bound")
p("Define K<sub>i</sub>(t)=(1−t)I+tK<sub>i</sub> and μ<sub>t</sub>=∏K<sub>i</sub>(t)<sup>−1</sup>π. Positivity holds along this path. Commutativity yields")
eq(r"\dot\mu_t=\sum_i B_i(t)\mu_t,\qquad B_i(t)=-K_i(t)^{-1}(K_i-I).")
p("Every B<sub>i</sub> has coefficient mass zero and coefficient ℓ<sub>1</sub> norm at most 4q for q≤1/8. For h<sub>t</sub>=log(μ<sub>t</sub>/π), the rooted expansion bounds its oscillation under one site translation:")
eq(r"{\rm osc}_i(h_t)\le2dwU(t)\le64dw\,tq e^{w\lambda_{\max}}.")
p("Differentiate relative entropy. The derivative of total probability vanishes, and B<sub>i</sub>'s zero coefficient mass lets us subtract h<sub>t</sub>(s) before bounding the translation difference. Therefore")
eq(r"{d\over dt}D(\mu_t\Vert\pi)=\sum_i\langle\mu_t,B_i(t)^*h_t\rangle\le256wdN\,tq^2e^{w\lambda_{\max}},")
eq(r"D(\mu_1\Vert\pi)\le128wdNq^2e^{w\lambda_{\max}},\qquad \Delta F=\beta^{-1}D(\mu_1\Vert\pi).")
p("The free-energy identity holds for decoder-frame states with the same logical density matrix in every syndrome sector: their entropy is syndrome entropy plus that common logical entropy. It is a state-function bound, not a circuit attaining reversible work. Control, copying, metrology, interconnect, reset, refrigeration and fabrication energy remain separate and can dominate it.")
h("A sharp elementary temperature limit")
eq(r"r=(1+e^\lambda)^{-1},\qquad \mu(1)={r-p\over1-2p}\ge0\quad\Longleftrightarrow\quad p\le r\quad(p<1/2).")
p("A thermal bit followed by a bit flip has this unique preimage. Thus no fixed nonzero noise allowance can remain uniform as β tends to infinity. The theorem is a fixed-temperature construction, not zero-temperature purification.", "small")

# 16
page("15. Unknown quantum ports have a sharp floor")
p("The operation accepts a qubit that may be entangled with an inaccessible reference. It does not estimate, copy or assume a classical description of that qubit. Noisy upward injection makes its O(p) boundary corruption an encoded logical channel and suppresses subsequent protected-code leakage. All later decoding and delivery are actual noisy circuits.")
theorem("Theorem D: irreducible raw-port error", "Let an unknown input cross a depolarizing raw cut D<sub>a</sub>, and let final local output cross an independent D<sub>b</sub>, where D<sub>a</sub>(ρ)=(1−a)ρ+aI Tr(ρ)/2. No intermediate channel R can have half-diamond error below ¾(a+b−ab), and R=id attains this bound.")
eq(r"\inf_R {1\over2}\|\mathcal D_b\circ R\circ\mathcal D_a-{\rm id}\|_\diamond={3\over4}(a+b-ab).")
p("Apply the channel to half a Bell pair. A replacement-by-I/2 event on either cut gives Bell overlap 1/4, even for a nonunital R. Consequently")
eq(r"F_e=(1-a)(1-b)F_e(R)+{1-(1-a)(1-b)\over4}\le1-{3\over4}(a+b-ab).")
p("The Bell projector distinguishes the output from the ideal state with trace distance at least 1−F<sub>e</sub>. Identity between the cuts yields depolarizing parameter a+b−ab, whose half-diamond distance to identity is exactly three quarters of that parameter. This proves both the lower bound and attainment.")
h("What accuracy is actually delivered")
p("A fixed nonzero raw component rate supports O(p)+ε, not arbitrarily small error through a fixed unprotected port. Encoded handoff can have accuracy ε but is a different, explicitly priced output format. The same floor applies to the strongest active competitor using those raw ports. Internal logical access and reuse do not reinsert the original unknown raw input; its one boundary error is not multiplied by the number of protected operations.")
p("At the N physical memory ports, local errors are tolerated by the inverse/forward syndrome construction. At the final useful single-qubit port, there is no larger code after delivery to correct its last unobserved error. These are distinct endpoints with different roles. Requiring zero raw error would turn a physically unavoidable boundary into an impossible specification.")
p("The theorem is a concrete lower bound for the stated depolarizing cuts, not a claim that every component noise law has exactly this coefficient. The completed interface uses a uniform O(p) bound for its specified iid Pauli primitives.", "small")

# 17
page("16. Acquisition with noisy preparation and readout")
p("The sole unknown component-noise law is a stationary one-qubit Pauli channel Λ, independently applied at every specified wire and measurement cut. Known native templates determine all reset, readout and record-capture faults from Λ, with no additional unknown SPAM channels. For each axis use paired noisy plus/minus preparations, t idles and the same capture template. Their contrast cancels any fixed affine capture offset:")
eq(r"m_t={\mathbb{E}[Y\mid+]-\mathbb{E}[Y\mid-]\over2}=A\lambda^t,\qquad\lambda=m_1/m_0.")
p("The amplitude A is bounded away from zero below a fixed error threshold and cancels in the ratio. Three axes identify the Pauli probabilities. Constant-duration trials and protected arithmetic give η accuracy with O(η<sup>−2</sup>log(1/δ)) samples. This identifies parameters inside the stationary model; it does not certify that model against arbitrary drift.")
h("Computing the effective endpoint law")
p("Each finite endpoint template defines a channel. Clifford paths admit stabilizer Monte Carlo. More generally, use protected quantum simulation of the known finite noisy circuit and explicit virtual decoder: decode the comparison Bell resource, discard its logical pair, reinsert an ideal logical Bell pair in the simulated target, retain the syndrome marginal, and simulate descent. Encoded Bell-basis measurements sample the resulting Pauli law. This is a known-state, classical-output computation, with its own faults suppressed; it is not an ideal physical step on the unknown input.")
p("Estimating channel i to variation η<sub>i</sub> takes O(η<sub>i</sub><sup>−2</sup>log(1/δ<sub>i</sub>)) trials times simulation cost. Product-channel error is at most Ση<sub>i</sub>. Compare actual K with K̂ on the valid state sampled for K̂; no extensive inverse norm is needed. Estimates and sampler outputs remain encoded when used by the preparation circuit, rather than crossing an unprotected classical port and being reimported as exact.")
h("Actual-check calibration without an ideal thermometer")
p("Selectively isolate J<sub>a</sub>(1−S<sub>a</sub>)/2 on its bounded support, with the same bath. A known gap g<sub>min</sub>&gt;0 makes its sector a two-state chain; hidden within-sector modes do not affect excitation. Wait at least g<sub>min</sub><sup>−1</sup>log(1/η<sub>r</sub>), then measure the check with its finite noisy Clifford circuit and complete capture template. Both affine coefficients follow from calibrated Λ:")
eq(r"r_a=(1+e^{\lambda_a})^{-1},\qquad m_a=c_a+a_a(1-2r_a).")
p("Subtract c<sub>a</sub> before debiasing by a<sub>a</sub>. This yields βJ directly. Per-check count O(e<sup>2λmax</sup>η<sub>λ</sub><sup>−2</sup>log(m/δ)) suffices; η<sub>λ</sub>=O(ε/m) controls Gibbs-law error. Resets, warmup, measurement, capture and arithmetic are charged. Selective isolation, stable switching and g<sub>min</sub> are extra access, not consequences of global on/off control. Without them this acquisition route is unavailable.", "small")

# 18
page("17. Deployment and the complete cost ledger")
p("Install a constant-size terminal code cell at each memory site, including finite bottom-gadget ancillas. A constant geometric dilation can accommodate these cells, with correspondingly larger fixed interaction range. The growing protected blocks, factories and classical pools reside in a separately paid active fabric. The model explicitly permits its nonlocal gates with stated latency, error and cost, at most one gate per qubit per clock.")
p("All output schedules are padded. Protected transport and waiting continue until synchronized local descent. The final correction and local SWAP have bounded duration. Reading begins all local injections together. If actual link latency grows, its idles, protected transport and occupied workspace must be included. BDL bounded density alone supplies no finite-speed local routing theorem.")
table([
 ["Resource", "What must be charged"],
 ["Fabrication", "Memory qubits, check order/range/density, positive coupling precision, terminal cells, isolatable couplers, switching and nonlocal link hardware."],
 ["Acquisition", "Component/SPAM estimation, effective-channel simulation, coefficient calibration, confidence budgets, drift revalidation and actual experimental time."],
 ["Commissioning", "History graph construction, signed correction evaluation, source sampling, protected encoder, Bell factories and classical pools."],
 ["Useful access", "Actual upward interfaces, protected decoding and logical work, refresh when used, raw delivery, transport and all waiting."],
 ["Maintenance", "Static Hamiltonian hardware, bath/cooling, retained records, controller availability when on, and restart after blackout."],
 ["Reset and reuse", "Fresh ancillas, pools and fine transcripts, per-refresh source preparation, per-use energy; only legitimately reusable setup is amortized."],
], [119, WIDTH-119])
eq(r"E=E_{\rm fab}+E_{\rm acquire}+E_{\rm commission}+E_{\rm access}+E_{\rm reset}+\int(P_{\rm static}+P_{\rm cool}+P_{\rm records}+P_{\rm ctrl})\,dt.")
p("Quantum spacetime is ∫N<sub>q</sub>(t)dt. Classical controller and record spacetime are separate quantities; active time is the full critical path. The history sampler is polynomial, protected simulation has its chosen threshold overhead, and the regenerator adds a polynomial number of encoded leaves and descents. These costs are not all polylogarithmic. Gate count alone does not determine thermodynamic energy.", "small")

# 19
page("18. A common-bath controller-blackout theorem")
p("A capability claim needs a comparison within one physical class. Fix local Pauli system-bath couplings and the spectral law below. If [H,P<sub>ω</sub>]=−ωP<sub>ω</sub>, the Davies jump coefficient is")
eq(r"g_\beta(\omega)={2\gamma\over1+e^{-\beta\omega}},\qquad g_\beta(-\omega)=e^{-\beta\omega}g_\beta(\omega),\qquad g_\beta\le2\gamma.")
p("The same law, temperature and coupling operators apply to both holding choices. The bath is unobserved: no purifying jump record or ongoing environment metrology is available. Every information-carrying quantum helper undergoes its stipulated holding channel; fresh decoding ancillas remain allowed. For BDL this bath satisfies the accepted holding assumptions. For H=0, all frequencies vanish and the exact channel is")
eq(r"\mathcal L_0(\rho)=\gamma\sum_{i,a=X,Y,Z}(a_i\rho a_i-\rho),\qquad \mathcal E_t=\mathcal D_{e^{-4\gamma t}}^{\otimes N},")
p("where D<sub>λ</sub>(ρ)=λρ+(1−λ)I/2. These are different energy-resolved generators under the same bath specification; interacting BDL holding has not been replaced by independent depolarization.")
theorem("Theorem E: size-independent blackout obstruction", "If all quantum memory degrees of freedom have H=0 and every active quantum controller is disabled for t≥log(3)/(4γ), the complete input-output channel is entanglement breaking, for any encoding, any N, any retained classical records and any subsequent decoding. Its half-diamond error from an unknown-qubit identity channel is at least ½.")
eq(r"\mathcal D_{1/3}(\rho)={1\over3}\sum_{a=X,Y,Z}\sum_{s=\pm1}\langle a,s|\rho|a,s\rangle\,|a,s\rangle\langle a,s|.")
p("This is measure and prepare. For 0≤λ≤1/3, D<sub>λ</sub>=3λD<sub>1/3</sub>+(1−3λ)D<sub>0</sub> is also entanglement breaking, as is its tensor power. Conditional on each retained classical record, it destroys reference entanglement; averaging and later local decoding cannot restore it. Every separable state has overlap at most ½ with a Bell pair, proving the stated distance lower bound.")
p("The passive register can exceed this blackout with its protective interactions left on. A competitor given the same passive hardware may adopt the same operation. Autonomous interacting correction, engineered dissipation, a quantum side memory and controllers left on are outside the H=0 blackout premise. The consequence concerns control availability, not a method-exclusive or universal resource advantage.", "small")

# 20
page("19. Strongest applicable competitors and prices")
p("Ordinary active fault tolerance already gives long storage at constant component error with noisy encoding/readout. It receives exactly the same gate set, cooling, routing, switching, metrology and input access. The new operation is compatibility with an actual thermal holding interval; it is not a new abstract active threshold.")
table([
 ["Existing method", "What it supplies; what remains distinct"],
 ["AB / local active FT [1,10]", "Long active computation at fixed error, protected controllers and ordinary encoded storage. During an H=0 controller blackout it faces Theorem E."],
 ["CFG I/O [2,3]", "Explicit physical ports and residual local-stochastic output noise; the newer qLDPC construction can have constant quantum-space overhead for stated workloads. It does not automatically provide independent thermal endpoint noise or local routing."],
 ["Precompensation [4]", "Known-state inverse-channel positivity tests and optimization. The new ingredients here are uniform Gibbs positivity, efficient constrained sampling, unknown logical references and noisy implementation."],
 ["Autonomous 2D correction [8]", "A fixed local update rule, hierarchical noisy classical control and quantum correction; continuous engineered dissipation. It is a strong autonomous competitor, not an externally clocked strawman."],
], [145, WIDTH-145])
p("The autonomous construction uses persistent engineered computation/correction, a distinct holding resource from a thermal detailed-balance Hamiltonian. If the task merely removes an external clock, it may already meet that goal. The blackout task here disables all active correction machinery while preserving static interactions and the bath. No impossibility for autonomous protected memories is claimed.")
h("Exact price-dependent comparison")
eq(r"E_P=A_P+TP_P,\quad E_A=A_A+TP_A,\qquad T_*={A_P-A_A\over P_A-P_P}\quad(P_A>P_P).")
p("This crossover applies only while the chosen designs and reliability targets are fixed. If P<sub>A</sub>≤P<sub>P</sub> and A<sub>P</sub>≥A<sub>A</sub>, there is no favorable crossover. Passive size sufficient for the certified lifetime grows roughly as [log(T/ε)]<sup>1/η</sup>, including the log N correction; active constructions also have T times a polynomial in log(T/ε), with different constants. These expressions establish no total-spacetime ordering.")
p("If passive maintenance is at least mN<sub>P</sub> and complete active holding power at most MN<sub>A</sub>, then N<sub>P</sub>/N<sub>A</sub>→∞ forces greater passive total energy, when setup is lower order. Zero active-control work during holding does not remove maintenance. No universal thermodynamic energy per gate has been assumed.", "small")

# 21
page("20. Stronger boundary: any noninteracting hold")
theorem("Theorem F: arbitrary one-site gaps do not remove the blackout bound", "In the same unobserved isotropic local-Pauli bath, let the static holding Hamiltonian on all information-carrying quantum systems be H=ΣH<sub>i</sub>. For t≥log(2)/(4γ), every encoded-and-decoded unknown-qubit channel has half-diamond error at least ¼, regardless of N, gaps, temperature, encoder, final readout or retained classical records. Bath-jump records and outside quantum storage are not supplied.")
p("Diagonalize each H<sub>i</sub>. Isotropy of the three Pauli couplings preserves the bath under that change of basis. The two transverse couplings give total upward plus downward population relaxation 4γ. They contribute coherence decay 2γ; the longitudinal zero-frequency coupling adds 2γ. Thus, up to the one-site Hamiltonian unitary, each holding channel has the exact form")
eq(r"\mathcal E_{i,t}(\rho)=\lambda\rho+(1-\lambda)\tau_i\operatorname{Tr}\rho,\qquad \lambda=e^{-4\gamma t},")
p("with τ<sub>i</sub> its Gibbs state. When λ≤½, this channel has a symmetric two-output extension:")
eq(r"\mathcal B_i(\rho)=\lambda\rho_A\otimes\tau_{i,B}+\lambda\tau_{i,A}\otimes\rho_B+(1-2\lambda)\tau_{i,A}\otimes\tau_{i,B}\operatorname{Tr}\rho.")
p("Every term is completely positive and the coefficients sum to one. Both marginals equal E<sub>i,t</sub>. Apply the product of these extensions after an arbitrary encoder, copy its classical record to both branches, and apply the allowed decoder separately on each branch. The unknown-reference/output state has a symmetric extension to two candidate outputs. Fresh decoding ancillas and arbitrary readout complexity do not change this fact.")
p("Let P<sub>RA</sub> and P<sub>RB</sub> be Bell projectors between a two-dimensional reference and each output. The sum P<sub>RA</sub>⊗I<sub>B</sub>+P<sub>RB</sub>⊗I<sub>A</sub> has operator norm 3/2. Equal marginals therefore have Bell fidelity at most 3/4. Measuring the desired Bell projector gives half trace distance at least 1/4 and hence the claimed half-diamond bound.")
h("The intervention's substantive meaning")
p("Arbitrarily large individual energy gaps, extra noninteracting qubits and cooling do not escape this bound in the stipulated common bath. Persistent protective interactions change the failure dynamics and are the resource used by the thermal register. The H=0 case has the stronger entanglement-breaking bound after log(3)/(4γ). The theorem does not exclude interacting autonomous correction or a competitor that adopts the same static protective memory.")

# 22
page("21. Finite checks of the two central mechanisms")
p("The thermal checks enumerate small constrained systems independently of the asymptotic proof. They verify inverse laws, all endpoint prefixes, a context-dependent heat-bath chain, connected-subset logarithms, and a reference-entangled five-qubit example. They do not estimate a BDL lifetime or hardware threshold.")
figure(ROOT / "precompensation_verification.png", 215)
p("Top figure: direct noise on a thermal product target causes extensive global mismatch; compensation is algebraically exact. The second panel propagates a finite transition matrix from two stated starts, and compares their larger TV distance with the uniform path-coupling bound. It is not a measured worst-case mixing curve.", "caption")
p("The classical checks separately exhaust finite voter identities and iterate the mixed local-stochastic bound. The reference process has exact leaves only as a proof device; the actual circuit has noisy leaves, voters, links and output. Its growing tree removes dependence on old history while retaining a known nonzero raw error.")
figure(ROOT / "classical_tree_regenerator.png", 215)
p("Bottom figure: the uniform and iterated coupling bounds versus the exact recursion for one explicit input law; 100 independent forests of 4096 outputs illustrate the remaining endpoint noise. Shading is twice the Monte Carlo standard error. These finite plots do not replace the arbitrary-reference proof.", "caption")

# 23
page("22. Verification scope and physical constants")
table([
 ["Finite independent check", "Observed result"],
 ["Seven-spin ring, 64 valid even syndromes", "Positive inverse; every prefix checked; final TV 3.58 × 10<super>−16</super>."],
 ["Eight-check chain, 36 interval polymers", "Detailed-balance residual 2.71 × 10<super>−20</super>; stationarity residual 1.21 × 10<super>−16</super>; influence bound 0.085663 &lt; ½."],
 ["Finite transition matrix", "Both stated starts reach TV ≤ 10<super>−6</super> after 540 updates; reversible spectral gap 0.0274304."],
 ["Order-four connected-subset logarithm", "Six selected syndromes, 90-digit arithmetic; largest selected error 6.46 × 10<super>−22</super>."],
 ["Five-qubit Gibbs and unknown-input outputs", "Gibbs half trace error 2.62 × 10<super>−16</super>; Bell-reference error 3.04 × 10<super>−6</super>, below 5q = 5 × 10<super>−6</super>."],
 ["Voter and disagreement witnesses", "8 ideal truth cases, 1024 input/fault complement cases, and 64 paired child configurations exhaustively checked."],
 ["Common-bath and broadcasting identities", "36 generator cases: residual ≤8.46 × 10<super>−16</super>. 9 extensions: marginal residual ≤1.20 × 10<super>−16</super>, minimum Choi eigenvalue −9.42 × 10<super>−17</super>; Bell-projector norm 1.5."],
], [214, WIDTH-214])
h("The published family is not a practical resource estimate")
p("BDL's published random-embedding choices are approximately 5.4 × 10<super>24</super> for the displayed scale and 6.6 × 10<super>10</super> for the density bound [7, §3.4]. Its displayed witness exponent is about η=0.01 [7, §6]. These unoptimized existence constants, the very small sufficient noise threshold at low temperature, the large AB base code and the polynomial regeneration pools remain in fabrication and execution costs. No practical crossover is inferred.")
h("The new scientific consequence and its boundary")
p("The interface converts fixed-rate imperfect control into a specified thermal starting law while preserving unknown logical information and references. It also exports history-independent calibrated raw noise from correlated protected classical syndromes. The endpoint law, sampled thermal source and anytime read are proved together; no unproved noisy dynamical basin is supplied as an input.")
p("The complete operation earns a controller-blackout capability with an explicit common-bath obstruction for every noninteracting holding Hamiltonian. It does not establish total-resource dominance, general noncommuting robustness, a finite-speed local 3D processor, or accuracy below a final raw cut. Earlier direct-prevention, productive-control/repair, burst-loss, first-event and reusable-register results remain archived at their original scopes. No new physical reduction between those classes is asserted.", "small")

# 24
page("Primary sources and proof provenance")
p("Sources are used at their stated hypotheses. The new bridges proved here are the signed Gibbs preimage and sampler, mixed local-stochastic regeneration and Bell composition, anytime-read hitting bound, and the resulting operational boundary. No priority claim is made for standard threshold, precompensation or polymer-expansion ideas.", "small")
refs = [
 ("[1] Aharonov and Ben-Or", "Fault-Tolerant Quantum Computation With Constant Error Rate. Measurement-free noisy primitives, spread and sparse-fault validity; same-code precursor used here.", "https://arxiv.org/pdf/quant-ph/9906129"),
 ("[2] Christandl, Fawzi and Goswami", "Fault-tolerant quantum input/output, v3. Many-to-one code algebra, pure preparation and destructive-measurement factorization, adjacent-level interfaces. Its ideal classical side is explicitly replaced here.", "https://arxiv.org/pdf/2408.05260v3"),
 ("[3] Christandl, Fawzi and Goswami", "Fault-tolerant interfaces for quantum LDPC codes, v2. Strong space-overhead comparator; residual local-stochastic noise and physical output timing.", "https://arxiv.org/pdf/2602.16948v2"),
 ("[4] Zhang, Li, Lu, Yuan and Duan", "Quantum error pre-compensation for quantum noisy channels. Prior known-state inverse-channel positivity and optimization.", "https://arxiv.org/pdf/2309.01434"),
 ("[5] Kotecký and Preiss", "Cluster expansion for abstract polymer models, Communications in Mathematical Physics 103, 491-498 (1986). Convergence and zero-free polymer expansion.", "https://doi.org/10.1007/BF01211762"),
 ("[6] van Enter, Fernández, den Hollander and Redig", "Possible loss and recovery of Gibbsianness during the stochastic evolution of Gibbs measures. Forward connected spin-flip island expansion; the required signed inverse is derived here.", "https://arxiv.org/pdf/math-ph/0105001"),
 ("[7] Balasubramanian, Davydova and Lin", "A passive self-correcting quantum memory in three dimensions. Published scale/density: §3.4; witness growth: §6. Accepted loader and process proofs remain separate archive inputs.", "https://arxiv.org/html/2605.10943v1"),
 ("[8] Dünnweber, Styliaris and Trivedi", "Quantum Memory and Autonomous Computation in Two Dimensions, v1. Local autonomous correction and noisy hierarchical control.", "https://arxiv.org/html/2601.20818v1"),
 ("[9] Horodecki, Shor and Ruskai", "Entanglement Breaking Channels. Measure-and-prepare characterization; the explicit common-bath calculations are proved here.", "https://arxiv.org/pdf/quant-ph/0302031"),
 ("[10] Gottesman", "Fault-Tolerant Quantum Computation with Local Gates. Local active-threshold comparator; geometric overhead is not inferred from nonlocal control.", "https://arxiv.org/pdf/quant-ph/9903099"),
 ("[11] Christandl and Müller-Hermes", "Fault-tolerant Coding for Quantum Communication. Physical interfaces and the correlated auxiliary-environment obstruction to naive iid boundary noise.", "https://arxiv.org/pdf/2009.07161"),
]
for name, desc, url in refs:
    p("<b>" + name + ".</b> " + desc + " " + link(url, url.replace("https://", "")), "small")
p("Reproduction: build_report.py creates this report. verify_precompensation.py, verify_blackout_boundary.py, classical_tree_regenerator.py, passive_route/check_static_tree.py and endpoint_route/check_interface_identities.py regenerate the finite checks. Companion notes give expanded proofs and operation/resource details. Imported third-party full texts are not required to rebuild it.", "caption")

PDF = OUT / "Astra_Noisy_Thermal_Interface.pdf"
def decorate(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8E0E4"))
    canvas.line(48, A4[1]-35, A4[0]-48, A4[1]-35)
    canvas.setFont("DSans", 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(48, A4[1]-26, "ASTRA  /  NOISY THERMAL QUANTUM INTERFACE")
    canvas.drawRightString(A4[0]-48, A4[1]-26, "5 NOVEMBER 2026")
    canvas.line(48, 39, A4[0]-48, 39)
    canvas.drawString(48, 26, "Constructive theorem under explicit physical contracts")
    canvas.drawRightString(A4[0]-48, 26, str(doc.page))
    canvas.restoreState()

doc = SimpleDocTemplate(str(PDF), pagesize=A4, rightMargin=48, leftMargin=48,
    topMargin=52, bottomMargin=52, title="A noisy interface to a long-lived thermal quantum register",
    author="Astra research construction", subject="Fixed-rate noisy quantum write-hold-read interfaces")
doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
(OUT / "Astra_Noisy_Thermal_Interface_text.txt").write_text("\n\n".join(plain), encoding="utf-8")
print(str(PDF))

