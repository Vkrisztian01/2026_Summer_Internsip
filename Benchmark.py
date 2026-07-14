import time
import infrared as ir
from A_Graphs import Graph

def run_tree_containment(network_file, tree_file):
    try:
        g = Graph(network_file)
        mapping = g.get_mapping()
        t = Graph(tree_file)
        g.rewrite_edges(mapping)
        t.rewrite_edges(mapping)
        
        N, num_edges, num_nodes = g.get_graph()
        T, num_colors, _ = t.get_graph()

        model = ir.Model()
        model.add_variables(num_edges + 1, num_colors + 1)

        ir.def_constraint_class("DummyDeclaration",
                                lambda x, y: [x],
                                lambda x_c, y: x_c == y )

        ir.def_constraint_class("StartOne",
                            lambda x, y, color: [x, y],
                            lambda x_c, y_c, color: [x_c, y_c].count(color) == 1 or color == num_colors)

        ir.def_constraint_class("Continuation",
                            lambda edge, prev1, prev2, c1, c2: [edge, prev1, prev2],
                            lambda color, p_c1, p_c2, c1, c2: (color not in [p_c1, p_c2] and color in [c1, c2] ) or ([p_c1, p_c2].count(color) == 1 and color not in [c1, c2]) or (color == num_colors) 
                            )

        model.add_constraints(DummyDeclaration(num_edges, num_colors))

        to_edges = [[] for _ in range(num_nodes)]
        from_edges = [[] for _ in range(num_nodes)]
        leaving_colors = [[] for _ in range(num_nodes)]
        incoming_colors = [[] for _ in range(num_nodes)]

        for idx, edge in enumerate(N):
            to_edges[edge[1]].append(idx)
            from_edges[edge[0]].append(idx)

        for idx, edge in enumerate(T):
            leaving_colors[edge[0]].append(idx)
            incoming_colors[edge[1]].append(idx)

        for i in range(num_nodes):
            while len(to_edges[i]) < 2: to_edges[i].append(num_edges)
            while len(from_edges[i]) < 2: from_edges[i].append(num_edges)
            while len(leaving_colors[i]) < 2: leaving_colors[i].append(num_colors)
            while len(incoming_colors[i]) < 2: incoming_colors[i].append(num_colors)

        for idx, (tail, head) in enumerate(N):
            fr = to_edges[tail]
            to = from_edges[head]
            col = leaving_colors[tail]
            model.add_constraints(Continuation(idx, fr[0], fr[1], col[0], col[1]))
            col = incoming_colors[head]
            model.add_constraints(Continuation(idx, to[0], to[1], col[0], col[1]))

        for node in range(num_nodes):
            model.add_constraints(StartOne(from_edges[node][0], from_edges[node][1], leaving_colors[node][0]))
            model.add_constraints(StartOne(from_edges[node][0], from_edges[node][1], leaving_colors[node][1]))

        solver = ir.Sampler(model)
        assignment = solver.sample()
        return "YES", num_nodes
        
    except Exception:
        return "NO", num_nodes


# =====================================================================
# BENCHMARK RUNNER & FILE WRITER
# =====================================================================
print(f"{'Test ID':<10}{'Contained':<12}{'Bad Tree':<12}{'Time1 (s)':<10}{'Time2 (s)':<10}")
print("-" * 55)

with open("results.txt", "w") as txt_file:
    for i in range(1, 301):
        net_file = f"n{i}.txt"
        good_tree = f"t{i}.txt"
        bad_tree = f"bt{i}.txt"
        
        # 1. Test Network + Contained Tree
        start1 = time.perf_counter()
        ans1, num_nodes = run_tree_containment(net_file, good_tree)
        end1 = time.perf_counter()
        runtime1 = end1 - start1
        
        # 2. Test Network + Non-contained Tree
        start2 = time.perf_counter()
        ans2, num_nodes = run_tree_containment(net_file, bad_tree)
        end2 = time.perf_counter()
        runtime2 = end2 - start2
        
        # Terminal display (aligned columns)
        print(f"{i:<10}{ans1:<12}{ans2:<12}{runtime1:.4f}     {runtime2:.4f}")
        
        # Write format: <num_nodes> <ans1> <ans2> <runtime1> <runtime2>
        txt_file.write(f"{num_nodes} {ans1} {ans2} {runtime1:.4f} {runtime2:.4f}\n")

print("\nBenchmarking complete! Results successfully saved to 'results.txt'.")
