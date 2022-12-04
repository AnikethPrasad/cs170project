from starter import *
import random, math, numpy as np
cost = float('inf')
curr_cost = 0
cw = 0
ck = 0
cp = 0
better_team_size = 0
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
    temp = cw
    for node, info in G.adj[u].items():
        if G.nodes[node]['team'] == old_team:
            temp = temp - info['weight']
        elif G.nodes[node]['team'] == new_team:
            temp = temp + info['weight']
    return temp       
    
def updated_cost(G: nx.graph, node, new_team, separated=False):
    global cw, ck, cp, better_team_size
    old_team = G.nodes[node]['team']
    output = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
    teams, counts = np.unique(output, return_counts=True)
    k = np.max(teams)
    b_vec = (counts / G.number_of_nodes()) - 1 / k
    temp_cw = new_cw(G, node, old_team, new_team)
    new_cp(G, b_vec, old_team, new_team)
    if separated:
        return temp_cw, ck, cp
    return temp_cw, temp_cw + ck + cp


def getSortedEdgeWeightSum(G) -> dict:
    node_edge_weight_sums = {}
    for i in range(G.number_of_nodes()):
        node_edge_weight_sums[i] = sum(e[1] for e in G.edges(i))
    s = sorted(node_edge_weight_sums, key=lambda x:node_edge_weight_sums[x], reverse=True)
    return s

def build_better_graph(G: nx.graph):
    global better_team_size
    for i in range(G.number_of_nodes()):
        G.nodes[i]['team'] = 1
    better_team_size = int(G.number_of_nodes() // (10 + random.uniform(0.05, 0.1) * G.number_of_nodes()))
    return G, better_team_size

def build_graph(G: nx.Graph, size = None):
    # n = getSortedEdgeWeightSum(G)
    print(G, size)
    best_graph = G.copy()
    best_cost = float('inf')
    best_team = -1
    team_size = size
    for i in range(G.number_of_nodes()):
        G.nodes[i]['team'] = random.randint(1,team_size+1)
    x = score(G)
    best_graph = G.copy()
    return best_graph, team_size
    if x < best_cost:
        best_graph = G.copy()
        best_cost = x
        best_team = team_size
    return best_graph, best_team

def solve(G: nx.Graph, size = None):
    # TODO implement this function with your solver
    # Assign a team to v with G.nodes[v]['team'] = team_id
    # Access the team of v with team_id = G.nodes[v]['team']
    # sorted_nodes = getSortedEdgeWeightAverage(G)
    # print(sorted_nodes)
    g, TEAM_SIZE = build_graph(G, size)
    global cw, ck, cp
    #are we sure this is the order of score?
    
    cw, ck, cp = score(g, separated=True)
    curr_cost = score(g)
    
    print("INIT",curr_cost, cw)
    prev_cost = float('inf')
    best_node = -1
    best_team = -1
    while prev_cost > curr_cost:
        # do best swap
        prev_cost = curr_cost
        for n in range(g.number_of_nodes()):
            for t in range(1,TEAM_SIZE+1):
                if g.nodes[n]['team'] == t:
                    continue
                curr_cw, new_cost = updated_cost(g,n,t)
                if new_cost < curr_cost:
                    curr_cost = new_cost
                    best_node = n
                    best_team = t
                    best_cw = curr_cw
        g.nodes[best_node]["team"] = best_team
        cw = best_cw
    print("FINAL",score(g))
    G.update(g)
    return g
# G = read_input('./inputs/small1.in')
# # build_graph(G)
# solve(G)
# validate_output(G)
# # visualize(G)
# score(G)

# #Test accuracy
# run(solve, './inputs/small1.in', 'small1.out', overwrite=True)

# #Run all cases
def main():
    args = run_all(solve, './inputs', 'output')
    try:
        with Pool(10) as pool:
            pool.starmap(run, args)
    except Exception as e:
        print(e)
        main()
    tar('output')
    main()

if __name__ == "__main__":
    main()

    
'''
Ideas:

    Algorithm:
    1. Preprocess (sort by # of neighbors, edge weight) + Add node by node with greedy approach, assign current node to best possible team.
    2. Generate team assignments (randomly or w/greedy?), move nodes until satisfied.
    3. f(nodes) nodes = list of nodes        min_cost(for i in range(len(nodes)): f(nodes \ {i}))
    4. divide n concor?
    5. multiplicative weights with multiple algorithms 😮

'''