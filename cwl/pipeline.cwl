#!/usr/bin/env cwl-runner
# CWL Workflow: the naive-integration baseline, one run per join mode
# (exact | transitive) — see scripts/naive_join.py for what each means.
cwlVersion: v1.2
class: Workflow
inputs:
  negative: File
  positive: File
  mode: string
outputs:
  result:
    type: File
    outputSource: evaluate/result
steps:
  build_edges:
    run: build_edges.cwl
    in:
      negative: negative
      positive: positive
    out: [edges]
  naive_join:
    run: naive_join.cwl
    in:
      edges: build_edges/edges
      mode: mode
    out: [groups]
  evaluate:
    run: evaluate.cwl
    in:
      negative: negative
      positive: positive
      groups: naive_join/groups
      mode: mode
    out: [result]
