import sys; sys.path.insert(0, "tools")
from mk import *

save("vlans", "VLANs", "VLANs", [
 hook("building", [("One open-plan office",0),("Every message reaches everyone",1,RED),("A flat network",2),("Split it into floors",3,CY)],
  "Picture one giant open-plan office. Every announcement reaches every desk. That's a flat network. Let's split it into floors, using something called a V L A N."),
 story("The apartment building", "Think of an apartment building with one hundred flats. Each floor is its own V L A N. Mail only gets delivered to flats on the same floor. The sticker on each letter says which floor it belongs to. A flat's front door only belongs to one floor, and that's an access port. The shared stairwell that carries every floor is called a trunk.",
  [("building","Each floor","A VLAN",1),("envelope","Mail stays on the floor","Separate broadcast domain",2),("list","Floor sticker on a letter","802.1Q tag",3),("door","A flat's front door","Access port (one VLAN)",4),("road","The shared stairwell","Trunk (many VLANs)",5)]),
 flow("Setting one up", "Setting one up takes three steps. First, create the V L A N on the switch. Second, put the port in access mode. Third, assign that port to the V L A N. Then check your work.",
  [("building","Create the VLAN","vlan 10 and give it a name",1),("door","Access mode","switchport mode access",2),("key","Assign the port","switchport access vlan 10",3),("list","Verify","show vlan brief",4)]),
 traps("Three mix-ups catch people out. A V L A N is a Layer two idea, not Layer three. A trunk port carries lots of floors at once, not just one. And the native V L A N doesn't have to be number one. Pick an unused one for safety.",
  [("A VLAN is a Layer 3 concept","It's Layer 2; subnets just map onto it",1),("A trunk carries only one VLAN","It carries many, tagged with 802.1Q",2),("Native VLAN must be VLAN 1","Any VLAN works; use an unused one",3)]),
 rc("VLAN", [("A V L A N splits one switch into separate floors.","A VLAN splits one switch into separate floors"),("Access ports belong to one floor, and trunks carry many.","Access ports: one VLAN. Trunks: many"),("And create the V L A N before you assign ports to it.","Create the VLAN before assigning ports")]),
])

save("trunking", "Trunking and 802.1Q", "Trunking", [
 hook("link", [("Two switches",0),("Ten floors",1),("One cable",2,RED),("Colour stickers to the rescue",3,CY)],
  "Two switches. Ten different floors. Just one cable between them. So how does the mail avoid getting mixed up?"),
 story("The colour-coded mailroom", "Picture a mail carrier delivering letters for every floor of a building. Each letter gets a coloured sticker saying which floor it belongs to. That sticker is a small tag defined by the standard called eight oh two dot one Q. The cable between the two mailrooms is the trunk. Letters for the default floor travel with no sticker at all. That default floor is the native V L A N.",
  [("envelope","A sticker on each letter","VLAN tag (4 bytes)",1),("stamp","The sticker standard","802.1Q",2),("road","Cable between mailrooms","Trunk link",3),("door","Letters with no sticker","Native VLAN",5)]),
 term("Trunk commands", "The commands are short. Force the port to be a trunk. Limit which floors are allowed through. And check the result with show interfaces trunk.",
  [("switchport mode trunk","Force this port to trunk",1),("switchport trunk allowed vlan 10,20","Only these VLANs cross the link",2),("show interfaces trunk","Status, native VLAN, allowed VLANs",3,CY)]),
 traps("Watch for three slip-ups. Frames on the native V L A N travel untagged. Both ends must agree on the native V L A N, or traffic leaks. And two ports set to dynamic auto will never form a trunk.",
  [("Every frame on a trunk is tagged","Native VLAN frames are untagged",1),("Native VLAN can differ per side","Both ends must match or traffic leaks",2),("Two dynamic auto ports make a trunk","One side must be trunk or desirable",3)]),
 rc("trunking", [("A trunk carries many V L A N over one cable, using little tags.","A trunk carries many VLANs using 802.1Q tags"),("The native V L A N goes untagged, and both ends must match.","Native VLAN: untagged, must match"),("And never rely on dynamic auto at both ends.","Never dynamic auto on both ends")]),
])

save("inter-vlan-routing", "Inter-VLAN Routing", "Inter-VLAN routing", [
 hook("building", [("Each floor keeps to itself",0),("Sales → Engineering?",1,OR),("It needs an elevator",2,CY)],
  "Each floor of the building keeps to itself, and that's on purpose. So how does Sales send a file to Engineering? It needs an elevator."),
 story("Floors and elevators", "Each floor is a V L A N, and people move freely inside it. To go between floors, you need a router, which is the elevator. A router on a stick is one elevator with a single door onto the shared stairwell. It works, but a crowd queues up. A Layer three switch is a whole bank of fast elevators. Each floor's button is a virtual interface called an S V I.",
  [("router","The elevator","Router (the gateway)",1),("road","One elevator, one door","Router on a stick",2),("switch","A bank of elevators","Layer 3 switch",4),("door","Each floor's button","SVI",5)]),
 versus("Two ways to route", "Router on a stick", "Layer 3 switch", "Here's how the two approaches compare. Router on a stick uses one cable, split into sub interfaces. A Layer three switch uses S V Is and routes at wire speed. Pick the switch when speed matters.",
  [("How it's built","One cable + subinterfaces","SVIs inside the switch",1),("Speed","Can become a bottleneck","Wire speed",2),("Needs","A trunk to the router","ip routing turned on",3)]),
 traps("Three common slip-ups. The switch port facing the router must be a trunk for router on a stick. A Layer three switch won't route until you turn on I P routing. And an S V I stays down unless a port in that V L A N is up.",
  [("Any switch port will do for the router","It must be a trunk",1),("SVIs route out of the box","You must enter: ip routing",2),("An SVI is always up","Only if a port in that VLAN is up",3)]),
 rc("inter-VLAN routing", [("Every V L A N needs a gateway, and that's a router or a Layer three switch.","Each VLAN needs a router as its gateway"),("Router on a stick means sub interfaces on a trunk.","Router on a stick = subinterfaces on a trunk"),("Layer three switches use S V Is, and need I P routing turned on.","Layer 3 switch = SVIs + ip routing")]),
])

save("etherchannel", "EtherChannel", "EtherChannel", [
 hook("link", [("Four cables between two switches",0),("Only one carries traffic",1,RED),("The rest are switched off",2),("What a waste",3,CY)],
  "Four cables between two switches. But only one actually carries traffic. The rest are switched off to avoid a loop. What a waste."),
 story("Merging the tollbooths", "Imagine four tollbooths into the same city. Spanning tree closes three of them to stop loops. EtherChannel merges all four into one super booth with four lanes. To the rest of the network, it looks like a single link. Cars are assigned a lane by a hash of who they are and where they're going. So one conversation always stays in one lane, and nothing arrives out of order.",
  [("lock","Booths closed to stop loops","Spanning tree blocking",1),("road","One super booth","EtherChannel (port-channel)",2),("scale","Lane picked by a hash","Load balancing per flow",4),("list","Same trip, same lane","No out-of-order frames",5)]),
 versus("Negotiating the bundle", "LACP (open standard)", "PAgP (Cisco)", "There are two ways to negotiate a bundle. L A C P is the open standard, with modes active and passive. Cisco has its own version, with modes desirable and auto. You can also force it with mode on, but nothing checks the other side.",
  [("Standard","Open (IEEE 802.3ad)","Cisco only",1),("Modes","active / passive","desirable / auto",2),("No negotiation","mode on","mode on",3)]),
 traps("Three things to watch. Traffic isn't shared packet by packet. It's hashed per flow. Two active L A C P ports do form a bundle. And every link in the bundle must match on speed and duplex.",
  [("Traffic is shared packet by packet","A hash keeps each flow on one link",1),("LACP active needs passive on the other end","Active with active works fine",2),("You can mix 1G and 10G links","Speed and duplex must match",3)]),
 rc("EtherChannel", [("EtherChannel bundles several links into one, for more speed and backup.","Several links bundled into one"),("L A C P is the standard, and active on both ends works well.","LACP: use active on both ends"),("Spanning tree sees one link, so nothing gets blocked.","STP sees one link, nothing is blocked")]),
])

save("rstp", "Rapid Spanning Tree", "Rapid STP", [
 hook("clock", [("Classic STP: up to 50 seconds",0,RED),("That's a long time with no network",1),("Rapid STP: about 6",2,CY),("Here's how",3)],
  "Classic spanning tree can take fifty seconds to recover. That's a long time with no network. Rapid S T P does it in about six. Here's how."),
 story("Fire doors that pop open", "Classic spanning tree is a fire marshal who waits twenty seconds before unlocking any door. Rapid S T P is a building where every floor manager talks to their neighbours constantly. If a door fails, a neighbour just agrees to open its own straight away. That quick chat is called proposal and agreement. Doors to end devices open instantly, because they're edge ports.",
  [("clock","A marshal waits 20 seconds","Classic STP timers",0),("people","Managers talk constantly","BPDUs on every port",1),("list","The quick chat","Proposal and agreement",3),("door","Doors to end devices","Edge ports (PortFast)",4)]),
 versus("Port states and roles", "Classic STP", "Rapid STP", "The port states got simpler. Classic has four working states, and Rapid has just three. The roles also changed, because Rapid adds alternate and backup ports. Both are ready to take over the moment something fails.",
  [("Port states","Blocking, Listening, Learning, Forwarding","Discarding, Learning, Forwarding",1),("Extra roles","None","Alternate and Backup",2),("Recovery","30 to 50 seconds","About 6 seconds or less",3)]),
 traps("Three mix-ups. Rapid S T P has three states, not five. An alternate port backs up the root port, while a backup port backs up a designated port. And on shared half duplex links, it falls back to slow timers.",
  [("RSTP has five port states","Just three: Discarding, Learning, Forwarding",1),("Alternate backs up a designated port","Alternate backs up the root port",2),("RSTP is always fast","Only on full-duplex, point-to-point links",3)]),
 rc("Rapid STP", [("Rapid S T P recovers in seconds, using handshakes instead of timers.","Handshakes instead of timers"),("It has three states and four roles.","3 states, 4 roles"),("And Cisco's Rapid P V S T plus runs one copy per V L A N.","Rapid PVST+ runs one instance per VLAN")]),
])

save("port-security", "Port Security", "Port security", [
 hook("lock", [("Any laptop, any spare wall port",0,OR),("Instantly on your network",1,RED),("Port security is the guard on the door",2,CY)],
  "Anyone can plug a laptop into a spare wall port. And just like that, they're on your network. Port security is the guard on the door."),
 story("The security guard", "Think of an apartment where a guard checks every visitor. The guard knows the allowed devices by their M A C address. By default, only one device per port is allowed. Sticky learning means the guard memorises the first visitor. But the guard's notebook is only kept if you save the config.",
  [("shield","The guard","Port security",0),("key","A visitor's ID card","MAC address",1),("people","One visitor per door","Maximum: 1 (default)",2),("book","Guard memorises the first","Sticky MAC address",3),("list","Notebook not saved","Running config only",4)]),
 flow("Three responses", "When an unknown device shows up, you choose the response. Protect silently drops the frames. Restrict drops them and logs a warning. Shutdown, the default, locks the door completely.",
  [("shield","Protect","Drops quietly, no log",1),("bell","Restrict","Drops and logs",2),("lock","Shutdown (default)","Port goes err-disabled",3)]),
 term("The configuration", "Here's the config. Turn it on for the port. Set how many devices are allowed. Choose what happens on a violation. And verify with show port security.",
  [("switchport port-security","Enable on the interface",1),("switchport port-security maximum 2","Allow two devices",2),("switchport port-security violation restrict","Choose the response",3),("show port-security interface","Check the result",4,CY)]),
 traps("Three slip-ups. Protect mode doesn't send any log message. Sticky addresses aren't saved until you save the config. And the default maximum is one address, not zero.",
  [("Protect mode sends a syslog message","Only restrict and shutdown log",1),("Sticky MACs are saved automatically","Save the running config yourself",2),("Default maximum is zero","The default maximum is one",3)]),
 rc("port security", [("Port security limits which devices can use a port.","Limits which devices may use a port"),("The default is one device, and the default response is shutdown.","Default: 1 device, shutdown"),("Sticky addresses need saving to survive a reboot.","Sticky MACs: save the config")]),
])

save("mac-address-table", "The MAC Address Table", "MAC address table", [
 hook("book", [("Which cable leads where?",0),("Nobody tells the switch",1,OR),("It watches and takes notes",2,CY)],
  "How does a switch know which cable leads to which computer? Nobody tells it. It simply watches and takes notes."),
 story("The hotel guest directory", "You're the front desk clerk at a big hotel. Every time a guest sends something, you note their name and room number. That's the switch learning the source M A C address. When a delivery arrives for a known guest, you send it straight to the room. For an unknown guest, you page every room, which is called flooding. Entries expire after five minutes without activity.",
  [("book","Name and room number","MAC address + port",2),("door","Straight to the room","Forward",3),("bell","Page every room","Flood unknown unicast",4),("clock","Entry expires","Aging time: 300 seconds",5)]),
 flow("Three decisions", "For every frame, the switch makes one of three decisions. Forward: the guest is in a different room, so send it there. Filter: the guest is on the same port, so drop it. Flood: nobody knows this guest, so send it everywhere else.",
  [("door","Forward","Known MAC, different port",1),("lock","Filter","Known MAC, same port",2),("bell","Flood","Unknown or broadcast",3)]),
 traps("Three mix-ups. A switch learns from the source address, not the destination. It doesn't flood everything just because the table is empty. And static entries never age out.",
  [("Learns from the destination MAC","It learns from the source MAC",1),("Empty table = flood every frame","Only unknown unicast and broadcast flood",2),("Static entries age out too","Only dynamic entries age out",3)]),
 rc("MAC table", [("A switch learns the source M A C address of every frame it sees.","Learns from the source MAC"),("Then it forwards, filters or floods.","Forward, filter or flood"),("And show M A C address table lets you look inside.","show mac address-table")]),
])

save("ipv4-addressing", "IPv4 Addressing", "IPv4 addressing", [
 hook("map", [("Every device needs an address",0),("Four numbers and three dots",1,CY),("Let's decode one",2)],
  "Every device on a network needs an address, just like a house needs a street address. An I P version four address is just four numbers with dots between them. Let's decode one."),
 story("Street addresses", "An I P address has two parts, like a street address. The first part is the street name, which is the network. The second part is the house number, which is the host. The first number on the street is the name of the street itself, the network address. The last number is the shout to everyone, the broadcast address. Everything in between belongs to real houses.",
  [("map","Street name","Network portion",1),("building","House number","Host portion",2),("list","First number on the street","Network address",3),("bell","Last number: shout to all","Broadcast address",4),("people","Houses in between","Usable hosts",5)]),
 term("The old classes", "Early on, addresses came in sizes called classes. Class A starts with one to one twenty-six, and has millions of hosts. Class B starts with one twenty-eight to one ninety-one. Class C starts with one ninety-two to two twenty-three, and has two fifty-four hosts. And three private ranges are kept for use inside your own network.",
  [("Class A   1 – 126   /8","About 16 million hosts",1),("Class B   128 – 191   /16","About 65 thousand hosts",2),("Class C   192 – 223   /24","254 hosts",3),("Private: 10.x  172.16.x  192.168.x","Never routed on the internet",4,OR)]),
 traps("Three easy mistakes. One twenty-seven is loopback, not a usable class A network. A class B network uses slash sixteen, not slash twenty-four. And private addresses never travel across the public internet.",
  [("127.x.x.x is a normal Class A network","It's reserved for loopback",1),("Class B default mask is /24","Class B is /16; /24 is Class C",2),("Private addresses route on the internet","Routers drop them",3)]),
 rc("IPv4 addressing", [("An I P version four address is thirty-two bits, split into network and host.","32 bits: network + host"),("Usable hosts equal two to the power of the host bits, minus two.","Hosts = 2^(host bits) − 2"),("And remember the three private ranges.","10.x, 172.16–31.x, 192.168.x are private")]),
])

save("ipv6-addressing", "IPv6 Addressing", "IPv6 addressing", [
 hook("question", [("IPv4 ran out",0,RED),("IPv6 has 340 undecillion",1),("Different kinds, easy to mix up",2,CY)],
  "The internet ran out of version four addresses. I P version six has three hundred and forty undecillion of them. But there are different kinds, and they're easy to mix up."),
 story("Different kinds of address", "Picture one person with several addresses. Their worldwide street address works from anywhere, and it starts with two or three. Their internal company address only works inside the business, and it starts with F C or F D. Their hallway slot number only works on the same floor, and it starts with F E. And announcements to a group use multicast, which starts with F F. There's no broadcast in version six at all.",
  [("map","Worldwide street address","Global unicast: 2000::/3",1),("building","Internal company address","Unique local: FC00::/7",2),("door","Hallway slot number","Link-local: FE80::/10",3),("bell","A group announcement","Multicast: FF00::/8",4)]),
 traps("Three things to remember. Link-local addresses are never routed beyond their own link. Multicast isn't broadcast by another name, because only group members listen. And anycast isn't its own prefix. It's a normal address shared by several devices.",
  [("Link-local can be routed inside a site","Link-local is never routed",1),("Multicast is broadcast by another name","Only group members receive it",2),("Anycast has its own prefix","A normal address shared by many",3)]),
 rc("IPv6 addressing", [("Global addresses start with two or three, and work everywhere.","Global unicast: starts with 2 or 3"),("Link-local addresses start with F E, and never leave the link.","Link-local: FE80, never routed"),("And there's no broadcast, only multicast.","No broadcast, only multicast")]),
])

save("nat-concepts", "NAT and PAT", "NAT and PAT", [
 hook("envelope", [("One public address",0),("Hundreds of people online",1,OR),("Meet the mail room clerk",2,CY)],
  "Your whole office shares one public address, yet everyone browses the web. So how does a reply find the right person? Meet the mail room clerk."),
 story("The mail room clerk", "A building with a thousand residents has one street address. The clerk logs each outgoing package with the resident's flat number and a package number. Then the clerk relabels it with the building's address and a new number. When the reply comes back, the clerk checks the log and sends it to the right flat. That log is the N A T table.",
  [("envelope","Relabel with building address","Private IP → public IP",2),("door","Reply goes to the right flat","Port number finds the host",3),("book","The clerk's log","NAT table",4)]),
 flow("Three types of NAT", "There are three flavours of N A T. Static is a permanent one to one swap. Dynamic borrows an address from a pool, one to one. And P A T, also called overload, shares one address between many hosts, using port numbers.",
  [("lock","Static","One private = one public, permanent",1),("list","Dynamic","One to one, from a pool",2),("people","PAT (overload)","Many hosts, one address",3)]),
 term("PAT in a few lines", "Here's the P A T setup. Mark which interface faces inside. And which faces outside. Match your private hosts with an access list. Then overload the outside interface. Check it with show I P nat translations.",
  [("ip nat inside","On the LAN interface",1),("ip nat outside","On the internet interface",2),("access-list 1 permit 192.168.1.0 0.0.0.255","Who may be translated",3),("ip nat inside source list 1 interface g0/1 overload","The PAT rule",4),("show ip nat translations","See the active log",5,CY)]),
 traps("Three slip-ups. P A T and dynamic N A T aren't the same thing. The access list matches your private addresses, not the public ones. And static N A T never times out.",
  [("PAT and dynamic NAT are the same","PAT shares one address using ports",1),("The ACL matches public addresses","It matches the private (inside) ones",2),("Static NAT times out","It stays until you remove it",3)]),
 rc("NAT", [("N A T swaps private addresses for public ones.","NAT swaps private for public addresses"),("P A T lets many hosts share one public address, using port numbers.","PAT: many hosts, one address, using ports"),("And the N A T table is how replies find their way back.","The NAT table sends replies home")]),
])
