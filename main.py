from starter import *
import random
from collections import deque

def updated_cost(new_node, new_team):
    pass
def getSortedEdgeWeightAverage(G) -> dict:
    node_edge_weight_sums = {}
    for i in range(G.number_of_nodes()):
        node_edge_weight_sums[i] = sum(e[1] for e in G.edges(i))
    s = sorted(node_edge_weight_sums, key=lambda x:node_edge_weight_sums[x])
    print([node_edge_weight_sums[n] for n in s])
    return s


def solve(G: nx.Graph):
    # TODO implement this function with your solver
    # Assign a team to v with G.nodes[v]['team'] = team_id
    # Access the team of v with team_id = G.nodes[v]['team']
    sorted_nodes = getSortedEdgeWeightAverage(G)
    print(sorted_nodes)

    for i in range(G.number_of_nodes()):
        G.nodes[i]['team'] = random.randint(1,8)
    

G = read_input('./inputs/small1.in')
print(G.nodes[0])
solve(G)
validate_output(G)
visualize(G)
score(G)

# #Test accuracy
# run(solve, './inputs/small1.in', 'small1.out', overwrite=True)

# #Run all cases
# run_all(solve, './inputs', 'output')
# tar('output')

   
'''
Ideas:

    Algorithm:
    1. Preprocess (sort by # of neighbors, edge weight) + Add node by node with greedy approach, assign current node to best possible team.
    2. Generate team assignments (randomly or w/greedy?), move nodes until satisfied.
    3. f(nodes) nodes = list of nodes        min_cost(for i in range(len(nodes)): f(nodes \ {i}))
    4. divide n concor?
    5. multiplicative weights with multiple algorithms 😮

'''