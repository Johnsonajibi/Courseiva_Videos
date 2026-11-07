import sys; sys.path.insert(0, "tools")
from mk import *

save("virtualization", "NFV", "NFV", [
 H("box", [("A box for every job",  "Traditionally, every network job needed its own special box."),("A router box, a firewall box",  "A router box, a firewall box, a load balancer box.",OR),("NFV turns them into software","N F V turns them into software.",CY)]),
 S("From appliances to apps", "Think of swapping a drawer full of gadgets for apps on one phone.",
  [("box","Network functions run as software on ordinary servers.","VNF","Virtual network function"),
   ("server","The servers and hypervisor underneath are the N F V I.","NFVI","The hardware and virtualisation layer"),
   ("gear","M A N O is the manager that starts, stops and scales them.","MANO","Orchestration"),
   ("cloud","Virtual routers and firewalls are common examples.","Examples","Virtual router, firewall, load balancer")]),
 TR("Three tips.",
  [("NFV needs special hardware","Commodity servers are enough","Ordinary servers do the job."),
   ("NFV and SDN are the same","Different ideas, often paired","N F V virtualises functions, and S D N separates control."),
   ("MANO runs the traffic","It manages the functions","M A N O manages, it doesn't forward.")]),
 rc("NFV", [("N F V turns network boxes into software.","NFV: boxes become software"),("Three parts: N F V I, V N F and M A N O.","NFVI, VNFs, MANO"),("It runs on ordinary servers.","Runs on commodity servers")]),
])

save("network-documentation", "Network Documentation", "Documentation", [
 H("book", [("The engineer leaves",  "Your best engineer leaves the company."),("Everything is in their head",  "And everything about the network was in their head.",RED),("Documentation is the cure","Good documentation is the cure.",CY)]),
 S("Blueprints for engineers", "Networks need two kinds of drawings.",
  [("building","A physical diagram shows cables, ports and where things sit.","Physical diagram","Cables, ports, locations"),
   ("map","A logical diagram shows addresses, V L A Ns and routing.","Logical diagram","IPs, VLANs, routing"),
   ("clock","A baseline records what normal looks like.","Baseline","Taken in normal operation"),
   ("list","Every change needs a rollback plan written down.","Rollback plan","In every change record")]),
 TR("Three tips.",
  [("One diagram is enough","You need physical and logical","You need both kinds."),
   ("Document after problems","Keep it current always","Keep it up to date all the time."),
   ("Baselines can wait","Take one while healthy","Take a baseline while things are healthy.")]),
 rc("documentation", [("Keep a physical and a logical diagram.","Physical + logical diagrams"),("Take a baseline when things are healthy.","Baseline when healthy"),("Always write a rollback plan.","Always write a rollback plan")]),
])

save("change-management", "Change Management", "Change management", [
 H("clock", [("A quick fix on Friday",  "A quick fix on a Friday afternoon seems harmless."),("Then the network goes down",  "Then the whole network goes down.",RED),("Change management prevents that","Change management is there to prevent that.",CY)]),
 F("The five steps", "Every change follows the same path.",
  [("list","Someone raises a request for change.","1. RFC","Request"),
   ("people","Others review the risk.","2. Review","Impact and risk"),
   ("stamp","Someone approves it.","3. Approval","Sign-off"),
   ("gear","The change is carried out.","4. Implementation","With a rollback plan"),
   ("book","Afterwards, the result is reviewed.","5. PIR","Post-implementation review")]),
 V("Types of change", "Standard", "Normal", "Not every change takes the same route.",
  [("Approval","Pre-approved","Needs review","Standard changes are pre-approved."),
   ("Risk","Low and routine","Higher","Normal changes carry more risk."),
   ("Example","Add a user","Replace a core switch","Replacing a core switch is a normal change.")]),
 rc("change management", [("Five steps from request to review.","RFC, review, approval, implement, PIR"),("Every change needs a rollback plan.","Always a rollback plan"),("Standard changes are pre-approved.","Standard = pre-approved")]),
])

save("disaster-recovery", "Failover Testing", "Failover testing", [
 H("bell", [("A fire drill",  "A fire drill tests that people can leave the building."),("Your network needs one",  "Your network needs the same kind of test.",CY),("Does the backup really work?","Does the backup really take over?",OR)]),
 S("Fire drill for your network", "Backups are only useful if they actually work.",
  [("router","Pull the plug on the main router and watch what happens.","Failover test","Simulate a failure"),
   ("clock","H S R P says hello every three seconds, with a ten second hold.","HSRP: 3 s / 10 s","Default timers"),
   ("scale","V R R P advertises every second, with about three seconds before takeover.","VRRP: 1 s / ~3 s","Default timers"),
   ("book","Write down how long it took, and compare with your target.","Measure convergence","Under a second is the goal for FHRPs")]),
 TR("Three tips.",
  [("Redundancy works without testing","Test it","Untested redundancy is a guess."),
   ("Test in business hours","Schedule it","Schedule tests as changes."),
   ("One test is enough","Repeat after changes","Retest after any change.")]),
 rc("failover testing", [("Test your backups before you need them.","Test backups early"),("Know the default timers.","Know default timers"),("Write down how long failover takes.","Record failover time")]),
])

save("high-availability", "Network Redundancy", "High availability", [
 H("shield", [("A spare tyre",  "Every car needs a spare tyre."),("Networks need spares too",  "A network needs spares as well.",CY),("That's redundancy","That's called redundancy.",OR)]),
 S("The spare tyre", "Each layer has its own way of being redundant.",
  [("switch","Spanning tree stops loops, with a hello of two seconds.","STP","Hello 2, max age 20, forward 15"),
   ("clock","Rapid S T P recovers in one to three seconds.","RSTP","Proposal and agreement"),
   ("router","H S R P gives hosts a gateway that survives failure.","HSRP","3 s hello, 10 s hold"),
   ("link","Ether channel bundles links, so one failing doesn't matter.","EtherChannel","Bundled links")]),
 TR("Three traps.",
  [("Redundancy means no downtime","It reduces it","It reduces downtime, not removes it."),
   ("STP is fast","Classic STP is slow","Classic S T P is slow to recover."),
   ("One link is enough","Add a backup","A single link is a single point of failure.")]),
 rc("redundancy", [("Add a spare at every layer.","A spare at every layer"),("R S T P is much faster than S T P.","RSTP faster than STP"),("Test the backups.","Test the backups")]),
])

save("capacity-planning", "Capacity Planning", "Capacity planning", [
 H("road", [("The road gets busier",  "Every year, more cars use the road."),("Add lanes before it jams",  "A sensible council adds lanes before it jams.",CY),("That's capacity planning","That's capacity planning.",OR)]),
 S("The highway system", "Capacity planning follows a simple loop.",
  [("scale","Measure how busy your links are today.","Measure","SNMP history"),
   ("bell","Set limits, seventy percent as a warning and ninety as critical.","Thresholds","70% / 90%"),
   ("map","Forecast how much growth is coming.","Forecast","Trend lines"),
   ("wrench","Upgrade before the link saturates.","Upgrade early","Before the jam")]),
 TR("Three tips.",
  [("Wait until it's full","Plan before saturation","Plan ahead of saturation."),
   ("Only peak counts","Trends count too","Look at the trend as well."),
   ("SNMP shows who's talking","NetFlow does","Use NetFlow to see who's talking.")]),
 rc("capacity planning", [("Measure, set thresholds, forecast, upgrade.","Measure, threshold, forecast, upgrade"),("Seventy is a warning, and ninety is critical.","70% warn; 90% critical"),("Use S N M P for history, and NetFlow for who.","SNMP: history. NetFlow: who")]),
])

save("exam-strategy", "CCNA Exam Traps", "Exam strategy", [
 H("question", [("The exam is full of traps",  "The CCNA exam is full of traps."),("Most are the same numbers",  "Most come down to numbers you should know cold.",OR),("Let's learn them","Let's learn the key ones.",CY)]),
 T("Numbers to know cold", "Learn these defaults.",
  [("OSPF dead   40 s","Four times the 10 s hello","O S P F dead time is forty seconds."),
   ("EIGRP hold   15 s","Three times the 5 s hello","E I G R P hold is fifteen seconds."),
   ("STP   2 / 20 / 15","Hello, max age, forward delay","S T P uses two, twenty and fifteen."),
   ("MAC aging   300 s","Five minutes","M A C entries age out after three hundred seconds.",CY)]),
 S("The airport checkpoint", "A few habits pay off on exam day.",
  [("question","Read the whole question, because the trap is often in the last line.","Read it all","Spot the trap"),
   ("list","Eliminate the answers that are clearly wrong first.","Eliminate","Narrow it down"),
   ("clock","Don't spend too long on any one question.","Watch the clock","Flag and move on"),
   ("book","Learn the defaults, since many questions are just defaults.","Know the defaults","Numbers matter")]),
 rc("the exam", [("Learn the default timers.","Learn default timers"),("Read the whole question.","Read the whole question"),("Eliminate, then guess.","Eliminate, then guess")]),
])

save("aws-vpc-basics", "AWS VPC Basics", "AWS VPC", [
 H("building", [("A condo in a big city",  "Imagine owning a private condo in a huge city."),("Yours alone",  "Nobody else can walk in.",CY),("That's a VPC","That's an A W S V P C.",OR)]),
 S("The big city condo", "A V P C has a few building blocks.",
  [("building","A V P C is your private network inside one region.","VPC","One region"),
   ("lock","Plan the address range carefully, because the C I D R can't be changed.","CIDR block","Plan it first"),
   ("door","Each subnet lives in exactly one availability zone.","Subnet","One AZ"),
   ("road","A subnet is public only if its route table points at an internet gateway.","Public subnet","Route to the IGW")]),
 TR("Three traps.",
  [("A VPC spans regions","One region only","A V P C lives in one region."),
   ("A subnet spans zones","One AZ only","A subnet lives in one zone."),
   ("Any subnet is public by default","Needs an IGW route","It needs a route to an internet gateway.")]),
 rc("AWS VPC", [("A V P C is a private network in one region.","VPC: private network, one region"),("A subnet lives in one zone.","Subnet: one AZ"),("Public means a route to an internet gateway.","Public = IGW route")]),
])

save("aws-private-connectivity", "VPC Endpoints", "VPC endpoints", [
 H("envelope", [("Reaching S3",  "Your server needs to reach S three."),("Through the internet?",  "Does that traffic really have to go over the internet?",OR),("No, use an endpoint","No, a V P C endpoint keeps it private.",CY)]),
 S("The private mailroom", "There are two kinds of endpoint.",
  [("box","Gateway endpoints are free, and only work for S three and Dynamo D B.","Gateway endpoint","S3 and DynamoDB, free"),
   ("link","They work through your route table.","Route table entry","No ENI"),
   ("shield","Interface endpoints use PrivateLink, and cover most other services.","Interface endpoint","PrivateLink"),
   ("clock","They cost an hourly fee, plus data charges.","Paid","Hourly + per GB")]),
 TR("Three traps.",
  [("Gateway endpoints cover every service","S3 and DynamoDB only","Only S three and Dynamo D B."),
   ("Interface endpoints are free","They cost money","They have an hourly cost."),
   ("Both use route tables","Only gateway endpoints","Only gateway endpoints use route tables.")]),
 rc("VPC endpoints", [("Gateway endpoints: free, S three and Dynamo D B.","Gateway: free; S3, DynamoDB"),("Interface endpoints use PrivateLink.","Interface: PrivateLink"),("Both keep traffic off the internet.","Both avoid the internet")]),
])

save("aws-transit-gateway", "Transit Gateway", "Transit Gateway", [
 H("link", [("Twenty VPCs",  "You have twenty V P Cs."),("A tunnel between each pair",  "Peering every pair means a tangle of connections.",RED),("Transit Gateway is the hub","A Transit Gateway is the hub that replaces the tangle.",CY)]),
 S("The train network", "Think of a central station that every line passes through.",
  [("building","Transit Gateway is a regional hub in a star shape.","Hub and spoke","Regional"),
   ("link","Each V P C and each site attaches once to the hub.","Attachments","One per network"),
   ("list","The gateway has its own route tables, separate from the V P C ones.","TGW route tables","Independent"),
   ("map","Different tables let you keep some networks isolated.","Segmentation","Associations and propagation")]),
 TR("Three traps.",
  [("TGW uses VPC route tables","It has its own","It has its own route tables."),
   ("Peering is transitive","Peering isn't; TGW is","Peering isn't transitive."),
   ("It spans regions on its own","Regional; needs peering","It's regional, so you peer gateways across regions.")]),
 rc("Transit Gateway", [("It's a hub that replaces many peerings.","A hub replacing many peerings"),("It has its own route tables.","Own route tables"),("It's regional.","Regional")]),
])

save("aws-hybrid", "AWS Hybrid Connectivity", "AWS hybrid", [
 H("building", [("Your office and the cloud",  "Your office needs a link to the cloud."),("Three delivery services",  "There are different delivery services to choose from.",CY),("Pick the right one","Picking the right one depends on speed, cost and time.",OR)]),
 S("Three delivery services", "Each option suits a different need.",
  [("lock","A Site to Site V P N is encrypted, over the public internet.","Site-to-Site VPN","Quickest, cheapest"),
   ("road","Direct Connect is a private dedicated cable to the cloud.","Direct Connect","Dedicated, consistent"),
   ("clock","Direct Connect takes weeks to set up, but is steadier.","Longer setup","Consistent performance"),
   ("shield","Many firms run a V P N as a backup for Direct Connect.","VPN as backup","Common design")]),
 TR("Three traps.",
  [("VPN is the most consistent","Direct Connect is","Direct Connect is more consistent."),
   ("Direct Connect is encrypted by default","It isn't","It isn't encrypted by default."),
   ("Direct Connect is quick to order","It takes time","It can take weeks.")]),
 rc("AWS hybrid", [("V P N is quick and cheap.","VPN: quick, cheap"),("Direct Connect is dedicated and steady.","Direct Connect: dedicated"),("Use a V P N as backup.","VPN as backup")]),
])

save("aws-dns-cdn", "Route 53 and CloudFront", "Route 53 and CloudFront", [
 H("book", [("A phone directory",  "Route fifty three is a phone directory for your sites."),("CloudFront is the local branch",  "CloudFront keeps copies near your visitors.",CY),("Together they're quick","Together, they make sites fast.",OR)]),
 S("The library directory", "Two services, two jobs.",
  [("book","Route fifty three turns names into addresses.","Route 53","DNS"),
   ("link","An alias record is the only way to point a root domain at an A W S resource.","Alias record","Zone apex"),
   ("cloud","CloudFront caches copies at edge locations.","CloudFront","CDN"),
   ("clock","It's pull based, so the first visitor fetches the file.","Pull-based cache","Cached after first request")]),
 TR("Three traps.",
  [("CNAME works at the root","Use an alias","You can't use a C N A M E at the root."),
   ("CloudFront pre-loads everything","Pull-based","It caches after the first request."),
   ("Route 53 is only DNS","Also health checks","It also does health checks.")]),
 rc("Route 53 and CloudFront", [("Use an alias for the root domain.","Alias for the root domain"),("CloudFront caches at the edge.","CloudFront caches at the edge"),("It fills the cache on first request.","Cache fills on first request")]),
])

save("aws-network-security", "AWS Network Security", "AWS network security", [
 H("shield", [("An embassy checkpoint",  "An embassy has several security checkpoints."),("Each one checks something different",  "Each one checks something different.",CY),("AWS works the same way","A W S layers its security in the same way.",OR)]),
 V("Security groups vs NACLs", "Security group", "Network ACL", "These two get mixed up all the time.",
  [("Level","On the instance","On the subnet","Security groups guard the instance, and network A C Ls guard the subnet."),
   ("State","Stateful","Stateless","Security groups are stateful, and network A C Ls are stateless."),
   ("Rules","Allow only","Allow and deny","Security groups only allow, but network A C Ls can also deny.")]),
 S("Higher up", "Other tools go further.",
  [("shield","W A F inspects web requests, at layer seven.","AWS WAF","Blocks SQL injection, XSS"),
   ("bell","It can also rate limit noisy addresses.","Rate limiting","Per IP"),
   ("lock","Shield helps against flood attacks.","AWS Shield","DDoS protection")]),
 rc("AWS security", [("Security groups are stateful and allow only.","SG: stateful, allow only"),("Network A C Ls are stateless, with allow and deny.","NACL: stateless, allow and deny"),("W A F protects at layer seven.","WAF: layer 7")]),
])

save("aws-network-ops", "AWS Network High Availability", "AWS network ops", [
 H("building", [("A hot dog cart",  "Picture a hot dog cart with one stand."),("If it's closed, no sales",  "If that stand is shut, there are no sales.",RED),("Run more than one","Run several, in different places.",CY)]),
 S("The hot dog carts", "A few ideas keep services running.",
  [("building","One availability zone is a single point of failure.","Single AZ","Risky"),
   ("people","So spread across at least two zones.","Multi-AZ","Survives a data centre outage"),
   ("router","A load balancer shares traffic between healthy targets.","Load balancer","Healthy targets only"),
   ("box","It doesn't cache or change the data.","Not a cache","Just distributes")]),
 TR("Three traps.",
  [("One AZ is fine","Use two or more","Use at least two."),
   ("A load balancer caches","It only distributes","It doesn't cache."),
   ("It sends to every target","Only healthy ones","It only uses healthy targets.")]),
 rc("AWS high availability", [("Use at least two zones.","Use 2+ AZs"),("A load balancer spreads traffic.","Load balancer spreads traffic"),("It skips unhealthy targets.","Skips unhealthy targets")]),
])

save("gcp-vpc", "GCP VPC Basics", "GCP VPC", [
 H("building", [("A university campus",  "Think of a university campus."),("One campus, many buildings",  "One campus, many buildings, in different cities.",CY),("That's a GCP VPC","That's a Google Cloud V P C.",OR)]),
 S("The campus", "Google's V P C works differently from Amazon's.",
  [("map","A V P C is global, and can span regions.","Global VPC","Spans regions"),
   ("building","Subnets are regional, and cover every zone in the region.","Regional subnets","All zones"),
   ("shield","Firewall rules are stateful.","Stateful firewall","VPC level"),
   ("lock","Rules match tags or service accounts, not just addresses.","Targets","Tags and service accounts")]),
 TR("Three traps.",
  [("A VPC is regional","It's global","It's global in Google Cloud."),
   ("A subnet is zonal","Regional","Subnets are regional."),
   ("Rules are stateless","They're stateful","The firewall is stateful.")]),
 rc("GCP VPC", [("A V P C is global.","VPC: global"),("Subnets are regional.","Subnets: regional"),("Firewall rules are stateful.","Firewall: stateful")]),
])

save("gcp-vpc-sharing", "VPC Peering and Shared VPC", "VPC peering", [
 H("link", [("Two networks",  "You have two separate networks."),("They need to talk",  "They need to talk privately.",CY),("Two ways to do it","There are two ways to do it.",OR)]),
 S("Apartments and a shared driveway", "Peering and sharing solve different problems.",
  [("link","Peering joins two V P Cs directly and privately.","VPC peering","Direct, private"),
   ("lock","It isn't transitive, so A to B and B to C doesn't give A to C.","Not transitive","Needs its own peering"),
   ("building","Shared V P C puts network control in one host project.","Shared VPC","Central network"),
   ("people","Other projects, the service projects, use it.","Service projects","Use the shared network")]),
 TR("Three traps.",
  [("Peering is transitive","It isn't","Peering isn't transitive."),
   ("Shared VPC joins different orgs","Same organisation","It's within one organisation."),
   ("Peering needs a gateway","Direct","Peering is direct.")]),
 rc("peering and Shared VPC", [("Peering is direct but not transitive.","Peering: direct, not transitive"),("Shared V P C centralises control.","Shared VPC: central control"),("Service projects use the host's network.","Service projects share it")]),
])

save("gcp-hybrid", "Cloud VPN and Interconnect", "GCP hybrid", [
 H("building", [("Two cities, one factory",  "Your factory has sites in two cities."),("A road between them",  "They need a road between them.",CY),("Two kinds of road","There are two kinds of road.",OR)]),
 S("The two city factory", "Google offers a cheap road and a fast road.",
  [("lock","Cloud V P N is encrypted, over the public internet.","Cloud VPN","Lower bandwidth, backup"),
   ("road","Cloud Interconnect is a private dedicated connection.","Cloud Interconnect","Bypasses the internet"),
   ("scale","Choose Interconnect for high performance.","High-performance","Dedicated"),
   ("shield","Many firms use V P N as a backup.","VPN as backup","Common design")]),
 TR("Three traps.",
  [("VPN is the faster one","Interconnect","Interconnect is faster."),
   ("Interconnect uses the internet","It bypasses it","It bypasses the internet."),
   ("They can't be combined","Often used together","They're often combined.")]),
 rc("GCP hybrid", [("V P N is encrypted over the internet.","VPN: encrypted, over internet"),("Interconnect is private and fast.","Interconnect: private, fast"),("Use both for resilience.","Use both for resilience")]),
])

save("gcp-load-balancing-cdn", "GCP Load Balancing", "GCP load balancing", [
 H("people", [("A food truck festival",  "Imagine a food truck festival with a long queue."),("Spread the people out",  "You'd send people to the shortest line.",CY),("That's load balancing","That's what a load balancer does.",OR)]),
 S("The food truck festival", "Load balancers come at two layers.",
  [("list","Layer four balancers decide using addresses and ports.","Layer 4","IP and port"),
   ("map","Layer seven balancers look at the content of the request.","Layer 7","URLs and headers"),
   ("server","Both spread traffic across several backends.","Backends","No single server overwhelmed"),
   ("cloud","A C D N caches content near the visitor.","CDN","Edge caching")]),
 TR("Three traps.",
  [("Layer 4 reads URLs","Layer 7 does","Only layer seven reads the content."),
   ("A balancer stores your data","It just distributes","It only distributes traffic."),
   ("CDN is the same as a balancer","Different jobs","They do different jobs.")]),
 rc("GCP load balancing", [("Layer four uses addresses and ports.","L4: IP and port"),("Layer seven reads the request.","L7: reads the content"),("A C D N caches near users.","CDN caches near users")]),
])

save("gcp-nat-router", "Cloud NAT", "Cloud NAT", [
 H("lock", [("Private servers",  "Your servers have no public addresses."),("They still need updates",  "But they still need to download updates.",OR),("Cloud NAT lets them out","Cloud N A T lets them out, safely.",CY)]),
 S("The mailroom underground", "Cloud NAT is a one way door.",
  [("door","It gives private V Ms outbound internet access.","Outbound only","No public IP on the VM"),
   ("shield","Nothing from the internet can start a connection in.","No inbound","Safer"),
   ("cloud","Private Google Access reaches Google's own services privately.","Private Google Access","Stays on Google's network"),
   ("lock","So private V Ms can still use Google A P Is.","Google APIs","Without public IPs")]),
 TR("Three traps.",
  [("Cloud NAT allows inbound","Outbound only","It's outbound only."),
   ("VMs need public IPs","They don't","They don't need public addresses."),
   ("Private Google Access uses the internet","Internal network","It uses Google's internal network.")]),
 rc("Cloud NAT", [("Cloud N A T gives outbound access only.","Outbound only"),("V Ms keep no public address.","No public IPs"),("Private Google Access reaches Google A P Is.","Private Google Access = Google APIs")]),
])

save("gcp-ha-security", "GCP High Availability", "GCP HA", [
 H("shield", [("A hospital",  "A hospital has a backup generator."),("And a second hospital",  "And a second hospital in another city.",CY),("That's HA and DR","That's high availability and disaster recovery.",OR)]),
 S("Generator and second hospital", "Two ideas protect services at different scales.",
  [("building","High availability spreads across zones in one region.","High availability","Multiple zones"),
   ("map","Disaster recovery spreads across regions.","Disaster recovery","Multiple regions"),
   ("router","Load balancing sends traffic only to healthy backends.","Health checks","Skip failed backends"),
   ("shield","Together they survive both small and big failures.","Layered protection","Zone and region")]),
 TR("Three traps.",
  [("HA covers a region outage","Needs multiple regions","That's disaster recovery."),
   ("One zone is enough","Use several","Use more than one zone."),
   ("DR and HA are the same","Different scale","They protect against different things.")]),
 rc("GCP HA", [("Zones give high availability.","Zones = HA"),("Regions give disaster recovery.","Regions = DR"),("Health checks skip failed backends.","Health checks skip failures")]),
])

save("cloud-networking-concepts", "Cloud Networking Concepts", "Cloud networking", [
 H("cloud", [("A shared office building",  "Think of the cloud as a shared office building."),("Your floor is private",  "Your floor is private, though the building is shared.",CY),("That's how cloud networking works","That's how cloud networking works.",OR)]),
 S("The shared building", "A few models and terms organise the cloud.",
  [("cloud","Public, private, hybrid and community are the four deployment models.","Deployment models","Public, private, hybrid, community"),
   ("list","I a a S, P a a S and S a a S are the three service models.","Service models","IaaS, PaaS, SaaS"),
   ("scale","You control less as you move from I a a S to S a a S.","Control decreases","IaaS > PaaS > SaaS"),
   ("building","A V P C is your isolated network inside the cloud.","VPC / VNet","Logically isolated")]),
 TR("Three traps.",
  [("SaaS gives most control","IaaS does","I a a S gives most control."),
   ("Hybrid means two clouds","Cloud plus on-premises","Hybrid mixes cloud with on premises."),
   ("A VPC is physical","It's logical","It's a logical network.")]),
 rc("cloud networking", [("Four deployment models, three service models.","4 deployment, 3 service models"),("Control falls from I a a S to S a a S.","Control: IaaS > PaaS > SaaS"),("A V P C is a private logical network.","VPC = private logical network")]),
])

save("cloud-networking-ops", "Cloud Networking Operations", "Cloud ops", [
 H("road", [("A city transit system",  "Cloud networking is like a city transit system."),("Stops, lines and tickets",  "It has stops, lines and ticket checks.",CY),("Let's learn the rules","Let's learn the key rules.",OR)]),
 S("The transit system", "Four rules cause most problems.",
  [("map","Address ranges must never overlap between connected networks.","No overlapping CIDRs","With VPCs or on-prem"),
   ("shield","Security groups are stateful.","Security groups","Stateful"),
   ("lock","Network A C Ls are stateless.","Network ACLs","Stateless"),
   ("door","A N A T gateway lets private subnets out, but nothing in.","NAT gateway","Outbound only")]),
 TR("Three traps.",
  [("Overlapping ranges are fine","They break routing","Overlaps break routing."),
   ("NAT gateways allow inbound","Outbound only","They only allow outbound."),
   ("Both firewalls are stateful","SG yes, NACL no","Only security groups are stateful.")]),
 rc("cloud operations", [("Never overlap address ranges.","No overlapping CIDRs"),("Security groups are stateful, and N A C Ls are stateless.","SG stateful; NACL stateless"),("N A T gateways are outbound only.","NAT gateway: outbound only")]),
])
