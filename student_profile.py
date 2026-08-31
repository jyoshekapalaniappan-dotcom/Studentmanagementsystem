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
# STUDENT PROFILE WINDOW
# =========================================================

class StudentProfileWindow(ctk.CTkToplevel):

    def __init__(self, parent=None, student_id=None):

        super().__init__(parent)

        self.parent = parent
        self.database_id = student_id

        self.title("My Profile")
        self.geometry("1050x750")
        self.minsize(900, 650)

        self.configure(
            fg_color="#F5F7FB"
        )

        # -------------------------------------------------
        # CHECK STUDENT ID
        # -------------------------------------------------

        if self.database_id is None:

            messagebox.showerror(
                "Student Profile",
                "No student was selected.",
                parent=self
            )

            self.destroy()
            return

        # -------------------------------------------------
        # CREATE UI
        # -------------------------------------------------

        self.create_ui()

        # -------------------------------------------------
        # LOAD PROFILE
        # -------------------------------------------------

        self.load_profile()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        if parent:
            self.transient(parent)

        self.focus_force()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )


    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self,
            height=100,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)


        ctk.CTkLabel(
            header,
            text="👤  My Profile",
            text_color="white",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=30
        )


        ctk.CTkLabel(
            header,
            text="View your personal information",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left"
        )


        # =================================================
        # CLOSE BUTTON
        # =================================================

        ctk.CTkButton(
            header,
            text="Close",
            width=100,
            height=38,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.close_window
        ).pack(
            side="right",
            padx=25
        )


        # =================================================
        # SCROLL AREA
        # =================================================

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.scroll.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # =================================================
        # PROFILE HEADER CARD
        # =================================================

        profile_card = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        profile_card.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5
        )

        profile_card.grid_columnconfigure(
            1,
            weight=1
        )


        # -------------------------------------------------
        # AVATAR
        # -------------------------------------------------

        avatar = ctk.CTkFrame(
            profile_card,
            width=90,
            height=90,
            corner_radius=45,
            fg_color="#2563EB"
        )

        avatar.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=25,
            pady=20
        )

        avatar.pack_propagate(False)


        ctk.CTkLabel(
            avatar,
            text="👨‍🎓",
            font=ctk.CTkFont(
                size=38
            )
        ).pack(
            expand=True
        )


        # -------------------------------------------------
        # NAME
        # -------------------------------------------------

        self.name_label = ctk.CTkLabel(
            profile_card,
            text="Student",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        self.name_label.grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(20, 2)
        )


        # -------------------------------------------------
        # STUDENT ID
        # -------------------------------------------------

        self.id_label = ctk.CTkLabel(
            profile_card,
            text="Student ID: -",
            text_color="#2563EB",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.id_label.grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 20)
        )


        # =================================================
        # STUDENT INFORMATION TITLE
        # =================================================

        ctk.CTkLabel(
            self.scroll,
            text="Student Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(25, 10)
        )


        # =================================================
        # DETAILS FRAME
        # =================================================

        self.details_frame = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        self.details_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5
        )

        self.details_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # =================================================
        # ATTENDANCE TITLE
        # =================================================

        ctk.CTkLabel(
            self.scroll,
            text="Attendance Summary",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(30, 10)
        )


        # =================================================
        # ATTENDANCE FRAME
        # =================================================

        self.attendance_frame = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        self.attendance_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5
        )

        self.attendance_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )


        self.present_label = self.create_stat(
            self.attendance_frame,
            0,
            "Present",
            "0"
        )


        self.absent_label = self.create_stat(
            self.attendance_frame,
            1,
            "Absent",
            "0"
        )


        self.percentage_label = self.create_stat(
            self.attendance_frame,
            2,
            "Attendance",
            "0%"
        )


        # =================================================
        # HISTORY TITLE
        # =================================================

        ctk.CTkLabel(
            self.scroll,
            text="Attendance History",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(30, 10)
        )


        # =================================================
        # HISTORY FRAME
        # =================================================

        self.history_frame = ctk.CTkScrollableFrame(
            self.scroll,
            height=250,
            fg_color="white",
            corner_radius=15
        )

        self.history_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=(0, 20)
        )


    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat(
        self,
        parent,
        column,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        frame.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=10,
            pady=15
        )


        ctk.CTkLabel(
            frame,
            text=title,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(15, 3)
        )


        value_label = ctk.CTkLabel(
            frame,
            text=value,
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 15)
        )


        return value_label


    # =====================================================
    # LOAD PROFILE
    # =====================================================

    def load_profile(self):

        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT
                    student_id,
                    name,
                    gender,
                    dob,
                    phone,
                    email,
                    address,
                    course,
                    department,
                    year,
                    admission_date
                FROM students
                WHERE id = ?
                """,
                (
                    self.database_id,
                )
            )


            student = cursor.fetchone()

            conn.close()


            if not student:

                messagebox.showerror(
                    "Student Profile",
                    "Student record was not found.",
                    parent=self
                )

                self.destroy()

                return


            (
                student_id,
                name,
                gender,
                dob,
                phone,
                email,
                address,
                course,
                department,
                year,
                admission_date
            ) = student


            # =================================================
            # HEADER INFORMATION
            # =================================================

            self.name_label.configure(
                text=name or "Student"
            )


            self.id_label.configure(
                text=f"Student ID: {student_id or '-'}"
            )


            # =================================================
            # STUDENT DETAILS
            # =================================================

            details = [

                ("Gender", gender),

                ("Date of Birth", dob),

                ("Phone", phone),

                ("Email", email),

                ("Course", course),

                ("Department", department),

                ("Year", year),

                ("Admission Date", admission_date),

                ("Address", address)

            ]


            # Remove old details if any

            for widget in self.details_frame.winfo_children():

                widget.destroy()


            # Create details

            for index, (title, value) in enumerate(details):

                row = index // 2

                column = index % 2

                self.create_detail(
                    title,
                    value,
                    row,
                    column
                )


            # =================================================
            # LOAD ATTENDANCE
            # =================================================

            self.load_attendance()


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load profile.\n\n{e}",
                parent=self
            )


    # =====================================================
    # DETAIL CARD
    # =====================================================

    def create_detail(
        self,
        title,
        value,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            self.details_frame,
            fg_color="#F8FAFC",
            corner_radius=8
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=8,
            pady=8
        )


        ctk.CTkLabel(
            frame,
            text=title,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(8, 0)
        )


        ctk.CTkLabel(
            frame,
            text=(
                str(value)
                if value not in (None, "")
                else "-"
            ),
            text_color="#334155",
            anchor="w",
            justify="left",
            wraplength=380,
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(2, 8)
        )


    # =====================================================
    # LOAD ATTENDANCE
    # =====================================================

    def load_attendance(self):

        # -------------------------------------------------
        # CLEAR HISTORY
        # -------------------------------------------------

        for widget in self.history_frame.winfo_children():

            widget.destroy()


        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()


            # =================================================
            # ATTENDANCE SUMMARY
            # =================================================

            cursor.execute(
                """
                SELECT
                    COUNT(*),

                    SUM(
                        CASE
                            WHEN LOWER(TRIM(status)) = 'present'
                            THEN 1
                            ELSE 0
                        END
                    ),

                    SUM(
                        CASE
                            WHEN LOWER(TRIM(status)) = 'absent'
                            THEN 1
                            ELSE 0
                        END
                    )

                FROM attendance

                WHERE student_id = ?
                """,
                (
                    self.database_id,
                )
            )


            result = cursor.fetchone()


            total = result[0] or 0

            present = result[1] or 0

            absent = result[2] or 0


            # -------------------------------------------------
            # PERCENTAGE
            # -------------------------------------------------

            if total > 0:

                percentage = (
                    present / total
                ) * 100

            else:

                percentage = 0


            # -------------------------------------------------
            # UPDATE LABELS
            # -------------------------------------------------

            self.present_label.configure(
                text=str(present)
            )

            self.absent_label.configure(
                text=str(absent)
            )

            self.percentage_label.configure(
                text=f"{percentage:.1f}%"
            )


            # =================================================
            # ATTENDANCE HISTORY
            # =================================================

            cursor.execute(
                """
                SELECT
                    attendance_date,
                    status

                FROM attendance

                WHERE student_id = ?

                ORDER BY attendance_date DESC
                """,
                (
                    self.database_id,
                )
            )


            history = cursor.fetchall()

            conn.close()


            # =================================================
            # TABLE HEADER
            # =================================================

            headers = [
                ("Date", 250),
                ("Status", 200)
            ]


            for column, (text, width) in enumerate(headers):

                ctk.CTkLabel(
                    self.history_frame,
                    text=text,
                    width=width,
                    height=38,
                    fg_color="#E2E8F0",
                    text_color="#0F172A",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    )
                ).grid(
                    row=0,
                    column=column,
                    padx=3,
                    pady=3
                )


            # =================================================
            # NO RECORDS
            # =================================================

            if not history:

                ctk.CTkLabel(
                    self.history_frame,
                    text="No attendance records found.",
                    text_color="#64748B",
                    font=ctk.CTkFont(
                        size=13
                    )
                ).grid(
                    row=1,
                    column=0,
                    columnspan=2,
                    pady=30
                )

                return


            # =================================================
            # HISTORY ROWS
            # =================================================

            for row, (
                attendance_date,
                status
            ) in enumerate(
                history,
                start=1
            ):


                ctk.CTkLabel(
                    self.history_frame,
                    text=str(
                        attendance_date
                    ),
                    width=250,
                    height=38,
                    anchor="w",
                    fg_color="#F8FAFC",
                    text_color="#334155"
                ).grid(
                    row=row,
                    column=0,
                    padx=3,
                    pady=2
                )


                ctk.CTkLabel(
                    self.history_frame,
                    text=str(
                        status
                    ),
                    width=200,
                    height=38,
                    fg_color="#F8FAFC",
                    text_color="#334155",
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold"
                    )
                ).grid(
                    row=row,
                    column=1,
                    padx=3,
                    pady=2
                )


        except Exception as e:

            messagebox.showerror(
                "Attendance Error",
                f"Unable to load attendance.\n\n{e}",
                parent=self
            )


    # =====================================================
    # CLOSE WINDOW
    # =====================================================

    def close_window(self):

        self.destroy()


# =========================================================
# OPEN STUDENT PROFILE
# =========================================================

def open_student_profile(
    student_id=None,
    parent=None
):

    if student_id is None:

        messagebox.showwarning(
            "Student Profile",
            "No student was selected.",
            parent=parent
        )

        return None


    try:

        student_id = int(
            student_id
        )

    except (
        TypeError,
        ValueError
    ):

        messagebox.showerror(
            "Student Profile",
            "Invalid student database ID.",
            parent=parent
        )

        return None


    window = StudentProfileWindow(
        parent=parent,
        student_id=student_id
    )

    window.focus_force()

    return window


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    # -----------------------------------------------------
    # Do not normally run this file directly.
    #
    # Student Profile should be opened from
    # student_portal.py using the logged-in student's
    # database ID.
    # -----------------------------------------------------

    app.mainloop()