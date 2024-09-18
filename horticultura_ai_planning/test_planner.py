import unittest
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search.astar import astar_search
from pyperplan.heuristics.blind import BlindHeuristic

class TestPlanner(unittest.TestCase):
    def test_plan(self):
        domain_file = 'domain.pddl'
        problem_file = 'problem.pddl'
        
        parser = Parser(domain_file, problem_file)
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)
        
        task = _ground(problem)
        heuristic = BlindHeuristic(task)
        plan = _search(task, astar_search, heuristic)
        
        expected_plan = [
            '(plantar planta2 invernadero)',
            '(plantar planta1 jardin)',
            '(regar planta2)',
            '(regar planta1)'
        ]
        
        self.assertEqual([str(action) for action in plan], expected_plan)

if __name__ == '__main__':
    unittest.main()