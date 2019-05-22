T0
G91
G1 Z3 F7500         ; lower print platform slightly
G90
G1 X0,Y100 F6000    ;go to left side quickly, at the center
G1 X-12 F500        ;make the switch, slowly
G1 F7500
T1

;optionalG1
;optionalZmove
