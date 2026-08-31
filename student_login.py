import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import os

# =========================================================
# SETTINGS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "student.db")


# =========================================================
# STUDENT LOGIN WINDOW
# =========================================================

class StudentLoginWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Student Login")
        self.geometry("500x550")
        self.minsize(450, 500)

        self.configure(fg_color="#F5F7FB")

        self.create_ui()

        self.bind("<Return>", lambda event: self.login_student())

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            height=120,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🎓 Student Portal",
            text_color="white",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Student Login",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=14
            )
        )

        subtitle.pack()

        # -------------------------------------------------
        # LOGIN CARD
        # -------------------------------------------------

        card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=35
        )

        heading = ctk.CTkLabel(
            card,
            text="Welcome Back!",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        heading.pack(
            pady=(30, 5)
        )

        info = ctk.CTkLabel(
            card,
            text="Login using your Student ID and phone number",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12
            )
        )

        info.pack(
            pady=(0, 25)
        )

        # -------------------------------------------------
        # STUDENT ID
        # -------------------------------------------------

        id_label = ctk.CTkLabel(
            card,
            text="Student ID",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        id_label.pack(
            anchor="w",
            padx=35
        )

        self.student_id_entry = ctk.CTkEntry(
            card,
            height=42,
            corner_radius=8,
            placeholder_text="Example: ST001"
        )

        self.student_id_entry.pack(
            fill="x",
            padx=35,
            pady=(5, 18)
        )

        # -------------------------------------------------
        # PHONE
        # -------------------------------------------------

        phone_label = ctk.CTkLabel(
            card,
            text="Phone Number",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        phone_label.pack(
            anchor="w",
            padx=35
        )

        self.phone_entry = ctk.CTkEntry(
            card,
            height=42,
            corner_radius=8,
            placeholder_text="Enter registered phone number",
            show="*"
        )

        self.phone_entry.pack(
            fill="x",
            padx=35,
            pady=(5, 25)
        )

        # -------------------------------------------------
        # LOGIN BUTTON
        # -------------------------------------------------

        login_button = ctk.CTkButton(
            card,
            text="🔐  Login",
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.login_student
        )

        login_button.pack(
            fill="x",
            padx=35,
            pady=(0, 10)
        )

        # -------------------------------------------------
        # CLEAR BUTTON
        # -------------------------------------------------

        clear_button = ctk.CTkButton(
            card,
            text="Clear",
            height=40,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.clear_fields
        )

        clear_button.pack(
            fill="x",
            padx=35
        )

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------

        footer = ctk.CTkLabel(
            card,
            text="Student Management System",
            text_color="#94A3B8",
            font=ctk.CTkFont(
                size=11
            )
        )

        footer.pack(
            pady=(25, 15)
        )

    # =====================================================
    # LOGIN
    # =====================================================

    def login_student(self):

        student_id = self.student_id_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not student_id:

            messagebox.showwarning(
                "Login",
                "Please enter your Student ID.",
                parent=self
            )

            self.student_id_entry.focus()
            return

        if not phone:

            messagebox.showwarning(
                "Login",
                "Please enter your phone number.",
                parent=self
            )

            self.phone_entry.focus()
            return

        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    student_id,
                    name,
                    phone
                FROM students
                WHERE student_id = ?
                AND phone = ?
                """,
                (
                    student_id,
                    phone
                )
            )

            student = cursor.fetchone()

            conn.close()

            if not student:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid Student ID or phone number.",
                    parent=self
                )

                return

            database_id = student[0]

            # -------------------------------------------------
            # OPEN STUDENT PORTAL
            # -------------------------------------------------

            try:

                import student_portal

                self.withdraw()

                student_portal.open_student_portal(
                    database_id,
                    self
                )

            except Exception as e:

                self.deiconify()

                messagebox.showerror(
                    "Student Portal Error",
                    f"Unable to open Student Portal.\n\n{e}",
                    parent=self
                )

        except sqlite3.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to access student database.\n\n{e}",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Login Error",
                str(e),
                parent=self
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_fields(self):

        self.student_id_entry.delete(
            0,
            "end"
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.student_id_entry.focus()


# =========================================================
# OPEN LOGIN
# =========================================================

def open_student_login():

    app = StudentLoginWindow()

    app.mainloop()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    open_student_login()