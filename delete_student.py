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
# DELETE STUDENT WINDOW
# =========================================================

class DeleteStudentWindow(ctk.CTkToplevel):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.parent = parent

        self.title("Delete Student")
        self.geometry("1000x650")
        self.minsize(900, 550)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()

        if parent:
            self.transient(parent)

        self.focus_force()

        self.load_students()


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
            fg_color="#7F1D1D"
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
            text="🗑️  Delete Student",
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
            text="Remove a student record",
            text_color="#FECACA",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left"
        )


        # =================================================
        # SEARCH AREA
        # =================================================

        search_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )


        # -------------------------------------------------
        # SEARCH ENTRY
        # -------------------------------------------------

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=42,
            corner_radius=8,
            placeholder_text=(
                "🔍  Search by Student ID, "
                "name or course..."
            )
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=15
        )


        # Search while typing
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_students()
        )


        # -------------------------------------------------
        # REFRESH
        # -------------------------------------------------

        refresh_button = ctk.CTkButton(
            search_frame,
            text="⟳ Refresh",
            width=110,
            height=42,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.load_students
        )

        refresh_button.pack(
            side="right",
            padx=15
        )


        # =================================================
        # INFORMATION
        # =================================================

        ctk.CTkLabel(
            self,
            text=(
                "Select the student you want to delete. "
                "This action cannot be undone."
            ),
            text_color="#64748B",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(5, 10)
        )


        # =================================================
        # TABLE CONTAINER
        # =================================================

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


        # =================================================
        # SCROLLABLE TABLE
        # =================================================

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


        # =================================================
        # TABLE HEADERS
        # =================================================

        headers = [
            ("ID", 70),
            ("Student ID", 120),
            ("Name", 180),
            ("Gender", 100),
            ("Course", 180),
            ("Year", 120),
            ("Action", 150)
        ]


        for column, (
            text,
            width
        ) in enumerate(headers):

            label = ctk.CTkLabel(
                self.table,
                text=text,
                width=width,
                height=40,
                fg_color="#FEE2E2",
                text_color="#7F1D1D",
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
                pady=2,
                sticky="ew"
            )


    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students(self):

        self.clear_rows()

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
                    course,
                    year
                FROM students
                ORDER BY id DESC
            """)

            students = cursor.fetchall()

            conn.close()

            self.display_students(
                students
            )

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

        text = (
            self.search_entry
            .get()
            .strip()
        )

        self.clear_rows()

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()


            if text:

                value = f"%{text}%"

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

            self.display_students(
                students
            )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Unable to search students.\n\n{e}",
                parent=self
            )


    # =====================================================
    # DISPLAY STUDENTS
    # =====================================================

    def display_students(
        self,
        students
    ):

        if not students:

            ctk.CTkLabel(
                self.table,
                text="No students found.",
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=14
                )
            ).grid(
                row=1,
                column=0,
                columnspan=7,
                pady=30
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
                70,
                120,
                180,
                100,
                180,
                120
            ]


            # -------------------------------------------------
            # DATA CELLS
            # -------------------------------------------------

            for column, value in enumerate(
                values
            ):

                label = ctk.CTkLabel(
                    self.table,
                    text=str(value),
                    width=widths[column],
                    height=42,
                    fg_color=(
                        "#FFF7F7"
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
                    pady=2,
                    sticky="ew"
                )


            # -------------------------------------------------
            # DELETE BUTTON
            # -------------------------------------------------

            delete_button = ctk.CTkButton(
                self.table,
                text="🗑 Delete",
                width=130,
                height=34,
                corner_radius=7,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                ),
                command=lambda sid=database_id:
                    self.confirm_delete(sid)
            )

            delete_button.grid(
                row=row_number,
                column=6,
                padx=5,
                pady=5
            )


    # =====================================================
    # CONFIRM DELETE
    # =====================================================

    def confirm_delete(
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
                    name,
                    course
                FROM students
                WHERE id = ?
            """, (
                database_id,
            ))

            student = cursor.fetchone()

            conn.close()


            if not student:

                messagebox.showerror(
                    "Error",
                    "Student record was not found.",
                    parent=self
                )

                return


            student_id = student[0]
            name = student[1]
            course = student[2]


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to find student.\n\n{e}",
                parent=self
            )

            return


        # =================================================
        # CONFIRMATION
        # =================================================

        answer = messagebox.askyesno(
            "Confirm Delete",
            (
                "Are you sure you want to delete "
                "this student?\n\n"
                f"Student ID : {student_id}\n"
                f"Name       : {name}\n"
                f"Course     : {course}\n\n"
                "⚠ This action cannot be undone."
            ),
            parent=self
        )


        if answer:

            self.delete_student(
                database_id
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


            # =================================================
            # SUCCESS
            # =================================================

            if deleted > 0:

                messagebox.showinfo(
                    "Student Deleted",
                    "Student deleted successfully.",
                    parent=self
                )

                self.load_students()

            else:

                messagebox.showwarning(
                    "Not Found",
                    "Student record was not found.",
                    parent=self
                )


        except sqlite3.IntegrityError as e:

            messagebox.showerror(
                "Delete Error",
                (
                    "This student cannot be deleted because "
                    "another record depends on this student.\n\n"
                    f"{e}"
                ),
                parent=self
            )


        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                f"Unable to delete student.\n\n{e}",
                parent=self
            )


    # =====================================================
    # CLEAR TABLE ROWS
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
# OPEN DELETE STUDENT
# =========================================================

def open_delete_student(
    parent=None
):

    window = DeleteStudentWindow(
        parent=parent
    )

    window.focus_force()

    return window


# =========================================================
# TEST DIRECTLY
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    window = DeleteStudentWindow(
        parent=app
    )

    app.mainloop()