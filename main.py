import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox


# =========================================================
# SETTINGS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "student.db")


# =========================================================
# APPEARANCE
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =========================================================
# LOGIN WINDOW
# =========================================================

class LoginWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Student Management System - Login"
        )

        self.geometry(
            "1000x650"
        )

        self.minsize(
            850,
            550
        )

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # =================================================
        # LEFT PANEL
        # =================================================

        left = ctk.CTkFrame(
            self,
            width=430,
            corner_radius=0,
            fg_color="#0F172A"
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="🎓",
            text_color="white",
            font=ctk.CTkFont(
                size=70
            )
        ).pack(
            pady=(100, 10)
        )

        ctk.CTkLabel(
            left,
            text="Student\nManagement System",
            text_color="white",
            justify="center",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack()

        ctk.CTkLabel(
            left,
            text=(
                "Manage students,\n"
                "attendance, events\n"
                "and announcements"
            ),
            text_color="#CBD5E1",
            justify="center",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=20
        )

        # =================================================
        # RIGHT PANEL
        # =================================================

        right = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=0
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            right,
            text="Welcome Back!",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            pady=(80, 5)
        )

        ctk.CTkLabel(
            right,
            text="Login to continue",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=(0, 30)
        )

        # =================================================
        # LOGIN AS
        # =================================================

        ctk.CTkLabel(
            right,
            text="Login As",
            text_color="#334155",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=70
        )

        self.role_combo = ctk.CTkComboBox(
            right,
            values=[
                "Admin",
                "Student"
            ],
            height=45,
            corner_radius=8
        )

        self.role_combo.pack(
            fill="x",
            padx=70,
            pady=(5, 15)
        )

        self.role_combo.set(
            "Admin"
        )

        # =================================================
        # USERNAME
        # =================================================

        ctk.CTkLabel(
            right,
            text="Username",
            text_color="#334155",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=70
        )

        self.username_entry = ctk.CTkEntry(
            right,
            height=45,
            corner_radius=8,
            placeholder_text="Enter username"
        )

        self.username_entry.pack(
            fill="x",
            padx=70,
            pady=(5, 15)
        )

        # =================================================
        # PASSWORD
        # =================================================

        ctk.CTkLabel(
            right,
            text="Password",
            text_color="#334155",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=70
        )

        self.password_entry = ctk.CTkEntry(
            right,
            height=45,
            corner_radius=8,
            placeholder_text="Enter password",
            show="*"
        )

        self.password_entry.pack(
            fill="x",
            padx=70,
            pady=(5, 20)
        )

        # =================================================
        # LOGIN BUTTON
        # =================================================

        ctk.CTkButton(
            right,
            text="🔐 Login",
            height=48,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.login
        ).pack(
            fill="x",
            padx=70
        )

        # =================================================
        # DEFAULT ADMIN
        # =================================================

        ctk.CTkLabel(
            right,
            text="Admin Login: admin / admin123",
            text_color="#94A3B8",
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            pady=20
        )

        # =================================================
        # ENTER KEY
        # =================================================

        self.bind(
            "<Return>",
            lambda event: self.login()
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        role = (
            self.role_combo
            .get()
            .strip()
            .lower()
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not username:

            messagebox.showwarning(
                "Login",
                "Please enter username.",
                parent=self
            )

            return

        if not password:

            messagebox.showwarning(
                "Login",
                "Please enter password.",
                parent=self
            )

            return

        # =================================================
        # ADMIN LOGIN
        # =================================================

        if role == "admin":

            if (
                username == "admin"
                and password == "admin123"
            ):

                self.open_admin_dashboard()

            else:

                messagebox.showerror(
                    "Admin Login Failed",
                    "Invalid Admin username or password.",
                    parent=self
                )

            return

        # =================================================
        # STUDENT LOGIN
        # =================================================

        if role == "student":

            self.login_student(
                username,
                password
            )

            return

        # =================================================
        # INVALID ROLE
        # =================================================

        messagebox.showerror(
            "Login",
            "Invalid login type.",
            parent=self
        )

    # =====================================================
    # OPEN ADMIN DASHBOARD
    # =====================================================

    def open_admin_dashboard(self):

        try:

            # Import your working dashboard
            import dashboard

            # Close login window
            self.destroy()

            # Start the exact same dashboard
            # that worked with python dashboard.py
            dashboard.open_dashboard(
                "Admin"
            )

        except Exception as e:

            messagebox.showerror(
                "Dashboard Error",
                f"Unable to open Dashboard.\n\n{e}"
            )

    # =====================================================
    # STUDENT LOGIN
    # =====================================================

    def login_student(
        self,
        username,
        password
    ):

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            # -------------------------------------------------
            # CHECK USERS TABLE
            # -------------------------------------------------

            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='users'
            """)

            table = cursor.fetchone()

            if table is None:

                conn.close()

                messagebox.showerror(
                    "Student Login",
                    "Student login table was not found.",
                    parent=self
                )

                return

            # -------------------------------------------------
            # CHECK STUDENT
            # -------------------------------------------------

            cursor.execute("""
                SELECT
                    student_id
                FROM users
                WHERE username = ?
                AND password = ?
                AND LOWER(role) = 'student'
            """, (
                username,
                password
            ))

            result = cursor.fetchone()

            conn.close()

            if result is None:

                messagebox.showerror(
                    "Student Login Failed",
                    "Invalid student username or password.",
                    parent=self
                )

                return

            student_id = result[0]

            if student_id is None:

                messagebox.showerror(
                    "Student Login",
                    "This student account is not linked "
                    "to a student record.",
                    parent=self
                )

                return

            # Open portal
            self.open_student_portal(
                student_id
            )

        except Exception as e:

            messagebox.showerror(
                "Student Login Error",
                str(e),
                parent=self
            )

    # =====================================================
    # OPEN STUDENT PORTAL
    # =====================================================

    def open_student_portal(
        self,
        student_id
    ):

        try:

            import student_portal

            self.destroy()

            portal = (
                student_portal.StudentPortalWindow(
                    parent=None,
                    database_id=student_id
                )
            )

            portal.mainloop()

        except Exception as e:

            messagebox.showerror(
                "Student Portal Error",
                f"Unable to open Student Portal.\n\n{e}"
            )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app = LoginWindow()

    app.mainloop()