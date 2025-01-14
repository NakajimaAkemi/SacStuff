[General]
ned-path = .;../queueinglib
network = Erlang
#cpu-time-limit = 60s
cmdenv-config-name = ErlangBase
#tkenv-default-config = ErlangBase
qtenv-default-config = ErlangBase
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config ErlangBase]
description = "Global scenario"
**.srv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
**.rho=0.8
%for K in [1, 2, 3, 4]:

[Config Erlang_K${"%d" % K}]
extends=ErlangBase
**.K=${K}
%endfor

