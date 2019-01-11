G90             ;absolute mode
G28 XY ; agregado martin
G1 X100 Y100 F4000 ; agregado martin
G28 Z ; agregado martin
G0 Z10 F7200    ;make nozzles be about 10 cm above bed
T0 ;change to T0
; G32             ;perform bed levelling
;findBedSetOrigin
G0 Z10 F7200
