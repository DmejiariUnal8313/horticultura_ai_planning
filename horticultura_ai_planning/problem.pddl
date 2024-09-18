(define (problem horticultura-problema)
  (:domain horticultura)
  
  (:objects
    planta1 planta2 - planta
    regadera - herramienta
    jardin invernadero - lugar
  )
  
  (:init
    (en-lugar planta1 jardin)
    (en-lugar planta2 invernadero)
    (tiene-herramienta regadera)
  )
  
  (:goal
    (and
      (plantada planta1)
      (regada planta1)
      (plantada planta2)
      (regada planta2)
    )
  )
)