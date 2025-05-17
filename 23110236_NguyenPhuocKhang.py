import pygame
from collections import deque
import heapq
import random
import time

# Khởi tạo Pygame
pygame.init()
clock = pygame.time.Clock()  # Tạo Clock để kiểm soát FPS

# Kích thước cửa sổ - kéo to thêm
WIDTH, HEIGHT = 1200, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle Solver")

# Kích thước ô
TILE_SIZE = 190 # Kích thước ô vuông
BOARD_SIZE = 3
PADDING = 18 #khoảng cách lề giữa các thành phần trong giao diện.

# Màu sắc
grey = (200, 200, 200)
black = (0, 0, 0)
blue = (100, 149, 237)
white = (255, 255, 255)
green = (50, 205, 50)



# Font chữ
tile_font = pygame.font.SysFont(None, 60)
button_font = pygame.font.SysFont(None, 32)
title_font = pygame.font.SysFont(None, 36)

# Hàm sinh trạng thái hợp lệ
def generate_fixed_puzzle():
    """Trả về trạng thái 8-Puzzle cố định theo đề bài."""

    return  [2, 6, 5, 
            0, 8, 7,  # Ô trống là số 0
           4, 3, 1]

# Tính toán heuristic Manhattan distance
def manhattan_distance(state):
    goal_pos = {val: (idx % 3, idx // 3) for idx, val in enumerate(range(1, 9))}
    goal_pos[0] = (2, 2)
    return sum(abs((state.index(val) % 3) - goal_pos[val][0]) + abs((state.index(val) // 3) - goal_pos[val][1]) for val in state if val != 0)

# Thuật toán A*
def astar_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    queue = [(manhattan_distance(start_state), 0, start_state, [])]  # (f, g, state, path)
    
    while queue:
        _, g, state, path = heapq.heappop(queue)
        
        if state == goal_state:
            return path
            
        if tuple(state) in visited:
            continue
            
        visited.add(tuple(state))
        
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải
        
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                if tuple(new_state) not in visited:
                    new_g = g + 1  # Tăng chi phí đường đi
                    new_h = manhattan_distance(new_state)  # Heuristic
                    new_f = new_g + new_h  # Tổng chi phí ước lượng
                    heapq.heappush(queue, (new_f, new_g, new_state, path + [(zero_idx, new_idx)]))
    
    return None 

def ida_star_solve(start_state):
    goal_state = list(range(1, 9)) + [0]

    def search(state, g, bound, path):
        """Hàm tìm kiếm đệ quy có cắt tỉa theo ngưỡng."""
        f = g + manhattan_distance(state)  
        if f > bound:
            return f  # Trả về chi phí tối thiểu để tiếp tục tìm kiếm
        if state == goal_state:
            return path  # Trả về đường đi nếu đạt trạng thái đích

        min_cost = float('inf')
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải
        next_states = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                next_states.append((new_state, path + [(zero_idx, new_idx)]))

        # **Ưu tiên trạng thái có heuristic nhỏ trước**
        next_states.sort(key=lambda x: manhattan_distance(x[0]))

        for new_state, new_path in next_states:
            cost = search(new_state, g + 1, bound, new_path)
            if isinstance(cost, list):  # Nếu tìm thấy lời giải, trả về ngay
                return cost
            min_cost = min(min_cost, cost)

        return min_cost  # Trả về chi phí tối thiểu nếu chưa tìm thấy lời giải

    # **Bắt đầu IDA* với các ngưỡng tăng dần** 
    bound = manhattan_distance(start_state)
    while True:
        result = search(start_state, 0, bound, [])
        if isinstance(result, list):  # Nếu tìm thấy lời giải
            return result
        if result == float('inf'):
            return None  # Không tìm thấy lời giải
        bound = result  # Cập nhật giới hạn

def ida_star_solve_optimized(start_state):
    goal_state = list(range(1, 9)) + [0]

    def search(state, g, bound, path, visited):
        f = g + manhattan_distance(state)
        if f > bound:
            return f
        if state == goal_state:
            return path

        min_cost = float('inf')
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    cost = search(new_state, g + 1, bound, path + [(zero_idx, new_idx)], visited)
                    if isinstance(cost, list):
                        return cost
                    min_cost = min(min_cost, cost)
                    visited.remove(tuple(new_state))

        return min_cost

    bound = manhattan_distance(start_state)
    visited = set()
    visited.add(tuple(start_state))

    while True:
        result = search(start_state, 0, bound, [], visited)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return None
        bound = result

# Thuật toán tìm kiếm
def bfs_solve(start_state):
    return generic_solve(start_state, queue=deque([(start_state, [])]), pop_method='popleft')

def dfs_solve(start_state, max_depth=100):
    """Giải 8-Puzzle bằng DFS nhưng giới hạn độ sâu để tránh lặp vô hạn."""
    stack = [(start_state, [])]  # Sử dụng stack để tránh đệ quy quá sâu
    visited = set()
    
    while stack:
        state, path = stack.pop()

        # Nếu đạt trạng thái đích, trả về lời giải
        if state == list(range(1, 9)) + [0]:
            return path

        # Nếu quá sâu, bỏ qua trạng thái này
        if len(path) >= max_depth:
            continue

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải
        next_states = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    next_states.append((new_state, path + [(zero_idx, new_idx)]))

        # **Ưu tiên mở rộng trạng thái gần đích trước để giảm thời gian tìm kiếm**
        next_states.sort(key=lambda x: manhattan_distance(x[0]), reverse=False)

        for new_state, new_path in next_states:
            visited.add(tuple(new_state))
            stack.append((new_state, new_path))

    return None  # Không tìm thấy lời giải trong giới hạn 200 bước

def ucs_solve(start_state):
    return generic_solve(start_state, queue=[(0, start_state, [])], pop_method='heappop', is_priority=True)

def greedy_solve(start_state):
    return generic_solve(start_state, queue=[(manhattan_distance(start_state), start_state, [])], pop_method='heappop', is_priority=True)

def iddfs_solve(start_state):
    """Giải 8-Puzzle bằng IDDFS với giới hạn độ sâu động."""
    goal_state = list(range(1, 9)) + [0]

    def dls(state, path, depth_limit, visited):
        """DFS có giới hạn độ sâu (DLS) để tránh đi quá sâu."""
        if state == goal_state:
            return path
        if len(path) >= depth_limit:
            return None  # Đạt giới hạn độ sâu

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải
        next_states = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]

                if tuple(new_state) not in visited:
                    next_states.append((new_state, path + [(zero_idx, new_idx)]))

        # **Ưu tiên trạng thái gần lời giải trước** để giảm số bước lặp không cần thiết
        next_states.sort(key=lambda x: manhattan_distance(x[0]))

        for new_state, new_path in next_states:
            visited.add(tuple(new_state))
            result = dls(new_state, new_path, depth_limit, visited)
            if result is not None:
                return result  # Trả về lời giải nếu tìm thấy

        return None

    # **Dùng Iterative Deepening để thử nhiều độ sâu tăng dần**
    for depth_limit in range(5, 50, 5):  # Tăng dần giới hạn độ sâu
        visited = set()
        solution = dls(start_state, [], depth_limit, visited)
        if solution is not None:
            return solution  # Nếu tìm thấy lời giải, trả về ngay

    return None  # Không tìm thấy lời giải
def simple_hill_climbing(start_state):
    goal_state = list(range(1, 9)) + [0]

    def get_neighbors(state):
        neighbors = []
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append((new_state, (zero_idx, new_idx)))
        return neighbors

    current = start_state[:]
    path = []
    nodes_explored = 0

    while True:
        current_h = manhattan_distance(current)
        neighbors = get_neighbors(current)
        nodes_explored += len(neighbors)

        next_state = None
        for state, move in neighbors:
            if manhattan_distance(state) < current_h:
                current_h = manhattan_distance(state)
                next_state = (state, move)

        if next_state:
            current, move = next_state
            path.append(move)
            if current == goal_state:
                return path, nodes_explored
        else:
            break

    return path if path else None, nodes_explored

def random_restart_hill_climbing(start_state, max_restarts=10):
    goal_state = list(range(1, 9)) + [0]
    best_path = None
    total_nodes = 0

    for _ in range(max_restarts):
        state = start_state[:] if _ == 0 else random.sample(range(9), 9)
        path, explored = simple_hill_climbing(state)
        total_nodes += explored
        if state == goal_state or (path and state == goal_state):
            return path, total_nodes
        if not best_path or (path and len(path) < len(best_path)):
            best_path = path

    return best_path if best_path else None, total_nodes

def steepest_ascent_hill_climbing(start_state):
    goal_state = list(range(1, 9)) + [0]

    def get_neighbors(state):
        neighbors = []
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                neighbors.append((new_state, (zero_idx, new_idx)))
        return neighbors

    current = start_state[:]
    path = []
    nodes_explored = 0

    while True:
        current_h = manhattan_distance(current)
        neighbors = get_neighbors(current)
        nodes_explored += len(neighbors)

        # Tìm hàng xóm có heuristic thấp nhất
        best_neighbor = None
        best_h = current_h

        for state, move in neighbors:
            h = manhattan_distance(state)
            if h < best_h:
                best_h = h
                best_neighbor = (state, move)

        if best_neighbor:
            current, move = best_neighbor
            path.append(move)
            if current == goal_state:
                return path, nodes_explored
        else:
            break  # Không có hàng xóm tốt hơn ⇒ cực trị

    return path if path else None, nodes_explored

def simulated_annealing_solve(start_state, initial_temp=5000, cooling_rate=0.998, min_temp=1e-5, max_steps=20000, restart_threshold=1000):
    goal_state = list(range(1, 9)) + [0]

    def get_random_neighbor(state):
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        valid_neighbors = []

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                valid_neighbors.append((new_state, (zero_idx, new_idx)))

        return random.choice(valid_neighbors) if valid_neighbors else (state, None)

    current = start_state[:]
    path = []
    current_cost = manhattan_distance(current)
    temp = initial_temp
    nodes_explored = 0
    best_state = current[:]
    best_cost = current_cost
    steps_since_improvement = 0

    for step in range(max_steps):
        if current == goal_state:
            return path, nodes_explored

        neighbor, move = get_random_neighbor(current)
        neighbor_cost = manhattan_distance(neighbor)
        delta = neighbor_cost - current_cost
        nodes_explored += 1

        # Luôn nhận trạng thái tốt hơn, có xác suất nhận trạng thái kém hơn
        if delta < 0 or random.random() < pow(2.71828, -delta / temp):
            current = neighbor
            current_cost = neighbor_cost
            if move:
                path.append(move)

            # Cập nhật trạng thái tốt nhất
            if current_cost < best_cost:
                best_state = current[:]
                best_cost = current_cost
                steps_since_improvement = 0
        else:
            steps_since_improvement += 1

        # Khởi động lại nếu không cải thiện trong một số bước
        if steps_since_improvement >= restart_threshold:
            current = random.sample(range(9), 9)
            current_cost = manhattan_distance(current)
            steps_since_improvement = 0

        # Làm mát nhiệt độ
        temp *= cooling_rate
        if temp < min_temp:
            break

    # Trả về trạng thái tốt nhất nếu không tìm thấy lời giải
    return path if best_state == goal_state else None, nodes_explored

def beam_search_solve(start_state, beam_width=3):
    goal_state = list(range(1, 9)) + [0]
    queue = [(manhattan_distance(start_state), start_state, [])]
    visited = set()

    while queue:
        # Giữ tối đa `beam_width` trạng thái tốt nhất
        queue.sort(key=lambda x: x[0])
        queue = queue[:beam_width]

        next_queue = []

        for _, state, path in queue:
            if state == goal_state:
                return path

            zero_idx = state.index(0)
            moves = [-3, 3, -1, 1]

            for move in moves:
                new_idx = zero_idx + move
                if 0 <= new_idx < 9 and (
                    (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                    (move in [-3, 3])
                ):
                    new_state = state[:]
                    new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                    if tuple(new_state) not in visited:
                        visited.add(tuple(new_state))
                        h = manhattan_distance(new_state)
                        next_queue.append((h, new_state, path + [(zero_idx, new_idx)]))

        queue = next_queue

    return None

def and_or_solve(start_state):
    goal_state = list(range(1, 9)) + [0]
    
    # Set to track visited states to avoid revisiting them
    visited = set()

    def search(state, depth=0, max_depth=50):  # Limit recursion depth
        if depth > max_depth:  # Stop if max depth is reached
            return None
        
        if state == goal_state:
            return []  # If the goal state is found, return an empty path
        
        # If this state has already been visited, skip it
        if tuple(state) in visited:
            return None
        
        visited.add(tuple(state))  # Mark this state as visited
        
        zero_idx = state.index(0)  # Find the index of the empty space
        moves = [-3, 3, -1, 1]  # Define possible moves (up, down, left, right)
        next_states = []

        for move in moves:
            new_idx = zero_idx + move

            # Ensure that moves don't go out of bounds
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or  # Check left/right within same row
                (move in [-3, 3])  # Check up/down within the same column
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                next_states.append((new_state, new_idx))  # Record new_idx here

        # Search recursively for the next valid states
        for new_state, move in next_states:
            path = search(new_state, depth + 1, max_depth)
            if path is not None:
                return [(zero_idx, move)] + path  # Add the move to the path
        
        return None  # Return None if no solution found in this branch
    
    return search(start_state)  # Start the search with the initial state

def fitness(state):
    return manhattan_distance(state)  # Hàm fitness là Manhattan distance

def create_population(pop_size):
    """Khởi tạo quần thể ngẫu nhiên."""
    return [random.sample(range(9), 9) for _ in range(pop_size)]
def select_parents(population):
    """Chọn lọc hai cá thể tốt nhất từ quần thể sử dụng Tournament Selection."""
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=fitness)
    return tournament[0], tournament[1]
def crossover(parent1, parent2):
    """Lai tạo giữa hai cá thể để tạo ra cá thể con hợp lệ."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child1 = [-1] * size
    child2 = [-1] * size

    # Copy đoạn giữa từ cha mẹ
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Điền các giá trị còn lại từ cha mẹ kia
    fill_child(child1, parent2, start, end)
    fill_child(child2, parent1, start, end)

    return child1, child2

def fill_child(child, parent, start, end):
    size = len(parent)
    current_pos = end
    used = set(child[start:end])
    for val in parent:
        if val not in used:
            while child[current_pos % size] != -1:
                current_pos += 1
            child[current_pos % size] = val
            used.add(val)
def mutate(state, mutation_rate=0.1):
    """Đột biến cá thể với xác suất mutation_rate."""
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(state)), 2)
        state[idx1], state[idx2] = state[idx2], state[idx1]
    return state
def genetic_algorithm(pop_size=100, generations=1000, mutation_rate=0.1):
    population = create_population(pop_size)
    best_state = None
    best_fitness = float('inf')

    for generation in range(generations):
        population.sort(key=fitness)
        if fitness(population[0]) < best_fitness:
            best_state = population[0]
            best_fitness = fitness(population[0])

        if fitness(best_state) == 0:
            return best_state, generation + 1  # ✅ Trả về số vòng lặp luôn

        new_population = population[:2]
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))

        population = new_population

    return best_state, generations


# Giải thuật chung
def generic_solve(start_state, queue, pop_method, is_priority=False):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    while queue:
        if is_priority:
            _, state, path = heapq.heappop(queue)
        else:
            state, path = getattr(queue, pop_method)()
        if state == goal_state:
            return path
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]
        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and ((move in [-1, 1] and zero_idx // 3 == new_idx // 3) or (move in [-3, 3])):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                if tuple(new_state) not in visited:
                    visited.add(tuple(new_state))
                    if is_priority:
                        heapq.heappush(queue, (manhattan_distance(new_state), new_state, path + [(zero_idx, new_idx)]))
                    else:
                        queue.append((new_state, path + [(zero_idx, new_idx)]))
    return None
def general_problem_component_solver(start_state):
    """Component of a General Problem: Mô hình hóa rồi giải bằng BFS."""

    # 1. Không gian trạng thái: tất cả các hoán vị của 0-8.
    state_space = set()

    # 2. Trạng thái ban đầu
    initial_state = start_state

    # 3. Trạng thái mục tiêu
    goal_state = list(range(1, 9)) + [0]

    # 4. Phép toán: di chuyển 0 lên, xuống, trái, phải
    moves = [-3, 3, -1, 1]  # Lên, Xuống, Trái, Phải

    # 5. Chi phí đường đi: mỗi bước di chuyển tính là 1

    # Giải bài toán bằng BFS (vì Component of a General Problem không quy định thuật toán cụ thể)
    return bfs_solve(initial_state)

def draw_board(state):
    """Vẽ bảng 8-Puzzle với hiệu ứng bóng đổ đẹp hơn."""
    
    # Vị trí bảng (giữ bên phải màn hình)
    board_x = WIDTH - TILE_SIZE * 3 - PADDING * 2
    board_y = (HEIGHT - TILE_SIZE * 3) // 2
    
    # Vẽ nền bảng (Xám đậm) + Viền (Xám trung bình)
    pygame.draw.rect(WINDOW, (50, 50, 50),  # Xám đậm (nền)
                     (board_x - 10, board_y - 10, TILE_SIZE * 3 + 20, TILE_SIZE * 3 + 20), 
                     border_radius=12)

    pygame.draw.rect(WINDOW, (169, 169, 169),  # Xám trung bình (Viền bảng)
                     (board_x - 10, board_y - 10, TILE_SIZE * 3 + 20, TILE_SIZE * 3 + 20), 
                     4, border_radius=12)

    # Duyệt từng ô trong bảng
    for i, num in enumerate(state):
        x = board_x + (i % 3) * TILE_SIZE
        y = board_y + (i // 3) * TILE_SIZE

        if num != 0:  # Không vẽ ô trống
            # Hiệu ứng bóng đổ (Tạo cảm giác 3D)
            pygame.draw.rect(WINDOW, (70, 70, 70),  # Xám đậm hơn (bóng đổ)
                             (x + 5, y + 5, TILE_SIZE - 4, TILE_SIZE - 4), 
                             border_radius=10)

            # Vẽ ô chính (Màu sáng hơn)
            pygame.draw.rect(WINDOW, (240, 240, 240),  # Xám rất nhạt
                             (x, y, TILE_SIZE - 4, TILE_SIZE - 4), 
                             border_radius=10)

            # Viền ô (Giúp tách biệt các ô)
            pygame.draw.rect(WINDOW, (100, 100, 100),  # Xám trung bình
                             (x, y, TILE_SIZE - 4, TILE_SIZE - 4), 
                             3, border_radius=10)
            
            # Hiển thị số trên ô (Màu đen)
            text = tile_font.render(str(num), True, (0, 0, 0))  
            text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            WINDOW.blit(text, text_rect)

def searching_with_no_observation(start_state):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    queue = deque([(start_state, [])])
    
    while queue:
        state, path = queue.popleft()

        # Tạm coi không quan sát được trạng thái, chỉ biết vị trí trống
        if state == goal_state:
            return path

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                
                # Chỉ kiểm tra visited dựa trên vị trí trống
                state_signature = tuple(new_state)
                if state_signature not in visited:
                    visited.add(state_signature)
                    queue.append((new_state, path + [(zero_idx, new_idx)]))

    return None
import heapq

def belief_astar_solve(start_state):
    goal_state = list(range(1, 9)) + [0]

    visited = set()
    queue = []
    heapq.heappush(queue, (manhattan_distance(start_state), 0, start_state, []))
    nodes_explored = 0  # Đếm số node đã xét

    while queue:
        f, g, state, path = heapq.heappop(queue)
        nodes_explored += 1

        if state == goal_state:
            return path, nodes_explored  # ✅ Trả về path và số node đã duyệt

        state_key = tuple(state)
        if state_key in visited:
            continue
        visited.add(state_key)

        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                if tuple(new_state) not in visited:
                    h = manhattan_distance(new_state)
                    heapq.heappush(queue, (g + 1 + h, g + 1, new_state, path + [(zero_idx, new_idx)]))

    return None, nodes_explored  # Không tìm được


def backtracking_search_solve(start_state, max_depth=50):
    goal_state = list(range(1, 9)) + [0]
    visited = set()
    nodes = [0]  # List để đếm số nodes duyệt qua (dùng list để truyền tham chiếu)

    def backtrack(state, path, depth):
        nodes[0] += 1  # Mỗi lần vào backtrack thì duyệt thêm 1 node
        if state == goal_state:
            return path
        if depth > max_depth:
            return None
        
        visited.add(tuple(state))
        zero_idx = state.index(0)
        moves = [-3, 3, -1, 1]

        for move in moves:
            new_idx = zero_idx + move
            if 0 <= new_idx < 9 and (
                (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                (move in [-3, 3])
            ):
                new_state = state[:]
                new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
                if tuple(new_state) not in visited:
                    result = backtrack(new_state, path + [(zero_idx, new_idx)], depth + 1)
                    if result is not None:
                        return result
        visited.remove(tuple(state))  # Quay lui
        return None

    result = backtrack(start_state, [], 0)
    # Trả về tuple: (solution, số node duyệt)
    return result, nodes[0]


from itertools import permutations

def sensorless_search_solve(start_state, max_steps=50):
    goal_state = tuple(range(1, 9)) + (0,)

    all_states = list(permutations(range(9)))
    belief = set(all_states)

    path = []
    moves = [-3, 3, -1, 1]
    nodes_explored = 0

    steps = 0  # Đếm số bước đã đi

    while True:
        if all(state == goal_state for state in belief):
            # Đã thu hẹp toàn bộ belief về goal
            return path, nodes_explored

        if steps > max_steps:
            return None, nodes_explored  # Tránh vòng lặp vô hạn

        found_valid_move = False
        for move in moves:
            new_belief = set()
            for state in belief:
                try:
                    zero_idx = state.index(0)
                    new_idx = zero_idx + move
                    if 0 <= new_idx < 9 and (
                        (move in [-1, 1] and zero_idx // 3 == new_idx // 3) or
                        (move in [-3, 3])
                    ):
                        state = list(state)
                        state[zero_idx], state[new_idx] = state[new_idx], state[zero_idx]
                        new_belief.add(tuple(state))
                        nodes_explored += 1
                except:
                    continue

            if new_belief and len(new_belief) < len(belief):
                belief = new_belief
                path.append(move)  # chỉ lưu move, xử lý animation sau
                found_valid_move = True
                steps += 1
                break  # Ưu tiên bước thu hẹp belief nhanh

        if not found_valid_move:
            return None, nodes_explored


from collections import deque

def ac3_solve(start_state):
    """
    Áp dụng AC-3 để kiểm tra consistency trạng thái 8-puzzle.
    Trả về số node đã duyệt và trạng thái nếu consistency OK.
    """
    arcs = deque()
    for i in range(9):
        for j in range(9):
            if i != j:
                arcs.append((i, j))

    domains = {i: {start_state[i]} for i in range(9)}
    nodes_explored = 0  # Đếm số arc đã kiểm tra

    def revise(xi, xj):
        nonlocal nodes_explored
        revised = False
        for val in domains[xi].copy():
            # Nếu không tồn tại giá trị khác trong xj thỏa mãn ràng buộc
            if not any(val != other for other in domains[xj]):
                domains[xi].remove(val)
                revised = True
        nodes_explored += 1
        return revised

    while arcs:
        xi, xj = arcs.popleft()
        if revise(xi, xj):
            if not domains[xi]:
                return [], nodes_explored  # Không còn giá trị hợp lệ
            for xk in range(9):
                if xk != xi and xk != xj:
                    arcs.append((xk, xi))

    # Dựng lại trạng thái nếu consistency OK
    result_state = [list(domains[i])[0] for i in range(9)]

    # Nếu trạng thái đúng goal thì không cần animation
    if result_state == list(range(1, 9)) + [0]:
        return [], nodes_explored

    # Nếu khác trạng thái gốc, sinh animation từ start_state → result_state
    solution = []
    current = start_state[:]
    for i in range(9):
        if current[i] != result_state[i]:
            target_idx = current.index(result_state[i])
            current[i], current[target_idx] = current[target_idx], current[i]
            solution.append((i, target_idx))

    return solution, nodes_explored

def q_learning_solve(start_state):
    from collections import defaultdict

    goal_state = tuple(range(1, 9)) + (0,)
    alpha = 0.7
    gamma = 0.9
    epsilon = 0.1
    episodes = 50000  # tăng huấn luyện
    Q = defaultdict(lambda: [0] * 4)  # Up, Down, Left, Right
    moves = [-3, 3, -1, 1]

    def is_valid(state, move):
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        return (
            0 <= new_idx < 9 and
            ((move == -1 and zero_idx % 3 != 0) or
             (move == 1 and zero_idx % 3 != 2) or
             move in [-3, 3])
        )

    def apply_move(state, move):
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        new_state = list(state)
        new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
        return tuple(new_state)

    # === Huấn luyện ===
    for _ in range(episodes):
        if random.random() < 0.3:
            state = tuple(start_state)
        else:
            state = tuple(random.sample(range(9), 9))

        for _ in range(50):
            if state == goal_state:
                break
            if random.random() < epsilon:
                action = random.choice(range(4))
            else:
                action = max(range(4), key=lambda a: Q[state][a])

            move = moves[action]
            if is_valid(state, move):
                next_state = apply_move(state, move)
                reward = 100 if next_state == goal_state else -1
                Q[state][action] += alpha * (reward + gamma * max(Q[next_state]) - Q[state][action])
                state = next_state

    # === Suy luận ===
    state = tuple(start_state)
    path = []
    nodes_explored = 0

    for _ in range(100):  # tránh lặp vô hạn
        if state == goal_state:
            return path, nodes_explored

        q_values = Q[state]
        max_q = max(q_values)

        # Nếu Q-values bằng nhau hoặc chưa học
        if q_values == [0, 0, 0, 0] or max_q == 0:
            break

        action = q_values.index(max_q)
        move = moves[action]
        if not is_valid(state, move):
            break

        new_state = apply_move(state, move)
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        path.append((zero_idx, new_idx))
        state = new_state
        nodes_explored += 1

    if state != goal_state:
        return None, nodes_explored
    return path, nodes_explored

def reinforce_policy_gradient(start_state, episodes=10000, alpha=0.01, gamma=0.9):
    import math
    from collections import defaultdict

    goal_state = tuple(range(1, 9)) + (0,)
    moves = [-3, 3, -1, 1]  # Up, Down, Left, Right

    # Khởi tạo trọng số chính sách π(a|s) ~ softmax
    policy = defaultdict(lambda: [0.0] * 4)

    def is_valid(state, move):
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        return (
            0 <= new_idx < 9 and
            ((move == -1 and zero_idx % 3 != 0) or
             (move == 1 and zero_idx % 3 != 2) or
             move in [-3, 3])
        )

    def apply_move(state, move):
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        new_state = list(state)
        new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[zero_idx]
        return tuple(new_state)

    def softmax(x):
        max_x = max(x)
        exps = [math.exp(i - max_x) for i in x]
        sum_exps = sum(exps)
        return [e / sum_exps for e in exps]

    def choose_action(state):
        probs = softmax(policy[state])
        return random.choices(range(4), weights=probs, k=1)[0]

    # === Huấn luyện ===
    for _ in range(episodes):
        state = tuple(start_state)
        trajectory = []

        for _ in range(50):  # Giới hạn số bước
            if state == goal_state:
                break

            action = choose_action(state)
            move = moves[action]

            if not is_valid(state, move):
                reward = -10
                trajectory.append((state, action, reward))
                break

            next_state = apply_move(state, move)
            reward = 100 if next_state == goal_state else -1
            trajectory.append((state, action, reward))
            state = next_state

        # Cập nhật chính sách
        G = 0
        for state, action, reward in reversed(trajectory):
            G = reward + gamma * G
            probs = softmax(policy[state])
            for a in range(4):
                grad = (1 if a == action else 0) - probs[a]
                policy[state][a] += alpha * G * grad

    # === Suy luận ===
    state = tuple(start_state)
    path = []
    nodes_explored = 0

    for _ in range(100):
        if state == goal_state:
            return path, nodes_explored

        action = choose_action(state)
        move = moves[action]
        if not is_valid(state, move):
            break

        new_state = apply_move(state, move)
        zero_idx = state.index(0)
        new_idx = zero_idx + move
        path.append((zero_idx, new_idx))
        state = new_state
        nodes_explored += 1

    return None, nodes_explored

def draw_time_and_nodes(time_elapsed, nodes_explored, step_count):
    """Hiển thị thời gian thực hiện, số node đã duyệt và số bước di chuyển."""
    # Vẽ lại thông tin thời gian
    time_text = button_font.render(f"Time: {time_elapsed:.3f}s", True, black)
    time_rect = time_text.get_rect(midbottom=(WIDTH // 2 - 200, HEIGHT - 20))
    WINDOW.blit(time_text, time_rect)

    # Vẽ lại số node đã duyệt
    nodes_text = button_font.render(f"Nodes: {nodes_explored}", True, black)
    nodes_rect = nodes_text.get_rect(midbottom=(WIDTH // 2 + 200 , HEIGHT - 20))
    WINDOW.blit(nodes_text, nodes_rect)

    
# Thêm một nút giải thuật di truyền vào giao diện
def draw_buttons():
    """Vẽ các nút chọn thuật toán với hiệu ứng bóng đổ, chia làm 2 cột."""
    buttons = ["BFS", "DFS", "UCS", "Greedy", "IDDFS", "A*", "IDA*", 
               "Simple Hill", "Steepest Hill", "Rand Restart", 
               "Simulated", "Beam", "AND-OR", "Genetic Algorithm",
               "No Observation", "Component Problem", "Belief A*", 
               "Backtracking","Sensorless Search","AC-3","Q-Learning", "REINFORCE","Reset"]
    
    colors = [blue] * (len(buttons) - 1) + [green]  # "Reset" là màu xanh lá

    button_width = 230
    button_height = 36
    spacing = 10

    button_area_x = PADDING * 2
    button_area_y = 20  # Đẩy lên trên

    button_positions = []

    for i, (btn_text, color) in enumerate(zip(buttons, colors)):
        col = i // 17  # Mỗi cột chứa tối đa 10 nút
        row = i % 17

        x = button_area_x + col * (button_width + 30)  # Cách giữa 2 cột
        y = button_area_y + row * (button_height + spacing)

        # Bóng đổ
        pygame.draw.rect(WINDOW, (50, 50, 50),
                         (x + 4, y + 4, button_width, button_height),
                         border_radius=12)

        # Nút chính
        pygame.draw.rect(WINDOW, color,
                         (x, y, button_width, button_height),
                         border_radius=12)

        # Viền nút
        pygame.draw.rect(WINDOW, (100, 100, 100),
                         (x, y, button_width, button_height),
                         3, border_radius=12)

        # Chữ trên nút
        text = button_font.render(btn_text, True, black)
        text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
        WINDOW.blit(text, text_rect)

        button_positions.append((x, y, button_width, button_height))

    return button_positions


# Thêm logic xử lý cho "Genetic Algorithm"
def get_clicked_button(pos, button_positions):
    algorithm_names = [
        "BFS", "DFS", "UCS", "Greedy", "IDDFS", "A*", "IDA*", 
        "Simple Hill", "Steepest Hill", "Rand Restart", "Simulated", 
        "Beam", "AND-OR", "Genetic Algorithm", "No Observation","Component Problem","Belief A*","Backtracking","Sensorless Search","AC-3","Q-Learning",  "REINFORCE","Reset"
    ]
    algorithms = [
        bfs_solve, dfs_solve, ucs_solve, greedy_solve, iddfs_solve, astar_solve, ida_star_solve,
        simple_hill_climbing, steepest_ascent_hill_climbing, random_restart_hill_climbing,
        simulated_annealing_solve, beam_search_solve, and_or_solve,
        genetic_algorithm, searching_with_no_observation,general_problem_component_solver,belief_astar_solve, backtracking_search_solve,sensorless_search_solve,ac3_solve, q_learning_solve,reinforce_policy_gradient,"reset"
    ]

    for i, (x, y, width, height) in enumerate(button_positions):
        if x <= pos[0] <= x + width and y <= pos[1] <= y + height:
            return algorithms[i], algorithm_names[i]
    return None, None




# Vẽ số bước
def draw_step_count(step_count):
    step_text = button_font.render(f"Steps: {step_count}", True, black)
    step_rect = step_text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    WINDOW.blit(step_text, step_rect)

# Hiển thị thuật toán đang chạy
def draw_selected_algorithm(algorithm_name):
    if algorithm_name:
        algo_text = button_font.render(f"Running: {algorithm_name}", True, black)
        algo_rect = algo_text.get_rect(midtop=(WIDTH - TILE_SIZE * 1.5, PADDING * 2))
        WINDOW.blit(algo_text, algo_rect)

# Khởi tạo trạng thái ban đầu
original_state = generate_fixed_puzzle()
start_state = original_state[:]

running = True
solving = False
solution = []
step = 0
selected_algorithm = None
algorithm_name = None
step_count = 0  # Đếm số bước di chuyển



def is_valid_state(state):
    """Kiểm tra trạng thái có hợp lệ không (đủ các số từ 0 đến 8)."""
    return sorted(state) == list(range(9))
def input_partial_state():
    print("Nhập trạng thái đầu vào : ")
    raw = input(">>> ").strip()
    nums = [int(x) for x in raw.split() if x.isdigit()]
    used = set(nums)

    # Đảm bảo có đủ số từ 0 đến 8
    missing = [x for x in range(9) if x not in used]
    full = nums + missing
    full = list(set(full))[:9]  # loại trùng và giới hạn 9 số

    full_state = sorted([x for x in full if x != 0]) + [0]

    print(f"Trạng thái hoàn chỉnh : {full_state}")
    return full_state


# Vòng lặp chính
time_elapsed = 0
nodes_explored = 0
step_count = 0  # Đảm bảo step_count bắt đầu lại từ 0
running = True
solving = False
solution = []
step = 0
selected_algorithm = None
algorithm_name = None

while running:
    WINDOW.fill((211, 211, 211))  # Làm mới cửa sổ
    button_positions = draw_buttons()
    draw_board(start_state)
    draw_step_count(step_count)
    draw_selected_algorithm(algorithm_name)
    draw_time_and_nodes(time_elapsed, nodes_explored, step_count)  # Hiển thị thời gian, node, step

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_algo, algo_name = get_clicked_button(event.pos, button_positions)
            if selected_algo is not None:
                if selected_algo == "reset":
                    # Reset toàn bộ
                    start_state = original_state[:]
                    solving = False
                    solution = []
                    step = 0
                    step_count = 0
                    algorithm_name = None
                    time_elapsed = 0
                    nodes_explored = 0
                    selected_algorithm = None
                    pygame.display.flip()
                else:
                    solving = True
                    algorithm_name = algo_name
                    start_time = time.time()

                    try:
                        # Thuật toán cần trạng thái nhập từ người dùng
                        if algorithm_name in ["Belief A*", "Backtracking", "Sensorless Search", "AC-3"]:
                            start_state = input_partial_state()
                        else:
                            start_state = original_state[:]

                        if algorithm_name in ["Simple Hill", "Steepest Hill", "Rand Restart", "Simulated"]:
                            solution, nodes_explored = selected_algo(start_state)

                        elif algorithm_name == "No Observation":
                            result = searching_with_no_observation(start_state)
                            if result is None:
                                solution = []
                                nodes_explored = 0
                                solving = False
                                algorithm_name = "No solution"
                            else:
                                solution = result
                                nodes_explored = len(result)

                        elif algorithm_name == "Sensorless Search":
                            path, nodes_explored = sensorless_search_solve(start_state)
                            if path is None:
                                solution = []
                                solving = False
                                #algorithm_name = "No solution"
                            else:
                                current = start_state[:]
                                solution = []
                                for move in path:
                                    zero_idx = current.index(0)
                                    move_idx = zero_idx + move
                                    current[zero_idx], current[move_idx] = current[move_idx], current[zero_idx]
                                    solution.append((zero_idx, move_idx))

                        elif algorithm_name == "Genetic Algorithm":
                            best_state, generations = genetic_algorithm()
                            if not is_valid_state(best_state):
                                raise ValueError(f"Invalid best_state: {best_state}")
                            start_state = best_state
                            nodes_explored = generations
                            solution = []
                            step_count = 0

                        elif algorithm_name == "Belief A*":
                             solution, nodes_explored = belief_astar_solve(start_state)
                             if solution is None:
                                    solution = []
                                    solving = False
                                    algorithm_name = "No solution"

                        elif algorithm_name == "Backtracking":
                            solution = backtracking_search_solve(start_state)
                            nodes_explored = len(solution) if solution else 0

                        elif algorithm_name == "AC-3":
                            solution, nodes_explored = ac3_solve(start_state)
                            if solution is None or not isinstance(solution, list):
                                solution = []
                                solving = False
                                algorithm_name = "No solution"
                        elif algorithm_name == "Q-Learning":
                            solution, nodes_explored = q_learning_solve(start_state)
                            if solution is None:
                                solution = []
                                solving = False
                                algorithm_name = "Q-Learning"
                        elif algorithm_name == "REINFORCE":
                            solution, nodes_explored = reinforce_policy_gradient(start_state)
                            if solution is None:
                                solution = []
                                solving = False
                                algorithm_name = "REINFORCE"
                        else:
                            solution = selected_algo(start_state)
                            nodes_explored = len(solution) if solution else 0
                        
                    except Exception as e:
                        print(f"Error while running {algorithm_name}: {e}")
                        solution = []
                        nodes_explored = 0
                        solving = False
                        algorithm_name = "Error"

                    end_time = time.time()
                    time_elapsed = end_time - start_time
                    step = 0


    pygame.display.flip()  # Cập nhật giao diện

    # Nếu đang giải quyết và có solution
    if solving and solution:
        if isinstance(solution, list) and step < len(solution):
            zero_idx, move_idx = solution[step]

            # Kiểm tra nếu chỉ số hợp lệ
            if 0 <= zero_idx < len(start_state) and 0 <= move_idx < len(start_state):
                # Hoán đổi các ô
                start_state[zero_idx], start_state[move_idx] = start_state[move_idx], start_state[zero_idx]
            else:
                print(f"Invalid indices: zero_idx={zero_idx}, move_idx={move_idx}")
                solving = False  # Dừng giải quyết nếu có lỗi chỉ số
            step += 1
            step_count += 1  # Tăng số bước
            pygame.display.flip()
            pygame.time.delay(300)
        else:
            solving = False  # Nếu giải xong hoặc không có giải pháp, dừng giải quyết

pygame.quit()

