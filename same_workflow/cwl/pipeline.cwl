#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: Workflow
inputs:
  go_terms: File
outputs:
  classified_terms:
    type: File
    outputSource: filter_sort/classified_terms
steps:
  lookup:
    run: lookup.cwl
    in: {go_terms: go_terms}
    out: [go_details]
  filter_sort:
    run: filter_sort.cwl
    in: {go_details: lookup/go_details}
    out: [classified_terms]
