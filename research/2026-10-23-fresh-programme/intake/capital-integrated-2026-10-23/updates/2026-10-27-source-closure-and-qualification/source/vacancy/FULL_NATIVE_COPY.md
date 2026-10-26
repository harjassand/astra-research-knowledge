## Astra Chemistry — New construction: a vacancy-driven molecular frontier

The strongest alternative to a DNA instruction motor is emerging from the geometry of DNA-templated synthesis.

The proposed change is to let each successfully incorporated peptide module carry a temporary DNA/PNA recognition handle. Its attachment to the growing product would make that handle available for local rebinding to the template. Addresses already occupied by product-attached handles would become less accessible to free donors; the next unoccupied address would define the growth frontier.

The underlying operations have substantial precedent. Niu, Hili and Liu demonstrated DNA-programmed assembly of chemically diverse polymers using PNA adapters, including a 26-kDa product with 16 coupled building blocks. Spaltenstein and colleagues demonstrated traceless, templated peptide ligation using removable attachments. Neither paper establishes the proposed independently retriable, vacancy-controlled NCL relay.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Nature Chemistry

+2



### Why this changes the mechanism

One DNA template, two possible chemical histories

Molecule A — missed its last incorporation

1

Bound

2

Bound

3

Vacant

4

Vacant

The next intended donor occupies address 3.

Molecule B — successfully incorporated at address 3

1

Bound

2

Bound

3

Bound

4

Vacant

The next intended donor occupies address 4.

The essential advantage is that chemical ancestry potentially determines which positions are already occupied. The system would not need to electronically or enzymatically increment an instruction counter after every reaction.

This remains conditional on a difficult physical requirement: product-attached handles must rebind their intended addresses with sufficiently high fidelity, while unreacted donors can be removed without destroying the growing molecule.

### 1. New result: local reanchoring removes a major polymer-length penalty

Suppose a growing peptide is connected to its DNA template only at the starting point. In an ideal Gaussian-chain model, its reactive end becomes progressively less likely to encounter a distant instruction site.

For two independently flexible strands rooted at the same point, the local contact density at instruction \\(j\\) scales as

\\[ a_j=a_1j^{-3/2}. \\]

If each successful module instead supplies a new local PNA anchor, the relevant encounter distance can remain approximately one module long. Subject to compatible geometry and reliable rebinding, the correct-reaction rate need not decline with total chain length.

With irreversible damage rate \\(d\\), the exact competing-clock model gives

\\[ P\_{\mathrm{correct}}= \prod\_{j=1}^{L}\frac{a_j}{a_j+d}. \\]

Illustrative correctness from geometric accessibility alone

Assume \\(d/a_1=10^{-6}\\), no incorrect bond chemistry, and identical first-step rates.

| Required additions | Only original root tether | New local anchor each addition |
| ------------------ | ------------------------- | ------------------------------ |
| 16                 | 99.956%                   | 99.998%                        |
| 64                 | 98.673%                   | 99.994%                        |
| 1,024              | 0.000167%                 | 99.898%                        |

This does not predict actual peptide yields. The Gaussian-chain approximation has restrictions, and existing prepositioned-adapter methods already exploit local tethering. The useful result is identifying local reanchoring as a potentially necessary scalability condition, rather than assuming better DNA address sequences alone can maintain effective coupling rates.

### 2. The newest anchor can detach and recover

A stronger observation follows from the physical model. The newly attached PNA handle does not have to remain permanently hybridized.

Let \\(B\\) denote the correctly docked terminal handle and \\(U\\) its temporarily undocked state. Suppose it undocks at rate \\(u\\), rebinds at rate \\(v\\), forms the correct bond at rate \\(a\\) while docked, and suffers wrong chemistry at rates \\(w_B,w_U\\) in those respective states. Let \\(d\\) be irreversible parent damage.

The exact probability of eventual correct ligation before irreversible failure, starting docked, is

\\[ \boxed{ P_B= \frac{a}{ a+w_B+d+ u\frac{w_U+d}{v+w_U+d} }. } \\]

This reveals that undocking is not necessarily a fatal error. Its effective penalty is reduced by successful local rebinding.

Illustrative 1,024-addition programme

For hypothetical \\(a=0.05,\ u=0.01,\ w_U=10^{-4},\ w_B=0,\ d=10^{-7}\\), all in s⁻¹:

| Rebinding rate \\(v\\) | Full-chain correctness |
| ---------------------- | ---------------------- |
| 0.01 s⁻¹               | 13.14%                 |
| 0.1 s⁻¹                | 81.32%                 |
| 1.0 s⁻¹                | 97.77%                 |
| 10 s⁻¹                 | 99.59%                 |

The expression passed 600 independently constructed Markov-generator checks and a 55,000-trajectory stochastic test.

This is a useful physical distinction: the system needs a recoverable local growth frontier, not perfect simultaneous attachment of all historical tags.

### 3. A counterexample rules out requiring every historical tag to be bound

Suppose each of \\(j\\) old product tags correctly rehybridizes during a refresh with independent probability \\(\theta\\). If the assembler requires all previous tags to be correctly bound on every cycle, its probability of satisfying that condition throughout \\(L\\) steps is

\\[ P\_{\mathrm{all\ bound}}=\theta^{L(L+1)/2}. \\]

Even at \\(\theta=0.9999\\), the probability is approximately \\(1.61\times10^{-23}\\) for 1,024 steps.

That requirement is untenable under the independence model. The better construction is to rely on the newest tip anchor for productive coupling, while tolerating some older undocked tags if their interference with the current terminus is sufficiently weak.

There is a corresponding obstruction on the other side of the frontier: downstream vacant addresses may recruit incorrect donors. If the unwanted interaction falls with positional distance as \\(r^{-\alpha}\\), then total exposure scales quadratically when \\(\alpha=0\\), as \\(L\log L\\) when \\(\alpha=1\\), and linearly when \\(\alpha>1\\).

For the hypothetical 1,024-step model, a uniform non-frontier hazard ratio of \\(10^{-5}\\) yields only 0.54% full correctness, whereas an \\(r^{-3/2}\\) interaction gives 97.48%.

Thus a molecular vacancy is not sufficient by itself. The assembler needs both locally enhanced desired chemistry and spatially suppressed incorrect chemistry.

### 4. A global cleanup operation may remove accumulated tags more efficiently

An important concern is that each successful module carries an additional temporary PNA attachment. Eventually, those attachments must be removed if the product is to be an unmodified peptide.

CAPTN and earlier click-assisted NCL studies establish traceless removal of temporary peptide attachments in short, experimentally tested systems. They do not establish simultaneous removal of hundreds of individually attached PNA handles from a long product.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+1



I derived an exact limit for simultaneous removal. Suppose \\(L\\) linkers independently cleave at rate \\(u\\), while the entire product experiences a damage rate \\(d\\).

The probability that all linkers are removed by time \\(t\\) without damaging the product is

\\[ G_L(t)=e^{-dt}(1-e^{-ut})^L. \\]

The optimal common removal time is

\\[ \boxed{t^\*=\frac{1}{u}\ln\left(1+\frac{Lu}{d}\right).} \\]

Unlike independently sacrificing product survival at every sequential cleavage, the optimized shared cleanup time increases only logarithmically with the number of tags.

With hypothetical \\(d/u=0.001\\), this model predicts 98.80% whole-product success for 64 tags and 98.53% for 1,024 tags, excluding any site-specific damage.

There is a decisive limitation: if each tag has its own independent irreversible injury hazard \\(h\\), the probability acquires a factor \\((u/(u+h))^L\\). At \\(L=1024\\) and \\(h/u=5\times10^{-5}\\), the illustrative success drops to 93.61%.

Therefore simultaneous removal can overcome accumulated processing time, but cannot eliminate cumulative incorrect cleavage chemistry.

## Strongest construction after these tests

The highest-value architecture is now a rooted, locally reanchoring peptide relay with chemical cleanup between shared incorporation cycles.

A correct NCL reaction would incorporate a peptide module carrying its next PNA recognition handle. The rooted product would survive a denaturing wash that removes unincorporated donors. After rebinding to its own DNA template, the newly incorporated module would localize the subsequent growth reaction. A molecule that missed incorporation would retain its original competent terminal cysteine and its prior product-attached recognition handles.

The same wash does not automatically remove a reversibly attached thioester intermediate: that species is still covalently connected to the root. This makes the earlier thioester-resolution work indispensable. Wrong stable amides remain an independent, irreversible failure class.

The strongest equally informed alternative is the experimentally established prepositioned PNA-adapter system of Niu and colleagues, combined conceptually with CAPTN's selective activation. It already demonstrates meaningful DNA-directed synthetic chemistry without requiring a moving controller. The proposed relay would justify its greater complexity only by showing robust recovery of missed incorporations and independently progressing programmes, not merely by making another sequence-defined polymer.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Nature Chemistry

+2



The decisive unresolved experiment is a mixed two-programme construction in which one rooted parent is deliberately stalled and another has advanced. After chemical resolution, complete donor removal and rehybridization, each must recruit and form the correct next backbone amide at its own position. Product-attached versus free tags, transient thioesters, wrong stable junctions and terminal-protection integrity must be measured separately.

I preserved the calculations and their assumptions in the scientific derivation, with executable polymer geometry, clearance and vacancy-frontier checks and the independently checked terminal reanchoring model.

Research outcome: A promising construction principle survives: chemical incorporation can potentially maintain its own local synthesis frontier through product-retained, reversibly rebinding adapters, rather than a permanently locked instruction counter. The mathematical improvement is substantial under the stated assumptions. The decisive missing evidence is whether real NCL chemistry, PNA registration, donor clearance and traceless linker removal can coexist with sufficiently low wrong-bond rates. No integrated new manufacturing capability has yet been demonstrated.