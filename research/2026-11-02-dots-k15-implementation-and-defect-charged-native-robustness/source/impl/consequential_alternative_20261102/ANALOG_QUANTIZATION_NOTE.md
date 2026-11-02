# Square-qubit GKP reliability quantization diagnostic

Requested bounded calculation, 2026-11-02. Noise variance v in each quadrature, [q,p]=i. Let L=sqrt(pi), H=L/2=.8862269254527579, s in [-H,H). The nearest-cell corrected logical flip probability is

  g_v(s)=sum_m f_v(s+mL), a_v(s)=sum_{m odd}f_v(s+mL), p_v(s)=a_v(s)/g_v(s).

Quantize |s| using B intervals [t_(b-1),t_b], t_0=0,t_B=H. The exact flag weight and conditional flip probability are

  w_b=2 integral_(t_(b-1))^(t_b) g_v(s) ds,
  e_b=2 integral_(t_(b-1))^(t_b) a_v(s) ds, p_b=e_b/w_b.

Integrals in w,e are Gaussian CDF differences. Minimize H_B=sum_b w_b h2(p_b). The requested symmetric-input one-use coherent information is I_B=1-2 H_B. This is NOT maximization over all input states: a pure input always gives zero, while the values below are negative. Nor is a negative I_B a capacity zero proof.

## Results (bits per physical mode)

| v | Continuous I | B=2 I | B=3 I | B=4 I |
|---|---:|---:|---:|---:|
| 1/e | -.00000459133091447 | -.0428849508499375 | -.0183860027198622 | -.0101493945174113 |
| .37 | -.00678031184348374 | -.0494610998306962 | -.0250748990223591 | -.0168769940158776 |

Corresponding binning penalties I_continuous-I_B:

| v | B=2 | B=3 | B=4 |
|---|---:|---:|---:|
| 1/e | .0428803595190231 | .0183814113889477 | .0101448031864968 |
| .37 | .0426807879872124 | .0182945871788753 | .0100966821723939 |

Thus B=4 keeps the loss relative to the continuous analog channel near .0101 bits/mode. At v=.37 an outer construction would need to recover the full .016877-bit/mode symmetric-information deficit to cross zero, not merely the binning loss. Comparing this deficit to another channel's enhancement is only heuristic; the flagged mixture is not an effective binary channel determined by its entropy alone.

## Optimized thresholds in physical syndrome units

v=1/e:
- B2: [.542139870995451]
- B3: [.4115815901627014, .6662570072827316]
- B4: [.34022275991964845, .5488715204497766, .7240736754156544]

v=.37:
- B2: [.5417836311703227]
- B3: [.411270187526216, .6660108613908934]
- B4: [.3399682610836249, .5485705584114442, .7238881650066498]

## Ready-to-use B=4 flagged Pauli channel at v=.37

w = [.441781212304599, .23515882793922252, .17374023963226093, .14931972012391756]
p = [.04076238610869689, .11086401527185301, .23379136678398044, .4046394986156898]

The q and p flags j,k are independent, giving 16 joint flags with weights w_j w_k. With q displacement producing X and p displacement producing Z, their conditional probabilities in [I,X,Y,Z] order are

  [(1-p_j)(1-p_k), p_j(1-p_k), p_j p_k, (1-p_j)p_k].

All B2/B3/B4 weights and probabilities at both v are in analog_quantization_results.json.

## Method and status

Float64 scipy quad for the continuous entropy; exact-in-form normal-CDF bin masses; scalar bounded optimization for B2; 65-start constrained SLSQP with analytic gradients for B3/B4. All chosen solutions report optimizer success and near-zero interior gradients. An independent 50-decimal mpmath reevaluation of the selected thresholds and continuous integrals agrees to approximately 15 decimal places. The mpmath script uses exact v=1/e and v=.37, rather than binary float representations.

This is a high-accuracy diagnostic, not an interval certificate or proof of global optimality. Lattice sums use |m|<=12 in float64 and <=8 in the high-precision check. No claim of positive coherent information, asymptotic rate, or realized finite-energy decoder is made.

Files: analog_quantization.py, analog_quantization_results.json, analog_quantization_validate.py, analog_quantization_validation.json.
