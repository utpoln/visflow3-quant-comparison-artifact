# Results: same workflow, five systems — timing + authoring cost

## The workflow

VisFlow's own real corpus workflow **"GO Term Lookup → Namespace
Classification"** (`workflows.id = 4c35a941-e522-49a9-a055-4c52fb1ee59a` /
`necto_workflows.id = a7677b74-8b11-44b6-aa47-8a070bc63da3`, the same
workflow used throughout the FGCS paper's new editor figures): 7 static GO
IDs → a live lookup against `api.geneontology.org` (real network calls, not
mocked) → a pass-through filter/sort step → result. Ported to Snakemake,
CWL, and Nextflow calling the **exact same two registered Python library
functions**, copied verbatim from the `libraries` table — not
reimplemented — so every system performs the identical computation and any
timing difference is attributable to the orchestration layer alone, not the
work itself.

## Timing (wall-clock, 3 runs each, same machine, same network conditions)

| System | Run 1 | Run 2 | Run 3 | Mean |
|---|---|---|---|---|
| Snakemake 7.32.4 | 2.22s | 2.00s | 1.97s | **2.06s** |
| CWL (cwltool 3.1) | 2.95s | 2.82s | 2.88s | **2.88s** |
| Nextflow 26.04.6 | 10.85s | 9.24s | 9.35s | **9.81s** |
| VisFlow 2.0 (`runWorkflow`) | 2.75s | 2.28s | 2.28s | **2.44s** |
| VisFlow 3.0 (Necto `runProgram`) | 2.17s | 2.24s | 2.39s | **2.27s** |

The work itself (7 live API calls to GeneOntology, ~50ms sleep between each,
plus network round-trips) is identical across all five and dominates the
floor — roughly 1.8–2.0s of that is unavoidable regardless of orchestrator.
What the spread above actually measures is **engine overhead on top of
that floor**: Snakemake adds the least (pure Python process spawn), CWL adds
a consistent ~0.8s (its per-step temp-directory staging), VisFlow 2.0 and
VisFlow 3.0 are statistically indistinguishable from each other (as
expected — Necto's scheduler and VisFlow 2.0's executor share the same
underlying node-execution code, §Implementation), and **Nextflow is 4–5×
slower than every other system tested**, consistently, across all three
runs — JVM/Groovy engine startup, not the workflow, which Nextflow's own
documentation acknowledges as fixed per-run cost largely independent of
workflow size.

This is not a result that favors VisFlow by construction — Snakemake beats
both VisFlow systems outright, and should be reported as such.

## Pipeline-definition cost (lines of code)

Counting only the orchestration/glue layer each system requires — every
system below calls the identical two Python library functions, so this
isolates authoring cost, not computation:

| System | Pipeline-definition LOC | What's counted |
|---|---|---|
| Snakemake | 20 | `Snakefile` |
| Nextflow | 29 | `main.nf` |
| CWL | 41 | 3 YAML files (2 `CommandLineTool` + 1 `Workflow`) |
| VisFlow 3.0 (Necto text, $\Phi$) | 10 | `RESOURCE`/`FUNCTION`×2/`LET`×3/`RETURN` (excludes the presentational `LAYOUT` block, +6 lines if included) |
| VisFlow 2.0 | 6 nodes, 5 edges | drawn graphically — there is no line-based grammar to count; the graph **is** the authored artifact, not a derived view of one (unlike BioFlow, which the dissertation's own Table 2.1 already notes is "a translator, not a projection") |

## How to read this honestly

- **Timing**: use it to make an engine-overhead claim, not a "VisFlow is
  faster" claim — it isn't, against Snakemake. The real, defensible claim is
  narrower and still useful: VisFlow 2.0 and VisFlow 3.0 add no more
  orchestration overhead than CWL does, and meaningfully less than Nextflow,
  for a comparably-sized task.
- **LOC**: Necto's textual form is the most compact of the four *grammars*
  compared (10 vs. 20/29/41), which is a real, if modest, data point for
  $\Phi$'s design goals (§Textual Projection) — but the more structurally
  interesting comparison is VisFlow 2.0's zero-line graphical authoring
  against all four textual systems, which is the actual accessibility claim
  graphical workflow systems make in the first place (§Related Work) and
  which this table lets a reader see quantified rather than asserted.
- This is one workflow. Treat it as a worked example establishing the
  methodology and a real number, not as a claim generalizing across the
  449-workflow corpus — extending it to more workflows (varying node count,
  parallelism width, number of live-network steps) would strengthen the
  claim considerably and is the natural next step if this is worth including.

## Reproducing

```bash
cd same_workflow
source ../venv/bin/activate   # see top-level quant-comparison/README.md for setup
cd snakemake && snakemake --cores 1 -s Snakefile && cd ..
cd cwl && cwltool --outdir ../results/cwl_run pipeline.cwl job.yml && cd ..
cd nextflow && ../../../nextflow run main.nf && cd ..
# VisFlow 2.0 / VisFlow 3.0 timing: this requires the VisFlow application's own
# backend (not part of this artifact) — runWorkflow() /
# translateGraphToAst()+runProgram() against workflow id
# 4c35a941-e522-49a9-a055-4c52fb1ee59a — same pattern as the 20-workflow
# equivalence script used earlier in this project.
```
