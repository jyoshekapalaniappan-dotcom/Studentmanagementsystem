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
# ATTENDANCE REPORT WINDOW
# =========================================================

class AttendanceReportWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        self.title("Attendance Report")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()
        self.load_report()

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

        ctk.CTkLabel(
            header,
            text="📊  Attendance Report",
            text_color="white",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=30
        )

        ctk.CTkLabel(
            header,
            text="View student attendance performance",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left"
        )

        # -------------------------------------------------
        # SEARCH CARD
        # -------------------------------------------------

        search_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        search_card.pack(
            fill="x",
            padx=25,
            pady=20
        )

        search_card.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            search_card,
            height=42,
            corner_radius=8,
            placeholder_text="🔍 Search Student ID, Name or Course..."
        )

        self.search_entry.grid(
            row=0,
            column=0,
            padx=(15, 8),
            pady=15,
            sticky="ew"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.filter_report()
        )

        refresh_button = ctk.CTkButton(
            search_card,
            text="⟳ Refresh",
            width=110,
            height=42,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.load_report
        )

        refresh_button.grid(
            row=0,
            column=1,
            padx=(5, 15),
            pady=15
        )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        self.summary_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.summary_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        for column in range(5):

            self.summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.total_label = self.create_summary_card(
            0,
            "👥 Students",
            "0"
        )

        self.present_label = self.create_summary_card(
            1,
            "✅ Present",
            "0"
        )

        self.absent_label = self.create_summary_card(
            2,
            "❌ Absent",
            "0"
        )

        self.late_label = self.create_summary_card(
            3,
            "⏰ Late",
            "0"
        )

        self.leave_label = self.create_summary_card(
            4,
            "🏖 Leave",
            "0"
        )

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        table_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        self.table = ctk.CTkScrollableFrame(
            table_card,
            fg_color="white"
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        headers = [
            ("No.", 55),
            ("Student ID", 130),
            ("Name", 200),
            ("Course", 190),
            ("Total Days", 100),
            ("Present", 90),
            ("Absent", 90),
            ("Late", 80),
            ("Leave", 80),
            ("Attendance %", 120)
        ]

        for column, (text, width) in enumerate(headers):

            ctk.CTkLabel(
                self.table,
                text=text,
                width=width,
                height=42,
                fg_color="#E2E8F0",
                text_color="#0F172A",
                corner_radius=5,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=column,
                padx=2,
                pady=2,
                sticky="ew"
            )

    # =====================================================
    # SUMMARY CARD
    # =====================================================

    def create_summary_card(
        self,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            self.summary_frame,
            fg_color="white",
            corner_radius=12
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            pady=(12, 2)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 12)
        )

        return value_label

    # =====================================================
    # LOAD REPORT
    # =====================================================

    def load_report(self):

        self.clear_rows()

        self.report_data = []

        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            # -------------------------------------------------
            # Make sure attendance table exists
            # -------------------------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    attendance_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    UNIQUE(student_id, attendance_date)
                )
            """)

            conn.commit()

            # -------------------------------------------------
            # Get student attendance report
            # -------------------------------------------------

            cursor.execute("""
                SELECT
                    s.id,
                    s.student_id,
                    s.name,
                    s.course,

                    COUNT(a.id) AS total_days,

                    SUM(
                        CASE
                            WHEN LOWER(a.status) = 'present'
                            THEN 1
                            ELSE 0
                        END
                    ) AS present,

                    SUM(
                        CASE
                            WHEN LOWER(a.status) = 'absent'
                            THEN 1
                            ELSE 0
                        END
                    ) AS absent,

                    SUM(
                        CASE
                            WHEN LOWER(a.status) = 'late'
                            THEN 1
                            ELSE 0
                        END
                    ) AS late,

                    SUM(
                        CASE
                            WHEN LOWER(a.status) = 'leave'
                            THEN 1
                            ELSE 0
                        END
                    ) AS leave

                FROM students s

                LEFT JOIN attendance a
                    ON s.id = a.student_id

                GROUP BY
                    s.id,
                    s.student_id,
                    s.name,
                    s.course

                ORDER BY s.id DESC
            """)

            rows = cursor.fetchall()

            conn.close()

            # -------------------------------------------------
            # Calculate percentage
            # -------------------------------------------------

            for row in rows:

                (
                    database_id,
                    student_id,
                    name,
                    course,
                    total_days,
                    present,
                    absent,
                    late,
                    leave
                ) = row

                total_days = total_days or 0
                present = present or 0
                absent = absent or 0
                late = late or 0
                leave = leave or 0

                if total_days > 0:

                    percentage = (
                        present + late
                    ) / total_days * 100

                else:

                    percentage = 0

                self.report_data.append(
                    (
                        database_id,
                        student_id,
                        name,
                        course,
                        total_days,
                        present,
                        absent,
                        late,
                        leave,
                        percentage
                    )
                )

            self.display_report(
                self.report_data
            )

            self.update_summary(
                self.report_data
            )

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                f"Unable to load attendance report.\n\n{e}",
                parent=self
            )

    # =====================================================
    # DISPLAY REPORT
    # =====================================================

    def display_report(self, data):

        self.clear_rows()

        for row_number, row in enumerate(
            data,
            start=1
        ):

            (
                database_id,
                student_id,
                name,
                course,
                total_days,
                present,
                absent,
                late,
                leave,
                percentage
            ) = row

            values = [
                row_number,
                student_id or "",
                name or "",
                course or "",
                total_days,
                present,
                absent,
                late,
                leave,
                f"{percentage:.1f}%"
            ]

            widths = [
                55,
                130,
                200,
                190,
                100,
                90,
                90,
                80,
                80,
                120
            ]

            for column, value in enumerate(values):

                # Attendance percentage display
                if column == 9:

                    if percentage >= 75:

                        text_color = "#15803D"

                    elif percentage >= 50:

                        text_color = "#D97706"

                    else:

                        text_color = "#DC2626"

                else:

                    text_color = "#334155"

                ctk.CTkLabel(
                    self.table,
                    text=str(value),
                    width=widths[column],
                    height=42,
                    fg_color=(
                        "#F8FAFC"
                        if row_number % 2 == 0
                        else "white"
                    ),
                    text_color=text_color,
                    anchor="w",
                    font=ctk.CTkFont(
                        size=12,
                        weight=(
                            "bold"
                            if column == 9
                            else "normal"
                        )
                    )
                ).grid(
                    row=row_number,
                    column=column,
                    padx=2,
                    pady=2,
                    sticky="ew"
                )

    # =====================================================
    # FILTER
    # =====================================================

    def filter_report(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not search_text:

            filtered = self.report_data

        else:

            filtered = []

            for row in self.report_data:

                (
                    database_id,
                    student_id,
                    name,
                    course,
                    total_days,
                    present,
                    absent,
                    late,
                    leave,
                    percentage
                ) = row

                searchable_values = [
                    str(student_id or ""),
                    str(name or ""),
                    str(course or "")
                ]

                if any(
                    search_text in value.lower()
                    for value in searchable_values
                ):

                    filtered.append(row)

        self.display_report(
            filtered
        )

        self.update_summary(
            filtered
        )

    # =====================================================
    # UPDATE SUMMARY
    # =====================================================

    def update_summary(self, data):

        student_count = len(data)

        present = sum(
            row[5]
            for row in data
        )

        absent = sum(
            row[6]
            for row in data
        )

        late = sum(
            row[7]
            for row in data
        )

        leave = sum(
            row[8]
            for row in data
        )

        self.total_label.configure(
            text=str(student_count)
        )

        self.present_label.configure(
            text=str(present)
        )

        self.absent_label.configure(
            text=str(absent)
        )

        self.late_label.configure(
            text=str(late)
        )

        self.leave_label.configure(
            text=str(leave)
        )

    # =====================================================
    # CLEAR TABLE
    # =====================================================

    def clear_rows(self):

        if not hasattr(
            self,
            "table"
        ):

            return

        for widget in self.table.winfo_children():

            info = widget.grid_info()

            try:

                row = int(info["row"])

                if row > 0:

                    widget.destroy()

            except:

                pass


# =========================================================
# OPEN FUNCTION
# =========================================================

def open_attendance_report(parent=None):

    window = AttendanceReportWindow(
        parent
    )

    window.focus_force()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    open_attendance_report(app)

    app.mainloop()