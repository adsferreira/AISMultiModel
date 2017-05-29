(set! num-bands 16)
(set! mesh-size 7)

(set! k-points (list (vector3 0 0 0)     ; Gamma
                     (vector3 0.5 0 0)   ; X
                     (vector3 0.5 0.5 0) ; M
                     (vector3 0 0 0)))   ; Gamma

(set! k-points (interpolate 4 k-points))

(set! geometry (list 
                     (make cylinder (center 0.00636321617137 -0.0177616116075 0.0) (radius 0.388405463051) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center -0.289342497734 -0.28380274294 0.0) (radius 0.170153280904) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center -0.133254754848 0.178175528872 0.0) (radius 0.0523006732363) (height infinity)
                      (material (make dielectric (epsilon 11.56)))   
                     )
                     (make cylinder (center 0.36840920396 0.0407214757707 0.0) (radius 0.0298672668592) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center -0.062729161998 0.36038804876 0.0) (radius 0.0334891122886) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center 0.172617242729 0.478475744063 0.0) (radius 0.0155288057974) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center -0.0213867908885 0.296683981233 0.0) (radius 0.106459756515) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center -0.135393577668 -0.00189169693325 0.0) (radius 0.188654943666) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center 0.365215685468 0.0408678801542 0.0) (radius 0.127030336213) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
                     (make cylinder (center 0.0857986425555 -0.268296206239 0.0) (radius 0.206916519766) (height infinity)
                      (material (make dielectric (epsilon 11.56)))
                     )
               )
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))
(set! output-epsilon (lambda () (print "skipping output-epsilon\n")))
(set! resolution 32)

(run)
