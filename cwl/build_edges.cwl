#!/usr/bin/env cwl-runner
# CWL CommandLineTool: step 1 of the naive-integration pipeline (see
# scripts/build_edges.py for what this actually does and why). CWL has no
# identity-mediation primitive either — a CommandLineTool just wraps
# whatever command a scientist would run, which is this script.
cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: build_edges.py
        entry: $(inputs._script)
baseCommand: [python3, build_edges.py]
inputs:
  _script:
    type: File
    default: {class: File, location: ../scripts/build_edges.py}
  negative:
    type: File
    inputBinding: {prefix: --negative}
  positive:
    type: File
    inputBinding: {prefix: --positive}
outputs:
  edges:
    type: File
    outputBinding: {glob: edges.csv}
arguments:
  - --out
  - edges.csv
