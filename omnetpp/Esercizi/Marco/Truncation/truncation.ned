import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;

network truncation{
    parameters:
        double lambda = default(6);
        double mu = default(10);
        double delta = default(0.01);

        lowLoadSrc.interArrivalTime = 1s * exponential(1/lambda);
        srv.serviceTime = 1s * truncnormal((1/mu), delta);

    submodules:
        srv: Queue;
        lowLoadSrc: Source;
        sink: Sink;
    connections:
        lowLoadSrc.out --> srv.in++;
        srv.out --> sink.in++;
}