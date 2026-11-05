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


# New PDF operation marker ran before this file was authored.
p('ASTRA RESEARCH / FOUNDATIONAL BOUNDARY / 5 NOVEMBER 2026', 'label')
p('When finite temperature does not protect a quantum output', 'title')
p('A connected, gapped, product-ground Gibbs family with no fixed final-port noise tolerance', 'h2')
p('<b>Resolved question.</b> Do finite temperature, finite-range interactions, uniformly mixed local marginals and a trivial uniformly gapped ground state guarantee a size-independent tolerance to an imperfect quantum output port? They do not. The construction here gives a connected two-dimensional family for which independent errors on selected single-qubit ports make every delivered state asymptotically orthogonal to the Gibbs target, even with perfect preparation beforehand.')
eq(r'\inf_\sigma D\!\left(\Lambda_p^{\otimes m}(\sigma),\rho_m\right)\longrightarrow1,\qquad 0<p<\frac12.')
p('The infimum allows every upstream density operator, including arbitrary entanglement across the device. The last unobserved root channel is Λₚ(σ)=(1−p)σ+pXσX. The target uses nearest-neighbor qubit interactions of norm at most one, a unique product ground state, a gap at least one and a fixed inverse temperature β=12.')
p('<b>Consequence.</b> Preparation complexity and physical delivery feasibility are distinct. Unlimited fault tolerance, calibration and upstream computation cannot place an output outside the image of its last channel. A quantitative family requires the physical output error to decrease as a power of total device volume to retain even fixed global trace accuracy.')
p('<b>Closest prior result.</b> Pettinari’s recent weak-Gibbsianity counterexample already implies exponential exact endpoint fragility. This report adds the positive gapped product-ground construction, a normalized witness, connected amplification against arbitrary upstream entanglement and a fixed interaction pattern that fails for every nonzero port rate. Precompensation and imaginary-time operator growth are established machinery.')
p('This is a mathematical boundary, not a laboratory capability or a total-resource advantage. Conservative constants are extremely unfavorable. The accepted bounded-factory operation and all predecessors are preserved unchanged at their actual scopes.', 'small')

page('1. The full theorem and endpoint')
theorem('Connected strong converse', 'For every fixed 0<p<1/2, an explicit connected square-lattice qubit Gibbs family at β=12 has the following properties: degree at most three; positive local terms of norm at most one; unique product vacuum; spectral gap at least one; and trace distance tending to one between its target and every output of independent final root bit-flip channels. All other ports may be perfect.')
theorem('One pattern for every rate', 'One fixed computable aperiodic connected interaction pattern, independent of p, has the same conclusion along its consistent growing finite-volume restrictions, for every fixed p in (0,1/2). For J cells it has O(J) occupied qubits and a containing rectangle of O(J^(4/3)) lattice sites. Translation invariance is not claimed for this connected theorem.')
p('The final faults are independent between selected roots and independent of the upstream system and records. They are unobserved. The preparer may know the exact target and noise law, use arbitrary ideal encoders, ancillas, cooling, nonlocal links, active correction, classical computation and postselection, and prepare an arbitrary correlated state. All such choices yield a density operator σ immediately before the last channel. Earlier postselection merely selects another such σ.')
p('The target is the actual unencoded physical Gibbs state at release, in global trace distance. A recovery after the last noise, an encoded output, a fault flag, a different target, or an observable-estimation task changes the contract. Target-preserving analog thermalization that avoids this output map also changes the contract. No universal impossibility for analog Gibbs preparation is asserted.')
p('This comparison grants all upstream acquisition, preparation, reset, switching, routing, synchronization and computation for free. Impossibility under that stronger access implies impossibility after their real costs are imposed. It does not establish a resource advantage for a different apparatus. The distinguishing measurement is a mathematical witness; its inexpensive physical implementation is not presumed.')

page('2. Exact feasibility of a noisy port')
p('For a full-rank target ρ and Hermitian unitary U, let Λₚ=(1−p)Id+p Adᵤ, 0<p<1/2. Since Adᵤ²=Id, the only possible preimage is')
eq(r'\sigma_p=\frac{(1-p)\rho-pU\rho U}{1-2p}.')
p('Its trace is one. Conjugating its positivity condition by ρ⁻¹ᐟ² gives the exact threshold')
eq(r'p\le p_{\max}(\rho,U)=\frac1{1+\kappa},\qquad\kappa=\|\rho^{-1/2}U\rho^{1/2}\|^2.')
p('For ρ=e⁻ᵝᴴ/Z the partition function cancels:')
eq(r'\kappa=\|e^{\beta H/2}Ue^{-\beta H/2}\|^2,\qquad \log\kappa=D_{\max}(U\rho U\|\rho).')
p('This specializes established error-precompensation image and SDP machinery [1]. A positive inverse is a mathematical state; that fact alone does not supply its physical synthesis. Conversely, a negative inverse rules out every preparation protocol before the specified endpoint.')
h('The mechanism')
p('The relevant stability notion is operator order, measured by a worst-direction probability ratio. A local change can have bounded energetic cost and bounded ordinary relative entropy while changing a rare global quantum direction by an exponentially large ratio. Local full rank does not control that ratio uniformly in volume.')
h('Depolarizing outputs are also covered')
p('For Depₚ=(1−p)Id+(p/3)(Adₓ+Adᵧ+Ad_z), 0<p<1/2, factor off a bit-flip channel of rate q=p/4. Inverting the classical Pauli convolution leaves nonnegative coefficients: the smallest potentially problematic numerator is (1−q)p/3−q(1−p)=p/12+p²/6>0. Thus Depₚ=Λ_q∘R for a Pauli channel R, so its image lies inside the Λ_q image. The theorem applies with q. This proved factorization does not imply unrestricted noise robustness.')

page('3. A physical planar cell')
p('Start T₀ with one root. At level h, put L=2^(h−1), draw horizontal paths from the root to (±L,0), then vertical paths to (±L,±L), and attach four translated Tₕ₋₁ trees. Subdivide every path into unit square-lattice edges. The subtrees lie in disjoint open quadrants. Each tree meets its vertical axis only at its root, so incoming paths never cross it.')
eq(r'n_h=3(4^h-2^h),\quad N_h=n_h+1,\quad A_h=(2^{h+1}-1)^2=\frac{4N_h-1}{3}.')
p('Here nₕ is the number of edges, Nₕ the occupied qubits and Aₕ the containing-square sites. Maximum degree is three. The geometry pays for all subdivisions and area; it does not use an abstract tree with free long links.')
figure(ROOT.parent/'results'/'planar_cell.png', maxheight=342, caption='Figure 1. The h=3 cell has 169 qubits and 168 unit-length edges. The empty vertical axis provides a physical corridor for the connecting wire. The root is the selected noisy output port.')
p('The construction is not translation invariant. The local interaction coefficients, however, are fixed and do not require increasing precision as the cell grows.', 'small')

page('4. Positive Hamiltonian and tree histories')
p('Orient edges away from the root and set nᵥ=(I−Zᵥ)/2. Define')
eq(r'H_h=\sum_v n_v+\frac12\sum_{u\to v}n_u(I+X_v).')
p('Every displayed term is positive and has norm one. Every term annihilates the vacuum. Since H≥Σnᵥ, the vacuum is the unique ground state and the gap is at least one. Also ‖H‖≤2n+1. The interactions overlap and do not commute. A product of onsite Z gates changes the off-diagonal signs, making this Hamiltonian stoquastic; a sign problem is not needed for the obstruction.')
p('Let s be the root-only occupied state and F the all-occupied state. All computational-basis entries of H are nonnegative. Each parent-before-child activation order contributes 2⁻ⁿ to ⟨F|Hⁿ|s⟩. If sᵥ is the descendant-subtree size, the rooted-tree hook formula gives n!/Pₕ orders, where Pₕ=∏ᵥ≠root sᵥ. Hence')
eq(r'\langle F|H^n|s\rangle\ge\frac{n!}{2^nP_h},\qquad P_h\le16^n.')
p('The count follows by recursively interleaving the child-subtree orders. With N=Nₕ₋₁ and L=2^(h−1), the exact product recurrence is')
eq(r'P_h=P_{h-1}^4\left[\prod_{k=0}^{L-1}(N+k)\right]^4\left[\prod_{k=0}^{L-1}(2N+2L-1+k)\right]^2.',11)
p('Vertical connector descendant sizes are at most 3·4^(h−1), horizontal ones at most 6·4^(h−1). Summing scale contributions gives log₂(Pₕ)/nₕ≤2+log₂3+1/3−2h/(2ʰ−1)<4. This establishes the explicit constant 16.')
p('Lattice-tree factorial histories and complex-time amplification are primary machinery [2–4]. The positive terms preserve the activation mechanism while forcing a product ground state and uniform gap.')

page('5. A normalized Perron witness')
p('Root occupation commutes with H. In its root-one sector, H is irreducible, nonnegative and has positive diagonal. Its positive Perron eigenvector ψ is coordinatewise increasing. To see this, start power iteration from the constant positive vector. Onsite multiplication preserves nonnegative increasing functions, and an edge acts as xᵤ[f(x)+f(x with child v flipped)]/2. The bracket is independent of the child bit and increasing in the others. Thus the same cone is preserved.')
p('The sector is connected: activate all sites, then deactivate unwanted ones from leaves toward the root. Since the all-occupied entry is largest, and the sector dimension is 2ⁿ,')
eq(r'\psi(F)\ge2^{-n/2},\qquad 1+\frac32n\le E\le2n+1\le3n.')
p('The energy lower bound is the all-occupied diagonal Rayleigh quotient. Apply Hⁿ between s and ψ, use the activation bound, and n!≥(n/e)ⁿ. This gives')
eq(r'r=|\langle s|\psi\rangle|^2\ge A^{-2n},\qquad A=96e\sqrt2.')
p('The vacuum has energy zero and Xroot maps it to s. Therefore')
eq(r'\kappa\ge r e^{\beta E}\ge e^{\beta+g_\beta n},\qquad g_\beta=\frac32\beta-2\log A.')
eq(r'\frac1{1+e^{\beta(2n+1)}}\le p_{\max}\le\frac1{1+e^{\beta+g_\beta n}}.')
p('At β=12, gᵦ=6.1781564365…>0, so −log pmax=Θ(N). The lower bound uses κ≤exp(β‖H‖). It describes mathematical inverse positivity, not an attaining physical preparation algorithm.')
p('The simpler single Taylor-term argument only has a useful base at β>64. A separate residence-time improvement gives exact-radius collapse already at β=8. The main normalized-witness theorem uses β=12, and no weaker temperature restriction is substituted for it.', 'small')

page('6. A gap for approximate delivery')
p('Put P=|ψ⟩⟨ψ| and Q=Xroot P Xroot. They have orthogonal root-occupation supports. Define O=(1−p)P−pQ. Its outcomes are −p, 0 and 1−p, an interval of length one. Direct calculation gives')
eq(r'\Lambda_p^*(O)=(1-2p)P\succeq0.')
p('Every obtainable output has nonnegative expectation of O, regardless of its input. The Gibbs target has a negative expectation: the P contribution is e⁻ᵝᴱ/Z, whereas the vacuum component of Xψ contributes at least r/Z to Q. Since H≥Σnᵥ, eigenvalue min-max gives Z≤(1+e⁻ᵝ)ⁿ⁺¹. Thus')
eq(r'\operatorname{Tr}(\rho O)\le-\delta,\qquad \delta=\frac{pA^{-2n}-(1-p)e^{-\beta(1+3n/2)}}{(1+e^{-\beta})^{n+1}}>0.',12)
p('The partition-function bound uses scalar monotonicity on ordered eigenvalues. It does not assume the false operator monotonicity of matrix exponentiation. For every fixed p>0, some fixed cell has δ>0. At fixed β, an eligible cell has n=O(log(1/p)); its inverse margin is bounded by a fixed power of 1/p, with extremely unfavorable constants.')
h('The entangled-input issue')
p('Apply the final independent root channels to M cells, with an arbitrary joint input. Measure the Oᵢ successively. Conditional on earlier outcomes, the remaining cell is still the image of its own channel: operations on other cells commute with that channel and only condition its input. Hence E[Yᵢ|past]≥0 even with arbitrary upstream entanglement. Conditional Hoeffding bounds the output probability of ΣYᵢ≤−δM/2 by exp(−Mδ²/2). For independent target cells, the reverse event has the same upper bound.')
p('This argument closes the gap between a formal nonpositive inverse and a macroscopic approximation obstruction. It remains to connect the target cells through actual interactions without losing the uniform negative conditional mean.')

page('7. Connecting the target without losing the proof')
p('Align identical cell squares above y=2. Run occupation-qubit wires downward from each root through its empty vertical axis to a horizontal spine at y=0. Add onsite n_w terms and positive diagonal nᵤnᵥ couplings on wires and root attachments. Degree remains at most three. Every edge is a unit square-lattice edge, and every local term has norm at most one. The graph is genuinely connected, with fixed coefficients one or one half.')
p('All wire occupations commute with the Hamiltonian. Conditional on their complete bit configuration, the cells are independent Gibbs states with Hamiltonians H+tᵢnroot, tᵢ∈{0,1}. This retains their actual correlations; it does not assume an independent wire ensemble.')
p('Because ψ lies wholly in root sector one, the added field leaves ψ unchanged. Write u₁=Tr(Pe⁻ᵝᴴ), u₀=Tr(Qe⁻ᵝᴴ). The conditional witness mean is')
eq(r'\frac{(1-p)e^{-\beta t_i}u_1-pu_0}{Z(t_i)}\le-\delta.')
p('The already negative numerator decreases with tᵢ≥0, while Z(tᵢ)≤Z(0). The same margin therefore holds for every wire configuration. Conditional target concentration survives averaging over the wires. The output concentration proof continues to allow arbitrary entanglement among all cells and wires. Consequently')
eq(r'\inf_\sigma D\!\left(\Lambda_p^{\otimes M}(\sigma),\rho_{\mathrm{connected}}\right)\ge1-2e^{-M\delta^2/2}.')
p('The inequality Htotal≥Σall nᵥ preserves the unique product vacuum and gap at least one. Wire length is O(√N) per cell. Occupied volume and containing rectangle are O(MN). No vanishing connector strength, hidden long link or product-source premise is used.')
p('This is the central new composition: a rare cell discrepancy becomes a connected global strong converse while retaining the quantum/classical conditional interface exactly.')

page('8. One fixed interaction pattern for every rate')
p('To remove dependence of the target layout on p, number cells j=1,2,… and choose their H-tree types using the 2-adic valuation v₂(j):')
eq(r'h(j)=1+\left\lfloor\frac{v_2(j)}3\right\rfloor.')
p('Type h has frequency 7/8ʰ. Give the varying-size trees disjoint horizontal spans, align their bottoms at y=2 and connect them to the same spine through their empty vertical axes. This gives one fixed computable aperiodic nearest-neighbor interaction pattern, independent of the noise rate.')
p('For J=8ᵐ cells, each h≤m occurs exactly 7J/8ʰ times, and the final cell has type m+1. Summing Nₕ≤3·4ʰ gives at most 33J tree qubits. Wires and total horizontal width are O(J). Maximum height is O(J¹ᐟ³), so the containing rectangle can have O(J⁴ᐟ³) sites. This empty area remains part of the physical geometry.')
p('For any fixed p>0, choose one eligible type h*. It has a fixed positive witness margin and appears at positive density among the cells. Test only this type. Conditioning on every wire occupation still yields independent target tests with uniformly negative means; every output has nonnegative conditional means. The number tested diverges, and trace distance tends to one.')
p('The volumes are consistent prefixes of this same pattern. This is stronger than choosing a new Hamiltonian after learning the error rate. No translation invariance, finite-temperature uniqueness or finite-temperature clustering theorem is asserted. A zero-temperature gap does not establish those properties.')
h('Why global accuracy matters')
p('Each fixed cell discrepancy can be extraordinarily small, and every finite target is full rank. Repetition makes the discrepancy macroscopic. The theorem concerns the global physical state over growing volumes. It is not a hardness theorem for local observables, energy-density measurements or classical output sampling.')

page('9. A necessary final-port precision law')
p('The same connected amplifier yields a family where even fixed global accuracy forces the physical output error to decrease with volume. Let B=1+e⁻ᵝ, a=2log A+log B and g=3β/2−2log A. Choose')
eq(r'q=\left\lceil\frac{3\beta+2\log B}{\log2}\right\rceil,\qquad M_h=2^{q n_h}.')
p('Connect Mₕ identical h-th cells. If p≥2e⁻ᵝ⁻ᵍⁿ, then δ≥p e⁻ᵃⁿ/(2B). If any output has D≤ε<1, the strong converse forces Mδ²≤2log[2/(1−ε)]. Hence')
eq(r'p\le C_\epsilon e^{-gn},\qquad C_\epsilon=2B\sqrt{2\log\frac2{1-\epsilon}}.')
p('The below-threshold branch already obeys the same inequality because Cε≥2e⁻ᵝ. This covers both cases. Put S=2ʰ−1 and w=2S+3. The row has exact occupied-site count V=M(n+3S+5)−2S−2 and containing rectangle R=(Mw−2)w. Direct algebra gives nM≤V≤7nM/3 and V≤R<2V. Thus both actual sites and full footprint are Θ(n2ᑫⁿ).')
eq(r'p=O_\epsilon\!\left[\left(\frac{V}{\log V}\right)^{-\alpha}\right],\qquad \alpha=\frac{g}{q\log2}.')
p('At β=12, q=52 and α=0.1714076087…. As the fixed β increases, this sufficient exponent approaches one half. The law holds along the explicit discrete volumes Vₕ. Arbitrary-volume interpolation is not supplied.')
p('This is a necessary physical endpoint precision law, not an attaining preparation algorithm. The number of cells is exponential in cell size: already the first n=6 cell uses M=2³¹² copies. The constants and volumes make this a mathematical asymptotic result, not a useful engineering design. This quantitative equal-cell sequence is separate from the aperiodic all-rate pattern in Section 8.')

page('10. Consequences beyond the example')
h('Every fixed local marginal stays uniformly full rank')
p('Write H=I_S⊗Hfar+K for a fixed set S, with ‖K‖≤J_S. Jensen’s inequality on |a⟩⊗|j⟩, where |j⟩ is an Hfar eigenvector, lower-bounds the numerator by e⁻ᵝᴶˢ Zfar. Eigenvalue min-max bounds the denominator by d_S eᵝᴶˢ Zfar. Therefore')
eq(r'\rho_S\succeq\frac{e^{-2\beta J_S}}{d_S}I_S.')
p('Here J_S≤4|S|, uniformly in total volume. Thus no fixed-support full-rank test implies a positive global noise radius.')
h('Ordinary thermodynamic stability is insufficient')
p('For U=Xroot, only the onsite term and two tree edges change, so ‖UHU−H‖≤3. Nevertheless')
eq(r'D(U\rho U\|\rho)=\beta\operatorname{Tr}\rho(UHU-H)\le3\beta,\qquad D_{\max}(U\rho U\|\rho)\ge\beta+gn.',11)
p('The connector changes the ordinary relative-entropy constant to 4β. Bounded local energy and bounded ordinary relative entropy do not control the worst-direction ratio that governs noise inversion.')
h('Even the root marginal has a fixed tolerance')
p('The two root sectors have Hamiltonians H₀ and H₀+V, I≤V≤3I. Trace min-max places root occupation between 1/(1+e³ᵝ) and 1/(1+eᵝ). Its isolated bit-flip inverse stays positive on a fixed nonzero interval, although the whole-state threshold vanishes.')
h('The earlier positive result remains intact')
p('The accepted one-dimensional mixed-block and bounded-factory theorems retain their scopes. For commuting local Hamiltonians, far terms cancel in single-port imaginary-time conjugation, giving κ≤exp(2β‖Hnear‖). The present two-dimensional noncommuting counterexample does not contradict either positive class. A separate translation-invariant positive square-lattice variant is recorded in the technical note only at its own single-port scope.')

page('11. Strong alternatives and prior-art boundary')
p('The strongest relevant comparison is not a deliberately expensive preparation algorithm. The theorem grants every upstream density operator for free. Ideal Gibbs samplers, constant-depth sources, qLDPC interfaces, active quantum error correction and better classical computation are all included. They cannot change the image of the final physical channel.')
p('Fault-tolerant quantum input/output explicitly retains controlled noise at physical input and output [5]. This is compatible with the present theorem: improving internal logic is not equivalent to eliminating an unobserved final physical fault. Autonomous correction after that fault moves the endpoint and is a useful different operation; no claim against the other autonomous-processing branch is made.')
h('What Pettinari already supplies')
p('Pettinari [4] uses the facilitated square-lattice Hamiltonian JΣordered neighbors nᵢXⱼ with Gibbs convention e⁺ᵝᴴ. Its vacuum is a zero-energy eigenvector, not asserted to be a ground state. Remark 2.8 gives a+b≥exp(c|X|−2Jβ)b, where b is the vacuum probability on Y=X∪{r} and a the root-only-flip probability. A positive bit-flip preimage, tested on the vacuum, immediately requires')
eq(r'p\le\frac{b}{a+b}\le e^{2J\beta-c|X|}.')
p('Thus bare exponential exact endpoint fragility is already an operational corollary of that primary. Disconnected-copy amplification is also accessible from a general witness. Neither is claimed here as an original discovery.')
p('The added conjunction is a positive gapped product-ground Hamiltonian with counted planar geometry, an explicit normalized witness, and fixed-strength diagonal connectors preserving that witness conditional on every wire record. This yields the connected strong converse against arbitrary upstream entanglement, the one-pattern all-rate result and the necessary precision law.')
p('This is a substantial boundary on universal physical Gibbs delivery. It is not evidence of a civilisation-scale practical capability, a general sampling-hardness result or certified priority over all work outside the sources examined.')

page('12. Verification, accounting and preserved failures')
p('All-size conclusions have analytic proofs. Independent finite geometry checks through h=6 covered 12,097 vertices. A separate implementation through h=7 covered 48,769 vertices and verified no intersections, degree three, exact area and hook recurrence, and Pₕ≤16ⁿ.')
p('A seven-site spectral calculation checked gap one and inverse positivity at β=0.25, 0.5 and 1. At 0.9pmax the inverse was positive; at 1.1pmax it had a negative eigenvalue. These moderate-condition diagnostics supplement the proof. Ill-conditioned low-temperature floating-point diagonalization is not used to certify β=12.')
h('Resource accounting')
p('The counterexample specifies fixed qubit dimension, nearest-neighbor interactions and fixed coefficients. It pays for subdivision, wires and containing area. No target acquisition, cooling, sample generation, calibration or reset protocol is claimed. They are relaxed in the impossibility comparison. Computing and measuring the Perron projector may be very expensive. No practical threshold or energy advantage follows.')
h('Failed routes kept at valid scope')
p('A generator-uniformization route based on a strictly positive conditional Choi matrix gives a formal channel mixture, but finite gate durations, idles and causal scheduling remain an unclosed implementation. It is not counted as a physical simulator. A fermionic extent argument survives when total local causal time, including classical propagation, is charged. Fermionic teleportation and entanglement swapping defeat a stronger lower bound based on quantum gate layers alone. The valid bound and explicit bypass are retained.')
h('Accepted science remains unchanged')
p('The bounded-factory archive is embedded byte for byte, recursively retaining earlier results. Its five-bit controller interface, finite-bit fallback, separate six-layer cluster family, quantum-positivity/controller-threshold distinction and positive-domain calibration constants are unchanged.')
p('Preserved archive SHA-256: 538341c447bbfe939c7ad0807647943a4d8b67ce30b010510bbea771f9f50761.', 'small')
p('The package contains the full governing proof, independent audit, primary comparison, scoped failures, verification code and receipts, this report and a file manifest. Downloaded primary full texts are not republished.', 'small')

page('13. Primary sources and notation')
refs=[
('[1] C. Zhang, L. Li, G. Lu, H. Yuan and R. Duan. Quantum error pre-compensation for quantum noisy channels (2023).','https://arxiv.org/abs/2309.01434'),
('[2] G. Bouch. Complex-time singularity and locality estimates for quantum lattice systems. arXiv:1011.1875; Journal of Mathematical Physics (2015).','https://arxiv.org/abs/1011.1875'),
('[3] H. Tasaki. Trees that can be grown in “too many” ways: Bouch’s construction and a bound for every size. arXiv:2412.16912v4.','https://arxiv.org/abs/2412.16912v4'),
('[4] L. Pettinari. A Finite-Range, Translation-Invariant Counterexample to Weak Gibbsianity. arXiv:2610.41871v2, 2 November 2026; PDF dated 3 November. Remark 2.8 is the closest endpoint comparator.','https://arxiv.org/abs/2610.41871v2'),
('[5] M. Christandl, O. Fawzi and A. Goswami. Fault-tolerant quantum input/output. arXiv:2408.05260.','https://arxiv.org/abs/2408.05260'),
('[6] M. Christandl, O. Fawzi and A. Goswami. Fault-tolerant interfaces for quantum LDPC codes. arXiv:2602.16948v2 (2026).','https://arxiv.org/abs/2602.16948'),
('[7] S. Pilatowsky-Cameo, G. Styliaris, A. Bakshi and D. Malz. One-dimensional quantum Gibbs states in constant circuit depth. arXiv:2609.35973 (2026).','https://arxiv.org/abs/2609.35973'),
('[8] C. Rouzé and D. Stilck França. Rapid mixing of Gibbs samplers via quantum Dobrushin–Shlosman conditions. arXiv:2610.03578 (2026).','https://arxiv.org/abs/2610.03578'),
('[9] T. Debarba et al. Teleporting quantum information encoded in fermionic modes. arXiv:2002.08201. Used for the preserved bypass, not the main theorem.','https://arxiv.org/abs/2002.08201')]
for text,url in refs:p(html.escape(text)+' '+link(url,url),'small')
h('Conventions')
p('D(ρ,σ)=‖ρ−σ‖₁/2; logarithms are natural unless a base is shown. Energies are in units where each local term has norm at most one, and kB=1. β=12 is an explicit sufficient mathematical value, not a material-specific temperature prediction. The word “final” describes causal order: no subsequent uncharged recovery is allowed at the same endpoint.', 'small')
p('Original calculations and new deductions are proved in the report and its technical notes. Primary citations identify imported machinery and the strongest direct alternatives. No experimental action, expenditure, outreach or external worker was used.', 'small')

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#CBD8DD'));canvas.setLineWidth(.4)
    canvas.line(48,43,A4[0]-48,43);canvas.setFont('DSans',8);canvas.setFillColor(MUTED)
    canvas.drawString(48,29,'ASTRA • THERMAL OUTPUT FEASIBILITY • 5 NOVEMBER 2026')
    canvas.drawRightString(A4[0]-48,29,str(doc.page));canvas.restoreState()
path=OUT/'Astra_Thermal_Output_Boundary.pdf'
doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=58,
    title='When finite temperature does not protect a quantum output',author='Astra research collaboration',pageCompression=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'report_text.txt').write_text('\n\n'.join(plain))
print(path)
