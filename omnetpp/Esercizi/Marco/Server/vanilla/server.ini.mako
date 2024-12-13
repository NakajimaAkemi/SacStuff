[General]
ned-path = .;../queueinglib
network = server
cmdenv-config-name = server
#tkenv-default-config = MM1Base
qtenv-default-config = server
repeat = 5
sim-time-limit = 10000s
**.vector-recording = false

[Config server]
**.net.queueLength.result-recording-modes = +histogram
**.cpu.queueLength.result-recording-modes = +histogram
**.disk.queueLength.result-recording-modes = +histogram
**.sink.lifeTime.result-recording-modes = +histogram
**.mun = 20
**.muc = 10
**.mud = 15
**.lambda = 6

%for lada in [7, 7.9, 8]:
[Config server-${"%03d" % int(lada*100)}]
extends=server
**.lambda = ${lada}
%endfor