import os
import threading
import tkinter as tk
from tkinter import ttk
import datetime
import math
import Orange
import numpy as np

try:
    import tkintermapview
except ImportError:
    tkintermapview = None

try:
    from PIL import Image, ImageTk
except ImportError:
    Image, ImageTk = None, None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "paramedicure_logo.png")

DATASET_PATH = os.path.join(SCRIPT_DIR, "emergency_kiosk_dataset.tab")

COLOR_BG, COLOR_SIDEBAR, COLOR_SIDEBAR_BTN, COLOR_SIDEBAR_BTN_ACTIVE = "#0f1b2b", "#0a1420", "#16273d", "#1f8ef1"
COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED, COLOR_CARD = "#f4f7fb", "#9fb2c8", "#16273d"
COLOR_YELLOW, COLOR_GREEN, COLOR_RED = "#f5c518", "#2ecc71", "#e74c3c"

FONT_TITLE, FONT_H2, FONT_H3, FONT_BODY, FONT_SIDEBAR = ("Segoe UI", 30, "bold"), ("Segoe UI", 18, "bold"), ("Segoe UI", 14, "bold"), ("Segoe UI", 12), ("Segoe UI", 14, "bold")
KIOSKS = [
    {"name": "Lilongwe Central Kiosk", "lat": -13.9626, "lon": 33.7741}, {"name": "Lilongwe Area 25 Kiosk", "lat": -13.95, "lon": 33.65},
    {"name": "Blantyre Kiosk", "lat": -15.7861, "lon": 35.0058}, {"name": "Limbe Kiosk", "lat": -15.8092, "lon": 35.0508},
    {"name": "Mzuzu Kiosk", "lat": -11.4581, "lon": 34.0151}, {"name": "Zomba Kiosk", "lat": -15.3833, "lon": 35.3333}
]
AMBULANCE_SPEED_KMH = 45  

def mk_label(parent, text="", font=FONT_BODY, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def mk_button(parent, text, font, bg, command, fg="white", **kw):
    return tk.Button(parent, text=text, font=font, bg=bg, fg=fg, relief="flat", cursor="hand2", command=command, **kw)

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2)**2
    return 2 * r * math.asin(min(1, a**0.5))

def get_base_kiosk(lat, lon):
    nearest = min(KIOSKS, key=lambda k: haversine_km(lat, lon, k.get("lat", 0), k.get("lon", 0)))
    distance_km = haversine_km(lat, lon, nearest.get("lat", 0), nearest.get("lon", 0))
    return nearest, distance_km, max(1, round(distance_km / AMBULANCE_SPEED_KMH * 60))

class ParamediCureApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ParamediCure-Medical Kiosk Detection")
        self.configure(bg=COLOR_BG)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        self.nav_buttons = {}
        self.pinned_location, self.selected_stage_info, self.map_widget, self.pinned_marker, self.nearest_marker, self.dispatch_path = None, None, None, None, None, None
        self.pin_status_var, self.selected_diagnosis_var = tk.StringVar(value="No location pinned yet"), tk.StringVar(value="")
        self.is_ai_mode = tk.BooleanVar(value=True)
        
        self._build_layout()
        self._show_page("Home")
        self._generate_initial_training_data()

    def _generate_initial_training_data(self):
        if os.path.exists(DATASET_PATH): return
        domain = Orange.data.Domain(
            [Orange.data.ContinuousVariable("Latitude"), Orange.data.ContinuousVariable("Longitude")],
            Orange.data.DiscreteVariable("Recommended_Kiosk", values=[k["name"] for k in KIOSKS])
        )
        data_rows = []
        for _ in range(60):
            rand_kiosk = KIOSKS[np.random.randint(0, len(KIOSKS))]
            lat_noise = rand_kiosk["lat"] + np.random.uniform(-0.05, 0.05)
            lon_noise = rand_kiosk["lon"] + np.random.uniform(-0.05, 0.05)
            data_rows.append([lat_noise, lon_noise, rand_kiosk["name"]])
        table = Orange.data.Table.from_list(domain, data_rows)
        table.save(DATASET_PATH)

    def _build_layout(self):
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        mk_label(self.sidebar, "ParamediCure", bg=COLOR_SIDEBAR, font=("Segoe UI", 15, "bold"), pady=30, wraplength=200, justify="center").pack(fill="x")

        for key, label in [("Home", "Home"), ("Emergency", "Emergency"), ("About", "About Us")]:
            btn = tk.Button(self.sidebar, text=label, font=FONT_SIDEBAR, bg=COLOR_SIDEBAR_BTN, fg=COLOR_TEXT_LIGHT, activebackground=COLOR_SIDEBAR_BTN_ACTIVE, activeforeground="white", relief="flat", bd=0, anchor="w", padx=20, pady=16, cursor="hand2", command=lambda k=key: self._show_page(k))
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        ai_frame = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR, pady=10)
        ai_frame.pack(side="bottom", fill="x", padx=20)
        tk.Checkbutton(ai_frame, text="AI Dispatch Engine", variable=self.is_ai_mode, bg=COLOR_SIDEBAR, fg=COLOR_GREEN, activebackground=COLOR_SIDEBAR, selectcolor=COLOR_SIDEBAR, font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.clock_label = mk_label(self.sidebar, bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10))
        self.clock_label.pack(side="bottom", pady=10)
        self._tick_clock()
        mk_button(self.sidebar, "Exit Kiosk", ("Segoe UI", 10), COLOR_SIDEBAR, self.destroy, fg=COLOR_TEXT_MUTED, bd=0).pack(side="bottom", pady=(0, 5))

        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True)
        self.pages = {"Home": self._build_home_page(), "Emergency": self._build_emergency_page(), "About": self._build_about_page()}
        for page in self.pages.values(): page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _tick_clock(self):
        self.clock_label.config(text=datetime.datetime.now().strftime("%A, %d %B %Y   %H:%M:%S"))
        self.after(1000, self._tick_clock)

    def _show_dialog(self, title, message, accent=None):
        accent = accent or COLOR_SIDEBAR_BTN_ACTIVE
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.configure(bg=accent)
        dlg.transient(self)
        dlg.attributes("-topmost", True)
        card = tk.Frame(dlg, bg=COLOR_CARD)
        card.pack(fill="both", expand=True, padx=2, pady=2)
        mk_label(card, title, font=FONT_H2, bg=COLOR_CARD).pack(pady=10)
        mk_label(card, message, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=350, justify="center").pack(padx=20, pady=10)
        mk_button(card, "OK", ("Segoe UI", 12, "bold"), accent, dlg.destroy, padx=30, pady=5).pack(pady=15)
        dlg.geometry(f"440x260+{self.winfo_rootx() + 400}+{self.winfo_rooty() + 200}")

    def _show_page(self, key):
        self.pages[key].tkraise()
        for k, btn in self.nav_buttons.items(): btn.configure(bg=COLOR_SIDEBAR_BTN_ACTIVE if k == key else COLOR_SIDEBAR_BTN)

    def _build_home_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)
        wrapper = tk.Frame(page, bg=COLOR_BG)
        wrapper.place(relx=0.5, rely=0.42, anchor="center")
        mk_label(wrapper, "ParamediCure AI", font=FONT_TITLE, fg=COLOR_TEXT_LIGHT).pack()
        mk_label(wrapper, "Machine Learning Guided Triage Framework.", fg=COLOR_TEXT_MUTED).pack(pady=(6, 25))
        mk_button(wrapper, "Start Emergency Check", FONT_H3, COLOR_RED, lambda: self._show_page("Emergency"), padx=25, pady=14).pack()
        return page

    STAGE_DATA = [
        {"label": "STAGE 1", "color": COLOR_YELLOW, "text_color": "#3a2e00", "title": "Fractures", "choices": ["Arm / Wrist Fracture", "Leg / Ankle Fracture", "Rib Fracture"]},
        {"label": "STAGE 2", "color": COLOR_GREEN, "text_color": "#0a2e17", "title": "Fainting & Related", "choices": ["Fainting / Dizziness", "Low Blood Pressure", "Mild Breathing Difficulty"]},
        {"label": "STAGE 3", "color": COLOR_RED, "text_color": "#ffffff", "title": "Cardiac / Critical", "choices": ["Cardiac Arrest", "Heart Attack", "Stroke Symptoms"]}
    ]

    def _build_emergency_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)
        canvas = tk.Canvas(page, bg=COLOR_BG, highlightthickness=0)
        vscroll = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")
        sf = tk.Frame(canvas, bg=COLOR_BG)
        wid = canvas.create_window((0, 0), window=sf, anchor="nw")
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(wid, width=e.width))

        mk_label(sf, "Emergency AI Predictive Dispatch", font=FONT_H2).pack(pady=(25, 5), padx=30, anchor="w")
        dc = tk.Frame(sf, bg=COLOR_CARD)
        dc.pack(fill="x", padx=30, pady=(0, 20))
        db = tk.Frame(dc, bg=COLOR_CARD)
        db.pack(fill="x", padx=20, pady=20)
        db.columnconfigure((0,1), weight=1)

        mw = tk.Frame(db, bg=COLOR_CARD)
        mw.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        mc = tk.Frame(mw, width=430, height=430, bg="#0b1826", highlightthickness=1, highlightbackground="#22364f")
        mc.pack(); mc.pack_propagate(False)

        if tkintermapview:
            self.map_widget = tkintermapview.TkinterMapView(mc, width=430, height=430, corner_radius=0)
            self.map_widget.pack(fill="both", expand=True)
            self.map_widget.add_left_click_map_command(self._on_map_clicked)
            for k in KIOSKS: self.map_widget.set_marker(k["lat"], k["lon"], text=k["name"])
            self._refresh_dispatch_map()
        else:
            mk_label(mc, "Live map unavailable.", font=("Segoe UI", 10), bg="#0b1826", fg=COLOR_TEXT_MUTED).pack(expand=True)

        cw = tk.Frame(db, bg=COLOR_CARD)
        cw.grid(row=0, column=1, sticky="nsew")
        mk_label(cw, "Patient Coordinate Vector", font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(0, 6))
        mk_label(cw, textvariable=self.pin_status_var, bg="#0f1b2b", anchor="w", padx=10, pady=10).pack(fill="x", pady=(0, 8))
        
        mk_label(cw, "Active Triage Variant", font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(10, 4))
        self.diagnosis_display = mk_label(cw, textvariable=self.selected_diagnosis_var, bg="#0f1b2b", anchor="w", padx=10, pady=10)
        self.diagnosis_display.pack(fill="x", pady=(0, 4))
        self.dispatch_result_var = tk.StringVar()
        mk_label(cw, textvariable=self.dispatch_result_var, font=("Segoe UI", 11, "bold"), fg=COLOR_GREEN, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(0, 10))

        mk_button(cw, "RUN MACHINE LEARNING DISPATCH", ("Segoe UI", 13, "bold"), COLOR_RED, self._send_emergency_dispatch, pady=14).pack(fill="x", side="bottom")

        stf = tk.Frame(sf, bg=COLOR_BG)
        stf.pack(fill="x", expand=True, padx=30, pady=(0, 30))
        stf.columnconfigure((0, 1, 2), weight=1, uniform="stage")
        for col, stage in enumerate(self.STAGE_DATA): self._build_stage_card(stf, stage, col)
        return page

    def _on_map_clicked(self, coords):
        if not self.map_widget: return
        lat, lon = coords
        if self.pinned_marker: self.pinned_marker.delete()
        self.pinned_marker = self.map_widget.set_marker(lat, lon, text="Target Node")
        lbl = f"{lat:.4f}, {lon:.4f}"
        self.pinned_location = {"name": lbl, "lat": lat, "lon": lon}
        self.pin_status_var.set(lbl)
        self._refresh_dispatch_map(show_dispatch=True)

    def _predict_kiosk_via_knn(self, lat, lon):
        try:
            dataset = Orange.data.Table(DATASET_PATH)
            knn_learner = Orange.classification.KNNLearner(n_neighbors=3)
            knn_classifier = knn_learner(dataset)
            test_instance = Orange.data.Instance(dataset.domain, [lat, lon, "?"])
            prediction_idx = knn_classifier(test_instance)
            predicted_name = dataset.domain.class_var.values[int(prediction_idx)]
            for k in KIOSKS:
                if k["name"] == predicted_name: return k
        except Exception as e:
            print(f"[AI Model Warmup Fallback] {e}")
        return min(KIOSKS, key=lambda k: haversine_km(lat, lon, k["lat"], k["lon"]))

    def _refresh_dispatch_map(self, show_dispatch=False):
        if not self.map_widget or not self.pinned_location: return None
        if self.nearest_marker: self.nearest_marker.delete()
        if self.dispatch_path: self.dispatch_path.delete()
        lat, lon = self.pinned_location["lat"], self.pinned_location["lon"]
        self.map_widget.set_position(lat, lon)
        if show_dispatch:
            if self.is_ai_mode.get():
                target_kiosk = self._predict_kiosk_via_knn(lat, lon)
                prefix = "AI Predicted Node: "
            else:
                target_kiosk, _, _ = get_base_kiosk(lat, lon)
                prefix = "Closest Node: "
            self.nearest_marker = self.map_widget.set_marker(target_kiosk["lat"], target_kiosk["lon"], text=f"{prefix}{target_kiosk['name']}")
            self.dispatch_path = self.map_widget.set_path([(lat, lon), (target_kiosk["lat"], target_kiosk["lon"])], color=COLOR_RED, width=3)
            return target_kiosk

    def _build_stage_card(self, parent, stage, col):
        card = tk.Frame(parent, bg=COLOR_CARD)
        card.grid(row=0, column=col, sticky="nsew", padx=12, pady=10)
        banner = tk.Frame(card, bg=stage["color"])
        banner.pack(fill="x")
        mk_label(banner, stage["label"], font=("Segoe UI", 11, "bold"), bg=stage["color"], fg=stage["text_color"], pady=6).pack()
        body = tk.Frame(card, bg=COLOR_CARD, padx=18, pady=18)
        body.pack(fill="both", expand=True)
        mk_label(body, stage["title"], font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x")
        for choice in stage["choices"]:
            tk.Radiobutton(body, text=choice, value=choice, variable=self.selected_diagnosis_var, font=FONT_BODY, bg=COLOR_CARD, fg=COLOR_TEXT_LIGHT, selectcolor="#0f1b2b", activebackground=COLOR_CARD, command=lambda s=stage: [setattr(self, 'selected_stage_info', s), self.dispatch_result_var.set(""), self.diagnosis_display.configure(fg=s["color"])]).pack(fill="x", pady=2, anchor="w")

    def _send_emergency_dispatch(self):
        diag = self.selected_diagnosis_var.get()
        if not diag or not self.selected_stage_info:
            self._show_dialog("System Prompt", "Select target diagnostic configuration index.")
            return
        if not self.pinned_location:
            self._show_dialog("System Prompt", "Drop tracking location matrix vector pin.")
            return

        lat, lon = self.pinned_location["lat"], self.pinned_location["lon"]
        target_kiosk = self._refresh_dispatch_map(show_dispatch=True)
        dst = haversine_km(lat, lon, target_kiosk["lat"], target_kiosk["lon"])
        eta = max(1, round(dst / AMBULANCE_SPEED_KMH * 60))
        engine_lbl = "KNN ML CLASSIFIER" if self.is_ai_mode.get() else "DETERMINISTIC PROXY"
        self.dispatch_result_var.set(f"Engine: {engine_lbl}\nTarget: {target_kiosk['name']}\nETA: ~{eta} min")
        
        self._show_dialog("AI Dispatch Sequence Confirmed", f"Deployment Target: {target_kiosk['name']}\nCalculated Matrix Range: {dst:.2f} KM\nPredicted Target Intercept: ~{eta} Minutes\nTriage Vector: {diag}", accent=COLOR_GREEN)

        try:
            dataset = Orange.data.Table(DATASET_PATH)
            row = [float(lat), float(lon), str(target_kiosk['name'])]
            updated_table = Orange.data.Table.concatenate([dataset, Orange.data.Table.from_list(dataset.domain, [row])])
            updated_table.save(DATASET_PATH)
        except Exception as e:
            print(f"Incremental learning execution failure: {e}")

    def _build_about_page(self):
        page = tk.Frame(self.content, bg=COLOR_BG)
        mk_label(page, "AI System Architecture", font=FONT_H2).pack(pady=(30, 5), padx=30, anchor="w")
        container = tk.Frame(page, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        container.columnconfigure((0, 1), weight=1)
        fields = [
            ("Core AI Pipeline", "Implements an online learning pipeline utilizing Orange's KNN Machine Learning Classifier."),
            ("Academic Context", "Birla Public School - Class XII-I Capstone Artificial Intelligence Deployment Model Framework Project.")
        ]
        for i, (title, text) in enumerate(fields):
            r, c = divmod(i, 2)
            box = tk.Frame(container, bg=COLOR_CARD)
            box.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            mk_label(box, title, font=FONT_H3, bg=COLOR_CARD, anchor="w", padx=12, pady=8).pack(fill="x")
            txt = tk.Text(box, font=FONT_BODY, bg="#0f1b2b", fg=COLOR_TEXT_LIGHT, relief="flat", wrap="word", padx=10, pady=10, height=5)
            txt.insert("1.0", text); txt.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        return page

if __name__ == "__main__":
    ParamediCureApp().mainloop()
