(define (problem horticultura-problema-jardin)
  (:domain horticultura)
  
  (:objects
    planta1 planta4 - planta
    regadera fertilizante tijeras - herramienta
    jardin - lugar
    camino1 - camino
  )
  
  (:init
    (en-lugar planta1 jardin)
    (en-lugar planta4 jardin)
    (tiene-herramienta regadera)
    (tiene-herramienta fertilizante)
    (tiene-herramienta tijeras)
    (conectado jardin camino1)
  )

  (:goal
    (and
      (cosechada planta1)
      (cosechada planta4)
    )
  )
)