[General]
ned-path = .;../queueinglib
network = unbalanced
cmdenv-config-name = unbalanced
#tkenv-default-config = MM1Base
qtenv-default-config = unbalanced
repeat = 5
sim-time-limit = 10000s
**.vector-recording = false

[Config unbalanced]
description = "Global Scenario"
**.highLoadSrv.queueLength.result-recording-modes = +histogram
**.lowLoadSrv.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0, 1, 2, 3]:
[Config unbalanced-${delta}]
extends = unbalanced
**.delta = ${delta}
%endfor