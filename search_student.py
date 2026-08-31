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
# SEARCH STUDENT WINDOW
# =========================================================

class SearchStudentWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        self.title("Search Student")
        self.geometry("1000x700")
        self.minsize(850, 600)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()

        if parent:
            self.transient(parent)

        self.focus_force()


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


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            header,
            text="🔍  Search Student",
            text_color="white",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=30
        )


        # -------------------------------------------------
        # SUBTITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            header,
            text="Find student information quickly",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left"
        )


        # =================================================
        # SEARCH CARD
        # =================================================

        search_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
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


        # -------------------------------------------------
        # SEARCH ENTRY
        # -------------------------------------------------

        self.search_entry = ctk.CTkEntry(
            search_card,
            height=45,
            corner_radius=8,
            placeholder_text=(
                "Search Student ID, Name, Phone, "
                "Email or Course..."
            )
        )

        self.search_entry.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=20,
            sticky="ew"
        )


        # Press Enter to search

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_student()
        )


        # -------------------------------------------------
        # SEARCH BUTTON
        # -------------------------------------------------

        search_button = ctk.CTkButton(
            search_card,
            text="🔍 Search",
            width=120,
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.search_student
        )

        search_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=20
        )


        # -------------------------------------------------
        # CLEAR BUTTON
        # -------------------------------------------------

        clear_button = ctk.CTkButton(
            search_card,
            text="Clear",
            width=90,
            height=45,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.clear_search
        )

        clear_button.grid(
            row=0,
            column=2,
            padx=(5, 20),
            pady=20
        )


        # =================================================
        # RESULT AREA
        # =================================================

        self.result_area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.result_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )


        # -------------------------------------------------
        # INITIAL MESSAGE
        # -------------------------------------------------

        self.show_message(
            "Enter a Student ID, name, phone, email or course "
            "and click Search."
        )


    # =====================================================
    # SEARCH STUDENT
    # =====================================================

    def search_student(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )


        if not search_text:

            messagebox.showwarning(
                "Search",
                "Please enter something to search.",
                parent=self
            )

            return


        self.clear_results()


        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()


            value = f"%{search_text}%"


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
                WHERE
                    student_id LIKE ?
                    OR name LIKE ?
                    OR phone LIKE ?
                    OR email LIKE ?
                    OR course LIKE ?
                    OR department LIKE ?
                ORDER BY id DESC
            """, (
                value,
                value,
                value,
                value,
                value,
                value
            ))


            students = cursor.fetchall()

            conn.close()


            # =================================================
            # NO RESULTS
            # =================================================

            if not students:

                self.show_message(
                    f"No student found for: {search_text}"
                )

                return


            # =================================================
            # RESULT TITLE
            # =================================================

            result_title = ctk.CTkLabel(
                self.result_area,
                text=f"Search Results ({len(students)})",
                text_color="#0F172A",
                font=ctk.CTkFont(
                    size=20,
                    weight="bold"
                )
            )

            result_title.pack(
                anchor="w",
                padx=10,
                pady=(5, 15)
            )


            # =================================================
            # DISPLAY STUDENTS
            # =================================================

            for student in students:

                self.create_student_card(
                    student
                )


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search students.\n\n{e}",
                parent=self
            )


    # =====================================================
    # STUDENT CARD
    # =====================================================

    def create_student_card(
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


        # =================================================
        # CARD
        # =================================================

        card = ctk.CTkFrame(
            self.result_area,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )


        # =================================================
        # TOP SECTION
        # =================================================

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )


        # -------------------------------------------------
        # NAME
        # -------------------------------------------------

        ctk.CTkLabel(
            top,
            text=name or "No Name",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        ).pack(
            side="left"
        )


        # -------------------------------------------------
        # STUDENT ID
        # -------------------------------------------------

        ctk.CTkLabel(
            top,
            text=f"Student ID: {student_id or '-'}",
            text_color="#2563EB",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="right"
        )


        # =================================================
        # SEPARATOR
        # =================================================

        ctk.CTkFrame(
            card,
            height=1,
            fg_color="#E2E8F0"
        ).pack(
            fill="x",
            padx=20
        )


        # =================================================
        # DETAILS
        # =================================================

        details = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        details.pack(
            fill="x",
            padx=20,
            pady=15
        )

        details.grid_columnconfigure(
            (0, 1),
            weight=1
        )


        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

        self.add_detail(
            details,
            "Gender",
            gender,
            0,
            0
        )

        self.add_detail(
            details,
            "Date of Birth",
            dob,
            0,
            1
        )

        self.add_detail(
            details,
            "Phone",
            phone,
            1,
            0
        )

        self.add_detail(
            details,
            "Email",
            email,
            1,
            1
        )

        self.add_detail(
            details,
            "Course",
            course,
            2,
            0
        )

        self.add_detail(
            details,
            "Department",
            department,
            2,
            1
        )

        self.add_detail(
            details,
            "Year",
            year,
            3,
            0
        )

        self.add_detail(
            details,
            "Admission Date",
            admission_date,
            3,
            1
        )


        # =================================================
        # ADDRESS
        # =================================================

        address_frame = ctk.CTkFrame(
            details,
            fg_color="#F8FAFC",
            corner_radius=8
        )

        address_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=(10, 5)
        )


        ctk.CTkLabel(
            address_frame,
            text="Address",
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
            address_frame,
            text=address or "-",
            text_color="#334155",
            justify="left",
            anchor="w",
            wraplength=800,
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(2, 8)
        )


        # =================================================
        # ACTION BUTTONS
        # =================================================

        action_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        action_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        # -------------------------------------------------
        # EDIT
        # -------------------------------------------------

        edit_button = ctk.CTkButton(
            action_frame,
            text="✏️ Edit Student",
            width=140,
            height=38,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=lambda sid=database_id:
                self.edit_student(sid)
        )

        edit_button.pack(
            side="left"
        )


        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        delete_button = ctk.CTkButton(
            action_frame,
            text="🗑 Delete Student",
            width=150,
            height=38,
            corner_radius=8,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=lambda sid=database_id:
                self.delete_student(sid)
        )

        delete_button.pack(
            side="left",
            padx=10
        )


    # =====================================================
    # DETAIL FIELD
    # =====================================================

    def add_detail(
        self,
        parent,
        title,
        value,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#F8FAFC",
            corner_radius=8
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=5,
            pady=5
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
            text=value or "-",
            text_color="#334155",
            anchor="w",
            justify="left",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(2, 8)
        )


    # =====================================================
    # EDIT STUDENT
    # =====================================================

    def edit_student(
        self,
        database_id
    ):

        try:

            import update_student


            update_student.open_update_student(
                student_id=database_id,
                parent=self
            )


        except ModuleNotFoundError:

            messagebox.showerror(
                "Update Error",
                "update_student.py was not found.",
                parent=self
            )


        except Exception as e:

            messagebox.showerror(
                "Update Error",
                f"Unable to open Update Student.\n\n{e}",
                parent=self
            )


    # =====================================================
    # DELETE STUDENT
    # =====================================================

    def delete_student(
        self,
        database_id
    ):

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    student_id,
                    name
                FROM students
                WHERE id = ?
            """, (
                database_id,
            ))


            student = cursor.fetchone()

            conn.close()


            if not student:

                messagebox.showerror(
                    "Not Found",
                    "Student record was not found.",
                    parent=self
                )

                return


            student_id = student[0]
            name = student[1]


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to find student.\n\n{e}",
                parent=self
            )

            return


        # =================================================
        # CONFIRM
        # =================================================

        answer = messagebox.askyesno(
            "Confirm Delete",
            (
                "Are you sure you want to delete this student?\n\n"
                f"Student ID: {student_id}\n"
                f"Name: {name}\n\n"
                "This action cannot be undone."
            ),
            parent=self
        )


        if not answer:
            return


        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM students
                WHERE id = ?
                """,
                (
                    database_id,
                )
            )


            deleted = cursor.rowcount

            conn.commit()

            conn.close()


            if deleted > 0:

                messagebox.showinfo(
                    "Deleted",
                    "Student deleted successfully.",
                    parent=self
                )

                self.search_student()


            else:

                messagebox.showwarning(
                    "Not Found",
                    "Student record was not found.",
                    parent=self
                )


        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                f"Unable to delete student.\n\n{e}",
                parent=self
            )


    # =====================================================
    # SHOW MESSAGE
    # =====================================================

    def show_message(
        self,
        text
    ):

        label = ctk.CTkLabel(
            self.result_area,
            text=text,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=15
            ),
            justify="center"
        )

        label.pack(
            expand=True,
            pady=100
        )


    # =====================================================
    # CLEAR RESULTS
    # =====================================================

    def clear_results(self):

        for widget in self.result_area.winfo_children():

            widget.destroy()


    # =====================================================
    # CLEAR SEARCH
    # =====================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.clear_results()

        self.show_message(
            "Enter a Student ID, name, phone, email or course "
            "and click Search."
        )

        self.search_entry.focus()


# =========================================================
# OPEN SEARCH STUDENT
# =========================================================

def open_search_student(
    parent=None
):

    window = SearchStudentWindow(
        parent=parent
    )

    window.focus_force()

    return window


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    window = SearchStudentWindow(
        parent=app
    )

    app.mainloop()