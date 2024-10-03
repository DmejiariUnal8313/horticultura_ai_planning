from django.shortcuts import render, redirect
import os
import random
from pyperplan.pddl.parser import Parser
from pyperplan.task import Task
from pyperplan.planner import _ground
from pyperplan.search import astar_search
from pyperplan.heuristics.blind import BlindHeuristic


# Definir una clase Node simple si no está disponible en pyperplan
class Node:
    def __init__(self, state):
        self.state = state

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

def heuristica(request):
    """
    Aplica una heurística al problema PDDL y muestra el resultado.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el resultado de la heurística.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domain_file = os.path.join(base_dir, 'domain.pddl')
    problem_files = [
        os.path.join(base_dir, 'problem_jardin.pddl'),
        os.path.join(base_dir, 'problem_invernadero.pddl'),
        os.path.join(base_dir, 'problem_huerto.pddl')
    ]

    heuristica_content = ""

    for i, problem_file in enumerate(problem_files):
        # Parsear los archivos PDDL
        parser = Parser(domain_file, problem_file)
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)

        # Generar la tarea
        task = _ground(problem)

        # Aplicar la heurística
        heuristic = BlindHeuristic(task)
        initial_node = Node(task.initial_state)
        heuristic_value = heuristic(initial_node)

        # Añadir detalles al contenido de la respuesta
        heuristica_content += (
            f"Camino {i+1}:\n"
            f"Estado inicial:\n{task.initial_state}\n\n"
            f"Objetivos:\n{task.goals}\n\n"
            f"Valor heurístico aplicado al estado inicial: {heuristic_value}\n\n"
        )

    return render(request, 'heuristica.html', {'heuristica_content': heuristica_content})

def mostrar_dominio_y_problemas(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domain_file = os.path.join(base_dir, 'domain.pddl')
    problem_files = {
        'jardin': os.path.join(base_dir, 'problem_jardin.pddl'),
        'invernadero': os.path.join(base_dir, 'problem_invernadero.pddl'),
        'huerto': os.path.join(base_dir, 'problem_huerto.pddl')
    }
    problems = {}

    with open(domain_file, 'r', encoding='utf-8') as file:
        domain_content = file.read()

    for problem_type, problem_file in problem_files.items():
        with open(problem_file, 'r', encoding='utf-8') as file:
            problems[problem_type] = file.read()

    return render(request, 'dominio_y_problemas.html', {'domain_content': domain_content, 'problems': problems})

def generar_plan(request):
    """
    Genera un plan para cada uno de los problemas específicos.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la página de ver plan.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    domain_file = os.path.join(base_dir, 'domain.pddl')
    problem_files = [
        os.path.join(base_dir, 'problem.pddl'),
        os.path.join(base_dir, 'problem_jardin.pddl'),
        os.path.join(base_dir, 'problem_invernadero.pddl'),
        os.path.join(base_dir, 'problem_huerto.pddl')
    ]

    plans = []

    for problem_file in problem_files:
        # Parsear el archivo PDDL seleccionado
        parser = Parser(domain_file, problem_file)
        domain = parser.parse_domain()
        problem = parser.parse_problem(domain)

        # Generar la tarea
        task = _ground(problem)

        # Aplicar la heurística y buscar el plan
        heuristic = BlindHeuristic(task)
        plan = astar_search(task, heuristic)

        # Convertir el plan a una lista de nombres de acciones
        plan_steps = [str(action) for action in plan]

        # Convertir objetos complejos a tipos de datos simples
        initial_state_str = str(task.initial_state)
        goal_str = str(task.goals)

        # Agregar detalles del plan
        plan_details = {
            'problem_file': os.path.basename(problem_file),
            'initial_state': initial_state_str,
            'goal': goal_str,
            'actions': plan_steps
        }

        # Agregar el plan a la lista de planes
        plans.append(plan_details)

    # Guardar los planes en la sesión
    request.session['plans'] = plans

    return redirect('/ver_plan')

def ver_plan(request):
    """
    Muestra los planes generados guardados en la sesión.
    """
    plans = request.session.get('plans', [])
    return render(request, 'ver_plan.html', {'plans': plans})

def simulacion(request):
    """
    Muestra una simulación de los planes generados en una página web.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la simulación de los planes.
    """
    plans = request.session.get('plans', [])

    simulacion_content = ""
    for i, plan in enumerate(plans):
        simulacion_content += f"Simulación del Camino {i+1}:\n" + "\n".join(plan) + "\n\n"

    return render(request, 'simulacion.html', {'simulacion_content': simulacion_content})
