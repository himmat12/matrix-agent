
# Arithmetic Tool Agent Benchmark

This benchmark evaluates an agent using arithmetic tools: add, subtract, multiply, divide, mod, pi, and get_x_percentage_of_y.

## Suggested evaluation loop
1. Load the JSON benchmark specification.
2. Run each prompt through the agent.
3. Capture tool calls, arguments, latency, and final answer.
4. Score each case with the rubric.
5. Aggregate by category and overall weighted score.

## What to log
- Prompt
- Tool sequence
- Tool arguments
- Tool outputs
- Final answer
- Error messages
- Latency
- Number of retries

## Notes
- Keep one expected primary tool per simple case.
- For chained tasks, allow a sequence of tool calls.
- For invalid inputs, require graceful failure.
