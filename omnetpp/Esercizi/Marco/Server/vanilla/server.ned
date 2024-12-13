import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;

network server{
    parameters:
        double lambda = default(6);
        double mun = default(20);
        double muc = default(10);
        double mud = default(15);

        src.interArrivalTime = 1s * exponential(1/lambda);
        net.serviceTime = 1s * exponential(1/mun);
        cpu.serviceTime = 1s * exponential(1/muc);
        disk.serviceTime = 1s * exponential(1/mud);
    
    submodules:
        src: Source;
        net: Queue;
        cpu: Queue;
        disk: Queue;
        sink: Sink;

    connections:
        src.out --> net.in++;
        net.out --> cpu.in++;
        cpu.out --> disk.in++;
        disk.out --> sink.in++;
}