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
# THEME
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =========================================================
# DATABASE
# =========================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


def setup_attendance_table():

    conn = get_connection()
    cursor = conn.cursor()

    # Create attendance table only if it does not exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Make sure the table exists.
setup_attendance_table()


# =========================================================
# ATTENDANCE WINDOW
# =========================================================

class AttendanceWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent=None,
        database_id=None
    ):

        super().__init__(parent)

        self.parent = parent
        self.database_id = database_id

        self.title("Attendance")

        self.geometry("1100x720")

        self.minsize(
            900,
            600
        )

        self.configure(
            fg_color="#F5F7FB"
        )

        self.selected_student_id = None

        self.create_ui()

        if self.database_id is not None:

            # Student Portal mode
            self.load_student_attendance()

        else:

            # Admin mode
            self.load_students()

        if parent:

            self.transient(parent)

        self.focus_force()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =====================================================
    # UI
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

        title_text = (
            "📊  My Attendance"
            if self.database_id is not None
            else "📊  Attendance Management"
        )

        title = ctk.CTkLabel(
            header,
            text=title_text,
            text_color="white",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        )

        title.pack(
            side="left",
            padx=30
        )

        subtitle_text = (
            "View your attendance"
            if self.database_id is not None
            else "Manage student attendance"
        )

        subtitle = ctk.CTkLabel(
            header,
            text=subtitle_text,
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        )

        subtitle.pack(
            side="left",
            padx=10
        )

        # -------------------------------------------------
        # MAIN SCROLL
        # -------------------------------------------------

        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # -------------------------------------------------
        # STUDENT SELECTION
        # -------------------------------------------------

        if self.database_id is None:

            self.create_admin_selection()

        # -------------------------------------------------
        # STUDENT INFORMATION
        # -------------------------------------------------

        self.student_card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15
        )

        self.student_card.pack(
            fill="x",
            padx=5,
            pady=(5, 15)
        )

        self.student_name_label = ctk.CTkLabel(
            self.student_card,
            text="Select a student",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.student_name_label.pack(
            anchor="w",
            padx=25,
            pady=(18, 3)
        )

        self.student_details_label = ctk.CTkLabel(
            self.student_card,
            text="",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.student_details_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        # -------------------------------------------------
        # STATISTICS TITLE
        # -------------------------------------------------

        stats_title = ctk.CTkLabel(
            self.main,
            text="Attendance Summary",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        stats_title.pack(
            anchor="w",
            padx=10,
            pady=(5, 10)
        )

        # -------------------------------------------------
        # STATISTICS FRAME
        # -------------------------------------------------

        self.stats_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        self.stats_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 20)
        )

        for column in range(4):

            self.stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # IMPORTANT:
        # create_stat_card requires:
        # parent, title, value, column

        self.total_value = self.create_stat_card(
            self.stats_frame,
            "Total Classes",
            0,
            0
        )

        self.present_value = self.create_stat_card(
            self.stats_frame,
            "Present",
            0,
            1
        )

        self.absent_value = self.create_stat_card(
            self.stats_frame,
            "Absent",
            0,
            2
        )

        self.percentage_value = self.create_stat_card(
            self.stats_frame,
            "Attendance %",
            "0.00%",
            3
        )

        # -------------------------------------------------
        # ADMIN MARK ATTENDANCE
        # -------------------------------------------------

        if self.database_id is None:

            self.create_mark_attendance_section()

        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        history_title = ctk.CTkLabel(
            self.main,
            text="Attendance History",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        history_title.pack(
            anchor="w",
            padx=10,
            pady=(20, 10)
        )

        self.history_frame = ctk.CTkScrollableFrame(
            self.main,
            fg_color="white",
            corner_radius=15,
            height=260
        )

        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 25)
        )

        self.show_no_history()

    # =====================================================
    # ADMIN STUDENT SELECTION
    # =====================================================

    def create_admin_selection(self):

        selection_card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15
        )

        selection_card.pack(
            fill="x",
            padx=5,
            pady=(5, 15)
        )

        title = ctk.CTkLabel(
            selection_card,
            text="Select Student",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.student_combo = ctk.CTkComboBox(
            selection_card,
            values=["Loading..."],
            height=42,
            corner_radius=8,
            command=self.on_student_selected
        )

        self.student_combo.pack(
            fill="x",
            padx=20,
            pady=(5, 20)
        )

    # =====================================================
    # MARK ATTENDANCE SECTION
    # =====================================================

    def create_mark_attendance_section(self):

        title = ctk.CTkLabel(
            self.main,
            text="Mark Attendance",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(5, 10)
        )

        card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=5,
            pady=(0, 20)
        )

        card.grid_columnconfigure(
            0,
            weight=1
        )

        card.grid_columnconfigure(
            1,
            weight=1
        )

        card.grid_columnconfigure(
            2,
            weight=1
        )

        # Date

        date_label = ctk.CTkLabel(
            card,
            text="Date",
            text_color="#334155",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        date_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.date_entry = ctk.CTkEntry(
            card,
            height=40,
            placeholder_text="DD-MM-YYYY"
        )

        self.date_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        # Status

        status_label = ctk.CTkLabel(
            card,
            text="Status",
            text_color="#334155",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        status_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=15,
            pady=(15, 5)
        )

        self.status_combo = ctk.CTkComboBox(
            card,
            values=[
                "PRESENT",
                "ABSENT"
            ],
            height=40
        )

        self.status_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

        self.status_combo.set(
            "PRESENT"
        )

        # Button

        mark_button = ctk.CTkButton(
            card,
            text="✓ Mark Attendance",
            height=40,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.mark_attendance
        )

        mark_button.grid(
            row=1,
            column=2,
            sticky="ew",
            padx=15,
            pady=(0, 15)
        )

    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5,
            pady=5
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        title_label.pack(
            pady=(18, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 18)
        )

        return value_label

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students(self):

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    name
                FROM students
                ORDER BY name COLLATE NOCASE
            """)

            students = cursor.fetchall()

            conn.close()

            values = []

            self.student_lookup = {}

            for database_id, student_id, name in students:

                display = (
                    f"{database_id} - "
                    f"{student_id or '-'} - "
                    f"{name or 'No Name'}"
                )

                values.append(
                    display
                )

                self.student_lookup[
                    display
                ] = database_id

            if values:

                self.student_combo.configure(
                    values=values
                )

                self.student_combo.set(
                    values[0]
                )

                self.on_student_selected(
                    values[0]
                )

            else:

                self.student_combo.configure(
                    values=[
                        "No students available"
                    ]
                )

                self.student_combo.set(
                    "No students available"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load students.\n\n{e}",
                parent=self
            )

    # =====================================================
    # STUDENT SELECTED
    # =====================================================

    def on_student_selected(
        self,
        selected
    ):

        if not selected:

            return

        if selected == "No students available":

            return

        database_id = self.student_lookup.get(
            selected
        )

        if database_id is None:

            return

        self.selected_student_id = database_id

        self.load_attendance(
            database_id
        )

    # =====================================================
    # LOAD STUDENT ATTENDANCE
    # =====================================================

    def load_student_attendance(self):

        self.selected_student_id = (
            self.database_id
        )

        self.load_attendance(
            self.database_id
        )

    # =====================================================
    # LOAD ATTENDANCE
    # =====================================================

    def load_attendance(
        self,
        database_id
    ):

        try:

            conn = get_connection()

            cursor = conn.cursor()

            # -------------------------------------------------
            # STUDENT
            # -------------------------------------------------

            cursor.execute("""
                SELECT
                    id,
                    student_id,
                    name,
                    course,
                    department,
                    year
                FROM students
                WHERE id = ?
            """, (
                database_id,
            ))

            student = cursor.fetchone()

            if not student:

                conn.close()

                messagebox.showerror(
                    "Attendance",
                    "Student record was not found.",
                    parent=self
                )

                return

            (
                db_id,
                student_id,
                name,
                course,
                department,
                year
            ) = student

            # -------------------------------------------------
            # TOTAL
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM attendance
                WHERE student_id = ?
            """, (
                database_id,
            ))

            total_classes = (
                cursor.fetchone()[0]
            )

            # -------------------------------------------------
            # PRESENT
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM attendance
                WHERE student_id = ?
                AND LOWER(TRIM(status)) = 'present'
            """, (
                database_id,
            ))

            present_count = (
                cursor.fetchone()[0]
            )

            # -------------------------------------------------
            # ABSENT
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM attendance
                WHERE student_id = ?
                AND LOWER(TRIM(status)) = 'absent'
            """, (
                database_id,
            ))

            absent_count = (
                cursor.fetchone()[0]
            )

            # -------------------------------------------------
            # PERCENTAGE
            # -------------------------------------------------

            if total_classes > 0:

                percentage = (
                    present_count /
                    total_classes
                ) * 100

            else:

                percentage = 0

            # -------------------------------------------------
            # HISTORY
            # -------------------------------------------------

            cursor.execute("""
                SELECT
                    attendance_date,
                    status
                FROM attendance
                WHERE student_id = ?
                ORDER BY
                    attendance_date DESC,
                    id DESC
            """, (
                database_id,
            ))

            history = cursor.fetchall()

            conn.close()

            # -------------------------------------------------
            # UPDATE STUDENT CARD
            # -------------------------------------------------

            self.student_name_label.configure(
                text=name or "Student"
            )

            self.student_details_label.configure(
                text=(
                    f"Student ID: {student_id or '-'}"
                    f"    |    "
                    f"Course: {course or '-'}"
                    f"    |    "
                    f"Department: {department or '-'}"
                    f"    |    "
                    f"Year: {year or '-'}"
                )
            )

            # -------------------------------------------------
            # UPDATE STATISTICS
            # -------------------------------------------------

            self.total_value.configure(
                text=str(total_classes)
            )

            self.present_value.configure(
                text=str(present_count)
            )

            self.absent_value.configure(
                text=str(absent_count)
            )

            self.percentage_value.configure(
                text=f"{percentage:.2f}%"
            )

            # -------------------------------------------------
            # HISTORY
            # -------------------------------------------------

            self.display_history(
                history
            )

        except Exception as e:

            messagebox.showerror(
                "Attendance Error",
                f"Unable to load attendance.\n\n{e}",
                parent=self
            )

    # =====================================================
    # DISPLAY HISTORY
    # =====================================================

    def display_history(
        self,
        history
    ):

        for widget in (
            self.history_frame.winfo_children()
        ):

            widget.destroy()

        if not history:

            self.show_no_history()

            return

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            self.history_frame,
            fg_color="#E2E8F0",
            corner_radius=8
        )

        header.pack(
            fill="x",
            padx=8,
            pady=(8, 4)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            header,
            text="Date",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            header,
            text="Status",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            padx=15,
            pady=10
        )

        # -------------------------------------------------
        # RECORDS
        # -------------------------------------------------

        for index, (
            attendance_date,
            status
        ) in enumerate(history):

            row = ctk.CTkFrame(
                self.history_frame,
                fg_color=(
                    "#F8FAFC"
                    if index % 2 == 0
                    else "white"
                ),
                corner_radius=8
            )

            row.pack(
                fill="x",
                padx=8,
                pady=2
            )

            row.grid_columnconfigure(
                0,
                weight=1
            )

            row.grid_columnconfigure(
                1,
                weight=1
            )

            ctk.CTkLabel(
                row,
                text=(
                    attendance_date
                    or "-"
                ),
                text_color="#334155",
                font=ctk.CTkFont(
                    size=13
                )
            ).grid(
                row=0,
                column=0,
                padx=15,
                pady=10
            )

            status_text = (
                str(status or "-").upper()
            )

            status_color = (
                "#16A34A"
                if status_text == "PRESENT"
                else "#DC2626"
                if status_text == "ABSENT"
                else "#64748B"
            )

            ctk.CTkLabel(
                row,
                text=status_text,
                text_color=status_color,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=1,
                padx=15,
                pady=10
            )

    # =====================================================
    # NO HISTORY
    # =====================================================

    def show_no_history(self):

        for widget in (
            self.history_frame.winfo_children()
        ):

            widget.destroy()

        ctk.CTkLabel(
            self.history_frame,
            text="No attendance history.",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=60
        )

    # =====================================================
    # MARK ATTENDANCE
    # =====================================================

    def mark_attendance(self):

        if self.selected_student_id is None:

            messagebox.showwarning(
                "Select Student",
                "Please select a student first.",
                parent=self
            )

            return

        date_value = (
            self.date_entry.get().strip()
        )

        status = (
            self.status_combo.get().strip().upper()
        )

        if not date_value:

            messagebox.showwarning(
                "Date Required",
                "Please enter the attendance date.\n\n"
                "Example: 31-08-2026",
                parent=self
            )

            self.date_entry.focus()

            return

        if status not in [
            "PRESENT",
            "ABSENT"
        ]:

            messagebox.showwarning(
                "Invalid Status",
                "Please select PRESENT or ABSENT.",
                parent=self
            )

            return

        try:

            conn = get_connection()

            cursor = conn.cursor()

            # -------------------------------------------------
            # CHECK EXISTING ATTENDANCE
            # -------------------------------------------------

            cursor.execute("""
                SELECT id
                FROM attendance
                WHERE student_id = ?
                AND attendance_date = ?
            """, (
                self.selected_student_id,
                date_value
            ))

            existing = cursor.fetchone()

            # -------------------------------------------------
            # UPDATE EXISTING
            # -------------------------------------------------

            if existing:

                cursor.execute("""
                    UPDATE attendance
                    SET status = ?
                    WHERE id = ?
                """, (
                    status,
                    existing[0]
                ))

                message = (
                    "Attendance updated successfully."
                )

            # -------------------------------------------------
            # INSERT NEW
            # -------------------------------------------------

            else:

                cursor.execute("""
                    INSERT INTO attendance (
                        student_id,
                        attendance_date,
                        status
                    )
                    VALUES (?, ?, ?)
                """, (
                    self.selected_student_id,
                    date_value,
                    status
                ))

                message = (
                    "Attendance marked successfully."
                )

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                message,
                parent=self
            )

            self.load_attendance(
                self.selected_student_id
            )

        except Exception as e:

            messagebox.showerror(
                "Attendance Error",
                f"Unable to save attendance.\n\n{e}",
                parent=self
            )

    # =====================================================
    # CLOSE
    # =====================================================

    def close_window(self):

        self.destroy()

        if self.parent:

            try:

                self.parent.focus_force()

            except:

                pass


# =========================================================
# OPEN ATTENDANCE
# =========================================================

def open_attendance(
    parent=None,
    database_id=None
):

    window = AttendanceWindow(
        parent,
        database_id
    )

    window.focus_force()

    return window


# =========================================================
# COMPATIBILITY FUNCTION
# =========================================================

def open_attendance_window(
    parent=None,
    database_id=None
):

    return open_attendance(
        parent,
        database_id
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    # -----------------------------------------------------
    # ADMIN TEST
    # -----------------------------------------------------
    #
    # window = open_attendance(app)
    #
    # -----------------------------------------------------
    # STUDENT TEST
    # -----------------------------------------------------
    #
    # Replace 1 with an existing students.id
    #
    # window = open_attendance(
    #     app,
    #     1
    # )

    app.mainloop()