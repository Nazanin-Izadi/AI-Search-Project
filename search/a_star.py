import heapq

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calculate_mst_cost(targets):
    if not targets or len(targets) <= 1:
        return 0

    targets_list = list(targets)

    connected = {targets_list[0]}
    unconnected = set(targets_list[1:])
    total_mst_cost = 0

    while unconnected:
        min_dist = float('inf')
        best_node = None
        
        for u in connected:
            for v in unconnected:
                dist = manhattan_distance(u, v)
                if dist < min_dist:
                    min_dist = dist
                    best_node = v
                    
        connected.add(best_node)
        unconnected.remove(best_node)
        total_mst_cost += min_dist

    return total_mst_cost

def a_star(initial_state):
    def heuristic(state):
        targets = state.get_targets_positions()
        if not targets:
            return 0

        agent_pos = state.get_agent_position()
        
        closest_target_dist = min(manhattan_distance(agent_pos, t) for t in targets)
        
        mst_cost = calculate_mst_cost(targets)

        return (closest_target_dist + mst_cost) * 10

    pq = []
    initial_h = heuristic(initial_state)
    heapq.heappush(pq, (initial_h, 0, id(initial_state), initial_state, []))
    
    visited = {}

    while pq:
        f_cost, g_cost, _, state, path = heapq.heappop(pq)

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
            new_g = g_cost + step_cost
            new_h = heuristic(next_state)
            new_f = new_g + new_h
            
            heapq.heappush(pq, (new_f, new_g, id(next_state), next_state, path + [act]))

    return []