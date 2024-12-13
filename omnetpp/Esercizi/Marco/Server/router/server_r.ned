import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Router;

network server_r{
    parameters:
        double lambda = default(6);
        double mun = default(20);
        double muc = default(10);
        double mud = default(15);

        src.interArrivalTime = 1s * exponential(1/lambda);
        net.serviceTime = 1s * exponential(1/mun);
        cpu1.serviceTime = 1s * exponential(1/muc);
        cpu2.serviceTime = 1s * exponential(1/muc);
        disk.serviceTime = 1s * exponential(1/mud);
        r.routingAlgorithm = "random";
    submodules:
        src: Source;
        net: Queue;
        r: Router;
        cpu1: Queue;
        cpu2: Queue;
        disk: Queue;
        sink: Sink;

    connections:
        src.out --> net.in++;
        net.out --> r.in++;
        r.out++ --> cpu1.in++;
        r.out++ --> cpu2.in++;
        cpu1.out --> disk.in++;
        cpu2.out --> disk.in++;
        disk.out --> sink.in++;
}