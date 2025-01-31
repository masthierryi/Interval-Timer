# Interval Timer by masTHIERRYi - 2025
import tkinter as tk
import customtkinter as ctk

# Configuração dos modos (tempos e cores) -------------------------------------------
SETUPS = {
    "MAIN": {"PREPARE": 60, "WORK": 60*25, "REST": 60*5, "CYCLES": 6, 
             "COLORS": {"PREPARE": "#093d85", "WORK": "#0e172e", "REST": "#093d85"}},
    "TODO": {"PREPARE": 60, "WORK": 60*5, "REST": 60*1.7, "CYCLES": 8, 
             "COLORS": {"PREPARE": "#960026", "WORK": "#330819", "REST": "#960026"}}
}
# -----------------------------------------------------------------------------------

class IntervalTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interval Timer")
        self.geometry("300x230")
        self.overrideredirect(True)  # Remove a barra de título padrão
        self.attributes("-topmost", True)  # Sempre no topo
        self.timer_id = None
        self.current_mode = "MAIN"
        self.resizing = False

        # Barra de título personalizada ---------------------------------------------
        fonte = "Trebuchet MS"
        self.title_bar = tk.Frame(self, bg="black", relief="raised", bd=0)
        self.title_bar.pack(fill=tk.X)
        
        self.title_label = tk.Label(self.title_bar, text="Interval Timer", fg="white",
                                    bg="black", font=(fonte, 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=20, height=10,
                                      command=self.destroy, font=(fonte, 12, "bold"))
        self.close_button.pack(side=tk.RIGHT, padx=6, pady=5)

        # self.min_button = ctk.CTkButton(self, text="_", width=20, height=10,
        #                                 command = lambda: self.wm_state("iconic"))
        # self.min_button.pack(side=tk.RIGHT, padx=6, pady=5)
        
        # self.max_button = ctk.CTkButton(self.title_bar, text="□", width=20, height=10,
        #                                 command=self.toggle_maximize, font=("Courier", 12, "bold"))
        # self.max_button.pack(side=tk.RIGHT, padx=6, pady=5)
        
        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Button-1>", self.get_pos)
        # ---------------------------------------------------------------------------

        # UI ------------------------------------------------------------------------
        self.phase_label = tk.Label(self, font=(fonte, 40, "bold"), fg="#8f96a1")
        self.phase_label.place(relx=0.5, rely=0.45, anchor="s")

        self.time_label = tk.Label(self, font=(fonte, 60), fg="white")
        self.time_label.place(relx=0.5, rely=0.45, anchor="n")

        self.pause_button = ctk.CTkButton(self, text="II", font=(fonte, 20, "bold"), 
                                      command=self.toggle_pause, width=30)
        self.pause_button.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

        self.main_button = ctk.CTkButton(self, text="MAIN", font=(fonte, 12, "bold"), 
                                     command=lambda: self.set_mode("MAIN"), width=20)
        self.main_button.place(relx=0, rely=1, anchor="sw", x=14, y=-10)

        self.todo_button = ctk.CTkButton(self, text="TO DO", font=(fonte, 12, "bold"), 
                                     command=lambda: self.set_mode("TODO"), width=20)
        self.todo_button.place(relx=0, rely=1, anchor="sw", x=(14*3+20), y=-10) 
        # ---------------------------------------------------------------------------

        # Área de redimensionamento
        self.grip = tk.Label(self, cursor="bottom_right_corner")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<ButtonPress-1>", self.start_resize)
        self.grip.bind("<B1-Motion>", self.do_resize)

        self.set_mode("MAIN")  # Inicia no modo MAIN
    
    # -------------------------------------------------------------------------------
    def get_pos(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def move_window(self, event):
        self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")
    # -------------------------------------------------------------------------------

    # def toggle_maximize(self):
    #     if self.maximized:
    #         self.geometry("300x230")
    #         self.maximized = False
    #     else:
    #         self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
    #         self.maximized = True

    # -------------------------------------------------------------------------------
    def start_resize(self, event):
        self.resizing = True
        self.x_start = event.x_root
        self.y_start = event.y_root
        self.width_start = self.winfo_width()
        self.height_start = self.winfo_height()

    def do_resize(self, event):
        if self.resizing:
            new_width = self.width_start + (event.x_root - self.x_start)
            new_height = self.height_start + (event.y_root - self.y_start)
            self.geometry(f"{new_width}x{new_height}")
    # -------------------------------------------------------------------------------

    def set_mode(self, mode):
        self.current_mode = mode
        self.setup = SETUPS[mode]
        self.phases = [("PREPARE", self.setup["PREPARE"])]+[("WORK", self.setup["WORK"]),
                                       ("REST", self.setup["REST"])] * self.setup["CYCLES"]
        self.current_phase = 0
        self.time_left = self.phases[self.current_phase][1]
        self.running = False
        self.start_timer()

    # def minim(self):
    #     self.wm_state("iconic")

    # -------------------------------------------------------------------------------
    def start_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.update_display()
        self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.timer_id = self.after(1000, self.countdown)
        elif self.running:
            self.next_phase()

    def next_phase(self):
        self.current_phase += 1
        if self.current_phase < len(self.phases):
            self.time_left = self.phases[self.current_phase][1]
            self.update_display()
            self.countdown()
        else:
            self.phase_label.config(text="END", bg=self.setup["COLORS"]["PREPARE"])
            self.time_label.config(text="", bg=self.setup["COLORS"]["PREPARE"])
            self.running = False
    # -------------------------------------------------------------------------------

    def toggle_pause(self):
        self.running = not self.running
        if self.running:
            self.countdown()
        else:
            if self.timer_id:
                self.after_cancel(self.timer_id)        

    # -------------------------------------------------------------------------------
    def update_display(self): 
        phase_name, _ = self.phases[self.current_phase]
        bg_color = self.setup["COLORS"][phase_name]
        self.configure(bg=bg_color)

        darker_bg_color = "#%02x%02x%02x" % tuple(max(0, int(bg_color[i:i+2], 16) - 30) for i in (1, 3, 5))

        self.title_bar.configure(bg=bg_color)
        self.title_label.configure(bg=bg_color)
        self.close_button.configure(fg_color=bg_color, hover_color=darker_bg_color)

        self.pause_button.configure(fg_color=bg_color, hover_color=darker_bg_color)
        self.main_button.configure(fg_color=bg_color, hover_color=darker_bg_color)
        self.todo_button.configure(fg_color=bg_color, hover_color=darker_bg_color)
        self.grip.configure(bg = bg_color)
    # -------------------------------------------------------------------------------

        self.time_label.config(text=f"{self.time_left // 60:02}:{self.time_left % 60:02}", bg=bg_color)
        self.phase_label.config(text=phase_name, bg=bg_color)

if __name__ == "__main__":
    app = IntervalTimer()
    app.mainloop()

