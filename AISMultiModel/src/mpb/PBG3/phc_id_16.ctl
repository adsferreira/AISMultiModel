(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center 0.396980644642 -0.00845111626614 0.0) (radius 0.0353352713118) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.187250471553 0.21399900219 0.0) (radius 0.12784683713) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center 0.390663042356 -0.0160805368542 0.0) (radius 0.0421348749165) (height infinity)
		       (material (make dielectric (epsilon 12.082576)))           
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(run)
