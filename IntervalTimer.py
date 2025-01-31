# Interval Timer by masTHIERRYi - 2025
import tkinter as tk
import customtkinter as ctk

SETUPS = {
    "MAIN": {"PREPARE": 7, "WORK": 2, "REST": 1, "CYCLES": 2, 
             "COLORS": {"PREPARE": "#093d85", "WORK": "#0e172e", "REST": "#093d85"}},
    "TODO": {"PREPARE": 5, "WORK": 3, "REST": 3, "CYCLES": 2, 
             "COLORS": {"PREPARE": "#960026", "WORK": "#330819", "REST": "#960026"}}
}

class IntervalTimer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interval Timer")
        self.geometry("300x230")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.timer_id = None
        self.running = False
        self.current_mode = "MAIN"
        self.resizing = False

        # UI - Barra de título personalizada
        fonte = "Trebuchet MS"
        self.title_bar = tk.Frame(self, bg="black")
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text="Interval Timer", fg="white", bg="black", font=(fonte, 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10)
        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=20, height=10, command=self.destroy, font=(fonte, 12, "bold"))
        self.close_button.pack(side=tk.RIGHT, padx=6, pady=5)

        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Button-1>", self.get_pos)

        # UI - Labels e botões
        self.phase_label = ctk.CTkLabel(self, font=(fonte, 40, "bold"), text_color="#8f96a1")
        self.phase_label.place(relx=0.5, rely=0.45, anchor="s")

        self.time_label = ctk.CTkLabel(self, font=(fonte, 60), text_color="white")
        self.time_label.place(relx=0.5, rely=0.45, anchor="n")

        self.pause_button = ctk.CTkButton(self, text="II", font=(fonte, 20, "bold"), command=self.toggle_pause, width=30)
        self.pause_button.place(relx=1, rely=1, anchor="se", x=-10, y=-10)

        self.main_button = ctk.CTkButton(self, text="MAIN", font=(fonte, 12, "bold"), command=lambda: self.set_mode("MAIN"), width=20)
        self.main_button.place(relx=0, rely=1, anchor="sw", x=14, y=-10)

        self.todo_button = ctk.CTkButton(self, text="TO DO", font=(fonte, 12, "bold"), command=lambda: self.set_mode("TODO"), width=20)
        self.todo_button.place(relx=0, rely=1, anchor="sw", x=58, y=-10) 

        # Área de redimensionamento
        self.grip = tk.Label(self, cursor="bottom_right_corner")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<ButtonPress-1>", self.start_resize)
        self.grip.bind("<B1-Motion>", self.do_resize)

        self.set_mode("MAIN")  # Inicia no modo MAIN
    
    # -------------------------------------------------------------------------------
    def get_pos(self, event):
        self.x_offset, self.y_offset = event.x, event.y

    def move_window(self, event):
        self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")

    # -------------------------------------------------------------------------------
    def start_resize(self, event):
        self.resizing = True
        self.x_start, self.y_start = event.x_root, event.y_root
        self.width_start, self.height_start = self.winfo_width(), self.winfo_height()

    def do_resize(self, event):
        if self.resizing:
            self.geometry(f"{self.width_start + (event.x_root - self.x_start)}x{self.height_start + (event.y_root - self.y_start)}")

    # -------------------------------------------------------------------------------
    def set_mode(self, mode):
        self.current_mode = mode
        self.setup = SETUPS[mode]
        self.phases = [("PREPARE", self.setup["PREPARE"])] + [("WORK", self.setup["WORK"]), ("REST", self.setup["REST"])] * self.setup["CYCLES"]
        self.current_phase = 0
        self.time_left = self.phases[self.current_phase][1]
        self.running = False
        self.start_timer()

    # -------------------------------------------------------------------------------
    def start_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.update_display()
        self.countdown()

    def countdown(self):
        if self.running:
            if self.time_left > 0:
                if self.time_left <= 3:
                    self.flash_screen(self.time_left * 2)
                else:
                    self.time_left -= 1
                    self.update_display()
                    self.timer_id = self.after(1000, self.countdown)
            else:
                self.update_display()
                self.after(500, self.next_phase)

    def flash_screen(self, flashes, count=0):
        if count < flashes:
            new_bg = "white" if count % 2 == 0 else self.setup["COLORS"][self.phases[self.current_phase][0]]
            self.set_background(new_bg)
            # self.phase_label.configure(fg_color=color)
            self.time_label.configure(text_color="#8f96a1" if count % 2 == 0 else "white")

            if count % 2 == 1:
                self.time_left -= 1
                self.update_display()

            self.after(500, lambda: self.flash_screen(flashes, count + 1))
        else:
            self.countdown() if self.time_left > 0 else self.after(500, self.next_phase)

    def next_phase(self):
        self.current_phase += 1
        if self.current_phase < len(self.phases):
            self.time_left = self.phases[self.current_phase][1]
            self.start_timer()
        else:
            self.phase_label.configure(text="END")
            self.time_label.configure(text="")
            self.running = False

    # -------------------------------------------------------------------------------
    def toggle_pause(self):
        self.running = not self.running
        if self.running:
            self.countdown()
        elif self.timer_id:
            self.after_cancel(self.timer_id)

    # -------------------------------------------------------------------------------
    def update_display(self):
        phase_name, _ = self.phases[self.current_phase]
        bg_color = self.setup["COLORS"][phase_name]
        self.set_background(bg_color)
        self.time_label.configure(text=f"{self.time_left // 60:02}:{self.time_left % 60:02}")
        self.phase_label.configure(text=phase_name)

    def set_background(self, color):
        phase_name, _ = self.phases[self.current_phase]
        bg_color = self.setup["COLORS"][phase_name]
        darker_color = "#%02x%02x%02x" % tuple(max(0, int(bg_color[i:i+2], 16) - 30) for i in (1, 3, 5))

        for widget in [self, self.title_bar, self.title_label, self.grip]:
            widget.configure(bg=color)

        for button in [self.close_button, self.pause_button, self.main_button, self.todo_button]:
            button.configure(fg_color=color, hover_color=darker_color)
            
if __name__ == "__main__":
    app = IntervalTimer()
    app.mainloop()
