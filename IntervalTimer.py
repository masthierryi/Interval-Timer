# Interval Timer v13.0 (Final Polished) by masTHIERRYi & Gemini - 2025
import tkinter as tk
import customtkinter as ctk
from tkinter import colorchooser
from collections import OrderedDict
import json
import os

# --- Settings Management Functions ---

def load_settings():
    """Loads settings from a JSON file. If it doesn't exist, uses defaults."""
    if os.path.exists('timer_settings.json'):
        with open('timer_settings.json', 'r') as f:
            try:
                return OrderedDict(json.load(f))
            except json.JSONDecodeError:
                pass  # If file is corrupted, fall back to defaults
    return OrderedDict([
        ("MAIN", {"PREPARE": 10, "WORK": 1560, "REST": 120, "CYCLES": 4,
                  "COLORS": {"PREPARE": "#093d85", "WORK": "#0e172e", "REST": "#093d85"}}),
        ("TODO", {"PREPARE": 30, "WORK": 300, "REST": 120, "CYCLES": 2,
                  "COLORS": {"PREPARE": "#960026", "WORK": "#330819", "REST": "#960026"}})
    ])

def save_settings(setups_dict):
    """Saves the settings dictionary to a JSON file."""
    with open('timer_settings.json', 'w') as f:
        json.dump(setups_dict, f, indent=4)

SETUPS = load_settings()

class IntervalTimer(tk.Tk):
    # PROPERTIES ====================================================================
    def __init__(self):
        super().__init__()
        self._configure_window()
        self._initialize_state()
        self._setup_ui()
        self.set_mode(self.current_mode)

    # --- Initialization Methods ---

    def _configure_window(self):
        """Sets up the main window properties."""
        self.SQUARE_GEOMETRY = "550x550"
        self.title("Interval Timer")
        self.geometry(self.SQUARE_GEOMETRY)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.font = "Trebuchet MS"

    def _initialize_state(self):
        """Initializes state variables for the application."""
        self.SETTINGS_BG = "#1C1C1C"
        self.SETTINGS_BTN_COLOR = "#424242"
        self.SETTINGS_BTN_HOVER = "#616161"
        self.timer_id = None
        self.running = False
        self.settings_visible = False
        self.current_mode = list(SETUPS.keys())[0]
        self.resizing_grip = None

    def _setup_ui(self):
        """Builds the main user interface by creating and packing frames."""
        self.title_bar = tk.Frame(self, bg="black")
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side=tk.TOP, fill="both", expand=True)
        self.settings_frame = ctk.CTkFrame(self, fg_color=self.SETTINGS_BG, corner_radius=10)
        
        self._create_title_bar_widgets()
        self._create_main_frame_widgets()
        self._create_settings_frame_widgets()
        self._create_resizing_grips()

    def _create_title_bar_widgets(self):
        """Creates widgets for the custom title bar and binds move events."""
        self.title_label = tk.Label(self.title_bar, text="Interval Timer", fg="white", bg="black", font=(self.font, 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=20, height=10, command=self.on_close, font=(self.font, 12, "bold"))
        self.close_button.pack(side=tk.RIGHT, padx=10, pady=8) # Increased padding
        
        # Bind move events to the entire bar and the label for robust dragging
        for widget in [self.title_bar, self.title_label]:
            widget.bind("<B1-Motion>", self.move_window)
            widget.bind("<Button-1>", self.get_pos)

    def _create_main_frame_widgets(self):
        """Creates widgets for the main timer display area."""
        self.phase_label = ctk.CTkLabel(self.main_frame, text="", font=(self.font, 40, "bold"), text_color="#8f96a1")
        self.phase_label.place(relx=0.5, rely=0.5, anchor="s", y=-10)
        self.time_label = ctk.CTkLabel(self.main_frame, text="", font=(self.font, 60), text_color="white")
        self.time_label.place(relx=0.5, rely=0.5, anchor="n", y=-10)
        
        bottom_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_bar.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.toggle_settings_button = ctk.CTkButton(bottom_bar, text="🖉", font=(self.font, 16, "bold"), command=self.toggle_settings_panel, width=30, height=30)
        self.toggle_settings_button.pack(side="right", padx=(5,0))
        self.pause_button = ctk.CTkButton(bottom_bar, text="▶", font=(self.font, 20, "bold"), command=self.toggle_pause, width=30, height=30)
        self.pause_button.pack(side="right")
        
        self.mode_buttons_frame = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        self.mode_buttons_frame.pack(side="top", expand=True)
        self.buttons = {}
        self._recreate_mode_buttons()

    def _create_settings_frame_widgets(self):
        """Creates widgets for the collapsible settings panel."""
        self.settings_frame.grid_rowconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        content_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        content_frame.grid(row=0, column=0, pady=10)

        labels_info = {"Name:": (0, 0), "Prep (s):": (0, 1), "Work (s):": (0, 2), "Rest (s):": (0, 3), "Cycles:": (0, 4)}
        for text, (r, c) in labels_info.items():
            ctk.CTkLabel(content_frame, text=text, font=(self.font, 12), text_color="white").grid(row=r, column=c)

        self.name_entry = ctk.CTkEntry(content_frame, width=100, font=(self.font, 12)); self.name_entry.grid(row=1, column=0, padx=3, pady=3)
        self.prepare_entry = ctk.CTkEntry(content_frame, width=70, font=(self.font, 12)); self.prepare_entry.grid(row=1, column=1, padx=3, pady=3)
        self.work_entry = ctk.CTkEntry(content_frame, width=70, font=(self.font, 12)); self.work_entry.grid(row=1, column=2, padx=3, pady=3)
        self.rest_entry = ctk.CTkEntry(content_frame, width=70, font=(self.font, 12)); self.rest_entry.grid(row=1, column=3, padx=3, pady=3)
        self.cycles_entry = ctk.CTkEntry(content_frame, width=70, font=(self.font, 12)); self.cycles_entry.grid(row=1, column=4, padx=3, pady=3)
        
        self.work_color_button = ctk.CTkButton(content_frame, text="Work Color", font=(self.font, 12), command=self._pick_work_color); self.work_color_button.grid(row=2, column=0, columnspan=2, pady=3, padx=3, sticky="ew")
        self.rest_color_button = ctk.CTkButton(content_frame, text="Rest Color", font=(self.font, 12), command=self._pick_rest_color); self.rest_color_button.grid(row=2, column=2, columnspan=3, pady=3, padx=3, sticky="ew")

        action_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        action_frame.grid(row=3, column=0, columnspan=5, pady=3)
        self.save_button = ctk.CTkButton(action_frame, text="✓", height=28, width=68, font=(self.font, 16, "bold"), command=self.save_custom_time, fg_color=self.SETTINGS_BTN_COLOR, hover_color=self.SETTINGS_BTN_HOVER); self.save_button.pack(side="left", padx=3)
        self.add_button = ctk.CTkButton(action_frame, text="+", height=28, width=35, font=(self.font, 16, "bold"), command=self._add_new_preset, fg_color=self.SETTINGS_BTN_COLOR, hover_color=self.SETTINGS_BTN_HOVER); self.add_button.pack(side="left", padx=3)
        self.delete_button = ctk.CTkButton(action_frame, text="🗑", height=28, width=35, font=(self.font, 16, "bold"), command=self._delete_current_preset, fg_color=self.SETTINGS_BTN_COLOR, hover_color=self.SETTINGS_BTN_HOVER); self.delete_button.pack(side="left", padx=3)

    def _create_resizing_grips(self):
        """Creates and places invisible labels to act as resizing grips on the corners."""
        self.grips = {}
        grip_size = 10
        
        # Only create grips for the four corners
        grip_configs = {
            'top_left': {'cursor': 'top_left_corner', 'place': {'relx': 0.0, 'rely': 0.0, 'anchor': 'nw'}},
            'top_right': {'cursor': 'top_right_corner', 'place': {'relx': 1.0, 'rely': 0.0, 'anchor': 'ne'}},
            'bottom_left': {'cursor': 'bottom_left_corner', 'place': {'relx': 0.0, 'rely': 1.0, 'anchor': 'sw'}},
            'bottom_right': {'cursor': 'bottom_right_corner', 'place': {'relx': 1.0, 'rely': 1.0, 'anchor': 'se'}},
        }

        for name, config in grip_configs.items():
            grip = tk.Label(self, cursor=config['cursor'])
            grip.place(**config['place'], width=grip_size, height=grip_size)
            grip.bind("<ButtonPress-1>", lambda event, n=name: self.start_resize(event, n))
            grip.bind("<B1-Motion>", self.do_resize)
            self.grips[name] = grip

    # METHODS =======================================================================
    def on_close(self):
        """Saves settings and closes the application."""
        save_settings(SETUPS)
        self.destroy()

    def get_pos(self, event): self.x_offset, self.y_offset = event.x, event.y
    def move_window(self, event): self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")
    
    def start_resize(self, event, grip_name):
        """Records initial values for a resize operation."""
        self.resizing_grip = grip_name
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.winfo_width()
        self.resize_start_height = self.winfo_height()
        self.resize_start_win_x = self.winfo_x()
        self.resize_start_win_y = self.winfo_y()

    def do_resize(self, event):
        """Calculates and applies new window geometry based on the active grip."""
        if not self.resizing_grip: return

        delta_x = event.x_root - self.resize_start_x
        delta_y = event.y_root - self.resize_start_y
        
        new_x, new_y = self.resize_start_win_x, self.resize_start_win_y
        new_width, new_height = self.resize_start_width, self.resize_start_height

        if 'left' in self.resizing_grip:
            new_width -= delta_x; new_x += delta_x
        if 'right' in self.resizing_grip:
            new_width += delta_x
        if 'top' in self.resizing_grip:
            new_height -= delta_y; new_y += delta_y
        if 'bottom' in self.resizing_grip:
            new_height += delta_y
        
        if new_width < 300: new_width = 300
        if new_height < 300: new_height = 300
        self.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

    def toggle_settings_panel(self):
        """Shows or hides the settings panel."""
        self.settings_visible = not self.settings_visible
        if self.settings_visible:
            self.settings_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
            self.toggle_settings_button.configure(text="v")
        else:
            self.settings_frame.pack_forget()
            self.toggle_settings_button.configure(text="🖉")

    def _recreate_mode_buttons(self):
        """Clears and recreates the mode selection buttons."""
        for widget in self.mode_buttons_frame.winfo_children(): widget.destroy()
        self.buttons = {}
        for i, mode in enumerate(SETUPS.keys()):
            self.buttons[mode] = ctk.CTkButton(self.mode_buttons_frame, text=mode, font=(self.font, 12, "bold"), command=lambda m=mode: self.set_mode(m), width=75)
            self.buttons[mode].pack(side="left", padx=3)

    def _update_entry_fields(self):
        """Populates the entry fields with data from the current mode."""
        if self.current_mode in SETUPS:
            s = SETUPS[self.current_mode]
            self.name_entry.delete(0, 'end'); self.name_entry.insert(0, self.current_mode)
            self.prepare_entry.delete(0, 'end'); self.prepare_entry.insert(0, str(s["PREPARE"]))
            self.work_entry.delete(0, 'end'); self.work_entry.insert(0, str(s["WORK"]))
            self.rest_entry.delete(0, 'end'); self.rest_entry.insert(0, str(s["REST"]))
            self.cycles_entry.delete(0, 'end'); self.cycles_entry.insert(0, str(s.get("CYCLES", 1)))
            self.work_color_button.configure(fg_color=s["COLORS"]["WORK"])
            self.rest_color_button.configure(fg_color=s["COLORS"]["REST"])

    def _pick_work_color(self):
        """Opens a color chooser for the work color."""
        color_code = colorchooser.askcolor(title="Choose Work Color")
        if color_code and color_code[1]: self.work_color_button.configure(fg_color=color_code[1])

    def _pick_rest_color(self):
        """Opens a color chooser for the rest color."""
        color_code = colorchooser.askcolor(title="Choose Rest Color")
        if color_code and color_code[1]: self.rest_color_button.configure(fg_color=color_code[1])

    def _add_new_preset(self):
        """Creates a new preset with a unique name and default settings."""
        base_name = "New Preset"; new_name = base_name; count = 1
        while new_name in SETUPS: new_name = f"{base_name} {count}"; count += 1
        SETUPS[new_name] = {"PREPARE": 5, "WORK": 10, "REST": 5, "CYCLES": 1,
                            "COLORS": {"PREPARE": "#4CAF50", "WORK": "#388E3C", "REST": "#4CAF50"}}
        self._recreate_mode_buttons(); self.set_mode(new_name)

    def _delete_current_preset(self):
        """Deletes the current preset if it's not the last one."""
        if len(SETUPS) <= 1: return
        del SETUPS[self.current_mode]; self._recreate_mode_buttons()
        self.set_mode(list(SETUPS.keys())[0])

    def save_custom_time(self):
        """Saves the current settings from the entry fields."""
        global SETUPS
        try:
            old_name = self.current_mode; new_name = self.name_entry.get().strip()
            if not new_name: return
            updated_settings = {
                "PREPARE": int(self.prepare_entry.get()), "WORK": int(self.work_entry.get()),
                "REST": int(self.rest_entry.get()), "CYCLES": int(self.cycles_entry.get()),
                "COLORS": { "WORK": self.work_color_button.cget("fg_color"), "REST": self.rest_color_button.cget("fg_color"), "PREPARE": self.rest_color_button.cget("fg_color")}
            }
            if old_name != new_name:
                new_setups = OrderedDict([(new_name if k == old_name else k, updated_settings if k == old_name else v) for k, v in SETUPS.items()])
                SETUPS = new_setups; self._recreate_mode_buttons(); self.set_mode(new_name)
            else: SETUPS[old_name] = updated_settings; self.set_mode(old_name)
        except (ValueError, KeyError): self._update_entry_fields()

    def set_mode(self, mode):
        """Sets the timer to a specific mode and resets its state."""
        if self.timer_id: self.after_cancel(self.timer_id)
        self.current_mode = mode; self.setup = SETUPS[mode]
        self.phases = [("PREPARE", self.setup["PREPARE"])] + [("WORK", self.setup["WORK"]), ("REST", self.setup["REST"])] * self.setup.get("CYCLES", 1)
        self.current_phase = 0; self.time_left = self.phases[self.current_phase][1] if self.phases else 0
        self.running = False; self.update_display(); self._update_entry_fields()

    def countdown(self):
        """The main timer loop, decrements time by 1 second."""
        if not self.running: return
        if self.time_left > 0:
            if self.time_left <= 3: self.flash_screen(self.time_left * 2)
            else: self.time_left -= 1; self.update_display(); self.timer_id = self.after(1000, self.countdown)
        else: self.next_phase()

    def next_phase(self):
        """Moves to the next phase in the sequence."""
        self.current_phase += 1
        if self.current_phase < len(self.phases):
            self.time_left = self.phases[self.current_phase][1]
            self.update_display()
            self.countdown()
        else:
            self.phase_label.configure(text="END"); self.time_label.configure(text="00:00")
            self.running = False; self.update_display()

    def flash_screen(self, flashes, count=0):
        """Flashes the screen for the last 3 seconds."""
        if not self.running: self.update_display(); return
        if count < flashes:
            color = self.setup["COLORS"][self.phases[self.current_phase][0]]; bg = "white" if count % 2 == 0 else color
            self.set_background(bg, is_flashing=True); self.time_label.configure(text_color="#8f96a1" if count % 2 == 0 else "white")
            if count % 2 == 1: self.time_left -= 1; self.update_display()
            self.after(500, lambda: self.flash_screen(flashes, count + 1))
        else:
            self.update_display()
            if self.time_left > 0: self.countdown()
            else: self.after(500, self.next_phase)

    def toggle_pause(self):
        """Toggles the running state of the timer."""
        self.running = not self.running
        if self.running: self.countdown()
        elif self.timer_id: self.after_cancel(self.timer_id)
        self.update_display()

    def update_display(self):
        """Updates the timer labels and background color."""
        self.pause_button.configure(text="II" if self.running else "▶")
        if self.current_phase >= len(self.phases): return
        phase_name, _ = self.phases[self.current_phase]
        self.set_background(self.setup["COLORS"][phase_name])
        self.time_label.configure(text=f"{self.time_left // 60:02}:{self.time_left % 60:02}")
        self.phase_label.configure(text=phase_name)

    def _calculate_darker_color(self, color_hex):
        """Calculates a darker shade of a given hex color."""
        try:
            rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            darker_rgb = tuple(max(0, c - 30) for c in rgb)
            return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"
        except (ValueError, TypeError):
            return color_hex

    def set_background(self, color, is_flashing=False):
        """Sets the background color for the main UI elements."""
        if not is_flashing and self.current_phase < len(self.phases):
            phase_name, _ = self.phases[self.current_phase]
            color = self.setup["COLORS"][phase_name]
        
        darker_color = self._calculate_darker_color(color)
        
        main_interface_buttons = [self.close_button, self.pause_button, self.toggle_settings_button] + list(self.buttons.values())
        for button in main_interface_buttons:
            button.configure(fg_color=color, hover_color=darker_color)
        
        # Color the grips to make them invisible against the background
        for widget in [self, self.title_bar, self.title_label] + list(self.grips.values()):
            widget.configure(bg=color)
        self.main_frame.configure(fg_color=color)

if __name__ == "__main__":
    app = IntervalTimer()
    app.mainloop()
