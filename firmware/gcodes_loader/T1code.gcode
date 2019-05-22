T0
G91
G1 Z3 F7500			; bajar la plataforma ligeramente
G90
G1 X0,Y100 F7500	;ir hacia el costado izq. rápidamente, pero en el centro
G1 X-12 F500		;hacer el cambio lentamente
G1 F7500
T1

;optionalG1
;optionalZmove
