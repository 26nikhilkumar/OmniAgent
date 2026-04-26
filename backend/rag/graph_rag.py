import networkx as nx


class CoOccurrenceGraph:
    def __init__(self) -> None:
        self.graph = nx.Graph()

    def add_chunk(self, chunk: str) -> None:
        tokens = [t.strip(".,!?:;()[]{}\"'").lower() for t in chunk.split()]
        terms = [t for t in tokens if len(t) > 3]
        for i in range(len(terms) - 1):
            a, b = terms[i], terms[i + 1]
            if a == b:
                continue
            self.graph.add_edge(a, b, weight=self.graph.get_edge_data(a, b, {}).get("weight", 0) + 1)

    def related_terms(self, term: str, depth: int = 1) -> list[str]:
        term = term.lower()
        if term not in self.graph:
            return []
        frontier = {term}
        visited = {term}
        for _ in range(depth):
            nxt = set()
            for node in frontier:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        nxt.add(neighbor)
            frontier = nxt
        visited.remove(term)
        return sorted(visited)
