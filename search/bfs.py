def bfs(initial_state):
    # Queue stores tuples of (state, path_of_actions)
    queue = deque([(initial_state, [])])
    visited = set()
    
    while queue:
        state, path = queue.popleft()
        
        if state.is_goal_state():
            return path
            
        # Create a unique signature for the current state
        state_sig = (state.get_agent_position(), tuple(sorted(state.get_target_positions())))
        
        if state_sig in visited:
            continue
        visited.add(state_sig)
        
        for act, cost, next_state in state.get_successors(toward_walls=True):
            # In BFS, we manually avoid the enemy since cost isn't evaluated
            if not next_state.is_collision_state():
                queue.append((next_state, path + [act]))
                
    return []
