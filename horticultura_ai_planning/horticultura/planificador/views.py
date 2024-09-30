from django.shortcuts import render, redirect
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _parse, _ground, _search
from pyperplan.search import astar_search
from pyperplan.heuristics.blind import BlindHeuristic
import os

def index(request):
    """
    Muestra la página principal del planificador.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la página principal del planificador.
    """
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'generar_plan':
            return redirect('/generar_plan')
    return render(request, 'index.html')

def mostrar_dominio(request):
    """
    Muestra el contenido del archivo PDDL en una página web.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el contenido del archivo PDDL.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domain_file = os.path.join(base_dir, 'domain.pddl')
    with open(domain_file, 'r') as file:
        domain_content = file.read()
    return render(request, 'dominio.html', {'domain_content': domain_content})

def mostrar_problema(request):
    """
    Muestra el contenido del archivo del problema PDDL en una página web.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el contenido del archivo del problema PDDL.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problem_file = os.path.join(base_dir, 'problem.pddl')
    with open(problem_file, 'r') as file:
        problem_content = file.read()
    return render(request, 'problema.html', {'problem_content': problem_content})

def generar_plan(request):
    """
    Genera un plan basado en los archivos PDDL y lo guarda en la sesión.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la página de ver plan.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domain_file = os.path.join(base_dir, 'domain.pddl')
    problem_file = os.path.join(base_dir, 'problem.pddl')

    # Parsear los archivos PDDL
    parser = Parser(domain_file, problem_file)
    domain = parser.parse_domain()
    problem = parser.parse_problem(domain)

    # Generar el plan
    task = _ground(problem)
    heuristic = BlindHeuristic(task)
    plan = astar_search(task, heuristic)

    # Guardar el plan en la sesión
    plan_steps = [str(step) for step in plan]
    request.session['plan_steps'] = plan_steps
    request.session['initial_state'] = [str(fact) for fact in problem.initial_state]
    request.session['goal'] = [str(fact) for fact in problem.goal]

    return redirect('/ver_plan')

def ver_plan(request):
    """
    Muestra el plan generado guardado en la sesión.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el plan generado.
    """
    plan_steps = request.session.get('plan_steps', [])
    return render(request, 'plan.html', {'plan_steps': plan_steps})

def simulacion(request):
    """
    Muestra una simulación del plan generado en una página web.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la simulación del plan.
    """
    initial_state = request.session.get('initial_state', [])
    plan_steps = request.session.get('plan_steps', [])
    goal = request.session.get('goal', [])

    simulacion_content = "Estado inicial:\n"
    simulacion_content += "\n".join(initial_state)
    simulacion_content += "\n\nPasos del plan:\n"
    simulacion_content += "\n".join(plan_steps)
    simulacion_content += "\n\nEstado final ideal:\n"
    simulacion_content += "\n".join(goal)

    return render(request, 'simulacion.html', {'simulacion_content': simulacion_content})


