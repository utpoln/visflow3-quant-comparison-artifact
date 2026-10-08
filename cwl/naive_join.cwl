#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: naive_join.py
        entry: $(inputs._script)
baseCommand: [python3, naive_join.py]
inputs:
  _script:
    type: File
    default: {class: File, location: ../scripts/naive_join.py}
  edges:
    type: File
    inputBinding: {prefix: --edges}
  mode:
    type: string
    inputBinding: {prefix: --mode}
outputs:
  groups:
    type: File
    outputBinding: {glob: groups.csv}
arguments:
  - --out
  - groups.csv
