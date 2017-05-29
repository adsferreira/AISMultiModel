(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center 0.0398989709479 0.109773389065 0.0) (radius 0.364606701848) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center -0.101309568068 0.00826939490673 0.0) (radius 0.217489937973) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.171368792276 -0.0956603319062 0.0) (radius 0.100086634254) (height infinity)
		       (material (make dielectric (epsilon 12.082576)))           
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(run)
