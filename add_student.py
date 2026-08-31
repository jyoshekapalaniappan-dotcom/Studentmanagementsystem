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
# DATABASE
# =========================================================

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            name TEXT NOT NULL,
            gender TEXT,
            dob TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            course TEXT,
            department TEXT,
            year TEXT,
            admission_date TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# ADD STUDENT WINDOW
# =========================================================

class AddStudentWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Add Student")
        self.geometry("900x700")
        self.minsize(800, 650)

        self.configure(fg_color="#F5F7FB")

        self.create_ui()

        self.transient(parent)
        self.grab_set()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            corner_radius=0,
            height=100
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="➕  Add New Student",
            text_color="white",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            )
        )

        title.pack(
            side="left",
            padx=30,
            pady=25
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Enter student information",
            text_color="#CBD5E1",
            font=ctk.CTkFont(size=13)
        )

        subtitle.pack(
            side="left",
            padx=5,
            pady=30
        )

        # Scroll area
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
            (0, 1),
            weight=1
        )

        # =================================================
        # PERSONAL INFORMATION
        # =================================================

        personal_title = ctk.CTkLabel(
            scroll,
            text="Personal Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        personal_title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(5, 15)
        )

        # Student ID
        self.student_id = self.create_entry(
            scroll,
            "Student ID",
            1,
            0,
            "Example: ST001"
        )

        # Name
        self.name = self.create_entry(
            scroll,
            "Student Name *",
            1,
            1,
            "Enter full name"
        )

        # Gender
        gender_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        gender_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        gender_label = ctk.CTkLabel(
            gender_frame,
            text="Gender",
            text_color="#334155",
            font=ctk.CTkFont(size=13)
        )

        gender_label.pack(
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

        self.gender.set("MALE")

        # DOB
        self.dob = self.create_entry(
            scroll,
            "Date of Birth",
            2,
            1,
            "DD-MM-YYYY"
        )

        # =================================================
        # CONTACT INFORMATION
        # =================================================

        contact_title = ctk.CTkLabel(
            scroll,
            text="Contact Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        contact_title.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(30, 15)
        )

        self.phone = self.create_entry(
            scroll,
            "Phone Number",
            4,
            0,
            "Enter phone number"
        )

        self.email = self.create_entry(
            scroll,
            "Email",
            4,
            1,
            "Enter email address"
        )

        # Address
        address_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        address_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=8
        )

        address_label = ctk.CTkLabel(
            address_frame,
            text="Address",
            text_color="#334155",
            font=ctk.CTkFont(size=13)
        )

        address_label.pack(
            anchor="w",
            pady=(0, 5)
        )

        self.address = ctk.CTkTextbox(
            address_frame,
            height=80,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        self.address.pack(
            fill="x"
        )

        # =================================================
        # ACADEMIC INFORMATION
        # =================================================

        academic_title = ctk.CTkLabel(
            scroll,
            text="Academic Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        academic_title.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=(30, 15)
        )

        self.course = self.create_entry(
            scroll,
            "Course",
            7,
            0,
            "Example: BSc Computer Science"
        )

        self.department = self.create_entry(
            scroll,
            "Department",
            7,
            1,
            "Example: Computer Science"
        )

        # Year
        year_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        year_frame.grid(
            row=8,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        year_label = ctk.CTkLabel(
            year_frame,
            text="Year",
            text_color="#334155",
            font=ctk.CTkFont(size=13)
        )

        year_label.pack(
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

        self.year.set("1st Year")

        self.admission_date = self.create_entry(
            scroll,
            "Admission Date",
            8,
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
            row=9,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(30, 20)
        )

        button_frame.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            height=48,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.clear_form
        )

        clear_button.grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="ew"
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="✓  Save Student",
            height=48,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.save_student
        )

        save_button.grid(
            row=0,
            column=1,
            padx=(8, 0),
            sticky="ew"
        )

    # =====================================================
    # ENTRY CREATOR
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

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            text_color="#334155",
            font=ctk.CTkFont(size=13)
        )

        label.pack(
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
    # SAVE STUDENT
    # =====================================================

    def save_student(self):

        student_id = self.student_id.get().strip()
        name = self.name.get().strip()
        gender = self.gender.get().strip()
        dob = self.dob.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        address = self.address.get("1.0", "end").strip()
        course = self.course.get().strip()
        department = self.department.get().strip()
        year = self.year.get().strip()
        admission_date = self.admission_date.get().strip()

        # Required field
        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the student name.",
                parent=self
            )
            self.name.focus()
            return

        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO students
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
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
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
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Student added successfully!",
                parent=self
            )

            self.clear_form()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to save student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_form(self):

        self.student_id.delete(0, "end")
        self.name.delete(0, "end")
        self.dob.delete(0, "end")
        self.phone.delete(0, "end")
        self.email.delete(0, "end")
        self.address.delete("1.0", "end")
        self.course.delete(0, "end")
        self.department.delete(0, "end")
        self.admission_date.delete(0, "end")

        self.gender.set("MALE")
        self.year.set("1st Year")

        self.name.focus()


# =========================================================
# OPEN FUNCTION
# =========================================================

def open_add_student(parent=None):

    create_table()

    window = AddStudentWindow(parent)

    window.focus()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    create_table()

    app = ctk.CTk()

    app.withdraw()

    window = AddStudentWindow(app)

    app.mainloop()