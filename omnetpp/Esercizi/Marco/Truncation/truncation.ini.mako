[General]
ned-path = .;../queueinglib
network = truncation
cmdenv-config-name = truncation
qtenv-default-config = truncation
repeat = 5
sim-time-limit = 10000s
**.vector-recording = false

[Config truncation]
**.srv.queueLength.result-recording-modes = +histogram
**.lowLoadSrc.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram

%for delta in [0.01, 0.05, 0.1, 0.5, 1]:
[Config truncation-${"%03d" % int(delta*100)}]
extends=truncation
**.delta = ${delta}
%endfor