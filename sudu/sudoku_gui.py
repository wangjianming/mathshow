import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("数独求解器")
        self.master.geometry("550x650")
        
        # 数字颜色定义
        self.number_colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "orange",
            6: "brown",
            7: "pink",
            8: "gray",
            9: "cyan"
        }
        
        # 初始化保存的题目列表
        self.saved_puzzles = []
        self.load_saved_puzzles()
        
        # 创建标题
        title_label = tk.Label(self.master, text="数独求解器", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # 创建说明文本
        instruction_label = tk.Label(self.master, text="请输入初始数字（1-9），空格子留空或填0", font=("Arial", 10))
        instruction_label.pack()
        
        # 创建框架用于放置数独网格
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(pady=20)
        
        # 创建9x9网格输入框
        self.entries = []
        self.create_grid()
        
        # 创建按钮框架
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)
        
        # 创建求解按钮
        solve_button = tk.Button(button_frame, text="求解", command=self.solve_sudoku, width=8, bg="#4CAF50", fg="white")
        solve_button.pack(side=tk.LEFT, padx=5)
        
        # 创建清除按钮
        clear_button = tk.Button(button_frame, text="清除", command=self.clear_grid, width=8, bg="#f44336", fg="white")
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # 创建示例按钮
        example_button = tk.Button(button_frame, text="示例", command=self.load_example, width=8, bg="#2196F3", fg="white")
        example_button.pack(side=tk.LEFT, padx=5)
        
        # 创建记忆功能按钮框架
        memory_frame = tk.Frame(self.master)
        memory_frame.pack(pady=10)
        
        # 创建保存按钮
        save_button = tk.Button(memory_frame, text="保存题目", command=self.save_puzzle, width=8, bg="#FF9800", fg="white")
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 创建加载按钮
        load_button = tk.Button(memory_frame, text="加载题目", command=self.load_puzzle, width=8, bg="#9C27B0", fg="white")
        load_button.pack(side=tk.LEFT, padx=5)
        
        # 创建删除按钮
        delete_button = tk.Button(memory_frame, text="删除题目", command=self.delete_puzzle, width=8, bg="#607D8B", fg="white")
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # 显示已保存题目数量
        self.update_saved_count_label()
        
    def create_grid(self):
        # 创建9x9网格输入框
        self.entries = []
        for i in range(9):
            row_entries = []
            for j in range(9):
                # 创建每个单元格的输入框
                entry = tk.Entry(
                    self.grid_frame,
                    width=3,
                    font=("Arial", 14, "bold"),
                    justify="center",
                    bd=1,
                    relief="solid"
                )
                
                # 绑定按键事件以实现实时颜色变化
                entry.bind("<KeyRelease>", lambda e, ent=entry: self.on_key_release(ent))
                
                # 设置间距以区分3x3子网格
                padx = (0, 5) if (j + 1) % 3 == 0 and j != 8 else (0, 1)
                pady = (0, 5) if (i + 1) % 3 == 0 and i != 8 else (0, 1)
                
                entry.grid(row=i, column=j, padx=padx, pady=pady, ipady=5)
                row_entries.append(entry)
            
            self.entries.append(row_entries)
    
    def on_key_release(self, entry):
        """处理按键释放事件，实现实时数字颜色变化"""
        # 获取输入的值
        value = entry.get()
        
        # 清除颜色设置
        entry.config(fg="black")
        
        # 如果是数字1-9，设置对应颜色
        if value.isdigit() and 1 <= int(value) <= 9:
            fg_color = self.number_colors.get(int(value), "black")
            entry.config(fg=fg_color)
    
    def get_grid_values(self):
        """获取网格中的所有值"""
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                else:
                    row.append(0)
            grid.append(row)
        return grid
    
    def set_grid_values(self, grid):
        """设置网格中的所有值"""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(grid[i][j]))
                    # 设置数字颜色
                    fg_color = self.number_colors.get(grid[i][j], "black")
                    self.entries[i][j].config(fg=fg_color)
    
    def clear_grid(self):
        """清空整个网格"""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
    
    def load_example(self):
        """加载示例数独"""
        # 一个经典的数独题目
        example_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        
        self.set_grid_values(example_grid)
    
    def save_puzzle(self):
        """保存当前数独题目"""
        # 获取当前网格值
        grid = self.get_grid_values()
        
        # 检查是否有输入数字
        has_numbers = any(any(cell != 0 for cell in row) for row in grid)
        if not has_numbers:
            messagebox.showwarning("警告", "网格为空，请先输入数字再保存！")
            return
        
        # 检查是否达到保存上限
        if len(self.saved_puzzles) >= 10:
            messagebox.showwarning("警告", "已达到保存上限（10组）！请删除一些题目后再保存。")
            return
        
        # 获取题目名称
        puzzle_name = simpledialog.askstring("保存题目", "请输入题目名称：")
        if not puzzle_name:
            return
        
        # 检查名称是否已存在
        if any(puzzle["name"] == puzzle_name for puzzle in self.saved_puzzles):
            messagebox.showerror("错误", "题目名称已存在，请使用其他名称！")
            return
        
        # 保存题目
        self.saved_puzzles.append({
            "name": puzzle_name,
            "grid": grid
        })
        
        # 保存到文件
        self.save_puzzles_to_file()
        
        # 更新显示
        self.update_saved_count_label()
        
        messagebox.showinfo("成功", f"题目 '{puzzle_name}' 已保存！")
    
    def load_puzzle(self):
        """加载已保存的数独题目"""
        if not self.saved_puzzles:
            messagebox.showinfo("提示", "没有已保存的题目！")
            return
        
        # 创建选择对话框
        puzzle_names = [puzzle["name"] for puzzle in self.saved_puzzles]
        puzzle_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(puzzle_names)])
        selected_index = simpledialog.askinteger(
            "加载题目", 
            f"请选择要加载的题目（1-{len(puzzle_names)}）：\n\n{puzzle_list}",
            minvalue=1, 
            maxvalue=len(puzzle_names)
        )
        
        if selected_index is None:
            return
        
        # 加载选中的题目
        selected_puzzle = self.saved_puzzles[selected_index - 1]
        self.set_grid_values(selected_puzzle["grid"])
        messagebox.showinfo("成功", f"题目 '{selected_puzzle['name']}' 已加载！")
    
    def delete_puzzle(self):
        """删除已保存的数独题目"""
        if not self.saved_puzzles:
            messagebox.showinfo("提示", "没有已保存的题目！")
            return
        
        # 创建选择对话框
        puzzle_names = [puzzle["name"] for puzzle in self.saved_puzzles]
        puzzle_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(puzzle_names)])
        selected_index = simpledialog.askinteger(
            "删除题目", 
            f"请选择要删除的题目（1-{len(puzzle_names)}）：\n\n{puzzle_list}",
            minvalue=1, 
            maxvalue=len(puzzle_names)
        )
        
        if selected_index is None:
            return
        
        # 删除选中的题目
        deleted_puzzle = self.saved_puzzles.pop(selected_index - 1)
        
        # 保存到文件
        self.save_puzzles_to_file()
        
        # 更新显示
        self.update_saved_count_label()
        
        messagebox.showinfo("成功", f"题目 '{deleted_puzzle['name']}' 已删除！")
    
    def load_saved_puzzles(self):
        """从文件加载已保存的题目"""
        try:
            if os.path.exists("sudoku_puzzles.json"):
                with open("sudoku_puzzles.json", "r", encoding="utf-8") as f:
                    self.saved_puzzles = json.load(f)
        except Exception as e:
            print(f"加载保存的题目时出错: {e}")
            self.saved_puzzles = []
    
    def save_puzzles_to_file(self):
        """将题目保存到文件"""
        try:
            with open("sudoku_puzzles.json", "w", encoding="utf-8") as f:
                json.dump(self.saved_puzzles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("错误", f"保存题目时出错: {e}")
    
    def update_saved_count_label(self):
        """更新已保存题目数量显示"""
        # 如果已存在标签则更新，否则创建新标签
        if hasattr(self, 'saved_count_label'):
            self.saved_count_label.config(text=f"已保存题目: {len(self.saved_puzzles)}/10")
        else:
            self.saved_count_label = tk.Label(self.master, text=f"已保存题目: {len(self.saved_puzzles)}/10", font=("Arial", 10))
            self.saved_count_label.pack(pady=5)
    
    def solve_sudoku(self):
        """求解数独"""
        # 获取当前网格值
        grid = self.get_grid_values()
        
        # 检查初始状态是否有效
        if not self.is_valid_initial_grid(grid):
            messagebox.showerror("错误", "初始输入无效，请检查输入的数字是否符合数独规则！")
            return
        
        # 尝试求解
        if self.solve(grid):
            # 显示解决方案
            self.set_grid_values(grid)
            messagebox.showinfo("成功", "数独已解决！")
        else:
            messagebox.showerror("无解", "此数独无解或初始输入有误！")
    
    def is_valid_initial_grid(self, grid):
        """检查初始网格是否有效"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    num = grid[i][j]
                    grid[i][j] = 0  # 临时设为0以检查有效性
                    if not self.is_safe(grid, i, j, num):
                        grid[i][j] = num  # 恢复原值
                        return False
                    grid[i][j] = num  # 恢复原值
        return True
    
    def is_safe(self, grid, row, col, num):
        """检查在给定位置放置数字是否安全"""
        # 检查行
        for x in range(9):
            if grid[row][x] == num:
                return False
        
        # 检查列
        for x in range(9):
            if grid[x][col] == num:
                return False
        
        # 检查3x3子网格
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def find_empty_location(self, grid):
        """找到第一个空位置"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None
    
    def solve(self, grid):
        """使用回溯法求解数独"""
        empty_pos = self.find_empty_location(grid)
        
        # 如果没有空位置，则数独已解决
        if not empty_pos:
            return True
        
        row, col = empty_pos
        
        # 尝试数字1到9
        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                
                # 递归求解
                if self.solve(grid):
                    return True
                
                # 回溯
                grid[row][col] = 0
        
        return False

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()