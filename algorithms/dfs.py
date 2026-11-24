from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        best_depth = {initial.tiles: 0}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            state = frontier.pop()
            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated,
                                    max_frontier_size, state.cost)
            if state.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            # Reversão para que a primeira direção da lista seja explorada
            # primeiro pela pilha LIFO.
            for child in reversed(state.neighbors()):
                depth = child.cost
                previous_depth = best_depth.get(child.tiles)
                if previous_depth is None or depth < previous_depth:
                    best_depth[child.tiles] = depth
                    frontier.append(child)
                    nodes_generated += 1
            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
