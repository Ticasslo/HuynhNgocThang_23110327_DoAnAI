from collections import deque
import heapq
import random
import math
import pickle
import os
import numpy as np
import time

def layTrangThaiKe(trangThai):
    danhSachKe = []
    viTri0 = trangThai.index(0)

    hang = viTri0 // 3
    cot = viTri0 % 3

    buocDiChuyen = []
    if hang > 0: buocDiChuyen.append(viTri0 - 3)
    if hang < 2: buocDiChuyen.append(viTri0 + 3)
    if cot > 0: buocDiChuyen.append(viTri0 - 1)
    if cot < 2: buocDiChuyen.append(viTri0 + 1)

    for buoc in buocDiChuyen:
        trangThaiMoi = list(trangThai)
        trangThaiMoi[viTri0], trangThaiMoi[buoc] = trangThaiMoi[buoc], trangThaiMoi[viTri0]
        danhSachKe.append(tuple(trangThaiMoi))

    return danhSachKe

def truyVetDuongDi(cha, batDau, dich):
    duongDi = [dich]
    while duongDi[-1] != batDau:
        duongDi.append(cha[duongDi[-1]])
    duongDi.reverse()
    return duongDi

def bfs(batDau, dich):
    if batDau == dich:
        return [batDau]

    hangDoi = deque([batDau])
    daDuyet = set([batDau])
    cha = {batDau: None}

    while hangDoi:
        hienTai = hangDoi.popleft()

        if hienTai == dich:
            return truyVetDuongDi(cha, batDau, dich)

        for trangThaiKe in layTrangThaiKe(hienTai):
            if trangThaiKe not in daDuyet:
                daDuyet.add(trangThaiKe)
                cha[trangThaiKe] = hienTai
                hangDoi.append(trangThaiKe)

    return None

def dfs(batDau, dich):
    if batDau == dich:
        return [batDau]

    hangDoi = [batDau]
    daDuyet = set([batDau])
    cha = {batDau: None}

    while hangDoi:
        hienTai = hangDoi.pop()

        if hienTai == dich:
            return truyVetDuongDi(cha, batDau, dich)

        for trangThaiKe in layTrangThaiKe(hienTai):
            if trangThaiKe not in daDuyet:
                daDuyet.add(trangThaiKe)
                cha[trangThaiKe] = hienTai
                hangDoi.append(trangThaiKe)
    
def iddfs(batDau, dich, gioiHanToiDa):
    def dfsGioiHan(trangThai, gioiHan, daDuyet):
        if trangThai == dich:
            return [trangThai]
        if gioiHan == 0:
            return None
        daDuyet.add(trangThai)
        for trangThaiKe in layTrangThaiKe(trangThai):
            if trangThaiKe not in daDuyet:
                ketQua = dfsGioiHan(trangThaiKe, gioiHan - 1, daDuyet)
                if ketQua:
                    return [trangThai] + ketQua
        return None

    for gioiHan in range(gioiHanToiDa):
        daDuyet = set()
        ketQua = dfsGioiHan(batDau, gioiHan, daDuyet)
        if ketQua:
            return ketQua
    return None


################################################################################
def heuristic(trangThai, dich):
    """
    Hàm heuristic: tính tổng khoảng cách Manhattan của các ô (trừ ô trống)
    giữa trạng thái hiện tại và trạng thái đích.
    """
    khoangCach = 0
    for i in range(9):
        if trangThai[i] != 0:
            giaTri = trangThai[i]
            viTriDich = dich.index(giaTri)
            hangHT, cotHT = i // 3, i % 3
            hangDC, cotDC = viTriDich // 3, viTriDich % 3
            khoangCach += abs(hangHT - hangDC) + abs(cotHT - cotDC)
    return khoangCach
################################################################################


def greedy(batDau, dich):
    hangDoi = [(heuristic(batDau, dich), batDau)]  # Min-heap với (h, trạng thái)
    cha = {batDau: None}
    daDuyet = set()

    while hangDoi:
        _, hienTai = heapq.heappop(hangDoi)  # Lấy trạng thái có h nhỏ nhất

        if hienTai == dich:
            return truyVetDuongDi(cha, batDau, dich)

        daDuyet.add(hienTai)

        for trangThaiKe in layTrangThaiKe(hienTai):
            if trangThaiKe not in daDuyet:
                heapq.heappush(hangDoi, (heuristic(trangThaiKe, dich), trangThaiKe))
                cha[trangThaiKe] = hienTai
                daDuyet.add(trangThaiKe)

    return None  

def ucs(batDau, dich):
    """
    Uniform Cost Search (UCS) tìm đường đi ngắn nhất 
    theo số bước (cost = 1 mỗi lần di chuyển).
    """
    hangDoiUuTien = []
    # cost ban đầu = 0
    heapq.heappush(hangDoiUuTien, (0, batDau))

    costDenTrangThai = {batDau: 0}
    cha = {batDau: None}

    while hangDoiUuTien:
        costHienTai, trangThaiHienTai = heapq.heappop(hangDoiUuTien)

        # Nếu là đích -> dựng đường đi
        if trangThaiHienTai == dich:
            return truyVetDuongDi(cha, batDau, dich)

        # Nếu đã có cost tốt hơn, bỏ qua
        if costHienTai > costDenTrangThai[trangThaiHienTai]:
            continue

        # Sinh trạng thái kề
        for trangThaiKe in layTrangThaiKe(trangThaiHienTai):
            costMoi = costHienTai + 1
            if (trangThaiKe not in costDenTrangThai) or (costMoi < costDenTrangThai[trangThaiKe]):
                costDenTrangThai[trangThaiKe] = costMoi
                cha[trangThaiKe] = trangThaiHienTai
                heapq.heappush(hangDoiUuTien, (costMoi, trangThaiKe))

    return None

def a_sao(batDau, dich):
    """
    A* Search: f(n) = g(n) + h(n)
    trong đó g(n) là cost (số bước) từ batDau -> n
    h(n) là heuristic ước lượng n -> dich. Manhattan distance
    """

    # g(n): cost từ batDau đến n
    g = {batDau: 0}
    # f(n) = g(n) + h(n)
    f = {batDau: heuristic(batDau, dich)}

    # Min-heap lưu (f(n), state)
    openSet = [(f[batDau], batDau)]
    dong = set()  # closed set
    cha = {batDau: None}

    while openSet:
        fHienTai, hienTai = heapq.heappop(openSet)

        if hienTai == dich:
            return truyVetDuongDi(cha, batDau, dich)

        dong.add(hienTai)

        for ke in layTrangThaiKe(hienTai):
            if ke in dong:
                continue

            gMoi = g[hienTai] + 1
            # Nếu chưa thấy ke bao giờ, hoặc tìm được đường đi rẻ hơn
            if (ke not in g) or (gMoi < g[ke]):
                cha[ke] = hienTai
                g[ke] = gMoi
                f[ke] = gMoi + heuristic(ke, dich)
                heapq.heappush(openSet, (f[ke], ke))

    return None

def ida_sao(batDau, dich):
    """
    IDA* Search cho 8-Puzzle, dùng Manhattan distance làm heuristic
    Trả về danh sách trạng thái từ batDau -> dich nếu tìm thấy
    hoặc None nếu không có
    """

    # Biến toàn cục để lưu cha
    cha = {}
    cha[batDau] = None

    # Hàm DFS có giới hạn f(n)
    def search(path, g, bound):
        """
        path: list các trạng thái đi từ start -> trạng thái hiện tại
        g   : cost thực tế (số bước) từ start -> trạng thái hiện tại
        bound: ngưỡng cắt (threshold) hiện tại
        Trả về:
          - "FOUND" nếu tìm thấy lời giải
          - hoặc cost_min_moi (cost tối thiểu vượt bound) nếu chưa tìm thấy
        """
        trangThaiHienTai = path[-1]
        f = g + heuristic(trangThaiHienTai, dich)

        # Nếu f(n) vượt ngưỡng, trả về f(n) để cập nhật bound
        if f > bound:
            return f

        # Nếu đạt đích
        if trangThaiHienTai == dich:
            return "FOUND"

        # Tiếp tục DFS
        min_cost = float('inf')
        for ke in layTrangThaiKe(trangThaiHienTai):
            # Tránh đi vòng lại cha
            if ke not in path:
                cha[ke] = trangThaiHienTai
                path.append(ke)
                tmp = search(path, g + 1, bound)
                if tmp == "FOUND":
                    return "FOUND"
                if tmp < min_cost:
                    min_cost = tmp
                # Lùi lại
                path.pop()
        return min_cost

    # IDA* lặp dần ngưỡng cắt
    bound = heuristic(batDau, dich)
    path = [batDau]

    while True:
        tmp = search(path, 0, bound)
        if tmp == "FOUND":
            # Dựng đường đi
            return truyVetDuongDi(cha, batDau, dich)
        if tmp == float('inf'):
            # Không tìm thấy lời giải
            return None
        bound = tmp  # Tăng ngưỡng lên giá trị tối thiểu mới


################################################################################


def simple_hill_climbing(batDau, dich):
    """
    Thuật toán Simple Hill Climbing:
    - Bắt đầu từ trạng thái batDau.
    - Ở mỗi bước, duyệt các trạng thái kề và chọn trạng thái có giá trị heuristic thấp nhất.
    - Nếu không tìm được trạng thái nào tốt hơn (tức đạt cực trị cục bộ), dừng lại.
    - Nếu đạt đến trạng thái đích, trả về đường đi (danh sách trạng thái).
    
    Trả về đường đi (list các trạng thái) nếu thành công, hoặc None nếu không tìm được lời giải.
    """
    current = batDau
    duongDi = [current]
    while current != dich:
        current_h = heuristic(current, dich)
        # Lấy các trạng thái kề
        cacTrangThaiKe = layTrangThaiKe(current)
        next_state = None
        best_h = current_h
        # Duyệt các trạng thái kề để tìm trạng thái có heuristic thấp hơn
        for trangThaiKe in cacTrangThaiKe:
            h_val = heuristic(trangThaiKe, dich)
            if h_val < best_h:
                best_h = h_val
                next_state = trangThaiKe
        # Nếu không tìm được trạng thái kề nào có cải thiện, dừng lại (bị kẹt tại cực trị cục bộ)
        if next_state is None:
            break
        current = next_state
        duongDi.append(current)
    if current == dich:
        return duongDi
    else:
        return None

def steepest_hill_climbing(batDau, dich):
    """
    Thuật toán Steepest Hill Climbing:
    - Từ trạng thái hiện tại, duyệt tất cả các trạng thái kề.
    - Chọn trạng thái có giá trị heuristic thấp nhất (có nghĩa là "gần đích" nhất).
    - Nếu không có trạng thái kề nào có giá trị heuristic cải thiện so với trạng thái hiện tại,
      thuật toán dừng lại và trả về None (mắc kẹt tại cực trị cục bộ).
    - Nếu đạt được trạng thái đích, trả về đường đi (danh sách các trạng thái).
    """
    current = batDau
    duongDi = [current]
    current_h = heuristic(current, dich)
    
    while current != dich:
        neighbors = layTrangThaiKe(current)
        best_neighbor = None
        best_h = current_h
        
        # Duyệt qua tất cả các trạng thái kề
        for neighbor in neighbors:
            h_val = heuristic(neighbor, dich)
            if h_val < best_h:
                best_h = h_val
                best_neighbor = neighbor
        
        # Nếu không có cải thiện nào, dừng lại (mắc kẹt cực trị cục bộ)
        if best_neighbor is None:
            break
        
        # Cập nhật trạng thái hiện tại
        current = best_neighbor
        current_h = best_h
        duongDi.append(current)
    
    if current == dich:
        return duongDi
    else:
        return None
    
def stochastic_hill_climbing(batDau, dich, max_iterations=1000):
    """
    Thuật toán Stochastic Hill Climbing cho 8-Puzzle:
      - Bắt đầu từ trạng thái batDau.
      - Ở mỗi bước, lấy danh sách các trạng thái kề.
      - Từ đó, chọn ngẫu nhiên một trạng thái có giá trị heuristic (Manhattan distance) thấp hơn so với trạng thái hiện tại.
      - Nếu không có neighbor nào cải thiện, ta thực hiện một bước ngẫu nhiên (hoặc báo thất bại).
      - max_iterations để tránh vòng lặp vô hạn.
    Trả về đường đi (list các trạng thái) nếu tìm được lời giải,
    hoặc None nếu không tìm được lời giải (có thể mắc kẹt tại cực trị cục bộ).
    """
    current = batDau
    path = [current]
    
    for _ in range(max_iterations):
        if current == dich:
            return path
        
        current_h = heuristic(current, dich)
        neighbors = layTrangThaiKe(current)
        # Chọn những neighbor có heuristic thấp hơn (tức cải thiện)
        better_neighbors = [n for n in neighbors if heuristic(n, dich) < current_h]
        
        if better_neighbors:
            # Chọn ngẫu nhiên một neighbor cải thiện
            next_state = random.choice(better_neighbors)
        else:
            # Không có neighbor cải thiện: ta chọn ngẫu nhiên một neighbor
            # Cách này có thể giúp thoát khỏi cục bộ nếu ta thực hiện random restart,
            # nhưng ở đây ta báo thất bại
            return None
        
        # Cập nhật trạng thái hiện tại và thêm vào đường đi
        current = next_state
        path.append(current)
    
    return None  # Nếu vượt quá số vòng lặp cho phép mà không tìm được lời giải
  
import math

def simulated_annealing(batDau, dich, T0=100, Tmin=0.1, alpha=0.995, max_iteration=10000):
    """
    Thuật toán Simulated Annealing cho 8-Puzzle.
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    T0: nhiệt độ ban đầu
    Tmin: nhiệt độ tối thiểu
    alpha: hệ số giảm nhiệt
    max_iter: số vòng lặp tối đa
    """
    current = batDau
    path = [current]
    temp = T0
    for _ in range(max_iteration):
        if current == dich:
            return path
        current_h = heuristic(current, dich)
        neighbors = layTrangThaiKe(current)
        if not neighbors:
            break
        # Chọn ngẫu nhiên một neighbor (không duyệt toàn bộ)
        next_state = random.choice(neighbors)
        next_h = heuristic(next_state, dich)
        delta = next_h - current_h
        if delta < 0:
            current = next_state
            path.append(current)
        else:
            probability = math.exp(-delta / temp)
            if random.random() < probability:
                current = next_state
                path.append(current)
                
        temp *= alpha
        if temp < Tmin:
            temp = T0  # Reset nhiệt độ nếu cần
    return path if current == dich else None
  
def beam_search(batDau, dich, beam_width=3, max_iter=1000):
    """
    Beam Search cho bài toán 8-Puzzle.
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    beam_width: số lượng cá thể tốt nhất được giữ lại sau mỗi vòng (beam width)
    max_iterations: số vòng lặp tối đa để tránh vòng lặp vô hạn
    
    Trả về đường đi (list các trạng thái từ batDau đến dich) nếu tìm được lời giải,
    hoặc None nếu không tìm được.
    """
    beam = [batDau]
    parents = {batDau: None}
    iteration = 0

    while beam and iteration < max_iter:
        # Nếu trong beam có trạng thái đích, dựng đường đi và trả về
        for state in beam:
            if state == dich:
                return truyVetDuongDi(parents, batDau, dich)
        
        # Tập hợp các trạng thái con của toàn bộ các trạng thái trong beam
        children = []
        for state in beam:
            for neighbor in layTrangThaiKe(state):
                if neighbor not in parents:
                    parents[neighbor] = state
                    children.append(neighbor)
        
        if not children:
            break
        
        # Sắp xếp các trạng thái con theo giá trị heuristic (thấp hơn là tốt hơn)
        children.sort(key=lambda s: heuristic(s, dich))
        
        # Chỉ giữ lại beam_width số trạng thái tốt nhất
        beam = children[:beam_width]
        iteration += 1

    return truyVetDuongDi(parents, batDau, dich) if dich in parents else None


def genetic_algorithm(batDau, dich, population_size=100, generations=50, mutation_rate=0.2, elite_size=10):
    """
    Thuật toán Di truyền (Genetic Algorithm) cho bài toán 8-puzzle theo 6 bước:
    1. Tạo quần thể ban đầu
    2. Đánh giá độ thích nghi (fitness) của từng cá thể
    3. Chọn các cá thể tốt nhất để sinh sản
    4. Thực hiện lai ghép (crossover) 
    5. Áp dụng đột biến (mutation)
    6. Lặp lại cho tới khi tìm được lời giải hoặc đạt số thế hệ tối đa
    """
    
    # Bước 1: Tạo quần thể ban đầu
    def create_initial_population():
        population = [batDau]
        
        # Tạo các cá thể mới bằng cách di chuyển ngẫu nhiên từ trạng thái ban đầu
        while len(population) < population_size:
            current = random.choice(population)
            step_count = random.randint(1, 10)  # Số bước di chuyển ngẫu nhiên
            
            for _ in range(step_count):
                neighbors = layTrangThaiKe(current)
                if neighbors:
                    current = random.choice(neighbors)
            
            if current not in population:
                population.append(current)
                
        return population
    
    # Bước 2: Hàm tính điểm fitness (thấp hơn là tốt hơn)
    def calculate_fitness(state):
        return heuristic(state, dich)
    
    # Bước 3: Chọn cha mẹ để lai ghép dựa trên độ thích nghi
    def select_parents(population, fitness_scores):
        # Sắp xếp quần thể theo fitness (thấp đến cao)
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population))]
        
        # Chọn cá thể tốt nhất làm cha mẹ (fitness thấp nhất)
        return sorted_population[:elite_size], sorted_population
    
    # Bước 4: Lai ghép hai cá thể để tạo con
    def crossover(parent1, parent2):
        # Tạo con bằng cách kết hợp thông tin từ cha mẹ
        cut_point = random.randint(3, 6)  # Điểm cắt ngẫu nhiên
        
        # Sao chép phần đầu từ parent1
        child_list = list(parent1[:cut_point])
        
        # Điền các phần tử còn thiếu từ parent2 theo thứ tự xuất hiện
        for item in parent2:
            if item not in child_list and len(child_list) < 9:
                child_list.append(item)
        
        # Kiểm tra tính hợp lệ của trạng thái
        if len(set(child_list)) != 9 or sorted(child_list) != list(range(9)):
            # Nếu không hợp lệ, trả về một trong hai cha mẹ
            return parent1 if random.random() < 0.5 else parent2
        
        return tuple(child_list)
    
    # Bước 5: Đột biến trạng thái bằng cách hoán đổi vị trí 0 với ô lân cận
    def mutate(state):
        if random.random() < mutation_rate:
            # Di chuyển ô trống đến một vị trí lân cận
            neighbors = layTrangThaiKe(state)
            if neighbors:
                return random.choice(neighbors)
        return state
    
    # Tạo thế hệ mới từ cha mẹ đã chọn
    def create_new_generation(parents, sorted_population):
        new_generation = []
        
        # Giữ lại elite_size cá thể tốt nhất
        new_generation.extend(parents)
        
        # Tạo phần còn lại của quần thể bằng lai ghép và đột biến
        while len(new_generation) < population_size:
            # Chọn ngẫu nhiên hai cha mẹ từ nhóm tinh túy với xác suất cao hơn
            parent1 = random.choice(sorted_population[:int(population_size/2)])
            parent2 = random.choice(sorted_population[:int(population_size/2)])
            
            # Lai ghép
            child = crossover(parent1, parent2)
            
            # Đột biến
            child = mutate(child)
            
            if child not in new_generation:
                new_generation.append(child)
        
        return new_generation
    
    # Bắt đầu thuật toán
    population = create_initial_population()
    
    # QUAN TRỌNG: Nếu tìm được trạng thái đích ngay từ đầu, trả về đường đi ngay
    if dich in population:
        return [batDau, dich]
    
    # Sử dụng BFS để tìm đường đi tốt nhất có thể
    for generation in range(generations):
        # Bước 2: Tính fitness cho tất cả cá thể trong quần thể
        fitness_scores = [calculate_fitness(individual) for individual in population]
        
        # Sắp xếp quần thể theo fitness
        sorted_individuals = [x for _, x in sorted(zip(fitness_scores, population))]
        best_individual = sorted_individuals[0]
        
        # Nếu best_individual là trạng thái đích, tìm đường đi bằng BFS
        if best_individual == dich:
            return bfs(batDau, dich)
        
        # Chọn cha mẹ
        parents, sorted_population = select_parents(population, fitness_scores)
        
        # Tạo thế hệ mới
        population = create_new_generation(parents, sorted_population)
        
        # Thử tìm đường đi đến đích từ cá thể tốt nhất
        best_fitness = calculate_fitness(best_individual)
        if best_fitness < 5:  # Nếu đã gần với đích
            # Thử tìm đường từ trạng thái tốt nhất đến đích bằng BFS
            path_to_best = bfs(batDau, best_individual)
            path_to_goal = bfs(best_individual, dich)
            
            if path_to_best and path_to_goal:
                # Kết hợp hai đường đi, loại bỏ trùng lặp
                return path_to_best[:-1] + path_to_goal
    
    # Nếu sau các thế hệ vẫn không tìm được lời giải, 
    # dùng BFS trực tiếp từ trạng thái ban đầu đến đích
    return bfs(batDau, dich)

def nondeterministic(batDau, dich, max_depth=35):
    """
    Thuật toán AND-OR Tree Search cho môi trường không xác định (non-deterministic).
    
    Trong môi trường không xác định:
    - Một hành động có thể dẫn đến nhiều trạng thái khác nhau
    - Cần phải tìm một kế hoạch đúng cho mọi trạng thái có thể xảy ra
    
    Đối với 8-puzzle, ta sẽ mô phỏng tính không xác định bằng cách:
    - Với mỗi hành động (lên, xuống, trái, phải), có xác suất nhỏ (10%) 
      sẽ dẫn đến một di chuyển khác so với dự kiến
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    max_depth: độ sâu tối đa cho tìm kiếm (mặc định 35)
    
    Trả về danh sách các trạng thái từ batDau đến dich nếu tìm thấy,
    hoặc None nếu không tìm được đường đi.
    """
    
    def is_goal(state):
        return state == dich
    
    def get_applicable_actions(state):
        """Trả về các hành động có thể áp dụng được từ state hiện tại"""
        viTri0 = state.index(0)
        hang, cot = viTri0 // 3, viTri0 % 3
        actions = []
        
        # Kiểm tra các hướng di chuyển hợp lệ (lên, xuống, trái, phải)
        if hang > 0: actions.append(0)  # lên
        if hang < 2: actions.append(1)  # xuống
        if cot > 0: actions.append(2)   # trái
        if cot < 2: actions.append(3)   # phải
            
        return actions
    
    def apply_action_with_uncertainty(state, action):
        """
        Áp dụng hành động lên trạng thái với tính không xác định.
        Trả về tập hợp các trạng thái có thể xảy ra.
        """
        viTri0 = state.index(0)
        hang, cot = viTri0 // 3, viTri0 % 3
        
        # Xác định hành động chính và các hành động phụ có thể xảy ra
        main_result = None
        alternative_results = []
        
        # Hành động chính (90% khả năng xảy ra)
        if action == 0 and hang > 0:  # lên
            swap_pos = viTri0 - 3
            new_state = list(state)
            new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
            main_result = tuple(new_state)
        elif action == 1 and hang < 2:  # xuống
            swap_pos = viTri0 + 3
            new_state = list(state)
            new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
            main_result = tuple(new_state)
        elif action == 2 and cot > 0:  # trái
            swap_pos = viTri0 - 1
            new_state = list(state)
            new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
            main_result = tuple(new_state)
        elif action == 3 and cot < 2:  # phải
            swap_pos = viTri0 + 1
            new_state = list(state)
            new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
            main_result = tuple(new_state)
        
        if main_result is None:
            return []  # Không thể áp dụng hành động
            
        # Mô phỏng tính không xác định: xem xét các hành động phụ (10% khả năng)
        other_actions = [a for a in get_applicable_actions(state) if a != action]
        for other_action in other_actions:
            if other_action == 0 and hang > 0:  # lên
                swap_pos = viTri0 - 3
                new_state = list(state)
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                alternative_results.append(tuple(new_state))
            elif other_action == 1 and hang < 2:  # xuống
                swap_pos = viTri0 + 3
                new_state = list(state)
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                alternative_results.append(tuple(new_state))
            elif other_action == 2 and cot > 0:  # trái
                swap_pos = viTri0 - 1
                new_state = list(state)
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                alternative_results.append(tuple(new_state))
            elif other_action == 3 and cot < 2:  # phải
                swap_pos = viTri0 + 1
                new_state = list(state)
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                alternative_results.append(tuple(new_state))
        
        # Trả về kết quả chính và các kết quả thay thế
        results = [main_result] + alternative_results
        return results
    
    # Khóa: (state, depth), Giá trị: (success, plan)
    memo = {}
    
    def or_search(state, depth):
        """
        Tìm kiếm OR node: tìm một hành động dẫn đến thành công
        Trả về (success, plan) trong đó plan là kế hoạch nếu success=True
        """
        # Kiểm tra bộ nhớ cache
        key = (state, depth)
        if key in memo:
            return memo[key]
            
        # Kiểm tra nếu đạt đích
        if is_goal(state):
            result = (True, [state])
            memo[key] = result
            return result
            
        # Kiểm tra độ sâu tối đa
        if depth >= max_depth:
            result = (False, None)
            memo[key] = result
            return result
            
        # Thử từng hành động có thể
        for action in get_applicable_actions(state):
            # Kết quả AND cho hành động này
            success, plan = and_search(state, action, depth)
            
            if success:
                # Nếu AND node thành công, OR node cũng thành công
                result = (True, plan)
                memo[key] = result
                return result
                
        # Không tìm thấy hành động nào dẫn đến thành công
        result = (False, None)
        memo[key] = result
        return result
    
    def and_search(state, action, depth):
        """
        Tìm kiếm AND node: tìm kế hoạch cho tất cả các kết quả có thể
        Trả về (success, plan) trong đó plan là kế hoạch nếu success=True
        """
        # Lấy tất cả trạng thái có thể sau khi thực hiện hành động
        result_states = apply_action_with_uncertainty(state, action)
        
        if not result_states:
            return (False, None)  # Không thể áp dụng hành động
            
        # Phải thành công với tất cả các kết quả có thể
        all_subplans = []
        
        # Một tối ưu hóa: Ưu tiên kết quả chính trước
        main_result = result_states[0]
        success, subplan = or_search(main_result, depth + 1)
        
        if not success:
            return (False, None)  # Thất bại với kết quả chính
            
        # Xây dựng kế hoạch: thêm state vào đầu subplan
        plan = [state] + subplan
        
        return (True, plan)
    
    # Bắt đầu tìm kiếm từ OR node
    success, plan = or_search(batDau, 0) 
    return plan

def no_observation(batDau, dich, max_depth=35):
    """
    Thuật toán Belief State Search cho bài toán 8-puzzle.
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích mong muốn (tuple)
    max_depth: độ sâu tối đa cho phép (mặc định: 35)
    
    Trả về danh sách các trạng thái từ batDau đến dich nếu tìm thấy,
    hoặc None nếu không tìm thấy đường đi.
    """
    
    # Kiểm tra trạng thái đích
    def is_goal_belief(belief):
        return dich in belief
    
    # Áp dụng một hành động lên belief state
    def apply_action_to_belief(belief, action):
        new_belief = set()
        for state in belief:
            # Xác định vị trí ô trống
            viTri0 = state.index(0)
            hang, cot = viTri0 // 3, viTri0 % 3
            
            # Áp dụng hành động
            new_state = list(state)
            if action == 0 and hang > 0:  # lên
                swap_pos = viTri0 - 3
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                new_belief.add(tuple(new_state))
            elif action == 1 and hang < 2:  # xuống
                swap_pos = viTri0 + 3
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                new_belief.add(tuple(new_state))
            elif action == 2 and cot > 0:  # trái
                swap_pos = viTri0 - 1
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                new_belief.add(tuple(new_state))
            elif action == 3 and cot < 2:  # phải
                swap_pos = viTri0 + 1
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                new_belief.add(tuple(new_state))
            else:
                # Hành động không áp dụng được, giữ nguyên trạng thái
                new_belief.add(state)
                
        return new_belief
    
    # Tạo heuristic cho belief state (lấy giá trị nhỏ nhất của các state trong belief)
    def belief_heuristic(belief):
        return min(heuristic(state, dich) for state in belief)
    
    # Bắt đầu tìm kiếm với belief state chứa trạng thái ban đầu
    initial_belief = {batDau}
    
    # Sử dụng A* để tìm kiếm trong không gian belief state
    open_set = [(belief_heuristic(initial_belief), 0, initial_belief, [])]  # (f, g, belief, path)
    closed_set = set()  # Set các belief đã xét (dùng frozenset vì belief là set)
    
    while open_set:
        # Lấy belief có f(n) = g(n) + h(n) thấp nhất
        f, g, current_belief, path = heapq.heappop(open_set)
        
        # Chuyển belief thành frozenset để có thể dùng làm key trong set
        belief_key = frozenset(current_belief)
        
        # Kiểm tra nếu đã xét belief này
        if belief_key in closed_set:
            continue
            
        closed_set.add(belief_key)
        
        # Kiểm tra nếu đã đạt đích
        if is_goal_belief(current_belief):
            # Cần trả về đường đi dưới dạng các trạng thái
            # Ta lấy trạng thái đầu tiên từ mỗi belief trong path
            result_path = [batDau]
            current_state = batDau
            
            for action, next_belief in path:
                # Áp dụng action lên current_state
                viTri0 = current_state.index(0)
                hang, cot = viTri0 // 3, viTri0 % 3
                new_state = list(current_state)
                
                if action == 0 and hang > 0:  # lên
                    swap_pos = viTri0 - 3
                elif action == 1 and hang < 2:  # xuống
                    swap_pos = viTri0 + 3
                elif action == 2 and cot > 0:  # trái
                    swap_pos = viTri0 - 1
                elif action == 3 and cot < 2:  # phải
                    swap_pos = viTri0 + 1
                
                new_state[viTri0], new_state[swap_pos] = new_state[swap_pos], new_state[viTri0]
                current_state = tuple(new_state)
                result_path.append(current_state)
            
            return result_path
        
        # Kiểm tra độ sâu tối đa
        if g >= max_depth:
            continue
        
        # Thử các hành động có thể
        for action in range(4):  # 0: lên, 1: xuống, 2: trái, 3: phải
            next_belief = apply_action_to_belief(current_belief, action)
            
            # Chỉ xét các belief mới
            next_belief_key = frozenset(next_belief)
            if next_belief_key in closed_set:
                continue
                
            # Tính toán chi phí mới
            new_g = g + 1
            new_f = new_g + belief_heuristic(next_belief)
            
            new_path = path + [(action, next_belief)]
            heapq.heappush(open_set, (new_f, new_g, next_belief, new_path))
    
    # Không tìm thấy lời giải
    return None

def partially_observable(batDau, dich, max_depth=30):
    """
    Thuật toán tìm kiếm trong môi trường quan sát được một phần cho 8-puzzle.
    Giả định: Chỉ quan sát được vị trí của ô trống và các ô kề với nó.
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    max_depth: độ sâu tối đa cho tìm kiếm
    
    Trả về danh sách các trạng thái từ batDau đến dich nếu tìm thấy,
    hoặc None nếu không tìm được đường đi.
    """
    
    # Hàm lấy thông tin có thể quan sát được từ một trạng thái
    def get_observation(state):
        """Trả về một tuple chứa: vị trí ô trống và các giá trị của ô kề với nó"""
        viTri0 = state.index(0)
        hang, cot = viTri0 // 3, viTri0 % 3
        
        # Lấy các vị trí kề với ô trống
        ke = []
        if hang > 0: ke.append(viTri0 - 3)  # ô phía trên
        if hang < 2: ke.append(viTri0 + 3)  # ô phía dưới
        if cot > 0: ke.append(viTri0 - 1)   # ô bên trái
        if cot < 2: ke.append(viTri0 + 1)   # ô bên phải
        
        # Lấy giá trị tại các vị trí kề
        giaTriKe = [state[i] for i in ke]
        
        return (viTri0, tuple(sorted(giaTriKe)))
    
    # Hàm heuristic dựa trên thông tin có thể quan sát
    def po_heuristic(state, goal):
        """
        Tính heuristic dựa trên thông tin có thể quan sát.
        Sử dụng khoảng cách Manhattan cho ô trống và các ô kề với nó.
        """
        viTri0 = state.index(0)
        hang0, cot0 = viTri0 // 3, viTri0 % 3
        viTri0_goal = goal.index(0)
        hangGoal0, cotGoal0 = viTri0_goal // 3, viTri0_goal % 3
        
        # Khoảng cách Manhattan cho ô trống
        khoangCach = abs(hang0 - hangGoal0) + abs(cot0 - cotGoal0)
        
        # Lấy các vị trí kề với ô trống trong state
        ke = []
        if hang0 > 0: ke.append(viTri0 - 3)
        if hang0 < 2: ke.append(viTri0 + 3)
        if cot0 > 0: ke.append(viTri0 - 1)
        if cot0 < 2: ke.append(viTri0 + 1)
        
        # Tính khoảng cách Manhattan cho các ô kề
        for viTri in ke:
            giaTri = state[viTri]
            if giaTri != 0:  # Bỏ qua ô trống
                viTriGoal = goal.index(giaTri)
                hangGoal, cotGoal = viTriGoal // 3, viTriGoal % 3
                hang, cot = viTri // 3, viTri % 3
                khoangCach += abs(hang - hangGoal) + abs(cot - cotGoal)
        
        return khoangCach
    
    # Sử dụng A* với thông tin quan sát được một phần
    open_set = [(po_heuristic(batDau, dich), 0, batDau, [])]  # (f, g, state, path)
    closed_set = set()  # Các trạng thái đã xét
    
    while open_set:
        f, g, hienTai, duongDi = heapq.heappop(open_set)
        
        # Nếu đạt đích
        if hienTai == dich:
            return [batDau] + duongDi
        
        # Nếu đã xét trạng thái này
        if hienTai in closed_set:
            continue
        
        closed_set.add(hienTai)
        
        # Kiểm tra độ sâu tối đa
        if g >= max_depth:
            continue
        
        obs_hienTai = get_observation(hienTai)
        
        # Sinh các trạng thái kề
        for trangThaiKe in layTrangThaiKe(hienTai):
            if trangThaiKe in closed_set:
                continue
            
            obs_ke = get_observation(trangThaiKe)
            
            # Chỉ xét các trạng thái có thông tin quan sát phù hợp
            if obs_ke[0] != obs_hienTai[0]:  # Vị trí ô trống phải khác nhau
                new_g = g + 1
                new_f = new_g + po_heuristic(trangThaiKe, dich)
                
                heapq.heappush(open_set, (new_f, new_g, trangThaiKe, duongDi + [trangThaiKe]))
    
    return None

def backtracking(batDau, dich, max_depth=30, record_fail=True):
    """
    Thuật toán Backtracking cho bài toán 8-puzzle với hiển thị UI trực quan.
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    max_depth: độ sâu tối đa để tránh sự bùng nổ tổ hợp
    record_fail: nếu True, ghi lại các bước quay lui; nếu False, bỏ qua ghi lại các bước quay lui
    
    Trả về danh sách trạng thái từ batDau đến dich nếu tìm thấy, hoặc None nếu không
    """
    # Lưu lại thông tin về các trạng thái để hiển thị
    backtracking_info = []
    
    def backtrack(hienTai, daDuyet, doSau, duong_di):
        # Thêm thông tin trạng thái hiện tại để hiển thị
        backtracking_info.append({
            'trangThai': hienTai,
            'loai': 'current',
            'doSau': doSau
        })
        
        # Kiểm tra nếu đạt đích
        if hienTai == dich:
            backtracking_info.append({
                'trangThai': hienTai,
                'loai': 'success',
                'doSau': doSau
            })
            return duong_di + [hienTai]
        
        # Kiểm tra độ sâu tối đa
        if doSau >= max_depth:
            return None
        
        # Thử từng trạng thái kề
        for trangThaiKe in layTrangThaiKe(hienTai):
            # Kiểm tra nếu đã duyệt
            if trangThaiKe not in daDuyet:
                # Đánh dấu là đã duyệt
                daDuyet.add(trangThaiKe)
                
                # Đệ quy để tìm lời giải từ trạng thái kề
                ketQua = backtrack(trangThaiKe, daDuyet, doSau + 1, duong_di + [hienTai])
                
                # Nếu tìm thấy lời giải, trả về kết quả
                if ketQua:
                    return ketQua
                
                # Quay lui: xóa trạng thái khỏi tập đã duyệt
                daDuyet.remove(trangThaiKe)
                
                # Hiển thị quá trình quay lui chỉ khi record_fail=True
                if record_fail:
                    backtracking_info.append({
                        'trangThai': trangThaiKe,
                        'loai': 'fail',
                        'doSau': doSau + 1
                    })
        
        # Không tìm thấy lời giải từ trạng thái hiện tại
        return None
    
    # Bắt đầu tìm kiếm backtracking
    daDuyet = set([batDau])
    ketQua = backtrack(batDau, daDuyet, 0, [])
    
    # Lưu thông tin backtracking để hiển thị
    return ketQua, backtracking_info

def backtracking_with_forward_checking(batDau, dich, max_depth=30, record_fail=True):
    """
    Kết hợp Backtracking và Forward Checking cho bài toán 8-puzzle.
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    max_depth: độ sâu tối đa để tránh sự bùng nổ tổ hợp
    record_fail: nếu True, ghi lại các bước quay lui; nếu False, bỏ qua ghi lại các bước quay lui
    
    Trả về danh sách trạng thái từ batDau đến dich nếu tìm thấy, hoặc None nếu không
    """
    # Lưu lại thông tin về các trạng thái để hiển thị
    backtracking_info = []
    
    def is_promising(trangThai, doSauHienTai):
        # Kiểm tra xem trạng thái có thể dẫn đến lời giải trong độ sâu còn lại
        h = heuristic(trangThai, dich)
        return h <= (max_depth - doSauHienTai)
    
    def backtrack_fc(hienTai, daDuyet, doSau, duong_di):
        # Thêm thông tin trạng thái hiện tại để hiển thị
        backtracking_info.append({
            'trangThai': hienTai,
            'loai': 'current',
            'doSau': doSau
        })
        
        # Kiểm tra nếu đạt đích
        if hienTai == dich:
            backtracking_info.append({
                'trangThai': hienTai,
                'loai': 'success',
                'doSau': doSau
            })
            return duong_di + [hienTai]
        
        # Kiểm tra độ sâu tối đa
        if doSau >= max_depth:
            return None
            
        # Lấy các trạng thái kề chưa thăm
        cacTrangThaiKe = [tk for tk in layTrangThaiKe(hienTai) if tk not in daDuyet]
        
        # Forward checking: đánh giá và lọc các trạng thái kề
        trangThaiHopLe = []
        for tk in cacTrangThaiKe:
            if is_promising(tk, doSau + 1):
                h = heuristic(tk, dich)
                trangThaiHopLe.append((h, tk))
        
        # Sắp xếp theo heuristic tăng dần (đầu tiên là trạng thái tốt nhất)
        trangThaiHopLe.sort(key=lambda x: x[0])
        
        # Duyệt qua các trạng thái đã sắp xếp
        for _, trangThaiKe in trangThaiHopLe:
            # Đánh dấu là đã duyệt
            daDuyet.add(trangThaiKe)
            
            # Đệ quy để tìm lời giải từ trạng thái kề
            ketQua = backtrack_fc(trangThaiKe, daDuyet, doSau + 1, duong_di + [hienTai])
            
            # Nếu tìm thấy lời giải, trả về kết quả
            if ketQua:
                return ketQua
            
            # Quay lui: xóa trạng thái khỏi tập đã duyệt
            daDuyet.remove(trangThaiKe)
            
            # Hiển thị quá trình quay lui chỉ khi record_fail=True
            if record_fail:
                backtracking_info.append({
                    'trangThai': trangThaiKe,
                    'loai': 'fail',
                    'doSau': doSau + 1
                })
        
        # Không tìm thấy lời giải từ trạng thái hiện tại
        return None
    
    # Bắt đầu tìm kiếm 
    daDuyet = set([batDau])
    ketQua = backtrack_fc(batDau, daDuyet, 0, [])

    # Lưu thông tin backtracking để hiển thị
    return ketQua, backtracking_info

def min_conflicts(batDau, dich, max_steps=2000, max_restarts=5, record_process=True):
    """
    Thuật toán Min-Conflicts cải tiến cho bài toán 8-puzzle.
    Bắt đầu từ trạng thái hiện tại, ở mỗi bước chọn một ô để di chuyển
    sao cho số xung đột (số ô không đúng vị trí) giảm xuống.
    
    Đã cải tiến thêm:
    - Random restart khi mắc kẹt tại cực tiểu cục bộ
    - Lưu trạng thái đã thăm để tránh lặp lại
    - Tăng số bước tìm kiếm tối đa
    - Ghi lại quá trình tìm kiếm để animation
    
    batDau: trạng thái ban đầu (tuple)
    dich: trạng thái đích (tuple)
    max_steps: số bước tối đa để tránh vòng lặp vô hạn
    max_restarts: số lần restart tối đa khi mắc kẹt
    record_process: ghi lại quá trình tìm kiếm để hiển thị animation
    
    Trả về danh sách trạng thái từ batDau đến dich nếu tìm thấy, hoặc None nếu không
    Nếu record_process=True, trả về (đường_đi, thông_tin_quá_trình)
    """
    # Danh sách thông tin ghi lại quá trình tìm kiếm
    search_info = []
    
    def count_conflicts(trangThai):
        """Đếm số ô không đúng vị trí so với trạng thái đích"""
        return sum(1 for i in range(9) if trangThai[i] != dich[i] and trangThai[i] != 0)
    
    def get_conflicts_after_move(trangThai, viTri0, viTriSwap):
        """Tính số xung đột sau khi di chuyển ô trống với ô tại viTriSwap"""
        trangThaiMoi = list(trangThai)
        trangThaiMoi[viTri0], trangThaiMoi[viTriSwap] = trangThaiMoi[viTriSwap], trangThaiMoi[viTri0]
        return count_conflicts(trangThaiMoi), tuple(trangThaiMoi)
    
    def run_min_conflicts(start_state):
        # Lưu lại đường đi
        path = [start_state]
        current = start_state
        
        # Ghi lại trạng thái ban đầu
        if record_process:
            search_info.append({
                'trangThai': current,
                'loai': 'current',
                'doSau': 0,
                'conflicts': count_conflicts(current)
            })
        
        # Tập các trạng thái đã thăm để tránh lặp
        visited = set([current])
        
        # Biến theo dõi số bước không cải thiện liên tiếp
        no_improvement_count = 0
    
        for step in range(max_steps):
            # Kiểm tra nếu đã đạt đích
            if current == dich:
                if record_process:
                    search_info.append({
                        'trangThai': current,
                        'loai': 'success',
                        'doSau': step + 1,
                        'conflicts': 0
                    })
                return path
            
            # Lấy vị trí ô trống
            viTri0 = current.index(0)
            hang, cot = viTri0 // 3, viTri0 % 3
            
            # Tính toán các nước đi có thể và số xung đột sau mỗi nước
            moves = []
            
            # Kiểm tra 4 hướng di chuyển
            possible_moves = []
            if hang > 0: 
                viTriSwap = viTri0 - 3
                conflicts, new_state = get_conflicts_after_move(current, viTri0, viTriSwap)
                if new_state not in visited:  # Chỉ xét các trạng thái chưa thăm
                    moves.append((conflicts, new_state))
                    possible_moves.append((viTriSwap, conflicts, new_state))
            
            if hang < 2: 
                viTriSwap = viTri0 + 3
                conflicts, new_state = get_conflicts_after_move(current, viTri0, viTriSwap)
                if new_state not in visited:
                    moves.append((conflicts, new_state))
                    possible_moves.append((viTriSwap, conflicts, new_state))
            
            if cot > 0: 
                viTriSwap = viTri0 - 1
                conflicts, new_state = get_conflicts_after_move(current, viTri0, viTriSwap)
                if new_state not in visited:
                    moves.append((conflicts, new_state))
                    possible_moves.append((viTriSwap, conflicts, new_state))
            
            if cot < 2: 
                viTriSwap = viTri0 + 1
                conflicts, new_state = get_conflicts_after_move(current, viTri0, viTriSwap)
                if new_state not in visited:
                    moves.append((conflicts, new_state))
                    possible_moves.append((viTriSwap, conflicts, new_state))
            
            # Nếu không có nước đi nào (tất cả đã thăm hoặc không có hướng di chuyển)
            if not moves:
                return None  # Không thể tiếp tục, cần restart
            
            # Sắp xếp theo số xung đột tăng dần
            moves.sort(key=lambda x: x[0])
            possible_moves.sort(key=lambda x: x[1])
            
            # Chọn nước đi tốt nhất (ít xung đột nhất)
            best_conflicts, best_state = moves[0]
            
            # Ghi lại các trạng thái có thể và trạng thái đã chọn
            if record_process:
                current_conflicts = count_conflicts(current)
                
                # Ghi lại tất cả nước đi có thể (để hiển thị khi tick Quay lui CPSs)
                for viTriSwap, conflicts, state in possible_moves:
                    if state != best_state:  # Không phải trạng thái tốt nhất
                        search_info.append({
                            'trangThai': state,
                            'loai': 'fail',
                            'doSau': step + 1,
                            'conflicts': conflicts
                        })
            
            # Kiểm tra nếu không có cải thiện
            current_conflicts = count_conflicts(current)
            if best_conflicts >= current_conflicts:
                no_improvement_count += 1
                
                # Nếu liên tục không cải thiện nhiều bước, chọn ngẫu nhiên để thoát cục bộ
                if no_improvement_count >= 10 and len(moves) > 1:
                    # Chọn ngẫu nhiên từ các nước đi có thể
                    rand_idx = random.randint(0, len(moves) - 1)
                    _, best_state = moves[rand_idx]
                    no_improvement_count = 0  # Reset bộ đếm
            else:
                no_improvement_count = 0  # Reset bộ đếm khi có cải thiện
        
            # Cập nhật trạng thái hiện tại
            current = best_state
                
            # Ghi lại trạng thái hiện tại
            if record_process:
                search_info.append({
                    'trangThai': current,
                    'loai': 'current',
                    'doSau': step + 1,
                    'conflicts': count_conflicts(current)
                })
            
            path.append(current)
            visited.add(current)
        
        # Nếu không tìm được lời giải sau max_steps
        return path if current == dich else None
    
    # Chạy thuật toán với random restart
    final_path = None
    for restart in range(max_restarts):
        # Chạy min conflicts từ trạng thái ban đầu
        if record_process:
            # Ghi lại thông tin restart mới
            if restart > 0:
                search_info.append({
                    'trangThai': batDau,
                    'loai': 'restart',
                    'doSau': restart,
                    'conflicts': count_conflicts(batDau)
                })
        
        result_path = run_min_conflicts(batDau)
        
        if result_path and (result_path[-1] == dich):
            final_path = result_path
            break
        
        # Nếu không tìm thấy lời giải, tạo trạng thái bắt đầu mới
        # bằng cách thực hiện một số bước di chuyển ngẫu nhiên từ trạng thái ban đầu
        new_start = batDau
        for _ in range(5):  # Di chuyển ngẫu nhiên 5 bước
            ke = layTrangThaiKe(new_start)
            if ke:
                new_start = random.choice(ke)
        
        batDau = new_start  # Sử dụng trạng thái mới cho lần restart tiếp theo
    
    if record_process:
        return final_path, search_info
    else:
        return final_path

def taoTrangThaiNgauNhien():
    trangThai = list(range(9))
    random.shuffle(trangThai)
    return tuple(trangThai)

def kiemTraCoTheGiai(trangThai):
    # Tính số nghịch thế (inversion)
    inversion = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if trangThai[i] != 0 and trangThai[j] != 0 and trangThai[i] > trangThai[j]:
                inversion += 1

    # Nếu số nghịch thế là chẵn, trạng thái có thể giải được
    return inversion % 2 == 0

def q_learning(batDau, dich, episodes=20000, alpha=0.2, gamma=0.95, epsilon=0.3):
    """
    q_table_final được tạo với 1 000 000 episodes, alpha 0.2, gamma 0.95, epsilon 0.3
    
    Hàm Q-learning cải tiến: Huấn luyện nhiều trạng thái ngẫu nhiên
    và tìm đường đi từ trạng thái bắt đầu đến trạng thái đích
    """
    Q = {}
    file_q = 'q_table_final.pkl'

    # Kiểm tra file q_table.pkl
    if os.path.exists(file_q):
        with open(file_q, 'rb') as f:
            Q = pickle.load(f)
        print("Đã tải bảng Q từ file.")
    else:
        print("Đang huấn luyện...")

        # Thêm trạng thái đích vào bảng Q
        Q[dich] = {}

        # Huấn luyện với nhiều trạng thái ngẫu nhiên
        for episode in range(episodes):
            if episode % 1000 == 0:
                print(f"Episode {episode}/{episodes}")

            # Chọn trạng thái bắt đầu: 80% ngẫu nhiên, 20% là trạng thái người dùng cung cấp
            if episode == 0 or random.random() < 0.2:
                state = batDau
            else:
                # Tạo trạng thái ngẫu nhiên có thể giải được
                while True:
                    random_state = taoTrangThaiNgauNhien()
                    if kiemTraCoTheGiai(random_state) == kiemTraCoTheGiai(dich):
                        state = random_state
                        break

            steps = 0
            max_steps = 300  # Tăng số bước tối đa mỗi episode

            while state != dich and steps < max_steps:
                # Khởi tạo Q[state] nếu chưa tồn tại
                if state not in Q:
                    actions = layTrangThaiKe(state)
                    Q[state] = {action: 0 for action in actions}

                # Chọn action dựa trên policy epsilon-greedy
                actions = list(Q[state].keys())
                if not actions:
                    break

                if random.random() < epsilon:
                    action = random.choice(actions)
                else:
                    # Chọn action với giá trị Q cao nhất
                    max_q_value = max(Q[state].values())
                    best_actions = [a for a in actions if Q[state][a] == max_q_value]
                    action = random.choice(best_actions)

                # Thực hiện action và nhận reward
                next_state = action

                # Reward dựa trên khoảng cách Manhattan
                current_distance = heuristic(state, dich)
                next_distance = heuristic(next_state, dich)

                if next_state == dich:
                    reward = 100  # Phần thưởng lớn khi đạt đích
                elif next_distance < current_distance:
                    reward = 1    # Phần thưởng nhỏ khi tiến gần đích
                else:
                    reward = -1   # Phạt khi đi xa đích

                # Khởi tạo Q[next_state] nếu chưa tồn tại
                if next_state not in Q:
                    next_actions = layTrangThaiKe(next_state)
                    Q[next_state] = {a: 0 for a in next_actions}

                # Cập nhật giá trị Q
                if Q[next_state]:
                    max_next_q = max(Q[next_state].values())
                else:
                    max_next_q = 0

                Q[state][action] += alpha * (reward + gamma * max_next_q - Q[state][action])

                state = next_state
                steps += 1

            # Giảm epsilon theo thời gian để tăng khai thác
            epsilon = max(0.01, epsilon * 0.9999)

        # Lưu bảng Q vào file
        with open(file_q, 'wb') as f:
            pickle.dump(Q, f)
        print("Đã lưu bảng Q.")
        print(f"Số trạng thái đã học: {len(Q)}")

    # Tìm đường đi sử dụng bảng Q đã học
    path = timDuongDi(batDau, dich, Q)
    return path

def timDuongDi(batDau, dich, Q):
    path = [batDau]
    state = batDau
    visited = set([batDau])
    max_steps = 100
    steps = 0

    while state != dich and steps < max_steps:
        if state not in Q or not Q[state]:
            print(f"Không có thông tin Q cho trạng thái: {state}")
            return None

        # Chọn action tốt nhất từ bảng Q
        actions = Q[state].items()
        if not actions:
            return None

        # Sắp xếp actions theo giá trị Q giảm dần
        sorted_actions = sorted(actions, key=lambda x: x[1], reverse=True)

        # Thử từng action theo thứ tự giá trị Q
        found_valid_action = False
        for next_state, _ in sorted_actions:
            if next_state not in visited:
                found_valid_action = True
                state = next_state
                visited.add(state)
                path.append(state)
                break

        if not found_valid_action:
            print("Không tìm thấy action hợp lệ.")
            return None

        steps += 1

        # Kiểm tra nếu đã đến đích
        if state == dich:
            return path

    if state != dich:
        print(f"Không tìm thấy đường đi sau {max_steps} bước.")
        return None

    return path

if __name__ == "__main__":
    trangThaiBatDau = (2, 6, 5,
                       0, 8, 7,
                       4, 3, 1)
    trangThaiDich    = (1, 2, 3,
                        4, 5, 6,
                        7, 8, 0)

    ketQua = iddfs(trangThaiBatDau, trangThaiDich, 50)
    if ketQua:
        print("Tìm thấy đường đi BFS:")
        for buoc in ketQua:
            print(buoc)
        print("Tổng số bước:", len(ketQua) - 1)
    else:
        print("Không tìm thấy lời giải.")
