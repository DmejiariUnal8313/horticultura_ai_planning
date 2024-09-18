# app.py
from flask import Flask, render_template, request
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search.astar import astar_search
from pyperplan.heuristics.blind import BlindHeuristic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    domain_file = 'domain.pddl'
    problem_file = 'problem.pddl'
    
    parser = Parser(domain_file, problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    
    task = _ground(problem)
    heuristic = BlindHeuristic(task)
    plan = _search(task, astar_search, heuristic)
    
    plan_str = '\n'.join(str(action) for action in plan)
    return render_template('plan.html', plan=plan_str)

if __name__ == '__main__':
    app.run(debug=True)