[General]
ned-path = .;../queueinglib
network = MM1_LB1
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

[Config MM1_Unbalanced_Source]
extends=MM1Base
**.Balance="Default"
**.mu1=5.0
**.mu2=5.0
**.lambda1=4.5
**.lambda2=2

[Config MM1_Unbalanced_Processing]
extends=MM1Base
**.Balance="Default"
**.mu1=6.0
**.mu2=4.0
**.lambda1=4
**.lambda2=4

[Config MM1_Unbalanced_Processing_Bal]
extends=MM1Base
**.Balance="Pers"
**.mu1=6.0
**.mu2=4.0
**.lambda1=4
**.lambda2=4
**.r.randomGateIndex=(uniform(0,10.0)<=6.0?0:1)
