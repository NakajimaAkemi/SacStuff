[General]
ned-path = .;../queueinglib
network = examNetwork
#cpu-time-limit = 60s
cmdenv-config-name = Base
#tkenv-default-config = Base
qtenv-default-config = Base
repeat = 5
sim-time-limit = 10000s
#debug-on-errors = true
**.vector-recording = false

# parameters of the simulation
[Config Base]
description = "Global scenario"
**.mu=5.0

[Config Base1]
extends=Base
**.lambda1=3.5
**.lambda2=3.5