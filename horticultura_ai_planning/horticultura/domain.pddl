(define (domain horticultura)
  (:requirements :strips :typing :action-costs)
  
  (:types
    planta herramienta lugar camino calidad ; Anadir 'camino' aqui
  )
  
  (:predicates
    (en-lugar ?p - planta ?l - lugar)
    (tiene-herramienta ?h - herramienta)
    (plantada ?p - planta)
    (regada ?p - planta)
    (fertilizada ?p - planta)
    (podada ?p - planta)
    (cosechada ?p - planta)
    (conectado ?l1 - lugar ?l2 - lugar)  ; Anadir predicado 'conectado'
    (todas_plantas_cultivadas)  ; Añadir predicado 'todas_plantas_cultivadas'
  )
  
  (:action plantar
    :parameters (?p - planta ?l - lugar)
    :precondition (and (en-lugar ?p ?l))
    :effect (plantada ?p)
    :cost 1
  )
  
  (:action regar
    :parameters (?p - planta)
    :precondition (and (plantada ?p))
    :effect (regada ?p)
    :cost 1
  )
  
  (:action fertilizar
    :parameters (?p - planta)
    :precondition (and (plantada ?p))
    :effect (fertilizada ?p)
    :cost 2
  )
  
  (:action podar
    :parameters (?p - planta)
    :precondition (and (plantada ?p))
    :effect (podada ?p)
    :cost 2
  )
  
  (:action cosechar
    :parameters (?p - planta)
    :precondition (and (plantada ?p) (regada ?p) (fertilizada ?p) (podada ?p))
    :effect (cosechada ?p)
    :cost 3
  )
)