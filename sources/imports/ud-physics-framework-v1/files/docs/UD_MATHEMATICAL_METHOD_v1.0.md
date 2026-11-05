# UD mathematical analysis protocol v1.0

Status: runtime method for the Discovery sandbox. This defines how to analyze and record a claim; it does not amend source theory, establish a physical bridge, or restore mainline eligibility. Hypotheses, inverse design, target-selected formulas, and calibration remain permitted with explicit provenance.

## 1. Start with typed objects

Before consequential algebra, define the question, carrier/state space, coefficient domain, basis/orientation, maps with domains/codomains, metric/measure, boundary conditions and intended readout. Use stable object IDs as well as symbols.

Keep counts, chain dimensions, representation multiplicities, operators, eigenvalues, amplitudes, probabilities, clocks, units and physical measurements distinct. A shared numerical value does not identify two objects. Distinguish dimension of a vector space, topological dimension and physical units.

For each consequential quantity record its exact expression or measured value, source version/section/object ID, assumptions, dependencies, normalization, units, and origin: imported, derived, assumed, fitted, numerical or measured. Propagate changed assumptions to dependent conclusions. A symbolic equality does not upgrade the evidence status of its premises.

## 2. Select the applicable techniques

Use this table as a question-driven menu. Mark irrelevant techniques N/A with a short reason rather than manufacturing a factorization or clock interpretation for every problem.

| Technique | Required question or receipt |
| --- | --- |
| Integer/combinatorial analysis | What is counted; are multiplicities, constraints and boundary ownership correct? |
| Distinction/register and parity analysis | What alphabet, admissible words, encoding, parity/check constraints and hidden degrees of freedom are defined? |
| Rational/exact symbolic algebra | Which quantities are exact, and what do numerator and denominator mean? |
| Prime factorization and valuations | Which declared counts, divisibility constraints or scale products are being compared? |
| Clock/modular arithmetic | What is the state, modulus, update and meaning of a residue? |
| Group/permutation structure | What action, orbit, stabilizer or representation justifies a count or selection? |
| Chain/homology analysis | What boundary maps, coefficient domain, ranks and possible torsion are relevant? |
| Spectral/operator analysis | Which generator, metric, adjoint, active modes and normalization determine dynamics? |
| Local transport/support analysis | What local continuity, stock, current, source/sink and gate laws are specified? |
| Projection/coarse-graining | What map and kernel separate retained and discarded observables? |
| Geometry/continuum analysis | Which geometric structures, refinement and limiting assumptions are imposed or derived? |
| Recursive/hierarchical scaling | What is transferred per layer, why that depth, and what boundary/termination law applies? |
| Physical units and calibration | What explicit map connects internal variables to measurements? |
| Fit/null/sensitivity analysis | What was target-informed, how flexible is the model, and what distinguishes it? |

## 3. Integer and fraction discipline

- Derive finite counts from an explicit set, complex, register, action or constraint. Multiplying counts assumes a product or justified conditional count; do not assume independence because a product fits.
- For quotient counts, verify orbit/stabilizer structure. Division by a symmetry-group order counts free orbits only when the action is free; use the appropriate stabilizers or orbit-counting formula otherwise.
- Keep exact integers and reduced fractions through derivation. Preserve the unreduced counting expression and each factor's source even after cancellation. Separate a signed amplitude from a nonnegative stock or probability.
- Use rational/symbolic tools for exact inputs; construct fractions from integers or explicit decimal strings, not binary floating-point intermediates. A measured decimal remains a measurement with uncertainty even when represented exactly as a decimal rational.
- Keep radicals, algebraic roots, pi and symbolic parameters exact when possible. For an implicit algebraic root, state the defining polynomial and the selected root/branch.
- Distinguish amplitude, norm-squared/probability and energy factors; a scaling factor need not act with the same power on all three. Keep angular frequency, cycle frequency and period conventions explicit.
- Label rational reconstruction, guessed integer relations, chosen exponents and target-selected normalizations as hypotheses/FIT. State bounds, tolerance and search freedom; numerical agreement does not prove an identity.

For a positive integer, report prime powers when they answer a defined question. For a nonzero rational, factor reduced numerator and denominator separately; signed prime exponents expose divisibility and scaling. Separate the sign. Zero has no prime factorization. Record partial rather than complete factorization if unresolved factors remain.

Use gcd, lcm and divisibility for actual compatibility questions. For a proposed finite subgroup embedding, order divisibility is a necessary preliminary check, not a sufficient embedding proof. Shared prime factors alone establish no shared mechanism, scale law or physical constant.

## 4. Clock arithmetic and recurrence

Declare whether the object is an integer event index, a cyclic register, a permutation cycle, a continuous phase or a physical clock. Give the modulus, residue convention, update rule, initial phase, coupling and clock-unit map.

For an additive register x(n+1)=x(n)+a mod m, m>=1, its orbit length is m/gcd(a,m). For uncoupled registers updated once per common integer tick, the joint return period is the lcm of their individual orbit lengths. Coupling, gating or nonuniform update schedules require the actual joint map.

Division modulo m is allowed only for a unit: a is invertible iff gcd(a,m)=1. Distinguish the ring Z/mZ from a finite field; a composite modulus generally has zero divisors. State whether quadratic residues include zero. A residue class or non-residue does not forbid a transition unless a declared admissibility law does so.

A finite deterministic state map gives eventual periodicity; a bijection on a finite state set gives periodicity from the initial state. This does not transfer to a continuous-amplitude flow or a stochastic trajectory.

For simultaneous phase return of active nonzero continuous frequencies, require omega_j*T in 2*pi*Z. A common nonzero period requires commensurate active frequencies. Distinguish exact return, approximate recurrence, state-specific return, projective/gauge equivalence, and recurrence of only a projected observable. Floating rational approximations do not prove exact commensurability.

Treat a chosen modulus, tick rate or phase identification as assumed/FIT unless source-derived. No modulus, prime or clock unit is privileged merely because it matches a target.

## 5. UD structural and dynamical checks

### Distinctions, codes and phase transport

Specify the distinction alphabet and admissibility constraints before counting register states. For parity/code claims give the check map, coefficient domain, kernel and detection/correction scope. The count of distinguishable labels is not automatically a physical information capacity; state the encoding/readout and noise model.

For sign/phase transport declare real signs versus a continuous/discrete phase group, orientations, path composition and gauge/frame transformations. Verify any claimed loop/readout invariant under the stated transformations. Phase quantization or a residue-sector gate needs an explicit rule; listing roots of unity alone does not derive one.

### Complexes and chain spaces

Specify K, C_k(K;R), the coefficient ring/field, cell ordering/orientation and B_k:C_k->C_(k-1). Check B_k B_(k+1)=0 exactly in the declared domain. Record face counts, ranks, kernels and Euler characteristic when relevant.

Do not confuse real/finite-field ranks with integer homology. Integer torsion requires an appropriate integer invariant computation, such as Smith normal form. Characteristic reduction can change ranks; field Betti numbers do not by themselves specify integral homology.

### Generators, metrics and spectra

State the actual generator, continuous/discrete evolution, initial state, boundaries and observables. For real/complex spaces with positive metric H, the metric adjoint is A^(dagger_H)=H^(-1) A^* H. Here * is transpose over the reals and conjugate transpose over the complexes. Verify self/skew-adjointness in that metric, not by an unqualified transpose. Finite-field bilinear forms do not inherit real positivity.

For boundary maps between differently weighted chain spaces, use the appropriate domain/codomain metric adjoints. Distinguish a self-adjoint Hodge/Dirac operator from a skew evolution generator and state factors of i, signs and rate scales. Record eigenvalue multiplicities, zero modes, active eigenspaces, characteristic/minimal polynomials when useful, and whether reported frequencies are squared or unsquared.

Exact finite-matrix checks can establish identities for that carrier and metric. Numerical spectra, finite examples and representation dimensions do not alone prove universal dynamics, physical dimensions or particle identifications. For symmetry/commutant calculations, declare the group action, base field and representation type before using multiplicity formulas.

### Locality, stocks and readout

Define local neighborhoods, support, positive stocks, signed currents, source/sink terms and gate conditions. Check conservation or the explicit continuity balance, positivity assumptions, boundary leakage and memory/reset/outgoing-record accounting where relevant. A balance residual is not automatically a predictive constitutive law.

For a projection/compression, give the map, metric-dependent adjoint or inclusion, rank and kernel. Identify which modes/observables survive. Dimension lost to a kernel is not a Shannon-information loss percentage without a probability/channel model. Use a stated common ambient space or intertwiner when comparing operators on different carriers.

Separate topological admissibility, kinematic possibility, dynamical persistence, attraction and growth preference. A static shape, count or invariant cannot substitute for an evolution/selection law.

For hierarchical products or powers, specify the transferred quantity, per-layer law, dependence between layers, depth/termination rule and boundary correction. Preserve the source of each exponent and prefactor. A uniform product law is an assumption until justified; target-selected depths or attenuation factors remain FIT.

## 6. Physical spacetime interpretation

Specify the proposed maps from internal state, event index and geometry to time, length, energy, fields and measured readout. Label each component imported, assumed, derived or calibrated. Carry scale factors and uncertainty; do not hide an unknown conversion by setting it to one.

For metric, coframe or causal-cone proposals, define the geometric object and signature. Identify the local generator/principal symbol or other mechanism that produces any claimed propagation cone. An imposed Lorentzian form is a hypothesis, not an emergent-signature derivation. State refinement, scaling and convergence assumptions for continuum claims.

A modular model does not automatically embed into a real/complex physical geometry. Specify a compatible representation, lattice/reduction or other explicit map; modular identities do not silently become real-field identities.

For a best fit, state the target, exposed data, uncertainty model, objective, parameters/formula search, units, baseline and identifiability. Preserve selection history even when the final formula is exact. Look for a residual, symmetry, scaling or intervention response that a conventional baseline does not already explain. Discovery does not require preregistration; independent predictive success requires genuinely unused evaluation under a frozen rule.

## 7. Worked method example: exact numbers, different objects

This is an illustrative reconstruction of a familiar ratio, deliberately chosen for instruction, not a new independent UD derivation.

Let X={1,...,24}, Theta={0,1}^3, Omega=X×Theta and E={1}×(Theta minus {000}). By construction |Omega|=24*8=192=2^6*3 and |E|=8-1=7, so |E|/|Omega|=7/192. It is a probability only under an explicitly uniform law on Omega. It is not a physical coupling, capacity or decay rate.

The supplied historical ledger v0.39 lists a separately sourced r_Delta=7/192 at C01. Numerical equality with this toy ratio does not identify their objects or mechanisms. The same ledger's Q03 and Q04 both equal 3/2 but describe different typed roles.

As a separate clock example, strides 3 mod 8 and 8 mod 12 have orbit lengths 8 and 3, and return jointly after 24 common ticks under the uncoupled update convention. Since gcd(8,12)=4, 8 has no multiplicative inverse mod 12. None of these arithmetic facts supplies a physical tick duration.

## 8. Calculation receipt and runtime contract

For a consequential result, fill [the mathematical receipt template](../templates/mathematical_receipt.json), store it under the owning candidate/session, and link it from the journal, handoff and PR. It records objects, exact forms, source dependencies, techniques, assumptions, normalization, fits, checks and interpretation limits.

Before work, the BOOT REPORT states the coefficient domain/exactness plan, relevant methods, clock/metric conventions and intended physical map. Unknown choices may remain explicit assumptions or OPEN; they do not stop useful conditional Discovery work.

Before reporting:
1. Check types, units, orientations, normalization and declared assumptions.
2. Verify central exact identities by a proof or reproducible exact calculation. Label a second implementation, self-review, separate-context review and independent experiment distinctly.
3. Use numerical methods where necessary; record precision, tolerances, conditioning, truncation/convergence and uncertainty rather than pretending exactness.
4. Preserve failed alternatives, limiting/counterexamples and target-selection history. Archive inputs/code/outputs and source revision through the existing capture workflow.
5. State what was proved, computed, fitted, assumed and physically tested separately.

This is a runtime analysis contract, not an automated proof checker. Current CI checks record integrity and its declared tooling tests; it does not certify a mathematical proof or a physical interpretation merely because a receipt exists.

## Source anchors and scope

- [Supplied Coefficient Provenance Ledger v0.39](../sources/imports/2026-10-22/UD_COEFFICIENT_PROVENANCE_LEDGER_v0.39.md), dated 2026-08-22: Canonical ledger P01–P06, F01–F06, C01/C06, Q03/Q04, Q13–Q21, Q122/Q125, Q169–Q179 illustrate typed counts, normalizations, conditional sources and event/physical-clock separation. It is a historical snapshot, not an assertion of the latest mainline state.
- [Supplied CRL-2 amendment v1.0](../sources/imports/2026-10-22/UD_GOVERNANCE_CRL2_SUBDIVISION_v1.0.md), §§2,4,5: dependency support, development lane and provenance. Its source status is governance proposal; adoption is not inferred.
- The user's current instruction requests integer, fraction, clock, factorization and provenance methods. This protocol extends those into a question-driven Discovery workflow; method recommendations are not new source theorems.
