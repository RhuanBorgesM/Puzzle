from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial.tiles}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            state = frontier.popleft()
            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated,
                                    max_frontier_size, state.cost)

            nodes_expanded += 1
            for child in state.neighbors():
                if child.tiles not in visited:
                    visited.add(child.tiles)
                    frontier.append(child)
                    nodes_generated += 1
            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
