#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: evaluate.py
        entry: $(inputs._script)
baseCommand: [python3, evaluate.py]
inputs:
  _script:
    type: File
    default: {class: File, location: ../scripts/evaluate.py}
  negative:
    type: File
    inputBinding: {prefix: --negative}
  positive:
    type: File
    inputBinding: {prefix: --positive}
  groups:
    type: File
    inputBinding: {prefix: --groups}
  mode:
    type: string
    inputBinding: {prefix: --mode}
outputs:
  result:
    type: File
    outputBinding: {glob: result.json}
arguments:
  - --out
  - result.json
