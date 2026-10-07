"""Small three-terminal cubic gadgets and reproducible model expansion.

Requires NetworkX. Vertex labels of expanded graphs are one-based.
A cell's first terminal is the distinguished terminal.
"""
from __future__ import annotations
from pathlib import Path
import json
from typing import Any
import networkx as nx


def cell(size: int) -> tuple[nx.Graph, list[int]]:
    if size == 3:
        return nx.cycle_graph(3), [0, 1, 2]
    if size == 7:
        edges = [(0, 2), (0, 5), (1, 2), (2, 3), (3, 1),
                 (4, 5), (5, 6), (6, 4), (3, 6)]
        return nx.Graph(edges), [0, 1, 4]
    if size == 15:
        small, _ = cell(7)
        graph = nx.Graph()
        graph.add_nodes_from(range(15))
        for offset in (1, 8):
            graph.add_edges_from((u + offset, v + offset)
                                 for u, v in small.edges())
        graph.add_edges_from([(0, 2), (0, 9), (5, 12)])
        return graph, [0, 1, 8]
    raise ValueError(f"Unsupported cell size: {size}")


def expand(core: nx.Graph, choices: dict[int, tuple[int, int]]) -> nx.Graph:
    """choices[v] = (cell size, neighbour attached to distinguished terminal)."""
    if not core or any(d != 3 for _, d in core.degree()):
        raise ValueError("The core must be a simple cubic graph")
    graph = nx.Graph()
    ports: dict[tuple[int, int], int] = {}
    offset = 1
    for u in sorted(core):
        size, special = choices[u]
        template, terminals = cell(size)
        neighbours = sorted(core[u])
        if special not in neighbours:
            raise ValueError(f"Invalid distinguished neighbour at {u}")
        graph.add_nodes_from(range(offset, offset + size))
        graph.add_edges_from((a + offset, b + offset)
                             for a, b in template.edges())
        order = [special] + [v for v in neighbours if v != special]
        for v, terminal in zip(order, terminals):
            ports[u, v] = offset + terminal
        offset += size
    for u, v in core.edges():
        graph.add_edge(ports[u, v], ports[v, u])
    if any(d != 3 for _, d in graph.degree()):
        raise AssertionError("Expansion did not preserve cubicity")
    return graph


def load_model(path: Path) -> tuple[nx.Graph, dict[int, tuple[int, int]]]:
    data = json.loads(path.read_text())
    core = nx.Graph()
    core.add_edges_from(data["core_edges"])
    choices = {int(v): (int(value[0]), int(value[1]))
               for v, value in data["choices"].items()}
    return core, choices


def load_core(path: Path) -> tuple[nx.Graph, dict[int, tuple[int, int]]]:
    rows = path.read_text().splitlines()
    n = int(rows[0])
    data = [list(map(int, line.split())) for line in rows[1:] if line.strip()]
    if len(data) != n:
        raise ValueError("Wrong row count in .core file")
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    choices = {}
    for u, row in enumerate(data):
        if len(row) != 5:
            raise ValueError("A .core row must contain five integers")
        kind, special_slot, *neighbours = row
        if kind not in (0, 1) or special_slot not in (0, 1, 2):
            raise ValueError("Invalid cell type or special slot")
        if len(set(neighbours)) != 3 or u in neighbours:
            raise ValueError("Core is not simple")
        choices[u] = (7 if kind else 3, neighbours[special_slot])
        graph.add_edges_from((u, v) for v in neighbours)
    if any(d != 3 for _, d in graph.degree()):
        raise ValueError("Core is not cubic")
    return graph, choices


def read_dimacs(path: Path) -> nx.Graph:
    graph = nx.Graph()
    n = m = None
    for line in path.read_text().splitlines():
        fields = line.split()
        if not fields or fields[0] == 'c':
            continue
        if fields[0] == 'p':
            _, _, ns, ms = fields
            n, m = int(ns), int(ms)
            graph.add_nodes_from(range(1, n + 1))
        elif fields[0] == 'e':
            a, b = map(int, fields[1:])
            if a == b or graph.has_edge(a, b):
                raise ValueError("Loop or duplicate edge")
            graph.add_edge(a, b)
        else:
            raise ValueError(f"Unknown DIMACS record: {line}")
    if n is None or len(graph) != n or graph.number_of_edges() != m:
        raise ValueError("DIMACS header disagrees with graph")
    return graph


def write_dimacs(graph: nx.Graph, path: Path) -> None:
    edges = sorted(tuple(sorted(edge)) for edge in graph.edges())
    path.write_text(f"p edge {len(graph)} {len(edges)}\n" +
                    ''.join(f"e {u} {v}\n" for u, v in edges))


def bounded_cycles(graph: nx.Graph, limit: int):
    """Canonical DFS, independent of NetworkX's simple_cycles implementation."""
    neighbours = {u: sorted(graph[u]) for u in graph}
    def dfs(root, first, path, used):
        u = path[-1]
        if len(path) >= 3 and root in neighbours[u] and first < u:
            yield tuple(path)
        if len(path) >= limit:
            return
        for v in neighbours[u]:
            if v > root and v not in used:
                yield from dfs(root, first, path + [v], used | {v})
    for root in sorted(graph):
        for first in neighbours[root]:
            if first > root:
                yield from dfs(root, first, [root, first], {root, first})
