# password_analyzer.py
import math
from collections import defaultdict
from .keyboard_graph import build_qwerty_graph

class PasswordAnalyzer:
    def __init__(self, graph=None):
        self.graph = graph or build_qwerty_graph()

    def induced_subgraph(self, pw):
        nodes = set(pw)
        edges = set()
        adj = defaultdict(set)
        for i in range(len(pw)-1):
            a, b = pw[i], pw[i+1]
            if b in self.graph.get(a, ()):  # adjacent on keyboard
                edge = tuple(sorted((a, b)))
                edges.add(edge)
                adj[a].add(b)
                adj[b].add(a)
            else:
                adj.setdefault(a, set())
                adj.setdefault(b, set())
        return nodes, edges, dict(adj)

    def adjacency_ratio(self, pw):
        if len(pw) <= 1:
            return 0.0
        adj_count = 0
        for i in range(len(pw)-1):
            if pw[i+1] in self.graph.get(pw[i], ()):
                adj_count += 1
        return adj_count / max(1, (len(pw)-1))

    def longest_simple_path_segment(self, pw):
        best_len = 1
        best_seg = pw[0] if pw else ""
        n = len(pw)
        for i in range(n):
            visited = set([pw[i]])
            cur_len = 1
            j = i
            while j+1 < n and pw[j+1] in self.graph.get(pw[j], ()) and pw[j+1] not in visited:
                visited.add(pw[j+1])
                cur_len += 1
                j += 1
            if cur_len > best_len:
                best_len = cur_len
                best_seg = pw[i:i+cur_len]
        return best_len, best_seg

    def avg_log_degree(self, pw):
        if not pw:
            return 0.0
        s = 0.0
        for ch in pw:
            deg = max(0, len(self.graph.get(ch, [])))
            s += math.log(deg + 1)
        return s / len(pw)

    def greedy_vertex_cover(self, nodes, edges):
        edges = set(edges)
        cover = set()
        adj_e = defaultdict(set)
        for u, v in edges:
            adj_e[u].add((u, v))
            adj_e[v].add((u, v))
        while edges:
            # pick node with maximum incident edges
            node = max(nodes, key=lambda x: len(adj_e.get(x, set())))
            cover.add(node)
            for e in list(adj_e.get(node, set())):
                if e in edges:
                    edges.remove(e)
                    u, v = e
                    if e in adj_e[u]:
                        adj_e[u].remove(e)
                    if e in adj_e[v]:
                        adj_e[v].remove(e)
            adj_e[node] = set()
        return cover

    def variety_score(self, pw):
        classes = 0
        if any(c.islower() for c in pw): classes += 1
        if any(c.isupper() for c in pw): classes += 1
        if any(c.isdigit() for c in pw): classes += 1
        if any((not c.isalnum()) for c in pw): classes += 1
        return classes / 4.0

    def length_score(self, pw, target=12):
        L = len(pw)
        if L <= 4:
            return 0.0
        return min(1.0, (L - 4) / max(1, (target - 4)))

    def analyze(self, pw):
        nodes, edges, induced_adj = self.induced_subgraph(pw)
        adj_ratio = self.adjacency_ratio(pw)
        path_len, path_seg = self.longest_simple_path_segment(pw)
        avg_lndeg = self.avg_log_degree(pw)
        cover = self.greedy_vertex_cover(nodes, edges)
        vc_ratio = len(cover) / max(1, len(nodes))
        var = self.variety_score(pw)
        lscore = self.length_score(pw)
        path_score = path_len / max(1, len(pw))

        final = 100 * (
            0.35 * var
            + 0.25 * lscore
            + 0.20 * (1 - adj_ratio)
            + 0.10 * (1 - path_score)
            + 0.10 * (1 - vc_ratio)
        )

        if final < 30:
            rating = "very weak"
        elif final < 50:
            rating = "weak"
        elif final < 70:
            rating = "moderate"
        elif final < 85:
            rating = "strong"
        else:
            rating = "very strong"

        trace = {
            "password": pw,
            "length": len(pw),
            "variety_score": var,
            "length_score": lscore,
            "adjacency_ratio": adj_ratio,
            "longest_simple_path_length": path_len,
            "longest_path_segment": path_seg,
            "avg_log_degree": avg_lndeg,
            "induced_nodes": list(nodes),
            "induced_edges": [list(e) for e in edges],
            "vertex_cover": list(cover),
            "vc_ratio": vc_ratio,
            "final_score": final,
            "rating": rating
        }
        return trace
