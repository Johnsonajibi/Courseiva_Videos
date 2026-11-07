import sys; sys.path.insert(0, "tools")
from mk import *

save("ntp", "NTP", "NTP", [
 H("clock", [("Every clock disagrees",  "Every device has its own clock, and they all drift."),("Logs become useless",  "Logs from different devices stop lining up.",RED),("NTP fixes the time","N T P keeps every clock in step.",CY)]),
 S("The town clock", "Think of a town clock that everyone sets their pocket watch by.",
  [("clock","The most accurate source is stratum zero, like an atomic clock.","Stratum 0","Reference clock"),
   ("building","Each step away adds one to the stratum number.","Stratum 1 to 15","Further from the source"),
   ("lock","Sixteen means the device isn't in sync at all.","Stratum 16","Unsynchronised"),
   ("link","It all runs over U D P port one two three.","UDP 123","Time messages")]),
 T("Setting it up", "Setup is short.",
  [("ntp server 192.168.1.10","Point at a time source","Point the device at a time server."),
   ("ntp authenticate","Check the source is genuine","Turn on authentication."),
   ("show ntp status","Is it synced?","Check the status."),
   ("show ntp associations","Who are we syncing to?","And check who it's syncing with.",CY)]),
 TR("Three traps.",
  [("ntp server makes it a server","It makes it a client","That command makes it a client."),
   ("A key alone enables authentication","Also ntp authenticate","You must also turn on authentication."),
   ("Every server needs ntp master","Only when no upstream","Only use master when there's no better source.")]),
 rc("NTP", [("N T P keeps clocks in sync over U D P one two three.","NTP: UDP 123"),("Lower stratum means closer to the source.","Lower stratum = closer to source"),("Stratum sixteen means unsynchronised.","Stratum 16 = unsynced")]),
])

save("syslog", "Syslog", "Syslog", [
 H("bell", [("Devices are talking",  "Your network devices are constantly reporting what happens."),("Too much noise",  "Some messages are trivial, and some are urgent.",OR),("Severity sorts them","Syslog severity sorts them out.",CY)]),
 S("The hospital triage", "A hospital triages patients from zero to seven.",
  [("bell","Zero is an emergency, the most serious of all.","0: Emergency","Most severe"),
   ("wrench","Three is an error, and four is a warning.","3: Error, 4: Warning","Common levels"),
   ("book","Six is informational, and seven is debugging.","6: Info, 7: Debug","Least severe"),
   ("link","Messages travel over U D P port five fourteen by default.","UDP 514","TCP optional")]),
 T("Basic setup", "Send logs to a server like this.",
  [("logging host 192.168.1.50","Where to send messages","Choose the log server."),
   ("logging trap informational","Level to send","Pick the severity to send."),
   ("service timestamps log datetime","Add the time","Add timestamps."),
   ("show logging","See the buffer","And read the local log.",CY)]),
 TR("Three traps.",
  [("Zero is the least severe","Zero is the most severe","Zero is the most severe."),
   ("Default trap level is 7","It's 6, informational","The default trap level is six."),
   ("Syslog uses TCP 514","UDP 514","It uses U D P five fourteen.")]),
 rc("syslog", [("Severity zero is the worst, and seven is the chattiest.","0 worst; 7 chattiest"),("Default trap level is informational.","Default trap level: 6"),("It runs on U D P five fourteen.","UDP 514")]),
])

save("snmp", "SNMP", "SNMP", [
 H("gear", [("A hundred devices",  "A network might have a hundred devices to watch."),("You can't visit each one",  "You can't walk up to each one.",OR),("SNMP asks them remotely","S N M P lets you ask them remotely.",CY)]),
 S("A gated community", "Think of a gated community with different gate systems.",
  [("book","Version two C uses a community string, like a shared password.","SNMPv2c","Plaintext community"),
   ("shield","Version three adds real logins and encryption.","SNMPv3","Users, auth, privacy"),
   ("lock","Auth priv gives both authentication and encryption.","authPriv","MD5 or SHA, plus AES"),
   ("link","Queries use U D P one sixty one, and traps use one sixty two.","UDP 161 / 162","Polls and traps")]),
 V("Versions", "SNMPv2c", "SNMPv3", "Here's how they compare.",
  [("Login","Community string","Username","Version two C uses a community string, and version three uses a username."),
   ("Encryption","None","AES available","Version two C has no encryption, but version three can encrypt."),
   ("Security level","None","noAuth, auth, authPriv","And version three has three security levels.")]),
 TR("Three traps.",
  [("authNoPriv encrypts","It authenticates only","Auth no priv doesn't encrypt."),
   ("Community strings are encrypted","They're plaintext","Community strings are plaintext."),
   ("v3 uses community strings","It uses users","Version three uses users, not strings.")]),
 rc("SNMP", [("Version three is the secure one.","SNMPv3 is secure"),("Queries use U D P one sixty one, and traps use one sixty two.","UDP 161 queries; 162 traps"),("Community strings are plaintext.","Community strings are plaintext")]),
])

save("netflow", "NetFlow", "NetFlow", [
 H("map", [("Who's using the bandwidth?",  "Who is using all your bandwidth?"),("Interface counters don't say",  "Interface counters only show the total.",OR),("NetFlow shows who and what","NetFlow shows who, and what they're doing.",CY)]),
 S("Toll booth cameras", "Imagine cameras at a toll booth logging every car.",
  [("list","A flow is a stream of packets sharing the same seven fields.","A flow","Same 7 key fields"),
   ("map","Those include addresses, ports, protocol, type of service and interface.","Key fields","IPs, ports, protocol, ToS, interface"),
   ("clock","Flows are exported after thirty minutes, or fifteen seconds quiet.","Timeouts","Active 30 min; inactive 15 s"),
   ("server","Records go to a collector over U D P port two zero five five.","UDP 2055","Collector")]),
 TR("Three traps.",
  [("NetFlow captures payloads","Only headers and counts","It only records header information."),
   ("Export uses TCP","UDP","Export uses U D P."),
   ("Active timeout is 15 seconds","30 minutes","The active timeout is thirty minutes.")]),
 rc("NetFlow", [("NetFlow shows who talks to whom, not what they say.","Who talks to whom"),("A flow has seven key fields.","7 key fields"),("Export goes to a collector on U D P two zero five five.","UDP 2055 to a collector")]),
])

save("cdp-lldp", "CDP and LLDP", "CDP and LLDP", [
 H("people", [("A conference",  "At a conference, people swap business cards."),("Switches do too",  "Network devices swap cards with their neighbours.",CY),("CDP and LLDP are the cards","C D P and L L D P are those cards.",OR)]),
 S("Business cards", "Both protocols advertise who a device is.",
  [("stamp","C D P is Cisco's own, and it's on by default.","CDP","Cisco proprietary, on by default"),
   ("list","L L D P is the open standard, and it's off by default.","LLDP","IEEE 802.1AB, off by default"),
   ("clock","C D P sends a card every sixty seconds.","CDP timer: 60 s","Hold time 180 s"),
   ("door","Neither crosses a router, so it only finds direct neighbours.","Layer 2 only","One hop")]),
 T("Commands", "Check neighbours like this.",
  [("show cdp neighbors","Who's next door","See your C D P neighbours."),
   ("lldp run","Turn LLDP on","Turn on L L D P."),
   ("show lldp neighbors","LLDP neighbours","And see the L L D P neighbours.",CY)]),
 TR("Three traps.",
  [("LLDP is on by default","CDP is; LLDP isn't","L L D P is off by default."),
   ("CDP crosses routers","Direct neighbours only","It stops at the first router."),
   ("Holdtime equals timer","Hold is three times longer","The hold time is longer than the timer.")]),
 rc("CDP and LLDP", [("C D P is Cisco, and L L D P is the standard.","CDP: Cisco. LLDP: standard"),("Only C D P is on by default.","CDP on by default"),("They find direct neighbours only.","Direct neighbours only")]),
])

save("monitoring", "Network Monitoring", "Monitoring", [
 H("gear", [("A building management system",  "A building manager watches every room from one screen."),("Alarms and readings",  "They get readings, and alarms when something breaks.",CY),("SNMP does that for networks","S N M P does that for networks.",OR)]),
 S("The control room", "S N M P has two ways to hear from a device.",
  [("mic","Polling means the manager asks for a reading.","Polling","UDP 161"),
   ("bell","A trap is the device shouting that something happened.","Trap","UDP 162, unsolicited"),
   ("lock","Only version three has real security.","SNMPv3","Auth and encryption"),
   ("book","Old community strings are public for read and private for write.","public / private","v1 and v2c defaults")]),
 TR("Quick facts.",
  [("Traps go to port 161","Traps use 162","Traps use one sixty two."),
   ("Strings are secret","They're plaintext","Community strings are plaintext."),
   ("Version two is secure","Only version three","Only version three is secure.")]),
 rc("monitoring", [("Polls are on one sixty one, and traps are on one sixty two.","161 polls; 162 traps"),("A trap is an alert from the device.","Trap = alert from device"),("Use version three for security.","Use SNMPv3")]),
])

save("packet-capture", "Reading Packet Captures", "Packet captures", [
 H("book", [("A packet capture",  "A packet capture is a recording of what crossed the wire."),("Reading it is a skill",  "Reading one is a skill the exam now tests.",OR),("Look for the clues","Let's learn to spot the clues.",CY)]),
 S("The postal investigation", "Each type of packet leaves a clue.",
  [("question","A R P requests with no reply point to a layer two problem.","ARP, no reply","Wrong VLAN, host down"),
   ("bell","I C M P type three code four means the packet needed fragmenting.","ICMP 3/4","MTU problem"),
   ("clock","One time exceeded message is normal, since that's how traceroute works.","ICMP Time Exceeded","Not always a loop"),
   ("envelope","T C P retransmissions point to loss, or to a slow receiver.","TCP retransmits","Not always loss")]),
 TR("Three traps.",
  [("No ARP reply means the IP is wrong","Could be VLAN or host","It might be a VLAN or a host issue."),
   ("One Time Exceeded means a loop","Traceroute causes these","Traceroute causes them too."),
   ("Retransmits always mean loss","Could be a slow receiver","They can mean other things.")]),
 rc("packet captures", [("A R P with no reply means look at layer two.","ARP no reply = Layer 2"),("I C M P three four means M T U trouble.","ICMP 3/4 = MTU"),("Don't jump to conclusions from one packet.","Don't conclude from one packet")]),
])

save("troubleshooting-method", "Troubleshooting Method", "Troubleshooting", [
 H("wrench", [("Something's broken",  "Something on the network is broken."),("Where do you start?",  "Most people start guessing.",OR),("Start at the bottom","Good engineers start at the bottom.",CY)]),
 S("The car mechanic", "A mechanic checks the simple things first.",
  [("wrench","Start at layer one, the cables and the link lights.","Layer 1","Cables, power, link"),
   ("switch","Then layer two, such as V L A Ns and trunks.","Layer 2","VLANs, trunks, MAC"),
   ("router","Then layer three, addresses and routes.","Layer 3","IP, routing"),
   ("list","Work up one layer at a time until you find it.","Bottom-up","Don't skip layers")]),
 T("Go-to commands", "A few commands cover most checks.",
  [("show interfaces","Status and errors","Check the interface."),
   ("show vlan brief","Right VLAN?","Check the V L A N."),
   ("show interfaces trunk","Trunk allowed?","Check the trunk."),
   ("show ip route","Is there a route?","And check the route.",CY)]),
 TR("Three traps.",
  [("Up/up means layer 1 is perfect","Errors can hide","Up up can still hide errors."),
   ("A good ping means all is well","Apps can still fail","A ping doesn't prove everything works."),
   ("Reboot first","Last resort","Reboot is a last resort.")]),
 rc("troubleshooting", [("Start at layer one and work up.","Bottom-up"),("Check interfaces, V L A Ns, trunks and routes.","Interfaces, VLANs, trunks, routes"),("Never reboot first.","Reboot last")]),
])

save("performance", "Bandwidth Saturation", "Performance", [
 H("road", [("The highway is jammed",  "The highway is jammed at rush hour."),("Cars wait or give up",  "Some cars wait, and some are turned away.",OR),("Links do the same","A busy link does exactly the same.",CY)]),
 S("Highway congestion", "A link fills up when too much traffic arrives at once.",
  [("scale","Sustained use above seventy percent is a warning.","70%: warning","Sustained utilisation"),
   ("bell","Above ninety percent is critical.","90%: critical","Expect problems"),
   ("box","The key symptom is output drops on the interface.","Output drops","show interface"),
   ("gear","I perf measures the real throughput between two points.","iPerf3","Active test")]),
 TR("Three tips.",
  [("Full usage always means a fault","It means saturation","It just means the link is busy."),
   ("Only input counters matter","Output drops are the clue","Output drops are the real clue."),
   ("A ping shows throughput","iPerf does","I perf measures throughput.")]),
 rc("saturation", [("Seventy percent is a warning, and ninety is critical.","70% warn; 90% critical"),("Look for output drops.","Output drops"),("Test with I perf.","Test with iPerf")]),
])

save("qos", "QoS", "QoS", [
 H("clock", [("Voice and video can't wait",  "Voice and video can't wait in a queue."),("Email can",  "Email can wait quite happily.",CY),("QoS decides who goes first","Q o S decides who goes first.",OR)]),
 S("The VIP security lane", "Think of an airport with a fast lane for VIPs.",
  [("list","Classification spots which packets are which.","Classify","Identify traffic"),
   ("stamp","Marking stamps them with a priority value, called D S C P.","Mark: DSCP","Layer 3 marking"),
   ("mic","Voice gets E F, which is forty six.","EF = 46","Voice"),
   ("door","L L Q gives voice a strict priority queue.","LLQ","Strict priority")]),
 TR("Three traps.",
  [("QoS gives more bandwidth","It only chooses who goes first","It doesn't create bandwidth."),
   ("Priority gives unlimited bandwidth","It's policed","Priority is limited."),
   ("CoS survives routers","Only DSCP does","C o S doesn't cross routers.")]),
 rc("QoS", [("Classify, mark, then queue.","Classify, mark, queue"),("Voice is E F, forty six.","Voice = EF (46)"),("Q o S can't create bandwidth.","QoS adds no bandwidth")]),
])

save("network-management", "Network Management Tools", "Network management", [
 H("building", [("The building superintendent",  "A building superintendent has several tools."),("One for each job",  "Each one does a different job.",CY),("Pick the right one","Picking the right one is the skill.",OR)]),
 S("The superintendent", "Each protocol answers a different question.",
  [("gear","S N M P polls devices and sends traps.","SNMP","UDP 161 and 162"),
   ("bell","Syslog collects event messages.","Syslog","UDP 514"),
   ("map","NetFlow shows who is talking to whom.","NetFlow","UDP 2055"),
   ("scale","Severity zero is the most critical in syslog.","Severity 0","Most critical")]),
 TR("Three traps.",
  [("Syslog is best for real-time alerts","SNMP traps are","S N M P traps alert in real time."),
   ("NetFlow shows interface totals","SNMP does","S N M P gives interface totals."),
   ("Level one is the most critical","Zero is","Zero is the most critical.")]),
 rc("management tools", [("S N M P polls, syslog logs, and NetFlow shows flows.","SNMP polls; syslog logs; NetFlow shows flows"),("Zero is the worst syslog level.","Syslog 0 = worst"),("Know the ports: one sixty one, five fourteen, two zero five five.","161, 514, 2055")]),
])

save("automation-concepts", "Network Automation", "Network automation", [
 H("gear", [("A factory line",  "A factory assembly line builds the same thing, perfectly, every time."),("Handcrafting is slow",  "Handcrafting is slow, and no two are alike.",OR),("Automation is the line","Automation puts the network on the assembly line.",CY)]),
 S("Assembly line vs handcrafting", "Automation brings a few clear benefits.",
  [("list","It applies the same settings to every device.","Consistency","Fewer human errors"),
   ("clock","Idempotent means running it twice changes nothing new.","Idempotency","Safe to repeat"),
   ("people","Ansible is agentless, so nothing is installed on devices.","Ansible","Agentless"),
   ("shield","It frees engineers for the work that matters.","Doesn't replace engineers","Helps all sizes")]),
 TR("Three traps.",
  [("Automation replaces engineers","It supports them","It helps engineers, not replaces them."),
   ("Only for huge networks","Small ones benefit too","Small networks benefit too."),
   ("Ansible needs an agent","Agentless","Ansible is agentless.")]),
 rc("automation", [("Automation means fewer mistakes and faster changes.","Fewer mistakes; faster changes"),("Idempotent means safe to repeat.","Idempotent = safe to repeat"),("Ansible is agentless.","Ansible is agentless")]),
])

save("config-mgmt-tools", "Ansible", "Ansible", [
 H("list", [("A conductor and sheet music",  "An orchestra conductor reads from sheet music."),("The players follow",  "The players simply follow along.",CY),("That's Ansible","That's how Ansible works.",OR)]),
 S("The orchestra", "Ansible pushes instructions out to every device.",
  [("laptop","The control node is the conductor.","Control node","Pushes the config"),
   ("lock","It connects to each device over S S H.","SSH","No agent needed"),
   ("book","The sheet music is a playbook, written in Y A M L.","Playbook (YAML)","Plays and tasks"),
   ("gear","Each task calls a module to do one job.","Modules","Run on the control node")]),
 TR("Three traps.",
  [("Ansible needs an agent","Agentless","It's agentless."),
   ("Playbooks are JSON","YAML","Playbooks are written in Y A M L."),
   ("Modules run on the device","On the control node","Modules run on the control node.")]),
 rc("Ansible", [("Ansible pushes over S S H, with no agent.","Push over SSH; no agent"),("Playbooks are Y A M L.","Playbooks are YAML"),("Modules run on the control node.","Modules run on the control node")]),
])

save("python-networking", "Python for Networking", "Python", [
 H("laptop", [("A robot chef",  "Imagine a robot chef who follows recipe cards."),("Python is the recipe",  "Python is the recipe card for your network.",CY),("Netmiko is the chef","Netmiko is the chef that logs into devices.",OR)]),
 S("The robot chef", "A few libraries do the heavy lifting.",
  [("lock","Paramiko is the low level S S H library.","Paramiko","Low-level SSH"),
   ("gear","Netmiko is simpler, and built for network devices.","Netmiko","Easier for networks"),
   ("list","You give it a dictionary with the device type, host, user and password.","ConnectHandler","device_type, host, username, password"),
   ("book","Use send command to read, and send config set to change.","send_command / send_config_set","Read vs change")]),
 TR("Three traps.",
  [("Paramiko is easier than Netmiko","Netmiko is simpler","Netmiko is easier for network gear."),
   ("Python runs on the device","Runs on your computer","It normally runs on your own computer."),
   ("send_command enters config mode","Use send_config_set","Use send config set for changes.")]),
 rc("Python networking", [("Netmiko makes S S H easy.","Netmiko makes SSH easy"),("Send command reads, and send config set changes.","send_command reads; send_config_set changes"),("Scripts run on your computer.","Scripts run on your computer")]),
])

save("ai-network-ops", "AI in Network Operations", "AI network ops", [
 H("gear", [("A fleet manager",  "A fleet manager watches hundreds of vehicles."),("Spots trouble early",  "They spot trouble before it happens.",CY),("An AI agent does that","An A I agent can do the same for a network.",OR)]),
 S("The autonomous fleet manager", "An agent follows a simple loop.",
  [("wifi","It observes the network, using S N M P, NetFlow and logs.","Observe","Telemetry"),
   ("book","It builds a baseline of what normal looks like.","Baseline","Detect anomalies"),
   ("gear","It decides, and then it acts.","Decide and act","Within guardrails"),
   ("person","A human stays in charge of the limits.","Human oversight","Guardrails")]),
 TR("Three traps.",
  [("It's just scripting","It decides on its own","It makes decisions, not just scripts."),
   ("No oversight needed","Guardrails are essential","It needs guardrails."),
   ("It needs no data","Data is the fuel","It depends on good data.")]),
 rc("AI network ops", [("An agent observes, decides and acts.","Observe, decide, act"),("It learns what normal looks like.","Learns a baseline"),("Humans set the guardrails.","Humans set guardrails")]),
])

save("rest-apis", "REST APIs", "REST APIs", [
 H("book", [("A restaurant",  "Picture a restaurant with a menu and a waiter."),("You order, they bring it",  "You order from the menu, and the waiter brings it back.",CY),("That's a REST API","That's how a R E S T A P I works.",OR)]),
 S("Ordering at the restaurant", "Each H T T P method is a kind of order.",
  [("book","GET reads something from the menu.","GET","Read"),
   ("list","POST creates a new order.","POST","Create"),
   ("gear","PUT replaces an order, and PATCH changes part of it.","PUT / PATCH","Replace / modify"),
   ("lock","DELETE cancels it.","DELETE","Remove")]),
 T("Status codes", "The waiter answers with a number.",
  [("200 OK","It worked","Two hundred means it worked."),
   ("201 Created","New item made","Two oh one means something new was created."),
   ("401 Unauthorized","Log in first","Four oh one means you're not logged in."),
   ("404 Not Found","No such item","And four oh four means it doesn't exist.",CY)]),
 TR("Three traps.",
  [("REST is only for websites","Network devices use it too","Network devices use it too."),
   ("PUT and PATCH are the same","Replace vs modify","One replaces, one modifies."),
   ("401 means forbidden","403 means forbidden","Four oh three means forbidden.")]),
 rc("REST APIs", [("GET reads, POST creates, PUT replaces, DELETE removes.","GET, POST, PUT, DELETE"),("Two hundred means success.","200 = OK"),("Four oh one is login, and four oh three is forbidden.","401 login; 403 forbidden")]),
])

save("data-formats", "JSON for Networking", "JSON", [
 H("list", [("A shipping manifest",  "A shipping manifest lists everything in a neat, standard way."),("Machines read it easily",  "Machines can read it without guessing.",CY),("That's JSON","That's what J S O N does for data.",OR)]),
 S("The manifest", "J S O N has a few strict rules.",
  [("lock","Keys and text must use double quotes.","Double quotes only","Not single"),
   ("box","It has six types, including objects and arrays.","Six data types","String, number, boolean, null, object, array"),
   ("wrench","No trailing commas are allowed.","No trailing commas","Common mistake"),
   ("book","And no comments are allowed either.","No comments","Not like code")]),
 TR("Three traps.",
  [("Single quotes are fine","Double only","Only double quotes work."),
   ("Comments are allowed","They aren't","J S O N has no comments."),
   ("| json works everywhere","Not every command","The pipe doesn't work on every command.")]),
 rc("JSON", [("Double quotes, no trailing commas, no comments.","Double quotes; no trailing commas; no comments"),("Six data types.","Six data types"),("It's how scripts read device data.","How scripts read device data")]),
])

save("netconf-yang", "YANG and NETCONF", "YANG and NETCONF", [
 H("map", [("Blueprints for devices",  "Every device needs a blueprint for how it's configured."),("A shared language",  "A shared blueprint lets tools talk to any device.",CY),("That's YANG","That blueprint is called YANG.",OR)]),
 S("Building blueprints", "Three names get mixed up all the time.",
  [("map","YANG is the data model, the blueprint itself.","YANG","A modelling language"),
   ("link","NETCONF delivers it, using X M L.","NETCONF","XML, over SSH"),
   ("cloud","RESTCONF delivers it too, using X M L or J S O N.","RESTCONF","XML or JSON"),
   ("list","Models starting with I E T F are standard.","ietf- models","e.g. ietf-interfaces")]),
 TR("Three traps.",
  [("YANG is a protocol","It's a data model","It's a model, not a protocol."),
   ("YANG only models config","Also operational state","It models state too."),
   ("RESTCONF is JSON only","XML or JSON","It can use X M L or J S O N.")]),
 rc("YANG", [("YANG is the blueprint.","YANG = blueprint"),("NETCONF and RESTCONF carry it.","NETCONF and RESTCONF carry it"),("It covers config and state.","Config and state")]),
])

save("sdn", "Software-Defined Networking", "SDN", [
 H("building", [("An airport control tower",  "An airport has one control tower guiding every plane."),("Planes just fly",  "The planes only follow the instructions.",CY),("SDN works like that","S D N brings that idea to networks.",OR)]),
 S("The control tower", "S D N splits the brain from the muscle.",
  [("building","The controller is the control tower, the control plane.","Control plane","Centralised controller"),
   ("switch","Switches only forward, which is the data plane.","Data plane","Forwarding devices"),
   ("cloud","Northbound A P Is connect apps to the controller.","Northbound","REST APIs"),
   ("link","Southbound A P Is connect the controller to devices.","Southbound","OpenFlow, NETCONF")]),
 TR("Three traps.",
  [("SDN removes routing protocols","It centralises control","Routing logic moves, it doesn't vanish."),
   ("REST is southbound","REST is northbound","REST is northbound."),
   ("OpenFlow is the only southbound","NETCONF too","There are other southbound options.")]),
 rc("SDN", [("The controller is the brain, and the devices only forward.","Controller = brain; devices forward"),("Northbound talks to apps.","Northbound: apps"),("Southbound talks to devices.","Southbound: devices")]),
])

save("sdwan", "SD-WAN", "SD-WAN", [
 H("road", [("One expensive line",  "Old networks relied on one expensive private line."),("Cheap links sit idle",  "Cheaper links sat unused.",OR),("SD WAN uses them all","S D W A N uses every link at once.",CY)]),
 S("The smart highway", "Think of a highway system that watches the traffic.",
  [("building","Control is centralised, so policy is set in one place.","Central policy","Controller"),
   ("road","It can use M P L S, broadband and L T E together.","Multiple transports","MPLS, broadband, LTE"),
   ("wifi","It picks the best path for each application.","Application-aware routing","Per app"),
   ("shield","If a link degrades, traffic moves automatically.","Automatic failover","Resilience")]),
 rc("SD-WAN", [("S D W A N uses many links at once.","Many links at once"),("Policy is set centrally.","Central policy"),("Traffic moves to the best path.","Best path per app")]),
])
