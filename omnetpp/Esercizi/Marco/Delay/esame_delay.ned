import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Delay;

network esame_delay{
    double lambda = default(10);
    double mu = default(10);
    double delta = default(0.1);
    double frac = default(0.7);

    double lambdal = frac * lambda;
    double lambdac = lambda * (1 - frac);

    localSrc.interArrivalTime = 1s * exponential(1/lambdal);
    cloudSrc.interArrivalTime = 1s * exponential(1/lambdac);
    localProc.serviceTime = 1s * exponential(1/mu);
    cloudProc.delay = 1s * exponential(1/mu);
    cloudDelay.delay = 1s * exponential(delta);
    
    submodules:
        localSrc: Source;
        cloudSrc: Source;
        localProc: Queue;
        cloudDelay: Delay;
        cloudProc: Delay;
        sink: Sink;
        
    connections:
        localSrc.out --> localProc.in++;
        localProc.out --> sink.in++;
        cloudSrc.out --> cloudDelay.in++;
        cloudDelay.out --> cloudProc.in++;
        cloudProc.out --> sink.in++;
}