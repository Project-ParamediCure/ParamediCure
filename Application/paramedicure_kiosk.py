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

try:
    from PIL import Image, ImageTk
except ImportError:
    Image, ImageTk = None, None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "paramedicure_logo.png")

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
    {"name": "Lilongwe Central Kiosk", "lat": -13.9626, "lon": 33.7741},
    {"name": "Lilongwe Area 25 Kiosk", "lat": -13.95, "lon": 33.65},
    {"name": "Blantyre Kiosk", "lat": -15.7861, "lon": 35.0058},
    {"name": "Limbe Kiosk", "lat": -15.8092, "lon": 35.0508},
    {"name": "Mzuzu Kiosk", "lat": -11.4581, "lon": 34.0151},
    {"name": "Zomba Kiosk", "lat": -15.3833, "lon": 35.3333},
    {"name": "Karonga Kiosk", "lat": -9.9333, "lon": 33.9333},
    {"name": "Chitipa Kiosk", "lat": -9.7028, "lon": 33.2694},
    {"name": "Rumphi Kiosk", "lat": -11.0167, "lon": 33.85},
    {"name": "Nkhata Bay Kiosk", "lat": -11.6083, "lon": 34.2986},
    {"name": "Likoma Island Kiosk", "lat": -12.0748, "lon": 34.7333},
    {"name": "Livingstonia Kiosk", "lat": -10.6, "lon": 34.1167},
    {"name": "Ekwendeni Kiosk", "lat": -11.35, "lon": 33.85},
    {"name": "Embangweni Kiosk", "lat": -11.6833, "lon": 33.6833},
    {"name": "Kasungu Kiosk", "lat": -13.0333, "lon": 33.4833},
    {"name": "Dowa Kiosk", "lat": -13.65, "lon": 33.9333},
    {"name": "Mponela Kiosk", "lat": -13.517, "lon": 33.717},
    {"name": "Ntchisi Kiosk", "lat": -13.3667, "lon": 33.9167},
    {"name": "Dedza Kiosk", "lat": -14.3667, "lon": 34.3333},
    {"name": "Salima Kiosk", "lat": -13.7833, "lon": 34.45},
    {"name": "Nkhotakota Kiosk", "lat": -12.9333, "lon": 34.3},
    {"name": "Mchinji Kiosk", "lat": -13.8, "lon": 32.9},
    {"name": "Balaka Kiosk", "lat": -14.9833, "lon": 34.95},
    {"name": "Ntcheu Kiosk", "lat": -14.8167, "lon": 34.6333},
    {"name": "Mangochi Kiosk", "lat": -14.4783, "lon": 35.2645},
    {"name": "Monkey Bay Kiosk", "lat": -14.0833, "lon": 34.9167},
    {"name": "Liwonde Kiosk", "lat": -15.0667, "lon": 35.2167},
    {"name": "Machinga Kiosk", "lat": -15.15, "lon": 35.35},
    {"name": "Chiradzulu Kiosk", "lat": -15.6833, "lon": 35.15},
    {"name": "Thyolo Kiosk", "lat": -16.0667, "lon": 35.1333},
    {"name": "Luchenza Kiosk", "lat": -16.017, "lon": 35.3},
    {"name": "Mulanje Kiosk", "lat": -16.0333, "lon": 35.5},
    {"name": "Phalombe Kiosk", "lat": -15.8, "lon": 35.65},
    {"name": "Chikwawa Kiosk", "lat": -16.0333, "lon": 34.8},
    {"name": "Nsanje Kiosk", "lat": -16.9167, "lon": 35.2667},
    {"name": "Neno Kiosk", "lat": -15.4, "lon": 34.65}
]

AMBULANCE_SPEED_KMH = 45  

def mk_label(parent, text="", font=FONT_BODY, fg=COLOR_TEXT_LIGHT, bg=COLOR_BG, **kw):
    """Shortcut for a themed tk.Label - avoids repeating font/fg/bg on every call."""
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def mk_button(parent, text, font, bg, command, fg="white", **kw):
    """Shortcut for a themed, flat, hand-cursor tk.Button."""
    return tk.Button(parent, text=text, font=font, bg=bg, fg=fg, relief="flat",
                      cursor="hand2", command=command, **kw)

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

        mk_label(self.sidebar, "ParamediCure", bg=COLOR_SIDEBAR, font=("Segoe UI", 15, "bold"),
                 pady=30, wraplength=200, justify="center").pack(fill="x")

        nav_items = [("Home", "Home"), ("Emergency", "Emergency"), ("About", "About Us")]
        for key, label in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, font=FONT_SIDEBAR,
                bg=COLOR_SIDEBAR_BTN, fg=COLOR_TEXT_LIGHT,
                activebackground=COLOR_SIDEBAR_BTN_ACTIVE, activeforeground="white",
                relief="flat", bd=0, anchor="w", padx=20, pady=16, cursor="hand2",
                command=lambda k=key: self._show_page(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        self.clock_label = mk_label(self.sidebar, bg=COLOR_SIDEBAR, fg=COLOR_TEXT_MUTED, font=("Segoe UI", 10))
        self.clock_label.pack(side="bottom", pady=20)
        self._tick_clock()

        mk_button(self.sidebar, "Exit Kiosk", ("Segoe UI", 10), COLOR_SIDEBAR, self._confirm_exit,
                  fg=COLOR_TEXT_MUTED, bd=0).pack(side="bottom", pady=(0, 5))

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
        mk_label(card, icon, font=("Segoe UI", 14), bg=COLOR_CARD, fg=accent).pack(pady=(18, 4))
        mk_label(card, title, font=FONT_H2, bg=COLOR_CARD, wraplength=380, justify="center").pack(pady=(0, 8), padx=20)
        mk_label(card, message, bg=COLOR_CARD, fg=COLOR_TEXT_MUTED, wraplength=380, justify="center").pack(padx=20)

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

        ok_btn = mk_button(card, "OK", ("Segoe UI", 12, "bold"), accent or COLOR_SIDEBAR_BTN_ACTIVE,
                           dlg.destroy, padx=30, pady=8)
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

        no_btn = mk_button(btn_row, "Cancel", ("Segoe UI", 12, "bold"), COLOR_SIDEBAR_BTN, dlg.destroy, padx=24, pady=8)
        no_btn.pack(side="left", padx=(0, 10))

        yes_btn = mk_button(btn_row, "Exit", ("Segoe UI", 12, "bold"), accent or COLOR_RED, yes, padx=24, pady=8)
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

        self.logo_image = self._load_logo(target_height=200)
        if self.logo_image is not None:
            mk_label(wrapper, image=self.logo_image, bg=COLOR_BG).pack(pady=(0, 20))
        else:
            mk_label(wrapper, "[Logo image not found]", fg=COLOR_TEXT_MUTED).pack(pady=(0, 20))

        mk_label(wrapper, "ParamediCure", font=FONT_TITLE).pack()
        mk_label(wrapper, "Fast triage. Clear stages. Faster care.", fg=COLOR_TEXT_MUTED).pack(pady=(6, 25))
        mk_button(wrapper, "Start Emergency Check", FONT_H3, COLOR_RED,
                  lambda: self._show_page("Emergency"), padx=25, pady=14).pack()

        return page

    def _load_logo(self, target_height=200):
        if not os.path.exists(LOGO_PATH):
            return None
        if Image is not None and ImageTk is not None:
            img = Image.open(LOGO_PATH)
            ratio = target_height / img.height
            size = (max(1, round(img.width * ratio)), target_height)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        photo = tk.PhotoImage(file=LOGO_PATH)
        factor = max(1, round(photo.height() / target_height))
        return photo.subsample(factor, factor)

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

        mk_label(scroll_frame, "Emergency Dispatch & Triage", font=FONT_H2).pack(pady=(25, 5), padx=30, anchor="w")
        mk_label(scroll_frame, "1) Select your area   2) Choose the matching diagnosis below   3) Send the dispatch",
                 fg=COLOR_TEXT_MUTED).pack(pady=(0, 15), padx=30, anchor="w")

        dispatch_card = tk.Frame(scroll_frame, bg=COLOR_CARD)
        dispatch_card.pack(fill="x", padx=30, pady=(0, 20))

        mk_label(dispatch_card, "Dispatch Emergency Services", font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x", padx=20, pady=(16, 4))
        mk_label(dispatch_card, "Pin your exact location on the live map and we'll dispatch the nearest kiosk to you.",
                 font=("Segoe UI", 10), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, anchor="w").pack(fill="x", padx=20, pady=(0, 10))

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
                text="Live map unavailable.\n"
                     "Install the 'tkintermapview' package\n"
                     "(pip install tkintermapview)\n"
                     "to see the embedded dispatch map.",
                font=("Segoe UI", 10), bg="#0b1826", fg=COLOR_TEXT_MUTED,
                justify="center"
            ).pack(expand=True)

        mk_label(map_wrap, "Blue: Kiosk   Green: Pinned Location   Red: Nearest Dispatch  -  Tap map to drop pin",
                 font=("Segoe UI", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, wraplength=420, justify="left").pack(pady=(6, 0))

        control_wrap = tk.Frame(dispatch_body, bg=COLOR_CARD)
        control_wrap.grid(row=0, column=1, sticky="nsew")

        mk_label(control_wrap, "Your Location", font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(0, 6))

        self.pin_status_label = mk_label(control_wrap, textvariable=self.pin_status_var, font=FONT_BODY,
                                          bg="#0f1b2b", anchor="w", wraplength=260, justify="left", padx=10, pady=10)
        self.pin_status_label.pack(fill="x", pady=(0, 8))

        mk_button(control_wrap, "Pin Your Location on Map", ("Segoe UI", 11, "bold"),
                  COLOR_GREEN, self._prompt_pin_location, pady=10).pack(fill="x", pady=(0, 10))

        mk_label(control_wrap, "Selected Diagnosis", font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(10, 4))

        self.diagnosis_display = mk_label(control_wrap, textvariable=self.selected_diagnosis_var, font=FONT_BODY,
                                           bg="#0f1b2b", anchor="w", wraplength=260, justify="left", padx=10, pady=10)
        self.diagnosis_display.pack(fill="x", pady=(0, 4))
        mk_label(control_wrap, "(choose a diagnosis from a stage card below)", font=("Segoe UI", 9, "italic"),
                 fg=COLOR_TEXT_MUTED, bg=COLOR_CARD, anchor="w").pack(fill="x", pady=(0, 15))

        self.dispatch_result_var = tk.StringVar(value="")
        self.dispatch_result_label = mk_label(control_wrap, textvariable=self.dispatch_result_var, font=("Segoe UI", 10),
                                               fg=COLOR_GREEN, bg=COLOR_CARD, anchor="w", wraplength=260, justify="left")
        self.dispatch_result_label.pack(fill="x", pady=(0, 10))

        mk_button(control_wrap, "Recenter Map On My Area", ("Segoe UI", 11, "bold"), "#1f8ef1",
                  lambda: self._refresh_dispatch_map(show_dispatch=False), pady=10).pack(fill="x", pady=(0, 8))

        mk_button(control_wrap, "SEND EMERGENCY DISPATCH", ("Segoe UI", 13, "bold"), COLOR_RED,
                  self._send_emergency_dispatch, pady=14).pack(fill="x", side="bottom")

        mk_label(scroll_frame, "Choose the matching diagnosis", font=FONT_H3).pack(pady=(5, 10), padx=30, anchor="w")

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
            self.map_widget.set_position(-13.5, 34.0)
            self.map_widget.set_zoom(7)
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
        mk_label(banner, stage["label"], font=("Segoe UI", 11, "bold"),
                 bg=stage["color"], fg=stage["text_color"], pady=6).pack()

        body = tk.Frame(card, bg=COLOR_CARD, padx=18, pady=18)
        body.pack(fill="both", expand=True)

        mk_label(body, stage["title"], font=FONT_H3, bg=COLOR_CARD, anchor="w").pack(fill="x")
        mk_label(body, stage["note"], font=("Segoe UI", 10, "italic"), bg=COLOR_CARD, fg=stage["color"],
                 anchor="w", wraplength=260, justify="left").pack(fill="x", pady=(2, 14))
        mk_label(body, "Pick one:", font=("Segoe UI", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED,
                 anchor="w").pack(fill="x", pady=(0, 4))

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

        mk_label(page, "About Us", font=FONT_H2).pack(pady=(30, 5), padx=30, anchor="w")
        mk_label(page, "Type your facility / organisation information below.",
                 fg=COLOR_TEXT_MUTED).pack(pady=(0, 15), padx=30, anchor="w")

        container = tk.Frame(page, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        self.about_text_widgets = {}

        fields = [
            ("Our Mission", "ParamediCure is a project exploring how a simple kiosk interface could speed up emergency response letting someone pin their exact location, flag the nature of the emergency, and see the nearest dispatch point and estimated arrival time, all without needing a phone or having to explain their situation to a stranger. It is built as a working prototype of what community-level emergency dispatch could look like."),
            ("Our Vision", "By 2034, we envision a Malawi where distance never decides who survives an emergency where a kiosk within reach of every village, town, and city corner can connect a person in crisis to help within minutes, not hours. ParamediCure is a step toward that future: a model for decentralized, accessible emergency care that does not depend on owning a phone, knowing an address, or navigating a call center just a location pinned on a screen.\nWe believe empowering communities with tools like this simple, fast, and built for the moment someone needs it most can close the gap between emergency and response, especially for the people current systems reach last: rural areas, underserved districts, and anyone caught without immediate access to help."),
            ("Contact Information", "Project by: ParamediCure Team\nSchool Name: Birla Public School"),
            ("Facility Hours & Location", "This is a demonstration project, not a live emergency service. In a real deployment, kiosks would operate 24/7; for now this is a prototype showcasing the dispatch and triage workflow."),
        ]

        for i, (field_title, placeholder) in enumerate(fields):
            r, c = divmod(i, 2)
            box = tk.Frame(container, bg=COLOR_CARD)
            box.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            container.rowconfigure(r, weight=1)

            mk_label(box, field_title, font=FONT_H3, bg=COLOR_CARD, anchor="w", padx=12, pady=8).pack(fill="x")

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
