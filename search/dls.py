def dls(initial_state, depth_limit=150):
    stack = [(initial_state, [], 0)]
    visited = {}
    
    while stack:
        state, path, depth = stack.pop()
        
        if state.is_goal_state():
            return path
            
        if depth >= depth_limit:
            continue
            
        state_sig = (state.get_agent_position(), tuple(sorted(state.get_target_positions())))
        
        if state_sig in visited and visited[state_sig] <= depth:
            continue
        visited[state_sig] = depth
        
        for act, cost, next_state in state.get_successors(toward_walls=True):
            if not next_state.is_collision_state():
                stack.append((next_state, path + [act], depth + 1))
                
    return []
