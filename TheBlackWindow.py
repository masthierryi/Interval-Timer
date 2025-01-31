import tkinter as tk
import customtkinter as ctk 

# Configuração da Janela --------------------------------------------------
class CustomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.configure(fg_color="black")
        self.overrideredirect(True)  # Remove a barra de título
        self.attributes("-topmost", True)  # Sempre no topo
        self.resizing = False

        # Barra de título personalizada -----------------------------------
        fonte = "Trebuchet MS"
        self.title_bar = tk.Frame(self, bg="black", relief="raised", bd=0)
        self.title_bar.pack(fill=tk.X)
        
        self.title_label = tk.Label(self.title_bar, text="The Black Window by masTHIERRYi", fg="#030303", 
                                    bg="black", font=(fonte, 10, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=24, height=10,
                                      command=self.destroy, font=(fonte, 12, "bold"), text_color="black", fg_color= "black", hover_color="#1c1c1c")
        self.close_button.pack(side=tk.RIGHT, padx=6, pady=5)
        
        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Button-1>", self.get_pos)
        # ----------------------------------------------------------------

        # Área de redimensionamento --------------------------------------
        self.grip = tk.Label(self, cursor="bottom_right_corner",bg="black")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<ButtonPress-1>", self.start_resize)
        self.grip.bind("<B1-Motion>", self.do_resize)
        # ----------------------------------------------------------------
    
    # Movimentação da Janela ----------------------------------------------
    def get_pos(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def move_window(self, event):
        self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")
    # ---------------------------------------------------------------------
    
    # Redimensionamento da Janela -----------------------------------------
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
    # ---------------------------------------------------------------------

if __name__ == "__main__":
    app = CustomApp()
    app.mainloop()
