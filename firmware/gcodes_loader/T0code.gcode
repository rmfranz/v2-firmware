G91
G1 Z3 F7500
G90
G1 X200 F6000 ;don't go above or it may lose steps
G1 X220 F500
G1 X100 Y100 F7000 ; go to the center of the platform (do not remove or it will not calibrate correctly)
T0

;optionalG1
;optionalZmove
