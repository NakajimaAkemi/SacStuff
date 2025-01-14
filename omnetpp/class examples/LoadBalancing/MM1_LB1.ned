import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Sink;
import org.omnetpp.queueing.Source;
import org.omnetpp.queueing.Router;

network MM1_LB1
{
	parameters:
		double mu1=default(5);
		double mu2=default(5);
		double lambda1 = default(4.5);
		double lambda2 = default(2);
		src1.interArrivalTime = exponential(1s/lambda1);
		src2.interArrivalTime = exponential(1s/lambda2);
		srv1.serviceTime = 1s * exponential(1/mu1);
		srv2.serviceTime = 1s * exponential(1/mu2);
	submodules:
		src1: Source;
		src2: Source;
		// disable router by commenting out this line
		r: Router;
		srv1: Queue;
		srv2: Queue;
		sink1: Sink;
		sink2: Sink;
	connections:
		// to disable router:
		// src1.out --> srv1.in++
		src1.out --> r.in++;
		r.out++ --> srv1.in++;
		// to disable router:
		// src2.out --> srv2.in++
		src2.out --> r.in++;
		r.out++ --> srv2.in++;
		srv1.out --> sink1.in++;
		srv2.out --> sink2.in++;
}

