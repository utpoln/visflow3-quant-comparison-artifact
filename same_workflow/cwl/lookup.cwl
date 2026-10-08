#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: run_lookup.py
        entry: $(inputs._script)
      - entryname: lib_go_term_lookup.py
        entry: $(inputs._lib)
baseCommand: [python3, run_lookup.py]
inputs:
  _script:
    type: File
    default: {class: File, location: ../scripts/run_lookup.py}
  _lib:
    type: File
    default: {class: File, location: ../scripts/lib_go_term_lookup.py}
  go_terms:
    type: File
    inputBinding: {prefix: --input}
outputs:
  go_details:
    type: File
    outputBinding: {glob: go_details.json}
arguments: [--out, go_details.json]
