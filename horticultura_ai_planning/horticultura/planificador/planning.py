from pyperplan.pddl.parser import Parser
from pyperplan.task import Task
from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.search.breadth_first_search import breadth_first_search

def parse_problem(domain_file, problem_file):
    parser = Parser(domain_file, problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)
    return domain, problem

def generate_task(domain, problem):
    initial_state = problem.initial_state
    goal = problem.goal
    operators = domain.actions  # Cambiar 'operators' a 'actions'
    task = Task(initial_state, goal, operators)
    return task

def apply_heuristic(task):
    heuristic = BlindHeuristic(task)
    return heuristic(task.initial_state)

def generate_plan(task):
    plan = breadth_first_search(task)
    return plan