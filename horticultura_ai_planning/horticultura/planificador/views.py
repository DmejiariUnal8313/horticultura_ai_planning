from django.shortcuts import render
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search.astar import astar_search
from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search.astar import astar_search
from pyperplan.heuristics.blind import BlindHeuristic

def generar_plan(request):
	if request.method == 'POST':
		domain_file = 'domain.pddl'
		problem_file = 'problem.pddl'
		
		parser = Parser(domain_file, problem_file)
		domain = parser.parse_domain()
		problem = parser.parse_problem(domain)
		
		task = _ground(problem)
		heuristic = BlindHeuristic(task)
		plan = _search(task, astar_search, heuristic)
		
		plan_str = '\n'.join(str(action) for action in plan)
		return render(request, 'plan.html', {'plan': plan_str})
	return render(request, 'index.html')