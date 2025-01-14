import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network MM1 {
    parameters:
        int K=default(10);
        double rho=default(0.8);
        double mu=default(10);
        double lambda = mu*rho;
        src.interArrivalTime = 1s * exponential(1/lambda);
        srv.capacity = K;
        srv.serviceTime = 1s * exponential(1/mu);
    submodules:
        src: Source;
        srv: Queue;
        sink: Sink;
    connections:
        src.out --> srv.in++;
        srv.out --> sink.in++;
}


