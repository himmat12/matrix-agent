
import json
from dataclasses import dataclass, asdict

def score_case(result, case):
    score = 0
    score += int(result.get('tool_selection_correct', False))
    score += int(result.get('arguments_correct', False))
    score += int(result.get('final_correct', False))
    score += int(result.get('error_handled', False))
    score += int(result.get('efficient', False))
    return score

def run_benchmark(agent, cases):
    results = []
    for case in cases:
        result = agent(case['prompt'])
        results.append({'id': case['id'], 'case': case, 'result': result, 'score': score_case(result, case)})
    return results

if __name__ == '__main__':
    print('Import this module and pass in an agent callable.')
    
