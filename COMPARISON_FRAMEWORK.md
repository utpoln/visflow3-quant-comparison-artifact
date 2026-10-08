# A quantitative comparison framework: Nextflow, Snakemake, CWL, BioFlow (VisFlow 2.0), Necto (VisFlow 3.0)

This document separates three kinds of claim throughout, per dissertation-defense
standards:

- **(A) Experimentally measured** — run under controlled conditions, specific
  numbers, reproducible from a script in this repo.
- **(B) Objectively countable** — counted directly from a primary source
  (an official spec, a grammar, a source file) with no experiment needed.
- **(C) Qualitative capability** — present/absent/partial, sourced from
  official documentation, not a number.

A fourth label, **Not directly comparable**, is used whenever forcing a
number would misrepresent what's actually being measured — never filled
with an estimate.

---

## Part 1 — Dimension-by-dimension feasibility

| # | Dimension | What's actually measurable across all five | Evidence class |
|---|---|---|---|
| 1 | Expressiveness (constructs) | Whether the language has a *closed, enumerable* construct set at all; the count, where one exists | B (+ C where no closed set exists) |
| 2 | Data integration | Resource-source mechanisms, type-conversion/contract systems | C (+ B for contract primitives) |
| 3 | Language representation | Visual/textual duality, proven equivalence | B/C — only Necto has a *proven* equivalence; this is a presence/absence fact, not a spectrum |
| 4 | Polyglot execution | Number of natively-supported scripting languages, presence of a type-contract layer | B (language count) + C (contract presence) |
| 5 | Reproducibility | Container support, provenance export, resumability | C — all documented, binary presence/absence |
| 6 | Authoring burden | LOC/construct count for an *identical* ported workflow | A — only for workflows actually ported (§3) |
| 7 | Runtime/performance | Wall-clock time for an *identical* ported workflow, same machine | A — only for workflows actually run (§3) |
| 8 | Formal properties | Existence of a formal spec; existence of *proofs* (bijection, non-redundancy, confirmation-locality) | B — presence/absence of a cited theorem is a fact, not a score |

The recurring pattern: dimensions 1, 3, and 8 are mostly **structural facts**
(does X exist, yes/no, cite where) rather than measurements requiring an
experiment. Dimensions 6 and 7 are the *only* ones that require actually
running something, and are only honest for workflows that were actually
ported and run on all five systems — which is why they're scoped tightly to
§3 below rather than generalized to "VisFlow is faster/smaller," full stop.

---

## Part 2 — Metric catalog

Each entry: Metric, Definition, Measurement procedure, Unit, Data required,
measurability per system, Evidence/source, Threats to validity.
Recommended metrics (the 8–12 for the dissertation table) are marked ★.

### Dimension 1 — Expressiveness

**★ M1. Formal grammar existence**
- *Definition*: whether the language is defined by a closed, finite,
  published grammar (vs. an embedding in a general-purpose host language
  with an open-ended construct library).
- *Measurement procedure*: inspect the official specification / paper for
  a grammar (EBNF, BNF, or equivalent) enumerating all constructs.
- *Unit*: presence/absence (C), with the grammar's construct count where one exists (B).
- *Data required*: official spec documents.
- Nextflow: **No** — Groovy-embedded DSL2; no closed grammar document (Di Tommaso et al. 2017, [nextflow.io/docs](https://www.nextflow.io/docs/latest/index.html)).
- Snakemake: **No** — Python-embedded DSL; "workflows are described... using Python syntax" (Köster & Rahmann 2012, abstract).
- CWL: **Yes** — formal spec, v1.2, 4 process classes (`CommandLineTool`, `ExpressionTool`, `Workflow`, `Operation`) ([commonwl.org/v1.2](https://www.commonwl.org/v1.2/); Crusoe et al. 2022).
- BioFlow (VisFlow 2.0): **No** — textual export is a derived translation, not a specified grammar with its own document (dissertation Table 2.1's own note: "BioFlow is a translator, not a projection").
- Necto (VisFlow 3.0): **Yes** — EBNF grammar (dissertation Ch. 5/6; FGCS §Grammar), 17 distinct AST node kinds (counted directly from `src/necto/ast.js`'s `kind:` constructors in this repo).
- *Threats to validity*: "closed grammar" is itself a binary classification call — defensible because each claim is backed by a citable document (or its absence), not a judgment.

**M2. Construct count (raw number)**
- *Definition*: number of distinct top-level language constructs.
- *Measurement procedure*: count enumerated classes in the spec (CWL, Necto); count node types in the palette (VisFlow 2.0); **not defined** for Snakemake/Nextflow, whose rule-directives/channel-operators are open, versioned libraries, not a fixed enumerable set a dissertation could cite a single count for without an arbitrary cutoff.
- CWL: 4 process classes (B).
- Necto: 17 AST kinds (B; counted directly from source, this repo).
- BioFlow/VisFlow 2.0: 14 node types (B; counted directly from `visflow/src/utils/nodeDefinitions.js`'s `NODE_RULES`, this repo).
- Snakemake / Nextflow: **Not directly comparable** — no single authoritative enumeration exists to count against.
- *Threats to validity*: raw construct count is not a proxy for expressive power (a small grammar can still be Turing-complete via embedding, as Nextflow/Snakemake both are via their host languages) — report as a structural fact about *specification style*, not capability.

### Dimension 2 — Data integration

**★ M3. Identifier-drift-aware merge: false-merge rate on a real benchmark**
- *Definition*: of N real cases where a naive join would over-merge
  genuinely distinct entities, how many does the system's own idiomatic
  join strategy falsely merge?
- *Measurement procedure*: run the 116-case over-merge / 100-case true-match corpus (`mapbase_paper/MapBasePlanner/evaluation/data/table5_corpus/`) through each system's natural join expression; see `./RESULTS.md` for the full protocol.
- *Unit*: false merges / 116; recovered / 100.
- All five: **measurable, and measured** (A) — see dissertation-ready table in Part 4.
- *Threats to validity*: "idiomatic join" for Snakemake/Nextflow/CWL means the two ways anyone would write it absent a dedicated primitive (exact match; transitive closure via shared alias) — a sufficiently motivated engineer *could* hand-implement VisFlow's canonical-mediation algorithm in any of the three; the claim is about what ships, not what's theoretically possible to bolt on.

**M4. Resource-source mechanism count**
- *Definition*: number of natively documented ways to declare a data source (file, REST API, database, inline value, etc.).
- CWL: File/Directory types + any CLI tool as a source (C).
- Nextflow: file, S3/GCS/Azure paths, SRA/HTTP via plugins (C).
- Snakemake: local files, remote providers (HTTP/FTP/S3/etc. via `snakemake.remote`) (C).
- BioFlow/VisFlow 2.0: Data node source types — Static value, REST API, Database query, File upload, Environment var (B; `nodeDefinitions.js` `NODE_CONFIG.Data.fields`, 5 types).
- Necto: `ResourceDecl` with `STATIC`/`REST`/wrapper locator forms (B; `ast.js`).
- *Threats to validity*: a documented mechanism count is not a capability ceiling — all five are Turing-complete orchestrators that can call arbitrary code to reach any source; this counts first-class, no-code primitives only.

### Dimension 3 — Language representation

**★ M5. Proven graph/text equivalence**
- *Definition*: does the system have a machine-checkable or mathematically proven guarantee that its visual and textual forms represent the same program?
- Nextflow / Snakemake: **N/A** — no visual form exists at all (C).
- CWL: **No** — no visual authoring form is part of the spec itself (C).
- BioFlow/VisFlow 2.0: **No** — graph is authoritative, BioFlow is a one-way export (dissertation's own characterization) (C).
- Necto/VisFlow 3.0: **Yes** — Theorem 6.1 (bijection of $\Phi$/$\Psi$), machine-checked at corpus scale (see FGCS §Properties; this repo's `necto.test.js` corpus round-trip) (B).
- *Threats to validity*: none of the five comparators claim this property, so there is no disagreement to adjudicate — this is a presence/absence fact, not a judgment call, and is the single cleanest claim in the whole comparison.

### Dimension 4 — Polyglot execution

**M6. Natively supported foreign-call languages**
- Nextflow: any language via `shell`/`exec` (shell-script-level, language-agnostic but no typed contract) (C).
- Snakemake: Python, R, Julia, Rust via `script:`, any via `shell:`/`run:` (C; [snakemake.readthedocs.io](https://snakemake.readthedocs.io), "Scripts" section).
- CWL: any CLI-invokable language via `baseCommand`, no in-process contract (C).
- BioFlow/VisFlow 2.0 & Necto/VisFlow 3.0: Python, R, JavaScript via the Contract Execution Engine, **with** a typed input/output contract and automatic conversion (`convertToInputType`/`mergeByCardinality`, `src/executors/nodeExecutors.js`) (B for language count; C for contract presence).
- *Threats to validity*: "3 languages" is not inherently better than "any language" — CWL/Nextflow's language-agnosticism is a real strength this framework should not obscure; the contract layer is the differentiator, not the raw count.

**★ M7. Typed input/output contract at the integration boundary**
- *Definition*: does invoking a foreign function require/produce a declared type, with automatic conversion, rather than raw untyped text/JSON passthrough?
- CWL: **Yes** — formal type system (File, Directory, array, record, enum, union; part of the v1.2 spec) (B).
- Nextflow / Snakemake: **No** — I/O qualifiers (`val`/`path`/`tuple` in Nextflow; wildcards in Snakemake) are structural, not a conversion contract (C).
- BioFlow/VisFlow 2.0 & Necto: **Yes** — Contract Execution Engine (`deriveContract`/`convertToInputType`, this repo) (B).
- *Threats to validity*: CWL's type system and VisFlow's contract engine solve different problems (CWL types CLI arguments; VisFlow's contract reshapes in-memory data between a tabular canvas and a foreign function) — report as two independently real but non-identical mechanisms, not force a single ranking.

### Dimension 5 — Reproducibility

**M8. Container support** — Nextflow: Docker/Singularity/Apptainer/Podman/Charliecloud/Shifter, native (C). Snakemake: Docker/Singularity per-rule (C). CWL: `DockerRequirement`, part of the core spec (C). BioFlow/Necto: **No** (C; dissertation's own stated limitation, §Limitations / FGCS `tab:compare`).

**M9. Provenance export** — CWL: RO-Crate via `cwltool --provenance` (C). Nextflow: execution trace/report/timeline (C). Snakemake: `--report` HTML summary (C). BioFlow/Necto: execution logs in `executions`/`execution_node_results` tables, no portable provenance bundle format (C).

*Threats to validity (M8–M9)*: both are binary presence/absence facts sourced from official docs; no experiment needed, and no disagreement is plausible — these should appear in the table as settled, not contested.

### Dimension 6 — Authoring burden *(only for workflows actually ported — §3)*

**★ M10. Pipeline-definition LOC for an identical workflow**
- *Definition*: non-blank, non-comment lines in the orchestration-layer file(s) alone — excluding the shared computation every system calls identically.
- *Measurement procedure*: port one real workflow to all five, counting only glue code. See `same_workflow/RESULTS.md`.
- Measured (A) for the one workflow ported so far: Necto 10 / Snakemake 20 / Nextflow 29 / CWL 41 / VisFlow 2.0 — not a line count (graphical).
- *Threats to validity*: one workflow is a worked example, not a generalizable claim; LOC also does not capture authoring *time* or cognitive load, only artifact size.

### Dimension 7 — Runtime/performance *(only for workflows actually run — §3)*

**★ M11. Wall-clock execution time, identical workflow, same machine**
- *Measurement procedure*: 3 repetitions each, same machine, same network conditions, identical underlying computation (verbatim-copied library code). See `same_workflow/RESULTS.md`.
- Measured (A): Snakemake 2.06s / Necto 2.27s / VisFlow 2.0 2.44s / CWL 2.88s / Nextflow 9.81s (means).
- *Threats to validity*: single workflow, dominated by live network I/O common to all five (≈1.8–2.0s floor); isolates *engine overhead*, not general throughput or scalability under load/parallelism — extending to more workflows of varying shape would be needed before claiming a general ordering.

### Dimension 8 — Formal properties

**★ M12. Proven formal properties (count of distinct proven theorems/propositions)**
- CWL: 0 — the v1.2 document is a normative spec, not a theorem-bearing paper (B).
- Nextflow / Snakemake: 0 — no formal-methods publication associated with either system (B).
- BioFlow/VisFlow 2.0: 0 (B).
- Necto/VisFlow 3.0: **4** — bijection (Thm. 6.1), confirmation-site characterization (2 propositions), constructor non-redundancy (Thm., dissertation Ch. 5) (B; cite dissertation theorem labels directly).
- *Threats to validity*: a proof count is not inherently a quality signal independent of what's proven — report alongside a one-line gloss of each theorem's actual content (already in the dissertation), not as a bare number.

---

## Part 3 — Metrics NOT recommended (unfair or unmeasurable as a single number)

- **Raw construct count for Snakemake/Nextflow** — no closed enumeration exists; forcing a number invites an arbitrary cutoff. Report the *absence of a closed grammar* instead (already M1).
- **"Expressiveness score" on any 0–5 or 0–10 scale** — no documented, reproducible scoring rubric exists for any of the eight dimensions; the user's own rule against undefined scores applies directly here.
- **General "execution speed" ranking beyond the one ported workflow** — Nextflow/Snakemake/CWL are built for cluster/HPC-scale parallelism VisFlow was never designed for; a single-machine, single-workflow timing says nothing about scalability, and should never be extrapolated into a blanket speed claim.
- **"Authoring time" (wall-clock minutes to write the pipeline)** — would require a controlled user study with naïve authors in each tool, which doesn't exist and is out of scope; LOC is a defensible *proxy*, authoring time is not available as a measured fact.
- **Community adoption / ecosystem size** as a number (GitHub stars, nf-core pipeline count, etc.) — real, citable, but comparing a 10-year-old community-maintained ecosystem against a single-author research prototype on this axis is not informative; already correctly handled qualitatively in the FGCS paper's `tab:compare` ("research prototype" vs "large").

---

## Part 4 — Dissertation comparison table (defensible numbers only)

| Metric | Nextflow | Snakemake | CWL | BioFlow (VisFlow 2.0) | Necto (VisFlow 3.0) | Evidence |
|---|---|---|---|---|---|---|
| Closed formal grammar (M1) | No | No | Yes (4 classes) | No | Yes (17 AST kinds) | Official specs; `ast.js`, this repo |
| Proven graph/text equivalence (M5) | N/A | N/A | No | No | **Yes** (Thm. 6.1) | FGCS §Properties |
| Typed I/O contract at integration boundary (M7) | No | No | Yes | Yes | Yes | Official spec; `nodeExecutors.js` |
| Native foreign-call languages (M6) | any (shell-level) | Python/R/Julia/Rust + any | any (CLI-level) | Python/R/JS (contract) | Python/R/JS (contract) | Official docs; this repo |
| Container support (M8) | Yes | Yes | Yes | No | No | Official docs; dissertation §Limitations |
| Provenance export (M9) | Yes (trace/report) | Yes (`--report`) | Yes (RO-Crate) | Partial (DB logs only) | Partial (DB logs only) | Official docs; this repo |
| Identifier-drift false-merge rate (M3) | 116/116† | 116/116† | 116/116† | Not implemented in deployed merge‡ | 0/116 (canonical mediation)§ | `./RESULTS.md`, this repo |
| Identifier-drift recall (M3) | 100/100† | 100/100† | 100/100† | Not implemented‡ | 100/100§ | `./RESULTS.md`, this repo |
| Pipeline LOC, 1 ported workflow (M10) | 29 | 20 | 41 | drawn (not line-based) | 10 | `same_workflow/RESULTS.md`, this repo |
| Wall-clock time, 1 ported workflow (M11, mean of 3) | 9.81s | 2.06s | 2.88s | 2.44s | 2.27s | `same_workflow/RESULTS.md`, this repo |
| Proven theorems (M12) | 0 | 0 | 0 | 0 | 4 | Dissertation Ch. 5 |

† Under the transitive-closure join, the natural way to chain two joins through a shared alias column absent a dedicated identity primitive — all three reproduce this exactly (see `./RESULTS.md`). The exact-match alternative scores 0/116 false but 0/100 recovered for all three.
‡ Canonical mediation (dissertation Ch. 3) is a separate, formally proven contribution implemented in a sibling codebase (`mapbase_paper/MapBasePlanner`) — it is **not** currently wired into VisFlow 2.0's or VisFlow 3.0's own deployed `LINK`/`COMBINE` operators, which still use plain syntactic-equality joins (confirmed directly in `src/necto/scheduler.js`'s own code comment). Reporting VisFlow 2.0/3.0 as achieving 0/116 here would overclaim integration that does not exist; the honest entry is "not implemented in the deployed merge," with the formal result reported separately and explicitly as a standalone contribution, not a property of the shipped language.
§ This is MapBasePlanner's own measured result (`table5_safety.py`, canonical mediation semantics), reproduced independently through three external orchestrators in `./RESULTS.md` — included on this row to show what the *formal contribution* achieves, with the caveat in ‡ carried forward rather than hidden.

---

## Part 5 — Benchmark-suite design (for metrics not yet measured)

To extend M10/M11 beyond one workflow, and to measure M3's drift scenario
across more than one corpus:

**Candidate workflow set**: 5–10 workflows drawn from the existing 449-item
corpus (`workflows` table), selected on explicit, stated criteria:
- spans a range of node counts (3–10) and DAG shapes (linear, branching,
  diamond-merge) so LOC/time scaling isn't an artifact of one shape;
- includes at least one workflow with a real external API call (isolates
  network-bound vs. compute-bound timing);
- includes at least one `Combine`/`Fusion` (merge) workflow;
- excludes any workflow using `If`/`Repeat` (composite/control), since
  Necto's deployed scheduler cannot execute these (§Implementation) —
  porting a workflow neither Necto nor, for a fair comparison, the same
  logic expressed in CWL's `when`/`scatter` can execute identically is not
  a fair basis for a timing or LOC comparison; state this exclusion
  explicitly rather than silently dropping the hard cases.

**Protocol per workflow**: port by hand to Snakemake/Nextflow/CWL calling
the verbatim original library code (never reimplemented); run 3 times per
system on the same machine, same network conditions, back-to-back (to
control for time-of-day API latency drift); record wall-clock time and
pipeline-definition LOC for each.

**Statistical treatment**: with only 3 repetitions per cell, report
median and range rather than a parametric mean/CI (the sample is too
small for a normal approximation to be defensible); if the suite grows to
≥10 repetitions per workflow, a paired test (each workflow is a block,
compared across systems) — e.g. a Friedman test across systems with
Wilcoxon signed-rank post-hoc pairs — is appropriate, since the same
workflow/network conditions pair the observations across systems. Report
effect sizes (e.g. a rank-biserial correlation for the Wilcoxon pairs)
alongside p-values; with 5–10 workflows, significance should be
interpreted cautiously, and the honest framing is "consistent with" rather
than "proves."

**Inclusion/exclusion criteria, stated up front**: a workflow is included
only if (a) it translates to Necto's current deployed scope per
`translateGraphToAst` (Data/Library/Adapter/Analytics/Combine/Fusion,
single sink — already machine-checked at corpus scale, §FGCS Implementation),
and (b) every library it calls has no VisFlow-specific runtime dependency
that can't be extracted as a standalone script (true for all pure
Python/R function libraries in the registry; false for anything depending
on in-process VisFlow state).

---

## Part 6 — The six deliverables

### 1. Recommended quantitative comparison table
See Part 4 above — already dissertation-ready, every cell cited.

### 2. Experiments to actually run (in priority order)
1. Extend M10/M11 (LOC + timing) from 1 to 5–10 workflows per the Part 5 protocol — strengthens the single strongest currently-weak point (n=1).
2. Re-run M3's naive-join experiment on a *second*, independent drift corpus if one becomes available, to check the 116/116 result isn't an artifact of this specific corpus's construction.
3. If the mediated-identity integration (†/‡ above) is completed before the defense, re-measure M3 against VisFlow's *own* deployed merge rather than the sibling MapBasePlanner codebase — this closes the single most committee-exploitable gap in the current framework (a reviewer who reads footnote ‡ carefully will ask why the dissertation's flagship safety result isn't in the shipped language).

### 3. Metrics to NOT use
See Part 3 above in full; summarized: no raw construct count for Snakemake/Nextflow, no 0–5 scores anywhere, no speed ranking beyond the ported workflow(s), no authoring-time claim, no adoption-size number.

### 4. Methodology paragraph (dissertation-ready)
> Quantitative comparison against Nextflow, Snakemake, and CWL is scoped to
> what can be measured without fabricating a procedure: structural facts
> sourced directly from each system's official specification or
> documentation (formal grammar existence, construct counts where a closed
> enumeration exists, container and provenance support), and two controlled
> experiments. The first ports a real benchmark corpus — 116 documented
> over-merge cases and 100 true-match cases drawn from NCBI GEO, NCBI
> gene_info, and the HGNC withdrawn-symbol report — to a real, executed
> pipeline in each of the three systems, using the only two join strategies
> expressible without a dedicated identity-mediation primitive (none of the
> three ships one). The second ports one representative corpus workflow,
> calling its original, unmodified library code, to all three systems and
> to VisFlow 2.0 and VisFlow 3.0 directly, measuring wall-clock execution
> time (three repetitions, one machine, controlled network conditions) and
> pipeline-definition lines of code, excluding the shared computation every
> system calls identically. Metrics with no fair, reproducible measurement
> procedure across all five systems — expressiveness scores, raw construct
> counts for systems with no closed grammar, general speed rankings beyond
> the workflows actually ported — are explicitly excluded rather than
> estimated.

### 5. Findings paragraph (dissertation-ready, evidence-scoped)
> Across the structural dimensions, VisFlow 3.0 is the only system of the
> five with a machine-checked proof that its visual and textual forms
> represent the same program (Theorem 6.1); Nextflow and Snakemake, as
> embeddings in general-purpose host languages, have no closed grammar to
> prove such a property about in the first place, and CWL, while formally
> specified, makes no such equivalence claim because it defines no visual
> form. On identifier drift, the two natural ways to express this join in
> Snakemake, Nextflow, or CWL — none of which provides an identity-mediation
> primitive — reproduce the same result independently in all three:
> exact-match recovers nothing (0/100), and the alternative a scientist
> reaches for the moment more than one join chains through a shared alias
> column falsely merges every one of 116 distinct-entity test cases. This
> result characterizes the canonical-mediation algorithm proven in Chapter 3
> and implemented in a companion system, not VisFlow's own currently
> deployed merge operators, which use the same syntactic-equality join as
> the three comparators and inherit the same vulnerability until that
> integration is completed. On the one workflow ported end-to-end, VisFlow
> 2.0 and VisFlow 3.0 add no more orchestration overhead than CWL and
> substantially less than Nextflow, though Snakemake is faster than all
> five; Necto's textual form is the most compact of the four grammars
> compared, and VisFlow 2.0 requires no textual authoring at all for the
> same task. These findings extend only to the workflows and corpus
> actually measured; Part 5 above specifies what a larger benchmark suite
> would need to generalize them.

### 6. Revised Table 2.1 (quantitative + qualitative combined)

See the companion artifact for the fully designed version; in plain form:

| System | Heterog. resources | Multi-lingual | ID drift-aware merge | Proven graph/text | Formal grammar | Container support | Notes |
|---|---|---|---|---|---|---|---|
| Kepler | – | – | ✗ | ✗ | ✗ | – | Director/actor separation; no text form |
| Taverna | ✓ | – | ✗ | ✗ | ✗ | – | Eight built-in service types |
| Galaxy | – | – | ✗ | ✗ | ✗ | ✓ | Strong provenance; no cascade |
| Wings | – | ✗ | ✗ | ✗ | – (OWL-DL) | – | Constraint checking, not a grammar |
| Snakemake | – | ✓ (Python/R/Julia/Rust) | ✗ (116/116 false, measured) | N/A | ✗ | ✓ | Text-only; no canvas |
| Nextflow | – | ✓ (any, shell-level) | ✗ (116/116 false, measured) | N/A | ✗ | ✓ | Text-only; no canvas |
| CWL | – | ✓ (any, CLI-level) | ✗ (116/116 false, measured) | ✗ | ✓ (4 classes) | ✓ (core spec) | Text-only; no canvas; only formally specified comparator |
| VisFlow 2.0 (BioFlow) | ✓ | ✓ (Python/R/JS, contract) | ✗ (not implemented in deployed merge) | ✗ | ✗ | ✗ | BioFlow is a translator, not a projection |
| VisFlow 3.0 (Necto) | ✓ | ✓ (Python/R/JS, contract) | ✗ in deployed merge; 0/116 in proven, separately-implemented mediation | **✓** (Thm. 6.1) | ✓ (17 AST kinds) | ✗ | Formally strongest; weakest on reproducibility infrastructure |

The honest headline this table now supports: VisFlow 3.0's advantages are
**structural/formal**, not operational — it is the only system with a
proven notation-level guarantee, and the only one of the eight surveyed
where the identifier-drift problem has a *proven*, not just engineered,
answer — but it is the weakest of the five systems actually measured on
reproducibility infrastructure (no container support, no portable
provenance format), and that result holds regardless of which way the
other dimensions are read.
