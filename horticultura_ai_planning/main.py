from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search import astar_search
from pyperplan.heuristics.blind import BlindHeuristic

def main():
    domain_file = 'domain.pddl'
    problem_file = 'problem.pddl'
    
    parser = Parser(domain_file, problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    
    task = _ground(problem)
    heuristic = BlindHeuristic(task)
    plan = _search(task, astar_search, heuristic)
    
    for action in plan:
        print(action)

if __name__ == '__main__':
    main()

