import sys; sys.path.insert(0, "tools")
from mk import *

save("dns", "DNS", "DNS", [
 hook("book", [("You type a name",0),("Computers need a number",1,OR),("DNS is the phone book",2,CY)],
  "You type a website name. But computers only talk in numbers. D N S is the phone book that connects the two."),
 story("The phone book and the operator", "Say you want to call Alice, but you only know her name. You look her up in a phone book and find her number. D N S does exactly that for websites. Your computer asks a helper called the resolver, and the resolver does the legwork. It asks the root servers, then the top level domain servers, then the one that really knows. Finally it hands the number back, and remembers it for a while.",
  [("book","Name to number","Domain name to IP address",1),("person","Your computer asks a helper","Recursive resolver",2),("tree","Root, then TLD, then the expert","Authoritative server",3),("clock","Remembered for a while","Cached for the TTL",4)]),
 term("Setting it up on a router", "On a Cisco router, two commands turn D N S on. One enables lookups. The other tells the router which server to ask.",
  [("ip domain-lookup","Allow name lookups",1),("ip name-server 8.8.8.8","Which server to ask",2,CY)]),
 traps("Three mix-ups. Your computer does not ask the root server directly. It asks its resolver. D N S is not U D P only, because big answers and zone transfers use T C P. And the T T L is set by the authoritative server, not by the resolver.",
  [("The client asks the root server directly","It asks its resolver, which does the walking",1),("DNS only uses UDP","Large replies and zone transfers use TCP",2),("The resolver sets the TTL","The authoritative server sets it",3)]),
 rc("DNS", [("D N S turns names into I P addresses.","DNS turns names into IP addresses"),("Resolvers do the hard work, and cache the answers.","Resolvers do the work and cache answers"),("It uses port fifty-three, mostly U D P.","Port 53, mostly UDP")]),
])

save("static-routing", "Static Routing", "Static routing", [
 hook("map", [("Who tells the router where to go?",0),("You do",1,CY),("By writing it down",2)],
  "Who tells a router where to send traffic? Sometimes, you do. By simply writing it down."),
 story("The note in the mailroom", "Picture an office mailroom. The building manager writes a note. All packages for Accounting go to floor three. That note is a static route. It stays put until the manager changes it. If Accounting moves, the note is wrong, and packages go missing. The mailroom clerk never learns, they just follow the note.",
  [("book","The note","Static route",1),("clock","Stays until changed","Never updates itself",3),("question","Accounting moves","Traffic is lost",4),("person","The clerk never learns","No adapting to changes",5)]),
 term("Writing a static route", "The command is I P route, then the network, then the mask, then where to send it. A route to zero zero zero zero is the default route. And add a bigger number on the end, and you get a backup, called a floating static route.",
  [("ip route 192.168.1.0 255.255.255.0 10.0.0.1","Network, mask, next hop",0),("ip route 0.0.0.0 0.0.0.0 10.0.0.1","Default route: send everything here",1),("ip route 192.168.1.0 255.255.255.0 10.0.0.1 120","Floating backup (higher AD)",2,CY)]),
 traps("Three common slip-ups. Static routes do not update themselves when a link fails. The default distance is one, but you can change it. And the mask must be written in dotted form, not as a slash.",
  [("Static routes update when a link fails","They never adapt on their own",1),("AD is always 1","Default is 1, but you can set it",2),("You can write /24 in ip route","Use a dotted mask: 255.255.255.0",3)]),
 rc("static routing", [("A static route is a note you write by hand.","A static route is a hand-written note"),("A default route sends everything unknown one way.","Default route = 0.0.0.0 0.0.0.0"),("And a higher distance turns it into a backup.","Higher AD = floating backup")]),
])

save("admin-distance", "Administrative Distance", "Admin distance", [
 hook("scale", [("Two sources, two answers",0),("Who do you believe?",1,OR),("Trust ratings decide",2,CY)],
  "Two routing sources give you two different answers for the same place. Who does the router believe? The one with the best trust rating."),
 story("The trusted messenger", "Imagine a boss getting reports from three people. A veteran vice president, a decent senior manager, and a brand new intern. When their reports disagree, the boss goes with the most trusted source. In networking, that trust score is called administrative distance. Lower means more trusted. And it's checked before the metric ever is.",
  [("person","The veteran VP","Connected = 0, Static = 1",1),("people","The senior manager","OSPF = 110",2),("question","The new intern","RIP = 120",3),("scale","Trust is checked first","Lowest AD wins",4)]),
 term("Distances to know", "Here are the numbers worth learning. Connected is zero. Static is one. Internal E I G R P is ninety. O S P F is one ten. R I P is one twenty. And external E I G R P is one seventy.",
  [("Connected   0","Most trusted",1),("Static   1","Your own note",2),("EIGRP internal   90","",3),("OSPF   110","",4),("RIP   120","",5),("EIGRP external   170","Least trusted of these",6,OR)]),
 traps("Three mix-ups. A lower metric does not beat a lower distance across protocols. Static routes can have a different distance if you set one. And external E I G R P is less trusted than O S P F.",
  [("Lowest metric always wins","AD is compared first, then metric",1),("Static AD can't be changed","Set any value 1 to 255",2),("EIGRP external = internal","External is 170, internal is 90",3)]),
 rc("administrative distance", [("Administrative distance is how much the router trusts a source.","AD = how much a source is trusted"),("Lower is better, and it beats the metric.","Lower wins, before the metric"),("Learn the big ones: zero, one, ninety, one ten, one twenty.","0, 1, 90, 110, 120")]),
])

save("ospf-basics", "OSPF Basics", "OSPF basics", [
 hook("map", [("Every router draws the same map",0),("Then finds the shortest way",1,CY),("That's OSPF",2)]  ,
  "Imagine every router drawing the exact same map of the network. Then each one works out the shortest way across it. That's O S P F."),
 story("The postal planners", "Think of a national postal service with a team of planners. Each planner tells everyone which cities they connect to, and how far each road is. That message is a link state advertisement. Everyone collects all the messages and builds the same complete map. Then each planner works out the cheapest path for themselves. The cost is based on how fast the road is.",
  [("envelope","Each planner shares roads","LSA",1),("map","Everyone builds the same map","Link-state database",2),("ruler","Each finds the cheapest path","SPF calculation",3),("scale","Faster road, lower cost","Cost = 100 Mbps / bandwidth",4)]),
 term("Turning it on", "Three things to remember. Start the process. Tell it which interfaces to use, with a wildcard mask. And check your neighbours. Hello packets go out every ten seconds.",
  [("router ospf 1","Start OSPF",1),("network 192.168.1.0 0.0.0.255 area 0","Wildcard mask, not subnet mask",2),("show ip ospf neighbor","Check your neighbours",3,CY)]),
 traps("Three slip-ups. O S P F uses cost, not hop count. The network command takes a wildcard mask. And two way is perfectly normal between routers that are not the D R or B D R.",
  [("OSPF counts hops like RIP","It uses cost, based on bandwidth",1),("network uses a subnet mask","It uses a wildcard mask",2),("2-Way means a problem","Normal between non-DR routers",3)]),
 rc("OSPF", [("O S P F shares a full map, and every router finds its own best path.","Shared map, each router picks its path"),("Cost is based on bandwidth, not hops.","Cost comes from bandwidth"),("And the network command uses wildcard masks.","network uses wildcard masks")]),
])

save("ospf-neighbors", "OSPF Neighbors", "OSPF neighbors", [
 hook("people", [("Two routers meet",0),("They only become neighbours",1,OR),("If the details match",2,CY)],
  "Two O S P F routers meet on a link. They don't automatically become neighbours. That only happens if a few details match."),
 story("The neighbourhood watch", "Picture a gated community where every house waves a flag every ten seconds. The flag shows the house name, the street, and a secret handshake code. If a house stops waving for forty seconds, the others assume it's empty and cross it off. Those waves are hello packets, and forty seconds is the dead interval. For two houses to become neighbours, their street, handshake and timers must all match.",
  [("clock","Wave every 10 seconds","Hello interval",1),("bell","Silent for 40 seconds","Dead interval",2),("key","Secret handshake","Authentication",3),("map","Same street","Area ID must match",4)]),
 versus("What must match", "Must match", "Does not need to match", "Here's the checklist. Area, subnet, timers, authentication and stub flags must all match. The process I D and the router I D do not need to match at all.",
  [("Area and subnet","Yes","",0),("Hello and Dead timers","Yes","",1),("Process ID","","Local only",2)]),
 traps("Three things catch people out. Process I Ds are local, and can differ. O S P F does not negotiate timers, so a mismatch means no neighbour. And the router I D does not need to be on the link's subnet.",
  [("Process IDs must match","They are only locally significant",1),("Mismatched timers get negotiated","No: they just won't form a neighbour",2),("Router ID must be an interface on the link","It can be any 32-bit ID",3)]),
 rc("OSPF neighbor", [("Routers wave hello every ten seconds.","Hello: every 10 seconds"),("Area, timers and authentication must match.","Area, timers, authentication must match"),("And show I P O S P F neighbor is your first check.","show ip ospf neighbor")]),
])

save("eigrp-concepts", "EIGRP Concepts", "EIGRP concepts", [
 hook("map", [("A GPS with a backup route",0),("Ready before the road closes",1,CY),("That's EIGRP",2)],
  "Think of a G P S that already has a backup route ready. It's ready before your road even closes. That's E I G R P."),
 story("GPS with alternate routes", "Your G P S knows the main route, and keeps a few safe alternates in reserve. The main route is called the successor. A safe alternate is a feasible successor. It's only safe if it's guaranteed not to loop back through you. If the main road closes, the G P S switches instantly, without recalculating.",
  [("map","The main route","Successor",1),("road","A safe alternate","Feasible successor",2),("shield","Guaranteed no loop","Reported distance < feasible distance",3),("clock","Switches instantly","Fast convergence (DUAL)",4)]),
 term("What to check", "Three show commands cover E I G R P. Neighbours. The topology table. And the routes it installs.",
  [("show ip eigrp neighbors","Who we've met",1),("show ip eigrp topology","Successors and backups",2),("show ip route eigrp","Routes installed",3,CY)]),
 traps("Three mix-ups. E I G R P is not link state, it's advanced distance vector. It doesn't use T C P or U D P, it has its own transport. And the successor is the lowest total metric, not the lowest reported distance.",
  [("EIGRP is link-state","Advanced distance vector",1),("EIGRP uses TCP or UDP","Its own RTP over IP protocol 88",2),("Successor = lowest reported distance","Lowest total (feasible) distance",3)]),
 rc("EIGRP", [("E I G R P keeps a main route and safe backups.","A main route plus safe backups"),("A backup is safe if its reported distance beats your feasible distance.","Backup rule: RD < FD"),("Internal routes have distance ninety.","Internal AD = 90")]),
])

save("acl-standard-named", "Standard ACLs", "Standard ACLs", [
 hook("shield", [("A bouncer at the door",0),("Checks one thing only",1,OR),("Where you came from",2,CY)],
  "Picture a bouncer at a club door. This one checks only one thing. Where you came from."),
 story("The guest list", "The bouncer holds a clipboard, and that's the access list. Each line says allow or deny. Every person is checked from the top, and the first match wins. If you're not on the list at all, you're turned away. That's the implicit deny at the end. A standard list checks only the source address.",
  [("list","The clipboard","ACL",1),("door","Checked top to bottom","First match wins",2),("lock","Not on the list: out","Implicit deny",3),("person","Only checks who you are","Source IP only",4)]),
 term("Writing one", "Here's a named standard list. Permit one network. Then apply it to an interface, with a direction. Standard lists go close to the destination.",
  [("ip access-list standard GUESTS","Create and name it",1),("permit 192.168.1.0 0.0.0.255","Wildcard mask",2),("ip access-group GUESTS out","Apply with a direction",3,CY)]),
 traps("Three slip-ups. Standard lists cannot look at destinations or ports. A wildcard of all zeros matches one exact host, not everything. And lists don't work until you apply them with a direction.",
  [("Standard ACLs filter by destination","Source IP only",1),("Wildcard 0.0.0.0 matches any","It matches one exact host",2),("ACLs apply inbound by default","Apply them yourself; pick in or out",3)]),
 rc("standard ACL", [("A standard list checks only the source.","Standard ACL = source only"),("Top to bottom, first match wins, then implicit deny.","Top-down, first match, implicit deny"),("Place it close to the destination.","Place close to the destination")]),
])

save("acl-extended", "Extended ACLs", "Extended ACLs", [
 hook("shield", [("A stricter guard",0),("Who you are",1),("Where you're going, and why",2,CY)],
  "Now meet a stricter guard. They check who you are. Then they check where you're going, and why."),
 story("The embassy checkpoint", "At an embassy, the guard checks more than nationality. They also check which office you want, and what you're there for. In networking, that's the source, the destination and the port. For example, allow staff to reach the visa office, but only for secure web. Block everyone else. Because it can be so specific, an extended list goes close to the source.",
  [("person","Who you are","Source IP",1),("building","Which office","Destination IP",2),("door","What for","Protocol and port",3),("map","Place it near the source","Close to the source",4)]),
 term("Writing one", "Here's an example. Permit T C P from one network to a server on port four four three. The wildcard masks are inverse masks. And the invisible last line denies everything else.",
  [("ip access-list extended WEB","Create and name it",1),("permit tcp 10.1.1.0 0.0.0.255 host 10.2.2.2 eq 443","Source, destination, port",2),("ip access-group WEB in","Apply it",3,CY)]),
 traps("Three mix-ups. Extended lists can match ports and protocols, not just addresses. The wildcard is the inverse of the mask. And a list with only permits still blocks everything else.",
  [("Only source and destination IP","Also protocol, ports, ICMP types",1),("Wildcard = subnet mask","It's the inverse: 0 = match",2),("Only permits allows everything else","Implicit deny blocks the rest",3)]),
 rc("extended ACL", [("Extended lists check source, destination and port.","Source, destination, port"),("Place them close to the source.","Place near the source"),("And remember the implicit deny at the end.","Implicit deny at the end")]),
])

save("hsrp", "HSRP", "HSRP", [
 hook("router", [("One gateway fails",0,RED),("Everyone loses the internet",1),("HSRP keeps a spare ready",2,CY)],
  "If your one gateway fails, everyone loses the internet. That's a big problem. H S R P keeps a spare ready to step in."),
 story("Captain and first officer", "A plane has two pilots, but only one flies at a time. The captain is the active router. The first officer is the standby. Air traffic control uses one call sign, and that's the virtual I P address. If the captain can't fly, the first officer takes over. And the call sign never changes, so nobody notices.",
  [("router","The captain","Active router",1),("person","The first officer","Standby router",2),("key","One shared call sign","Virtual IP",3),("shield","Seamless takeover","Failover",4)]),
 term("Setting it up", "Give the group a virtual I P. Set a priority, where higher wins. And turn on preempt, because it's off by default. Then check with show standby brief.",
  [("standby 1 ip 10.0.0.1","The shared virtual IP",0),("standby 1 priority 110","Higher priority wins",1),("standby 1 preempt","Off by default",2),("show standby brief","Who is active",3,CY)]),
 traps("Three slip-ups. H S R P Hellos come from the real address, not the virtual one. H S R P is active standby, so it doesn't load balance by default. And only the active router answers A R P for the virtual address.",
  [("Hellos come from the virtual IP","They use the real interface IP",1),("HSRP load balances by default","One active router per group",2),("Standby answers ARP too","Only the active router replies",3)]),
 rc("HSRP", [("H S R P gives hosts one gateway that never goes down.","One virtual gateway that survives failure"),("Highest priority wins, default is one hundred.","Highest priority wins; default 100"),("Remember to turn on preempt.","Enable preempt")]),
])

save("osi-model", "The OSI Model", "OSI model", [
 hook("box", [("Seven layers",0),("One journey",1),("Let's ship a package",2,CY)],
  "Seven layers. One journey. Let's ship a package across the world and see what each layer does."),
 story("The shipping company", "You're sending a package from New York to Tokyo. At the top, you write the letter, that's the application. Lower down, it's packed, numbered, and tracked so lost pieces get resent, that's transport. Then someone reads the address and picks the route, that's network. Next, the local truck and its driver, that's data link. And at the very bottom, the road itself, that's physical.",
  [("envelope","Write the letter","Layer 7: Application",1),("box","Number and track it","Layer 4: Transport",2),("map","Pick the route","Layer 3: Network",3),("road","The truck and the road","Layers 2 and 1",4)]),
 term("Names to remember", "Each layer wraps the data in a new name. Layer four makes segments. Layer three makes packets. Layer two makes frames. And layer one is just bits. Routers live at layer three, and switches at layer two.",
  [("Layer 4   Segment","TCP or UDP",1),("Layer 3   Packet","Routers, IP address",2),("Layer 2   Frame","Switches, MAC address",3),("Layer 1   Bits","Cables and signals",4,CY)]),
 traps("Three mix-ups. The internet runs on T C P I P, and O S I is just a reference model. Layer seven is the network service, not the app itself. And encryption belongs to the presentation layer, not the session layer.",
  [("OSI is what the internet uses","The internet uses TCP/IP; OSI is a model",1),("Layer 7 is your browser","It's the service the browser uses",2),("Session layer encrypts","Presentation layer does",3)]),
 rc("OSI model", [("The O S I model has seven layers, from physical up to application.","7 layers, physical to application"),("Data is wrapped as it goes down: segment, packet, frame, bits.","Segment, packet, frame, bits"),("Routers work at layer three, and switches at layer two.","Routers: L3. Switches: L2")]),
])
