import sys; sys.path.insert(0, "tools")
from mk import *

save("tcp-udp", "TCP vs UDP", "TCP vs UDP", [
 hook("envelope", [("Two ways to send data",0),("Certified mail",1,CY),("Or a postcard",2,OR),("Which one do you need?",3)],
  "There are two ways to send data across a network. One is like certified mail. The other is like a postcard. Which one you need depends on the job."),
 story("Certified mail or postcard", "Certified mail is T C P. You fill in a form, pay for tracking, and get a signature back as proof. If it gets lost, you find out and send it again. It's reliable, but all that paperwork takes time. A postcard is U D P. You scribble a message, drop it in the box, and hope for the best. There's no receipt and no resend, but it's very quick. That's why video calls use postcards, and file downloads use certified mail.",
  [("stamp","Forms, tracking, signature","TCP: reliable, connection first",1),("clock","Paperwork takes time","TCP: slower, more overhead",3),("envelope","Quick scribble, no receipt","UDP: fast, no guarantees",4),("mic","Live calls can't wait","Voice and video use UDP",5)]),
 versus("Side by side", "TCP", "UDP", "Here's the comparison. T C P sets up a connection first, using a handshake. U D P just sends. T C P has a bigger header, between twenty and sixty bytes. U D P's header is always exactly eight. And for apps, web and email use T C P, while D N S queries, voice and streaming use U D P.",
  [("Connection","Handshake first","None",0),("Header size","20 to 60 bytes","Exactly 8 bytes",1),("Typical apps","Web, email, file transfer","DNS queries, voice, streaming",2)]),
 traps("Three mix-ups. U D P isn't faster because its packets are smaller. It's faster because it skips setup, receipts and resends. T C P can't promise delivery on a broken link. It only tells you when it gave up. And U D P still has port numbers, just like T C P.",
  [("UDP is faster because packets are smaller","It skips setup, acknowledgments and resends",1),("TCP guarantees delivery","On a dead link it gives up and reports failure",2),("UDP has no port numbers","It has source and destination ports",3)]),
 rc("TCP and UDP", [("T C P is reliable but slower, and U D P is fast but has no guarantees.","TCP: reliable. UDP: fast, no guarantees"),("The exam trick is to match the app. Files use T C P, and streaming uses U D P.","Match the app: files = TCP, streaming = UDP"),("D N S queries use U D P, but zone transfers use T C P.","DNS: UDP for queries, TCP for zone transfers")]),
])

save("tcp-handshake-flow", "The TCP Three-Way Handshake", "TCP handshake", [
 hook("question", [("Before any data moves",0),("Two computers say hello",1,CY),("In exactly three steps",2)],
  "Before any data moves, two computers have to say hello. It's a quick routine. And it takes exactly three steps."),
 story("A phone call", "Think of a phone call between Alice and Bob. Alice dials. That's the SYN. Bob picks up and says hello, and that's the SYN ACK. But Alice still has to say hello back, so he knows she can hear him. That's the final ACK. Only now do both sides know the line works, and the real conversation can start. If Bob is busy, he sends a busy signal, which is a reset.",
  [("mic","Alice dials","1. SYN",1),("person","Bob picks up","2. SYN-ACK",2),("people","Alice says hello back","3. ACK",3),("lock","Busy signal","RST",5)]),
 flow("The three steps", "Here are the three steps in order. The client sends a SYN. The server answers with a SYN ACK. The client finishes with an ACK. Now both sides are established.",
  [("laptop","Client sends SYN","I'd like to talk",0),("server","Server sends SYN-ACK","Fine, and I hear you",1),("laptop","Client sends ACK","Great, we're connected",2),("link","Both sides ESTABLISHED","Data can flow",3)]),
 traps("Three common slip-ups. The client never sends the first SYN ACK. It starts with a plain SYN. The handshake isn't finished after the SYN ACK. It needs that last ACK. And sequence numbers start at a random number. Wireshark just shows them as zero to make them easier to read.",
  [("Client sends SYN-ACK first","Client sends SYN; server sends SYN-ACK",1),("Done after the SYN-ACK","It needs the final ACK",2),("Sequence numbers start at 0","Random start; Wireshark shows relative",3)]),
 rc("TCP handshake", [("The handshake is SYN, then SYN ACK, then ACK.","SYN, SYN-ACK, ACK"),("Both sides must reach established before data flows.","Both sides ESTABLISHED, then data"),("Sequence numbers start random, not at zero.","Random starting sequence numbers")]),
])

save("arp", "ARP", "ARP", [
 hook("question", [("You know the I P address",0),("The switch needs a M A C",1,OR),("So who has it?",2,CY)],
  "Your computer knows the I P address it wants to reach. But the switch only understands M A C addresses. So how does it find the match? It asks."),
 story("The office directory", "Picture a big office with no central directory. Everyone keeps a personal notebook of who sits where. Bob wants to send Alice a document, but he only knows her name. So he shouts down the hallway. Who is Alice? Please tell me your office number. That shout is the A R P request, and everyone hears it. Alice answers Bob directly, just to him. Bob writes it in his notebook, and next time he doesn't need to shout.",
  [("mic","Bob shouts to everyone","ARP request (broadcast)",3),("person","Alice answers just Bob","ARP reply (unicast)",4),("book","Bob's notebook","ARP cache",5)]),
 flow("Request and reply", "It's a two step conversation. First, a broadcast asking who owns the address. Second, a direct reply with the answer. Then the answer is cached for later.",
  [("mic","Request","Broadcast to FF:FF:FF:FF:FF:FF",0),("envelope","Reply","Unicast straight back",1),("book","Cache it","Reuse for 4 hours on Cisco",2)]),
 term("Useful commands", "Two commands to know. Show I P arp lets you see the cache. And clear arp cache empties it.",
  [("show ip arp","See the ARP cache",0),("clear arp-cache","Flush it",1,CY)]),
 traps("Three mix-ups. A R P never crosses a router. It stays within one subnet. The reply is a unicast, not a broadcast. And cached entries do expire. On Cisco, after four hours by default.",
  [("ARP works across routers","It stays inside one broadcast domain",1),("The reply is a broadcast","The reply is a unicast",2),("ARP entries last forever","They time out (4 hours on Cisco)",3)]),
 rc("ARP", [("A R P turns an I P address into a M A C address on the same network.","ARP: IP address to MAC address, same subnet"),("The request is a broadcast, and the reply goes straight back.","Request: broadcast. Reply: unicast"),("Answers are cached, so it doesn't have to ask again.","Answers are cached")]),
])

save("icmp-ping-traceroute", "ICMP, Ping and Traceroute", "Ping and traceroute", [
 hook("bell", [("Is anybody out there?",0),("Ping asks",1,CY),("Traceroute follows the trail",2,OR)],
  "Is anybody out there? Ping is how you ask. And traceroute follows the trail to show you where things stop."),
 story("The return to sender slip", "Think of the postal service's pink return to sender slip. You didn't ask for it. It simply tells you why a delivery failed. That slip is I C M P. Ping is a letter marked, please reply if you get this. If the host is there, it writes back. Traceroute is cleverer. It sends letters that expire early, one hop at a time. Each router that tosses one back reveals itself.",
  [("envelope","The pink slip","ICMP messages",1),("bell","Please reply if you get this","Ping: Echo request and reply",3),("map","Letters that expire early","Traceroute uses TTL",5),("router","Each router reveals itself","Time Exceeded replies",6)]),
 term("Types to remember", "A few I C M P types show up on the exam. Type eight is the echo request, and type zero is the reply. Type three means destination unreachable. And type eleven means time exceeded, which is what traceroute listens for.",
  [("Type 8","Echo request (ping)",0),("Type 0","Echo reply",1),("Type 3","Destination unreachable",2),("Type 11","Time exceeded (traceroute)",3,CY)]),
 traps("Three slip-ups. Ping has no ports, because I C M P sits straight on top of I P. A good ping doesn't mean the web server works. And a failed ping doesn't prove there's no connection, because I C M P may be filtered. Also, Cisco traceroute sends U D P probes by default, not I C M P.",
  [("Ping uses TCP or UDP","ICMP sits directly on IP, no ports",1),("Ping works so the app works","It only tests IP reachability",2),("Failed ping means no connectivity","ICMP may simply be filtered",3),("Cisco traceroute uses ICMP","It uses UDP probes by default",4)]),
 rc("ping and traceroute", [("Ping checks if a host answers, using echo request and reply.","Ping = echo request and reply"),("Traceroute uses the T T L to reveal every router on the way.","Traceroute reveals each hop"),("And a failed ping doesn't always mean a broken network.","Failed ping is not proof of failure")]),
])

save("dhcp-relay", "DHCP Relay", "DHCP relay", [
 hook("question", [("One DHCP server",0),("Many subnets",1),("Broadcasts don't cross routers",2,RED),("So how does it work?",3,CY)],
  "You have one D H C P server. And many subnets. But broadcasts never cross a router. So how does a new device ever get an address?"),
 story("The campus mailroom", "A university has one central post office and lots of buildings. A student in the science building drops a request in the local mailroom. The clerk can't shout across campus, so they write a proper addressed envelope to the central post office. They also stamp it with the science building's return address, so the post office knows which pool of addresses to use. That clerk is the relay agent, and the return address is called the giaddr.",
  [("building","Each building","A subnet",0),("person","The local clerk","Relay agent (the router)",1),("envelope","A proper addressed envelope","Unicast to the DHCP server",2),("map","Building's return address","giaddr picks the pool",3)]),
 term("The command", "The magic command is I P helper address. It goes on the interface facing the clients, not the one facing the server. And you can add more than one, for backup.",
  [("interface g0/0","The interface facing the clients",0),("ip helper-address 10.0.0.5","Where the DHCP server lives",1),("show ip interface g0/0","Verify it's set",2,CY)]),
 traps("Three mix-ups. The relay doesn't pass the broadcast along. It creates a brand new unicast to the server. The giaddr holds the relay's own address, not the client's, because the client has none yet. And helper address goes on the client facing interface.",
  [("Relay forwards the broadcast as a broadcast","It sends a new unicast to the server",1),("giaddr is the client's address","It's the relay's address on the client's subnet",2),("Helper goes on the server-facing side","It goes on the client-facing interface",3)]),
 rc("DHCP relay", [("A relay lets one D H C P server serve many subnets.","One DHCP server, many subnets"),("The helper address goes on the client facing interface.","ip helper-address on the client side"),("And the giaddr tells the server which pool to use.","giaddr selects the address pool")]),
])

save("nat-config", "NAT Configuration", "NAT configuration", [
 hook("router", [("Same idea, three ways to set it up",1),("Static",2,CY),("Dynamic",3,LIME),("And overload",4,OR)],
  "Now let's actually configure N A T. There are three ways to set it up. Static. Dynamic. And overload."),
 story("The switchboard operator", "Think of a company switchboard. Two hundred staff share one public phone number, and each has a private extension. When extension two oh one calls out, the operator swaps in the company number, and notes it in a call log. When the customer calls back, she checks the log and connects them to the right extension. Outsiders never see the extensions, only the company number.",
  [("people","Staff with private extensions","Private IP addresses",1),("router","The operator swaps the number","NAT on the router",2),("book","The call log","NAT translation table",3),("shield","Outsiders see one number","Internal addresses hidden",4)]),
 versus("Static or dynamic", "Static NAT", "Dynamic NAT", "Here's how the first two differ. Static gives one fixed public address to one inside host. That's what you use for a server people connect to. Dynamic hands out addresses from a pool, and each host borrows one for a while.",
  [("Mapping","Fixed one-to-one","Borrowed from a pool",0),("Best for","Servers reachable from outside","Hosts going out",1),("Lasts","Until you remove it","Until it times out",2)]),
 term("Overload in four steps", "The most common setup is overload, also called P A T. Mark the inside and outside interfaces. Write an access list for who may be translated. Then tie it to the outside interface with overload. And verify with show I P nat translations.",
  [("ip nat inside / ip nat outside","Mark the interfaces",0),("access-list 1 permit 192.168.1.0 0.0.0.255","Who may be translated",1),("ip nat inside source list 1 interface g0/1 overload","The PAT rule",2),("show ip nat translations","Verify",3,CY)]),
 traps("Three things to remember. N A T hides addresses, but it isn't encryption or authentication. It can break protocols that hide addresses inside the data, like F T P. And translations time out, so entries disappear after a while.",
  [("NAT is a security feature","It hides addresses; no encryption or authentication",1),("NAT works with every protocol","FTP and others embed IPs and need help",2),("Translations stay forever","Dynamic entries time out",3)]),
 rc("NAT configuration", [("Static is one to one, dynamic uses a pool, and overload shares one address.","Static, dynamic, overload"),("Mark the inside and outside interfaces first.","Mark inside and outside first"),("And check your work with show I P nat translations.","show ip nat translations")]),
])

save("wifi-standards-bands", "Wi-Fi Standards and Bands", "Wi-Fi standards", [
 hook("wifi", [("b, g, n, a c, a x",0),("Alphabet soup",1,OR),("Let's make sense of it",2,CY)],
  "B, G, N, A C, A X. Wi Fi standards look like alphabet soup. Let's make sense of them."),
 story("Highways getting wider", "Think of Wi Fi standards as an upgrading highway system. The data rate is the speed limit. But real speed depends on traffic and road conditions, which is interference. Each new standard widens the road, and adds smarter lanes. Even so, you'll only ever get about half the posted speed in real life.",
  [("road","The speed limit","Maximum data rate",1),("cloud","Traffic and weather","Interference",2),("list","Wider road, smarter lanes","Newer standard",3),("scale","Real life is about half","Throughput is ~50-60% of rate",4)]),
 term("The family tree", "Here's the list in order. Eight oh two dot eleven b is old, with eleven megabits, on two point four gigahertz. Then a and g reach fifty-four. N is called Wi Fi four, and reaches six hundred. A C is Wi Fi five, and lives only on five gigahertz. And A X is Wi Fi six, which adds the six gigahertz band.",
  [("802.11b","11 Mbps, 2.4 GHz",1),("802.11a / g","54 Mbps, 5 GHz / 2.4 GHz",2),("802.11n (Wi-Fi 4)","Up to 600 Mbps, both bands",3),("802.11ac (Wi-Fi 5)","Up to 6.93 Gbps, 5 GHz only",4),("802.11ax (Wi-Fi 6)","Up to 9.6 Gbps, 2.4, 5 and 6 GHz",5,CY)]),
 traps("Three slip-ups. A C works only on five gigahertz. Wider channels aren't always better, because you get fewer that don't overlap. On two point four, there are only three clear channels, one, six and eleven. And N goes up to six hundred megabits, not fifty-four.",
  [("802.11ac uses both bands","5 GHz only",1),("Wider channels are always better","Fewer non-overlapping channels, more interference",2),("802.11n tops out at 54 Mbps","Up to 600 Mbps",3)]),
 rc("Wi-Fi standards", [("Each Wi Fi standard is a wider, smarter road.","Each standard widens and speeds up the road"),("A C is five gigahertz only, and A X adds six gigahertz.","ac: 5 GHz only. ax adds 6 GHz"),("On two point four, stick to channels one, six and eleven.","2.4 GHz: use channels 1, 6, 11")]),
])

save("wlan-architecture", "WLAN Architecture", "WLAN architecture", [
 hook("wifi", [("One access point is easy",0),("Five hundred is chaos",1,RED),("Time for a dispatcher",2,CY)],
  "Managing one access point is easy. Managing five hundred is chaos. You need a central dispatcher."),
 story("Pizza delivery", "A pizza shop starts with a few drivers, each with their own map and phone. Every driver makes their own decisions, and that's autonomous mode. As the city grows, drivers get lost and orders clash. So the shop opens a dispatch office, the wireless controller. Drivers still drive and carry the pizzas, but the office decides the routes and keeps everyone coordinated. Those drivers are lightweight access points, and they talk to the dispatcher using a tunnel called CAPWAP.",
  [("person","Drivers decide alone","Autonomous APs",1),("building","The dispatch office","Wireless LAN controller",3),("router","Drivers still deliver","Lightweight APs forward data",4),("link","The phone line to the office","CAPWAP tunnel",5)]),
 versus("Three models", "Controller based", "Cloud or FlexConnect", "There are a few ways to arrange it. A central controller manages every access point from one place. FlexConnect lets remote offices switch traffic locally while still managed centrally. And cloud managed, like Meraki, needs no on site controller, but does need the internet.",
  [("Where's the brain","Central controller","Cloud, or central with local switching",0),("Traffic","Tunnelled to the controller","Switched locally at the AP",1),("Needs","A controller on site","Internet access (cloud)",2)]),
 traps("Three mix-ups. CAPWAP uses U D P, not T C P. Control uses port fifty-two forty-six, and data uses fifty-two forty-seven. Not all traffic must go through the controller, because FlexConnect can switch it locally. And autonomous access points are still used in small sites.",
  [("CAPWAP uses TCP","UDP: 5246 control, 5247 data",1),("All traffic goes through the WLC","FlexConnect can switch locally",2),("Autonomous APs are obsolete","Still used in small deployments",3)]),
 rc("WLAN architecture", [("Autonomous access points work alone, and lightweight ones need a controller.","Autonomous vs lightweight APs"),("They talk to the controller using CAPWAP over U D P.","CAPWAP over UDP"),("FlexConnect keeps traffic local at remote sites.","FlexConnect = local switching")]),
])

save("wifi-security", "Wi-Fi Security", "Wi-Fi security", [
 hook("lock", [("Your Wi Fi password",0),("Is it really safe?",1,OR),("It depends which lock you use",2,CY)],
  "Your Wi Fi has a password. But is it really safe? That depends entirely on which lock you're using."),
 story("Hotel keys over the years", "Think of how hotel keys evolved. W E P was one metal key shared by every guest. Copy it once, and you can enter any room. W P A brought electronic locks with a new key per guest, but the cipher inside could still be picked. W P A two upgraded the lock to A E S, which is far tougher. But guests still shared one passphrase, so a weak one could be guessed offline. W P A three fixed that, and a stolen password no longer unlocks old traffic.",
  [("key","One key for everyone","WEP: static, easy to crack",1),("lock","Electronic lock, weak cipher","WPA: TKIP",2),("shield","Much tougher lock","WPA2: AES (CCMP)",3),("gear","Fresh key, can't be replayed","WPA3: SAE, forward secrecy",5)]),
 versus("WPA2 vs WPA3", "WPA2", "WPA3", "Here are the key differences. W P A two uses A E S with a hundred and twenty-eight bit key. W P A three moves to two fifty-six bit. W P A two Personal can be attacked offline if the passphrase is weak. W P A three uses S A E, which stops that.",
  [("Encryption","AES-128 (CCMP)","AES-256 (GCMP)",0),("Key exchange","PSK 4-way handshake","SAE handshake first",1),("Weak password","Can be cracked offline","Resists offline guessing",2)]),
 traps("Three mix-ups. W P A three isn't backward compatible, though many access points offer a transition mode. Enterprise mode adds per user logins, but W P A three Personal can still be stronger in some ways. And W P A three still has a four way handshake, but it follows S A E.",
  [("WPA3 is backward compatible","Transition mode offers both",1),("WPA2-Enterprise always beats WPA3","Different strengths; WPA3 has forward secrecy",2),("WPA3 drops the 4-way handshake","It keeps it, after SAE",3)]),
 rc("Wi-Fi security", [("W E P is broken. W P A uses T K I P. W P A two uses A E S.","WEP broken, WPA TKIP, WPA2 AES"),("W P A three adds S A E and forward secrecy.","WPA3: SAE + forward secrecy"),("Never use T K I P, and prefer W P A three.","Avoid TKIP; prefer WPA3")]),
])

save("poe", "Power over Ethernet", "PoE", [
 hook("switch", [("One cable",0),("Data and power",1,CY),("No wall socket needed",2)],
  "One cable. Data and power together. No wall socket needed. That's power over Ethernet."),
 story("The power strip", "A TV, a console and a soundbar each need a signal and a socket. A power strip lets one wall outlet feed several devices, but it has a total wattage limit. Go over it, and the breaker trips. Think of your switch as that power strip. Each port is a socket, and the switch's power supply is the wall outlet. The P o E standards say how much power each socket can give. And the switch has a total budget to share.",
  [("switch","The power strip","The PoE switch",2),("box","Each socket","A PoE port",3),("gear","The total wattage limit","The switch's power budget",5)]),
 term("Power levels", "There are three standards to know. A F gives fifteen point four watts per port. A T, called P o E plus, gives thirty. And B T goes up to sixty, or even a hundred watts.",
  [("802.3af (PoE)","15.4 W per port",0),("802.3at (PoE+)","30 W per port",1),("802.3bt (PoE++)","60 W or 100 W per port",2,CY)]),
 term("Checking your power", "To check power, use show power inline. By default, ports are on auto, which negotiates just what's needed. Static reserves the full amount. And never turns power off.",
  [("show power inline","Budget and per-port status",0),("power inline auto","Default: negotiate",1),("power inline static","Reserves the maximum",2),("power inline never","Switch PoE off",3,CY)]),
 traps("Three mix-ups. Not every P o E switch gives thirty watts. Check the standard. A normal device with an Ethernet port won't get power. It needs to be a powered device. And static mode wastes budget, because it reserves the maximum.",
  [("All PoE switches give 30 W","af = 15.4 W, at = 30 W, bt = up to 100 W",1),("PoE powers anything with an Ethernet port","Only powered devices with the right signature",2),("Static saves budget","It reserves the maximum; auto is more efficient",3)]),
 rc("PoE", [("P o E sends power and data over one cable.","PoE = power and data on one cable"),("Learn the three levels: fifteen, thirty and up to a hundred watts.","15.4 W, 30 W, up to 100 W"),("And remember the switch has a total power budget.","The switch has a total power budget")]),
])
