#!/usr/bin/env bash
set -euo pipefail

CORE_ID=2
RUNS=10
ITERATIONS=1
RESULT_FILE="logs/final/graph-traverse-write-nocache-pilot.csv"

printf '%s\n' \
  'timestamp,run_id,order,configuration,graph,core,iterations,flags,wall_time_s,user_time_s,sys_time_s,vol_ctx,invol_ctx,minflt,majflt,exit_status' \
  > "$RESULT_FILE"

run_case() {
  local run_id="$1"
  local order="$2"
  local configuration="$3"
  local graph="$4"
  local timestamp

  timestamp=$(date --iso-8601=seconds)

  /usr/bin/time \
    -f "$timestamp,$run_id,$order,$configuration,$graph,$CORE_ID,$ITERATIONS,\"--write --no-cache\",%e,%U,%S,%w,%c,%R,%F,%x" \
    -a -o "$RESULT_FILE" \
    taskset -c "$CORE_ID" \
    ./out/graph_traverse --write --no-cache "$ITERATIONS" "$graph" \
    > /dev/null

  sleep 2
}

for ((run_id = 1; run_id <= RUNS; run_id++)); do
  if ((run_id % 2 == 1)); then
    run_case "$run_id" 1 seq graph-seq.bin
    run_case "$run_id" 2 rand graph-rand.bin
  else
    run_case "$run_id" 1 rand graph-rand.bin
    run_case "$run_id" 2 seq graph-seq.bin
  fi
done
