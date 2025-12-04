# keyboard_graph.py
from collections import defaultdict

def build_qwerty_graph(include_shifted=True):
    """Builds an undirected keyboard adjacency graph.
    Nodes are characters; edges connect physically adjacent keys.
    Returns: dict node -> set(neighbors)
    """
    rows = [
        "`1234567890-=",
        "qwertyuiop[]\\",
        "asdfghjkl;'",
        "zxcvbnm,./"
    ]
    shifted = {
        '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^',
        '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+',
        '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
    }

    positions = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            positions[ch] = (r, c)
            if include_shifted and ch in shifted:
                positions[shifted[ch]] = (r, c)

    G = defaultdict(set)
    # connect neighbors within manhattan neighborhood (-1..1)
    for ch, (r, c) in positions.items():
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                for other, pos in positions.items():
                    if pos == (nr, nc):
                        G[ch].add(other)
                        G[other].add(ch)

    # normalize alphabet cases: ensure both lower & upper exist
    for ch in list(G.keys()):
        if ch.isalpha():
            low = ch.lower()
            up = ch.upper()
            G[low] = set(x.lower() if x.isalpha() else x for x in G[ch])
            G[up] = set(x.upper() if x.isalpha() else x for x in G[ch])

    return dict(G)
