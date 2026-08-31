import tkinter as tk
from tkinter import ttk
import math

class ToasterTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2b2b2b")
        self.is_toasting = False
        self.timer_id = None
        self.time_left = 0.0
        self.current_temp = 20.0 
        self.max_time = 0.0
        self.total_toasts = 0
        self.setup_ui()

    def setup_ui(self):
        # Left Panel: Graphics
        self.canvas = tk.Canvas(self, width=250, height=300, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=20)

        self.glow = self.canvas.create_rectangle(50, 110, 150, 180, fill="#2b2b2b", outline="")
        self.crust = self.canvas.create_oval(70, 30, 130, 70, fill="#CD853F", outline="#A0522D", width=2)
        self.bread = self.canvas.create_rectangle(70, 50, 130, 130, fill="#F5DEB3", outline="#DEB887", width=2)

        self.canvas.create_rectangle(35, 125, 215, 255, fill="#1a1a1a", outline="")
        self.canvas.create_polygon(30, 140, 40, 120, 200, 120, 210, 140, 210, 250, 30, 250, fill="#a0a0a0", outline="#505050", width=2)
        self.canvas.create_rectangle(40, 140, 170, 240, fill="#c0c0c0", outline="")
        self.canvas.create_line(50, 120, 150, 120, fill="#111111", width=8)

        self.canvas.create_line(190, 140, 190, 220, fill="#333333", width=6) 
        self.lever_knob = self.canvas.create_oval(180, 135, 200, 155, fill="#d9534f", outline="#ac2925", width=2)

        # Right Panel: Controls & Stats
        control_frame = tk.Frame(self, bg="#2b2b2b")
        control_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        stats_frame = tk.LabelFrame(control_frame, text=" Live Stats ", bg="#2b2b2b", fg="#5bc0de", font=("Courier", 12, "bold"))
        stats_frame.pack(fill="x", pady=10)

        self.lbl_temp = tk.Label(stats_frame, text="Temp: 20°C", bg="#2b2b2b", fg="white", font=("Courier", 10))
        self.lbl_temp.pack(anchor="w", padx=10, pady=2)
        self.lbl_time = tk.Label(stats_frame, text="Time Left: 0.0s", bg="#2b2b2b", fg="white", font=("Courier", 10))
        self.lbl_time.pack(anchor="w", padx=10, pady=2)

        tk.Label(control_frame, text="Doneness Dial:", bg="#2b2b2b", fg="white", font=("Arial", 10)).pack(pady=(10, 0))
        self.dial = tk.Scale(control_frame, from_=1, to=10, orient="horizontal", bg="#2b2b2b", fg="white", highlightthickness=0, length=180)
        self.dial.set(5)
        self.dial.pack(pady=5)

        self.btn_push = tk.Button(control_frame, text="Push Lever", font=("Arial", 12, "bold"), bg="#5cb85c", fg="white", command=self.start_toasting)
        self.btn_push.pack(fill="x", pady=5)
        self.btn_eject = tk.Button(control_frame, text="EJECT", font=("Arial", 12, "bold"), bg="#d9534f", fg="white", command=self.eject_toast, state="disabled")
        self.btn_eject.pack(fill="x", pady=5)
        self.status_label = tk.Label(control_frame, text="Waiting for bread...", bg="#2b2b2b", fg="#aaa", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=10)

    def start_toasting(self):
        if self.is_toasting: return
        self.is_toasting = True
        level = self.dial.get()
        self.max_time = level * 1.5 
        self.time_left = self.max_time
        
        self.btn_push.config(state="disabled", bg="#555")
        self.btn_eject.config(state="normal")
        self.dial.config(state="disabled")
        self.status_label.config(text=f"Toasting at level {level}...", fg="#f0ad4e")

        self.canvas.itemconfig(self.bread, fill="#F5DEB3", outline="#DEB887")
        self.canvas.itemconfig(self.crust, fill="#CD853F", outline="#A0522D")
        self.canvas.coords(self.bread, 70, 110, 130, 190)
        self.canvas.coords(self.crust, 70, 90, 130, 130)
        self.canvas.coords(self.lever_knob, 180, 200, 200, 220) 
        self.canvas.itemconfig(self.glow, fill="#ff4500") 

        self.tick() 

    def tick(self):
        if not self.is_toasting: return
        self.time_left -= 0.1
        target_temp = 20 + (self.dial.get() * 25)
        progress = (self.max_time - self.time_left) / self.max_time
        self.current_temp = 20 + (target_temp - 20) * progress

        self.lbl_time.config(text=f"Time Left: {max(0, self.time_left):.1f}s")
        self.lbl_temp.config(text=f"Temp: {int(self.current_temp)}°C")

        if self.time_left <= 0:
            self.pop_toast(completed=True)
        else:
            self.timer_id = self.after(100, self.tick)

    def eject_toast(self):
        if not self.is_toasting: return
        if self.timer_id: self.after_cancel(self.timer_id)
        self.pop_toast(completed=False)

    def pop_toast(self, completed):
        self.is_toasting = False
        self.canvas.itemconfig(self.glow, fill="#2b2b2b")
        self.current_temp = 20.0
        self.lbl_temp.config(text=f"Temp: {int(self.current_temp)}°C")
        self.lbl_time.config(text="Time Left: 0.0s")

        time_toasted = self.max_time - self.time_left
        if time_toasted <= 2: body_col, crust_col, msg = "#F0E68C", "#D2B48C", "Barely warm."
        elif time_toasted <= 7: body_col, crust_col, msg = "#CD853F", "#8B4513", "Perfectly golden!"
        elif time_toasted <= 12: body_col, crust_col, msg = "#8B4513", "#5C4033", "A bit dark, scrape it."
        else: body_col, crust_col, msg = "#2F4F4F", "#1a1a1a", "Charcoal. Tragic."

        if not completed: msg = "Ejected early! " + msg

        self.canvas.itemconfig(self.bread, fill=body_col, outline=crust_col)
        self.canvas.itemconfig(self.crust, fill=crust_col, outline=crust_col)
        self.canvas.coords(self.bread, 70, 50, 130, 130)
        self.canvas.coords(self.crust, 70, 30, 130, 70)
        self.canvas.coords(self.lever_knob, 180, 135, 200, 155)

        self.btn_push.config(state="normal", bg="#5cb85c")
        self.btn_eject.config(state="disabled")
        self.dial.config(state="normal")
        self.status_label.config(text=f"POP! {msg}", fg="#5cb85c")

class FanTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2b2b2b")
        self.angle = 0
        self.speed = 0 # 0=Off, 1=Low, 2=Med, 3=High
        self.rpm = 0
        self.setup_ui()
        self.animate_fan()

    def setup_ui(self):
        self.canvas = tk.Canvas(self, width=250, height=300, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=20)

        # Fan Base & Cage
        self.canvas.create_polygon(100, 280, 150, 280, 135, 180, 115, 180, fill="#a0a0a0")
        self.canvas.create_oval(100, 270, 150, 290, fill="#707070")
        self.canvas.create_oval(50, 60, 200, 210, outline="#c0c0c0", width=4)
        
        # Blade storage
        self.blades = [self.canvas.create_line(125, 135, 125, 135, fill="#5bc0de", width=12) for _ in range(3)]
        self.canvas.create_oval(115, 125, 135, 145, fill="#e0e0e0") # Center hub

        control_frame = tk.Frame(self, bg="#2b2b2b")
        control_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        stats_frame = tk.LabelFrame(control_frame, text=" Fan Stats ", bg="#2b2b2b", fg="#5bc0de", font=("Courier", 12, "bold"))
        stats_frame.pack(fill="x", pady=10)
        self.lbl_rpm = tk.Label(stats_frame, text="Motor RPM: 0", bg="#2b2b2b", fg="white", font=("Courier", 10))
        self.lbl_rpm.pack(anchor="w", padx=10, pady=5)

        tk.Label(control_frame, text="Speed Setting:", bg="#2b2b2b", fg="white", font=("Arial", 10)).pack(pady=(10, 0))
        btn_frame = tk.Frame(control_frame, bg="#2b2b2b")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="OFF", width=5, command=lambda: self.set_speed(0)).pack(side="left", padx=2)
        tk.Button(btn_frame, text="1", width=3, bg="#5cb85c", command=lambda: self.set_speed(1)).pack(side="left", padx=2)
        tk.Button(btn_frame, text="2", width=3, bg="#f0ad4e", command=lambda: self.set_speed(2)).pack(side="left", padx=2)
        tk.Button(btn_frame, text="3", width=3, bg="#d9534f", command=lambda: self.set_speed(3)).pack(side="left", padx=2)

    def set_speed(self, level):
        self.speed = level
        target_rpm = level * 800
        self.lbl_rpm.config(text=f"Motor RPM: {target_rpm}")

    def animate_fan(self):
        # Update angle based on speed
        if self.speed == 1: self.angle += 10
        elif self.speed == 2: self.angle += 25
        elif self.speed == 3: self.angle += 45
        
        # Calculate end points for 3 blades using sine/cosine
        cx, cy, length = 125, 135, 65
        for i, blade in enumerate(self.blades):
            offset = self.angle + (i * 120)
            rad = math.radians(offset)
            ex = cx + length * math.cos(rad)
            ey = cy + length * math.sin(rad)
            self.canvas.coords(blade, cx, cy, ex, ey)

        self.after(20, self.animate_fan) # ~50 FPS

class BreadMachineTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2b2b2b")
        self.phase = "IDLE"
        self.time_left = 0
        self.paddle_angle = 0
        self.dough_size = 0 
        self.setup_ui()
        self.run_cycle()

    def setup_ui(self):
        self.canvas = tk.Canvas(self, width=250, height=300, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(side="left", padx=10, pady=20)

        # Machine Outer Body
        self.canvas.create_rectangle(40, 100, 210, 260, fill="#f5f5f5", outline="#ccc", width=3)
        self.canvas.create_polygon(40, 100, 60, 70, 190, 70, 210, 100, fill="#e0e0e0", outline="#ccc", width=2)
        
        # Viewing Window (Dark glass)
        self.canvas.create_rectangle(70, 120, 180, 200, fill="#222", outline="#555", width=3)
        
        # Inside the viewing window: The Dough & Drive Paddle
        self.dough = self.canvas.create_oval(110, 185, 140, 195, fill="#F5DEB3", state="hidden")
        self.paddle = self.canvas.create_line(125, 190, 145, 190, fill="#888", width=4)

        control_frame = tk.Frame(self, bg="#2b2b2b")
        control_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        stats_frame = tk.LabelFrame(control_frame, text=" Machine Stats ", bg="#2b2b2b", fg="#5bc0de", font=("Courier", 12, "bold"))
        stats_frame.pack(fill="x", pady=10)
        self.lbl_phase = tk.Label(stats_frame, text="Phase: IDLE", bg="#2b2b2b", fg="white", font=("Courier", 10))
        self.lbl_phase.pack(anchor="w", padx=10, pady=2)
        self.lbl_time = tk.Label(stats_frame, text="Time Left: 0s", bg="#2b2b2b", fg="white", font=("Courier", 10))
        self.lbl_time.pack(anchor="w", padx=10, pady=2)

        self.btn_start = tk.Button(control_frame, text="Start Baking", font=("Arial", 12, "bold"), bg="#5cb85c", fg="white", command=self.start_machine)
        self.btn_start.pack(fill="x", pady=10)

    def start_machine(self):
        if self.phase != "IDLE": return
        self.phase = "KNEADING"
        self.time_left = 60 # 60 ticks per phase for demonstration
        self.dough_size = 0
        self.canvas.itemconfig(self.dough, state="normal", fill="#F5DEB3")
        self.btn_start.config(state="disabled")

    def run_cycle(self):
        if self.phase == "KNEADING":
            self.paddle_angle = (self.paddle_angle + 35) % 360
            rad = math.radians(self.paddle_angle)
            ex = 125 + 15 * math.cos(rad)
            ey = 190 + 15 * math.sin(rad)
            self.canvas.coords(self.paddle, 125, 190, ex, ey)
            self.time_left -= 1
            if self.time_left <= 0:
                self.phase = "RISING"
                self.time_left = 60

        elif self.phase == "RISING":
            # Expand dough slowly
            self.dough_size += 0.4
            self.canvas.coords(self.dough, 110 - self.dough_size, 185 - self.dough_size*1.5, 
                                            140 + self.dough_size, 195)
            self.time_left -= 1
            if self.time_left <= 0:
                self.phase = "BAKING"
                self.time_left = 60

        elif self.phase == "BAKING":
            # Gradually change color to brown
            progress = (60 - self.time_left) / 60
            r = int(245 - (245 - 139) * progress) 
            g = int(222 - (222 - 69) * progress)
            b = int(179 - (179 - 19) * progress)
            hex_col = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.itemconfig(self.dough, fill=hex_col)
            
            self.time_left -= 1
            if self.time_left <= 0:
                self.phase = "IDLE"
                self.lbl_phase.config(text="Phase: DONE!")
                self.btn_start.config(state="normal")
                self.lbl_time.config(text="Time Left: 0s")
                self.after(50, self.run_cycle)
                return

        if self.phase != "IDLE":
            self.lbl_phase.config(text=f"Phase: {self.phase}")
            self.lbl_time.config(text=f"Time Left: {self.time_left//10}s")

        self.after(100, self.run_cycle)


class MundaneAppliancesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mundane Appliance Simulator")
        self.root.geometry("500x380")
        
        # Configure Tkinter Styles for the Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a1a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#333', foreground='white', padding=[10, 5], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#5bc0de')], foreground=[('selected', 'black')])

        # Create the Notebook (Tab Manager)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Initialize Tabs
        self.tab1 = ToasterTab(self.notebook)
        self.tab2 = FanTab(self.notebook)
        self.tab3 = BreadMachineTab(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.tab1, text="  Toaster  ")
        self.notebook.add(self.tab2, text="  Desk Fan  ")
        self.notebook.add(self.tab3, text=" Bread Machine ")


if __name__ == "__main__":
    app_root = tk.Tk()
    app = MundaneAppliancesApp(app_root)
    app_root.mainloop()