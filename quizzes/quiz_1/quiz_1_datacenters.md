# CSCE 489 - Cloud Computing - Autumn 2017
## Quiz 1, Datacenters

### Question 1: Cloud apps vs local apps
*Does it always make sense to run applications on the data center rather than locally in a client? Explain with an example.*

While many useful and popular programs today are cloud-based, it doesn't make sense for every program to be one.  For example, an simple calculator app on a mobile device doesn't need to ping the server for answers every time we add two numbers.  What happens when I want to add numbers when I'm on vacation in the Maldives without internet access?

From this, we can induce some general principles for choosing a local (client based) vs cloud based method to implement a program.

- First, what is the platform the program needs to run on?  If the platform is a space explorer, then everything needs to be local.  If the platform is a (mostly) connected mobile device, then cloud apps become more viable.  So one aspect is the connectivity.  The other aspect is computing power.  If our smartphones are powerful enough to do augmented reality (AR), then the app would probably perform better if we do most of the AR on the device rather than risking a bad experience over the internet. 

- Second, what features does the program need?  If the program connects many people or computers, then it already needs to use the internet.  So cloud based programs make more sense when there is some sort of interconnective part of the program.  Think social networks, like Facebook.  The other part is computing power.  If a problem can be (significantly) better solved with more computing power, cloud based apps make more sense.  Machine learning, or search are problems best solved with the cloud.

So if you have a limited connected, powerful computer, then most of the programs should be local.  If you have an always connected weak computer (a phone?), then most of the programs should be cloud based.

### Question 2: Datacenter locations
*Even though it is expensive to afford space in New York City, some companies want to keep their datacenters there. What advantages could they be trying to leverage?*

If people are building datacenters in NYC, even if its extremely expensive, there must be a financial incentive to do so.  With NYC, Wall Street and the financial sector are increasingly relying on computers to help and make investment decisions.  Specifically, there's a type of computer-only trading named *high frequency trading* (HTF), where computers use complex (stochastic calculus?) algorithm to rapidly make trades.  In this field, where the bettors are computers, having low latency is extremely important, since a server with the same algorithm will make a faster trade with a better connection.  Therefore, it makes sense to build HTF datacenters in NYC, even if its expensive.

More generally, there might be economic sense in building data centers in expensive places.  One is if you need the low latency, like with HTF.  Another is if you can leverage the networks already there.  For example, if your data center is state of the art and needs researchers, it might be easier to find great researchers in an expensive city.  That's the human network.  You can also leverage the existing internet network, too.  If the choice is to build infrastructure and a datacenter at a cheaper area, or with just a datacenter at a more expensive area, then it still might make more sense to build the datacenter in the more expensive area, because you don't have to pay for the internet infrastucture.

### Question 3: Single Points of Failure
*Are there single points of failures in a datacenter with a large number of machines? Explain your answer.*

It depends on how you configure your workflow.  And also on the scale of the 'single' point.

For example, lets say we have a 3 tired architecture for a workflow, and for the business logic tier, we use only use one server.  Then that server becomes a single point of failure, since if it dies, then our workflow dies.  Now lets use multiple servers that are on the same rack, so they share a switch.  Then that switch becomes a single point of failure, since if that switch dies, then our workflow dies.  The same can be applied to a cluster switch.  Scaling that up, even a single datacenter can be considered as a single point of failure.  If we use all the servers in a datacenter in Florida for our business logic, then when Hurrican Irma hits, our workflow dies.  Replicating the workflow in multiple datacenters will get around that.  It really depends on how reliable you want the workflow to be.  A whole datacenter fails a lot less then one server.

If we're working with just one datacenter, we want to distribute our workflow so no one hardware component will take it out.  (So something distruted in multiple clusters?)

### Question 4: Latency differences in single servers
*There are four servers A, B, C, and D in the same datacenter. Can there be a difference in the latency or throughput between them?*

Absolutely.  In the datacenter, there are individual serves which are lined up in a rack.  They share a single switch (a 48 input one in the textbook).  Then that switch feeds into the datacenter switch (a 300 input one?).  The key constraint for switches is that they don't allow maximum throughput.  If a single server gets a 1 Gb connection, and there are 40 connected servers, that doesn't mean the switch outputs 40Gb.  It's a concept known as the *oversubscription factor.*  According to the book, there's an oversubscription factor from 10 to 5 (10 - 20%), so from 4 to 8 Gb of real connection.  There's also the big switch, too.

There is also a increase in latency to use each switch.  The amount is usually small (on the order of 10s of microseconds) (fram stackexchange) per switch.  So that won't usually matter that much.

So if server A sits on a rack where all the other servers are using the rack switch, then A's throughput could be 1/10 or 1/5 of server B, which sits in a rack where none of the other servers are using bandwidth.  However, the latencies should be pretty similar with each other.

### Question 5: Datacenter upgrade times
*A developer wants to deploy a new software to manage a datacenter. He is planning to deploy it at 2am, when he suspects that there is very little load on the system, and any bug will have a small impact. Does his reasoning sound right to you? Why?*

Instead of suspecting, he should have enough infrastructure tools to check the least usage times.  For example, maybe for Netflix, their lowest usage times isn't 2am, but probably 6am (where most people are asleep).

### Question 6: Economies of Scale
*Indicate three reasons that enable economy of scale on data centers for cloud computing. In other words, how can the providers sell computing and storage power so cheap and still have a good profit margin?*

Buy in bulk:  Since datacenters have a lot of commodity hardware, we can buy them (cores, switches, DRAM, cords, racks) at a cheaper price.
Automation:  Traditional computers are run physically by humans (from buying them, moving them, turning them on, installing an OS, running programs).  Datacenters have software (OpenStack, Docker, etc) that manages the hardware, freeing up human time.
Homogenization: Datacenters can be built from simple, similar components so there is less overhead in management and automation.  Traditional computers come in many, many different configs.  Kind of like the Android vs iOS.  Android has to support so many hardware configs so it runs much slower than iOS (which is why Apple can get away with worse hardware specs).

### Question 7: 3 Tier Architecture
*What is the 3-tier architecture? Explain the functionality of each layer.*

The 3 tier architecture is a workflow, a way to structure an app that uses multiple servers (the cloud).

- Client tier:
  - The frontend.  The program that users access and download from.
- Business logic tier:  
  - The control layer.  Takes input from the client layer, does validation and logic, sends it to the data layer.  It also does the reverse (﻿﻿take data, shape it, and sends it to the client to display)
- Data tier: 
  - The database layer.  Handles the data, allowing for efficient, safe, and reliable access, retrieval, and insertion of data.  Think distributed databases.

NOTE: Really similar to the MVC framework (Rails, Laravel)

### Question 8: Homogenous servers
Is it necessary for all the servers in a datacenter to be similar to each other (i.e., homogeneous)? Are there any advantages of having similar servers? What are the disadvantages?

It's not absolutely necessary, but makes sense economically.
- The advantage of homogenous servers is that it's easier to maintain.  It's easier to write or use server management software, to set up the virtualization configurations, set up the flavors, etc.  On the hardware side, we would need less different types of ports and equipment.
- The disadvantage is the lack of flexibility.  For example, there is an increased demand for GPU datacenters to do data crunching (tensorflow).  A default datacenter with no GPU can't handle that.  Different types of processors are better suited for different work, etc.

### Question 9: Optimizing smartphones or data centers energy consumption
It's tougher for datacenters, because they have more dimensions to work with.  ﻿﻿﻿It's a more complex system.  A datacenter has to worry about location (wide range of economic, temperature, network effects), physical layout of a building, the server design (CPU, DRAM, etc) and has many more moving parts.  A phone really just has its core components (CPU, GPU, hardware peripherals).  They do share some similarities like in designing an efficient CPU.

### Question 10: Could I do it?
If large cloud providers such as Microsoft Azure or Amazon AWS were to merge, and they hire you to run the combined data centers, would you be able to achieve higher cost efficiency?

I would start by consolidating, or standardizing.  I would merge the software stacks, the hardware, etc to have a standard data center architecture.  Then I would start phasing AWS and Azure to use that set.  With a larger budget, I could probably buy or develop a set of custom datacenter hardware components at an economic price.  I would also reuse and design IaaS software (Openstack, AWS CLI) to automate the cloud as much as possible.  By doing so, I think eventually we'll be able to get a higher cost efficiency (operational).  (Basically following the 3 economies of scale)