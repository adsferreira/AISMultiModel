(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center 0.151596009404 0.000458819352781 0.0) (radius 0.312812232256) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center -0.388437480821 -0.200250419132 0.0) (radius 0.0282894622822) (height infinity)
                       (material (make dielectric (epsilon 12.082576)))
                     )
                     (make cylinder (center -0.0126810732565 -0.303117308476 0.0) (radius 0.0907869634235) (height infinity)
		       (material (make dielectric (epsilon 12.082576)))           
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! resolution 32)
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(run)
