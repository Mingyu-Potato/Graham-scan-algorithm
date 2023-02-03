import tkinter as tk

from matplotlib.pyplot import grid

class Graham():
    def __init__(self, grid_size):
        self.root = tk.Tk()
        self.root.title("Graham Scan 알고리즘")
        self.points = []
        self.popped_points = []

        # # 모니터 화면 크기에 따른 가운데 정렬이 필요한 경우
        # self.window_x, self.window_y = int(grid_size[0])*40, int(grid_size[1])*40
        # print(self.window_x)
        # print(self.window_y)
        # self.screen_width = self.root.winfo_screenwidth()
        # self.screen_height = self.root.winfo_screenheight()

        # self.x_position = int((self.screen_width/2) - (self.window_x/2))
        # self.y_position = int((self.screen_height/2) - (self.window_y/2))

        # self.root.geometry(f"{self.window_x}x{self.window_y}+{self.x_position}+{self.y_position}")

        # 상단 프레임(Graham Scan 시작 버튼)
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(side="top")

        graham_start = tk.Button(self.frame_top, text="Graham Scan 시작", command=self.outerTrees)
        graham_start.pack(side="left")

        reset_btn = tk.Button(self.frame_top, text="Reset", command=self._init)
        reset_btn.pack(side="left")

        # 하단 프레임(Grid 버튼)
        self.frame_bot = tk.Frame(self.root)
        self.frame_bot.pack(side="top")

        for i in range(int(grid_size[1])):
            for j in range(int(grid_size[0])):
                globals()[f'btn_{j}_{i}'] = tk.Button(self.frame_bot, height=1, width=1,
                                                     bg='white', highlightbackground='black', highlightthickness=0.01, borderwidth=0.01,
                                                     activebackground='black', command=lambda x=f'btn_{j}_{i}': self.select_points(x))
                globals()[f'btn_{j}_{i}'].grid(row=j, column=i)


    def select_points(self, btn):
        globals()[btn].config(bg='black')

        pts = (int(btn.split('_')[1]), int(btn.split('_')[2]))
        self.points.append(pts)


    def outerTrees(self):
        # 가장 작은 좌표의 노드를 시작점으로 설정(외각 노드들을 찾으면 결국 가장 작은 좌표와 큰 좌표는 선택되기 때문)
        start = min(self.points, key=lambda p: (p[0], p[1]))
        self.popped_points.append(start)
        self.points.pop(self.points.index(start))

        # ccw 원에서 시작 노드를 기준으로 순회하기 위해 노드를 정렬
        self.points.sort(key=lambda p: (self.slope(p, start), -p[1], p[0]))

        # Add each point to the convex hull.
        # If the last 3 points make a cw turn, the second to last point is wrong. 
        ans = [start]
        for p in self.points:
            ans.append(p)
            while len(ans) > 2 and self.cross(ans[-3], ans[-2], ans[-1]) < 0:
                self.popped_points.append(ans[-2])
                ans.pop(-2)

        # graham scan 결과인 버튼은 배경을 빨간색으로 설정
        print('result :', ans)
        for p in ans:
            globals()[f'btn_{p[0]}_{p[1]}'].config(bg='red')

        # 바뀐 graham scan 결과에 포함되어 있지 않은 버튼은 배경을 검정색으로 설정
        for p in self.points:
            if not p in ans:
                globals()[f'btn_{p[0]}_{p[1]}'].config(bg='black')

        for p in self.popped_points:
            self.points.append(p)
        self.points = list(set(self.points)) # 중복 제거
        self.popped_points = []

    # 벡터와 p2p3 벡터의 외적 계산
    # ccw(counter clock wise)가 0이면 일직선상, < 0이면 우회전, > 0이면 좌회전
    def cross(self, p1, p2, p3):
        return (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0])

    # p1과 p2 간 직선의 경사 계산
    def slope(self, p1, p2):
        return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0]) if p1[0] != p2[0] else float('inf')

    # Reset 버튼을 누르면 선택된 버튼을 모두 초기화
    def _init(self):
        for p in self.points:
            globals()[f'btn_{p[0]}_{p[1]}'].config(bg='white')
        self.points = []

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    nrows = input("행 수를 입력하세요 : ")
    ncols = input("열 수를 입력하세요 : ")
    grid_size = (nrows, ncols)

    app = Graham(grid_size)
    app.mainloop()