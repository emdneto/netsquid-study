import yaml
import networkx as nx
from netsquid.nodes import Node
from netsquid.components import QuantumMemory
from netsquid.components import Channel, QuantumChannel
from netsquid.components.models import DelayModel
from pprint import pprint

G = nx.Graph()
yaml_file = open("descriptor.yaml", 'r')
sim_config = yaml.load(yaml_file, Loader=yaml.FullLoader)
qnodes = sim_config['general']['nodes']
length = sim_config['general']['distance'] / 1000

class PingPongDelayModel(DelayModel):
    def __init__(self, speed_of_light_fraction=0.5, standard_deviation=0.05):
        super().__init__()
        # (the speed of light is about 300,000 km/s)
        self.properties["speed"] = speed_of_light_fraction * 3e5
        self.properties["std"] = standard_deviation
        self.required_properties = ['length']  # in km

    def generate_delay(self, **kwargs):
        avg_speed = self.properties["speed"]
        std = self.properties["std"]
        speed = self.properties["rng"].normal(avg_speed, avg_speed * std)
        delay = 1e9 * kwargs['length'] / speed  # in nanoseconds
        return delay

nodes = [Node(name=f'n{i}') for i in range(1, qnodes+1)]
edges = []

for node in nodes:
    print(node.uid)

for i in range(qnodes-1):
    src = nodes[i].name
    dst = nodes[i+1].name
    qlink_1 = (src, dst)
    qlink_2 = (dst, src)
    edges.append(qlink_1)
    edges.append(qlink_2)
    print(qlink_1, qlink_2)


    
#qchannels_fwd = [QuantumChannel(name=f'{nodes[i].name}->{nodes[i+1].name}', length=length, models={"delay_model": PingPongDelayModel()}) for i in range(qnodes-1)]
#qchannels_fwd = [QuantumChannel(name=f'n{i}->n{i+1}', length=length, models={"delay_model": PingPongDelayModel()}) for i in range(1, qnodes)]
#qchannels_bck = [QuantumChannel(name=f'n{i+1}->n{i}', length=length, models={"delay_model": PingPongDelayModel()}) for i in range(1, qnodes)]
#print(qchannels_fwd)

G.add_nodes_from(nodes)
G.add_edges_from(edges)
#G.add_edges_from(qchannels_bck)
#G.add_edges_from(qchannels_fwd)
#print(G.nodes())
print(G)
#print(qchannels_fwd)

