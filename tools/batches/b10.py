import sys; sys.path.insert(0, "tools")
from mk import *

save("junos-overview", "Junos OS Overview", "Junos overview", [
 H("router", [("One OS, every device","Juniper has one operating system for every router, switch and firewall."),("Called Junos","It's called Junos."),("Built differently","And it's built in a clever, careful way.",CY)]),
 S("The office building","Think of a big office building. The concrete and steel are one thing, and the rules and security passes are another.",
   [("building","You can renovate a floor without shutting the building.","Control and forwarding are separate","Two planes"),
    ("gear","The management office makes the decisions.","The Routing Engine","Control plane: routing protocols"),
    ("router","The lifts and corridors move people fast.","The Packet Forwarding Engine","Forwarding plane: fast packets")]),
 T("Safe changes","Junos protects you from mistakes. Changes go into a draft first, called the candidate. Nothing is live until you commit. And if it goes wrong, you can roll back.",
   [("set ... (edit candidate)","Draft only, nothing live","First, you edit the draft candidate.",None),("commit","Make the draft live","Then commit makes it live.",None),("rollback 1","Go back one version","And rollback takes you to an earlier version.",CY)]),
 TR("Three things catch people out.",
   [("Junos is like Windows","It's a purpose-built OS based on FreeBSD","Junos is not like Windows, it's a purpose built system based on FreeBSD."),
    ("Every vendor splits control and forwarding","Not all do; Juniper does it by design","Not every vendor separates control from forwarding, but Juniper does."),
    ("A set command takes effect immediately","Only after commit","And a change only takes effect after you commit.")]),
 rc("Junos", [("Junos is one operating system for all Juniper devices.","One OS for all Juniper devices"),("The control plane and forwarding plane are separate.","Control plane and forwarding plane are separate"),("And nothing goes live until you commit.","Nothing goes live until commit")]),
])

save("junos-cli", "The Junos CLI", "Junos CLI", [
 H("book", [("Two menus","A Junos device gives you two menus."),("Customers and kitchen","One is for looking, and one is for changing.",CY),("Know which one you're in","The prompt tells you which is which.",OR)]),
 S("The restaurant and kitchen","Think of a restaurant. Customers read one menu, and the kitchen staff use another.",
   [("book","In the dining room, you can only look.","Operational mode","Prompt ends in >"),
    ("wrench","In the kitchen, you can change things.","Configuration mode","Prompt ends in #"),
    ("door","To walk into the kitchen, you type configure.","configure","Switch from > to #")]),
 T("Moving around","Here are the key commands. Configure takes you into the kitchen. Commit check tests your draft without serving it. Commit serves it. And rollback zero throws away unsaved changes.",
   [("configure","Enter configuration mode","Configure takes you into configuration mode.",None),("commit check","Test the draft safely","Commit check validates the draft without applying it.",None),("commit","Make it live","Commit applies it.",None),("rollback 0","Discard uncommitted changes","And rollback zero discards everything you haven't committed.",CY)]),
 TR("Here are three common mix-ups.",
   [("Any command works in any mode","Modes are strictly separate","Commands only work in the right mode."),
    ("configure applies changes at once","It only opens the draft","Typing configure does not apply anything."),
    ("exit discards changes automatically","It asks you first","And exit does not silently discard changes, it asks you.")]),
 rc("Junos CLI", [("The prompt tells you the mode. Greater than means operational, and hash means configuration.","> is operational, # is configuration"),("Nothing is live until you commit.","Nothing is live until commit"),("And rollback zero discards uncommitted changes.","rollback 0 discards uncommitted changes")]),
])

save("junos-config", "Junos Configuration Basics", "Junos configuration", [
 H("list", [("Everything has one place","In Junos, every setting has exactly one place to live."),("A tree, not a list","The configuration is a tree.",CY),("Follow the branches","So you follow the branches, you never guess.",OR)]),
 S("The menu with pages","Think of a restaurant menu with different pages for starters, mains and drinks. You write your order, and only then does the kitchen start cooking.",
   [("book","Each page is a section of the tree.","Hierarchy","Interfaces, protocols, system"),
    ("list","You write your order on a slip.","Candidate configuration","Edits go here first"),
    ("stamp","Handing it to the chef starts the cooking.","commit","Makes it active"),
    ("clock","The chef keeps the last fifty orders.","Rollback history","Last 50 commits")]),
 T("A deep example","Here's how deep the tree can go. This one line sets an address five levels down. Then you check it, commit it, and keep a note for the team.",
   [("set interfaces ge-0/0/0 unit 0 family inet address 192.168.1.1/24","Five levels deep","Here's one line five levels deep.",None),("commit check","Validate first","Check it first.",None),("commit comment \"add uplink\"","Go live, with a note","Then commit it with a note.",CY)]),
 TR("Three things to remember.",
   [("A set command applies at once","Only after commit","A set command doesn't apply until you commit."),
    ("rollback 0 undoes the last commit","It resets the draft to the last commit","Rollback zero doesn't undo a commit, it resets your draft to match the last commit."),
    ("Only one level under each section","It goes many levels deep","And the tree goes many levels deep.")]),
 rc("Junos configuration", [("The configuration is a tree, and every setting has one place.","A tree: every setting has one place"),("Edits go in a draft, and only commit makes them live.","Draft first; commit makes it live"),("Junos keeps the last fifty commits for rollback.","Last 50 commits kept")]),
])

save("junos-files-upgrades", "Junos Files and Upgrades", "Junos upgrades", [
 H("box", [("Upgrading a router","Upgrading a router sounds scary."),("Junos makes it safer","Junos makes it much safer.",CY),("It keeps the old version","Because it keeps a spare copy of the old software.",OR)]),
 S("Moving house","Imagine moving house, and keeping everything safe in labelled boxes. Your old home stays available until you're sure the new one is fine.",
   [("box","Boxes hold your files and images.","Directories like /var/tmp","Survives reboots"),
    ("building","There are two homes, current and backup.","Dual partitions","Old version is the fallback"),
    ("key","Moving in doesn't happen until you decide.","request system software add","Installs, does not reboot")]),
 F("The upgrade path","Here's the safe upgrade path. Copy the image over. Validate it. Install it. Then reboot when you're ready.",
   [("box","Copy the new image over.","file copy","Use FTP, SCP or HTTP"),("shield","Check it's good.","Validate the image","request system software validate"),("gear","Install it into the backup side.","Install","request system software add"),("clock","Restart when you choose.","Reboot","request system reboot")]),
 TR("Three misunderstandings.",
   [("Upgrading deletes your config","Config and logs stay untouched","An upgrade doesn't delete your configuration or logs."),
    ("software add restarts the router","A separate reboot is needed","The add command doesn't reboot anything."),
    ("Delete the old version straight away","Wait a few days as a fallback","And don't delete the old version straight away, it's your fallback.")]),
 rc("Junos upgrade", [("Junos keeps two software partitions, current and backup.","Two partitions: current and backup"),("Validate, add, then reboot when ready.","Validate, add, then reboot"),("And keep the old version for a few days.","Keep the old version for a few days")]),
])

save("junos-interfaces", "Junos Interfaces", "Junos interfaces", [
 H("link", [("One port, many identities","One physical port can carry many separate networks."),("Physical and logical","Junos splits every interface into two parts.",CY),("Let's decode the name","Let's decode the name.",OR)]),
 S("The letterbox with slots","Picture one letterbox at the door with several slots inside, one for each department. The box is the hardware, and each slot is its own compartment.",
   [("box","The letterbox itself is the physical interface.","Physical interface","ge-0/0/0"),
    ("door","Each slot is a logical unit.","Logical unit","ge-0/0/0 unit 10"),
    ("map","The address goes on the slot, never the box.","IP goes on the unit","family inet address")]),
 V("Special interfaces","Loopback (lo0)","Aggregated (ae)","Two special interfaces are worth knowing. The loopback is always up, so it's ideal for router I Ds. And an aggregated interface bundles several ports into one, using L A C P.",
   [("Always up","Yes, no cable needed","Only while members are up","The loopback needs no cable."),("Used for","Router ID, management","More bandwidth, backup","Aggregated links add bandwidth and backup."),("IP address goes on","The lo0 unit","The ae unit, not members","Only the ae interface gets the address.")]),
 TR("Three common traps.",
   [("Logical units stand alone","Always tied to a physical port","A logical unit always belongs to a physical port."),
    ("Put the IP on the physical port","Put it on a logical unit","The address goes on a unit, never the bare port."),
    ("Every ae member needs the same IP","Only ae0 gets an IP","And only the aggregate gets an address, not its members.")]),
 rc("Junos interfaces", [("Names follow type, then F P C, P I C and port, then the unit.","Name: type-fpc/pic/port.unit"),("The address goes on the logical unit.","IP goes on the unit"),("Loopback is always up, and ae bundles links.","lo0 always up; ae bundles links")]),
])

save("junos-ospf", "OSPF on Junos", "Junos OSPF", [
 H("map", [("Routers that learn on their own","Dynamic routing means routers learn paths without you typing them."),("O S P F does that","O S P F is one of the best known.",CY),("Here it is on Junos","Let's see how Junos does it.",OR)]),
 S("The sorting hub","Imagine a regional post office hub manager. They don't drive every van, but they know the map of how mail flows between hubs.",
   [("map","The manager knows every hub in the region.","Same area","Routers in an area share one map"),
    ("handshake" if False else "people","Hubs must agree on the basics to cooperate.","Neighbours","Same area, subnet and hello timers"),
    ("ruler","The faster the road, the cheaper the trip.","Cost","Based on bandwidth, not hops")]),
 T("Turning it on","The command is short. Put an interface into an area. Then check the neighbour state, and look at the routes you learned.",
   [("set protocols ospf area 0 interface ge-0/0/0.0","Add the interface to area 0","Put the interface into an area.",None),("show ospf neighbor","Look for state Full","Check the neighbour, and look for Full.",None),("show route protocol ospf","See learned routes","Then see what routes you learned.",CY)]),
 TR("Here are three mix-ups.",
   [("OSPF replaces the need for an IP address","It needs a valid IP on the interface","O S P F still needs an I P address on the interface."),
    ("OSPF learns every route in the world","Only routes advertised in its area","It only learns routes advertised by other O S P F routers."),
    ("Cost is the hop count","Cost comes from bandwidth","And cost comes from bandwidth, not hops.")]),
 rc("Junos OSPF", [("Add each interface to an area under protocols O S P F.","set protocols ospf area N interface X"),("Neighbours must match on area, subnet and timers.","Neighbours must match: area, subnet, timers"),("Check for the Full state with show O S P F neighbor.","show ospf neighbor: look for Full")]),
])

save("junos-static-routing", "Static Routing on Junos", "Junos static routes", [
 H("map", [("A brand new estate","Imagine moving into a brand new housing estate."),("Your sat nav doesn't know it","Your sat nav doesn't know the roads yet.",OR),("You draw the map yourself","So you draw the map by hand.",CY)]),
 S("The hand-drawn map","A static route is a hand drawn map. You tell the router exactly where to send traffic, and it never changes unless you change it.",
   [("map","You need a destination and a next hop.","Prefix plus next hop","Both are required"),
    ("road","The catch-all road is the default route.","0.0.0.0/0","Used when nothing else matches"),
    ("scale","If two maps disagree, the lower number wins.","Preference","Static default is 5")]),
 T("In Junos","Here's the syntax. A static route needs a prefix and a next hop. The default route uses zero slash zero. And you can add a higher preference to make it a backup.",
   [("set routing-options static route 10.0.0.0/8 next-hop 192.168.1.2","A normal static route","Here's a normal static route.",None),("set routing-options static route 0.0.0.0/0 next-hop 192.168.1.1","The default route","This is the default route.",None),("... preference 200","A backup route","And a higher preference makes it a backup.",CY)]),
 TR("Three traps.",
   [("Static routes fail over by themselves","Only if the interface goes down","A static route doesn't switch to a backup unless you configure one."),
    ("The default route beats everything","It's the least specific, so it loses","The default route is the last resort, because the most specific match wins."),
    ("The next hop is optional","You need a next hop or interface","And every static route needs a next hop.")]),
 rc("Junos static routing", [("A static route is a hand drawn map.","A static route is a hand-drawn map"),("The default route is the last resort.","Default route = last resort"),("Lower preference wins, and static defaults to five.","Lower preference wins; static default is 5")]),
])

save("junos-policy-filters", "Routing Policy and Firewall Filters", "Junos policy and filters", [
 H("shield", [("Two kinds of checkpoint","Junos has two kinds of checkpoint."),("One checks passengers","One checks the packets.",CY),("One checks the flights","The other checks the routes.",OR)]),
 S("Airport security and customs","At an airport, security screens the passengers, and customs checks the paperwork. Both follow a list of rules, from the top down.",
   [("shield","Screening checks every passenger.","Firewall filter","Works on packets"),
    ("map","Customs checks the flight list.","Routing policy","Works on routes"),
    ("list","Both use terms with from and then.","Terms","Evaluated top to bottom")]),
 V("What can they do","Firewall filter","Routing policy","Each one has its own set of actions. A filter can accept, discard, reject or log a packet. A policy can accept or reject a route, and also change its attributes.",
   [("Acts on","Packets","Routes","A filter handles packets, and a policy handles routes."),("Can modify","No, only pass or drop","Yes, route attributes","Only a policy can change a route's attributes."),("Apply point","On an interface","Import or export","And a policy applies on import or export.")]),
 TR("Three misunderstandings.",
   [("Filters and policies are the same","One acts on packets, one on routes","They're different, one works on packets and the other on routes."),
    ("Reject deletes the route","It just stops it being used","A reject stops the route being used, it doesn't wipe it from every table."),
    ("By default Junos blocks everything","By default it accepts","By default Junos allows traffic unless you apply a filter.")]),
 rc("Junos policy", [("Filters check packets, and policies check routes.","Filters: packets. Policies: routes"),("Both read terms from the top, first match wins.","Both are term-based, top-down"),("Reject sends a message back, and discard stays silent.","reject tells the sender; discard is silent")]),
])

save("junos-nat", "NAT on Junos", "Junos NAT", [
 H("envelope", [("Private addresses can't reach the internet","Private addresses can't travel across the internet."),("NAT fixes that","N A T fixes that.",CY),("But there's a catch","But on Junos, there's a catch.",OR)]),
 S("The visitor parking pass","Imagine an apartment block that only lets resident cars into the lot. A visitor's van is turned away until it's given a pass.",
   [("key","The pass swaps a private plate for a public one.","Source NAT","Outbound: private to public"),
    ("door","Visitors arriving get sent to the right flat.","Destination NAT","Inbound: public to private server"),
    ("lock","A permanent reserved space is another option.","Static NAT","Fixed one-to-one mapping")]),
 F("Two parts to every setup","On Junos, you always need two parts. The N A T rule changes the address. And a security policy allows the traffic. Without both, nothing flows.",
   [("key","Write the NAT rule.","NAT rule","Rewrites the address"),("shield","Add a security policy.","Security policy","Actually permits the traffic"),("list","Check it worked.","Verify","show security nat source")]),
 TR("Three traps to avoid.",
   [("Every device needs its own public IP","One public address can serve thousands","One public address can serve thousands of devices with source N A T."),
    ("Destination NAT and static NAT are identical","Destination is often per-port; static is one-to-one","Destination N A T and static N A T are not the same thing."),
    ("A NAT rule lets traffic through","You still need a security policy","And a N A T rule doesn't permit traffic, you still need a policy.")]),
 rc("Junos NAT", [("Source N A T rewrites outbound traffic, and destination N A T rewrites inbound.","Source = outbound, destination = inbound"),("Static N A T is a permanent one to one mapping.","Static = permanent one-to-one"),("A N A T rule needs a matching security policy.","NAT rule needs a security policy")]),
])

save("junos-security", "Security Zones and Policies", "Junos security", [
 H("shield", [("A firewall with floors","A Junos firewall divides your network into zones."),("Like floors in a building","Think of them as floors in an office building.",CY),("With a guard between them","And a security guard between each floor.",OR)]),
 S("The security desk","The lobby is public, the second floor is sales, and the server room is high security. The guard controls who moves between them.",
   [("building","Each floor is a zone.","Security zone","Interfaces belong to zones"),
    ("people","Moving within a floor is allowed.","Intra-zone","Permitted by default"),
    ("lock","Moving between floors needs a policy.","Inter-zone","Denied by default")]),
 T("A policy","A policy names a source zone, a destination zone, and the action. The first matching policy wins. And if nothing matches, the traffic is denied.",
   [("from-zone trust to-zone untrust","Where it's going","A policy names the two zones.",None),("match source-address any","What it matches","Then what it matches.",None),("then permit","The action","And the action to take.",CY)]),
 TR("Three misunderstandings.",
   [("Intra-zone traffic is blocked","It's permitted by default","Traffic inside a zone is allowed by default."),
    ("Policies attach to interfaces","They attach to zones","Policies reference zones, not interfaces."),
    ("No match means permit","No match means deny","And if nothing matches, the traffic is denied.")]),
 rc("Junos security", [("Interfaces belong to zones, and one interface lives in one zone.","One interface, one zone"),("Between zones is denied by default, and inside a zone is allowed.","Inter-zone denied; intra-zone allowed"),("Policies are checked top down, first match wins.","Policies: top-down, first match")]),
])

save("junos-stp", "Spanning Tree on Junos", "Junos STP", [
 H("tree", [("Extra exits are useful","A department store adds a second emergency exit."),("But extra paths cause loops","Extra paths in a network can cause loops.",RED),("S T P keeps them safe","Spanning tree keeps them safe.",CY)]),
 S("The escape routes","Shoppers can use any exit, but if every exit stays open, a crowd can circle forever. So some exits stay closed until they're needed.",
   [("tree","One switch is chosen as the boss.","Root bridge","Lowest priority, then lowest MAC"),
    ("lock","Backup exits stay closed.","Blocked ports","Alternate and backup ports"),
    ("clock","The old way is slow to reopen.","STP","30 to 50 seconds"),
    ("wifi","The new way is quick.","RSTP","One to two seconds")]),
 V("STP vs RSTP","Classic STP (802.1D)","RSTP (802.1w)","The two differ in speed and states. Classic S T P has five port states. R S T P has three, and recovers in seconds. And on Juniper E X switches, R S T P is the default.",
   [("Port states","Five","Three","STP has five states, and RSTP has three."),("Recovery","30 to 50 seconds","1 to 2 seconds","RSTP recovers in just a second or two."),("On Juniper EX","Not default","Default: rstp","And it's the default on E X switches.")]),
 TR("Three misconceptions.",
   [("STP and RSTP are the same","Different standards, different speed","They're different standards, not a rebrand."),
    ("Every port always forwards","Alternates and backups are blocked","In a stable network, some ports stay blocked."),
    ("The root is the most central switch","It's the lowest priority, then lowest MAC","And the root is chosen by priority and M A C, not location.")]),
 rc("Junos STP", [("Spanning tree blocks extra paths to stop loops.","STP blocks extra paths to stop loops"),("R S T P is faster, with three states.","RSTP: faster, three states"),("Check it with show spanning tree.","show spanning-tree")]),
])

save("junos-monitoring", "Junos Monitoring", "Junos monitoring", [
 H("bell", [("Your router is trying to tell you something","Your router is always trying to tell you something."),("Like a house alarm","It works like a house alarm.",CY),("You just have to listen","You just have to know where to look.",OR)]),
 S("The house alarm","The alarm panel has a timeline of everything that happened, even while you were away.",
   [("bell","The timeline is the log.","/var/log/messages","General system events"),
    ("gear","Each sensor has its own report.","Other logs","chassisd, auth, interactive-commands"),
    ("clock","Severity runs from zero to seven.","Syslog levels","0 to 3 are serious")]),
 T("Checking health","Three commands cover most checks. Look at the hardware, look at the logs, and reboot only when you must.",
   [("show chassis environment","Temperature, fans, power","Check temperature, fans and power.",None),("show log messages","Main system log","Read the main log.",None),("request system reboot","Graceful restart","And only then, reboot gracefully.",CY)]),
 TR("Three misunderstandings.",
   [("show system health shows per-process CPU","Use show system processes extensive","For per process detail, use show system processes extensive."),
    ("messages is the only log that matters","There are many logs","There are many logs, each with a purpose."),
    ("A reboot is always the same","Graceful versus forced","And a graceful reboot is different from a forced one.")]),
 rc("Junos monitoring", [("Logs live in slash var slash log, and messages is the main one.","Logs live in /var/log; messages is main"),("Show chassis environment checks the hardware.","show chassis environment = hardware health"),("Reboot gracefully, and force only when stuck.","Graceful reboot; force only when stuck")]),
])

save("junos-troubleshooting", "Junos Troubleshooting", "Junos troubleshooting", [
 H("question", [("Locked out of your own house","You're standing outside, and your keys are inside."),("Don't kick the door down","You don't kick the door down.",RED),("Work through it step by step","You work through it step by step.",CY)]),
 S("Finding the keys","You check the last place you remember, then retrace your steps. Troubleshooting a router works exactly the same way.",
   [("book","Check the last place you remember.","show log messages","Recent events"),
    ("link","Is the cable even plugged in?","show interfaces","Physical link: Up"),
    ("map","Retrace every step.","traceroute","Where do packets stop?")]),
 F("A simple routine","Here's a routine that works. Check the log. Check the link. Ping the destination. Then trace the path. Roll back as a last resort.",
   [("book","Start with the log.","Log","show log messages"),("link","Then the physical link.","Link","show interfaces"),("bell","Ping the destination.","Ping","Reachable or not?"),("map","Trace the path.","Traceroute","Find the hop that fails")]),
 TR("Three misunderstandings.",
   [("A failed ping means the destination is broken","It could be anything on the path","A failed ping could be the source, a router, a firewall or the destination."),
    ("A reboot clears logs and fixes problems","Logs persist; it rarely fixes config","Rebooting rarely fixes things, and logs stay on disk."),
    ("All logs live in messages","Many log files exist","And there are many logs, not just messages.")]),
 rc("Junos troubleshooting", [("Start with the logs, then the link, then the path.","Logs, then link, then path"),("A failed ping could be caused by anything along the way.","A failed ping can have many causes"),("And rollback is your safety net.","Rollback is your safety net")]),
])

save("junos-vlans", "VLANs and Layer 2 on Junos", "Junos VLANs", [
 H("building", [("Hundreds of residents","Imagine an apartment building with hundreds of residents."),("One mail room","There's one mail room with numbered mailboxes.",CY),("Sorted by the number on the envelope","The postie sorts by the number on the envelope, not the contents.",OR)]),
 S("The mail room","Each mailbox number is a VLAN. The postie never opens letters, they just read the number.",
   [("building","A VLAN is one broadcast domain at layer two.","VLAN","Isolated traffic"),
    ("door","An access port serves one VLAN.","Access port","Strips the 802.1Q tag"),
    ("road","A trunk port carries many.","Trunk port","Keeps the 802.1Q tag"),
    ("router","Between VLANs, you need a layer three interface.","IRB or router","Routes between VLANs")]),
 V("VLAN vs subnet","VLAN","Subnet","These two are related, but not the same thing. A V L A N is layer two. A subnet is layer three. You connect them by giving the I R B interface an address.",
   [("Layer","2","3","A VLAN lives at layer two, and a subnet at layer three."),("Where's the IP","None on the VLAN","On the IRB interface","The address goes on the I R B."),("Routes between","No","Yes, via IRB","Routing needs that layer three interface.")]),
 TR("Three misunderstandings.",
   [("A VLAN is a subnet","VLAN is layer 2; subnet is layer 3","A V L A N is not a subnet."),
    ("Trunks only connect switches","They can connect servers, routers, APs","Trunks can also connect servers, routers and access points."),
    ("A switch routes between VLANs on its own","It needs a layer 3 interface","And a switch won't route between V L A Ns without one.")]),
 rc("Junos VLANs", [("Access ports serve one VLAN, and trunks carry many.","Access: one VLAN. Trunk: many"),("The native VLAN is untagged, and both ends must match.","Native VLAN must match at both ends"),("Routing between VLANs needs a layer three interface.","Inter-VLAN routing needs layer 3")]),
])

save("junos-users", "Users and Authentication on Junos", "Junos users", [
 H("lock", [("Who can log in","Who gets to log in to your router?"),("And what can they do","And what are they allowed to do once they're in?",CY),("That's users and classes","That's users and login classes.",OR)]),
 S("The security badge","On your first day, security made you a badge with your name, photo and a chip listing the doors you can open. Every morning, the guard checks it.",
   [("person","The badge is a user account.","User account","Name plus authentication"),
    ("key","The chip lists your doors.","Login class","Decides which commands run"),
    ("shield","The root badge is special.","root","Can't be deleted")]),
 V("RADIUS vs TACACS+","RADIUS","TACACS+","There are two main servers for central logins. R A D I U S combines authentication and authorisation in one packet. T A C A C S plus keeps them separate, which gives finer control over commands.",
   [("Packets","Combined","Three separate","RADIUS combines them, and TACACS plus separates them."),("Fine control","Less","More, per command","So TACACS plus can control individual commands."),("Interchangeable","No","No","They're not interchangeable.")]),
 TR("Three misunderstandings.",
   [("Root is a normal account","It can't be deleted","The root account can't be deleted, only its authentication changed."),
    ("Operator can only look","It can run ping and traceroute","The operator class can also run ping and traceroute."),
    ("RADIUS and TACACS+ are the same","They split AAA differently","And RADIUS and TACACS plus split the work differently.")]),
 rc("Junos users", [("Every user needs a login class.","Every user needs a login class"),("The root account can't be deleted.","root can't be deleted"),("The default order checks the local password first.","Default: local password first")]),
])
