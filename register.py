#!/usr/bin/env python3
"""
Attendance Register Pro - MySQL (XAMPP) - Modern UI + Theme Toggle + Checkbox attendance
--------------------------------------------------------------------------------------
Single-file app.

DB schema (unchanged):
  students(id PK, first_name, last_name, ...)
  attendance(id PK, student_id FK->students.id, status, date, created_at)
  sessions(id PK, label, created_at) [optional]

Run: python attendance_register_mysql.py
Requires: mysql-connector-python
Optional extras: pip install matplotlib openpyxl reportlab tkcalendar
"""

import os
import json
import csv
import datetime as dt
import hashlib
import secrets
from functools import partial

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog

# MySQL connector
try:
    import mysql.connector
except Exception as e:
    mysql = None
    mysql_connector_error = e
else:
    mysql = mysql.connector
    mysql_connector_error = None

# Optional extras
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

try:
    from openpyxl import Workbook
except Exception:
    Workbook = None

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as pdf_canvas
except Exception:
    A4 = None
    pdf_canvas = None

# Optional date picker
Calendar = None
try:
    from tkcalendar import Calendar as TKCalendar  # type: ignore
    Calendar = TKCalendar
except Exception:
    pass

# --- Config / paths ---
APP_DIR = os.path.join(os.getcwd(), "attendance_data")
CONFIG_PATH = os.path.join(APP_DIR, "config.json")
BACKUP_DIR = os.path.join(APP_DIR, "backups")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # change if needed
    "database": "attendance_db",
    "port": 3306,
    "raise_on_warnings": True
}

# --- Utilities ---
def ensure_dirs():
    os.makedirs(APP_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def now_str():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_date():
    return dt.date.today()

def ymd(d: dt.date):
    return d.strftime("%Y-%m-%d")

def hash_password(pwd: str, salt: str = None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), bytes.fromhex(salt), 200_000).hex()
    return h, salt

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def init_config_if_missing():
    cfg = load_config()
    if cfg is None:
        h, s = hash_password("admin")
        cfg = {
            "username": "admin",
            "password_hash": h,
            "salt": s,
            "session_counter": 0,
            "theme": "light"
        }
        save_config(cfg)

def bump_session_id():
    cfg = load_config() or {}
    sid = int(cfg.get("session_counter", 0)) + 1
    cfg["session_counter"] = sid
    save_config(cfg)
    return sid

# --- DB helpers ---
def get_connection():
    if mysql is None:
        raise RuntimeError(f"mysql-connector not available: {mysql_connector_error}")
    return mysql.connect(**DB_CONFIG)

def init_db_mysql():
    """Verify DB connectivity (do not modify schema)."""
    try:
        cnx = get_connection()
        cnx.close()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("DB Error", f"Cannot connect to MySQL: {e}")
        root.destroy()
        raise

# --- Data functions ---
def add_student_db(first, last):
    first = first.strip().title()
    last = last.strip().title()
    try:
        with get_connection() as cnx:
            cur = cnx.cursor()
            try:
                cur.execute("INSERT INTO students (first_name, last_name) VALUES (%s, %s)", (first, last))
                cnx.commit()
                return cur.lastrowid
            except Exception:
                return None
    except Exception as e:
        messagebox.showerror("DB", f"Failed to add student: {e}")
        return None

def get_student_id(first, last):
    with get_connection() as cnx:
        cur = cnx.cursor()
        cur.execute("SELECT id FROM students WHERE first_name=%s AND last_name=%s", (first, last))
        row = cur.fetchone()
        return row[0] if row else None

def list_students():
    with get_connection() as cnx:
        cur = cnx.cursor()
        cur.execute("SELECT id, first_name, last_name FROM students ORDER BY first_name, last_name")
        return cur.fetchall()

def upsert_attendance(student_id, date_str, status):
    """Idempotent update: update-then-insert for (student_id, date)."""
    try:
        with get_connection() as cnx:
            cur = cnx.cursor()
            # validate student exists for clearer error
            cur.execute("SELECT id FROM students WHERE id=%s", (student_id,))
            if cur.fetchone() is None:
                raise ValueError(f"Student id {student_id} does not exist.")
            # update existing record
            cur.execute("""
                UPDATE attendance
                SET status=%s, created_at=%s
                WHERE student_id=%s AND date=%s
            """, (status, now_str(), student_id, date_str))
            if cur.rowcount == 0:
                # no row updated -> insert
                cur.execute("""
                    INSERT INTO attendance (student_id, date, status, created_at)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, date_str, status, now_str()))
            cnx.commit()
    except ValueError as ve:
        messagebox.showerror("DB Error", str(ve))
    except Exception as e:
        messagebox.showerror("DB Error", f"Failed to upsert attendance: {e}")

def fetch_attendance(date_str=None, name_query="", status=None):
    with get_connection() as cnx:
        cur = cnx.cursor()
        q = """
            SELECT a.id, s.id, s.first_name, s.last_name, a.status, DATE_FORMAT(a.date, '%Y-%m-%d')
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            WHERE 1=1
        """
        params = []
        if date_str:
            q += " AND a.date = %s"
            params.append(date_str)
        if name_query:
            q += " AND (LOWER(s.first_name) LIKE %s OR LOWER(s.last_name) LIKE %s)"
            like = f"%{name_query.lower()}%"
            params += [like, like]
        if status in ("Present", "Absent"):
            q += " AND a.status = %s"
            params.append(status)
        q += " ORDER BY s.first_name, s.last_name"
        cur.execute(q, params)
        return cur.fetchall()

def fetch_attendance_map_for_date(date_str):
    """Return dict student_id -> (attendance_id, status) for that date."""
    rows = fetch_attendance(date_str)
    return {r[1]: (r[0], r[4]) for r in rows}  # student_id -> (att_id, status)

def delete_attendance_rows(ids):
    if not ids:
        return
    try:
        with get_connection() as cnx:
            cur = cnx.cursor()
            cur.executemany("DELETE FROM attendance WHERE id=%s", [(i,) for i in ids])
            cnx.commit()
    except Exception as e:
        messagebox.showerror("DB", f"Failed to delete records: {e}")

def edit_student_name(id, new_first, new_last):
    nf = new_first.strip().title()
    nl = new_last.strip().title()
    try:
        with get_connection() as cnx:
            cur = cnx.cursor()
            cur.execute("SELECT id FROM students WHERE first_name=%s AND last_name=%s", (nf, nl))
            row = cur.fetchone()
            if row and row[0] != id:
                raise ValueError("Duplicate name exists.")
            cur.execute("UPDATE students SET first_name=%s, last_name=%s WHERE id=%s", (nf, nl, id))
            cnx.commit()
    except ValueError:
        raise
    except Exception as e:
        messagebox.showerror("DB", f"Failed to update name: {e}")

def attendance_summary(date_from, date_to):
    with get_connection() as cnx:
        cur = cnx.cursor()
        q = """
        SELECT DATE_FORMAT(a.date, '%Y-%m-%d') as date,
               SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) as present_count,
               COUNT(*) as total_count
        FROM attendance a
        WHERE a.date BETWEEN %s AND %s
        GROUP BY a.date
        ORDER BY a.date
        """
        cur.execute(q, (date_from, date_to))
        return cur.fetchall()

# --- Theming ---
DARK_PALETTE = {
    "bg": "#1f1f23",
    "bg2": "#2a2a31",
    "fg": "#f2f2f3",
    "muted": "#b8b8bf",
    "accent": "#4f8cff",
    "tree_alt": "#24242a",
}
LIGHT_PALETTE = {
    "bg": "#f7f7fb",
    "bg2": "#ffffff",
    "fg": "#222222",
    "muted": "#555555",
    "accent": "#2b6cb0",
    "tree_alt": "#f0f2f6",
}

def apply_theme(style: ttk.Style, theme_name: str):
    palette = DARK_PALETTE if theme_name == "dark" else LIGHT_PALETTE
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(".", background=palette["bg2"], foreground=palette["fg"], fieldbackground=palette["bg2"])
    style.configure("TFrame", background=palette["bg"])
    style.configure("TLabel", background=palette["bg"], foreground=palette["fg"])
    style.configure("TButton", padding=8)
    style.configure("TEntry", fieldbackground=palette["bg2"], foreground=palette["fg"])
    style.configure("TCombobox", fieldbackground=palette["bg2"], foreground=palette["fg"])
    style.configure("TNotebook", background=palette["bg"], tabmargins=[2,5,2,0])
    style.configure("TNotebook.Tab", padding=[10, 4])
    style.configure("Treeview",
                    background=palette["bg2"],
                    fieldbackground=palette["bg2"],
                    foreground=palette["fg"],
                    rowheight=26)
    style.map("Treeview",
              background=[("selected", palette["accent"])],
              foreground=[("selected", "#ffffff")])
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=palette["bg"], foreground=palette["fg"])
    style.configure("TSeparator", background=palette["muted"])

# --- App UI Classes ---
class LoginWindow:
    def __init__(self):
        ensure_dirs()
        init_config_if_missing()

        self.root = tk.Tk()
        self.root.title("Login - Attendance Register Pro")
        self.root.geometry("380x220")
        self.root.resizable(False, False)

        self.style = ttk.Style(self.root)
        cfg = load_config() or {}
        apply_theme(self.style, cfg.get("theme", "light"))

        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill=tk.BOTH, expand=True)

        ttk.Label(outer, text="Attendance Register Pro", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,8))

        form = ttk.Frame(outer)
        form.pack(fill=tk.X, expand=True)

        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w")
        self.username = ttk.Entry(form, width=30)
        self.username.grid(row=0, column=1, padx=(8,0), pady=(0,6))

        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w")
        self.password = ttk.Entry(form, width=30, show="*")
        self.password.grid(row=1, column=1, padx=(8,0), pady=(0,10))

        actions = ttk.Frame(outer)
        actions.pack(fill=tk.X)
        ttk.Button(actions, text="Login", command=self.login).pack(side=tk.LEFT)
        ttk.Button(actions, text="Change Password…", command=self.change_password).pack(side=tk.LEFT, padx=(8,0))

        self.username.focus_set()
        self.root.bind("<Return>", lambda e: self.login())
        self.root.mainloop()

    def change_password(self):
        cfg = load_config() or {}
        u = simpledialog.askstring("Change Password", "Confirm username:", parent=self.root)
        if not u:
            return
        if u != cfg.get("username"):
            messagebox.showerror("Error", "Username mismatch.")
            return
        cur_pwd = simpledialog.askstring("Change Password", "Current password:", show="*", parent=self.root)
        if not cur_pwd:
            return
        h, _ = hash_password(cur_pwd, cfg.get("salt", ""))
        if h != cfg.get("password_hash"):
            messagebox.showerror("Error", "Current password incorrect.")
            return
        new_pwd = simpledialog.askstring("Change Password", "New password:", show="*", parent=self.root)
        if not new_pwd:
            return
        h, s = hash_password(new_pwd)
        cfg["password_hash"] = h
        cfg["salt"] = s
        save_config(cfg)
        messagebox.showinfo("Success", "Password changed successfully.")

    def login(self):
        cfg = load_config() or {}
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Input", "Enter username and password.")
            return
        if user != cfg.get("username"):
            messagebox.showerror("Login Failed", "Invalid username or password")
            return
        h, _ = hash_password(pwd, cfg.get("salt", ""))
        if h == cfg.get("password_hash"):
            self.root.destroy()
            MainWindow()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Attendance Register Pro")
        self.root.geometry("1180x720")
        self.root.minsize(980, 560)
        self.apply_icon()

        # Theming
        self.style = ttk.Style(self.root)
        cfg = load_config() or {}
        self.theme = tk.StringVar(value=cfg.get("theme", "light"))
        apply_theme(self.style, self.theme.get())
        self._configure_menus_for_theme()

        # State
        self.date_var = tk.StringVar(value=ymd(today_date()))
        self.filter_name = tk.StringVar(value="")
        self.filter_status = tk.StringVar(value="All")
        self.status_var = tk.StringVar(value="Ready.")
        # For checkboxes in Take Attendance tab
        self.att_vars = {}  # student_id -> tk.IntVar()

        # Layout
        top = ttk.Frame(self.root, padding=(10,8))
        top.pack(fill=tk.X)

        ttk.Label(top, text="Date").grid(row=0, column=0, sticky="w")
        self.date_entry = ttk.Entry(top, textvariable=self.date_var, width=12)
        self.date_entry.grid(row=0, column=1, padx=(6,6))
        ttk.Button(top, text="Pick Date", command=self.pick_date).grid(row=0, column=2, padx=(0,10))

        ttk.Label(top, text="Search").grid(row=0, column=3, sticky="w")
        self.search_entry = ttk.Entry(top, textvariable=self.filter_name, width=24)
        self.search_entry.grid(row=0, column=4, padx=(6,6))

        ttk.Label(top, text="Status").grid(row=0, column=5, sticky="w")
        self.status_combo = ttk.Combobox(top, textvariable=self.filter_status, values=["All", "Present", "Absent"],
                                         width=12, state="readonly")
        self.status_combo.grid(row=0, column=6, padx=(6,6))
        self.status_combo.current(0)

        ttk.Button(top, text="Apply Filter", command=self.refresh_records).grid(row=0, column=7, padx=(6,6))
        ttk.Button(top, text="Reset", command=self.reset_filters).grid(row=0, column=8, padx=(0,10))

        ttk.Separator(top, orient="vertical").grid(row=0, column=9, sticky="ns", padx=8)

        ttk.Button(top, text="Add Student", command=self.add_student_dialog).grid(row=0, column=10, padx=(0,6))
        ttk.Button(top, text="Edit Selected", command=self.edit_record_dialog).grid(row=0, column=11, padx=(0,6))
        ttk.Button(top, text="Delete Selected", command=self.delete_selected).grid(row=0, column=12, padx=(0,6))

        ttk.Separator(top, orient="vertical").grid(row=0, column=13, sticky="ns", padx=8)
        self.theme_btn = ttk.Button(top, text="🌙 Dark" if self.theme.get()=="light" else "☀️ Light", command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=14)

        # Notebook: Take Attendance / Records
        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=(6,8))

        # Take Attendance tab
        self.tab_take = ttk.Frame(nb)
        nb.add(self.tab_take, text="Take Attendance")

        # Records tab
        self.tab_records = ttk.Frame(nb)
        nb.add(self.tab_records, text="Records")

        # --- Take Attendance UI ---
        ta_top = ttk.Frame(self.tab_take, padding=8)
        ta_top.pack(fill=tk.X)
        ttk.Label(ta_top, text="Mark present by checking the box. Click Save to apply.").pack(anchor="w")

        # Scrollable student list with checkboxes
        self.take_frame = ttk.Frame(self.tab_take, padding=8)
        self.take_frame.pack(fill=tk.BOTH, expand=True)

        self._create_take_attendance_scrollarea()

        ta_actions = ttk.Frame(self.tab_take, padding=(8,8))
        ta_actions.pack(fill=tk.X)
        ttk.Button(ta_actions, text="Select All", command=self.ta_select_all).pack(side=tk.LEFT)
        ttk.Button(ta_actions, text="Clear All", command=self.ta_clear_all).pack(side=tk.LEFT, padx=(6,0))
        ttk.Button(ta_actions, text="Save Attendance", command=self.ta_save).pack(side=tk.LEFT, padx=(12,0))
        ttk.Button(ta_actions, text="Export (CSV)", command=self.export_csv_current_date).pack(side=tk.RIGHT)

        # --- Records UI ---
        rec_top = ttk.Frame(self.tab_records, padding=8)
        rec_top.pack(fill=tk.X)
        ttk.Label(rec_top, text="Records (you can edit, toggle or delete rows)").pack(anchor="w")

        tree_frame = ttk.Frame(self.tab_records, padding=8)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.rec_y = ttk.Scrollbar(tree_frame, orient="vertical")
        self.rec_x = ttk.Scrollbar(tree_frame, orient="horizontal")

        columns = ("S/N", "First Name", "Last Name", "Status", "Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=self.rec_y.set, xscrollcommand=self.rec_x.set, selectmode="extended")
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
        self.tree.column("S/N", width=60, anchor="center")
        self.tree.column("First Name", width=180)
        self.tree.column("Last Name", width=180)
        self.tree.column("Status", width=110, anchor="center")
        self.tree.column("Date", width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.rec_y.config(command=self.tree.yview)
        self.rec_x.config(command=self.tree.xview)
        self.rec_y.grid(row=0, column=1, sticky="ns")
        self.rec_x.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Context menu for tree
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Toggle Attendance", command=self.toggle_selected)
        self.context_menu.add_command(label="Edit Selected", command=self.edit_record_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete Selected", command=self.delete_selected)
        self.tree.bind("<Button-3>", self._on_tree_right_click)
        self.tree.bind("<Double-1>", lambda e: self.toggle_selected())

        # Status and summary
        bottom = ttk.Frame(self.root)
        bottom.pack(fill=tk.X)
        self.summary_var = tk.StringVar(value="Summary: -")
        ttk.Label(bottom, textvariable=self.summary_var, font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(10,4))
        ttk.Label(bottom, textvariable=self.status_var).pack(side=tk.RIGHT, padx=(4,10))

        # Menus
        self.build_menu()

        # Shortcuts
        self.root.bind("<Control-s>", lambda e: self.save_session())
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        self.root.bind("<Control-f>", lambda e: self.search_entry.focus_set())
        self.root.bind("<Control-l>", lambda e: self.toggle_theme())

        # Initial load
        self.refresh_take_attendance()   # populates checkbox list for today's date
        self.refresh_records()           # populates tree

        self.root.mainloop()

    def apply_icon(self):
        try:
            self.root.iconbitmap("app.ico")
        except Exception:
            pass

    def _configure_menus_for_theme(self):
        try:
            palette = DARK_PALETTE if self.theme.get()=="dark" else LIGHT_PALETTE
            self.root.option_clear()
            self.root.option_add("*Menu*background", palette["bg2"])
            self.root.option_add("*Menu*foreground", palette["fg"])
            self.root.option_add("*Menu*activeBackground", palette["accent"])
            self.root.option_add("*Menu*activeForeground", "#ffffff")
        except Exception:
            pass

    def build_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Save Session\tCtrl+S", command=self.save_session, accelerator="Ctrl+S")
        file.add_separator()
        file.add_command(label="Export CSV", command=self.export_csv)
        file.add_command(label="Export Excel (.xlsx)", command=self.export_excel, state=("normal" if Workbook else "disabled"))
        file.add_command(label="Export PDF", command=self.export_pdf, state=("normal" if pdf_canvas else "disabled"))
        file.add_separator()
        file.add_command(label="Backup (marker)", command=self.backup_database)
        file.add_separator()
        file.add_command(label="Exit", command=self.root.quit)

        edit = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit)
        edit.add_command(label="Add Student", command=self.add_student_dialog)
        edit.add_command(label="Edit Selected", command=self.edit_record_dialog)
        edit.add_command(label="Toggle Attendance", command=self.toggle_selected)
        edit.add_command(label="Delete Selected", command=self.delete_selected, accelerator="Del")

        tools = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu=tools)
        tools.add_command(label="Attendance Report (Date Range)", command=self.analytics_dialog)
        tools.add_command(label="Change Password…", command=self._change_password_dialog)

        view = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view)
        view.add_command(label="Toggle Light/Dark\tCtrl+L", command=self.toggle_theme, accelerator="Ctrl+L")

        helpm = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpm)
        helpm.add_command(label="About", command=lambda: messagebox.showinfo("About", "Attendance Register Pro\nMySQL connected\nModern UI + Theme Toggle"))

    # --- Take Attendance scroll area creation ---
    def _create_take_attendance_scrollarea(self):
        # container with canvas + scrollbar
        outer = ttk.Frame(self.take_frame)
        outer.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(outer, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.ta_inner = ttk.Frame(canvas)
        # window inside canvas
        canvas.create_window((0,0), window=self.ta_inner, anchor="nw")
        def on_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.ta_inner.bind("<Configure>", on_config)

        # store canvas for potential programmatic scrolling
        self.ta_canvas = canvas

    # --- Take Attendance helpers ---
    def refresh_take_attendance(self):
        """Load students and show checkboxes reflecting existing attendance for date."""
        date = self._parse_date_or_alert()
        if date is None:
            return
        date_str = ymd(date)
        # Clear previous widgets & vars
        for w in self.ta_inner.winfo_children():
            w.destroy()
        self.att_vars.clear()

        students = list_students()
        att_map = fetch_attendance_map_for_date(date_str)  # student_id -> (att_id, status)

        # Build rows: a checkbutton per student
        for sid, first, last in students:
            var = tk.IntVar(value=1 if (sid in att_map and att_map[sid][1] == "Present") else 0)
            self.att_vars[sid] = var
            row = ttk.Frame(self.ta_inner, padding=(4,4))
            row.pack(fill=tk.X, expand=True)
            cb = ttk.Checkbutton(row, text=f"{first} {last}", variable=var)
            cb.pack(side=tk.LEFT, anchor="w")

        self.status_var.set(f"Loaded {len(students)} students for {date_str}")

    def ta_select_all(self):
        for v in self.att_vars.values():
            v.set(1)

    def ta_clear_all(self):
        for v in self.att_vars.values():
            v.set(0)

    def ta_save(self):
        date = self._parse_date_or_alert()
        if date is None:
            return
        date_str = ymd(date)
        count = 0
        for sid, var in self.att_vars.items():
            status = "Present" if var.get() else "Absent"
            upsert_attendance(sid, date_str, status)
            count += 1
        self.status_var.set(f"Saved attendance for {count} students on {date_str}")
        self.refresh_records()

    def export_csv_current_date(self):
        date = self._parse_date_or_alert()
        if date is None:
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], title="Export Current Day CSV")
        if not file:
            return
        rows = fetch_attendance(ymd(date))
        try:
            with open(file, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["First Name","Last Name","Status","Date"])
                for att_id, sid, first, last, st, d in rows:
                    w.writerow([first, last, st, d])
            messagebox.showinfo("Export", f"Exported {len(rows)} rows to {file}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export: {e}")

    # --- Records (tree) ---
    def refresh_records(self):
        date = self._parse_date_or_alert()
        if date is None:
            return
        date_str = ymd(date)
        qname = self.filter_name.get().strip()
        status = self.filter_status.get()
        status = None if status == "All" else status
        rows = fetch_attendance(date_str, qname, status)
        # clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, row in enumerate(rows, start=1):
            att_id, sid, first, last, st, d = row
            self.tree.insert("", "end", iid=str(att_id), values=(idx, first, last, st, d))
        self.status_var.set(f"Loaded {len(rows)} record(s) for {date_str}")
        self.update_summary()

    def _on_tree_right_click(self, event):
        try:
            sel = self.tree.identify_row(event.y)
            if sel:
                self.tree.selection_set(sel)
                self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def toggle_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Toggle", "Select rows to toggle.")
            return
        toggled = 0
        for iid in sel:
            att_id = int(iid)
            try:
                with get_connection() as cnx:
                    cur = cnx.cursor()
                    cur.execute("SELECT student_id, date, status FROM attendance WHERE id=%s", (att_id,))
                    row = cur.fetchone()
            except Exception as e:
                messagebox.showerror("DB", f"Failed to fetch record: {e}")
                continue
            if not row:
                continue
            sid, date_str, status = row
            new_status = "Absent" if status == "Present" else "Present"
            upsert_attendance(sid, date_str, new_status)
            toggled += 1
        if toggled:
            self.status_var.set(f"Toggled {toggled} record(s).")
        self.refresh_records()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Delete", "Select rows to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete {len(sel)} selected record(s)?"):
            return
        ids = [int(i) for i in sel]
        delete_attendance_rows(ids)
        self.refresh_records()
        self.status_var.set("Deleted selected record(s).")

    # --- Add / Edit student / record dialogs ---
    def add_student_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add Student")
        dlg.geometry("360x180")
        frm = ttk.Frame(dlg, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="First Name").grid(row=0, column=0, sticky="w")
        e1 = ttk.Entry(frm, width=28)
        e1.grid(row=0, column=1, padx=(8,0))
        ttk.Label(frm, text="Last Name").grid(row=1, column=0, sticky="w", pady=(8,0))
        e2 = ttk.Entry(frm, width=28)
        e2.grid(row=1, column=1, padx=(8,0), pady=(8,0))

        def submit():
            first = e1.get().strip().title()
            last = e2.get().strip().title()
            if not first or not last:
                messagebox.showwarning("Input", "Both names required.", parent=dlg)
                return
            sid = add_student_db(first, last)
            if sid is None:
                # maybe exists -> show helpful message
                sid = get_student_id(first, last)
                if sid is None:
                    messagebox.showerror("DB", "Failed to add or find student.", parent=dlg)
                    return
                else:
                    messagebox.showinfo("Exists", f"Student already exists: {first} {last}", parent=dlg)
            dlg.destroy()
            # refresh take attendance list so teacher doesn't have to reopen tab
            self.refresh_take_attendance()

        ttk.Button(frm, text="Add", command=submit).grid(row=3, column=0, pady=(14,0))
        ttk.Button(frm, text="Cancel", command=dlg.destroy).grid(row=3, column=1, pady=(14,0))

    def edit_record_dialog(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edit", "Select a single record to edit.")
            return
        if len(sel) > 1:
            messagebox.showinfo("Edit", "Please edit one record at a time.")
            return
        att_id = int(sel[0])
        try:
            with get_connection() as cnx:
                cur = cnx.cursor()
                cur.execute("""
                    SELECT a.id, s.id, s.first_name, s.last_name, a.date, a.status
                    FROM attendance a JOIN students s ON s.id = a.student_id
                    WHERE a.id=%s
                """, (att_id,))
                row = cur.fetchone()
        except Exception as e:
            messagebox.showerror("DB", f"Failed to fetch record: {e}")
            return
        if not row:
            messagebox.showerror("Edit", "Record not found.")
            return
        _, sid, first, last, date_str, status = row

        dlg = tk.Toplevel(self.root)
        dlg.title("Edit Record")
        frm = ttk.Frame(dlg, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="First Name").grid(row=0, column=0, sticky="w")
        e1 = ttk.Entry(frm, width=28)
        e1.insert(0, first)
        e1.grid(row=0, column=1, padx=(8,0))
        ttk.Label(frm, text="Last Name").grid(row=1, column=0, sticky="w")
        e2 = ttk.Entry(frm, width=28)
        e2.insert(0, last)
        e2.grid(row=1, column=1, padx=(8,0))
        ttk.Label(frm, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=(8,0))
        e_date = ttk.Entry(frm, width=28)
        e_date.insert(0, date_str)
        e_date.grid(row=2, column=1, padx=(8,0))
        ttk.Label(frm, text="Status").grid(row=3, column=0, sticky="w", pady=(8,0))
        cb = ttk.Combobox(frm, values=["Present", "Absent"], state="readonly", width=26)
        cb.set(status)
        cb.grid(row=3, column=1, padx=(8,0))

        def save_changes():
            nf = e1.get().strip().title()
            nl = e2.get().strip().title()
            nd = e_date.get().strip()
            new_status = cb.get()
            if not nf or not nl:
                messagebox.showwarning("Input", "Both names required.", parent=dlg)
                return
            try:
                dt.datetime.strptime(nd, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Date", "Enter valid date YYYY-MM-DD", parent=dlg)
                return
            # update student name, then upsert attendance
            try:
                edit_student_name(sid, nf, nl)
            except ValueError as ve:
                messagebox.showerror("Duplicate", str(ve), parent=dlg)
                return
            upsert_attendance(sid, nd, new_status)
            dlg.destroy()
            self.refresh_take_attendance()
            self.refresh_records()
            self.status_var.set("Record updated.")

        ttk.Button(frm, text="Save", command=save_changes).grid(row=4, column=0, pady=(12,0))
        ttk.Button(frm, text="Cancel", command=dlg.destroy).grid(row=4, column=1, pady=(12,0))

    # --- Date helpers ---
    def pick_date(self):
        if Calendar:
            win = tk.Toplevel(self.root)
            win.title("Pick Date")
            cal = Calendar(win, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(padx=8, pady=8)
            def set_date():
                self.date_var.set(cal.get_date())
                win.destroy()
                self.refresh_take_attendance()
                self.refresh_records()
            ttk.Button(win, text="Select", command=set_date).pack(pady=(6,8))
        else:
            messagebox.showinfo("Date", "tkcalendar not installed. Type date as YYYY-MM-DD.")

    def _parse_date_or_alert(self):
        txt = self.date_var.get().strip()
        try:
            d = dt.datetime.strptime(txt, "%Y-%m-%d").date()
            return d
        except Exception:
            messagebox.showerror("Date", "Enter date as YYYY-MM-DD")
            return None

    def reset_filters(self):
        self.filter_name.set("")
        self.filter_status.set("All")
        self.date_var.set(ymd(today_date()))
        self.refresh_take_attendance()
        self.refresh_records()

    # --- Theme toggle ---
    def toggle_theme(self):
        new = "dark" if self.theme.get()=="light" else "light"
        self.theme.set(new)
        apply_theme(self.style, new)
        self._configure_menus_for_theme()
        self.theme_btn.config(text="🌙 Dark" if new=="light" else "☀️ Light")
        cfg = load_config() or {}
        cfg["theme"] = new
        save_config(cfg)

    # --- Sorting / summary ---
    def sort_column(self, col):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        if col == "S/N":
            try:
                data.sort(key=lambda t: int(t[0]))
            except Exception:
                data.sort(key=lambda t: str(t[0]).lower())
        else:
            data.sort(key=lambda t: str(t[0]).lower())
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)

    def update_summary(self):
        date = self._parse_date_or_alert()
        if date is None:
            return
        rows = fetch_attendance(ymd(date))
        total = len(rows)
        present = sum(1 for r in rows if r[4] == "Present")
        pct = (present / total * 100) if total else 0
        self.summary_var.set(f"Summary: {present}/{total} present ({pct:.1f}%)")

    # --- Reports & exports ---
    def analytics_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Attendance Report (Date Range)")
        frm = ttk.Frame(dlg, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="From (YYYY-MM-DD)").grid(row=0, column=0, sticky="w")
        e_from = ttk.Entry(frm, width=14)
        e_from.insert(0, ymd(today_date() - dt.timedelta(days=7)))
        e_from.grid(row=0, column=1, padx=(8,0))
        ttk.Label(frm, text="To (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        e_to = ttk.Entry(frm, width=14)
        e_to.insert(0, ymd(today_date()))
        e_to.grid(row=1, column=1, padx=(8,0))

        def show_report():
            try:
                d1 = dt.datetime.strptime(e_from.get().strip(), "%Y-%m-%d").date()
                d2 = dt.datetime.strptime(e_to.get().strip(), "%Y-%m-%d").date()
            except Exception:
                messagebox.showerror("Date", "Enter valid dates YYYY-MM-DD", parent=dlg)
                return
            rows = attendance_summary(ymd(d1), ymd(d2))
            rep = tk.Toplevel(dlg)
            rep.title("Report")
            text = tk.Text(rep, width=60, height=20)
            text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            if not rows:
                text.insert(tk.END, "No data for this range.\n")
                return
            for date_str, present_count, total in rows:
                pct = (present_count/total*100) if total else 0
                text.insert(tk.END, f"{date_str}: {present_count}/{total} Present ({pct:.1f}%)\n")
            if plt:
                try:
                    x = [r[0] for r in rows]
                    y = [(r[1]/r[2]*100) if r[2] else 0 for r in rows]
                    plt.figure()
                    plt.plot(x, y, marker="o")
                    plt.title("Attendance % by Date")
                    plt.xlabel("Date")
                    plt.ylabel("Present (%)")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    plt.show()
                except Exception:
                    pass

        ttk.Button(frm, text="Generate", command=show_report).grid(row=2, column=0, pady=(12,0))
        ttk.Button(frm, text="Close", command=dlg.destroy).grid(row=2, column=1, pady=(12,0))

    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not file:
            return
        date = self._parse_date_or_alert()
        if date is None:
            return
        rows = fetch_attendance(ymd(date), self.filter_name.get().strip(),
                                None if self.filter_status.get()=="All" else self.filter_status.get())
        try:
            with open(file, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["First Name","Last Name","Status","Date"])
                for att_id, sid, first, last, st, d in rows:
                    w.writerow([first, last, st, d])
            messagebox.showinfo("Export", f"Exported {len(rows)} rows to {file}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to export: {e}")

    def export_excel(self):
        if not Workbook:
            messagebox.showerror("Excel", "openpyxl not installed.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Workbook","*.xlsx")])
        if not file:
            return
        date = self._parse_date_or_alert()
        if date is None:
            return
        rows = fetch_attendance(ymd(date), self.filter_name.get().strip(),
                                None if self.filter_status.get()=="All" else self.filter_status.get())
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance"
        ws.append(["First Name","Last Name","Status","Date"])
        for _, _, first, last, st, d in rows:
            ws.append([first, last, st, d])
        try:
            wb.save(file)
            messagebox.showinfo("Export", f"Exported to {file}")
        except Exception as e:
            messagebox.showerror("Export", f"Failed to save Excel: {e}")

    def export_pdf(self):
        if not pdf_canvas:
            messagebox.showerror("PDF", "reportlab not installed.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
        if not file:
            return
        date = self._parse_date_or_alert()
        if date is None:
            return
        rows = fetch_attendance(ymd(date), self.filter_name.get().strip(),
                                None if self.filter_status.get()=="All" else self.filter_status.get())
        try:
            c = pdf_canvas.Canvas(file, pagesize=A4)
            width, height = A4
            x, y = 40, height - 40
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x, y, "Attendance Export")
            y -= 20
            c.setFont("Helvetica", 10)
            c.drawString(x, y, f"Generated: {now_str()}")
            y -= 20
            c.drawString(x, y, f"Date: {self.date_var.get()} | Status: {self.filter_status.get()} | Name: {self.filter_name.get().strip()}")
            y -= 30
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x, y, "First Name")
            c.drawString(x+160, y, "Last Name")
            c.drawString(x+320, y, "Status")
            c.drawString(x+420, y, "Date")
            y -= 14
            c.setFont("Helvetica", 10)
            for _, _, first, last, st, d in rows:
                if y < 60:
                    c.showPage()
                    y = height - 40
                    c.setFont("Helvetica", 10)
                c.drawString(x, y, first)
                c.drawString(x+160, y, last)
                c.drawString(x+320, y, st)
                c.drawString(x+420, y, d)
                y -= 14
            c.showPage()
            c.save()
            messagebox.showinfo("Export", f"Exported to {file}")
        except Exception as e:
            messagebox.showerror("PDF", f"Failed to export PDF: {e}")

    # --- Save / backup / sessions ---
    def save_session(self):
        sid = bump_session_id()
        try:
            with get_connection() as cnx:
                cur = cnx.cursor()
                cur.execute("INSERT INTO sessions (label, created_at) VALUES (%s, %s)", (f"Session {sid}", now_str()))
                cnx.commit()
            self.status_var.set(f"Saved session #{sid}")
            messagebox.showinfo("Saved", f"Saved session #{sid}")
        except Exception as e:
            messagebox.showerror("DB", f"Failed to save session: {e}")

    def backup_database(self):
        # Since making a physical MySQL dump is out of scope here, we create a session marker
        try:
            sid = bump_session_id()
            with get_connection() as cnx:
                cur = cnx.cursor()
                cur.execute("INSERT INTO sessions (label, created_at) VALUES (%s, %s)", (f"Backup {sid}", now_str()))
                cnx.commit()
            messagebox.showinfo("Backup", f"Created backup session record #{sid}")
            self.status_var.set(f"Backup session created -> {sid}")
        except Exception as e:
            messagebox.showerror("Backup", f"Backup failed: {e}")

    # --- Misc security helper ---
    def _change_password_dialog(self):
        cfg = load_config() or {}
        cur_pwd = simpledialog.askstring("Change Password", "Current password:", show="*", parent=self.root)
        if not cur_pwd:
            return
        h, _ = hash_password(cur_pwd, cfg.get("salt", ""))
        if h != cfg.get("password_hash"):
            messagebox.showerror("Error", "Current password incorrect.")
            return
        new_pwd = simpledialog.askstring("Change Password", "New password:", show="*", parent=self.root)
        if not new_pwd:
            return
        h, s = hash_password(new_pwd)
        cfg["password_hash"] = h
        cfg["salt"] = s
        save_config(cfg)
        messagebox.showinfo("Success", "Password changed successfully.")

# --- Bootstrap ---
def main():
    ensure_dirs()
    init_config_if_missing()
    if mysql is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Missing Dependency",
                             f"mysql-connector-python is required.\nInstall with:\n\npip install mysql-connector-python\n\nError: {mysql_connector_error}")
        root.destroy()
        return
    try:
        init_db_mysql()
    except Exception:
        return
    LoginWindow()

if __name__ == "__main__":
    main()