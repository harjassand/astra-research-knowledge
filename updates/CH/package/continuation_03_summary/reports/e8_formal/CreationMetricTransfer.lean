import Lean

/-- The scalar interface needed to transfer the passive logarithmic-mean
metric identity to a creation port.  The passive weight is evaluated at the
frequency `v`; the creation weight is the passive weight at `-v`. -/
structure CreationMetricData (X : Type) [Neg X] where
  frequency : X → X → X
  logMean : X → X → X
  downWeight : X → X
  upWeight : X → X
  combine : X → X → X
  lowerThermal : X → X
  upperThermal : X → X
  frequency_swap : ∀ p q, frequency q p = -frequency p q
  logMean_symm : ∀ p q, logMean p q = logMean q p
  up_is_reversed_down : ∀ v, upWeight v = downWeight (-v)
  passive_metric : ∀ p q,
    combine (logMean p q) (downWeight (frequency p q)) =
      logMean (lowerThermal p) (upperThermal q)

/-- A passive metric identity and the frequency/mean symmetries force the
creation-port orientation: the thermal factors are reversed on that port. -/
theorem creation_port_metric_orientation
    {X : Type} [Neg X] (D : CreationMetricData X) (p q : X) :
    D.combine (D.logMean p q) (D.upWeight (D.frequency p q)) =
      D.logMean (D.upperThermal p) (D.lowerThermal q) := by
  calc
    D.combine (D.logMean p q) (D.upWeight (D.frequency p q)) =
        D.combine (D.logMean q p) (D.downWeight (D.frequency q p)) := by
          rw [D.logMean_symm p q, D.up_is_reversed_down, ← D.frequency_swap p q]
    _ = D.logMean (D.lowerThermal q) (D.upperThermal p) := D.passive_metric q p
    _ = D.logMean (D.upperThermal p) (D.lowerThermal q) :=
      D.logMean_symm (D.lowerThermal q) (D.upperThermal p)

#print axioms creation_port_metric_orientation
