[General]
ned-path = .;../queueinglib
network = esame_delay
#cpu-time-limit = 60s
cmdenv-config-name = esame_delay
#tkenv-default-config = MM1Base
qtenv-default-config = esame_delay
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

[Config esame_delay]
**.sink.lifeTime.result-recording-modes = +histogram

%for frac in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ,0.9]:
[Config esame_delay_frac-${"%04d" % int(frac*1000)}]
extends = esame_delay
**.frac = ${frac}
%endfor
