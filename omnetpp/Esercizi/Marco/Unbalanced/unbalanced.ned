import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;

network unbalanced{
    parameters:
        double mu = default(10);
        double lambda = default(6);
        double delta = default(0);

        highLoadSrc.interArrivalTime = 1s * exponential(1/(lambda + delta));
        lowLoadSrc.interArrivalTime = 1s * exponential(1/(lambda - delta));

        highLoadSrv.serviceTime = 1s * exponential(1/mu);
        lowLoadSrv.serviceTime = 1s * exponential(1/mu);

    submodules:
        lowLoadSrv: Queue;
        highLoadSrv: Queue;
        highLoadSrc: Source;
        lowLoadSrc: Source;
        sink: Sink;

    connections:
        lowLoadSrc.out --> lowLoadSrv.in++;
        lowLoadSrv.out --> sink.in++;
        highLoadSrc.out --> highLoadSrv.in++;
        highLoadSrv.out --> sink.in++;
}