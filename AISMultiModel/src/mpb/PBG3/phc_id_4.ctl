(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center -0.186824150069 -0.0651277292996 0.0) (radius 0.180039744437) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.011094499857 0.338135649526 0.0) (radius 0.0550541313622) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.156240822001 -0.0855356981961 0.0) (radius 0.283376702184) (height infinity)
		       (material (make dielectric (epsilon 12.082576)))           
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(run)
