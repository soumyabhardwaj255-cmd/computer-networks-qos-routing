"""Generate the default teaching topology and Packet Tracer configuration files."""
import json
from pathlib import Path
root = Path(__file__).resolve().parent
positions = {'R1':[0,0],'R2':[2,0],'R3':[4,0],'R12':[6,0],
             'R4':[1,2],'R5':[3,2],'R6':[5,2],
             'R7':[1,-2],'R8':[3,-2],'R9':[5,-2], 'R10':[2,3.5],'R11':[4,3.5]}
links = []
for a,b in [('R1','R2'),('R2','R3'),('R3','R12'),('R1','R4'),('R4','R5'),
            ('R5','R6'),('R6','R12'),('R1','R7'),('R7','R8'),('R8','R9'),
            ('R9','R12'),('R4','R10'),('R10','R11'),('R11','R6'),('R2','R5'),('R3','R8')]:
    core = (a,b) in [('R1','R2'),('R2','R3'),('R3','R12')]
    links.append(dict(a=a,b=b,bandwidth_mbps=10 if core else 20,
                      delay_ms=1 if core else 2,loss=.001,utilization=.15,core=core))
c = dict(seed=30806,trials=30,packets=1000,packet_bytes=1200,packets_per_second=25,
         delay_reference_ms=20,loss_reference=.1,congestion_loss_factor=.12,
         weights=dict(delay=.4,loss=.3,utilization=.2,hops=.1),
         conditions=dict(normal=.1,moderate=.7,high=.95),
         pairs=[['R1','R12'],['R2','R12'],['R1','R3']],positions=positions,links=links)
(root/'config.json').write_text(json.dumps(c,indent=2))
folder = root/'packet_tracer'
folder.mkdir(exist_ok=True)
ports = {
 'R1':[('GigabitEthernet0/0','10.0.12.1'),('GigabitEthernet0/1','10.0.13.1'),('GigabitEthernet0/2','192.168.1.1')],
 'R2':[('GigabitEthernet0/0','10.0.12.2'),('GigabitEthernet0/1','10.0.24.1')],
 'R3':[('GigabitEthernet0/0','10.0.13.2'),('GigabitEthernet0/1','10.0.34.1')],
 'R4':[('GigabitEthernet0/0','10.0.24.2'),('GigabitEthernet0/1','10.0.34.2'),('GigabitEthernet0/2','192.168.4.1')]}
for router, interfaces in ports.items():
    lines=['enable','configure terminal','hostname '+router,'no ip domain-lookup']
    for interface,ip in interfaces:
        lines += ['interface '+interface, 'ip address '+ip+(' 255.255.255.0' if ip.startswith('192') else ' 255.255.255.252'),
                  'ip ospf cost '+('30' if '13.' in ip or '34.' in ip else '10'),'no shutdown','exit']
    lines += ['router ospf 1','network 10.0.0.0 0.255.255.255 area 0','network 192.168.0.0 0.0.255.255 area 0','end','write memory']
    (folder/(router+'.txt')).write_text('\n'.join(lines)+'\n')
