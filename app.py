import json
import os
import tkinter as tk
from tkinter import ttk

DATA_FILE = "sysslor_data.json"


class VolvoPlannerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Volvo Planeraren - 240 & 940 Edition")
        self.root.geometry("880x620")
        self.root.configure(bg="#2c3e50")

        # Färgpalett
        self.bg_color = "#f4f6f9"
        self.sidebar_color = "#2c3e50"
        self.accent_color = "#2980b9"

        # Kategorier och deras färger
        self.categories = {
            "Alla": "#34495e",
            "Arbete & Studier": "#2980b9",
            "Hem & Hushåll": "#27ae60",
            "Bilarna (240 & 940)": "#c0392b",
            "Fritid & Övrigt": "#8e44ad",
        }

        self.current_category = "Alla"
        self.tasks = self.load_tasks()

        # Starta med välkomstskärmen
        self.show_welcome_screen()

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return [
            {
                "text": "Byta olja och filter på 940:n",
                "category": "Bilarna (240 & 940)",
                "done": False,
            },
            {
                "text": "Kolla tändstift och förgasare på 240:n",
                "category": "Bilarna (240 & 940)",
                "done": False,
            },
            {
                "text": "Handla mat inför helgen",
                "category": "Hem & Hushåll",
                "done": False,
            },
        ]

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    # ==========================================
    # VY 1: VÄLKOMSTSKÄRM MED VOLVO 240 & 940
    # ==========================================
    def show_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root, bg="#1a252f")
        self.welcome_frame.pack(fill="both", expand=True)

        title_lbl = tk.Label(
            self.welcome_frame,
            text="VÄLKOMMEN TILL DIN PLANERARE",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1a252f",
        )
        title_lbl.pack(pady=(35, 8))

        sub_lbl = tk.Label(
            self.welcome_frame,
            text="Dubbelt så pålitlig – med både Volvo 240 och 940 på uppfarten.",
            font=("Helvetica", 12, "italic"),
            fg="#bdc3c7",
            bg="#1a252f",
        )
        sub_lbl.pack(pady=(0, 15))

        # Bredare canvas (800 px) så båda bilarna får gott om plats
        canvas = tk.Canvas(
            self.welcome_frame,
            width=800,
            height=310,
            bg="#85c1e9",
            highlightthickness=0,
        )
        canvas.pack(pady=10)
        self.draw_scene(canvas)

        # Gör hela scenen klickbar
        canvas.bind("<Button-1>", lambda e: self.start_planner())
        canvas.config(cursor="hand2")

        start_btn = tk.Button(
            self.welcome_frame,
            text="Starta Planeraren  ➔",
            font=("Helvetica", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            padx=30,
            pady=12,
            borderwidth=0,
            cursor="hand2",
            command=self.start_planner,
        )
        start_btn.pack(pady=25)

    def draw_scene(self, c):
        """Ritar bakgrund samt både en blå Volvo 240 och en röd Volvo 940."""
        # Bakgrund: Sol och asfalt
        c.create_oval(700, 25, 760, 85, fill="#f1c40f", outline="")  # Sol
        c.create_rectangle(
            0, 235, 800, 310, fill="#34495e", outline=""
        )  # Asfalt

        # Vägmarkeringar
        for x in range(15, 800, 85):
            c.create_rectangle(x, 268, x + 45, 274, fill="#f1c40f", outline="")

        # Rubrik i himlen
        c.create_text(
            400,
            42,
            text="VOLVO 240  &  VOLVO 940",
            font=("Helvetica", 20, "bold"),
            fill="#1b4f72",
        )
        c.create_text(
            400,
            68,
            text="Klicka på bilarna för att öppna dina sysslor",
            font=("Helvetica", 10),
            fill="#2c3e50",
        )

        # Rita de två bilarna bredvid varandra
        self.draw_volvo_240(c, offset_x=35, offset_y=15)
        self.draw_volvo_940(c, offset_x=420, offset_y=15)

    def draw_volvo_240(self, c, offset_x=0, offset_y=0):
        """Ritar en klassisk blå Volvo 240 (extra kantig 80-talsprofil)."""
        ox, oy = offset_x, offset_y

        # Skugga under bilen
        c.create_oval(ox + 15, oy + 215, ox + 335, oy + 232, fill="#1c2833", outline="")

        car_color = "#2874a6"  # Klassisk Volvo 240-blå
        outline_color = "#1b4f72"
        trim_color = "#17202a"

        # Kaross (240 är ännu rakare i fronten och bakstammen än 940)
        body_points = [
            ox + 25, oy + 205,   # Bak nedre
            ox + 25, oy + 155,   # Rak bakstam
            ox + 85, oy + 155,   # Bagagelucka
            ox + 108, oy + 108,  # C-stolpe (brantare vinkel)
            ox + 235, oy + 108,  # Rakt tak
            ox + 265, oy + 155,  # A-stolpe / vindruta
            ox + 328, oy + 158,  # Lång, rak motorhuv
            ox + 330, oy + 205,  # Rak vertikal front
        ]
        c.create_polygon(body_points, fill=car_color, outline=outline_color, width=2)

        # Kromlist runt rutorna (typiskt 240)
        # Bakre sidoruta
        c.create_polygon(
            ox + 95, oy + 152,
            ox + 114, oy + 115,
            ox + 168, oy + 115,
            ox + 168, oy + 152,
            fill="#2c3e50",
            outline="#bdc3c7",
            width=1,
        )
        # Främre sidoruta
        c.create_polygon(
            ox + 176, oy + 152,
            ox + 176, oy + 115,
            ox + 230, oy + 115,
            ox + 255, oy + 152,
            fill="#2c3e50",
            outline="#bdc3c7",
            width=1,
        )

        # B-stolpe & dörrlinjer
        c.create_line(ox + 172, oy + 108, ox + 172, oy + 202, fill=outline_color, width=2)
        c.create_line(ox + 102, oy + 155, ox + 102, oy + 202, fill=outline_color, width=1)
        c.create_line(ox + 258, oy + 155, ox + 258, oy + 202, fill=outline_color, width=1)

        # Klassisk svart midjelist
        c.create_rectangle(ox + 25, oy + 178, ox + 330, oy + 184, fill=trim_color, outline="")

        # Kromade dörrhandtag
        c.create_rectangle(ox + 125, oy + 164, ox + 138, oy + 168, fill="#bdc3c7", outline="")
        c.create_rectangle(ox + 195, oy + 164, ox + 208, oy + 168, fill="#bdc3c7", outline="")

        # Extra kraftiga, utstickande 240-kofångare
        c.create_rectangle(ox + 14, oy + 190, ox + 40, oy + 208, fill=trim_color, outline="")
        c.create_rectangle(ox + 315, oy + 190, ox + 340, oy + 208, fill=trim_color, outline="")

        # Strålkastare (stående rektangulär 240-lykta + orange hörnblinkers)
        c.create_rectangle(ox + 324, oy + 160, ox + 331, oy + 176, fill="#fcf3cf", outline="#7f8c8d")
        c.create_rectangle(ox + 317, oy + 160, ox + 324, oy + 176, fill="#e67e22", outline="")

        # Bakljus
        c.create_rectangle(ox + 24, oy + 157, ox + 30, oy + 176, fill="#e74c3c", outline="")
        c.create_rectangle(ox + 24, oy + 164, ox + 30, oy + 170, fill="#f39c12", outline="")

        # Hjulhus & däck
        for wx in [ox + 78, ox + 280]:
            c.create_oval(wx - 28, oy + 176, wx + 28, oy + 232, fill="#17202a", outline="")
            c.create_oval(wx - 24, oy + 180, wx + 24, oy + 228, fill="#1c2833", outline="")
            # Klassiska plåtfälgar med kromad navkapsel
            c.create_oval(wx - 14, oy + 190, wx + 14, oy + 218, fill="#95a5a6", outline="#566573", width=2)
            c.create_oval(wx - 6, oy + 198, wx + 6, oy + 210, fill="#ecf0f1", outline="")

        # Modellskylt under bilen på asfalten
        c.create_text(
            ox + 178,
            oy + 242,
            text="Volvo 240",
            font=("Helvetica", 10, "bold"),
            fill="#ecf0f1",
        )

    def draw_volvo_940(self, c, offset_x=0, offset_y=0):
        """Ritar en röd Volvo 940 Sedan (något mer strömlinjeformad 90-talsprofil)."""
        ox, oy = offset_x, offset_y

        # Skugga under bilen
        c.create_oval(ox + 10, oy + 215, ox + 350, oy + 232, fill="#1c2833", outline="")

        car_color = "#b03a2e"  # Klassisk Volvo-röd
        outline_color = "#78281f"
        trim_color = "#17202a"

        # Huvudkaross (mer sluttande rutor och högre baklucka än 240)
        body_points = [
            ox + 20, oy + 205,   # Bakre nedre hörn
            ox + 20, oy + 155,   # Bakstam
            ox + 82, oy + 152,   # Bakluckans kant
            ox + 112, oy + 110,  # C-stolpe
            ox + 245, oy + 110,  # Taklinje
            ox + 280, oy + 152,  # A-stolpe / vindruta
            ox + 345, oy + 158,  # Lång motorhuv
            ox + 350, oy + 205,  # Front nedre hörn
        ]
        c.create_polygon(body_points, fill=car_color, outline=outline_color, width=2)

        # Rutor
        c.create_polygon(
            ox + 92, oy + 150,
            ox + 118, oy + 117,
            ox + 175, oy + 117,
            ox + 175, oy + 150,
            fill="#2c3e50",
            outline="",
        )
        c.create_polygon(
            ox + 183, oy + 150,
            ox + 183, oy + 117,
            ox + 240, oy + 117,
            ox + 270, oy + 150,
            fill="#2c3e50",
            outline="",
        )

        # B-stolpe & dörrlinjer
        c.create_line(ox + 179, oy + 110, ox + 179, oy + 202, fill=outline_color, width=2)
        c.create_line(ox + 102, oy + 152, ox + 102, oy + 202, fill=outline_color, width=1)
        c.create_line(ox + 272, oy + 152, ox + 272, oy + 202, fill=outline_color, width=1)

        # Klassisk svart sidolist
        c.create_rectangle(ox + 20, oy + 178, ox + 350, oy + 184, fill=trim_color, outline="")

        # Dörrhandtag
        c.create_rectangle(ox + 128, oy + 163, ox + 142, oy + 167, fill=trim_color, outline="")
        c.create_rectangle(ox + 200, oy + 163, ox + 214, oy + 167, fill=trim_color, outline="")

        # Rejäla integrerade 940-kofångare
        c.create_rectangle(ox + 12, oy + 190, ox + 36, oy + 207, fill=trim_color, outline="")
        c.create_rectangle(ox + 332, oy + 190, ox + 356, oy + 207, fill=trim_color, outline="")

        # Strålkastare
        c.create_rectangle(ox + 342, oy + 160, ox + 350, oy + 175, fill="#f9e79f", outline="#7f8c8d")
        c.create_rectangle(ox + 335, oy + 160, ox + 342, oy + 175, fill="#e67e22", outline="")

        # Bakljus
        c.create_rectangle(ox + 19, oy + 156, ox + 26, oy + 175, fill="#e74c3c", outline="")
        c.create_rectangle(ox + 19, oy + 163, ox + 26, oy + 169, fill="#f39c12", outline="")

        # Hjulhus & fälgar
        for wx in [ox + 78, ox + 295]:
            c.create_oval(wx - 28, oy + 176, wx + 28, oy + 232, fill="#17202a", outline="")
            c.create_oval(wx - 24, oy + 180, wx + 24, oy + 228, fill="#1c2833", outline="")
            # Lättmetallfälgar
            c.create_oval(wx - 15, oy + 189, wx + 15, oy + 219, fill="#bdc3c7", outline="#7f8c8d", width=2)
            c.create_oval(wx - 5, oy + 199, wx + 5, oy + 209, fill="#2c3e50", outline="")

        # Modellskylt under bilen på asfalten
        c.create_text(
            ox + 185,
            oy + 242,
            text="Volvo 940",
            font=("Helvetica", 10, "bold"),
            fill="#ecf0f1",
        )

    def start_planner(self):
        self.welcome_frame.destroy()
        self.build_main_ui()

    # ==========================================
    # VY 2: HUVUDPROGRAMMET (PLANERAREN)
    # ==========================================
    def build_main_ui(self):
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)

        # --- VÄNSTER SIDOPANEL (Kategorier) ---
        sidebar = tk.Frame(self.main_container, bg=self.sidebar_color, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_lbl = tk.Label(
            sidebar,
            text="🚗 VOLVO PLANERAREN",
            font=("Helvetica", 12, "bold"),
            fg="white",
            bg=self.sidebar_color,
        )
        logo_lbl.pack(pady=(25, 20), padx=10)

        cat_header = tk.Label(
            sidebar,
            text="KATEGORIER",
            font=("Helvetica", 9, "bold"),
            fg="#95a5a6",
            bg=self.sidebar_color,
        )
        cat_header.pack(anchor="w", padx=20, pady=(10, 5))

        self.cat_buttons = {}
        for cat_name in self.categories:
            btn = tk.Button(
                sidebar,
                text=f"  {cat_name}",
                font=("Helvetica", 11),
                fg="white",
                bg=self.sidebar_color,
                activebackground="#34495e",
                activeforeground="white",
                anchor="w",
                bd=0,
                padx=15,
                pady=10,
                cursor="hand2",
                command=lambda c=cat_name: self.select_category(c),
            )
            btn.pack(fill="x", pady=2)
            self.cat_buttons[cat_name] = btn

        # Knapp längst ner i sidopanelen för att se bilarna igen
        back_btn = tk.Button(
            sidebar,
            text="← Visa 240 & 940",
            font=("Helvetica", 10),
            fg="#bdc3c7",
            bg="#1a252f",
            bd=0,
            pady=10,
            cursor="hand2",
            command=self.return_to_volvo,
        )
        back_btn.pack(side="bottom", fill="x")

        # --- HÖGER HUVUDYTA (Sysslor) ---
        content_area = tk.Frame(self.main_container, bg=self.bg_color)
        content_area.pack(side="right", fill="both", expand=True, padx=25, pady=20)

        header_frame = tk.Frame(content_area, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 15))

        self.header_label = tk.Label(
            header_frame,
            text="Alla sysslor",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg=self.bg_color,
        )
        self.header_label.pack(side="left")

        self.count_label = tk.Label(
            header_frame,
            text="",
            font=("Helvetica", 11),
            fg="#7f8c8d",
            bg=self.bg_color,
        )
        self.count_label.pack(side="right", pady=8)

        # Inmatningsfält för ny syssla
        input_frame = tk.Frame(
            content_area,
            bg="white",
            padx=10,
            pady=10,
            highlightbackground="#dcdde1",
            highlightthickness=1,
        )
        input_frame.pack(fill="x", pady=(0, 20))

        self.task_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bd=0,
            fg="#2c3e50",
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(5, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Dropdown för kategori vid skapande
        selectable_cats = [c for c in self.categories.keys() if c != "Alla"]
        self.new_task_cat = tk.StringVar(value=selectable_cats[0])
        cat_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.new_task_cat,
            values=selectable_cats,
            state="readonly",
            width=18,
            font=("Helvetica", 10),
        )
        cat_dropdown.pack(side="left", padx=5)

        add_btn = tk.Button(
            input_frame,
            text="+ Lägg till",
            font=("Helvetica", 10, "bold"),
            bg="#27ae60",
            fg="white",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.add_task,
        )
        add_btn.pack(side="left", padx=(5, 0))

        # Scrollbar & lista för sysslor
        list_container = tk.Frame(content_area, bg=self.bg_color)
        list_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            list_container, bg=self.bg_color, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.select_category("Alla")

    def select_category(self, category):
        self.current_category = category
        self.header_label.config(text=category)

        if category != "Alla":
            self.new_task_cat.set(category)

        for name, btn in self.cat_buttons.items():
            if name == category:
                btn.config(bg="#34495e", font=("Helvetica", 11, "bold"))
            else:
                btn.config(bg=self.sidebar_color, font=("Helvetica", 11))

        self.render_tasks()

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return

        category = self.new_task_cat.get()
        self.tasks.append({"text": text, "category": category, "done": False})
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.render_tasks()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.render_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.render_tasks()

    def render_tasks(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        filtered = [
            (i, t)
            for i, t in enumerate(self.tasks)
            if self.current_category == "Alla"
            or t["category"] == self.current_category
        ]

        done_count = sum(1 for _, t in filtered if t["done"])
        self.count_label.config(text=f"{done_count} av {len(filtered)} klara")

        if not filtered:
            empty_lbl = tk.Label(
                self.scrollable_frame,
                text="Inga sysslor i denna kategori ännu!",
                font=("Helvetica", 12, "italic"),
                fg="#95a5a6",
                bg=self.bg_color,
            )
            empty_lbl.pack(pady=40)
            return

        for original_idx, task in filtered:
            card = tk.Frame(
                self.scrollable_frame,
                bg="white",
                pady=10,
                padx=12,
                highlightbackground="#e1e4e8",
                highlightthickness=1,
            )
            card.pack(fill="x", pady=4)

            cat_color = self.categories.get(task["category"], "#7f8c8d")
            color_bar = tk.Frame(card, bg=cat_color, width=5)
            color_bar.pack(side="left", fill="y", padx=(0, 10))

            var = tk.BooleanVar(value=task["done"])
            chk = tk.Checkbutton(
                card,
                variable=var,
                bg="white",
                activebackground="white",
                cursor="hand2",
                command=lambda idx=original_idx: self.toggle_task(idx),
            )
            chk.pack(side="left")

            text_font = (
                ("Helvetica", 11, "overstrike")
                if task["done"]
                else ("Helvetica", 11)
            )
            text_color = "#95a5a6" if task["done"] else "#2c3e50"

            lbl = tk.Label(
                card,
                text=task["text"],
                font=text_font,
                fg=text_color,
                bg="white",
                anchor="w",
            )
            lbl.pack(side="left", fill="x", expand=True, padx=5)

            badge = tk.Label(
                card,
                text=task["category"],
                font=("Helvetica", 8, "bold"),
                fg="white",
                bg=cat_color,
                padx=8,
                pady=2,
            )
            badge.pack(side="left", padx=10)

            del_btn = tk.Button(
                card,
                text="✕",
                font=("Helvetica", 10, "bold"),
                fg="#e74c3c",
                bg="white",
                activebackground="#fadbd8",
                bd=0,
                cursor="hand2",
                command=lambda idx=original_idx: self.delete_task(idx),
            )
            del_btn.pack(side="right")

    def return_to_volvo(self):
        self.main_container.destroy()
        self.show_welcome_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = VolvoPlannerApp(root)
    root.mainloop()