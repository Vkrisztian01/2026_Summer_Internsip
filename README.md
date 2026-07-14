# 2026_Summer_Internsip
I began organizing the work I have done in this repository. It contains the implementation, the benchmarking scripts, and the theoretical arguments, as well as the example dataset.

The core of the problem is finding a construction, this is done via introducing a set of constraints. The arguments are written in Reasoning.pdf
The construction is illustrated in illustration.jpg on paper, we can make a ton of examples like this more elegantly.

The inputs are sampled from A_NetworkSampler.py, which is a pseaudo uniform sampler. Making it completely uniform would be more costly but if it would mean an improvement we can use uniformly distributed graphs. (Actually, it would be an interesting use of Infrared)
The experience with the data shows that the construction satisfying alone is not that much faster than regular solvers, so optimization would be really relevant via the weighted case.
I used an example that you recommended, we can assign probabilities for the edges that represent our confidence that the edge exists. We optimize the solver to find the most confident construction(We assume independent distribution for the edges).
Using probabilities would require multiplying long franctions, so instead of that, we can use a logarithmic scale and just add the weights of the edges that we use in the construction. Since the probabilities will be between 0 and 1 the logarithm can be approximated with some negative number that we can scale up to
use as an integer. We can simply work with big negative numbers and addition and just look for a minimization.

I was able to benchmark the results for the core example using 300 inputs(Benchmark.py), and plotted them.
For the weighted case I ran into a technical problem, that I cant wrap my head around. That being said, it is a very natural extension of the problem so once we sort out the issue it will work nicely.

The code was ran on a windows 11 laptop with these paramters
Processor	Intel(R) Core(TM) i9-14900HX (2.20 GHz)
Installed RAM	32.0 GB (31.7 GB usable)
Device ID	29E5B649-6644-4975-92E5-5EF12464BFD0
Product ID	00330-53579-90468-AAOEM
System type	64-bit operating system, x64-based processor
Pen and touch	No pen or touch input is available for this display

