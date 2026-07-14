import random

def sample_network(num_nodes):

    edges = []

    in_deg = [0] * num_nodes
    out_deg = [0] * num_nodes

    for tail in range(num_nodes - 1):
        if in_deg[tail] == 2:
            if in_deg[tail + 1] == 0:
                edges.append((tail, tail + 1))
                in_deg[tail + 1] += 1
                out_deg[tail] += 1
            else:
                head = random.randint(tail + 1, num_nodes)
                while head != num_nodes and in_deg[head] > 1:
                    head = random.randint(tail + 1, num_nodes)
                if head == num_nodes:
                    continue
                edges.append((tail, head))
                in_deg[head] += 1
                out_deg[tail] += 1
        else:
            if in_deg[tail + 1] == 0:
                edges.append((tail, tail + 1))
                in_deg[tail + 1] += 1
                out_deg[tail] += 1
                head = random.randint(tail + 2, num_nodes)
                while head != num_nodes and in_deg[head] > 1:
                    head = random.randint(tail + 2, num_nodes)
                if head == num_nodes:
                    continue
                edges.append((tail, head))
                in_deg[head] += 1
                out_deg[tail] += 1
            else:
                head = random.randint(tail + 1, num_nodes)
                while head != num_nodes and in_deg[head] > 1:
                    head = random.randint(tail + 1, num_nodes)
                if head == num_nodes:
                    continue
                edges.append((tail, head))
                in_deg[head] += 1
                out_deg[tail] += 1
                head2 = head
                while head2 == head or (head2 != num_nodes and in_deg[head2] > 1):
                    head2 = random.randint(tail + 1, num_nodes)
                if head2 == num_nodes:
                    continue
                edges.append((tail, head2))
                in_deg[head2] += 1
                out_deg[tail] += 1
    
    return edges

    for x in in_deg:
        if x > 2:
            print("Error: in-degree greater than 2")

def ContainedTree(num_nodes, edges):
    adj_list = [[] for _ in range(num_nodes)]
    for tail, head in edges:
        adj_list[tail].append(head)
    
    visited = [False] * num_nodes
    ans = []
    def dfs(node, from_node):
        visited[node] = True
        if len(adj_list[node]) == 0:
            ans.append((from_node, node))
            return

        if from_node == node:
            for to in adj_list[node]:
                if not visited[to]:
                    dfs(to, node)
            return
        u = 0 if random.random() < 0.70 else 1
        if u == 0:
            to = random.choice(adj_list[node])
            if not visited[to]:
                dfs(to, from_node)
        else:
            ans.append((from_node, node))
            dfs(node, node)

    dfs(0, 0)
    return ans

def ContainedBadTree(edges):
    new_edges = edges.copy()

    i = random.randint(0, len(edges) - 1)
    new_edges[i] = (edges[i][1], edges[i][0])

    return new_edges

def generate_multiple_files(num_files):
    for k in range(1, num_files + 1):
        num_nodes = random.randint(5, 50)
        
        network_edges = sample_network(num_nodes)
        with open(f"n{k}.txt", 'w') as f:
            for tail, head in network_edges:
                f.write(f"{tail} {head}\n")
        
        tree_edges = ContainedTree(num_nodes, network_edges)
        with open(f"t{k}.txt", 'w') as f:
            for tail, head in tree_edges:
                f.write(f"{tail} {head}\n")

        bad_tree_edges = ContainedBadTree(tree_edges)
        with open(f"bt{k}.txt", 'w') as f:
            for tail, head in bad_tree_edges:
                f.write(f"{tail} {head}\n")

        print('finished generating files for test case', k)

generate_multiple_files(300)