"""Build the bounded quantum factory research report."""
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
    rendered = text.replace("⁻¹ᐟ²", "<super>−1/2</super>").replace("¹ᐟ²", "<super>1/2</super>")
    rendered = re.sub(r'<(?!/?(?:b|i|font|super|sub|link|br)(?:\s|/?>))', '&lt;', rendered)
    for symbol in ("ℓ", "≼"):
        rendered = rendered.replace(symbol, '<font name="DSans">'+symbol+'</font>')
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
                    if level == 0 and inside.startswith("\\over", k) and (k+5 == len(inside) or not inside[k+5].isalpha()): split = k; break
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
    tex = re.sub(r"\\(mathcal|overline|mathbf)\s+([A-Za-z])", r"\\\1{\2}", tex)
    tex = re.sub(r"\\sqrt([0-9])", r"\\sqrt{\1}", tex)
    tex = tex.replace(r"\mathbf1", r"\mathbf{1}")
    tex = re.sub(r"\\frac([0-9])([0-9])", r"\\frac{\1}{\2}", tex)
    tex = re.sub(r"\\frac([0-9])(?=\{)", r"\\frac{\1}", tex)
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


# The artifact-operation marker ran once before this file was authored.

p("ASTRA RESEARCH / CONSTRUCTIVE RESOLUTION / 5 NOVEMBER 2026", "label")
p("Accurate thermal states from bounded quantum factories", "title")
p("Complete noisy-channel compilation removes accuracy-dependent quantum encoding", "h2")
p("<b>Completed consequence.</b> For every fixed-temperature, bounded-range one-dimensional qubit Gibbs family covered by the accepted uniformly mixed-block theorem, a sufficiently low fixed component noise rate permits unencoded global-state delivery to arbitrary trace accuracy using quantum modules of bounded width and duration. Neither bound grows with chain length or requested accuracy. Classical computation, calibration, programming and record management do grow and remain paid.")
eq(r"\forall N,\epsilon>0:\quad \frac12\|\rho_{\mathrm{del}}-\rho_{\beta,N}\|_1\leq\epsilon,\qquad S_Q,G_Q\leq\mathrm{const}(\beta,r)")
p("The central operation compiles full channels on arbitrary inputs and references. A fixed schedule visits every candidate interval. Selected intervals prepare full-rank blocks; inactive intervals enact a small product depolarizing channel. The latter has a positive Choi margin. A finite library of actual noisy operations can therefore implement both kinds of call by positive classical randomization, even when individual branches join sites across the sampled partition.")
p("<b>Concrete companion.</b> A six-layer nearest-neighbor Clifford fabric prepares connected thermal cluster chains entangled across every bulk cut. A sixteen-state transfer-cone proof gives an all-length positivity certificate at quantum depolarizing rate p≤1/3000. Protected classical control has its own threshold. This avoids the universal construction's enormous block and channel-net constants.")
p("<b>Status and limits.</b> These are research derivations with full proofs, independent audits and executable finite checks. The acquired implementation retains a stationary independent Pauli circuit law and specified local ports, resets and timing. There is no experimental claim, arbitrary-noise claim, priority certification or total-resource advantage over equally informed active preparation.")
p("The archive includes the technical proofs, executable checks, a finite-bit fallback and the complete previous research archive unchanged.", "small")

page("1. Full target and earned theorem")
p("The question was whether the accepted bounded ideal blocks can be turned into an actual noisy preparation apparatus without increasing quantum coherent size or lifetime. The hard case is a wrong partition mask or selector joining blocks that the desired ensemble separates. Full rank of the blocks alone does not describe that apparatus channel.")
theorem("Bounded-coherence Gibbs delivery", "Fix finite inverse temperature β and finite interaction range r. Let the digitally specified N-qubit Hamiltonian have uniformly bounded local interaction strength. There exist computable constants p*>0, factory width S, slot length G, a fixed finite gate library, and a bounded number C of quantum rounds, independent of N and ε, with the following property. Under the acquired stationary Pauli apparatus and protected classical control model stated below, every requested ε>0 can be attained at the scheduled raw output ports without quantum encoding whose size or lifetime grows with N or ε⁻¹.")
p("The quantum operation accepts no unknown logical quantum input. Its endpoint is the specified mixed state at a scheduled release time. All pre-existing external references may be retained: the fresh preparation is a replacement process with a paid error bound, after erasing or explicitly retaining the new correlated sampling records.")
eq(r"\rho_{\beta,N}=\mathbb{E}_{\mu}\bigotimes_{A\in\mathcal P_\mu}\tau_{\mu,A},\qquad |A|\leq B,\qquad \tau_{\mu,A}\succeq\eta I/2^{|A|}")
p("This ensemble is accepted input, not reproved here. Its constants B and η depend only on β,r. We retain fixed slack in η for numerical approximations and subsequent inverse channels. The inherited efficient classical sampler keeps its stated numerical convention. A separate exhaustive rational construction proves ordinary finite-bit computability; it is much more expensive.")
p("The bounded objects are local processing cells and each data qubit's circuit lifetime. The N-qubit output and its entanglement may span the chain; cells exchange data through fixed bounded paths. Permanently isolated quantum islands are not claimed. Ordinary fault tolerance may adopt the same state-specific construction and omit a code when it is unnecessary.")

page("2. Compatible apparatus and accounting")
p("The implemented route uses the inherited stationary apparatus: every outgoing wire of a native clocked operation has the same unknown one-qubit Pauli channel, independently across locations and uses. Resets, measurements, classical capture, idle slots, controlled gates and local release have specified finite templates subject to that law. Small fixed primitive error is a design promise; finite calibration cannot certify arbitrary stationarity or exclude unrestricted drift.")
table([
 ["Resource or interface", "What is actually supplied and paid"],
 ["Target", "Computable local Hamiltonian terms and temperature, with target-description rounding charged. Learning a separate physical Hamiltonian is not included for free."],
 ["Quantum factory", "Fixed bounded input/output ports and ancillas, a finite native universal gate alphabet, noisy reset, bounded routing, noisy opcode gates, idles and final delivery."],
 ["Classical apparatus", "Noisy Boolean gates, memory, copied outputs and links. Repetition-based protection and the accepted history-erasing trees carry accuracy-dependent overhead."],
 ["Timing", "Fixed finite-duration location templates. Mutable opcodes and enables enter their noisy implementation. The circuit law does not cover arbitrary unmodelled global clock excursions."],
 ["Acquisition", "Actual noisy preparation/readout/capture assays of the finite homogeneous component law, plus classical propagation through bounded factory circuits."],
 ["Geometry", "Quantum support stays within candidate intervals. Classical link duration, routing and protection remain paid; no free bounded-density embedding is inferred."],
], [116,WIDTH-116])
p("A faulty factory branch may couple all qubits within its candidate interval, including sites in different intended blocks. What remains an assumption is predetermined finite support and independence of distinct native locations. Arbitrary long-range crosstalk or dependence on another call's private history requires another acquired model.")
p("The mathematical channel-net theorem tolerates arbitrary small perturbations of complete menu maps. The implemented acquisition route is narrower. This preserves the earlier arbitrary-product-channel theorem without turning it into identification of an arbitrary unknown apparatus.")

page("3. Robust coverage by a finite noisy channel menu")
p("For a k-qubit input/output port, put d=2ᵏ and use normalized Choi matrices. The set of all channels is the compact convex body")
eq(r"\mathcal K_d=\{J\succeq0:\operatorname{Tr}_{\mathrm{out}}J=I_d/d\},\qquad J_0=I_{d^2}/d^2")
theorem("Interior channel compiler", "Let an ideal menu form an r-net of this body in Hilbert-Schmidt norm. Suppose the actual complete map for each menu word is within e of its ideal vertex in that norm. Every target channel with Choi matrix J*≥aI belongs to the convex hull of the actual menu whenever r+e<a.")
p("The proof uses relative affine geometry, so it applies to complete channels, including their action on an arbitrary reference. For any Hermitian perturbation X in the trace-preserving tangent space, ||X||₂≤a implies ||X||∞≤a and J*+X≥0. The entire relative ball of radius a around J* is physical. For a unit tangent functional u, the actual menu's support function obeys")
eq(r"h_{\mathrm{actual}}(u)\geq h_{\mathcal K_d}(u)-r-e\geq\langle u,J_*\rangle+a-r-e")
p("Separation of convex sets proves containment. Positive mixture weights are found by finite linear programming or certified finite-precision convex optimization. A physical channel is implemented on every shot; there are no negative estimator weights and no quantum postselection.")
p("Positive mixtures of actual noisy channels and convex quantum-program optimization are established tools [3,4]. The present use adds a uniform interior cover, an actual acquired noisy program interface and an overlapping fixed-support preparation architecture. It does not claim convex channel programming itself as new.")
p("The identity channel has a rank-one Choi matrix and no such margin. This is why the inactive operation is deliberately chosen inside the channel body. The construction does not contradict limits on a finite processor implementing every unitary exactly [4].")

page("4. Bounded hardware for the noisy menu")
p("A k-qubit channel has a Stinespring realization with at most 2k environment qubits. Approximate its dilation with a finite universal gate set. Compactness supplies a finite covering length L. Take all padded length-L circuit words on the fixed register set. At fixed B and interior margin, word length and gate-synthesis precision are constants.")
p("A fixed per-slot opcode interpreter avoids an enormous coherent switch over all menu words. Each slot applies a bounded-choice controlled gate on the same physical ports. Schedule, support and slot duration do not depend on the sampled partition. Opcode bits, enables, swaps, resets and padding are noisy parts of the complete implemented map.")
eq(r"\widehat\Phi_w=\text{complete CPTP map of word }w\text{ under the acquired model}")
p("The classical history-erasing interface supplies a noisy reference word with an explicitly computed law. Wrong words and incorrect local selections are included in the map. A union bound on the fixed number of locations and program bits gives e≤L₀p for a fixed constant L₀, including fixed waiting exposure. Choose p small enough to retain the channel-cover margin.")
p("The program's accurate information is carried by probabilities over a finite alphabet, generated by protected noisy classical computation. No continuous gate angle needs ε-dependent precision, and no larger coherent code is inserted as ε decreases.")
p("Each finite map is computed by ordinary classical dense-matrix propagation from the acquired primitive law. This can be enormously expensive in the fixed block parameter; it never requires a quantum simulator growing with N or ε. Arbitrary unknown-map tomography is not substituted for the acquisition contract.")
p("For numerical implementation, acquire a parameter vector in the certified design region, simulate its CPTP maps, and find nonnegative weights to a requested residual. The strict cover margin preserves feasibility. Residual Choi error converts to diamond error using the fixed port dimension.")

page("5. A fixed schedule replaces the random mask")
p("For each interval length k=1,...,B, color intervals by their starting position modulo k. Intervals in one color are disjoint. Execute every color, giving")
eq(r"C=\sum_{k=1}^{B}k=\frac{B(B+1)}2")
p("rounds. At uncovered boundary sites, execute singleton padding calls. Every data qubit has a paid channel in every round, including idles and release. Small chains may be treated directly as one bounded block. The call count obeys M≤CN, and more sharply O(NB+B³) with this padding.")
p("Sample a block prescription classically before fresh data are reset. At interval I, request a replacement if I is a sampled block; otherwise request a product depolarizer:")
eq(r"\mathcal R_{\omega_I}(X)=\operatorname{Tr}(X)\omega_I,\qquad \mathcal D_\gamma=(1-\gamma)\mathrm{Id}+\gamma\mathrm{Depol}")
eq(r"\text{inactive }I:\quad\mathcal D_\gamma^{\otimes |I|}")
p("The label influences probabilities over local menu words. It never controls which quantum wires are connected. Actual inactive branches may be entangling; their compiled average is the required product channel on all inputs.")
if (FIG / "fixed_schedule.png").exists():
    figure(FIG / "fixed_schedule.png", maxheight=238, caption="B=3, N=8 illustration. Every interval call executes. Green calls replace sampled blocks; gray calls implement product noise. Gray intervals may cross sampled boundaries. Pale squares are singleton boundary padding.")

page("6. Composition and precompensation")
p("Conditional on a sampled partition, each site belongs to exactly one active replacement. All other active replacements are disjoint from its block. After block A is replaced, only product depolarizing maps can touch it. Let tᵢ≤C count its later rounds. Define")
eq(r"\omega_A=\left(\bigotimes_{i\in A}\mathcal D_\gamma^{t_i}\right)^{-1}(\tau_A)")
p("Choose fixed γ in the accepted local inverse radius with spectral slack. An elementary sufficient choice, after reserving a working block floor η, is")
eq(r"\gamma\leq\frac{\eta}{2^{B+4}BC}")
p("The product inverse differs from identity by at most exp(4BCγ)−1 in diamond norm, leaving ωA≥ηI/(2d). This selects a conservative constant without reproving the accepted arbitrary-product inverse theorem.")
eq(r"J(\mathcal R_{\omega_A})\succeq\frac{\eta}{2d^2}I,\qquad J(\mathcal D_\gamma^{\otimes k})\succeq\frac{\gamma^k}{d^2}I")
eq(r"a=\frac{\min\{\eta/2,\gamma^B\}}{4^B}>0")
p("Both call types have this common Choi floor. Apply the finite menu with r+e<a. Conditional on the partition, independently draw a word for each call according to its positive weights. Complete-map equality remains valid when a call's input is correlated with earlier blocks or an external reference. Replacement followed by the planned product noise delivers the target block. Averaging the partition delivers the Gibbs state.")
p("This closes the missing composition. A factory check only on one initialized test state would not suffice when inactive calls overlap prepared blocks. Complete channel equality permits microscopic joining faults while controlling the full referenced process.")

page("7. Classical reliability and record erasure")
p("All increasing computation acts on classical basis bits. The corrected controller uses repetition five, two majority-refresh rounds per correction, and unshared input-correction/gate/output-correction rectangles. It retains a strict hierarchical invariant: at least four of five children are regular for the intended bit. One fresh bad lower rectangle is tolerated; badness requires two, giving pⱼ₊₁≤A pⱼ² below a fixed threshold. All voters, links, memory and resets count.")
p("After protected fanout, each copy is decoded by its own physical majority-five tree. A fresh tag occurs at a faulty voter or when at least two child/edge tags occur. Its probability obeys q_next≤v+10(q+e)², uniformly bounded by 2s for s=max(v,e)≤1/200. An untagged node tolerates one old exceptional child plus one fresh tagged child. Thus raw errors have a genuine local-stochastic bound q_c=O(p), uniformly over old strict gauges. The five-ary decoder is classical and has O(5ʲ) size at protection level j. The accepted ternary history eraser then gives:")
eq(r"\delta_{\mathrm{tree}}\leq Kq_c\alpha^h,\qquad \alpha<1,\qquad \text{leaves}=K3^h")
p("K is the total number of program bits. Choose h=O(log(K/ε)). Copying one faulty raw bit many times is never substituted for protected pool generation. Quantum data are not alive while increasing prefix computation, source sampling, arithmetic and routing are completed.")
p("The reference root law comes from the actual finite voter truth table and fresh link noise. Roots are scheduled next to their ports and wait only a bounded number of quantum slots. This waiting belongs to the complete menu map. Actual root errors are coupled to the reference word before channel composition.")
p("Sample labels and fine menu records are correlated with the output. If retained, the result specifies that cq extension rather than claiming decoupling. For record-free delivery, reset records locally after their last use; opcode/root resets occur inside padded calls. Reset followed by fresh bit noise erases the old record without producing a perfect surviving zero. Parallel reset hardware, cooling and erasure energy are paid. There is no growing post-preparation erasure wait.")

page("8. Acquisition, precision and total error")
p("Use the accepted noisy Pauli contrast assay. For each axis, prepare both signs through the real noisy templates, insert zero or one idle, and measure through the same noisy capture path. The half-difference obeys mₜ=Aλᵗ. The ratio m₁/m₀ identifies λ while cancelling stationary contrast A. Retain its nonzero visibility in the trial count.")
p("This identifies the homogeneous primitive law, not an unrestricted unknown preparation/measurement pair. Bounded factory circuits are then simulated classically. The tree reference recursion is contractive in the low-error interval, so its parameter sensitivity is uniform in tree height; calibration need not pay inverse precision proportional to every leaf.")
eq(r"\|\Phi_w(\theta)-\Phi_w(\widehat\theta)\|_\diamond\leq L_{\mathrm{cal}}\|\theta-\widehat\theta\|_1")
p("Lcal is fixed by the template and root recursion. Compute a positive mixture for the estimated maps and propagate error forward through the actual apparatus. A global inverse condition number never multiplies this calibration bound.")
eq(r"D(\rho_{\mathrm{del}},\rho_\beta)\leq\epsilon_{\mathrm{src}}+\epsilon_{\mathrm{cl}}+Kq_c\alpha^h+\frac{M}{2}(\epsilon_{\mathrm{map}}+L_{\mathrm{cal}}\eta_{\mathrm{cal}})")
p("D is half trace norm. Map approximation includes channel simulation, probability rounding and convex-program residual in diamond norm. Separate budgets sum to ε. Calibration precision ηcal=O(ε/(M Lcal)) uses O((M Lcal/ε)² log(1/δ)) bounded-duration trials, with visibility and capture constants. With probability at least 1−δ, the acquired calibration is valid; an unconditional bound adds δ.")
p("One calibration can serve a declared campaign at its supported precision. Fresh faults must obey the stationary model. Errors add across adaptive uses, with record handling each time. Arbitrarily increasing accuracy under unbounded reuse is not obtained from fixed-precision acquisition for free.")

page("9. What grows, and what stays bounded")
table([
 ["Quantity", "General construction"],
 ["Coherent factory width", "S(B,η), fixed in N and ε; includes bounded program/interpreter ancillas whenever coherent."],
 ["Quantum data lifetime", "At most CG native slots from fresh reset to local release, independent of N and ε."],
 ["Installed quantum hardware", "O(MS) in a direct parallel deployment, including O(N) output sites. Constants may be prohibitive."],
 ["Quantum executions", "O(MG) data-stage work, plus Qacq calibration probes and Qcoin one-qubit randomness probes. Both probe counts and resets are paid."],
 ["Classical source", "Inherited sampler in its numerical convention, or separately costed exhaustive finite-bit fallback."],
 ["Classical control", "K3ʰ leaves and O(K3ʰ) tree gates/links, h=O(log(K/ε)); protected-prefix, O(5ʲ) raw decoders per leaf, storage and actual routing costs are additional."],
 ["Acquisition", "O((M Lcal/ε)² log(1/δ)) shots under the finite homogeneous model. Additional independently unknown types add work."],
 ["Commissioning and reset", "Gate-library synthesis, wiring, parameter acquisition, controller bootstrapping, fresh data reset, transcript erasure and module reinitialization."],
], [130,WIDTH-130])
p("Elapsed time includes source computation, protected routing/synchronization, calibration, all actual randomness probes and the bounded data stage. A reusable one-qubit coin source has bounded coherence per shot, but its total number of shots is not free. Total spacetime counts all classical and quantum hardware during its actual waits. Energy is the sum of gates, links, memory-time, cooling, reset and erasure in a specified implementation. The circuit model supplies no joule values or fabrication yields.")
p("Generic constants are extremely unfavorable: a sufficient threshold is of order a/L₀ with a≤γᴮ/4ᴮ, while accepted B is already enormous. At range two and β=1, its first exponential has exponent about 5.0×10¹³, before later growth. This earns a resource-structure conclusion. The next explicit family avoids these universal constants; neither construction establishes total-resource superiority.")

page("10. Independent finite-bit closure")
p("The inherited efficient sampler and ordinary finite-bit execution remain separate. A fallback closes the whole bounded-quantum operation without querying the accepted source's unknown real weights.")
p("Let D=2ᴺ. Enumerate all interval partitions and rational positive-floor block states on a fine grid. Leaf trace resolution ε/(128ND) suffices. Mapping each accepted block to a nearby grid point gives a mixture with small global trace error and small entrywise real-plus-imaginary ℓ₁ error:")
eq(r"\|A\|_1\leq C(A):=\sum_{ij}(|\Re A_{ij}|+|\Im A_{ij}|)\leq2D\|A\|_1")
p("Compute the dense target Gibbs matrix by certified finite-bit exponentiation and normalization. Solve the rational LP minimizing C(ΣwⱼVⱼ−ρhat) over nonnegative weights summing to one, linearizing absolute values. The accepted representation proves a small feasible residual exists. Sample the rational solution using finite coins and a capped rejection routine.")
eq(r"\#\{V_j\}\leq2^N\left(\frac{C_{B,\eta}N2^N}{\epsilon}\right)^{C_{B,\eta}N4^B}")
p("Only the classical grid and probability precision refine. Every grid block retains the same working spectral floor, so the fixed palette realizes its precompensated replacement. No increasing quantum circuit is hidden here. Target coefficients and the floor must be computable with certified precision.")
p("The cost is enormous and is not a new efficient Gibbs sampler. It proves a complete finite-bit route while preserving the inherited numerical convention. The explicit connected entangled family below has an independent polynomial-bit construction with a small fixed quantum circuit.")

page("11. A connected entangled thermal chain")
p("Let U be the nearest-neighbor CZ product on an open chain and Kᵢ=UXᵢU†. Interior Kᵢ=Zᵢ₋₁XᵢZᵢ₊₁, with natural boundary terms. Consider")
eq(r"H=-\sum_iJ_iK_i,\qquad t_i=\tanh(\beta J_i)\in(1/2,11/20]")
eq(r"\rho_\beta=\sum_s\pi(s)|G_s\rangle\langle G_s|,\quad \pi(s)=\prod_i\frac{1+t_i(-1)^{s_i}}2")
p("Across each cut (i,i+1), the left restrictions of Kᵢ,Kᵢ₊₁ anticommute, as do the right restrictions. Each side's two-component expectation vector has norm at most one. Cauchy-Schwarz and convexity give ⟨Kᵢ+Kᵢ₊₁⟩≤1 for states separable across that cut. The Gibbs state has value tᵢ+tᵢ₊₁>1. Every nontrivial cut is entangled; this does not assert genuine multipartite entanglement under every decomposition.")
p("Run six data slots: noisy reset; CNOT loading from an actual classical root; H; the first CZ matching; the second CZ matching; terminal local delivery. Every outgoing data wire has independent Pauli depolarization: I with probability 1−p and each nonidentity Pauli with probability p/3. Unmatched sites have noisy idles. All quantum bonds are always scheduled; there is no random quantum mask.")
p("The roots carry a sampled preimage label law. Their independent reference errors are BSC(qᵢ), with qᵢ≤10p supplied by actual trees. The first two gates of the final majority voter finish before data reset; its final Toffoli coincides with reset, and the root immediately controls the next-slot adjacent CNOT. No raw wait is omitted.")
p("Thermal graph states, ideal constant-depth preparation and graph-label Pauli convolution are established [5]. The new construction inverts all these physical fault layers with a positive all-length source and closes its noisy loading, finite-bit sampling and acquisition.")

page("12. Derive the signed transfer source")
p("Put c=1−4p/3. The first three data fault layers give singleton label channels with Fourier eigenvalue c. After the first matching, each endpoint translates its pair's label subgroup. The two endpoints combine into a uniform-pair depolarizer with parameter c². An unmatched odd last site gains one extra singleton factor c.")
p("After the graph is complete, a Pauli at i translates the subgroup generated by eᵢ and eᵢ₋₁+eᵢ₊₁. The second matching and terminal faults combine into DGi(c²). All label convolutions commute. Invert singleton factors, group adjacent pairs, and absorb endpoint factors entirely within a pair.")
eq(r"u_* =\frac{11/20}{c^4(1-20p)},\qquad a_j\in\{c^2,c^4,c^6\}")
eq(r"f_j(x)=a_j^{-1}\pi_{u_{2j}}(x_1)\pi_{u_{2j+1}}(x_2)-\frac{a_j^{-1}-1}{4}")
p("These normalized pair factors are positive if (1−u*)²>1−c⁶. Their largest-to-smallest value ratio is at most")
eq(r"R=\frac{(1+u_*)^2-(1-c^6)}{(1-u_*)^2-(1-c^6)}")
p("Each remaining boundary has two inverse subgroup channels. For a=c², one inverse has identity coefficient α=(3+a)/(4a) and three coefficients −β, where β=(1−a)/(4a). The boundary link has at most sixteen translations and")
eq(r"b(0)>0,\qquad \frac{\sum_{z\ne0}|b(z)|}{b(0)}\leq\zeta=6r_0+9r_0^2,\quad r_0=\frac{1-c^2}{3+c^2}")
p("At odd endpoints some translations merge; positive terms increase the identity coefficient and the triangle inequality preserves the bound. The complete inverse is a constant-width signed transfer network: positive f factors at link-shifted arguments, multiplied by signed b coefficients and summed over links. The technical note gives the exact network and all small-chain cases.")

page("13. Uniform positivity and an explicit certificate")
p("For a forward transfer vector, use the cone")
eq(r"v(0)>0,\qquad\sum_{z\ne0}|v(z)|\leq\kappa v(0),\qquad\kappa=1/(2R)")
p("If the next local factor has minimum m and maximum at most Rm, the next identity component is at least b(0)m(1−κR)v(0). Its nonidentity absolute sum is at most b(0)ζRm(1+κ)v(0). The cone is invariant provided")
eq(r"\zeta\leq\frac1{4R^2+2R}")
p("Start at the identity vector. The final positive local contraction gives a strictly positive number for every full label string and every chain length. Inverse channels preserve mass, so the result is a probability law. This all-length induction does not extrapolate finite-chain numerics.")
eq(r"p_Q\leq1/3000:\quad R=12.3402337684\ldots,\quad\zeta=0.001333777712\ldots")
eq(r"\zeta<0.001577769990\ldots=1/(4R^2+2R)")
p("Endpoint inequalities were checked exactly with rational arithmetic. Monotonicity covers smaller p. N=1 is a positive singleton inverse and N=2 is the positive pair with parameter c⁶. The general construction's enormous block length and universal menu are absent.")
p("This is a quantum-fabric positivity bound. A common-rate apparatus requires p≤min{1/3000,pcl}, with pcl the actual classical threshold. A proved two-type specialization allows quantum depolarization pQ≤1/3000 and classical bit-flip rate pC≤min{pcl,pQ}; both are fixed and acquired by their own noisy idle contrasts. No classical threshold of 1/3000 is inferred from the quantum calculation.")
p("The noisy voter has seven outgoing locations. With link error at most p, its independent reference recursion satisfies F(q)≤7p+3(q+p)² and preserves [0,10p]. Actual history error is paid by the same coupled trees as in the general operation.")

page("14. Finite-bit sampling and acquisition")
p("The signed network has at most sixteen states per link. Prefix masses are constant-width contractions. Positivity alone does not justify inaccurate division by tiny prefix masses.")
p("For true child masses a,b and clipped approximants a′,b′ each within δ, the conditional distributions obey")
eq(r"(a+b)\,d_{\mathrm{TV}}\left(\frac{(a,b)}{a+b},\frac{(a',b')}{a'+b'}\right)\leq2\delta")
p("This remains true if both approximants vanish and any coin is used. A sequential hybrid sum over possible prefixes bounds total variation by 2ᴺ⁺¹δ. Set δ=εs/2ᴺ⁺³ and reserve coin-rounding slack. The total absolute signed weight grows at most exponentially in N; O(N+log(N/εs)) bits suffice. Direct contraction uses O(N²) fixed-size operations; cached suffixes reduce this to O(N). Both have polynomial ordinary bit cost.")
p("Acquisition also avoids a tree-size penalty. On the invariant interval, |F′(q)|≤87p≤0.029. Changing one homogeneous component probability by η changes a voter-plus-links update by at most 10η. Hence")
eq(r"|q_h(p)-q_h(\widehat p)|\leq\frac{10|p-\widehat p|}{1-0.029}")
p("uniformly in tree height. Prepare the positive source for the estimated parameter and couple the two forward apparatus laws from that same source. Six data layers plus the roots give")
eq(r"D(\rho_{\mathrm{actual}},\rho_{\mathrm{estimated}})\leq N\left(6+\frac{10}{1-0.029}\right)|p-\widehat p|")
p("The boundary-safe bound above gives O((N/ε)² log(1/δacq)) shots. At fixed positive quantum/classical rates, a stronger comparison uses relative entropy of the independent fault histories. For F native faults and K reference roots, the forward trace error is at most sqrt([F KL(P||Phat)+K KL(Bern(q)||Bern(qhat))]/2). On an acquired compact positive-rate interval this needs parameter precision O(ε/√N), hence only O(N ε⁻² log(1/δacq)) shots, with inverse-rate and visibility constants retained. The new forward-metrology note gives the proof and coarse-commissioning cost; the source is held fixed during this comparison.")

page("15. Decisive checks and useful failure")
h("Complete-channel overlap test")
p("A two-qubit test contains 482 explicitly constructed CPTP menu maps. Its toy maps include an 8% correlated CZ branch, a 3% noisy-selector depolarizing fallback and 1% terminal local depolarization. Positive LPs realize an inactive product depolarizer and a full-rank replacer, with an entangling branch required to have nonzero weight in both mixtures.")
table([
 ["Executed check", "Result"],
 ["Entangling-branch negativity on the plus-state product", "0.40718"],
 ["Entangling weight: inactive / replacement mixture", "0.00860 / 0.04637"],
 ["Inactive / replacement normalized-Choi trace residual", "1.78×10⁻¹⁶ / 2.08×10⁻¹⁶"],
 ["AB replacement then BC inactive call, full ABC reference", "Choi trace residual 7.25×10⁻¹⁶; diamond upper bound 5.80×10⁻¹⁵"],
], [290,WIDTH-290])
p("This verifies the composition on referenced inputs. Its inactive channel has γ=0.9, well inside the channel body. It is not an 8% native threshold for the small-γ all-family construction and is not a hardware experiment.")
h("Exact failure of an overly noisy simple fabric")
p("For the same six-layer graph circuit at p=1/200, root BSC p, target t=11/20 and N=8, exact rational Walsh inversion gives three negative probabilities, with minimum −2.6064203783944344×10⁻⁷. The input-label-only architecture fails there. Coherent inputs cannot fix that same circuit's required negative input diagonal, because its graph-basis output diagonal depends only on the input diagonal.")
p("This is a boundary of the specified fabric, not a general impossibility. A separate audit rejected the first repetition-three arbitrary-gauge export argument. The repaired repetition-five/two-refresh controller passed 16,352 arbitrary-input validity cases and 6,132 one-input-error-plus-one-fault cases in its base-gadget check. The strict recursive invariant and fresh decoder tags are proved separately. The rejected argument remains documented; finite checks supplement the analytic proofs.")

page("16. Strongest same-access comparisons")
table([
 ["Existing method", "What it supplies / comparison"],
 ["Ideal block preparation [1]", "Exact bounded contiguous block mixtures and constant ideal depth. No ideal-depth advantage is claimed. The new operation closes actual noisy partition/program composition."],
 ["Quantum DS sampler [2]", "N polylog(N/ε) ideal gates and classical operations at fixed physical parameters. This is a stronger ideal complexity benchmark; noisy raw-state delivery needs an implementation bridge."],
 ["Precompensation and channel programming [3,4,6]", "Known-channel preimages, positive versus signed mixtures, and convex program optimization are established. Uniform interior coverage and this complete fixed-support composition are the deduction here."],
 ["Graph-noise tailoring [5]", "Graph-diagonal convolution is established. Main tailoring assumes noiseless operations; noisy detection uses estimator mitigation. Sparse global noise support is not implied by fixed positive local noise."],
 ["Ordinary FT / qLDPC [7,8]", "Protected preparation and gradual raw interfaces, with constant-space results in the stated regimes. Generic residual local-stochastic noise need not be the known law required for positive inversion. The comparator may adopt this state-specific compilation."],
 ["Autonomous correction [9]", "A separate active/dissipative cellular-automaton capability. Its source, controls and cooling cannot be identified with this apparatus without a reduction."],
], [120,WIDTH-120])
p("Give every comparator the same target information, gate alphabet, fabrication law, reset/cooling, acquisition, switching, timing, links and output access. No polylogarithmic space lower bound is attributed to current qLDPC methods. No conclusion follows that our classical trees and quadratic metrology beat their total spacetime or energy.")

page("17. Broad deductions and exact boundaries")
h("A reusable structural principle")
p("After the accepted ensemble is supplied, no thermal identity enters the compiler. Any described ensemble of uniformly full-rank bounded factors over a bounded-round catalogue of finite-support cells admits this replacement/product-noise architecture. Gibbs chains provide a broad noncommuting family. Other geometries need their own catalogue and ensemble theorem.")
h("Accuracy can be carried by classical probabilities")
p("For these known mixed targets, arbitrary global trace accuracy does not force larger coherent error-correcting blocks, longer quantum data lifetime or increasingly precise analog gates. Fixed quantum templates suffice; sampling, metrology and reliable classical control carry increasing precision. This is a sufficiency result. An equally informed preparer can make the same choice.")
h("Restrictions removed by construction")
p("No dynamically perfect block mask, ideal final selector, growing quantum controller or passive holding bath is used. Wrong within-call coupling across intended blocks is included. The explicit cluster family additionally avoids the enormous universal quantum library and uses fixed nearest-neighbor quantum gates.")
h("Substantive assumptions that remain")
p("Finite temperature and local rank margin, known native actions, the acquired stationary independent Pauli law, real reliable classical machinery, reset/cooling, finite support and timing, source computation and raw output access remain assumptions or costs. There is no bridge to arbitrary fabrication error, arbitrary-channel learning, unknown entangled-input transfer, a pure state or purification, long storage, or laboratory cost superiority.")
p("The accepted earlier process/memory, noisy boundary, product-channel, finite-bit, dimer, thermodynamic-limit and assay-programming results remain at their scopes. Their full archive is preserved byte for byte. The useful failed graph inverse is retained alongside the positive result.")

page("18. Primary sources and reproducibility")
refs = [
 ("[1] Pilatowsky-Cameo, Styliaris, Bakshi and Malz. One-dimensional quantum Gibbs states in constant circuit depth (2026).", "https://arxiv.org/abs/2609.35973"),
 ("[2] Rouze and Stilck Franca. Rapid mixing of Gibbs samplers via quantum Dobrushin-Shlosman conditions (2026).", "https://arxiv.org/abs/2610.03578"),
 ("[3] Jin, Zhang, Xu and Fan. Noisy Probabilistic Error Cancellation and Generalized Physical Implementability, v2 (2025).", "https://arxiv.org/html/2409.01000v2"),
 ("[4] Banchi, Pereira, Lloyd and Pirandola. Convex optimization of programmable quantum computers (2020).", "https://arxiv.org/abs/1905.01316"),
 ("[5] Park, Sun and Jeong. Low-overhead tailoring and learning of noise in graph states, v3 (15 October 2026).", "https://arxiv.org/html/2503.12870v3"),
 ("[6] Zhang, Li, Lu, Yuan and Duan. Quantum error pre-compensation for quantum noisy channels, PRA 106, 042440 (2022).", "https://arxiv.org/abs/2309.01434"),
 ("[7] Christandl, Fawzi and Goswami. Fault-tolerant quantum input/output, v3 (2025).", "https://arxiv.org/abs/2408.05260"),
 ("[8] Christandl, Fawzi and Goswami. Fault-tolerant interfaces for quantum LDPC codes, v2 (29 September 2026).", "https://arxiv.org/html/2602.16948v2"),
 ("[9] Quantum Memory and Autonomous Computation in Two Dimensions, v3 (2026).", "https://arxiv.org/html/2601.20818v3"),
 ("[10] Aliferis, Gottesman and Preskill. Quantum accuracy threshold for concatenated distance-3 codes (2006). Classical gadget application and export proved separately in the control note.", "https://arxiv.org/abs/quant-ph/0504218"),
]
for label, url in refs:
    p(label + " " + link(url, url), "small")
h("Reproducibility package")
p("The archive gives the complete compiler and classical-control proofs, independent audits, finite-bit fallback, explicit cluster cone and exact constants. Checks reproduce the channel-overlap example, rational positivity receipt and failed inverse. Source conventions and finite numerical evidence remain separate. The forward-metrology note gives the sharper positive-rate shot bound; the boundary-safe acquisition bound is retained.", "small")
p("The previous archive is unchanged. No predecessor proofs were recertified this round. No experiment, external worker, repository publication, outreach or spending was performed.", "small")

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8E0E4"))
    canvas.line(48, 39, A4[0]-48, 39)
    canvas.setFont("DSans", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(48, 25, "Astra | Bounded quantum factories | Research derivation")
    canvas.drawRightString(A4[0]-48, 25, str(doc.page))
    canvas.restoreState()

report_path = OUT / "Astra_Bounded_Quantum_Factories.pdf"
doc = SimpleDocTemplate(str(report_path), pagesize=A4,
    rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=54,
    title="Accurate thermal states from bounded quantum factories",
    author="Astra research construction", pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT / "report_text.txt").write_text("\n\n".join(plain))
print(report_path)
