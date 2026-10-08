# Table 2.2 — Quantitative Comparison (dissertation-ready)

Inserted into `Dissertation_Final_Revision/final_review.tex` as `\subsection{A Quantitative Comparison}` (§2.x, `sec:quant-comparison`), immediately after Table 2.1, wrapped in `\REV{}` (red, defined at top of preamble) for committee review. Table 2.1 itself was also corrected: VisFlow 3.0's "ID drift-aware merge" cell was `\cmark`, which is the exact overclaim this table exists to avoid — changed to `\xmark` with an inline note pointing to Table 2.2's footnote [f].

## Table 2.2 — Quantitative measurements (n=1 workflow, 3 repetitions)

| Metric | Nextflow | Snakemake | CWL | VisFlow 2.0 (BioFlow) | VisFlow 3.0 (Necto) |
|---|---|---|---|---|---|
| Pipeline-definition LOC [a] | 29 | 20 | 41 | n/a [b] | 10 |
| Mean execution time, s [c] | 9.81 | 2.06 | 2.88 | 2.44 | 2.27 |

## Table 2.3 — Objective structural and documented-capability comparison

| Property | Nextflow | Snakemake | CWL | VisFlow 2.0 (BioFlow) | VisFlow 3.0 (Necto) |
|---|---|---|---|---|---|
| Closed, finite grammar | ✗ | ✗ | ✓ | ✗ | ✓ |
| Enumerated construct count [d] | n/a | n/a | 4 | 14 | 17 |
| Proven graph/text equivalence | n/a | n/a | ✗ | ✗ | ✓ |
| Typed I/O contract at integration | ✗ | ✗ | ✓ | ✓ | ✓ |
| Native foreign-call languages | any (shell) | Py/R/Julia/Rust+any | any (CLI) | Py/R/JS | Py/R/JS |
| Container support | ✓ | ✓ | ✓ | ✗ | ✗ |
| Provenance support | ✓ | ✓ | ✓ | partial | partial |
| Identifier-drift false merges [e] | 116/116 | 116/116 | 116/116 | **not implemented [f]** | **not implemented [f]** |
| Formally proven properties [g] | 0 | 0 | 0 | 0 | 4 |

### Footnotes

- **[a]** Non-blank, non-comment lines in the orchestration file(s) alone. The two Python library functions every system calls are identical and excluded from every column. n=1 workflow.
- **[b]** VisFlow 2.0 authors this workflow as a 6-node, 5-edge graph — no line-based grammar to count; "not applicable," not zero.
- **[c]** Mean of 3 runs, same machine, same network conditions. ≈1.8–2.0s is a live-network floor common to all five; this measures per-run *engine overhead*, not general throughput or scalability, and not a claim beyond this one workflow.
- **[d]** Counted directly from each system's own defining artifact (CWL spec; VisFlow `NODE_RULES`; Necto `ast.js`). Not reported for Snakemake/Nextflow — both embed in a general-purpose host language with an open, versioned directive/operator library, not a closed grammar to enumerate without an arbitrary cutoff.
- **[e]** Of 116 real over-merge cases, how many a system's natural join (absent a dedicated identity-mediation primitive) concludes are the same entity. Measured independently through all three engines; the defensive alternative (exact-match) scores 0/116 false but also 0/100 recovered instead.
- **[f]** **Not implemented in the deployed merge.** Canonical mediation (Ch. 3) is proven and achieves 0/116 false / 100/100 recovered, but as a *separately implemented and evaluated* algorithm (MapBasePlanner), not part of VisFlow 2.0's or 3.0's own deployed `LINK`/`COMBINE`, which do the same plain syntactic-equality join as the three comparators and inherit the identical vulnerability until integration is completed.
- **[g]** Bijection (Thm. 6.1), confirmation-site characterization (2 propositions), constructor non-redundancy — a count of what's proven, not an independent quality signal.

## Methodology paragraph

> This comparison combines three kinds of evidence, kept visibly distinct rather than collapsed into one score: controlled quantitative measurements (Table 2.2), objectively countable structural properties sourced from each system's own specification or source code (Table 2.3's construct-count and proof-count rows), and documented capabilities (container and provenance support, sourced from official documentation). A metric is included only when a fair, reproducible measurement procedure exists for all five systems; where one does not, the value is omitted or marked not applicable rather than estimated.

## Findings paragraph

> The quantitative comparison indicates that VisFlow 3.0's primary distinction relative to Nextflow, Snakemake, and CWL is structural and formal rather than execution performance. For the evaluated workflow, Snakemake achieved the lowest measured execution time of all five systems, and Necto required fewer orchestration lines than the other three line-based representations evaluated, while VisFlow 2.0 required none at all since the workflow is authored graphically. VisFlow 3.0 is, however, the only one of the five with a machine-checked proof that its visual and textual representations denote the same program, and the only one accompanied by a formal grammar with an enumerable, finite construct set. On identifier drift, the two ways to express this join absent a dedicated mediation primitive are measured, independently and identically across Snakemake, Nextflow, and CWL, to force a choice between recovering nothing and falsely merging every one of 116 distinct-entity test cases — a finding about what ships in those three systems today, not a claim that VisFlow 3.0's own deployed merge avoids the same failure, which it currently does not. Established systems in turn provide stronger reproducibility infrastructure than either VisFlow system.

## Limitations paragraph

> The execution-time and lines-of-code measurements are based on a single representative workflow; extending both to a 5–10 workflow benchmark suite is future strengthening, not a precondition for reporting this result. Execution time is measured on one machine under one set of network conditions and is not a scalability or cluster-throughput claim. Lines of code measure artifact size, not authoring time, cognitive load, or usability. Some language constructs genuinely cannot be reduced to a common numerical count across systems with and without a closed grammar, and are reported as not applicable rather than zero. Most importantly, the identifier-drift safety result motivating Chapter 3 is not yet integrated into either VisFlow system's own deployed merge operators; until it is, VisFlow 2.0 and 3.0 share the same identifier-drift vulnerability as Nextflow, Snakemake, and CWL. This comparison should be read as a scoped, evidence-bounded report along eleven specific, independently verifiable axes, not a universal ranking of workflow systems.
