import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância Manhattan (sem contar o espaço vazio), admissível."""
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            row, col = divmod(index, 3)
            goal_row, goal_col = divmod(goal_index, 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        # Entradas inválidas (paridade ímpar) não podem alcançar o objetivo.
        inversions = sum(
            1 for i, tile in enumerate(initial.tiles) if tile
            for other in initial.tiles[i + 1:] if other and tile > other
        )
        if inversions % 2:
            return SearchResult(None, nodes_generated=1, max_frontier_size=1)

        counter = 0
        frontier = [(self.heuristic(initial), counter, initial)]
        best_cost = {initial.tiles: initial.cost}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            _, _, state = heapq.heappop(frontier)
            if state.cost != best_cost.get(state.tiles):
                continue
            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated,
                                    max_frontier_size, state.cost)

            nodes_expanded += 1
            for child in state.neighbors():
                if child.cost < best_cost.get(child.tiles, float("inf")):
                    best_cost[child.tiles] = child.cost
                    counter += 1
                    heapq.heappush(frontier,
                                   (child.cost + self.heuristic(child), counter, child))
                    nodes_generated += 1
            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
