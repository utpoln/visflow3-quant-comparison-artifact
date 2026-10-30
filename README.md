# VisFlow 3.0 — Quantitative Comparison Artifact

Evaluation artifact accompanying the dissertation *"Declarative Visual
Workflow Orchestration over Distributed FAIR Resources: A Theory and System
for Autonomous Scientific Computing."* This repo backs dissertation §7.4,
"A Quantitative Comparison Against Nextflow, Snakemake, and CWL" (Tables
7.6–7.7) — written in direct response to a committee request for a measured,
not purely qualitative, comparison against the three text-based workflow
systems the dissertation's own related-work survey (Table 2.1) already
groups together.

Two independent experiments:

1. **Identifier-drift correctness** (`scripts/`, `snakemake/`, `cwl/`,
   `nextflow/`) — the real 116-case over-merge / 100-case true-match corpus
   (`data/`) run through the two natural naive-join pipelines (exact-match,
   transitive-closure) in all three systems. See `RESULTS.md`.
2. **Same-workflow LOC/timing** (`same_workflow/`) — a real VisFlow corpus
   workflow ("GO Term Lookup → Namespace Classification"), calling its exact
   registered library code, ported to all three systems and timed against
   VisFlow 2.0 and VisFlow 3.0 directly. See `same_workflow/RESULTS.md`.

A third, unrelated evaluation also lives in this repo as a matter of
convenience, not because it's part of the Nextflow/Snakemake/CWL comparison:

3. **VisFlow 3.0 Φ/Ψ round-trip fidelity** (`roundtrip-evaluation/`) — backs
   Chapter 6's "Empirical Support for the Projection" claim, re-run against
   a restored copy of the real production workflow corpus. See
   `roundtrip-evaluation/README.md`.

`COMPARISON_FRAMEWORK.md` documents the full metric-by-metric methodology
behind both: what's measured, what's objectively counted, what's qualitative,
and what's explicitly excluded as unfair or unmeasurable.

## Why this exists

A dissertation committee member asked, of Table 2.1, **where the quantitative
comparison is**. It wasn't anywhere — every number in the dissertation and
the companion FGCS paper was measured on VisFlow alone; no other system was
ever actually run. Installing and fairly benchmarking the GUI/server-based
systems in that table (Kepler, Taverna, Galaxy, Wings, KNIME, Orange,
RapidMiner) is not realistic on a short timeline; Snakemake, Nextflow, and
CWL are lightweight, pip/CLI-installable, no GUI or account needed — real
numbers against these three were achievable, and this repo is that work.

## What's being compared (identifier drift)

The corpus in `data/` (sourcing: see `data/metadata.json`) also backs
dissertation Chapter 3's own Experiment 3, which evaluates three merge
*semantics*:

| Semantics | False merges | Recovered |
|---|---|---|
| Syntactic (exact string match) | 0/116 | 0/100 |
| Transitive closure (chain through shared alias) | 116/116 | 100/100 |
| **Canonical mediation (Chapter 3's own algorithm)** | **0/116** | **100/100** |

The first two rows are not arbitrary baselines — they are *exactly* the two
ways anyone would naturally write this join in Snakemake, Nextflow, or CWL,
because **none of the three provides any identity-mediation primitive at
all**. This repo re-implements both as **real, runnable pipelines in all
three systems** — independent scripts (`scripts/`) invoked by a real
`Snakefile`, a real CWL `Workflow`, and a real Nextflow `main.nf` — run
against the identical corpus, through each tool's actual execution engine.

**Important scope note** (carried through verbatim into the dissertation):
canonical mediation is proven and evaluated as a standalone algorithm in a
separate codebase (see
[`mediated-identity-evaluation`](https://github.com/utpoln/mediated-identity-evaluation)
for the corpus's canonical source and full provenance), not yet integrated
into VisFlow 2.0's or VisFlow 3.0's own deployed `LINK`/`COMBINE` operators.
Those operators currently perform the same plain syntactic-equality join as
Snakemake/Nextflow/CWL, and so share the same identifier-drift vulnerability
until that integration is completed. `data/` here is a copy of that repo's
corpus, included directly so this repo's pipelines are self-contained and
runnable without a second clone.

## Layout

```
data/                    the corpus (negative_cases.csv, positive_cases.csv,
                          metadata.json) — copied from mediated-identity-evaluation;
                          see that repo for full sourcing/provenance documentation
scripts/                 the shared, tool-agnostic join + scoring logic
                          (build_edges.py, naive_join.py, evaluate.py) —
                          identical code called by all three pipelines, so any
                          difference in outcome could only come from the join
                          strategy, never from which orchestrator ran it
snakemake/Snakefile      real Snakemake pipeline
cwl/*.cwl, *.yml         real CWL CommandLineTools + Workflow + job inputs
nextflow/main.nf         real Nextflow pipeline
results/                 output of actually running all three (JSON results +
                          full console logs under results/logs/)
same_workflow/           the second experiment (LOC + timing), self-contained
RESULTS.md               the final numbers, narrative, and the LaTeX table
                          fragments used in the dissertation
COMPARISON_FRAMEWORK.md  the full metric-by-metric methodology
```

## Reproducing

Needs Python 3.9+, and three external tools. On macOS, `datrie` (a Snakemake
dependency) fails to build against a stale conda `llvm-ar` unless overridden:

```bash
python3 -m venv venv && source venv/bin/activate
AR=/usr/bin/ar CC=/usr/bin/clang pip install snakemake cwltool pandas
pip install "pulp<2.8"   # snakemake 7.x expects pulp's older solver API
curl -s https://get.nextflow.io | bash   # installs ./nextflow in the cwd

cd snakemake && snakemake --cores 1 -s Snakefile -p && cd ..
cd cwl && cwltool --outdir ../results/cwl_exact pipeline.cwl job_exact.yml \
       && cwltool --outdir ../results/cwl_transitive pipeline.cwl job_transitive.yml && cd ..
cd nextflow && ../nextflow run main.nf && cd ..
```

Repeat under `same_workflow/` the same way (see `same_workflow/RESULTS.md`).

## What this does *not* claim

- It does not benchmark Kepler, Taverna, Galaxy, Wings, KNIME, Orange, or
  RapidMiner — those remain qualitative, sourced from their own publications;
  the dissertation says so explicitly rather than leaving the gap silent.
- It does not claim Snakemake/Nextflow/CWL are incapable of identity
  mediation in principle — a sufficiently motivated user could hand-write a
  canonicalization step equivalent to Chapter 3's. The claim is narrower and
  is the one the committee actually asked for a number on: *none of the
  three ships one*, so the idiomatic, undocumented-pitfall-free pipeline a
  working scientist writes today is one of these two, and both fail one of
  the two properties canonical mediation gets simultaneously.
- It does not include the canonical-mediation algorithm's own implementation
  — only the corpus it's evaluated against. That algorithm lives in a
  separate codebase tied to its own publication, not yet public.

## Related artifacts

- Mediated-identity corpus (canonical source, full provenance docs):
  https://github.com/utpoln/mediated-identity-evaluation
- VisFlow 2.0 (benchmark harness, seeded workflows, execution logs):
  https://github.com/utpoln/visflow2-evaluation-artifact
- CroW (web-extraction benchmark, case study, seeded-repository data):
  https://github.com/smart-db-lab/crow2-evaluation

## License

MIT (see `LICENSE`) for all code in this repository. `data/` is a copy of
public NCBI GEO, NCBI Gene, and HGNC reference data — see
[`mediated-identity-evaluation`](https://github.com/utpoln/mediated-identity-evaluation)
for exact sourcing and URLs.
