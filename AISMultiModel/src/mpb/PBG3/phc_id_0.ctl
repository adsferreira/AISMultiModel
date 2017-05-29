(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center -0.00611125062438 -0.152529403451 0.0) (radius 0.0624392287492) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.103083551051 -0.17430391454 0.0) (radius 0.032491831211) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center -0.188812941376 0.0757564206408 0.0) (radius 0.277435966938) (height infinity)
		       (material (make dielectric (epsilon 12.082576)))           
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(run)
