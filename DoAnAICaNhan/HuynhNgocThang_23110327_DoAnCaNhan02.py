import tkinter as tk
import tkinter.messagebox as messagebox
import random
from HuynhNgocThang_23110327_DoAnCaNhan01 import (bfs, dfs, iddfs, 
                                                   greedy, ucs, a_sao, ida_sao, 
                                                   simple_hill_climbing, steepest_hill_climbing, stochastic_hill_climbing, simulated_annealing,
                                                   beam_search, genetic_algorithm, nondeterministic, no_observation, partially_observable,
                                                   backtracking, min_conflicts, q_learning,
                                                   backtracking_with_forward_checking) 
import time
from PIL import Image, ImageTk, ImageGrab
import datetime
import os
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import numpy as np
import networkx as nx

CELL_SIZE = 95
ANIMATION_STEPS = 10
ANIMATION_DELAY = 10

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2 - 45
    window.geometry(f"{width}x{height}+{x}+{y}")
    
    window.resizable(False, False)

class GiaoDien8Puzzle:
    def __init__(self, cuaSoChinh):
        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "IDFS": lambda s, d: iddfs(s, d, 50),
            "Greedy": greedy,
            "UCS": ucs,
            "AStar": a_sao,
            "IDAStar": ida_sao,
            "Simple HC": simple_hill_climbing,
            "Steepest HC": steepest_hill_climbing,
            "Stochastic HC": stochastic_hill_climbing,
            "Simulated Annealing": simulated_annealing,
            "Beam Search": beam_search,
            "Genetic Algorithm": genetic_algorithm,
            "Non Deterministic": nondeterministic,
            "No Observation": no_observation,
            "Partially Observable": partially_observable,
            "Backtracking": backtracking,
            "Backtracking with FC": backtracking_with_forward_checking,
            "Min Conflicts":min_conflicts,
            "Q-learning": q_learning,
        }
        self.is_partially_observable_mode = False
        self.show_backtrack = tk.BooleanVar(value=False) # Mặc định hiển thị ko quay lui

        self.editing = False
        self.new_state = []

        self.cuaSoChinh = cuaSoChinh
        
        self.recording = False
        self.frames = []
        
        # Frame cho các điều khiển quay GIF
        self.gif_control_frame = tk.Frame(cuaSoChinh)
        self.gif_control_frame.grid(row=7, column=2, columnspan=3, pady=5)
        
        # Toggle button để bật/tắt quay GIF
        self.record_var = tk.BooleanVar()
        self.record_toggle = tk.Checkbutton(
            self.gif_control_frame, text="Quay GIF", variable=self.record_var,
            command=self.toggle_recording, font=("Arial", 10)
        )
        self.record_toggle.pack(side=tk.LEFT, padx=10)
        
        # Checkbox để bật/tắt hiển thị quay lui
        self.backtrack_toggle = tk.Checkbutton(
            self.gif_control_frame, text="Quay lui CPSs", variable=self.show_backtrack,
            font=("Arial", 10)
        )
        self.backtrack_toggle.pack(side=tk.LEFT, padx=10)
        
        # Nút xem node để hiển thị đồ thị đường đi
        self.view_node_button = tk.Button(
            self.gif_control_frame, text="Xem node", font=("Arial", 10),
            command=self.hienThiDoThiDuongDi, bg="#d1eaff"
        )
        self.view_node_button.pack(side=tk.LEFT, padx=10)
        
        self.frame_skip_var = tk.IntVar(value=1)  # Mặc định lấy mỗi frame

        
        # Nhãn trạng thái quay
        self.record_status = tk.Label(cuaSoChinh, text="", font=("Arial", 10), fg="blue")
        self.record_status.grid(row=9, column=0, columnspan=3, pady=5)
    
        self.board_size = 3 * CELL_SIZE
        self.canvas = tk.Canvas(cuaSoChinh, width=self.board_size, height=self.board_size)
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=1)
        
        for i in range(4):
            self.canvas.create_line(0, i*CELL_SIZE, self.board_size, i*CELL_SIZE, width=2)
            self.canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, self.board_size, width=2)
        
        # Tạo frame cho nút chọn thuật toán
        self.algo_frame = tk.Frame(self.cuaSoChinh)
        self.algo_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.nutBFS = tk.Button(self.algo_frame, text="BFS", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("BFS"), width=10, height=2)
        self.nutBFS.grid(row=0, column=0, padx=5, pady=5)

        self.nutDFS = tk.Button(self.algo_frame, text="DFS", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("DFS"), width=10, height=2)
        self.nutDFS.grid(row=0, column=1, padx=5, pady=5)

        self.nutIDFS = tk.Button(self.algo_frame, text="IDFS", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("IDFS"), width=10, height=2)
        self.nutIDFS.grid(row=0, column=2, padx=5, pady=5)

        self.nutUCS = tk.Button(self.algo_frame, text="UCS", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("UCS"), width=10, height=2)
        self.nutUCS.grid(row=0, column=3, padx=5, pady=5)

        self.nutGreedy = tk.Button(self.algo_frame, text="Greedy", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("Greedy"), width=10, height=2)
        self.nutGreedy.grid(row=1, column=0, padx=5, pady=5)

        self.nutAstar = tk.Button(self.algo_frame, text="A*", font=("Arial", 13),
                                command=lambda: self.giaiThuatToan("AStar"), width=10, height=2)
        self.nutAstar.grid(row=1, column=1, padx=5, pady=5)

        self.nutIDAstar = tk.Button(self.algo_frame, text="IDA*", font=("Arial", 13),
                                    command=lambda: self.giaiThuatToan("IDAStar"), width=10, height=2)
        self.nutIDAstar.grid(row=1, column=2, padx=5, pady=5)

        self.nutSimpleHC = tk.Button(self.algo_frame, text="Simple HC", font=("Arial", 11),
                                    command=lambda: self.giaiThuatToan("Simple HC"), width=10, height=2)
        self.nutSimpleHC.grid(row=1, column=3, padx=5, pady=5)

        self.nutSteepestHC = tk.Button(self.algo_frame, text="Steepest HC", font=("Arial", 11),
                                    command=lambda: self.giaiThuatToan("Steepest HC"), width=10, height=2)
        self.nutSteepestHC.grid(row=2, column=0, padx=5, pady=5)

        self.nutStochasticHC = tk.Button(self.algo_frame, text="Stochastic HC", font=("Arial", 11),
                                        command=lambda: self.giaiThuatToan("Stochastic HC"), width=10, height=2)
        self.nutStochasticHC.grid(row=2, column=1, padx=5, pady=5)

        self.nutSimulatedAnnealing = tk.Button(self.algo_frame, text="Simulated \nAnnealing", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Simulated Annealing"), width=10, height=2)
        self.nutSimulatedAnnealing.grid(row=2, column=2, padx=5, pady=5)

        self.nutBeam = tk.Button(self.algo_frame, text="Beam Search", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Beam Search"), width=10, height=2)
        self.nutBeam.grid(row=2, column=3, padx=5, pady=5)
        
        self.nutGenetic = tk.Button(self.algo_frame, text="Genetic Alg", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Genetic Algorithm"), width=10, height=2)
        self.nutGenetic.grid(row=3, column=0, padx=5, pady=5)
        
        self.nutAndOrTree = tk.Button(self.algo_frame, text="Non\nDeterministic", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Non Deterministic"), width=10, height=2)
        self.nutAndOrTree.grid(row=3, column=1, padx=5, pady=5)

        self.nutBeliefSearch = tk.Button(self.algo_frame, text="No\nObservation", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("No Observation"), width=10, height=2)
        self.nutBeliefSearch.grid(row=3, column=2, padx=5, pady=5)
        
        self.nutPartiallyObservable = tk.Button(self.algo_frame, text="Partially\nObservable", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Partially Observable"), width=10, height=2)
        self.nutPartiallyObservable.grid(row=3, column=3, padx=5, pady=5)
        
        self.nutBacktracking = tk.Button(self.algo_frame, text="Backtracking", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Backtracking"), width=10, height=2)
        self.nutBacktracking.grid(row=4, column=0, padx=5, pady=5)
        
        self.nutBacktrackingFC = tk.Button(self.algo_frame, text="Backtracking\nwith FC", font=("Arial", 10),
                                command=lambda: self.giaiThuatToan("Backtracking with FC"), width=10, height=2)
        self.nutBacktrackingFC.grid(row=4, column=1, padx=5, pady=5)
        
        self.nutMinConflicts = tk.Button(self.algo_frame, text="Min\nConflicts", font=("Arial", 11),
                                command=lambda: self.giaiThuatToan("Min Conflicts"), width=10, height=2)
        self.nutMinConflicts.grid(row=4, column=2, padx=5, pady=5)
        
        self.nutQLearning = tk.Button(self.algo_frame, text="Q-learning", font=("Arial", 11),
                              command=lambda: self.giaiThuatToan("Q-learning"), width=10, height=2)
        self.nutQLearning.grid(row=4, column=3, padx=5, pady=5)
        
        self.nutTao = tk.Button(cuaSoChinh, text="Tạo rand",font=("Arial", 9), command=self.taoTrangThaiNgauNhien, width=10, height=2)
        self.nutTao.grid(row=5, column=0, padx=1, pady=1)
        
        self.nutUndo = tk.Button(cuaSoChinh, text="Quay về lúc\nchưa sắp xếp", font=("Arial", 9), command=self.undoTrangThai, width=10, height=2)
        self.nutUndo.grid(row=5, column=2, padx=5, pady=1)
        
        self.nutSua = tk.Button(cuaSoChinh, text="Sửa", font=("Arial", 9), command=self.suaTrangThai, width=10, height=2)
        self.nutSua.grid(row=5, column=1, padx=5, pady=1)

        self.nutDung = tk.Button(cuaSoChinh, text="Dừng", font=("Arial", 9), command=self.dungGiaiThuatToan, width=10, height=2, bg="#ffaaaa")
        self.nutDung.grid(row=6, column=1, padx=5, pady=5)
        
        self.nutSoSanh = tk.Button(cuaSoChinh, text="So sánh\nthuật toán", font=("Arial", 9), command=self.moSoSanhThuatToan, width=10, height=2, bg="#aaffcc")
        self.nutSoSanh.grid(row=6, column=2, padx=5, pady=5)

        self.lblKetQua = tk.Label(cuaSoChinh, text="Time: ", font=("Arial", 12), fg="red")
        self.lblKetQua.grid(row=7, column=0, columnspan=3, padx=5, pady=1)
        
        # khung bảng hiển thị đường đi (bên phải)
        self.solution_frame = tk.Frame(cuaSoChinh)
        self.solution_frame.grid(row=0, column=3, rowspan=7, padx=10, pady=1, sticky="ns")
        self.scrollbar = tk.Scrollbar(self.solution_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txtSolution = tk.Text(self.solution_frame, width=40, height=20, yscrollcommand=self.scrollbar.set)
        self.txtSolution.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.txtSolution.config(state="disabled")  # Vô hiệu hóa chỉnh sửa từ đầu
        self.scrollbar.config(command=self.txtSolution.yview)

        # Scale để điều chỉnh Animation Delay (ms)
        self.animation_delay = ANIMATION_DELAY 
        self.scaleSpeed = tk.Scale(self.cuaSoChinh, from_=1, to=50, orient=tk.HORIZONTAL,
                                length=300,
                                command=self.update_speed, font=("Arial", 10))
        self.scaleSpeed.set(ANIMATION_DELAY)
        self.scaleSpeed.grid(row=8, column=0, columnspan=3, pady=10)

        self.trangThaiBatDau = (2, 6, 5,
                                0, 8, 7,
                                4, 3, 1)
        self.trangThaiDich   = (1, 2, 3,
                                4, 5, 6,
                                7, 8, 0)
        self.current_state = self.trangThaiBatDau
        self.daySo = list(range(9))

        self.tile_items = {}
        self.animationPlay = False
        self.animation_jobs = []  # Danh sách các job animation
        self.veTrangThai(self.current_state)
    
    def get_cell_center(self, index):
        row = index // 3
        col = index % 3
        x = col * CELL_SIZE + CELL_SIZE/2
        y = row * CELL_SIZE + CELL_SIZE/2
        return x, y
    
    def veTrangThai(self, trangThai, partially_observable_mode=False):
        for item in self.tile_items.values():
            self.canvas.delete(item[0])
            self.canvas.delete(item[1])
        self.tile_items = {}
        
        if partially_observable_mode:
            # Tìm vị trí ô trống (số 0)
            viTri0 = trangThai.index(0)
            hang0, cot0 = viTri0 // 3, viTri0 % 3
            
            # Xác định các ô kề với ô trống
            ke = []
            if hang0 > 0: ke.append(viTri0 - 3)  # ô phía trên
            if hang0 < 2: ke.append(viTri0 + 3)  # ô phía dưới
            if cot0 > 0: ke.append(viTri0 - 1)   # ô bên trái
            if cot0 < 2: ke.append(viTri0 + 1)   # ô bên phải
            
            # Vẽ các ô có thể quan sát được
            for index, giaTri in enumerate(trangThai):
                x, y = self.get_cell_center(index)
                # Nếu là ô trống hoặc kề với ô trống mới hiển thị, còn lại hiển thị màu xám
                if index == viTri0 or index in ke:
                    if giaTri != 0:
                        rect = self.canvas.create_rectangle(x - CELL_SIZE/2 + 10, y - CELL_SIZE/2 + 10,
                                                        x + CELL_SIZE/2 - 10, y + CELL_SIZE/2 - 10,
                                                        fill="lightblue")
                        text = self.canvas.create_text(x, y, text=str(giaTri), font=("Arial", 24))
                        self.tile_items[giaTri] = (rect, text)
                else:
                    # Hiển thị ô mờ đi hoặc dấu hỏi cho các ô không quan sát được
                    rect = self.canvas.create_rectangle(x - CELL_SIZE/2 + 10, y - CELL_SIZE/2 + 10,
                                                    x + CELL_SIZE/2 - 10, y + CELL_SIZE/2 - 10,
                                                    fill="gray")
                    text = self.canvas.create_text(x, y, text="?", font=("Arial", 24), fill="white")
                    self.tile_items[giaTri] = (rect, text)
        else:
            # Chế độ hiển thị bình thường
            for index, giaTri in enumerate(trangThai):
                if giaTri != 0:
                    x, y = self.get_cell_center(index)
                    rect = self.canvas.create_rectangle(x - CELL_SIZE/2 + 10, y - CELL_SIZE/2 + 10,
                                                    x + CELL_SIZE/2 - 10, y + CELL_SIZE/2 - 10,
                                                    fill="lightblue")
                    text = self.canvas.create_text(x, y, text=str(giaTri), font=("Arial", 24))
                    self.tile_items[giaTri] = (rect, text)
        
        self.current_state = trangThai
    
    def taoTrangThaiNgauNhien(self):
        if self.animationPlay == True:
            return
        
        self.lblKetQua.config(text=f"Time: ")
        random.shuffle(self.daySo)
        self.trangThaiBatDau = tuple(self.daySo)
        self.veTrangThai(self.trangThaiBatDau)
        
    def undoTrangThai(self):
        if self.animationPlay == True:
            return
        self.veTrangThai(self.trangThaiBatDau)
    
    def giaiThuatToan(self, tenThuatToan):
        if self.animationPlay:
            return
        
        func = self.algorithms.get(tenThuatToan)
        if func is None:
            self.lblKetQua.config(text="Thuật toán không hợp lệ!")
            return

        # Xử lý đặc biệt cho No Observation
        if tenThuatToan == "No Observation":
            self.moGiaoDienNoObservation()
            return
        
        # Reset frames nếu bắt đầu quay mới
        if self.recording:
            self.frames = []
            self.record_status.config(text=f"Đang quay {tenThuatToan}...")
        
        start_time = time.time()
        
        # Xử lý đặc biệt cho Backtracking và Backtracking with FC
        if tenThuatToan == "Backtracking" or tenThuatToan == "Backtracking with FC":
            duongDi, self.backtracking_info = func(self.current_state, self.trangThaiDich, 
                                                   record_fail=self.show_backtrack.get())
            # Lưu đường đi cuối cùng để sử dụng khi không hiển thị quay lui
            self.duongDi_cuoi = duongDi
        # Xử lý đặc biệt cho Min Conflicts
        elif tenThuatToan == "Min Conflicts":
            result = func(self.current_state, self.trangThaiDich, record_process=self.show_backtrack.get())
            if self.show_backtrack.get():
                duongDi, self.backtracking_info = result  # Nhận về đường đi và thông tin quá trình
                self.duongDi_cuoi = duongDi
            else:
                duongDi = result  # Chỉ nhận về đường đi
        else:
            duongDi = func(self.current_state, self.trangThaiDich)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if duongDi is None:
            self.lblKetQua.config(text=f"{tenThuatToan}: Không tìm thấy lời giải")
            self.txtSolution.config(state="normal")
            self.txtSolution.delete("1.0", tk.END)
            self.txtSolution.config(state="disabled")
        else:
            self.animationPlay = True
            
            steps = len(duongDi) - 1
            self.lblKetQua.config(text=f"{tenThuatToan}: Thời gian = {elapsed:.4f}s, Số bước = {steps}")
            self.txtSolution.config(state="normal")
            self.txtSolution.delete("1.0", tk.END)
            
            for idx, buoc in enumerate(duongDi):
                self.txtSolution.insert(tk.END, f"Bước {idx}: {buoc}\n")
            self.txtSolution.config(state="disabled")
            
            # Nếu là backtracking hoặc min_conflicts với checkbox được chọn, hiển thị quá trình tìm kiếm
            if (tenThuatToan in ["Backtracking", "Backtracking with FC", "Min Conflicts"] 
                and hasattr(self, 'backtracking_info') and self.show_backtrack.get()):
                self.animate_backtracking(0)
            else:
                # Nếu đang quay, chụp frame đầu tiên
                if self.recording:
                    self.capture_canvas()
                
                # Kiểm tra nếu là thuật toán Partially Observable
                is_partially_observable = (tenThuatToan == "Partially Observable")
                
                # Gán giá trị cho biến để theo dõi trạng thái hiển thị
                self.is_partially_observable_mode = is_partially_observable
                
                # Vẽ lại trạng thái hiện tại với chế độ thích hợp
                self.veTrangThai(self.current_state, is_partially_observable)
                
                # Animate giải pháp với chế độ thích hợp
                self.animate_solution(duongDi, 0)

    def veTrangThaiBacktracking(self, trangThai, loai):
        # Xóa tất cả các item hiện tại
        for item in self.tile_items.values():
            self.canvas.delete(item[0])
            self.canvas.delete(item[1])
        self.tile_items = {}
        
        # Màu sắc cho từng loại trạng thái
        colors = {
            "current": "lightblue",     # Đang xét
            "success": "gold",          # Tìm thấy đích
            "fail": "salmon"            # Quay lui (thất bại)
        }
        
        color = colors.get(loai, "lightblue")
        
        # Vẽ trạng thái với màu phù hợp
        for index, giaTri in enumerate(trangThai):
            if giaTri != 0:
                x, y = self.get_cell_center(index)
                rect = self.canvas.create_rectangle(x - CELL_SIZE/2 + 10, y - CELL_SIZE/2 + 10,
                                                x + CELL_SIZE/2 - 10, y + CELL_SIZE/2 - 10,
                                                fill=color)
                text = self.canvas.create_text(x, y, text=str(giaTri), font=("Arial", 24))
                self.tile_items[giaTri] = (rect, text)
        
        # Cập nhật trạng thái hiện tại
        self.current_state = trangThai
        
        # Hiển thị thông tin về trạng thái backtracking
        self.txtSolution.config(state="normal")
        self.txtSolution.insert(tk.END, f"\nĐang: {loai}, Trạng thái: {trangThai}\n")
        self.txtSolution.see(tk.END)  # Cuộn xuống cuối cùng
        self.txtSolution.config(state="disabled")

    def animate_backtracking(self, index):
        if not self.animationPlay or not hasattr(self, 'backtracking_info'):
            return
            
        # Nếu không hiển thị quay lui, sử dụng đường đi đã lưu
        if not self.show_backtrack.get() and hasattr(self, 'duongDi_cuoi') and self.duongDi_cuoi:
            # Sử dụng animate_solution để hiển thị animation cho đường đi từ start đến goal
            self.animate_solution(self.duongDi_cuoi, 0)
            return
        
        # Xử lý bình thường khi hiển thị quay lui (checkbox được chọn)
        if index < len(self.backtracking_info):
            info = self.backtracking_info[index]
            self.veTrangThaiBacktracking(info['trangThai'], info['loai'])
            
            # Chụp frame nếu đang quay
            if self.recording:
                self.capture_canvas()
                
            # Tiếp tục với bước tiếp theo sau khoảng thời gian delay
            job_id = self.cuaSoChinh.after(self.animation_delay * 10, 
                                lambda: self.animate_backtracking(index + 1))
            self.animation_jobs.append(job_id)
        else:
            # Hoàn thành quá trình animation
            self.animationPlay = False
            
            # Lưu GIF sau khi animation kết thúc nếu đang quay
            if self.recording:
                self.save_gif()
                self.record_var.set(False)  # Tự động tắt quay sau khi hoàn thành
                self.recording = False

    def suaTrangThai(self):
        if self.editing or self.animationPlay:
            return

        self.editing = True
        self.new_state = []
        
        self.edit_window = tk.Toplevel(self.cuaSoChinh)
        self.edit_window.title("Chỉnh sửa trạng thái")
        
        tk.Label(self.edit_window, text="Nhấn vào các số theo thứ tự:", font=("Arial", 12))\
            .grid(row=0, column=0, columnspan=3, pady=5)
        
        self.edit_grid = []  # Danh sách chứa 9 Label
        grid_frame = tk.Frame(self.edit_window)
        grid_frame.grid(row=1, column=0, columnspan=3, pady=5)
        for i in range(3):
            row_labels = []
            for j in range(3):
                lbl = tk.Label(grid_frame, text=" ", width=4, height=2, font=("Arial", 12), borderwidth=1, relief="solid")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                row_labels.append(lbl)
            self.edit_grid.append(row_labels)
        
        # Tạo 9 nút cho số 0 đến 8
        self.edit_buttons = {}
        for num in range(9):
            btn = tk.Button(self.edit_window, text=str(num), font=("Arial", 12),
                            width=4, height=2,
                            command=lambda n=num: self.select_number(n))
            self.edit_buttons[num] = btn
            row = 2 + num // 3
            col = num % 3
            btn.grid(row=row, column=col, padx=5, pady=5)
            
        # Khi cửa sổ đóng, reset editing
        self.edit_window.protocol("WM_DELETE_WINDOW", self.close_edit_window)

    def select_number(self, number):
        # Khi nút được click, thêm số vào new_state, cập nhật bảng 3x3
        self.new_state.append(number)
        index = len(self.new_state) - 1
        row, col = index // 3, index % 3
        self.edit_grid[row][col].config(text=str(number))
        self.edit_buttons[number].config(state="disabled")
        
        if len(self.new_state) == 9:
            # Khi đủ 9 số, cập nhật trạng thái, đóng cửa sổ sửa
            self.trangThaiBatDau = tuple(self.new_state)
            self.current_state = tuple(self.new_state)
            self.veTrangThai(self.current_state)
            self.txtSolution.delete("1.0", tk.END)
            self.lblKetQua.config(text="Time: ")
            self.close_edit_window()

    def close_edit_window(self):
        if hasattr(self, "edit_window"):
            self.edit_window.destroy()
        self.editing = False


    def update_speed(self, value):
        self.animation_delay = int(value)

    def animate_solution(self, duongDi, chiSo):
        if not self.animationPlay:
            return
        
        # Nếu đang quay và cần skip frame, xử lý ở đây
        should_capture = self.recording and (chiSo % self.frame_skip_var.get() == 0)
        
        if chiSo < len(duongDi)-1:
            old_state = duongDi[chiSo]
            new_state = duongDi[chiSo+1]
            
            # Chụp trạng thái hiện tại nếu đang quay và đúng step cần chụp
            if should_capture:
                self.capture_canvas()
                
            self.animate_transition(old_state, new_state, lambda: self.animate_solution(duongDi, chiSo+1))
        else:
            self.veTrangThai(duongDi[-1])
            
            # Chụp trạng thái cuối cùng
            if self.recording:
                self.capture_canvas()
                
            self.animationPlay = False
            
            # Lưu GIF sau khi animation kết thúc nếu đang quay
            if self.recording:
                self.save_gif()
                self.record_var.set(False)  # Tự động tắt quay sau khi hoàn thành
                self.recording = False
    
    def animate_transition(self, old_state, new_state, callback):
        old_blank = old_state.index(0)
        new_blank = new_state.index(0)
        tile_moved = old_state[new_blank]
        
        start_index = new_blank
        end_index = old_blank
        
        start_x, start_y = self.get_cell_center(start_index)
        end_x, end_y = self.get_cell_center(end_index)
        
        delta_x = (end_x - start_x) / ANIMATION_STEPS
        delta_y = (end_y - start_y) / ANIMATION_STEPS
        
        if tile_moved not in self.tile_items:
            callback()
            return
        rect, text = self.tile_items[tile_moved]
        
        def step_animation(step):
            if step < ANIMATION_STEPS:
                self.canvas.move(rect, delta_x, delta_y)
                self.canvas.move(text, delta_x, delta_y)
                job_id = self.cuaSoChinh.after(self.animation_delay, lambda: step_animation(step+1))
                self.animation_jobs.append(job_id)
            else:
                # Vẽ lại với chế độ Partially Observable nếu đang bật
                self.veTrangThai(new_state, getattr(self, 'is_partially_observable_mode', False))
                job_id = self.cuaSoChinh.after(self.animation_delay, callback)
                self.animation_jobs.append(job_id)
                    
        step_animation(0)

    def toggle_recording(self):
        self.recording = self.record_var.get()
        if self.recording:
            self.record_status.config(text="Đang sẵn sàng quay (khi chạy thuật toán)")
            self.frames = []  # Reset frames khi bắt đầu
        else:
            self.record_status.config(text="Đã tắt quay GIF")
            # Nếu có frames đã ghi thì lưu
            if hasattr(self, 'frames') and self.frames:
                self.save_gif()

    def capture_canvas(self):
        # Lấy chính xác vị trí và kích thước của canvas
        canvas_width = self.canvas.winfo_width() + 150
        canvas_height = self.canvas.winfo_height() + 100
        
        # Tính toán vị trí chính xác của canvas trên màn hình
        x = self.canvas.winfo_rootx() + 55
        y = self.canvas.winfo_rooty()
        
        # Buộc cập nhật giao diện trước khi chụp
        self.cuaSoChinh.update_idletasks()
        self.cuaSoChinh.update()
        
        # Chụp ảnh vùng của canvas
        image = ImageGrab.grab(bbox=(x, y, x+canvas_width, y+canvas_height))
        self.frames.append(image)
        
        print(f"Captured frame at {x},{y} with size {canvas_width}x{canvas_height}")

    def save_gif(self):
        if not self.frames:
            return
                
        # Lấy thông tin từ label kết quả
        ket_qua_text = self.lblKetQua.cget("text")
        
        # Trích xuất tên thuật toán
        algo = ket_qua_text.split(":")[0].strip() if ":" in ket_qua_text else "unknown"
        
        # Trích xuất thời gian
        thoi_gian = "0s"
        if "Thời gian = " in ket_qua_text:
            thoi_gian = ket_qua_text.split("Thời gian = ")[1].split("s")[0].strip() + "s"
            thoi_gian = thoi_gian.replace(".", "_")  # Thay dấu chấm bằng gạch dưới
        
        # Trích xuất số bước
        so_buoc = "0"
        if "Số bước = " in ket_qua_text:
            so_buoc = ket_qua_text.split("Số bước = ")[1].strip()
        
        # Tạo tên file mới
        filename = f"{algo}_time{thoi_gian}_step{so_buoc}.gif"
        
        # Lưu frames thành GIF với tốc độ phù hợp
        #duration = max(130, self.animation_delay * 5)
        duration = max(700, self.animation_delay * 20)
        
        self.frames[0].save(
            filename,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=duration,
            loop=0  # Lặp vô hạn
        )
        
        self.record_status.config(text=f"Đã lưu GIF: {filename}")
        self.frames = []  # Reset frames

    def moGiaoDienNoObservation(self):
        self.no_obs_window = tk.Toplevel(self.cuaSoChinh)
        self.no_obs_window.title("No Observation - Belief States")
        
        window_width = 1200
        window_height = 790
        
        screen_width = self.no_obs_window.winfo_screenwidth()
        screen_height = self.no_obs_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 45
        self.no_obs_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Tạo 6 canvas cho 6 belief states
        self.belief_canvases = []
        self.belief_status_labels = []  # Khởi tạo danh sách nhãn trạng thái
        canvas_size = CELL_SIZE // 1.4  # Tăng kích thước các bảng belief
        
        # Frame chứa các canvas
        belief_frame = tk.Frame(self.no_obs_window)
        belief_frame.pack(pady=1)
        
        # Tạo grid 2x3 chứa 6 bảng belief states
        for i in range(2):
            for j in range(3):
                frame = tk.Frame(belief_frame, borderwidth=2, relief="ridge", padx=5, pady=5)
                frame.grid(row=i, column=j, padx=15, pady=15)
                
                # Nhãn cho mỗi belief state
                label_frame = tk.Frame(frame)
                label_frame.pack(fill=tk.X)
                tk.Label(label_frame, text=f"Belief State {i*3+j+1}", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
                
                # Thêm nhãn trạng thái cho mỗi belief state
                status_label = tk.Label(label_frame, text="Đang tìm", font=("Arial", 9), fg="blue")
                status_label.pack(side=tk.RIGHT)
                self.belief_status_labels.append(status_label)
                
                canvas = tk.Canvas(frame, width=canvas_size*3, height=canvas_size*3)
                canvas.pack(padx=8, pady=2)
                self.belief_canvases.append(canvas)
                
                # Vẽ lưới cho mỗi canvas
                for k in range(4):
                    canvas.create_line(0, k*canvas_size, canvas_size*3, k*canvas_size, width=2)
                    canvas.create_line(k*canvas_size, 0, k*canvas_size, canvas_size*3, width=2)
        
        # Khung hiển thị thông tin
        info_frame = tk.Frame(self.no_obs_window)
        info_frame.pack(pady=15, fill=tk.X)
        
        self.belief_info = tk.Text(info_frame, width=80, height=6, font=("Arial", 11))
        self.belief_info.pack(padx=10, pady=1)
        self.belief_info.config(state="disabled")
        
        # Nút điều khiển
        control_frame = tk.Frame(self.no_obs_window)
        control_frame.pack(pady=2)
        
        # Biến để theo dõi trạng thái tự động chạy
        self.auto_run = False
        self.auto_run_job = None
        
        # Nút bước tiếp
        tk.Button(control_frame, text="Bước tiếp", 
                font=("Arial", 12), width=15, height=1, bg="#e0fff0",
                command=self.buocTiepNoObservation).pack(side=tk.LEFT, padx=15)
        
        # Nút tự động chạy
        self.auto_button = tk.Button(control_frame, text="Tự động chạy", 
                font=("Arial", 12), width=15, height=1, bg="#fff0e0",
                command=self.toggleAutoRunNoObservation)
        self.auto_button.pack(side=tk.LEFT, padx=15)
        
        # Slider điều chỉnh tốc độ chạy tự động
        speed_frame = tk.Frame(self.no_obs_window)
        speed_frame.pack(pady=1)
        
        tk.Label(speed_frame, text="Tốc độ chạy tự động:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.auto_speed = tk.Scale(speed_frame, from_=1, to=2000, orient=tk.HORIZONTAL, 
                            length=300, resolution=1, font=("Arial", 10))
        self.auto_speed.set(800)  # Mặc định 800ms
        self.auto_speed.pack(side=tk.LEFT, padx=5)
        tk.Label(speed_frame, text="ms", font=("Arial", 11)).pack(side=tk.LEFT)
        
        # Dữ liệu để theo dõi tiến trình tìm kiếm
        self.no_obs_step = 0
        self.belief_goal_reached = [False] * 6  # Theo dõi belief states đã đạt đích
        self.belief_no_path = [False] * 6  # Theo dõi belief states không có đường đi
        
        # Thêm biến để theo dõi lịch sử trạng thái gần đây cho mỗi belief state
        self.belief_state_history = [[] for _ in range(6)]  # Lịch sử trạng thái của 6 belief states
        self.history_limit = 10  # Giữ tối đa 10 trạng thái gần nhất
        
        # Hiển thị belief states ban đầu
        self.khoiTaoBeliefStates()
        
        self.no_obs_window.transient(self.cuaSoChinh)
        self.no_obs_window.grab_set()
        self.no_obs_window.protocol("WM_DELETE_WINDOW", self.dongGiaoDienNoObservation)

    def dongGiaoDienNoObservation(self):
        if self.auto_run_job:
            self.no_obs_window.after_cancel(self.auto_run_job)
            self.auto_run_job = None
            self.auto_run = False
        
        self.no_obs_window.destroy()

    def khoiTaoBeliefStates(self):
        # Tạo một số trạng thái có thể từ trạng thái ban đầu
        self.belief_states = [self.current_state]
        
        # Tạo thêm 5 trạng thái khác biệt
        attempts = 0
        max_attempts = 50  # Giới hạn số lần thử để tránh vòng lặp vô hạn
        
        while len(self.belief_states) < 6 and attempts < max_attempts:
            state = list(self.current_state)
            # số bước di chuyển ngẫu nhiên (5-10 bước)
            for _ in range(random.randint(5, 10)):
                pos0 = state.index(0)
                row, col = pos0 // 3, pos0 % 3
                # Tính các hướng di chuyển có thể
                moves = []
                if row > 0: moves.append(-3)  # lên
                if row < 2: moves.append(3)   # xuống
                if col > 0: moves.append(-1)  # trái
                if col < 2: moves.append(1)   # phải
                
                if moves:
                    # Chọn ngẫu nhiên một hướng
                    move = random.choice(moves)
                    new_pos = pos0 + move
                    # Hoán đổi
                    state[pos0], state[new_pos] = state[new_pos], state[pos0]
            
            state_tuple = tuple(state)
            # Kiểm tra xem trạng thái mới có trùng với các trạng thái đã có chưa
            if state_tuple not in self.belief_states:
                self.belief_states.append(state_tuple)
            
            attempts += 1
        
        # Nếu sau max_attempts lần thử mà vẫn chưa đủ 6 trạng thái khác nhau
        # thì tạo thêm các trạng thái hoàn toàn ngẫu nhiên
        while len(self.belief_states) < 6:
            # Tạo một bảng hoàn toàn ngẫu nhiên
            numbers = list(range(9))
            random.shuffle(numbers)
            state_tuple = tuple(numbers)
            
            if state_tuple not in self.belief_states:
                self.belief_states.append(state_tuple)
        
        # Hiển thị các trạng thái ban đầu lên canvas
        for i, state in enumerate(self.belief_states):
            if i < len(self.belief_canvases):
                self.veBeliefState(self.belief_canvases[i], state)

    def toggleAutoRunNoObservation(self):
        self.auto_run = not self.auto_run
        if self.auto_run:
            self.auto_button.config(text="Dừng tự động", bg="#ffcccb")
            self.autoRunNoObservation()
        else:
            self.auto_button.config(text="Tự động chạy", bg="#fff0e0")
            if self.auto_run_job:
                self.no_obs_window.after_cancel(self.auto_run_job)
                self.auto_run_job = None

    def autoRunNoObservation(self):
        if not self.auto_run:
            return
        
        # Nếu ít nhất một belief state đạt đích, dừng lại
        any_reached_goal = any(self.belief_goal_reached)
        
        if any_reached_goal:
            # Dừng tự động chạy có belief state đạt đích
            self.auto_run = False
            self.auto_button.config(text="Tự động chạy", bg="#fff0e0")
            return
        
        # Thực hiện bước tiếp theo
        self.buocTiepNoObservation()
        
        # Lên lịch thực hiện bước tiếp theo
        delay = self.auto_speed.get()
        self.auto_run_job = self.no_obs_window.after(delay, self.autoRunNoObservation)

    def veBeliefState(self, canvas, state):
        canvas.delete("all")
        # Vẽ lưới
        canvas_size = CELL_SIZE // 1.4  # Phải khớp với kích thước đã thiết lập ở trên
        for i in range(4):
            canvas.create_line(0, i*canvas_size, canvas_size*3, i*canvas_size, width=2)
            canvas.create_line(i*canvas_size, 0, i*canvas_size, canvas_size*3, width=2)
        
        # Vẽ các ô
        for index, value in enumerate(state):
            if value != 0:
                row, col = index // 3, index % 3
                x = col * canvas_size + canvas_size/2
                y = row * canvas_size + canvas_size/2
                canvas.create_rectangle(
                    x - canvas_size/2 + 5, 
                    y - canvas_size/2 + 5,
                    x + canvas_size/2 - 5, 
                    y + canvas_size/2 - 5,
                    fill="lightblue"
                )
                canvas.create_text(x, y, text=str(value), font=("Arial", 14))

    def coTheGiaiDuoc(self, state):
        """
        Kiểm tra nhanh xem một trạng thái có thể giải được không.
        Sử dụng thuật toán tính tổng nghịch thế (inversion count) cho puzzle.
        Hai trạng thái có thể đạt được từ nhau nếu chúng có cùng chẵn/lẻ tổng nghịch thế.
        """
        def tinhNghichThe(state):
            inversion = 0
            state_list = [x for x in state if x != 0]  # Loại bỏ ô trống
            for i in range(len(state_list)):
                for j in range(i + 1, len(state_list)):
                    if state_list[i] > state_list[j]:
                        inversion += 1
            return inversion
        
        # Tính nghịch thế của trạng thái ban đầu và đích
        inversion_state = tinhNghichThe(state)
        inversion_goal = tinhNghichThe(self.trangThaiDich)
        
        # Nếu có cùng tính chẵn lẻ của nghịch thế, có thể giải được
        return inversion_state % 2 == inversion_goal % 2

    def chayThuatToanNoObservation(self):
        # Reset lại tất cả biến theo dõi
        self.belief_goal_reached = [False] * 6
        self.belief_no_path = [False] * 6
        
        # Reset status labels
        for label in self.belief_status_labels:
            label.config(text="Đang tìm", fg="blue")
        
        # Kiểm tra các belief states
        for i, state in enumerate(self.belief_states):
            # Kiểm tra nếu đã ở trạng thái đích
            if state == self.trangThaiDich:
                self.belief_goal_reached[i] = True
                self.belief_status_labels[i].config(text="Đã đạt đích", fg="green")
            # Kiểm tra nếu không thể giải được
            elif not self.coTheGiaiDuoc(state):
                self.belief_no_path[i] = True
                self.belief_status_labels[i].config(text="Không thể giải", fg="red")
        
        # Cập nhật hiển thị cho tất cả belief states
        for i, state in enumerate(self.belief_states):
            self.veBeliefState(self.belief_canvases[i], state)
            
            # Vẽ khung xanh cho các belief states đã đạt đích
            if self.belief_goal_reached[i]:
                canvas_size = CELL_SIZE // 1.4
                self.belief_canvases[i].create_rectangle(
                    2, 2, canvas_size*3-2, canvas_size*3-2, 
                    outline="green", width=3
                )
            # Vẽ khung đỏ cho các belief states không thể giải
            elif self.belief_no_path[i]:
                canvas_size = CELL_SIZE // 1.4
                self.belief_canvases[i].create_rectangle(
                    2, 2, canvas_size*3-2, canvas_size*3-2, 
                    outline="red", width=3
                )
        
        # Cập nhật thông tin
        self.belief_info.config(state="normal")
        self.belief_info.delete("1.0", tk.END)
        self.belief_info.config(state="disabled")
        
        # Reset bước hiện tại
        self.no_obs_step = 0

    def manhattan_distance(self, state1, state2):
        distance = 0
        for i in range(1, 9):  # Chỉ tính cho các ô từ 1-8 (không tính ô trống 0)
            # Tìm vị trí của ô i trong hai trạng thái
            pos1 = state1.index(i)
            pos2 = state2.index(i)
            
            # Tính hàng và cột
            row1, col1 = pos1 // 3, pos1 % 3
            row2, col2 = pos2 // 3, pos2 % 3
            
            # Cộng dồn khoảng cách Manhattan
            distance += abs(row1 - row2) + abs(col1 - col2)
        
        return distance

    def buocTiepNoObservation(self):
        """Thực hiện bước tiếp theo trong tìm kiếm No Observation
        
        Trong môi trường không quan sát được (No Observation):
        - Ta duy trì một tập hợp các trạng thái có thể (belief states)
        - Mỗi khi thực hiện hành động, ta áp dụng nó cho tất cả các belief states
        - Ta không thể quan sát kết quả nên không biết chính xác đang ở trạng thái nào
        """
        if not hasattr(self, 'belief_states') or not self.belief_states:
            return
        
        # Tăng bước hiện tại
        self.no_obs_step += 1
        
        # Lựa chọn hành động tốt nhất dựa trên heuristic
        possible_actions = ["lên", "xuống", "trái", "phải"]
        
        # Phương thức chọn hành động thông minh hơn
        def evaluate_action(action):
            # Mô phỏng kết quả của hành động cho mỗi belief state đang hoạt động
            total_distance = 0
            active_states = 0
            
            for i, state in enumerate(self.belief_states):
                # Bỏ qua các belief states đã hoàn thành
                if self.belief_goal_reached[i] or self.belief_no_path[i]:
                    continue
                    
                active_states += 1
                
                # Áp dụng hành động để xem kết quả
                pos0 = state.index(0)
                row, col = pos0 // 3, pos0 % 3
                new_state = list(state)
                valid_move = False
                
                if action == "lên" and row > 0:
                    swap_pos = pos0 - 3
                    new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                    valid_move = True
                elif action == "xuống" and row < 2:
                    swap_pos = pos0 + 3
                    new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                    valid_move = True
                elif action == "trái" and col > 0:
                    swap_pos = pos0 - 1
                    new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                    valid_move = True
                elif action == "phải" and col < 2:
                    swap_pos = pos0 + 1
                    new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                    valid_move = True
                
                # Nếu di chuyển hợp lệ, đánh giá khoảng cách đến đích
                if valid_move:
                    new_state_tuple = tuple(new_state)
                    
                    # Kiểm tra xem trạng thái mới có trong lịch sử gần đây không
                    # Nếu có, phạt nặng để tránh lặp lại
                    if new_state_tuple in self.belief_state_history[i]:
                        # Phạt nặng hơn nếu trạng thái đã xuất hiện gần đây
                        history_index = len(self.belief_state_history[i]) - 1 - self.belief_state_history[i][::-1].index(new_state_tuple)
                        recency_penalty = 200 * (1 - history_index / len(self.belief_state_history[i]))
                        total_distance += 100 + recency_penalty  # Phạt cơ bản + phạt dựa vào độ gần
                    else:
                        distance = self.manhattan_distance(new_state_tuple, self.trangThaiDich)
                        total_distance += distance
                else:
                    # Phạt hành động không hợp lệ
                    total_distance += 100  # Giá trị lớn để tránh chọn hành động này
            
            # Nếu không có belief states đang hoạt động, trả về giá trị lớn
            if active_states == 0:
                return float('inf')
            
            # Trả về khoảng cách trung bình
            return total_distance / active_states
        
        # Đánh giá mỗi hành động và chọn hành động tốt nhất
        action_scores = [(action, evaluate_action(action)) for action in possible_actions]
        
        # Sắp xếp theo điểm số tăng dần (điểm thấp = tốt hơn)
        action_scores.sort(key=lambda x: x[1])
        
        # Tăng xác suất exploration theo số bước đã thực hiện
        # Nếu đã thực hiện nhiều bước mà chưa tìm ra đích, tăng xác suất chọn ngẫu nhiên
        exploration_prob = min(0.2 + (self.no_obs_step / 50) * 0.3, 0.5)  # Tối đa 50%
        
        # Chọn hành động tốt nhất với xác suất cao, nhưng đôi khi chọn ngẫu nhiên
        # để tránh bị mắc kẹt (exploration vs exploitation)
        if random.random() < (1 - exploration_prob):  # (1-exploration_prob)% chọn hành động tốt nhất
            selected_action = action_scores[0][0]
        else:  # exploration_prob% chọn ngẫu nhiên
            # Chọn ngẫu nhiên từ các hành động, loại trừ hành động tệ nhất nếu có ít nhất 2 lựa chọn
            if len(action_scores) > 1:
                # Loại bỏ hành động tệ nhất
                selected_action = random.choice([a[0] for a in action_scores[:-1]])
            else:
                selected_action = action_scores[0][0]
        
        # Cập nhật thông tin
        self.belief_info.config(state="normal")
        self.belief_info.delete("1.0", tk.END)
        self.belief_info.insert(tk.END, f"Bước {self.no_obs_step}: Hành động \"{selected_action}\" (Exploration: {exploration_prob:.2f})\n")
        
        # Hiển thị đánh giá của các hành động
        self.belief_info.insert(tk.END, "Đánh giá hành động (giá trị thấp hơn = tốt hơn):\n")
        for action, score in action_scores:
            self.belief_info.insert(tk.END, f"- {action}: {score:.2f}\n")
        
        # Áp dụng hành động cho tất cả các belief states
        new_belief_states = []  # Danh sách belief states mới
        
        # Lưu trữ số lượng belief states đã đạt đích
        reached_goal = 0
        
        for i, state in enumerate(self.belief_states):
            # Lưu trạng thái hiện tại vào lịch sử
            if not self.belief_goal_reached[i] and not self.belief_no_path[i]:
                # Thêm vào lịch sử
                self.belief_state_history[i].append(state)
                # Giữ kích thước lịch sử giới hạn
                if len(self.belief_state_history[i]) > self.history_limit:
                    self.belief_state_history[i].pop(0)
            
            # Nếu belief state này đã đạt đích, giữ nguyên
            if self.belief_goal_reached[i]:
                new_belief_states.append(self.trangThaiDich)
                reached_goal += 1
                continue
            
            # Nếu belief state này không có đường đi, giữ nguyên
            if self.belief_no_path[i]:
                new_belief_states.append(state)
                continue
            
            # Áp dụng hành động đã chọn
            pos0 = state.index(0)  # Vị trí ô trống
            row, col = pos0 // 3, pos0 % 3
            new_state = list(state)
            valid_move = False
            
            if selected_action == "lên" and row > 0:
                # Di chuyển ô trống lên
                swap_pos = pos0 - 3
                new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                valid_move = True
            elif selected_action == "xuống" and row < 2:
                # Di chuyển ô trống xuống
                swap_pos = pos0 + 3
                new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                valid_move = True
            elif selected_action == "trái" and col > 0:
                # Di chuyển ô trống sang trái
                swap_pos = pos0 - 1
                new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                valid_move = True
            elif selected_action == "phải" and col < 2:
                # Di chuyển ô trống sang phải
                swap_pos = pos0 + 1
                new_state[pos0], new_state[swap_pos] = new_state[swap_pos], new_state[pos0]
                valid_move = True
            
            new_state_tuple = tuple(new_state)
            
            # Nếu di chuyển hợp lệ, cập nhật belief state
            if valid_move:
                new_belief_states.append(new_state_tuple)
                
                # Kiểm tra nếu đã đạt đích
                if new_state_tuple == self.trangThaiDich:
                    self.belief_goal_reached[i] = True
                    self.belief_status_labels[i].config(text="Đã đạt đích", fg="green")
                    reached_goal += 1
            else:
                # Nếu không thể di chuyển, giữ nguyên trạng thái
                new_belief_states.append(state)
        
        # Cập nhật belief states
        for i, new_state in enumerate(new_belief_states):
            if i < len(self.belief_canvases):
                self.veBeliefState(self.belief_canvases[i], new_state)
                
                # Vẽ khung xanh cho các belief states đã đạt đích
                if self.belief_goal_reached[i]:
                    canvas_size = CELL_SIZE // 1.4
                    self.belief_canvases[i].create_rectangle(
                        2, 2, canvas_size*3-2, canvas_size*3-2, 
                        outline="green", width=3
                    )
                
                # Vẽ khung đỏ cho các belief states không có đường đi
                if self.belief_no_path[i]:
                    canvas_size = CELL_SIZE // 1.4
                    self.belief_canvases[i].create_rectangle(
                        2, 2, canvas_size*3-2, canvas_size*3-2, 
                        outline="red", width=3
                    )
        
        # Cập nhật trạng thái belief
        self.belief_states = new_belief_states
        
        self.belief_info.config(state="disabled")

    def dungGiaiThuatToan(self):
        if self.animationPlay:
            self.animationPlay = False
            
            # Hủy tất cả các animation jobs đã lên lịch
            for job_id in self.animation_jobs:
                try:
                    self.cuaSoChinh.after_cancel(job_id)
                except:
                    pass  # Bỏ qua nếu job không tồn tại
            
            # Đặt lại danh sách job
            self.animation_jobs = []
            
            # Trở về trạng thái ban đầu
            self.veTrangThai(self.trangThaiBatDau)
            
            # Cập nhật thông báo
            self.lblKetQua.config(text="Đã dừng giải thuật toán")
            
            # Đặt lại tất cả các biến về trạng thái ban đầu
            if hasattr(self, 'is_partially_observable_mode'):
                self.is_partially_observable_mode = False
            
            # Nếu đang quay gif, dừng lại
            if self.recording:
                self.save_gif()
                self.record_var.set(False)
                self.recording = False
                self.record_status.config(text="Quay gif đã dừng")

    def moSoSanhThuatToan(self):
        # Đọc thông tin từ tên file GIF trong thư mục
        algo_stats = self.docThongTinTuGIF()
        
        if not algo_stats:
            messagebox.showinfo("Thông báo", "Không tìm thấy file GIF để phân tích. Vui lòng chạy các thuật toán và quay GIF trước.")
            return
        
        so_sanh_window = tk.Toplevel(self.cuaSoChinh)
        so_sanh_window.title("So sánh thuật toán")
        so_sanh_window.resizable(False, False)
        center_window(so_sanh_window, 1200, 700)
        
        frame = tk.Frame(so_sanh_window)
        frame.pack(fill=tk.BOTH, expand=True)
        
        algorithm_order = [
            "BFS", "DFS", "IDFS", "UCS", "AStar", "IDAStar", "Greedy",
            "Simple HC", "Steepest HC", "Stochastic HC", "Simulated Annealing",
            "Beam Search", "Genetic Algorithm", "Non Deterministic", 
            "No Observation", "Partially Observable", "Backtracking", 
            "Backtracking with FC", "Min Conflicts", "Q-learning"
        ]
        
        # Lọc và sắp xếp theo thứ tự đã định nghĩa
        sorted_algos = []
        for algo in algorithm_order:
            if algo in algo_stats:
                sorted_algos.append(algo)
        
        # Thêm các thuật toán khác nếu không nằm trong danh sách đã định nghĩa
        remaining_algos = [algo for algo in algo_stats.keys() if algo not in sorted_algos]
        sorted_algos.extend(remaining_algos)
        
        fig = plt.figure(figsize=(12, 10))
        
        # Biểu đồ thời gian
        ax1 = fig.add_subplot(211)
        times = [algo_stats[algo]['time'] for algo in sorted_algos]
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(sorted_algos)))
        bar_width = 0.6
        x_positions = np.arange(len(sorted_algos))
        
        bars1 = ax1.bar(x_positions, times, color=colors, width=bar_width)
        ax1.set_ylabel('Thời gian (giây)', fontsize=10)
        ax1.set_title('So sánh thời gian thực thi các thuật toán', fontsize=12)
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels(sorted_algos, rotation=15, ha='right', fontsize=8)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Thêm giá trị lên đầu cột
        for bar in bars1:
            height = bar.get_height()
            ax1.annotate(f'{height:.4f}s',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 điểm dọc
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7)
        
        # Biểu đồ số bước
        ax2 = fig.add_subplot(212)
        steps = [algo_stats[algo]['steps'] for algo in sorted_algos]
        
        bars2 = ax2.bar(x_positions, steps, color=colors, width=bar_width)
        ax2.set_ylabel('Số bước', fontsize=10)
        ax2.set_title('So sánh số bước thực hiện của các thuật toán', fontsize=12)
        ax2.set_xticks(x_positions)
        ax2.set_xticklabels(sorted_algos, rotation=15, ha='right', fontsize=8)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Thêm giá trị lên đầu cột
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 điểm dọc
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7)
        
        # Thêm khoảng cách tốt hơn
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15, hspace=0.3)
        
        # Tạo canvas để hiển thị biểu đồ trong Tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Hàm đóng cửa sổ và giải phóng tài nguyên matplotlib
        def close_window():
            plt.close(fig)  # Đóng figure để giải phóng bộ nhớ
            so_sanh_window.destroy()
        
        # Đặt protocol khi đóng cửa sổ bằng nút X
        so_sanh_window.protocol("WM_DELETE_WINDOW", close_window)
        
    def docThongTinTuGIF(self):
        algo_stats = {}
        
        # Ví dụ: BFS_time12_34s_step15.gif
        pattern = r'(.+)_time(.+)s_step(\d+)'
        
        try:
            # Lấy danh sách file trong thư mục hiện tại
            files = [f for f in os.listdir() if f.endswith('.gif')]
            
            for file in files:
                match = re.search(pattern, file)
                if match:
                    algo_name = match.group(1).strip()
                    time_str = match.group(2).replace('_', '.')
                    steps = int(match.group(3))
                    
                    try:
                        time_val = float(time_str)
                        algo_stats[algo_name] = {
                            'time': time_val,
                            'steps': steps
                        }
                    except ValueError:
                        continue
            
            return algo_stats
            
        except Exception as e:
            print(f"Lỗi khi đọc file GIF: {e}")
            return {}

    def hienThiDoThiDuongDi(self):
        # Kiểm tra xem có đường đi nào không
        if not hasattr(self, 'txtSolution') or not self.txtSolution.get("1.0", tk.END).strip():
            messagebox.showinfo("Thông báo", "Chưa có đường đi nào để hiển thị. Vui lòng chạy một thuật toán trước.")
            return
            
        # Lấy nội dung từ text box hiển thị đường đi
        solution_text = self.txtSolution.get("1.0", tk.END)
        
        # Parse đường đi từ text
        duongDi = []
        for line in solution_text.strip().split('\n'):
            if line.startswith("Bước "):
                # Trích xuất trạng thái từ dòng "Bước X: (state)"
                try:
                    # Dạng: "Bước X: (1, 2, 3, 4, 5, 6, 7, 8, 0)"
                    state_str = line.split(":", 1)[1].strip()
                    state = eval(state_str)  # Chuyển string thành tuple
                    duongDi.append(state)
                except:
                    continue
        
        if not duongDi:
            messagebox.showinfo("Thông báo", "Không thể phân tích đường đi. Định dạng không hợp lệ.")
            return
        
        # Kiểm tra số lượng node để quyết định kiểu hiển thị
        num_nodes = len(duongDi)
        
        node_window = tk.Toplevel(self.cuaSoChinh)
        node_window.title("Đồ thị đường đi")
        node_window.resizable(False, False)
        center_window(node_window, 1000, 800)
        
        G = nx.DiGraph()
        
        # Thêm các node và cạnh
        for i in range(num_nodes-1):
            G.add_edge(str(i), str(i+1))
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        
        # Tạo vị trí cho layout tuyến tính theo chiều ngang
        if num_nodes <= 10:
            # Nếu số node ít hơn hoặc bằng 20, hiển thị tất cả trên một hàng
            pos = {}
            for i in range(num_nodes):
                pos[str(i)] = (i * 3, 0)  # Tăng từ 2 lên 3 để tăng khoảng cách
        else:
            # Nếu nhiều node, chia thành nhiều hàng
            pos = {}
            nodes_per_row = 10  # Thay đổi từ 5 thành 20 node trên một dòng
            for i in range(num_nodes):
                row = i // nodes_per_row
                col = i % nodes_per_row
                pos[str(i)] = (col * 3, -row * 3)  # Tăng từ 2 lên 3 để tăng khoảng cách
        
        # Vẽ đồ thị với vị trí đã định
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=600,  # Giảm từ 1200 xuống 900
                edge_color='black', linewidths=1, font_size=10, ax=ax, 
                arrows=True, arrowstyle='-|>', arrowsize=15)
                
        ax.set_title(f"Đồ thị đường đi ({num_nodes-1} bước)")
        
        # Hiển thị trạng thái ở mỗi node
        state_labels = {}
        for i, state in enumerate(duongDi):
            formatted_state = self.format_state_for_display(state)
            state_labels[str(i)] = formatted_state
        
        # Tạo vị trí cho các nhãn trạng thái (dưới node)
        pos_attrs = {}
        for node, coords in pos.items():
            pos_attrs[node] = (coords[0], coords[1] - 0.3)  # Giảm từ 0.5 xuống 0.4 để phù hợp với node nhỏ hơn
            
        # Vẽ nhãn trạng thái
        nx.draw_networkx_labels(G, pos_attrs, labels=state_labels, font_size=7,  # Giảm font size từ 8 xuống 7
                              horizontalalignment='center', verticalalignment='top')
        
        plt.axis('off')  
        ax.margins(0.2)
        ax.autoscale()
        
        # Tạo canvas để hiển thị trong Tkinter
        canvas = FigureCanvasTkAgg(fig, node_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Hàm đóng cửa sổ và giải phóng tài nguyên matplotlib
        def close_node_window():
            plt.close(fig)  # Đóng figure để giải phóng bộ nhớ
            node_window.destroy()
            
        node_window.protocol("WM_DELETE_WINDOW", close_node_window)
        

    def format_state_for_display(self, state):
        if not state or len(state) != 9:
            return "Invalid"
            
        # Tạo biểu diễn dạng ma trận 3x3
        rows = []
        for i in range(0, 9, 3):
            row = ' '.join(str(x) if x != 0 else '_' for x in state[i:i+3])
            rows.append(row)
        
        return '\n'.join(rows)

if __name__ == "__main__":
    root = tk.Tk()
    center_window(root, 800, 790)
    root.title("Các thuật toán giải 8-Puzzle")
    
    def on_closing():
        plt.close('all')
        
        # Hủy tất cả các tác vụ animation nếu có
        if hasattr(app, 'animation_jobs'):
            for job_id in app.animation_jobs:
                try:
                    root.after_cancel(job_id)
                except:
                    pass
                    
        # Đóng cửa sổ gốc và thoát chương trình
        root.destroy()
        root.quit()  # Đảm bảo thoát khỏi mainloop
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    app = GiaoDien8Puzzle(root)
    root.mainloop()
