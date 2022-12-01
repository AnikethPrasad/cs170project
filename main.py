from starter import *
import random, math, numpy as np
from collections import deque

cost = float('inf')
curr_cost = 0
cw = 0
ck = 0
cp = 0

def new_cp(G: nx.graph, b, old_team, new_team, return_b=False):
    global cp
    v = G.number_of_nodes()
    new_b = np.copy(b)
    new_b[old_team - 1] -= 1 / v
    new_b[new_team - 1] += 1 / v
    if return_b:
        return math.exp(B_EXP * np.linalg.norm(new_b, 2)), new_b
    cp = math.exp(B_EXP * np.linalg.norm(new_b, 2))

def new_cw(G, u, old_team, new_team):
    global cw
    for node, info in G.adj[u].items():
        if G.nodes[node]['team'] == old_team:
            cw = cw - info['weight']
        elif G.nodes[node]['team'] == new_team:
            cw = cw + info['weight']
            
def updated_cost(G: nx.graph, node, new_team):
    global cw, ck, cp
    old_team = G.nodes[node]['team']
    output = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
    teams, counts = np.unique(output, return_counts=True)
    k = np.max(teams)
    b_vec = (counts / G.number_of_nodes()) - 1 / k
    new_cw(G, node, old_team, new_team)
    new_cp(G, b_vec, old_team, new_team)
    return cw + ck + cp


def getSortedEdgeWeightAverage(G) -> dict:
    
    node_edge_weight_sums = {}
    for i in range(G.number_of_nodes()):
        node_edge_weight_sums[i] = sum(e[1] for e in G.edges(i))
    s = sorted(node_edge_weight_sums, key=lambda x:node_edge_weight_sums[x])
    return s


def solve(G: nx.Graph):
    # TODO implement this function with your solver
    # Assign a team to v with G.nodes[v]['team'] = team_id
    # Access the team of v with team_id = G.nodes[v]['team']
    # sorted_nodes = getSortedEdgeWeightAverage(G)
    # print(sorted_nodes)
    TEAM_SIZE = 10
    global cw, ck, cp
    for i in range(G.number_of_nodes()):
        G.nodes[i]['team'] = random.randint(1,TEAM_SIZE+1)
    #are we sure this is the order of score?
    cw, ck, cp = score(G, separated=True)
    curr_cost = score(G)
    
    print("INIT",curr_cost)
    prev_cost = float('inf')
    best_node = -1
    best_team = -1
    while prev_cost > curr_cost :
        # do best swap
        prev_cost = curr_cost
        for n in range(G.number_of_nodes()):
            for t in range(1,TEAM_SIZE+1):
                if G.nodes[n]['team'] == t:
                    continue
                new_cost = updated_cost(G,n,t)
                if new_cost < curr_cost:
                    curr_cost = new_cost
                    best_node = n
                    best_team = t
                curr_cost = min(curr_cost, updated_cost(G, n, t))
        G.nodes[best_node]["team"] = best_team
    print("FINAL",score(G))

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