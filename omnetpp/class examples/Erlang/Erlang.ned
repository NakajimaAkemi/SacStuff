import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;

network Erlang {
    parameters:
        int K=default(5);
        double rho=default(0.8);
        double mu=default(10);
        double lambda = mu*rho;
        src.interArrivalTime = 1s * exponential(1/lambda);
        srv[*].capacity = -1;
        srv[*].serviceTime = 1s * exponential(1/mu);
    submodules:
        src: Source;
        srv[K]: Queue;
        sink: Sink;
    connections:
        src.out --> srv[0].in++;
        for i=0..K-2 {
            srv[i].out --> srv[i+1].in++;
        }
        srv[K-1].out --> sink.in++;
}


