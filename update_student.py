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
# UPDATE STUDENT WINDOW
# =========================================================

class UpdateStudentWindow(ctk.CTkToplevel):

    def __init__(self, parent=None, student_id=None):

        super().__init__(parent)

        self.parent = parent
        self.student_id = student_id

        self.title("Update Student")
        self.geometry("900x700")
        self.minsize(800, 650)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()

        if parent:
            self.transient(parent)

        self.focus_force()

        # -------------------------------------------------
        # If a real database ID was supplied, load it
        # -------------------------------------------------

        if isinstance(
            self.student_id,
            int
        ):

            self.load_student()


    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # =================================================
        # HEADER
        # =================================================

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
            text="✏️  Update Student",
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
            text="Edit student information",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left",
            padx=5
        )


        # =================================================
        # SCROLL AREA
        # =================================================

        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        scroll.grid_columnconfigure(
            0,
            weight=1
        )

        scroll.grid_columnconfigure(
            1,
            weight=1
        )


        # =================================================
        # PERSONAL INFORMATION
        # =================================================

        ctk.CTkLabel(
            scroll,
            text="Personal Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(5, 15)
        )


        # -------------------------------------------------
        # STUDENT ID
        # -------------------------------------------------

        id_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        id_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            id_frame,
            text="Student ID",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.student_id_entry = ctk.CTkEntry(
            id_frame,
            height=40,
            corner_radius=8,
            placeholder_text="Example: ST001"
        )

        self.student_id_entry.pack(
            fill="x"
        )


        # -------------------------------------------------
        # LOAD BUTTON
        # -------------------------------------------------

        load_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        load_frame.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            load_frame,
            text="Load Student",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        ctk.CTkButton(
            load_frame,
            text="🔍 Load Student",
            height=40,
            corner_radius=8,
            fg_color="#0F766E",
            hover_color="#115E59",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.load_student_by_student_id
        ).pack(
            fill="x"
        )


        # =================================================
        # NAME
        # =================================================

        self.name_entry = self.create_entry(
            scroll,
            "Student Name *",
            2,
            0,
            "Enter full name"
        )


        # =================================================
        # GENDER
        # =================================================

        gender_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        gender_frame.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            gender_frame,
            text="Gender",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.gender = ctk.CTkComboBox(
            gender_frame,
            values=[
                "MALE",
                "FEMALE",
                "OTHER"
            ],
            height=40,
            corner_radius=8
        )

        self.gender.pack(
            fill="x"
        )

        self.gender.set(
            "MALE"
        )


        # =================================================
        # DATE OF BIRTH
        # =================================================

        self.dob_entry = self.create_entry(
            scroll,
            "Date of Birth",
            3,
            0,
            "DD-MM-YYYY"
        )


        # =================================================
        # PHONE
        # =================================================

        self.phone_entry = self.create_entry(
            scroll,
            "Phone Number",
            3,
            1,
            "Enter phone number"
        )


        # =================================================
        # EMAIL
        # =================================================

        self.email_entry = self.create_entry(
            scroll,
            "Email",
            4,
            0,
            "Enter email address"
        )


        # =================================================
        # ADDRESS
        # =================================================

        address_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        address_frame.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            address_frame,
            text="Address",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.address_entry = ctk.CTkTextbox(
            address_frame,
            height=80,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        self.address_entry.pack(
            fill="x"
        )


        # =================================================
        # ACADEMIC INFORMATION
        # =================================================

        ctk.CTkLabel(
            scroll,
            text="Academic Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(30, 15)
        )


        # =================================================
        # COURSE
        # =================================================

        self.course_entry = self.create_entry(
            scroll,
            "Course",
            6,
            0,
            "Example: BSc Computer Science"
        )


        # =================================================
        # DEPARTMENT
        # =================================================

        self.department_entry = self.create_entry(
            scroll,
            "Department",
            6,
            1,
            "Example: Computer Science"
        )


        # =================================================
        # YEAR
        # =================================================

        year_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        year_frame.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            year_frame,
            text="Year",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.year = ctk.CTkComboBox(
            year_frame,
            values=[
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ],
            height=40,
            corner_radius=8
        )

        self.year.pack(
            fill="x"
        )

        self.year.set(
            "1st Year"
        )


        # =================================================
        # ADMISSION DATE
        # =================================================

        self.admission_date_entry = self.create_entry(
            scroll,
            "Admission Date",
            7,
            1,
            "DD-MM-YYYY"
        )


        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        button_frame.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(30, 20)
        )

        button_frame.grid_columnconfigure(
            0,
            weight=1
        )

        button_frame.grid_columnconfigure(
            1,
            weight=1
        )


        # -------------------------------------------------
        # CANCEL
        # -------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=48,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.destroy
        ).grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="ew"
        )


        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="✓  Update Student",
            height=48,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.update_student
        ).grid(
            row=0,
            column=1,
            padx=(8, 0),
            sticky="ew"
        )


    # =====================================================
    # CREATE ENTRY
    # =====================================================

    def create_entry(
        self,
        parent,
        label_text,
        row,
        column,
        placeholder
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=10,
            pady=8
        )

        ctk.CTkLabel(
            frame,
            text=label_text,
            text_color="#334155",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        entry = ctk.CTkEntry(
            frame,
            height=40,
            corner_radius=8,
            placeholder_text=placeholder
        )

        entry.pack(
            fill="x"
        )

        return entry


    # =====================================================
    # LOAD USING STUDENT ID FIELD
    # =====================================================

    def load_student_by_student_id(self):

        student_id_value = (
            self.student_id_entry
            .get()
            .strip()
        )

        if not student_id_value:

            messagebox.showwarning(
                "Student ID",
                "Please enter Student ID.",
                parent=self
            )

            self.student_id_entry.focus()

            return

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            # -------------------------------------------------
            # Search by student_id text
            # -------------------------------------------------

            cursor.execute("""
                SELECT
                    id,
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
                WHERE student_id = ?
            """, (
                student_id_value,
            ))

            student = cursor.fetchone()

            conn.close()

            if not student:

                messagebox.showerror(
                    "Student Not Found",
                    f"No student found with Student ID:\n\n"
                    f"{student_id_value}",
                    parent=self
                )

                return

            self.student_id = student[0]

            self.fill_student_data(
                student
            )

            messagebox.showinfo(
                "Student Loaded",
                "Student information loaded successfully.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load student.\n\n{e}",
                parent=self
            )


    # =====================================================
    # LOAD USING DATABASE ID
    # =====================================================

    def load_student(self):

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
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
            """, (
                self.student_id,
            ))

            student = cursor.fetchone()

            conn.close()

            if not student:

                messagebox.showerror(
                    "Student Not Found",
                    "Student record was not found.",
                    parent=self
                )

                return

            self.fill_student_data(
                student
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load student.\n\n{e}",
                parent=self
            )


    # =====================================================
    # FILL FORM
    # =====================================================

    def fill_student_data(
        self,
        student
    ):

        (
            database_id,
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


        # -------------------------------------------------
        # Database ID
        # -------------------------------------------------

        self.student_id = database_id


        # -------------------------------------------------
        # Student ID
        # -------------------------------------------------

        self.set_entry(
            self.student_id_entry,
            student_id
        )


        # -------------------------------------------------
        # Name
        # -------------------------------------------------

        self.set_entry(
            self.name_entry,
            name
        )


        # -------------------------------------------------
        # Gender
        # -------------------------------------------------

        if gender:

            self.gender.set(
                str(gender).upper()
            )

        else:

            self.gender.set(
                "MALE"
            )


        # -------------------------------------------------
        # DOB
        # -------------------------------------------------

        self.set_entry(
            self.dob_entry,
            dob
        )


        # -------------------------------------------------
        # Phone
        # -------------------------------------------------

        self.set_entry(
            self.phone_entry,
            phone
        )


        # -------------------------------------------------
        # Email
        # -------------------------------------------------

        self.set_entry(
            self.email_entry,
            email
        )


        # -------------------------------------------------
        # Address
        # -------------------------------------------------

        self.address_entry.delete(
            "1.0",
            "end"
        )

        self.address_entry.insert(
            "1.0",
            address or ""
        )


        # -------------------------------------------------
        # Course
        # -------------------------------------------------

        self.set_entry(
            self.course_entry,
            course
        )


        # -------------------------------------------------
        # Department
        # -------------------------------------------------

        self.set_entry(
            self.department_entry,
            department
        )


        # -------------------------------------------------
        # Year
        # -------------------------------------------------

        if year:

            self.year.set(
                str(year)
            )

        else:

            self.year.set(
                "1st Year"
            )


        # -------------------------------------------------
        # Admission Date
        # -------------------------------------------------

        self.set_entry(
            self.admission_date_entry,
            admission_date
        )


    # =====================================================
    # SET ENTRY
    # =====================================================

    def set_entry(
        self,
        entry,
        value
    ):

        entry.delete(
            0,
            "end"
        )

        if value is not None:

            entry.insert(
                0,
                str(value)
            )


    # =====================================================
    # UPDATE STUDENT
    # =====================================================

    def update_student(self):

        if not isinstance(
            self.student_id,
            int
        ):

            messagebox.showwarning(
                "Load Student",
                "Please enter a Student ID and click "
                "'Load Student' first.",
                parent=self
            )

            return


        student_id_value = (
            self.student_id_entry
            .get()
            .strip()
        )

        name = (
            self.name_entry
            .get()
            .strip()
        )

        gender = (
            self.gender
            .get()
            .strip()
        )

        dob = (
            self.dob_entry
            .get()
            .strip()
        )

        phone = (
            self.phone_entry
            .get()
            .strip()
        )

        email = (
            self.email_entry
            .get()
            .strip()
        )

        address = (
            self.address_entry
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        course = (
            self.course_entry
            .get()
            .strip()
        )

        department = (
            self.department_entry
            .get()
            .strip()
        )

        year = (
            self.year
            .get()
            .strip()
        )

        admission_date = (
            self.admission_date_entry
            .get()
            .strip()
        )


        # =================================================
        # VALIDATION
        # =================================================

        if not student_id_value:

            messagebox.showwarning(
                "Missing Information",
                "Student ID is required.",
                parent=self
            )

            return


        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Student Name is required.",
                parent=self
            )

            self.name_entry.focus()

            return


        # =================================================
        # DATABASE UPDATE
        # =================================================

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE students
                SET
                    student_id = ?,
                    name = ?,
                    gender = ?,
                    dob = ?,
                    phone = ?,
                    email = ?,
                    address = ?,
                    course = ?,
                    department = ?,
                    year = ?,
                    admission_date = ?
                WHERE id = ?
            """, (
                student_id_value,
                name,
                gender,
                dob,
                phone,
                email,
                address,
                course,
                department,
                year,
                admission_date,
                self.student_id
            ))

            conn.commit()

            affected = cursor.rowcount

            conn.close()


            if affected == 0:

                messagebox.showerror(
                    "Update Failed",
                    "No student record was updated.",
                    parent=self
                )

                return


            # =================================================
            # SUCCESS
            # =================================================

            messagebox.showinfo(
                "Success",
                "Student information updated successfully.",
                parent=self
            )

            self.destroy()


        except sqlite3.IntegrityError as e:

            messagebox.showerror(
                "Database Error",
                f"Student ID may already exist.\n\n{e}",
                parent=self
            )


        except Exception as e:

            messagebox.showerror(
                "Update Error",
                f"Unable to update student.\n\n{e}",
                parent=self
            )


# =========================================================
# OPEN UPDATE STUDENT
# =========================================================

def open_update_student(
    parent=None,
    student_id=None
):

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # dashboard.py calls:
    #
    # open_update_student(self)
    #
    # Therefore self is the parent window.
    # -----------------------------------------------------

    window = UpdateStudentWindow(
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

    window = UpdateStudentWindow(
        parent=app
    )

    app.mainloop()