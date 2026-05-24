import heapq

def ucs(initial_state):
    pq = [(0, id(initial_state), initial_state, [])]
    visited = {}

    while pq:
        g_cost, _, state, path = heapq.heappop(pq)

        if state.is_goal_state():
            return path

        enemy_alive = getattr(state, "is_enemy_alive", lambda: True)()
        enemy_pos = state.get_enemy_position() if hasattr(state, 'get_enemy_position') else None

        state_sig = (
            state.get_agent_position(),
            tuple(sorted(state.get_targets_positions())),
            enemy_pos,
            enemy_alive
        )

        if state_sig in visited and visited[state_sig] <= g_cost:
            continue
        visited[state_sig] = g_cost

        for act, step_cost, next_state in state.get_successors(toward_walls=True):
            new_cost = g_cost + step_cost
            heapq.heappush(pq, (new_cost, id(next_state), next_state, path + [act]))

    return []