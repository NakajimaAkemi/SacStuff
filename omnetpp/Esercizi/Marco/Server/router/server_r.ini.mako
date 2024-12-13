[General]
ned-path = .;../queueinglib
network = server_r
cmdenv-config-name = server_r
qtenv-default-config = server_r
repeat = 5
sim-time-limit = 10000s
**.vector-recording = false

[Config server_r]
**.net.queueLength.result-recording-modes = +histogram
**.cpu1.queueLength.result-recording-modes = +histogram
**.cpu2.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
**.mun = 20
**.muc = 10
**.mud = 15
**.lambda = 6

%for lada in [10, 11, 12]:
[Config server_r-${"%03d" % int(lada*100)}]
extends=server_r
**.lambda = ${lada}
%endfor