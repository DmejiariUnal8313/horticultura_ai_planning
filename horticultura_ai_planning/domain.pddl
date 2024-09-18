(define (domain horticultura)
  (:requirements :strips :typing)
  
  (:types
    planta herramienta lugar
  )
  
  (:predicates
    (en-lugar ?p - planta ?l - lugar)
    (tiene-herramienta ?h - herramienta)
    (plantada ?p - planta)
    (regada ?p - planta)
  )
  
  (:action plantar
    :parameters (?p - planta ?l - lugar)
    :precondition (and (en-lugar ?p ?l))
    :effect (plantada ?p)
  )
  
  (:action regar
    :parameters (?p - planta)
    :precondition (and (plantada ?p))
    :effect (regada ?p)
  )
)