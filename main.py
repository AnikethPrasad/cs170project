from starter import *
import random

def solve(G: nx.Graph):
    # TODO implement this function with your solver
    # Assign a team to v with G.nodes[v]['team'] = team_id
    # Access the team of v with team_id = G.nodes[v]['team']
    for i in range(G.number_of_nodes()):
        G.nodes[i]['team'] = random.randint(1,8)
    

G = read_input('./inputs/small1.in')
print(G.nodes[0])
solve(G)
validate_output(G)
visualize(G)
score(G)

#Test accuracy
run(solve, './inputs/small1.in', 'small1.out', overwrite=True)

#Run all cases
# run_all(solve, 'input', 'output')
# tar('output')

   
'''
Ideas:

    Algorithm:
    1. Preprocess (sort by # of neighbors, edge weight) + Add node by node with greedy approach, assign current node to best possible team. O(V^2)
    2. Generate team assignments (randomly or w/greedy?), move nodes until satisfied.
    3. f(nodes) nodes = list of nodes        min_cost(for i in range(len(nodes)): f(nodes \ {i}))
    4. divide n concor?
    5. multiplicative weights with multiple algorithms 😮

'''