[General]
ned-path = .;../queueinglib
network = MM1
#cpu-time-limit = 60s
cmdenv-config-name = MM1Base
#tkenv-default-config = MM1Base
qtenv-default-config = MM1Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config MM1Base]
description = "Global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
%for K in [5, 7, 10, -1]:
%for rho in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.88, 0.9]:

[Config MM1_rho${"%03d" % int(rho*100)}_K${K if K>0 else "inf"}]
extends=MM1Base
**.K = ${K}
**.rho=${rho}
%endfor
%endfor
