def dls(initial_state, depth_limit=250):

    stack = [(initial_state, [], 0)]
    

    best_depth_visited = {}

    while stack:
        state, path, depth = stack.pop()

        if state.is_goal_state():
            return path

        if depth >= depth_limit:
            continue

        enemy_alive = getattr(state, "is_enemy_alive", lambda: True)()
        enemy_pos = state.get_enemy_position() if hasattr(state, 'get_enemy_position') else None

        state_sig = (
            state.get_agent_position(),
            tuple(sorted(state.get_targets_positions())),
            enemy_pos,
            enemy_alive
        )

        if state_sig in best_depth_visited and best_depth_visited[state_sig] <= depth:
            continue
            

        best_depth_visited[state_sig] = depth


        successors = state.get_successors(toward_walls=True)

        
        for act, cost, next_state in reversed(successors):
            if not next_state.is_collision_state():
                stack.append((next_state, path + [act], depth + 1))

    return []
