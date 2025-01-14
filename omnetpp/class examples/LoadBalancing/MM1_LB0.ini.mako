[General]
ned-path = .;../queueinglib
network = MM1_LB0
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
**.srv1.queueLength.result-recording-modes = +histogram
**.srv2.queueLength.result-recording-modes = +histogram
**.sink1.lifeTime.result-recording-modes = +histogram
**.sink2.lifeTime.result-recording-modes = +histogram

[Config MM1_Unbalanced_Source_NOBAL]
extends=MM1Base
**.Balance="Default"
**.mu1=5.0
**.mu2=5.0
**.lambda1=4.5
**.lambda2=2

