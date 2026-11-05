# Lattix research method v1.0

## Define before calculating

Specify objects, domains/codomains, integer widths and signedness, coordinate range, cell quantization, neighborhood radius, key and hash mapping, collision/probe rules, merge operation, capacities, overflow semantics and returned observables. Distinguish coordinate keys, bucket addresses, particle IDs, memory offsets and physical units even when numbers match.

For spatial proofs use exact integers/fractions and stated rounding/boundary conventions. Check negative coordinates, maximum ranges, duplicate keys, adversarial collisions, empty/full tables, bucket/spill exhaustion and counter overflow. Prime factors/modular arithmetic are useful only when answering a declared addressing/counting question. Never infer uniform hashes from a few examples.

For concurrent algorithms define publication, atomic operations, ordering, synchronization and failure behavior. A correct serial reference does not prove race freedom. Separate deterministic membership, deterministic ordering, fixed memory budgets, reproducible approximate trajectories and portable bitwise output. Make tie-breaking and merge algebra explicit.

## Define dynamics and measurements

For Particles specify state, timestep, integration, contact detection/response, boundaries, conserved quantities and quality readouts. Report penetration/tunneling or stability gates independently from timing. For Lab specify backend, hardware, driver/API, precision, seeds, tolerances, warmups, repetitions, timer resolution, queue completion and uncertainty.

Keep implementation counters, GPU time, wall time and application cost distinct. A fixed iteration count is not a physical clock. Physical correspondence remains unclaimed without its own calibrated observable, independent measurement and falsifiable acceptance rule.

## Verify and preserve

Use a small exact/CPU oracle and independently constructed adversarial cases where they discriminate. Record proof assumptions, counterexamples, numerical precision, fitted parameters and target exposure. Cross-implementation agreement is evidence only for the tested scope. Constructor review and independent replication are different.

Use [mathematical receipts](../templates/mathematical_receipt.json) for consequential derivations and [benchmark governance](BENCHMARK_GOVERNANCE.md) for measurements. Preserve failed alternatives and negative results. Source changes trigger dependency review and versioned amendments; promotion is never inferred from a green workflow.
