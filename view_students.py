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
# VIEW STUDENTS WINDOW
# =========================================================

class ViewStudentsWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.title("View Students")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()
        self.load_students()

        if parent:
            self.transient(parent)

        self.focus_force()

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self,
            height=90,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="👨‍🎓  View Students",
            text_color="white",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        title.pack(
            side="left",
            padx=30
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Manage registered students",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        )

        subtitle.pack(
            side="left"
        )

        # -------------------------------------------------
        # SEARCH BAR
        # -------------------------------------------------

        search_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        search_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=42,
            corner_radius=8,
            placeholder_text="🔍 Search by Student ID, Name or Course..."
        )

        self.search_entry.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=15,
            sticky="ew"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_students()
        )

        search_button = ctk.CTkButton(
            search_frame,
            text="🔍 Search",
            width=100,
            height=42,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.search_students
        )

        search_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=15
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="⟳ Refresh",
            width=100,
            height=42,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.load_students
        )

        refresh_button.grid(
            row=0,
            column=2,
            padx=(5, 15),
            pady=15
        )

        # -------------------------------------------------
        # TABLE CONTAINER
        # -------------------------------------------------

        container = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        self.table = ctk.CTkScrollableFrame(
            container,
            fg_color="white"
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # TABLE HEADERS
        # -------------------------------------------------

        headers = [
            ("ID", 60),
            ("Student ID", 120),
            ("Name", 180),
            ("Gender", 100),
            ("Course", 190),
            ("Year", 110),
            ("Actions", 210)
        ]

        for column, (text, width) in enumerate(headers):

            label = ctk.CTkLabel(
                self.table,
                text=text,
                width=width,
                height=40,
                fg_color="#E2E8F0",
                text_color="#0F172A",
                corner_radius=5,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=column,
                padx=2,
                pady=2
            )

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students(self):

        self.clear_rows()

        try:

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    name,
                    gender,
                    course,
                    year
                FROM students
                ORDER BY id DESC
            """)

            students = cursor.fetchall()

            conn.close()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}",
                parent=self
            )

    # =====================================================
    # SEARCH STUDENTS
    # =====================================================

    def search_students(self):

        search_text = self.search_entry.get().strip()

        self.clear_rows()

        try:

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            if search_text:

                value = f"%{search_text}%"

                cursor.execute("""
                    SELECT
                        id,
                        student_id,
                        name,
                        gender,
                        course,
                        year
                    FROM students
                    WHERE
                        student_id LIKE ?
                        OR name LIKE ?
                        OR course LIKE ?
                    ORDER BY id DESC
                """, (
                    value,
                    value,
                    value
                ))

            else:

                cursor.execute("""
                    SELECT
                        id,
                        student_id,
                        name,
                        gender,
                        course,
                        year
                    FROM students
                    ORDER BY id DESC
                """)

            students = cursor.fetchall()

            conn.close()

            self.display_students(students)

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Unable to search students.\n\n{e}",
                parent=self
            )

    # =====================================================
    # DISPLAY STUDENTS
    # =====================================================

    def display_students(self, students):

        if not students:

            no_data = ctk.CTkLabel(
                self.table,
                text="No students found.",
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=15
                )
            )

            no_data.grid(
                row=1,
                column=0,
                columnspan=7,
                pady=50
            )

            return

        for row_number, student in enumerate(
            students,
            start=1
        ):

            (
                database_id,
                student_id,
                name,
                gender,
                course,
                year
            ) = student

            values = [
                database_id,
                student_id or "",
                name or "",
                gender or "",
                course or "",
                year or ""
            ]

            widths = [
                60,
                120,
                180,
                100,
                190,
                110
            ]

            # -------------------------------------------------
            # DATA
            # -------------------------------------------------

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.table,
                    text=str(value),
                    width=widths[column],
                    height=42,
                    fg_color=(
                        "#F8FAFC"
                        if row_number % 2 == 0
                        else "white"
                    ),
                    text_color="#334155",
                    anchor="w"
                )

                label.grid(
                    row=row_number,
                    column=column,
                    padx=2,
                    pady=2
                )

            # -------------------------------------------------
            # ACTION FRAME
            # -------------------------------------------------

            action_frame = ctk.CTkFrame(
                self.table,
                width=200,
                height=42,
                fg_color="transparent"
            )

            action_frame.grid(
                row=row_number,
                column=6,
                padx=3,
                pady=3
            )

            action_frame.pack_propagate(False)

            # -------------------------------------------------
            # EDIT BUTTON
            # -------------------------------------------------

            edit_button = ctk.CTkButton(
                action_frame,
                text="✏️ Edit",
                width=85,
                height=32,
                corner_radius=6,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                command=lambda sid=database_id:
                self.edit_student(sid)
            )

            edit_button.pack(
                side="left",
                padx=3
            )

            # -------------------------------------------------
            # PROFILE BUTTON
            # -------------------------------------------------

            profile_button = ctk.CTkButton(
                action_frame,
                text="👤 Profile",
                width=90,
                height=32,
                corner_radius=6,
                fg_color="#7C3AED",
                hover_color="#6D28D9",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                command=lambda sid=database_id:
                self.open_profile(sid)
            )

            profile_button.pack(
                side="left",
                padx=3
            )

    # =====================================================
    # EDIT STUDENT
    # =====================================================

    def edit_student(self, student_id):

        try:

            import update_student

            update_student.open_update_student(
                student_id,
                self
            )

            # Refresh after closing update window
            self.wait_window(
                self.winfo_children()[-1]
            )

            self.load_students()

        except Exception as e:

            messagebox.showerror(
                "Update Error",
                f"Unable to open update student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # OPEN PROFILE
    # =====================================================

    def open_profile(self, student_id):

        try:

            import student_profile

            student_profile.open_student_profile(
                student_id,
                self
            )

        except Exception as e:

            messagebox.showerror(
                "Profile Error",
                f"Unable to open student profile.\n\n{e}",
                parent=self
            )

    # =====================================================
    # CLEAR TABLE
    # =====================================================

    def clear_rows(self):

        for widget in self.table.winfo_children():

            try:

                row = int(
                    widget.grid_info()["row"]
                )

                if row > 0:
                    widget.destroy()

            except Exception:
                pass


# =========================================================
# OPEN FUNCTION
# =========================================================

def open_view_students(parent=None):

    window = ViewStudentsWindow(parent)

    window.focus_force()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    window = ViewStudentsWindow(app)

    app.mainloop()