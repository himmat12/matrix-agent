import json
from runner import run_benchmark
from agent.tool_calling_agent import  run_agent

with open("output/benchmark.json", "r") as f:
    benchmark = json.load(f)

results = run_benchmark(run_agent, benchmark["test_cases"])
print(results)