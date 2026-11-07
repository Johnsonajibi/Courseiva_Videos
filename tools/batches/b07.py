import sys; sys.path.insert(0, "tools")
from mk import *

save("wifi-troubleshooting", "Wi-Fi Troubleshooting", "Wi-Fi troubleshooting", [
 H("wifi", [("Wi-Fi is slow",  "Wi Fi is slow, or it keeps dropping."),("Where do you start?",  "Where do you even start?",OR),("Work through it in order","Work through it in a set order.",CY)]),
 S("The noisy concert", "Imagine trying to chat in a loud concert venue.",
  [("wifi","First check the device actually joins the network.","1. Association","Can it connect at all?"),
   ("bell","Then check the signal, since below minus seventy five is poor.","2. Signal: RSSI, SNR","RSSI below -75 dBm is weak"),
   ("people","Then look for noise from other Wi Fi and other gadgets.","3. Interference","Channel use above 80% is congested"),
   ("wrench","Last, check the settings and how clients roam.","4. Config and roaming","SSID, VLAN, DHCP")]),
 TR("Common traps.",
  [("Seeing the SSID means the AP is fine","Other config can still be wrong","Seeing the name doesn't prove the setup is right."),
   ("More power always helps","It can add interference","More power can add interference."),
   ("An IP address means DHCP is fine","The scope may be wrong","Having an address doesn't prove D H C P is right.")]),
 rc("Wi-Fi troubleshooting", [("Go in order: join, signal, interference, config.","Join, signal, interference, config"),("Below minus seventy five is a weak signal.","RSSI below -75 dBm"),("More power isn't always better.","More power can hurt")]),
])

save("cabling-install-test", "Structured Cabling", "Structured cabling", [
 H("road", [("Cables are the city's utilities",  "Cables are a building's utility grid."),("Rules keep it working",  "A few strict rules keep it working.",CY),("Know the numbers","You need to know the numbers.",OR)]),
 T("Numbers to remember", "Here are the key limits.",
  [("Permanent link   90 m","Wall socket run","The permanent link is ninety metres."),
   ("Full channel   100 m","With patch cords","The full channel, with patch cords, is a hundred."),
   ("Cat6   10G to 55 m","Cat6a for 100 m","Cat six only does ten gig for fifty five metres."),
   ("T568A or T568B","Never mix in one site","Pick T five six eight A or B, and don't mix them.",CY)]),
 TR("Three traps.",
  [("Only the run counts toward 100 m","Patch cords count too","Patch cords count toward the hundred."),
   ("Mix A and B freely","Pick one standard","Pick one standard for the building."),
   ("Cat6 is fine for 10G at full length","Needs Cat6a","Cat six A is needed for the full distance.")]),
 rc("structured cabling", [("Ninety metres of cable, and a hundred in total.","90 m link, 100 m channel"),("Cat six A for full distance ten gig.","Cat6a for 10G at 100 m"),("One wiring standard per site.","One wiring standard")]),
])

save("data-center-physical", "Data Centre Physical Layer", "Data centre cabling", [
 H("server", [("Racks and racks of kit",  "A data centre is rows and rows of racks."),("Everything is cabled",  "Every one has to be cabled neatly.",CY),("The physical layer matters","The physical layer matters more than you'd think.",OR)]),
 S("The utility grid", "Think of cables as a city's power and water.",
  [("ruler","Copper runs stop at ninety metres, plus ten for patch cords.","90 + 10 = 100 m","Twisted pair limit"),
   ("wifi","Fibre ignores electrical noise, and goes much further.","Fibre: immune to EMI","Longer distances"),
   ("key","Straight through cables need the same standard at both ends.","T568B at both ends","Most common standard"),
   ("box","And neat labelled racks make faults far easier to find.","Label and organise","Faster fixes")]),
 TR("Three traps.",
  [("Copper goes any distance","100 m limit","Copper stops at a hundred metres."),
   ("Fibre is affected by EMI","Fibre is immune","Fibre ignores interference."),
   ("Different standards at each end are fine","Use the same","Use the same standard at both ends.")]),
 rc("data centre cabling", [("Copper to a hundred metres, fibre beyond.","Copper 100 m; fibre further"),("Fibre ignores interference.","Fibre is immune to EMI"),("Label everything.","Label everything")]),
])

save("eigrp-neighbors-advanced", "EIGRP Neighbor Adjacency", "EIGRP neighbors", [
 H("people", [("Two EIGRP routers",  "Two E I G R P routers sit on the same link."),("They won't talk",  "But they won't become neighbours.",RED),("Check the five conditions","Check the five conditions.",CY)]),
 S("The fifteen door building", "To become neighbours, five things must line up.",
  [("key","The A S number must match.","1. Same AS","Autonomous system number"),
   ("map","They must be on the same subnet.","2. Same subnet","On the shared link"),
   ("scale","The K values must match.","3. Same K-values","Metric weights"),
   ("lock","Any authentication must match.","4. Same authentication","If configured"),
   ("door","And the interface must not be passive.","5. Not passive","Passive blocks hellos")]),
 TR("Three traps.",
  [("Hostnames must match","Router IDs just need to be unique","Hostnames don't matter."),
   ("Changing hello changes the neighbour's","Hold time is per router","Each router sets its own timers."),
   ("Enabling EIGRP forms neighbours","You must advertise networks","You must also use the network command.")]),
 rc("EIGRP adjacency", [("Same A S, subnet, K values, authentication.","Same AS, subnet, K-values, auth"),("The interface must not be passive.","Not passive"),("Hello is five seconds and hold is fifteen.","Hello 5 s, hold 15 s")]),
])

save("vrf-bgp", "VRF-Lite and MP-BGP", "VRF and MP-BGP", [
 H("building", [("One router",  "One router can serve many customers."),("Each wants privacy",  "Each one wants their own private routing table.",CY),("VRF gives them that","A V R F gives them exactly that.",OR)]),
 S("The apartment mailroom", "Picture one mailroom with separate shelves for each tenant.",
  [("box","Each V R F is its own private routing table.","VRF","Isolated routes"),
   ("router","V R F lite works on one router, and needs no M P L S.","VRF-Lite","Single router, no MPLS"),
   ("link","M P B G P carries V P N routes between routers.","MP-BGP","Multiple address families"),
   ("stamp","A route distinguisher makes each route unique.","Route Distinguisher","Unique, but not a filter")]),
 TR("Three traps.",
  [("VRF-Lite uses MPLS","It doesn't","V R F lite doesn't use M P L S."),
   ("MP-BGP is only for IPv6","Many address families","M P B G P carries many address families."),
   ("RD controls which VRF","Route targets do","The route target controls import, not the R D.")]),
 rc("VRF and MP-BGP", [("A V R F is a private routing table.","VRF = private routing table"),("M P B G P carries V P N routes.","MP-BGP carries VPN routes"),("The R D only makes routes unique.","RD = unique only")]),
])

save("multicast-basics", "Multicast Basics", "Multicast", [
 H("mic", [("A conference call",  "A conference call sends one voice to many people."),("Not one at a time",  "It doesn't call each person separately.",CY),("That's multicast","That's multicast.",OR)]),
 S("The conference call", "Multicast uses a shared group address.",
  [("list","Group addresses start from two twenty four, called class D.","Class D: 224.0.0.0/4","Group addresses"),
   ("people","Hosts tell the router they want to join using I G M P.","IGMP","Hosts to router"),
   ("book","The M A C address starts with zero one, zero zero, five E.","MAC 01-00-5E","23 bits from the IP"),
   ("bell","And thirty two group addresses can share one M A C address.","32 IPs per MAC","Overlap is normal")]),
 TR("Three traps.",
  [("The source is the group address","The source is always unicast","The source is always a unicast address."),
   ("IGMP runs between routers","Between hosts and their router","I G M P runs between hosts and the router."),
   ("Each group has its own MAC","Thirty two share one","Several groups can share one M A C address.")]),
 rc("multicast", [("Multicast sends once to many.","One send, many receivers"),("I G M P handles joining.","IGMP handles joining"),("Group addresses are two twenty four and up.","224.0.0.0 and up")]),
])

save("ids-ips", "IDS vs IPS", "IDS and IPS", [
 H("shield", [("Airport security",  "Think of airport security."),("One camera watches",  "One system just watches and raises the alarm.",CY),("One stops you","Another stops you at the gate.",OR)]),
 S("Screening", "Both look for bad traffic, but they act differently.",
  [("bell","An I D S sits beside the traffic and only alerts.","IDS: passive","Out of band, uses SPAN or tap"),
   ("door","An I P S sits in the path and can block.","IPS: inline","Can drop traffic"),
   ("list","Both match signatures, odd behaviour and protocol rules.","Detection methods","Signature, anomaly, protocol"),
   ("clock","The price is that an I P S adds delay.","IPS adds latency","Inline cost")]),
 V("Compare", "IDS", "IPS", "Here's the difference at a glance.",
  [("Placement","Out of band","Inline","An I D S sits out of band, and an I P S sits inline."),
   ("Action","Alert only","Alert and block","An I D S only alerts, but an I P S can block."),
   ("Delay","None","Adds latency","And an I P S adds a little delay.")]),
 rc("IDS and IPS", [("I D S alerts, and I P S blocks.","IDS alerts; IPS blocks"),("I P S sits inline.","IPS is inline"),("An I P S adds a little delay.","IPS adds latency")]),
])

save("network-attacks", "Common Network Attacks", "Network attacks", [
 H("shield", [("The digital break-in crew",  "Meet the digital break in crew."),("Different tricks",  "Each member has a different trick.",OR),("Know them by name","Learn each one by name.",CY)]),
 S("The break-in crew", "Four tricks come up all the time.",
  [("bell","A denial of service attack floods a target so nobody can reach it.","DoS / DDoS","Targets availability"),
   ("envelope","A S Y N flood starts handshakes and never finishes them.","SYN flood","Fix: SYN cookies"),
   ("people","D N S amplification uses open resolvers to magnify a flood.","DNS amplification","Open resolvers"),
   ("lock","A R P spoofing lies about who owns an address.","ARP spoofing","Fix: DAI")]),
 TR("Quick matches.",
  [("DDoS comes from one source","Many sources","D D o S uses many sources."),
   ("SYN flood hits UDP","It abuses the TCP handshake","S Y N floods abuse the T C P handshake."),
   ("ARP spoofing works across routers","Same subnet only","A R P spoofing stays on the local subnet.")]),
 rc("network attacks", [("D o S attacks hit availability.","DoS hits availability"),("S Y N cookies help against S Y N floods.","SYN cookies stop SYN floods"),("D A I stops A R P spoofing.","DAI stops ARP spoofing")]),
])

save("crypto-basics", "Cryptography Basics", "Cryptography", [
 H("lock", [("A locked briefcase",  "Imagine a courier with a locked briefcase."),("One key or two",  "Does the sender and receiver share one key, or use two?",CY),("That's the big split","That's the big split in cryptography.",OR)]),
 S("The courier", "Two kinds of locks exist.",
  [("key","Symmetric uses one shared key, and it's fast.","Symmetric","One shared key, AES"),
   ("lock","Asymmetric uses a public key and a private key.","Asymmetric","Key pair, RSA"),
   ("stamp","A hash is a fingerprint that proves nothing changed.","Hash","SHA-256 or better"),
   ("shield","Diffie Hellman lets two sides agree on a key in public.","Diffie-Hellman","Group 14 or better")]),
 TR("Three traps.",
  [("SSH encrypts everything with RSA","RSA authenticates; the session uses symmetric","S S H uses R S A only for authentication."),
   ("MD5 is still fine","MD5 is broken","M D five is broken."),
   ("Signatures equal HMAC","Signatures use asymmetric keys","Signatures use asymmetric keys, H M A C doesn't.")]),
 rc("cryptography", [("Symmetric is fast, and asymmetric solves key sharing.","Symmetric: fast. Asymmetric: key sharing"),("Use S H A two fifty six or better.","SHA-256 minimum"),("Avoid M D five and D E S.","Avoid MD5 and DES")]),
])

save("vpn-types", "VPN Types", "VPN types", [
 H("lock", [("Two kinds of VPN",  "There are two main kinds of V P N."),("For offices",  "One connects whole offices together.",CY),("For people","The other connects one person to the office.",OR)]),
 S("Mailroom vs personal courier", "Think of the company mailroom and the personal courier.",
  [("building","A site to site V P N is the mailroom, moving all mail between offices.","Site-to-site VPN","Router to router"),
   ("person","A remote access V P N is a personal courier for one worker.","Remote access VPN","Client software"),
   ("key","Site to site normally uses I P sec, with I K E on U D P five hundred.","IPsec + IKE","UDP 500"),
   ("lock","Remote access can use I P sec or S S L.","IPsec or SSL/TLS","Both are valid")]),
 TR("Three traps.",
  [("Remote access is IPsec only","SSL works too","Remote access can use S S L too."),
   ("Site-to-site needs a client","Routers do it","Site to site needs no client software."),
   ("Phase 2 is the management tunnel","Phase 1 is","Phase one makes the management tunnel.")]),
 rc("VPN types", [("Site to site joins offices, and remote access joins people.","Site-to-site: offices. Remote: people"),("I K E has two phases.","IKE has two phases"),("Remote access can use S S L.","Remote can use SSL")]),
])

save("ipsec-vpn", "IPsec VPN", "IPsec", [
 H("shield", [("An armoured convoy",  "Picture an armoured convoy."),("Protects what's inside",  "It protects the cargo, and checks it hasn't been touched.",CY),("That's IPsec","That's what I P sec does for packets.",OR)]),
 S("The armoured convoy", "I P sec builds the convoy in two phases.",
  [("key","Phase one agrees the rules, using I K E on U D P five hundred.","IKE Phase 1","UDP 500, lasts 86400 s"),
   ("lock","Phase two builds the tunnel that carries the data.","IKE Phase 2","IPsec SA, lasts 3600 s"),
   ("shield","E S P encrypts and checks the data.","ESP","Encryption and integrity"),
   ("list","The crypto lists on each side must mirror each other.","Mirror-image ACLs","Source and destination swapped")]),
 TR("Three traps.",
  [("IKE uses TCP 500","UDP 500","I K E uses U D P."),
   ("AH is more secure than ESP","ESP can do both","E S P can encrypt and authenticate."),
   ("Both ACLs are identical","They are mirrors","They must be mirror images.")]),
 rc("IPsec", [("I K E phase one, then phase two.","IKE phase 1, then phase 2"),("E S P encrypts and checks data.","ESP encrypts and authenticates"),("Crypto lists must mirror each other.","Mirror the crypto ACLs")]),
])

save("gre", "GRE Tunnels", "GRE", [
 H("envelope", [("An express envelope",  "Imagine putting a letter inside a bigger envelope."),("It travels as one thing",  "The outer one carries the inner one across the network.",CY),("That's GRE","That's a G R E tunnel.",OR)]),
 S("The express envelope", "G R E wraps packets inside new ones.",
  [("envelope","It adds a four byte G R E header and a new I P header.","24 bytes overhead","4 + 20"),
   ("list","The outer I P protocol number is forty seven.","IP protocol 47","GRE"),
   ("link","Tunnels are point to point, and can carry multicast.","Point-to-point","Supports multicast"),
   ("lock","But G R E gives no encryption at all.","No encryption","Add IPsec for that")]),
 TR("Three traps.",
  [("GRE encrypts traffic","It doesn't","G R E has no security."),
   ("GRE is protocol 50","47 (ESP is 50)","G R E is forty seven, E S P is fifty."),
   ("GRE is multipoint by default","Point-to-point","G R E is point to point by default.")]),
 rc("GRE", [("G R E wraps packets, and adds twenty four bytes.","GRE adds 24 bytes"),("It's I P protocol forty seven.","IP protocol 47"),("Add I P sec if you need encryption.","Add IPsec for encryption")]),
])

save("dmvpn", "DMVPN and FlexVPN", "DMVPN", [
 H("map", [("Fifty offices",  "A company has fifty offices."),("A tunnel between each pair?",  "Building a tunnel between every pair would be a nightmare.",RED),("DMVPN builds them on demand","D M V P N builds them as needed.",CY)]),
 S("The private driver guild", "Drivers register with a central office, called the hub.",
  [("building","The hub is the register of where everyone is.","Hub","NHRP server"),
   ("people","Each spoke tells the hub its real address.","Spokes register","Using NHRP"),
   ("link","Spokes then find each other and build direct tunnels.","Spoke-to-spoke tunnels","Dynamic"),
   ("key","The I P sec profile goes on the tunnel interface.","IPsec profile","Not a crypto map")]),
 TR("Three traps.",
  [("DMVPN and FlexVPN are unrelated","Same purpose","They share the same purpose."),
   ("Phase 3 still goes via the hub","Spokes talk directly","Phase three lets spokes talk directly."),
   ("Use a crypto map","Use an IPsec profile","Use an I P sec profile.")]),
 rc("DMVPN", [("N H R P lets spokes find each other.","NHRP lets spokes find each other"),("Phase three builds direct tunnels.","Phase 3: direct tunnels"),("Flex V P N is the I K E version two way.","FlexVPN is IKEv2-based")]),
])

save("cisco-umbrella", "Cisco Umbrella", "Cisco Umbrella", [
 H("shield", [("A hotel concierge",  "Picture a hotel concierge who checks every address you ask for."),("Bad address?",  "If it's a known bad one, they don't let you go.",CY),("That's DNS filtering","That's what Umbrella does with D N S.",OR)]),
 S("The DNS concierge", "Umbrella sits in the cloud, and checks names before you connect.",
  [("cloud","It's a cloud service, backed by Cisco Talos threat research.","Cloud DNS security","Talos intelligence"),
   ("list","It judges each name by its reputation.","Domain reputation","Not IP reputation"),
   ("shield","Then it allows, blocks, or warns.","Policy actions","Allow, block, warn"),
   ("laptop","You can point a whole network at it, or use a roaming client.","Deployment options","DNS settings, appliance, client")]),
 TR("Three traps.",
  [("Umbrella is an on-site firewall","It's cloud-based","It's a cloud service."),
   ("Only clients are protected","Network-wide DNS works too","Pointing D N S at it protects the whole network."),
   ("It blocks by IP reputation","By domain reputation","It mainly uses domain reputation.")]),
 rc("Umbrella", [("Umbrella filters D N S in the cloud.","Cloud DNS filtering"),("It judges domain reputation.","Domain reputation"),("Use network D N S settings or a roaming client.","DNS settings or roaming client")]),
])

save("control-plane-policing", "Control Plane Policing", "CoPP", [
 H("shield", [("A bouncer at the VIP door",  "Think of a bouncer at the VIP door."),("Too many people at once",  "If everyone rushes in, the party stops.",RED),("CoPP limits the rush","Control plane policing limits the rush to the router's brain.",CY)]),
 S("The VIP bouncer", "CoPP protects the router's processor.",
  [("list","A class map picks out which traffic counts.","class-map","Matches with an ACL"),
   ("scale","A policy map says how fast it may arrive.","policy-map: police","Rate in bits per second"),
   ("door","You attach it under the control plane with service policy input.","control-plane","service-policy input"),
   ("lock","It only affects traffic sent to the router itself.","Control-plane traffic only","Not transit traffic")]),
 TR("Three traps.",
  [("CoPP filters transit traffic","Only traffic to the router","It only handles traffic to the router."),
   ("It's on by default","You must configure it","You have to configure it."),
   ("Rate is in packets per second","Bits per second","The rate is in bits per second.")]),
 rc("CoPP", [("CoPP protects the router's processor.","Protects the CPU"),("It uses class and policy maps.","Class map + policy map"),("It isn't on by default.","Not on by default")]),
])

save("ios-cli-show", "The Cisco CLI Modes", "IOS CLI", [
 H("building", [("An office building",  "Think of an office building with security."),("Floors you need a pass for",  "Each floor needs a higher pass.",CY),("IOS modes work the same way","I O S modes work the same way.",OR)]),
 S("The security levels", "You climb through the modes one at a time.",
  [("door","User mode ends with a greater than sign, and only allows basic checks.","User EXEC  >","Basic show and ping"),
   ("key","Type enable to reach privileged mode, which ends with a hash.","Privileged EXEC  #","enable"),
   ("gear","Configure terminal takes you to global configuration.","Global config  (config)#","configure terminal"),
   ("switch","From there, you enter interface or line modes.","Sub-modes  (config-if)#","Interface, line, router")]),
 TR("Three traps.",
  [("Config mode straight from user mode","Enable first","You must enable first."),
   ("Exit always goes to privileged","It goes back one level","Exit goes back one level."),
   ("Password and secret are the same","Secret wins","Enable secret takes priority.")]),
 rc("the CLI", [("Greater than is user mode, and hash is privileged.","> user; # privileged"),("Configure terminal enters global config.","configure terminal"),("Exit goes back one level.","exit = back one level")]),
])

save("ios-files-backup", "IOS Files and Backups", "IOS files", [
 H("book", [("A filing cabinet and a notepad",  "A router has a filing cabinet and a notepad."),("One survives a reboot",  "One survives a power cut.",CY),("One doesn't","The other doesn't.",RED)]),
 S("The cabinet and notepad", "Where things live decides whether they survive.",
  [("box","Flash holds the I O S image, and it survives a reboot.","Flash","Non-volatile, IOS image"),
   ("book","N V R A M holds the startup config, and it survives too.","NVRAM","startup-config"),
   ("clock","R A M holds the running config, and a reboot wipes it.","RAM","running-config, volatile"),
   ("gear","So always copy running config to startup config.","copy run start","Saves your work")]),
 T("Commands", "Three commands to remember.",
  [("dir flash:","List the files","List what's in flash."),
   ("copy running-config startup-config","Save changes","Save your changes."),
   ("show startup-config","What survives a reboot","And see what will survive a reboot.",CY)]),
 TR("Three traps.",
  [("Startup config lives in flash","NVRAM","Startup config is in N V R A M."),
   ("Config saves itself on exit","You must save","You have to save it yourself."),
   ("Delete frees space right away","It only marks the file","Delete just marks the file.")]),
 rc("IOS files", [("Running is in R A M, and startup is in N V R A M.","Running: RAM. Startup: NVRAM"),("Always copy run start.","copy run start"),("Flash holds the I O S image.","Flash = IOS image")]),
])

save("ios-upgrade-licensing", "Upgrading IOS", "IOS upgrade", [
 H("gear", [("Like a phone update",  "Upgrading a router is a lot like updating a phone."),("Download first",  "You download the new version first.",CY),("Then restart","Then you restart onto it.",OR)]),
 F("Upgrade steps", "Here's the sequence.",
  [("wrench","Check the current version.","show version","Version and uptime"),
   ("box","Check there's room in flash.","show flash:","Free space"),
   ("server","Copy the image from the server.","copy tftp: flash:","Source then destination"),
   ("gear","Set the boot variable to the new file.","boot system flash:","Before reload"),
   ("clock","Save, then reload.","copy run start; reload","Reload asks to confirm")]),
 TR("Three traps.",
  [("copy tftp flash goes to the server","From the server to flash","Source first, then destination."),
   ("Overwrite the old file to upgrade","Set the boot variable","Set the boot variable to the new file."),
   ("Reload is instant","It asks for confirmation","Reload asks first, and can be cancelled.")]),
 rc("IOS upgrades", [("Copy the image, then set the boot variable.","Copy image; set boot variable"),("Source comes before destination.","copy source destination"),("Save before you reload.","Save, then reload")]),
])

save("boot-process", "Router Boot Process", "Boot process", [
 H("clock", [("A phone starting up",  "A router starts up much like a smartphone."),("Step by step",  "It goes through a set order of steps.",CY),("Learn the order","The order is easy to learn.",OR)]),
 F("Boot order", "Here's what happens.",
  [("gear","The hardware test runs, called P O S T.","POST","Hardware check"),
   ("key","The bootloader starts, called R O M mon.","ROMMON","Bootloader"),
   ("box","It finds the I O S image.","Locate IOS","Flash by default"),
   ("router","It loads the I O S.","Load IOS","Into RAM"),
   ("book","Then it reads the startup config.","Load startup-config","From NVRAM")]),
 T("The config register", "A single register steers it.",
  [("0x2102","Default: boot from flash","The default is zero x two one oh two."),
   ("0x2142","Ignore startup config","Zero x two one four two ignores the saved config, for password recovery."),
   ("0x2100","Stay in ROMMON","And zero x two one zero zero stays in ROM mon.",CY)]),
 TR("Three traps.",
  [("POST loads the IOS","POST tests hardware","P O S T only tests the hardware."),
   ("Register is in the running config","It's separate","The register is stored separately."),
   ("BOOT variable = register","Different things","The boot variable and the register are different.")]),
 rc("booting", [("P O S T, then R O M mon, then I O S, then config.","POST, ROMMON, IOS, config"),("Zero x two one zero two is the default.","0x2102 default"),("Zero x two one four two skips the config.","0x2142 skips startup config")]),
])
