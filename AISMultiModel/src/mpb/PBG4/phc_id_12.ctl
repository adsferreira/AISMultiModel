(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center -0.209191414558 -0.0822738846385 0.0) (radius 0.284754958311) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center 0.109234018731 -0.163345144916 0.0) (radius 0.0278072309783) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
		     (make cylinder (center -0.230930195698 -0.430774309181 0.0) (radius 0.056254155075) (height infinity)
                      (material (make dielectric (epsilon 11.56)))   
                     )
		     (make cylinder (center -0.183629694212 -0.448407364893 0.0) (radius 0.00736316698858) (height infinity)  
                      (material (make dielectric (epsilon 11.56)))
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(set! resolution 32)

(run)
