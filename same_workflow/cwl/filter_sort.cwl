#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entryname: run_filter_sort.py
        entry: $(inputs._script)
      - entryname: lib_filter_and_sort.py
        entry: $(inputs._lib)
baseCommand: [python3, run_filter_sort.py]
inputs:
  _script:
    type: File
    default: {class: File, location: ../scripts/run_filter_sort.py}
  _lib:
    type: File
    default: {class: File, location: ../scripts/lib_filter_and_sort.py}
  go_details:
    type: File
    inputBinding: {prefix: --input}
outputs:
  classified_terms:
    type: File
    outputBinding: {glob: classified_terms.json}
arguments: [--out, classified_terms.json]
