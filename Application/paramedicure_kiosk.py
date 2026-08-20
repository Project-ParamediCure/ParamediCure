# ParamediCure - Medical Kiosk Application
# Built with Tkinter for class XII-I Project

import os
import threading
import tkinter as tk
from tkinter import ttk
import datetime
import math

try:
    import tkintermapview
except ImportError:
    tkintermapview = None

COLOR_BG            = "#0f1b2b"   
COLOR_SIDEBAR       = "#0a1420"   
COLOR_SIDEBAR_BTN   = "#16273d"   
COLOR_SIDEBAR_BTN_ACTIVE = "#1f8ef1"  
COLOR_TEXT_LIGHT    = "#f4f7fb"
COLOR_TEXT_MUTED    = "#9fb2c8"
COLOR_CARD          = "#16273d"

COLOR_YELLOW        = "#f5c518"   
COLOR_GREEN         = "#2ecc71"   
COLOR_RED           = "#e74c3c"   

FONT_TITLE   = ("Segoe UI", 30, "bold")
FONT_H2      = ("Segoe UI", 18, "bold")
FONT_H3      = ("Segoe UI", 14, "bold")
FONT_BODY    = ("Segoe UI", 12)
FONT_SIDEBAR = ("Segoe UI", 14, "bold")

KIOSKS = [
    {"name": "Thiruvananthapuram Medical College Kiosk", "lat": 8.5470, "lon": 76.9270},
    {"name": "Thiruvananthapuram General Hospital Kiosk", "lat": 8.5010, "lon": 76.9520},
    {"name": "Kollam City Kiosk", "lat": 8.8932, "lon": 76.6141},
    {"name": "Kochi Kiosk", "lat": 9.9312, "lon": 76.2673},
    {"name": "Kozhikode Kiosk", "lat": 11.2588, "lon": 75.7804},
    {"name": "Kannur Kiosk", "lat": 11.8745, "lon": 75.3704},
    {"name": "Kottayam Kiosk", "lat": 9.5916, "lon": 76.5222},
    {"name": "Kanyakumari Kiosk", "lat": 8.0883, "lon": 77.5385},
    {"name": "Chennai Central Kiosk", "lat": 13.0827, "lon": 80.2707},
    {"name": "Chennai Anna Nagar Kiosk", "lat": 13.0855, "lon": 80.2090},
    {"name": "Coimbatore Kiosk", "lat": 11.0183, "lon": 76.9725},
    {"name": "Madurai Kiosk", "lat": 9.9252, "lon": 78.1198},
    {"name": "Tiruchirappalli Kiosk", "lat": 10.7905, "lon": 78.7047},
    {"name": "Salem Kiosk", "lat": 11.6643, "lon": 78.1460},
    {"name": "Bengaluru City Kiosk", "lat": 12.9716, "lon": 77.5946},
    {"name": "Bengaluru Whitefield Kiosk", "lat": 12.9698, "lon": 77.7499},
    {"name": "Mysuru Kiosk", "lat": 12.3051, "lon": 76.6551},
    {"name": "Mangaluru Kiosk", "lat": 12.8720, "lon": 74.8469},
    {"name": "Hyderabad Kiosk", "lat": 17.3850, "lon": 78.4867},
    {"name": "Hyderabad Hitech City Kiosk", "lat": 17.4482, "lon": 78.3714},
    {"name": "Vijayawada Kiosk", "lat": 16.5062, "lon": 80.6480},
    {"name": "Visakhapatnam Kiosk", "lat": 17.6868, "lon": 83.2185},
    {"name": "Guntur Kiosk", "lat": 16.3067, "lon": 80.4365},
    {"name": "Mumbai Kiosk", "lat": 19.0760, "lon": 72.8777},
    {"name": "Mumbai Andheri Kiosk", "lat": 19.1136, "lon": 72.8697},
    {"name": "Pune Kiosk", "lat": 18.5204, "lon": 73.8567},
    {"name": "Pune Hinjawadi Kiosk", "lat": 18.5912, "lon": 73.7386},
    {"name": "Nagpur Kiosk", "lat": 21.1490, "lon": 79.0824},
    {"name": "Ahmedabad Kiosk", "lat": 23.0225, "lon": 72.5714},
    {"name": "Ahmedabad SG Highway Kiosk", "lat": 23.0505, "lon": 72.5108},
    {"name": "Surat Kiosk", "lat": 21.1702, "lon": 72.8311},
    {"name": "Vadodara Kiosk", "lat": 22.3000, "lon": 73.2000},
    {"name": "Jaipur Kiosk", "lat": 26.9124, "lon": 75.7873},
    {"name": "Jaipur Malviya Nagar Kiosk", "lat": 26.8500, "lon": 75.8000},
    {"name": "Jodhpur Kiosk", "lat": 26.2389, "lon": 73.0243},
    {"name": "Udaipur Kiosk", "lat": 24.5854, "lon": 73.7125},
    {"name": "Delhi Central Kiosk", "lat": 28.6139, "lon": 77.2090},
    {"name": "Delhi Rohini Kiosk", "lat": 28.7380, "lon": 77.0680},
    {"name": "Delhi Dwarka Kiosk", "lat": 28.5883, "lon": 77.0392},
    {"name": "Noida Kiosk", "lat": 28.5355, "lon": 77.3910},
    {"name": "Gurugram Kiosk", "lat": 28.4595, "lon": 77.0266},
    {"name": "Faridabad Kiosk", "lat": 28.4089, "lon": 77.3178},
    {"name": "Lucknow Kiosk", "lat": 26.8467, "lon": 80.9462},
    {"name": "Kanpur Kiosk", "lat": 26.4725, "lon": 80.3310},
    {"name": "Prayagraj Kiosk", "lat": 25.4358, "lon": 81.8463},
    {"name": "Varanasi Kiosk", "lat": 25.3117, "lon": 83.0104},
    {"name": "Patna Kiosk", "lat": 25.6093, "lon": 85.1376},
    {"name": "Muzaffarpur Kiosk", "lat": 26.1226, "lon": 85.3906},
    {"name": "Bhopal Kiosk", "lat": 23.2599, "lon": 77.4126},
    {"name": "Indore Kiosk", "lat": 22.7196, "lon": 75.8577},
    {"name": "Jabalpur Kiosk", "lat": 23.1815, "lon": 79.9864},
    {"name": "Raipur Kiosk", "lat": 21.2514, "lon": 81.6296},
    {"name": "Ranchi Kiosk", "lat": 23.3441, "lon": 85.3096},
    {"name": "Kolkata Kiosk", "lat": 22.5726, "lon": 88.3639},
    {"name": "Kolkata Salt Lake Kiosk", "lat": 22.5760, "lon": 88.4260},
    {"name": "Howrah Kiosk", "lat": 22.5736, "lon": 88.3186},
    {"name": "Bhubaneswar Kiosk", "lat": 20.2961, "lon": 85.8245},
    {"name": "Cuttack Kiosk", "lat": 20.4625, "lon": 85.8830},
    {"name": "Guwahati Kiosk", "lat": 26.1445, "lon": 91.7362},
    {"name": "Shillong Kiosk", "lat": 25.5788, "lon": 91.8933},
    {"name": "Agartala Kiosk", "lat": 23.8315, "lon": 91.2868},
    {"name": "Imphal Kiosk", "lat": 24.8170, "lon": 93.9368},
    {"name": "Aizawl Kiosk", "lat": 23.7271, "lon": 92.7176},
    {"name": "Itanagar Kiosk", "lat": 27.0844, "lon": 93.6053},
    {"name": "Gangtok Kiosk", "lat": 27.3314, "lon": 88.6138},
    {"name": "Dehradun Kiosk", "lat": 30.3165, "lon": 78.0322},
    {"name": "Haridwar Kiosk", "lat": 29.9457, "lon": 78.1642},
    {"name": "Shimla Kiosk", "lat": 31.1048, "lon": 77.1734},
    {"name": "Chandigarh Kiosk", "lat": 30.7333, "lon": 76.7794},
    {"name": "Amritsar Kiosk", "lat": 31.6340, "lon": 74.8723},
    {"name": "Ludhiana Kiosk", "lat": 30.9000, "lon": 75.8573},
    {"name": "Patiala Kiosk", "lat": 30.3398, "lon": 76.3869},
    {"name": "Srinagar Kiosk", "lat": 34.0837, "lon": 74.7973},
    {"name": "Jammu Kiosk", "lat": 32.7266, "lon": 74.8570},
    {"name": "Panaji Kiosk", "lat": 15.4909, "lon": 73.8278},
    {"name": "Belagavi Kiosk", "lat": 15.8669, "lon": 74.5083},
    {"name": "Hubballi Kiosk", "lat": 15.3647, "lon": 75.1240},
    {"name": "Warangal Kiosk", "lat": 17.9689, "lon": 79.5941},
    {"name": "Tirupati Kiosk", "lat": 13.6288, "lon": 79.4192},
    {"name": "Nellore Kiosk", "lat": 14.4426, "lon": 79.9865},
    {"name": "Rajahmundry Kiosk", "lat": 16.9870, "lon": 81.7787},
    {"name": "Tirunelveli Kiosk", "lat": 8.7274, "lon": 77.6838},
    {"name": "Kurnool Kiosk", "lat": 15.8222, "lon": 78.0362},
    {"name": "Alappuzha Kiosk", "lat": 9.4981, "lon": 76.3388},
    {"name": "Thrissur Kiosk", "lat": 10.5276, "lon": 76.2144},
    {"name": "Palakkad Kiosk", "lat": 10.7867, "lon": 76.6548},
    {"name": "Munnar Kiosk", "lat": 10.0889, "lon": 77.0595},
    {"name": "Dharwad Kiosk", "lat": 15.4589, "lon": 75.0078},
    {"name": "Vellore Kiosk", "lat": 12.9165, "lon": 79.1325},
    {"name": "Erode Kiosk", "lat": 11.3410, "lon": 77.7172},
    {"name": "Namakkal Kiosk", "lat": 11.2190, "lon": 78.1678},
    {"name": "Cuddalore Kiosk", "lat": 11.7471, "lon": 79.7714},
    {"name": "Nagercoil Kiosk", "lat": 8.1835, "lon": 77.4112},
    {"name": "Srikakulam Kiosk", "lat": 18.2949, "lon": 83.8960},
    {"name": "Karimnagar Kiosk", "lat": 18.4386, "lon": 79.1288},
    {"name": "Nashik Kiosk", "lat": 20.0110, "lon": 73.7903},
    {"name": "Solapur Kiosk", "lat": 17.6599, "lon": 75.9064},
    {"name": "Aurangabad Kiosk", "lat": 19.8762, "lon": 75.3433},
    {"name": "Kolhapur Kiosk", "lat": 16.7050, "lon": 74.2433},
    {"name": "Nanded Kiosk", "lat": 19.1383, "lon": 77.3210},
    {"name": "Sangli Kiosk", "lat": 16.8524, "lon": 74.5815},
    {"name": "Jalgaon Kiosk", "lat": 21.0077, "lon": 75.5626},
    {"name": "Bikaner Kiosk", "lat": 28.0229, "lon": 73.3119},
    {"name": "Ajmer Kiosk", "lat": 26.4499, "lon": 74.6399},
    {"name": "Alwar Kiosk", "lat": 27.5600, "lon": 76.6346},
    {"name": "Sikar Kiosk", "lat": 27.6165, "lon": 75.1443},
    {"name": "Bhilwara Kiosk", "lat": 25.3474, "tag_lon": 74.6384},
    {"name": "Kota Kiosk", "lat": 25.2138, "lon": 75.8648},
    {"name": "Sri Ganganagar Kiosk", "lat": 29.9094, "lon": 73.8770},
    {"name": "Rewari Kiosk", "lat": 28.1915, "lon": 76.6206},
    {"name": "Hisar Kiosk", "lat": 29.1492, "lon": 75.7217},
    {"name": "Rohtak Kiosk", "lat": 28.8955, "lon": 76.6066},
    {"name": "Meerut Kiosk", "lat": 28.9845, "lon": 77.7064},
    {"name": "Agra Kiosk", "lat": 27.1767, "lon": 78.0081},
    {"name": "Mathura Kiosk", "lat": 27.4924, "lon": 77.6737},
    {"name": "Aligarh Kiosk", "lat": 27.8815, "lon": 78.0740},
    {"name": "Bareilly Kiosk", "lat": 28.3670, "lon": 79.4304},
    {"name": "Moradabad Kiosk", "lat": 28.8386, "lon": 78.7830},
    {"name": "Saharanpur Kiosk", "lat": 29.9641, "lon": 77.5510},
    {"name": "Rishikesh Kiosk", "lat": 30.0869, "lon": 78.2676},
    {"name": "Pauri Kiosk", "lat": 30.1534, "lon": 78.7727},
    {"name": "Tezpur Kiosk", "lat": 26.6338, "lon": 92.7975},
    {"name": "Dibrugarh Kiosk", "lat": 27.4728, "lon": 94.9120},
    {"name": "Silchar Kiosk", "lat": 24.8273, "lon": 92.7979},
    {"name": "Jorhat Kiosk", "lat": 26.7500, "lon": 94.2038},
    {"name": "Dimapur Kiosk", "lat": 25.9090, "lon": 93.7278},
    {"name": "Kohima Kiosk", "lat": 25.6749, "lon": 94.1109},
    {"name": "Port Blair Kiosk", "lat": 11.6234, "lon": 92.7265},
    {"name": "Kavaratti Kiosk", "lat": 10.5626, "lon": 72.6369},
    {"name": "Leh Kiosk", "lat": 34.1526, "lon": 77.5771},
    {"name": "Kargil Kiosk", "lat": 34.5568, "lon": 76.1349}
]

AMBULANCE_SPEED_KMH = 45  

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2)
    return 2 * r * math.asin(min(1, a ** 0.5))

def nearest_kiosk_eta(lat, lon):
    nearest = min(KIOSKS, key=lambda k: haversine_km(lat, lon, k.get("lat", 0), k.get("lon", 0)))
    distance_km = haversine_km(lat, lon, nearest.get("lat", 0), nearest.get("lon", 0))
    eta_minutes = max(1, round(distance_km / AMBULANCE_SPEED_KMH * 60))
    return nearest, distance_km, eta_minutes

class ParamediCureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ParamediCure - Medical Kiosk")
        self.configure(bg=COLOR_BG)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.nav_buttons = {}

        self.pinned_location = None       
        self.pin_status_var = tk.StringVar(value="No location pinned yet")
        self.selected_diagnosis_var = tk.StringVar(value="")
        self.selected_stage_info = None   
        self.map_widget = None            
        self.pinned_marker = None         
        self.nearest_marker = None
        self.dispatch_path = None

        self._build_layout()
        self._show_page("Home")

    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Label(
            self.sidebar, text="ParamediCure", bg=COLOR_SIDEBAR,
            fg=COLOR_TEXT_LIGHT, font=("Segoe UI", 15, "bold"),
            pady=30, wraplength=200, justify="center"
        )
        logo.pack(fill="x")

        nav_items = [
            ("Home", "Home"),
            ("Emergency", "Emergency"),
            ("About", "About Us"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, font=FONT_SIDEBAR,
                bg=COLOR_SIDEBAR_BTN, fg=COLOR_TEXT_LIGHT,
                activebackground=COLOR_SIDEBAR_BTN_ACTIVE,
                activeforeground="white",
                relief="flat", bd=0, anchor="w", padx=20, pady=16,
                cursor="hand2",
                command=lambda k=key: self._show_page(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        self.clock_label = tk.Label(
            self.sidebar, text="", bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED,
            font=("Segoe UI", 10)
        )
        self.clock_label.pack(side="bottom", pady=20)
        self._tick_clock()

        exit_btn = tk.Button(
            self.sidebar, text="Exit Kiosk", font=("Segoe UI", 10),
            bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED, relief="flat", bd=0,
            cursor="hand2", command=self._confirm_exit
        )
        exit_btn.pack(side="bottom", pady=(0, 5))

        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True)

        self.pages = {}
        self.pages["Home"] = self._build_home_page()
        self.pages["Emergency"] = self._build_emergency_page()
        self.pages["About"] = self._build_about_page()

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _tick_clock(self):
        now = datetime.datetime.now().strftime("%A, %d %B %Y   %H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self._tick_clock)

    def _confirm_exit(self):
        self._show_confirm_dialog(
            "Exit Kiosk", "Close the ParamediCure application?",
            on_yes=self.destroy,
        )

    def _build_dialog_shell(self, title, message, accent, warning):
        accent = accent or COLOR_SIDEBAR_BTN_ACTIVE

        dlg = tk.Toplevel(self)
        dlg.title(title)          
        dlg.configure(bg=accent)  
        dlg.resizable(False, False)  
        dlg.transient(self)          
        dlg.attributes("-topmost", True)  
        dlg.withdraw()  

        card = tk.Frame(dlg, bg=COLOR_CARD)
        card.pack(fill="both", expand=True, padx=2, pady=2)

        icon = "Warning" if warning else "ParamediCure"
        tk.Label(card, text=icon, font=("Segoe UI", 14), bg=COLOR_CARD, fg=accent).pack(pady=(18, 4))
        tk.Label(
            card, text=title, font=FONT_H2, bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT,
            wraplength=380, justify="center"
        ).pack(pady=(0, 8), padx=20)
        tk.Label(
            card, text=message, font=FONT_BODY, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
            wraplength=380, justify="center"
        ).pack(padx=20)

        return dlg, card

    def _finalize_dialog(self, dlg, min_width=440):
        dlg.update_idletasks()
        w = max(min_width, dlg.winfo_reqwidth())
        h = dlg.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")
        dlg.deiconify()

    def _grab_dialog_safely(self, dlg, default_widget):
        def do_grab():
            try:
                dlg.grab_set()
            except tk.TclError:
                pass
            default_widget.focus_set()
        dlg.after(50, do_grab)

    def _show_dialog(self, title, message, accent=None, warning=False):
        dlg, card = self._build_dialog_shell(title, message, accent, warning)

        ok_btn = tk.Button(
            card, text="OK", font=("Segoe UI", 12, "bold"),
            bg=(accent or COLOR_SIDEBAR_BTN_ACTIVE), fg="white",
            relief="flat", padx=30, pady=8, cursor="hand2", command=dlg.destroy
        )
        ok_btn.pack(pady=(16, 18))

        dlg.protocol("WM_DELETE_WINDOW", dlg.destroy)
        dlg.bind("<Escape>", lambda e: dlg.destroy())
        dlg.bind("<Return>", lambda e: dlg.destroy())
        self._finalize_dialog(dlg)
        self._grab_dialog_safely(dlg, ok_btn)

    def _show_confirm_dialog(self, title, message, on_yes, accent=None):
        dlg, card = self._build_dialog_shell(title, message, accent, warning=False)

        def yes():
            dlg.destroy()
            on_yes()

        btn_row = tk.Frame(card, bg=COLOR_CARD)
        btn_row.pack(pady=(16, 18))

        no_btn = tk.Button(
            btn_row, text="Cancel", font=("Segoe UI", 12, "bold"),
            bg=COLOR_SIDEBAR_BTN, fg=COLOR_TEXT_LIGHT,
            relief="flat", padx=24, pady=8, cursor="hand2", command=dlg.destroy
        )
        no_btn.pack(side="left", padx=(0, 10))

        yes_btn = tk.Button(
            btn_row, text="Exit", font=("Segoe UI", 12, "bold"),
            bg=(accent or COLOR_RED), fg="white",
            relief="flat", padx=24, pady=8, cursor="hand2", command=yes
        )
        yes_btn.pack(side="left")

        dlg.protocol("WM_DELETE_WINDOW", dlg.destroy)
        dlg.bind("<Escape>", lambda e: dlg.destroy())
        self._finalize_dialog(dlg)
        self._grab_dialog_safely(dlg, no_btn)

    def _show_page(self, key):
        self.pages[key].tkraise()
        for k, btn in self.nav_buttons.items():
            btn.configure(bg=COLOR_SIDEBAR_BTN_ACTIVE if k == key else COLOR_SIDEBAR_BTN)

    def _build_home_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)

        wrapper = tk.Frame(page, bg=COLOR_BG)
        wrapper.place(relx=0.5, rely=0.42, anchor="center")

        canvas = tk.Canvas(wrapper, width=320, height=180, bg=COLOR_BG,
                            highlightthickness=0)
        canvas.pack(pady=(0, 20))
        self._draw_ambulance(canvas)

        title = tk.Label(
            wrapper, text="ParamediCure", font=FONT_TITLE,
            bg=COLOR_BG, fg=COLOR_TEXT_LIGHT
        )
        title.pack()

        subtitle = tk.Label(
            wrapper, text="Fast triage. Clear stages. Faster care.",
            font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED
        )
        subtitle.pack(pady=(6, 25))

        start_btn = tk.Button(
            wrapper, text="Start Emergency Check", font=FONT_H3,
            bg=COLOR_RED, fg="white", relief="flat", padx=25, pady=14,
            cursor="hand2", command=lambda: self._show_page("Emergency")
        )
        start_btn.pack()

        return page

    def _draw_ambulance(self, canvas):
        canvas.create_oval(30, 150, 290, 170, fill="#0a141f", outline="")
        canvas.create_rectangle(60, 70, 240, 140, fill="#ffffff", outline="#dcdcdc", width=2)
        canvas.create_polygon(240, 90, 280, 90, 290, 130, 240, 140,
                               fill="#ffffff", outline="#dcdcdc", width=2)
        canvas.create_polygon(248, 95, 272, 95, 280, 118, 248, 118, fill="#9fd8ff")
        canvas.create_rectangle(60, 118, 290, 128, fill=COLOR_RED, outline="")
        canvas.create_rectangle(130, 85, 150, 110, fill=COLOR_RED, outline="")
        canvas.create_rectangle(118, 92, 162, 103, fill=COLOR_RED, outline="")
        for wx in (100, 250):
            canvas.create_oval(wx - 15, 130, wx + 15, 160, fill="#1c1c1c", outline="")
            canvas.create_oval(wx - 6, 139, wx + 6, 151, fill="#666666", outline="")
        canvas.create_rectangle(150, 60, 210, 70, fill="#2b2b2b", outline="")
        canvas.create_oval(150, 58, 178, 70, fill=COLOR_RED, outline="")
        canvas.create_oval(182, 58, 210, 70, fill="#3b82f6", outline="")

    STAGE_DATA = [
        {
            "label": "STAGE 1", "color": COLOR_YELLOW, "text_color": "#3a2e00",
            "title": "Fractures",
            "note": "Non-critical, stable condition",
            "choices": [
                "Arm / Wrist Fracture",
                "Leg / Ankle Fracture",
                "Rib Fracture / Chest Injury (non-critical)",
            ],
        },
        {
            "label": "STAGE 2", "color": COLOR_GREEN, "text_color": "#0a2e17",
            "title": "Fainting & Related",
            "note": "Needs monitoring, urgent but stable",
            "choices": [
                "Fainting / Dizziness (Vasovagal)",
                "Low Blood Pressure Episode",
                "Mild Breathing Difficulty",
            ],
        },
        {
            "label": "STAGE 3", "color": COLOR_RED, "text_color": "#ffffff",
            "title": "Cardiac / Critical",
            "note": "Critical: Direct hospital admission within 15 minutes",
            "choices": [
                "Cardiac Arrest",
                "Heart Attack (Chest pain radiating to arm)",
                "Stroke Symptoms (Face drop / Slurred speech)",
            ],
        },
    ]

    def _build_emergency_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)

        outer_canvas = tk.Canvas(page, bg=COLOR_BG, highlightthickness=0)
        vscroll = ttk.Scrollbar(page, orient="vertical", command=outer_canvas.yview)
        outer_canvas.configure(yscrollcommand=vscroll.set)
        outer_canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        scroll_frame = tk.Frame(outer_canvas, bg=COLOR_BG)
        window_id = outer_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def _on_configure(event):
            outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
        scroll_frame.bind("<Configure>", _on_configure)

        def _on_canvas_resize(event):
            outer_canvas.itemconfig(window_id, width=event.width)
        outer_canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(event):
            if self.map_widget is not None:
                widget_path = str(event.widget)
                map_path = str(self.map_widget)
                if widget_path == map_path or widget_path.startswith(map_path + "."):
                    return
            outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        outer_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        tk.Label(scroll_frame, text="Emergency Dispatch & Triage", font=FONT_H2,
                 bg=COLOR_BG, fg=COLOR_TEXT_LIGHT).pack(pady=(25, 5), padx=30, anchor="w")
        tk.Label(scroll_frame,
                 text="1) Select your area   2) Choose the matching diagnosis below   3) Send the dispatch",
                 font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED
                 ).pack(pady=(0, 15), padx=30, anchor="w")

        dispatch_card = tk.Frame(scroll_frame, bg=COLOR_CARD)
        dispatch_card.pack(fill="x", padx=30, pady=(0, 20))

        tk.Label(dispatch_card, text="Dispatch Emergency Services", font=FONT_H3,
                 bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, anchor="w"
                 ).pack(fill="x", padx=20, pady=(16, 4))
        tk.Label(dispatch_card,
                 text="Pin your exact location on the live map and we'll dispatch the nearest kiosk to you.",
                 font=("Segoe UI", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w"
                 ).pack(fill="x", padx=20, pady=(0, 10))

        dispatch_body = tk.Frame(dispatch_card, bg=COLOR_CARD)
        dispatch_body.pack(fill="x", padx=20, pady=(0, 20))
        dispatch_body.columnconfigure(0, weight=1)
        dispatch_body.columnconfigure(1, weight=1)

        map_wrap = tk.Frame(dispatch_body, bg=COLOR_CARD)
        map_wrap.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        map_container = tk.Frame(map_wrap, width=430, height=430, bg="#0b1826",
                                  highlightthickness=1, highlightbackground="#22364f")
        map_container.pack()
        map_container.pack_propagate(False)

        if tkintermapview is not None:
            self.map_widget = tkintermapview.TkinterMapView(
                map_container, width=430, height=430, corner_radius=0
            )
            self.map_widget.pack(fill="both", expand=True)
            self.map_widget.add_left_click_map_command(self._on_map_clicked)
            self.kiosk_markers = []
            for kiosk in KIOSKS:
                self.kiosk_markers.append(
                    self.map_widget.set_marker(
                        kiosk.get("lat", 0), kiosk.get("lon", 0), text=kiosk.get("name", "Kiosk"),
                        marker_color_circle="#3b82f6", marker_color_outside="#1f8ef1",
                        text_color="#dceeff", font=("Segoe UI", 8),
                    )
                )
            self._refresh_dispatch_map()
        else:
            tk.Label(
                map_container,
                text="Live map unavailable.
Install the 'tkintermapview' package
"
                     "(pip install tkintermapview)
to see the embedded dispatch map.",
                font=("Segoe UI", 10), bg="#0b1826", fg=COLOR_TEXT_MUTED,
                justify="center"
            ).pack(expand=True)

        tk.Label(map_wrap, text="Blue: Kiosk   Green: Pinned Location   Red: Nearest Dispatch  -  Tap map to drop pin",
                 font=("Segoe UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=420, justify="left"
                 ).pack(pady=(6, 0))

        control_wrap = tk.Frame(dispatch_body, bg=COLOR_CARD)
        control_wrap.grid(row=0, column=1, sticky="nsew")

        tk.Label(control_wrap, text="Your Location", font=FONT_H3,
                 bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, anchor="w").pack(fill="x", pady=(0, 6))

        self.pin_status_label = tk.Label(
            control_wrap, textvariable=self.pin_status_var, font=FONT_BODY,
            bg="#0f1b2b", fg=COLOR_TEXT_LIGHT, anchor="w",
            wraplength=260, justify="left", padx=10, pady=10
        )
        self.pin_status_label.pack(fill="x", pady=(0, 8))

        pin_btn = tk.Button(
            control_wrap, text="Pin Your Location on Map", font=("Segoe UI", 11, "bold"),
            bg=COLOR_GREEN, fg="white", relief="flat", pady=10, cursor="hand2",
            command=self._prompt_pin_location
        )
        pin_btn.pack(fill="x", pady=(0, 10))

        tk.Label(control_wrap, text="Selected Diagnosis", font=FONT_H3,
                 bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, anchor="w").pack(fill="x", pady=(10, 4))

        self.diagnosis_display = tk.Label(
            control_wrap, textvariable=self.selected_diagnosis_var,
            font=FONT_BODY, bg="#0f1b2b", fg=COLOR_TEXT_LIGHT, anchor="w",
            wraplength=260, justify="left", padx=10, pady=10
        )
        self.diagnosis_display.pack(fill="x", pady=(0, 4))
        tk.Label(control_wrap, text="(choose a diagnosis from a stage card below)",
                 font=("Segoe UI", 9, "italic"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 15))

        self.dispatch_result_var = tk.StringVar(value="")
        self.dispatch_result_label = tk.Label(
            control_wrap, textvariable=self.dispatch_result_var, font=("Segoe UI", 10),
            bg=COLOR_CARD, fg=COLOR_GREEN, anchor="w", wraplength=260, justify="left"
        )
        self.dispatch_result_label.pack(fill="x", pady=(0, 10))

        recenter_btn = tk.Button(
            control_wrap, text="Recenter Map On My Area", font=("Segoe UI", 11, "bold"),
            bg="#1f8ef1", fg="white", relief="flat", pady=10, cursor="hand2",
            command=lambda: self._refresh_dispatch_map(show_dispatch=False)
        )
        recenter_btn.pack(fill="x", pady=(0, 8))

        send_btn = tk.Button(
            control_wrap, text="SEND EMERGENCY DISPATCH", font=("Segoe UI", 13, "bold"),
            bg=COLOR_RED, fg="white", relief="flat", pady=14, cursor="hand2",
            command=self._send_emergency_dispatch
        )
        send_btn.pack(fill="x", side="bottom")

        tk.Label(scroll_frame, text="Choose the matching diagnosis", font=FONT_H3,
                 bg=COLOR_BG, fg=COLOR_TEXT_LIGHT).pack(pady=(5, 10), padx=30, anchor="w")

        stages_frame = tk.Frame(scroll_frame, bg=COLOR_BG)
        stages_frame.pack(fill="x", expand=True, padx=30, pady=(0, 30))
        stages_frame.columnconfigure((0, 1, 2), weight=1, uniform="stage")

        for col, stage in enumerate(self.STAGE_DATA):
            self._build_stage_card(stages_frame, stage, col)

        return page

    def _prompt_pin_location(self):
        self._show_dialog(
            "Pin Your Location",
            "Tap anywhere on the live map to drop a pin at your location.\n\n"
            "We will look up the address and show you the nearest kiosk and "
            "its estimated arrival time.",
            accent=COLOR_GREEN,
        )

    def _on_map_clicked(self, coords):
        if self.map_widget is None:
            return
        lat, lon = coords

        if self.pinned_marker is not None:
            self.pinned_marker.delete()
            self.pinned_marker = None

        self.pinned_marker = self.map_widget.set_marker(
            lat, lon, text="Locating...",
            marker_color_circle=COLOR_GREEN, marker_color_outside="#1c8f4e",
        )
        self.pinned_location = {"name": f"{lat:.5f}, {lon:.5f}", "lat": lat, "lon": lon}
        self.pin_status_var.set("Locating address...")
        self.dispatch_result_var.set("")
        if self.nearest_marker is not None:
            self.nearest_marker.delete()
            self.nearest_marker = None
        if self.dispatch_path is not None:
            self.dispatch_path.delete()
            self.dispatch_path = None

        def lookup():
            try:
                adr = tkintermapview.convert_coordinates_to_address(lat, lon)
                parts = [str(p) for p in
                         (adr.street, adr.housenumber, adr.city, adr.state, adr.country)
                         if p]
                label = ", ".join(parts) if parts else f"{lat:.5f}, {lon:.5f}"
            except Exception:
                label = f"{lat:.5f}, {lon:.5f}"
            self.after(0, lambda: self._finish_pin(lat, lon, label))

        threading.Thread(target=lookup, daemon=True).start()

    def _finish_pin(self, lat, lon, label):
        if self.pinned_location is None or self.pinned_location["lat"] != lat or self.pinned_location["lon"] != lon:
            return  

        self.pinned_location["name"] = label
        self.pin_status_var.set(label)

        if self.pinned_marker is not None:
            try:
                self.pinned_marker.delete()
            except Exception:
                pass
        self.pinned_marker = self.map_widget.set_marker(
            lat, lon, text=f"Location: {label}",
            marker_color_circle=COLOR_GREEN, marker_color_outside="#1c8f4e",
        )

        nearest, distance_km, eta_minutes = nearest_kiosk_eta(lat, lon)
        self._show_dialog(
            "Location Pinned",
            f"{label}\n\n"
            f"Nearest kiosk: {nearest.get('name', 'Kiosk')}\n"
            f"Distance: {distance_km:.1f} km\n"
            f"Estimated arrival: ~{eta_minutes} min",
            accent=COLOR_GREEN,
        )

    def _refresh_dispatch_map(self, show_dispatch=False):
        if tkintermapview is None or self.map_widget is None:
            return

        if self.nearest_marker is not None:
            self.nearest_marker.delete()
            self.nearest_marker = None
        if self.dispatch_path is not None:
            self.dispatch_path.delete()
            self.dispatch_path = None

        if self.pinned_location is None:
            self.map_widget.set_position(22.5, 78.96)
            self.map_widget.set_zoom(5)
            return None

        lat, lon = self.pinned_location["lat"], self.pinned_location["lon"]
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(11)

        nearest = None
        if show_dispatch:
            nearest, distance_km, eta_minutes = nearest_kiosk_eta(lat, lon)
            self.nearest_marker = self.map_widget.set_marker(
                nearest.get("lat", 0), nearest.get("lon", 0), text=f"Nearest Dispatch: {nearest.get('name', 'Kiosk')}",
                marker_color_circle="#e74c3c", marker_color_outside="#a5271b",
            )
            self.dispatch_path = self.map_widget.set_path([
                (lat, lon), (nearest.get("lat", 0), nearest.get("lon", 0))
            ], color="#e74c3c", width=3)
            self.map_widget.set_zoom(7)

        return nearest

    def _build_stage_card(self, parent, stage, col):
        card = tk.Frame(parent, bg=COLOR_CARD, bd=0)
        card.grid(row=0, column=col, sticky="nsew", padx=12, pady=10)

        banner = tk.Frame(card, bg=stage["color"])
        banner.pack(fill="x")
        tk.Label(
            banner, text=stage["label"], font=("Segoe UI", 11, "bold"),
            bg=stage["color"], fg=stage["text_color"], pady=6
        ).pack()

        body = tk.Frame(card, bg=COLOR_CARD, padx=18, pady=18)
        body.pack(fill="both", expand=True)

        tk.Label(
            body, text=stage["title"], font=FONT_H3,
            bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, anchor="w"
        ).pack(fill="x")

        tk.Label(
            body, text=stage["note"], font=("Segoe UI", 10, "italic"),
            bg=COLOR_CARD, fg=stage["color"], anchor="w", wraplength=260, justify="left"
        ).pack(fill="x", pady=(2, 14))

        tk.Label(body, text="Pick one:", font=("Segoe UI", 10, "bold"),
                 bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, anchor="w").pack(fill="x", pady=(0, 4))

        for choice in stage["choices"]:
            rb = tk.Radiobutton(
                body, text=choice, value=choice, variable=self.selected_diagnosis_var,
                font=FONT_BODY, bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT,
                selectcolor="#0f1b2b", activebackground=COLOR_CARD,
                activeforeground=stage["color"], anchor="w", justify="left",
                wraplength=230, cursor="hand2",
                command=lambda s=stage: self._on_diagnosis_selected(s)
            )
            rb.pack(fill="x", pady=2, anchor="w")

    def _on_diagnosis_selected(self, stage):
        self.selected_stage_info = stage
        self.dispatch_result_var.set("")
        self.diagnosis_display.configure(fg=stage["color"])

    def _send_emergency_dispatch(self):
        diagnosis = self.selected_diagnosis_var.get()
        if not diagnosis or self.selected_stage_info is None:
            self._show_dialog(
                "Choose a Diagnosis",
                "Please select a diagnosis from Stage 1, 2, or 3 before sending the dispatch.",
                accent=COLOR_YELLOW, warning=True,
            )
            return

        if self.pinned_location is None:
            self._show_dialog(
                "Pin Your Location",
                "Please tap Pin Your Location on Map and drop a pin before sending the dispatch.",
                accent=COLOR_YELLOW, warning=True,
            )
            return

        stage = self.selected_stage_info
        lat, lon = self.pinned_location["lat"], self.pinned_location["lon"]

        nearest, distance_km, eta_minutes = nearest_kiosk_eta(lat, lon)
        self._refresh_dispatch_map(show_dispatch=True)

        urgent_note = ""
        if stage["label"] == "STAGE 3":
            urgent_note = "\n\nCritical: Direct hospital admission required within 15 minutes."

        result_text = (
            f"Dispatched: {nearest.get('name', 'Kiosk')}\n"
            f"Distance: {distance_km:.1f} km   ETA: ~{eta_minutes} min"
        )
        self.dispatch_result_var.set(result_text)

        self._show_dialog(
            "Emergency Dispatch Sent",
            f"Location: {self.pinned_location['name']}\n"
            f"Stage: {stage['label']} - {stage['title']}\n"
            f"Diagnosis: {diagnosis}\n\n"
            f"Nearest kiosk dispatched: {nearest.get('name', 'Kiosk')}\n"
            f"Distance: {distance_km:.1f} km\n"
            f"Estimated arrival: ~{eta_minutes} minutes"
            f"{urgent_note}",
            accent=COLOR_RED if stage["label"] == "STAGE 3" else COLOR_SIDEBAR_BTN_ACTIVE,
        )

        try:
            with open("emergency_dispatch_log.txt", "a", encoding="utf-8") as f:
                f.write(
                    f"[{datetime.datetime.now().isoformat(timespec='seconds')}] "
                    f"Location={self.pinned_location['name']} | Stage={stage['label']} ({stage['title']}) | "
                    f"Diagnosis={diagnosis} | Kiosk={nearest.get('name', 'Kiosk')} | "
                    f"Distance={distance_km:.1f}km | ETA={eta_minutes}min\n"
                )
        except OSError:
            pass  

    def _build_about_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)

        header = tk.Label(
            page, text="About Us", font=FONT_H2, bg=COLOR_BG, fg=COLOR_TEXT_LIGHT
        )
        header.pack(pady=(30, 5), padx=30, anchor="w")

        sub = tk.Label(
            page, text="Type your facility / organisation information below.",
            font=FONT_BODY, bg=COLOR_BG, fg=COLOR_TEXT_MUTED
        )
        sub.pack(pady=(0, 15), padx=30, anchor="w")

        container = tk.Frame(page, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self.about_text_widgets = {}

        fields = [
            ("Our Mission", "ParamediCure is a project exploring how a simple kiosk interface could speed up emergency response letting someone pin their exact location, flag the nature of the emergency, and see the nearest dispatch point and estimated arrival time, all without needing a phone or having to explain their situation to a stranger. It is built as a working prototype of what community-level emergency dispatch could look like."),
            ("Our Vision", "By 2034, we envision an India where distance never decides who survives an emergency where a kiosk within reach of every village, town, and city corner can connect a person in crisis to help within minutes, not hours. ParamediCure is a step toward that future: a model for decentralized, accessible emergency care that does not depend on owning a phone, knowing an address, or navigating a call center just a location pinned on a screen.\nWe believe empowering communities with tools like this simple, fast, and built for the moment someone needs it most can close the gap between emergency and response, especially for the people current systems reach last: rural areas, underserved neighborhoods, and anyone caught without immediate access to help."),
            ("Contact Information", "Project by: ParamediCure Team\nSchool Name: Birla Public School"),
            ("Facility Hours & Location", "This is a demonstration project, not a live emergency service. In a real deployment, kiosks would operate 24/7; for now this is a prototype showcasing the dispatch and triage workflow."),
        ]

        for i, (field_title, placeholder) in enumerate(fields):
            r, c = divmod(i, 2)
            box = tk.Frame(container, bg=COLOR_CARD)
            box.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            container.rowconfigure(r, weight=1)

            tk.Label(
                box, text=field_title, font=FONT_H3, bg=COLOR_CARD,
                fg=COLOR_TEXT_LIGHT, anchor="w", padx=12, pady=8
            ).pack(fill="x")

            text_widget = tk.Text(
                box, font=FONT_BODY, bg="#0f1b2b", fg=COLOR_TEXT_LIGHT,
                insertbackground=COLOR_TEXT_LIGHT, relief="flat", wrap="word",
                padx=10, pady=10, height=6
            )
            text_widget.insert("1.0", placeholder)
            text_widget.pack(fill="both", expand=True, padx=12, pady=(0, 12))
            self.about_text_widgets[field_title] = text_widget

        return page

if __name__ == "__main__":
    app = ParamediCureApp()
    app.mainloop()

