import sys; sys.path.insert(0, "tools")
from mk import *

save("vtp", "VTP", "VTP", [
 hook("book", [("Fifty switches",0),("Add one VLAN",1),("Do it fifty times?",2,OR),("VTP does it once",3,CY)],
  "You have fifty switches. You need to add one new V L A N. Do you really want to type it fifty times? V T P does it once."),
 story("The library catalogue", "Imagine a library with many branches. One head librarian keeps the master catalogue, which is the V L A N database. When a new book arrives, the head librarian updates the catalogue and sends fresh index cards to every branch. That's a V T P advertisement. Branches can be servers, who can change the catalogue, clients, who only copy it, or transparent, who keep their own and just pass cards along. Every update has a revision number, and the higher number always wins.",
  [("book","The master catalogue","VLAN database",1),("envelope","Fresh index cards","VTP advertisements",3),("people","Server, client, transparent","The three VTP modes",4),("scale","Higher number wins","Configuration revision number",5)]),
 versus("The three modes", "Server and client", "Transparent", "Here's how the modes behave. Servers create and delete V L A Ns, and share them. Clients can't create anything, they only learn. Transparent switches keep their own list, ignore the neighbours' updates, but still pass the messages on.",
  [("Can create VLANs","Server only","Yes, but local only",0),("Learns from others","Client and server","No",1),("Forwards updates","Yes","Yes",2)]),
 traps("Three warnings. A client can't create V L A Ns locally. A transparent switch does forward updates, it just doesn't use them. And the revision number lives in a file called vlan dot dat, so reloading the switch does not reset it. That's how a lab switch with a high number can wipe out a whole network.",
  [("Clients can create VLANs","Only servers can",1),("Transparent doesn't forward VTP","It forwards but doesn't apply",2),("Reload resets the revision number","It's stored in vlan.dat; it survives a reload",3)]),
 rc("VTP", [("V T P copies the V L A N list from one server to every switch.","VTP copies the VLAN list from a server"),("Remember the three modes: server, client and transparent.","Server, client, transparent"),("And always reset the revision number before adding a switch.","Reset the revision number before adding a switch")]),
])

save("stp-protection", "PortFast and BPDU Guard", "STP protection", [
 hook("door", [("Plug in a PC",0),("Wait thirty seconds?",1,RED),("No thank you",2,CY)],
  "You plug in a computer. And the port makes you wait thirty seconds before it works. That's spanning tree being careful. Let's speed it up, safely."),
 story("The hotel key card", "Walk into a hotel and swipe your card. The door opens at once. That's PortFast. Now picture a hotel that first checks with the front desk whether anyone else is already in the room. That's slow, but safe. Normal spanning tree is the cautious hotel. PortFast skips the wait for ports that only ever lead to a guest's room, meaning an end device. But what if someone plugs in a switch there? That's where B P D U Guard steps in and shuts the door.",
  [("key","Door opens at once","PortFast",2),("clock","Wait and check first","Normal STP: listening, learning",3),("laptop","Rooms only hold guests","Use on access ports only",6),("shield","The door shuts if a switch appears","BPDU Guard",8)]),
 term("The commands", "Turn on PortFast for the port. Then turn on B P D U Guard. If a B P D U ever arrives, the port goes into error disabled.",
  [("spanning-tree portfast","Skip the wait on this port",0),("spanning-tree bpduguard enable","Shut the port if a BPDU arrives",1),("show spanning-tree summary","Verify",2,CY)]),
 traps("Three mix-ups. PortFast isn't a replacement for spanning tree. It only skips the waiting. Don't put it on trunk ports, because that can cause loops. And B P D U Guard doesn't turn spanning tree off. It shuts the port down when something unexpected shows up.",
  [("PortFast replaces STP","STP still runs; only the wait is skipped",1),("PortFast is safe anywhere","Only on access ports, never trunks",2),("BPDU Guard disables STP","It err-disables the port instead",3)]),
 rc("PortFast and BPDU Guard", [("PortFast makes access ports start forwarding immediately.","PortFast: instant start on access ports"),("B P D U Guard shuts a port if a switch is plugged in.","BPDU Guard: err-disables on a BPDU"),("Use them together on every user port.","Use both on every user port")]),
])

save("vlan-security", "VLAN Hopping", "VLAN security", [
 hook("lock", [("Stuck on one floor",0),("But a cheeky guest",1,OR),("Sneaks into another",2,RED)],
  "You're only supposed to reach your own floor. But a clever attacker can sneak into someone else's. This is called V L A N hopping."),
 story("The hotel keycard mix-up", "Think of a hotel where each floor is a V L A N, and the lift is a trunk. In a switch spoofing attack, a guest pretends to be hotel staff. They flash a fake master keycard, using D T P, and the lift treats them like a trunk. Suddenly they can reach every floor. In double tagging, the guest stacks two stickers on a letter. The first lift removes one, and the second delivers to a floor they shouldn't reach.",
  [("person","Guest pretends to be staff","Switch spoofing (DTP)",1),("key","Fake master keycard","Dynamic desirable mode",2),("envelope","Two stickers on one letter","Double tagging",4),("building","The lift delivers it","Reaches another VLAN",5)]),
 flow("How to stop it", "The fixes are simple. Turn off D T P on access ports. Set unused ports to access mode and shut them down. And change the native V L A N to one nobody uses.",
  [("lock","Turn off DTP","switchport nonegotiate",0),("door","Fix ports as access","switchport mode access",1),("gear","Move the native VLAN","Use an unused VLAN",2)]),
 traps("Three mix-ups. D T P isn't a security feature. It's the thing attackers abuse. Double tagging can cross several switches if the native V L A N matches. And port security doesn't stop it, because it limits M A C addresses, not trunking.",
  [("DTP protects against trunking","It can be abused to form trunks",1),("Hopping needs the same switch","Double tagging crosses switches",2),("Port security stops it","It limits MACs, not trunk negotiation",3)]),
 rc("VLAN hopping", [("Switch spoofing abuses D T P, and double tagging abuses the native V L A N.","Spoofing abuses DTP; double tagging abuses native VLAN"),("Turn D T P off on access ports.","Turn DTP off on access ports"),("And move the native V L A N away from V L A N one.","Move the native VLAN away from VLAN 1")]),
])

save("layer2-attacks", "DHCP Snooping", "DHCP snooping", [
 hook("shield", [("Anyone can run a DHCP server",0,RED),("A rogue hands out bad addresses",1),("DHCP snooping stops it",2,CY)],
  "Anyone can plug in a D H C P server. A rogue one hands out bad addresses, and sends your traffic to the attacker. D H C P snooping stops it."),
 story("The bouncer at the party", "At a VIP party, the bouncer lets trusted hosts through the main door, and that's your real D H C P server. Everyone else uses side doors, and they're untrusted. If an untrusted guest tries to hand out party passes, the bouncer stops them. That means dropping offers and acknowledgements on untrusted ports. The bouncer also keeps a list of who got which address, called the binding database.",
  [("door","Main door for trusted hosts","Trusted port (to the real server)",1),("lock","Side doors for everyone else","Untrusted ports",2),("shield","Stops fake handouts","Drops Offer and Ack",3),("book","The guest list","Snooping binding database",4)]),
 term("Setting it up", "Turn it on globally. Turn it on per V L A N. And trust only the port that faces the real server.",
  [("ip dhcp snooping","Enable globally",0),("ip dhcp snooping vlan 10","Enable for this VLAN",1),("ip dhcp snooping trust","On the server-facing port only",2,CY)]),
 traps("Three mix-ups. Snooping doesn't block all D H C P on untrusted ports. It blocks only the server messages. It's turned on globally and per V L A N, not interface by interface. And the database stores client addresses, not the server's.",
  [("Blocks all DHCP on untrusted ports","Only server messages are blocked",1),("Enabled per interface","Global and per VLAN; trust is per interface",2),("Database stores the server IP","It stores client IP, MAC, VLAN, port",3)]),
 rc("DHCP snooping", [("D H C P snooping blocks rogue D H C P servers.","Blocks rogue DHCP servers"),("Only trust the port facing your real server.","Trust only the real server's port"),("The binding database powers other protections too.","The binding database helps other features")]),
])

save("dot1x", "802.1X Port Authentication", "802.1X", [
 hook("key", [("Plug in a cable",0),("And you're on the network",1,RED),("Unless the door checks your ID",2,CY)],
  "Plug in a cable, and you're on the network. Unless the door checks your I D first. That's eight oh two dot one X."),
 story("The hotel key card system", "A guest, called the supplicant, arrives with their I D. The lift, which is the authenticator, won't move until they've been checked. It passes the I D along to the front desk, the authentication server, which is a RADIUS server. The front desk checks the booking records, and says yes or no. The lift just follows the answer. The lift never makes the decision itself.",
  [("person","The guest","Supplicant (the device)",0),("switch","The lift","Authenticator (the switch)",1),("server","The front desk","Authentication server (RADIUS)",2),("list","Checks the booking","Credentials verified",3)]),
 flow("The sequence", "It runs in four steps. The device connects. The switch asks who it is, using E A P O L. The switch relays the answer to the server. The server says accept or reject, and the port opens or stays shut.",
  [("laptop","Device connects","Port is blocked",0),("switch","Switch asks for identity","EAPOL",1),("server","Server checks it","RADIUS",2),("door","Port opens or stays shut","Accept or reject",3)]),
 traps("Three mix-ups. The switch doesn't decide, the server does. E A P O L only runs between the device and the switch, and R A D I U S carries it onward. And eight oh two dot one X authenticates the supplicant on the device, which can still stand for a user.",
  [("The switch decides","The RADIUS server decides",1),("EAPOL goes all the way to the server","Only to the switch; RADIUS carries it on",2),("It only checks the device","The supplicant can prove a user's identity",3)]),
 rc("802.1X", [("Three roles: supplicant, authenticator and server.","Supplicant, authenticator, server"),("The port stays blocked until the server says yes.","Port blocked until the server accepts"),("E A P O L is on the cable, and R A D I U S is behind the switch.","EAPOL on the wire, RADIUS behind the switch")]),
])

save("ethernet-frames", "Ethernet Frames", "Ethernet frames", [
 hook("envelope", [("Your data goes in an envelope",0),("With addresses on the front",1,CY),("That's an Ethernet frame",2)],
  "Before data crosses a cable, it goes into an envelope. It has addresses on the front, and a check on the back. That's an Ethernet frame."),
 story("The postal envelope", "The letter inside is your I P packet. The envelope has a return address, which is the source M A C. It has a destination address, the destination M A C. And a little note saying what's inside, which is the EtherType. At the end, the post office adds a seal, called the F C S, so the receiver can check nothing was damaged. If the seal doesn't match, the frame is thrown away.",
  [("envelope","The envelope","Ethernet frame",0),("map","Return and destination","Source and destination MAC",1),("list","Note about contents","EtherType (0x0800 = IPv4)",2),("stamp","The seal","FCS: checks for damage",3)]),
 term("Sizes to know", "Three numbers matter. The smallest frame is sixty-four bytes. The biggest standard payload is fifteen hundred. And the header is fourteen bytes, with a four byte trailer.",
  [("Minimum frame   64 bytes","Smaller = runt",0),("Maximum payload   1500 bytes","The MTU",1),("Header 14 + FCS 4","18 bytes of overhead",2,CY)]),
 traps("Three slip-ups. The preamble and S F D aren't counted in the frame size. The minimum payload is forty-six bytes, not sixty-four. And in Ethernet two, the EtherType says what's inside, not how long it is.",
  [("The preamble counts in the frame size","It's physical layer overhead, not counted",1),("Minimum payload is 64 bytes","It's 46; the minimum frame is 64",2),("EtherType is always a length","In Ethernet II it's a protocol type",3)]),
 rc("Ethernet frames", [("A frame has addresses, a type, the data and a check.","Addresses, type, data, check"),("Minimum is sixty-four bytes, and maximum payload is fifteen hundred.","64 byte minimum; 1500 byte payload"),("A bad F C S means the frame is dropped.","Bad FCS = frame dropped")]),
])

save("duplex", "Duplex and Autonegotiation", "Duplex", [
 hook("mic", [("Walkie talkie or telephone?",0),("One talks, one listens",1),("Or both at once",2,CY)],
  "Walkie talkie or telephone? On one, you take turns. On the other, you talk at the same time. That's half duplex versus full duplex."),
 story("Walkie talkie vs telephone", "On a walkie talkie, you press to talk, and you can't hear the other person. If you both press at once, nobody hears anything, which is a collision. That's half duplex. A telephone lets both people talk and listen at the same time. That's full duplex, and it has no collisions. Modern switches negotiate this automatically, and it goes wrong if one side is hard set while the other is on auto.",
  [("mic","Press to talk","Half duplex",1),("bell","Both press at once","Collision",2),("people","Talk and listen together","Full duplex",3),("wrench","One side hard set","Duplex mismatch",5)]),
 versus("Half vs full", "Half duplex", "Full duplex", "Here's the comparison. Half duplex sends or receives, never both. Collisions are normal, and so is the C S M A C D back off. Full duplex does both at the same time, with no collisions. The speed each way stays the same, so it doesn't double the link.",
  [("Send and receive","One at a time","Both together",0),("Collisions","Possible","None",1),("Used with","Hubs or failed autonegotiation","Switch ports",2)]),
 traps("Three mix-ups. A switch isn't always full duplex. Hubs and failed negotiation can force half. Full duplex doesn't double the bandwidth in each direction. And autonegotiation doesn't always pick the best, especially if one side is hard coded. Then the other falls back to half.",
  [("A switch is always full duplex","Hubs or failed autoneg can force half",1),("Full duplex doubles bandwidth","Each direction stays at link speed",2),("Autoneg always picks best","A hard-coded side breaks it",3)]),
 rc("duplex", [("Half duplex takes turns, and full duplex doesn't.","Half takes turns; full doesn't"),("A mismatch causes slow links and late collisions.","Mismatch = slow link, late collisions"),("Set both ends to auto, or both to the same fixed value.","Both auto, or both fixed the same")]),
])

save("interface-errors", "Interface Errors", "Interface errors", [
 hook("wrench", [("The link is up",0),("But everything is slow",1,OR),("The counters will tell you why",2,CY)],
  "The link is up. But everything is slow. The interface counters can tell you why."),
 story("The parcel sorting office", "A sorting office has rules. Every parcel must be bigger than a shoebox and smaller than a suitcase. Too small is a runt, a broken fragment. Too big is a giant. If the seal doesn't match, that's a C R C error, usually a bad cable or noise. If two parcels crash on the belt late, that's a late collision, often a duplex mismatch. Watch which counter is growing, because it points straight at the cause.",
  [("box","Too small","Runts",1),("box","Too big","Giants",2),("stamp","Seal doesn't match","CRC errors: cable or noise",3),("bell","Late crash on the belt","Late collisions: duplex mismatch",4)]),
 term("Where to look", "Start with show interfaces. Look at the input errors, C R C and collisions. And clear the counters, so you can watch what grows.",
  [("show interfaces g0/1","Look for CRC, runts, giants",0),("show interfaces status","Speed and duplex at a glance",1),("clear counters g0/1","Reset, then watch what grows",2,CY)]),
 traps("Three habits to build. A growing C R C count means a physical problem, not a configuration one. Late collisions on a full duplex link point at a mismatch. And a few old errors don't matter if the number isn't climbing.",
  [("CRC errors mean misconfiguration","Usually cabling or interference",1),("Late collisions are normal","They signal a duplex mismatch",2),("Any error count is a crisis","Only worry if it keeps growing",3)]),
 rc("interface errors", [("Check the counters whenever a link feels slow.","Check counters on a slow link"),("C R C points at the cable, and late collisions point at duplex.","CRC = cable; late collisions = duplex"),("Clear the counters, then watch what grows.","Clear counters, watch what grows")]),
])

save("network-devices", "Collision and Broadcast Domains", "Network domains", [
 hook("building", [("Open plan office",0),("Or cubicles",1),("Which is quieter?",2,CY)],
  "An open plan office, or one with cubicles. Which one is quieter? Networks have the same question."),
 story("Open plan or cubicles", "In an open plan office, everyone hears everyone. If two people speak at once, it's a collision. That's a collision domain, like a hub. A switch gives every person a cubicle, so each port is its own collision domain. But if someone shouts for everyone, the whole floor still hears. That's a broadcast, and the floor is a broadcast domain. Only a router, or a V L A N, builds walls between floors.",
  [("people","Everyone hears everyone","Collision domain (hub)",1),("switch","Each person gets a cubicle","Each switch port",3),("bell","A shout everyone hears","Broadcast domain",5),("router","Walls between floors","Routers and VLANs",6)]),
 versus("What splits what", "Collision domains", "Broadcast domains", "Here's the key. A hub makes one collision domain for all ports. A switch makes one per port. A switch alone keeps one broadcast domain. A router, or a V L A N, makes a new one.",
  [("Hub","One for all ports","One",0),("Switch","One per port","One (unless VLANs)",1),("Router","One per interface","One per interface",2)]),
 traps("Three mix-ups. A switch doesn't make one big collision domain. It makes one for each port. V L A Ns split broadcast domains, not collision domains. And a router splits broadcast domains, while each of its interfaces is its own collision domain too.",
  [("A switch is one collision domain","One per port",1),("VLANs split collision domains","VLANs split broadcast domains",2),("Routers split both... confusingly","They split broadcast; each interface is its own collision domain",3)]),
 rc("network domains", [("Switch ports split collision domains.","Switch ports split collision domains"),("Routers and V L A Ns split broadcast domains.","Routers and VLANs split broadcast domains"),("Count them: that's a favourite exam question.","Count the domains: a common exam question")]),
])

save("cabling-types", "Cabling Types", "Cabling", [
 hook("road", [("Copper or fibre?",0),("Cheap and short",1),("Or fast and far",2,CY)],
  "Copper or fibre? One is cheap and short. The other is fast and goes far."),
 story("Highway vs express lane", "Copper Ethernet is a multi lane highway. It's cheap and easy, but beyond a hundred metres the traffic gets congested, and the signal fades. Fibre is a dedicated express lane that uses light. It goes much further, and noise can't touch it. Multimode fibre is for shorter runs in a building. Single mode fibre is for long distances between sites.",
  [("road","Cheap multi-lane highway","Copper twisted pair",1),("ruler","Congestion past 100 metres","100 m limit",2),("wifi","Express lane of light","Fibre optic",3),("building","Inside, or between sites","Multimode vs single-mode",4)]),
 term("Distances to know", "A few distances show up on the exam. Copper stops at a hundred metres. Multimode gigabit fibre reaches five fifty metres. Single mode reaches five kilometres, or much more with better optics. And Cat six only carries ten gigabit to fifty-five metres, while Cat six A does a full hundred.",
  [("Copper (Cat5e/6)   100 m","Twisted pair limit",1),("Multimode 1000BASE-SX   550 m","Inside buildings",2),("Single-mode 1000BASE-LX   5 km","Between sites",3),("Cat6 10GBASE-T   55 m","Cat6a reaches 100 m",4,CY)]),
 traps("Three mix-ups. Fibre has distance limits too, and they depend on the type. Not all Cat six carries ten gigabit for a hundred metres, only Cat six A. And a T D R test needs the interface shut down, because it sends test pulses down the cable.",
  [("Fibre has no limit","Limits depend on the fibre type",1),("Cat6 does 10G to 100 m","Cat6 only to 55 m; Cat6a to 100 m",2),("Run TDR on a live port","Shut the interface down first",3)]),
 rc("cabling", [("Copper is cheap but stops at a hundred metres.","Copper: 100 m"),("Fibre goes further, and single mode goes furthest.","Fibre goes further; single-mode furthest"),("Cat six A is what you need for ten gigabit at full distance.","Cat6a for 10G at 100 m")]),
])

save("rip", "RIP", "RIP", [
 hook("envelope", [("The oldest routing protocol",0),("Counts steps, nothing else",1),("Simple, slow and still tested",2,CY)],
  "R I P is the oldest routing protocol still on the exam. It counts steps and nothing else. It's simple, slow, and still tested."),
 story("The town crier", "In a quiet village, every resident knows only their neighbours. Every thirty seconds, the town crier walks round shouting every house they know and how many steps away it is. You write it down and add one step. That count is the hop count. Fifteen steps is the limit, and sixteen means unreachable. It's simple, but a long road takes forever to hear about.",
  [("mic","Shouts every 30 seconds","Periodic updates",1),("ruler","Count the steps","Hop count",3),("lock","Fifteen is the limit","16 = unreachable",4)]),
 term("Setting up RIPv2", "To set it up, use version two. Turn off auto summary. Advertise your networks. And check with show I P protocols.",
  [("router rip","Start RIP",0),("version 2","Use RIPv2, not v1",1),("no auto-summary","Stop classful summarising",2),("network 10.0.0.0","Advertise this network",3,CY)]),
 traps("Three mix-ups. R I P version two uses multicast, not broadcast. You can turn off auto summary with one command. And R I P uses U D P port five twenty, not T C P.",
  [("RIPv2 uses broadcast","It uses multicast 224.0.0.9",1),("You can't turn off auto-summary","Use: no auto-summary",2),("RIP uses TCP 520","It uses UDP 520",3)]),
 rc("RIP", [("R I P counts hops, and sixteen means unreachable.","RIP: hop count; 16 = unreachable"),("Use version two, and turn off auto summary.","Use v2; no auto-summary"),("It updates every thirty seconds over U D P.","Updates every 30 s over UDP 520")]),
])

save("floating-static", "Floating Static Routes", "Floating static", [
 hook("road", [("Your main link fails",0,RED),("Is there a plan B?",1),("A floating static route",2,CY)],
  "Your main link fails. Is there a plan B? A floating static route is the backup plan."),
 story("The backup route", "On a road trip, you plan the fast highway, and keep a longer route in reserve. Your G P S prefers the highway, but if it's closed, it quietly uses the backup. A floating static route works the same way. You give it a worse trust score, called a higher administrative distance. While the main route is working, the backup stays hidden. When the main route disappears, the backup floats up into the routing table.",
  [("road","The fast highway","Primary route (low AD)",0),("map","The longer backup","Floating static (higher AD)",1),("scale","Worse trust score","AD higher than the primary",3),("bell","Highway closes","Backup enters the table",5)]),
 term("Writing one", "Here's the idea. A normal static route, and then the same route with a higher number on the end. If your main protocol is O S P F at one ten, use something above that, like one thirty.",
  [("ip route 10.1.1.0 255.255.255.0 192.168.1.2","Primary static (AD 1)",0),("ip route 10.1.1.0 255.255.255.0 192.168.2.2 130","Backup: AD 130",1),("show ip route","Only the primary shows while it works",2,CY)]),
 traps("Three mix-ups. Raising the metric doesn't make a backup. The distance is what counts. A floating route only shows up when the main route is gone. And the default static distance is one, while connected is zero.",
  [("Higher metric makes a backup","Use a higher admin distance",1),("It's always in the table","Only when the primary is missing",2),("Static AD is 0","Static is 1; connected is 0",3)]),
 rc("floating static routes", [("A floating static route is a backup with a higher administrative distance.","Backup route = higher AD"),("Pick a number higher than your main protocol.","Choose an AD above the main protocol's"),("It only appears when the main route fails.","It appears only on failure")]),
])

save("eigrp-config", "EIGRP Configuration", "EIGRP configuration", [
 hook("router", [("Five commands",0),("And two routers are talking",1,CY),("Let's configure EIGRP",2)],
  "Five commands. And two routers are talking. Let's configure E I G R P."),
 story("Couriers and route cards", "Think of a team of couriers, one at each post office. Every five seconds, they swap route cards, called hello packets. When a new route turns up, they send a reliable update, and the other office must confirm it. Offices only become neighbours if they use the same autonomous system number. But the timers don't need to match, because each side uses its own hold time.",
  [("clock","Route cards every 5 seconds","Hello packets",1),("envelope","Update that must be confirmed","Reliable updates",2),("key","Same team number","AS number must match",3),("clock","Timers can differ","Hello/Hold need not match",4)]),
 term("The configuration", "Start the process with your A S number. Advertise the network, with a wildcard mask. Check your neighbours. And check your routes.",
  [("router eigrp 100","AS number must match",0),("network 10.0.0.0 0.0.0.255","Wildcard mask picks interfaces",1),("show ip eigrp neighbors","Who we've met",2),("show ip route eigrp","What we learned",3,CY)]),
 traps("Three mix-ups. The hello and hold timers don't have to match. E I G R P doesn't load balance unequal paths unless you set variance. And the network command uses a wildcard mask to pick exactly which interfaces to include.",
  [("Hello and Hold must match","They don't have to",1),("EIGRP balances unequal paths by default","Only with the variance command",2),("network is always classful","A wildcard mask narrows it",3)]),
 rc("EIGRP configuration", [("The A S number has to match on both sides.","AS number must match"),("The network command picks interfaces, using a wildcard mask.","network + wildcard mask picks interfaces"),("Check with show I P eigrp neighbors.","show ip eigrp neighbors")]),
])

save("routing-process", "How a Router Forwards a Packet", "Routing process", [
 hook("router", [("A packet arrives",0),("The router has a few seconds",1),("To decide where it goes",2,CY)],
  "A packet arrives at a router. It has a split second to decide where it goes. Here's how it thinks."),
 story("The sorting office", "A sorting office gets letters in an outer envelope addressed to the office itself. That's the frame, with the router's own M A C address. The worker opens the outer envelope and reads the inner address. That's the I P address. Then they check a giant wall chart, which is the routing table, for the best match. They put the letter in a new outer envelope for the next stop, and cross one off the lifetime count.",
  [("envelope","Outer envelope to the office","Frame to the router's MAC",1),("book","Read the inner address","Destination IP",3),("map","Check the wall chart","Routing table lookup",4),("clock","Cross one off the lifetime","TTL minus 1",5)]),
 flow("Four steps", "Every hop runs the same four steps. Strip the old frame. Look up the destination in the table. Lower the T T L by one. And wrap it in a new frame for the next hop.",
  [("envelope","Strip the old frame","Layer 2 removed",0),("map","Look up the destination","Longest prefix match",1),("clock","Reduce TTL by one","Drop it at zero",2),("box","Re-wrap in a new frame","New MAC for the next hop",3)]),
 traps("Three mix-ups. Routers forward on the I P address, not the M A C. The T T L drops by exactly one at each router. And a router only uses a default route if you've configured one. Otherwise, it drops the packet.",
  [("Routers forward by MAC","They route by destination IP",1),("TTL drops by hops remaining","It drops by exactly 1",2),("A default route exists automatically","You must configure 0.0.0.0/0",3)]),
 rc("the routing process", [("A router strips the frame, looks up the I P address, and wraps a new frame.","Strip, look up, re-wrap"),("The T T L goes down by one at every hop.","TTL decreases by 1 per hop"),("No matching route and no default means the packet is dropped.","No route and no default = dropped")]),
])
