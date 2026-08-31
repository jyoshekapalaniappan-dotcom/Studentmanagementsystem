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
# STUDENT PORTAL
# =========================================================

class StudentPortalWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent=None,
        student_id=None,
        student_data=None
    ):

        super().__init__(parent)

        self.parent = parent
        self.database_id = student_id
        self.student = None

        # =================================================
        # GET STUDENT ID
        # =================================================

        if self.database_id is None and student_data is not None:

            try:

                if isinstance(student_data, (tuple, list)):

                    self.database_id = student_data[0]

                elif isinstance(student_data, dict):

                    self.database_id = (
                        student_data.get("id")
                        or student_data.get("database_id")
                    )

            except Exception:
                pass

        # =================================================
        # WINDOW
        # =================================================

        self.title("Student Portal")

        self.geometry("1400x850")

        self.minsize(
            1100,
            700
        )

        self.configure(
            fg_color="#F5F7FB"
        )

        # =================================================
        # LOAD STUDENT
        # =================================================

        if self.database_id is not None:

            if not self.load_student():

                return

        else:

            messagebox.showerror(
                "Student Portal",
                "Student database ID is missing.",
                parent=self
            )

            self.destroy()

            return

        # =================================================
        # CREATE UI
        # =================================================

        self.create_ui()

        # =================================================
        # WINDOW SETTINGS
        # =================================================

        if parent:

            self.transient(parent)

        self.lift()

        self.focus_force()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # =====================================================
    # LOAD STUDENT
    # =====================================================

    def load_student(self):

        try:

            if not os.path.exists(DB_FILE):

                messagebox.showerror(
                    "Database Error",
                    f"student.db was not found.\n\n"
                    f"Expected location:\n{DB_FILE}",
                    parent=self
                )

                self.destroy()

                return False

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            cursor.execute(
                """
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
                """,
                (self.database_id,)
            )

            self.student = cursor.fetchone()

            conn.close()

            if not self.student:

                messagebox.showerror(
                    "Student Portal",
                    f"No student was found with database ID:\n\n"
                    f"{self.database_id}",
                    parent=self
                )

                self.destroy()

                return False

            return True

        except sqlite3.OperationalError as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to read the students table.\n\n{e}",
                parent=self
            )

            self.destroy()

            return False

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load student information.\n\n{e}",
                parent=self
            )

            self.destroy()

            return False

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self,
            height=105,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # =================================================
        # HEADER LEFT
        # =================================================

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="y",
            padx=35
        )

        ctk.CTkLabel(
            left,
            text="🎓",
            font=ctk.CTkFont(
                size=34
            ),
            text_color="white"
        ).pack(
            side="left",
            padx=(0, 12)
        )

        ctk.CTkLabel(
            left,
            text="Student Portal",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color="white"
        ).pack(
            side="left"
        )

        # =================================================
        # WELCOME
        # =================================================

        name = "Student"

        if self.student:

            name = self.student[2] or "Student"

        ctk.CTkLabel(
            header,
            text=f"Welcome, {name}",
            font=ctk.CTkFont(
                size=15
            ),
            text_color="#CBD5E1"
        ).pack(
            side="left",
            padx=20
        )

        # =================================================
        # LOGOUT
        # =================================================

        ctk.CTkButton(
            header,
            text="🚪 Logout",
            width=125,
            height=43,
            corner_radius=8,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.logout
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
            padx=30,
            pady=25
        )

        self.scroll.grid_columnconfigure(
            0,
            weight=1
        )

        self.scroll.grid_columnconfigure(
            1,
            weight=1
        )

        self.scroll.grid_columnconfigure(
            2,
            weight=1
        )

        # =================================================
        # SUMMARY
        # =================================================

        self.create_summary()

        # =================================================
        # CONTACT
        # =================================================

        self.create_contact_section()

        # =================================================
        # SERVICES
        # =================================================

        self.create_services_section()

    # =====================================================
    # SUMMARY
    # =====================================================

    def create_summary(self):

        name = "Student"
        student_id = "-"
        course = "-"
        department = "-"
        year = "-"

        if self.student:

            student_id = self.student[1] or "-"
            name = self.student[2] or "Student"
            course = self.student[8] or "-"
            department = self.student[9] or "-"
            year = self.student[10] or "-"

        # =================================================
        # NAME
        # =================================================

        self.create_summary_card(
            row=0,
            column=0,
            icon="👤",
            title=name,
            subtitle=f"Student ID: {student_id}"
        )

        # =================================================
        # COURSE
        # =================================================

        self.create_summary_card(
            row=0,
            column=1,
            icon="📚",
            title=course,
            subtitle=department
        )

        # =================================================
        # YEAR
        # =================================================

        self.create_summary_card(
            row=0,
            column=2,
            icon="🎓",
            title=f"Year {year}",
            subtitle="Academic Year"
        )

    # =====================================================
    # SUMMARY CARD
    # =====================================================

    def create_summary_card(
        self,
        row,
        column,
        icon,
        title,
        subtitle
    ):

        card = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        card.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=7,
            pady=7
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=35
            )
        ).pack(
            pady=(22, 5)
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            pady=(0, 5)
        )

        ctk.CTkLabel(
            card,
            text=subtitle,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            pady=(0, 22)
        )

    # =====================================================
    # CONTACT SECTION
    # =====================================================

    def create_contact_section(self):

        ctk.CTkLabel(
            self.scroll,
            text="Contact Information",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=(30, 10)
        )

        contact = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        contact.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=7,
            pady=5
        )

        contact.grid_columnconfigure(
            0,
            weight=1
        )

        contact.grid_columnconfigure(
            1,
            weight=1
        )

        phone = "-"
        email = "-"
        admission_date = "-"
        address = "-"

        if self.student:

            phone = self.student[5] or "-"
            email = self.student[6] or "-"
            address = self.student[7] or "-"
            admission_date = self.student[11] or "-"

        self.create_contact_item(
            contact,
            "📱 Phone",
            phone,
            0,
            0
        )

        self.create_contact_item(
            contact,
            "📧 Email",
            email,
            0,
            1
        )

        self.create_contact_item(
            contact,
            "📅 Admission Date",
            admission_date,
            1,
            0
        )

        self.create_contact_item(
            contact,
            "🏠 Address",
            address,
            1,
            1
        )

    # =====================================================
    # CONTACT ITEM
    # =====================================================

    def create_contact_item(
        self,
        parent,
        title,
        value,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=25,
            pady=18
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
            anchor="w"
        )

        ctk.CTkLabel(
            frame,
            text=str(value),
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            anchor="w",
            justify="left",
            wraplength=500
        ).pack(
            anchor="w",
            pady=(7, 0)
        )

    # =====================================================
    # SERVICES
    # =====================================================

    def create_services_section(self):

        ctk.CTkLabel(
            self.scroll,
            text="Student Services",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=(30, 10)
        )

        # =================================================
        # ATTENDANCE
        # =================================================

        self.create_service_card(
            row=4,
            column=0,
            icon="📊",
            title="Attendance",
            description="View your attendance records",
            button_text="Open",
            command=self.open_attendance
        )

        # =================================================
        # ANNOUNCEMENTS
        # =================================================

        self.create_service_card(
            row=4,
            column=1,
            icon="📢",
            title="Announcements",
            description="View notices published by admin",
            button_text="Open",
            command=self.open_announcements
        )

        # =================================================
        # EVENTS
        # =================================================

        self.create_service_card(
            row=4,
            column=2,
            icon="📅",
            title="Events & Meetings",
            description="View upcoming student events",
            button_text="Open",
            command=self.open_events
        )

        # =================================================
        # PROFILE
        # =================================================

        self.create_service_card(
            row=5,
            column=0,
            icon="👤",
            title="My Profile",
            description="View your complete profile",
            button_text="Open",
            command=self.open_profile
        )

        # =================================================
        # REFRESH
        # =================================================

        self.create_service_card(
            row=5,
            column=1,
            icon="🔄",
            title="Refresh",
            description="Reload student information",
            button_text="Refresh",
            command=self.refresh_portal
        )

    # =====================================================
    # SERVICE CARD
    # =====================================================

    def create_service_card(
        self,
        row,
        column,
        icon,
        title,
        description,
        button_text,
        command
    ):

        card = ctk.CTkFrame(
            self.scroll,
            fg_color="white",
            corner_radius=15
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=7,
            pady=7
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=35
            )
        ).pack(
            pady=(25, 8)
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            pady=(0, 7)
        )

        ctk.CTkLabel(
            card,
            text=description,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=13
            ),
            wraplength=300
        ).pack(
            pady=(0, 20)
        )

        ctk.CTkButton(
            card,
            text=button_text,
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=command
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

    # =====================================================
    # PROFILE
    # =====================================================

    def open_profile(self):

        try:

            import student_profile

            window = student_profile.open_student_profile(
                student_id=self.database_id,
                parent=self
            )

            if window:

                window.focus_force()

        except ModuleNotFoundError:

            messagebox.showerror(
                "Profile Error",
                "student_profile.py was not found.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Profile Error",
                f"Unable to open Student Profile.\n\n{e}",
                parent=self
            )

    # =====================================================
    # ATTENDANCE
    # =====================================================

    def open_attendance(self):

        try:

            import attendance

            # Preferred student function

            if hasattr(
                attendance,
                "open_student_attendance"
            ):

                window = attendance.open_student_attendance(
                    parent=self,
                    student_id=self.database_id
                )

                if window:

                    window.focus_force()

                return

            # Existing function

            if hasattr(
                attendance,
                "open_attendance"
            ):

                window = attendance.open_attendance(
                    self,
                    self.database_id
                )

                if window:

                    window.focus_force()

                return

            messagebox.showerror(
                "Attendance Error",
                "Attendance function was not found in attendance.py.",
                parent=self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Attendance Error",
                "attendance.py was not found.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Attendance Error",
                f"Unable to open Attendance.\n\n{e}",
                parent=self
            )

    # =====================================================
    # ANNOUNCEMENTS
    # =====================================================

    def open_announcements(self):

        try:

            import announcements

            # =================================================
            # STUDENT ANNOUNCEMENTS
            # =================================================

            if hasattr(
                announcements,
                "open_student_announcements"
            ):

                window = announcements.open_student_announcements(
                    parent=self
                )

                if window:

                    window.focus_force()

                return

            # =================================================
            # STUDENT MODE CLASS
            # =================================================

            if hasattr(
                announcements,
                "AnnouncementsWindow"
            ):

                try:

                    window = announcements.AnnouncementsWindow(
                        parent=self,
                        student_mode=True
                    )

                    window.focus_force()

                    return

                except TypeError:

                    pass

            # =================================================
            # FUNCTION NOT FOUND
            # =================================================

            messagebox.showwarning(
                "Announcements",
                "Student announcements are not available yet.\n\n"
                "Please make sure announcements.py contains:\n\n"
                "open_student_announcements(parent=self)",
                parent=self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Announcements Error",
                "announcements.py was not found.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Announcements Error",
                f"Unable to open Announcements.\n\n{e}",
                parent=self
            )

    # =====================================================
    # EVENTS
    # =====================================================

    def open_events(self):

        try:

            import events

            # =================================================
            # STUDENT EVENTS
            # =================================================

            if hasattr(
                events,
                "open_student_events"
            ):

                window = events.open_student_events(
                    parent=self
                )

                if window:

                    window.focus_force()

                return

            # =================================================
            # STUDENT MODE CLASS
            # =================================================

            if hasattr(
                events,
                "EventsWindow"
            ):

                try:

                    window = events.EventsWindow(
                        parent=self,
                        student_mode=True
                    )

                    window.focus_force()

                    return

                except TypeError:

                    pass

            # =================================================
            # FUNCTION NOT FOUND
            # =================================================

            messagebox.showwarning(
                "Events & Meetings",
                "Student Events are not available yet.\n\n"
                "Please make sure events.py contains:\n\n"
                "open_student_events(parent=self)",
                parent=self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Events Error",
                "events.py was not found.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Events Error",
                f"Unable to open Events & Meetings.\n\n{e}",
                parent=self
            )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh_portal(self):

        if self.database_id is None:

            return

        if not self.load_student():

            return

        # Destroy all existing widgets

        for widget in self.winfo_children():

            widget.destroy()

        # Rebuild

        self.create_ui()

        self.lift()

        self.focus_force()

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self
        )

        if not answer:

            return

        self.destroy()

        if self.parent:

            try:

                self.parent.deiconify()
                self.parent.lift()
                self.parent.focus_force()

            except Exception:
                pass

    # =====================================================
    # CLOSE
    # =====================================================

    def close_window(self):

        self.destroy()

        if self.parent:

            try:

                self.parent.deiconify()
                self.parent.lift()
                self.parent.focus_force()

            except Exception:
                pass


# =========================================================
# OPEN STUDENT PORTAL
# =========================================================

def open_student_portal(
    student_id=None,
    parent=None,
    student_data=None
):

    # =====================================================
    # GET ID FROM STUDENT DATA
    # =====================================================

    if student_id is None and student_data is not None:

        try:

            if isinstance(
                student_data,
                (tuple, list)
            ):

                student_id = student_data[0]

            elif isinstance(
                student_data,
                dict
            ):

                student_id = (
                    student_data.get("id")
                    or student_data.get("database_id")
                )

        except Exception:
            pass

    # =====================================================
    # VALIDATE
    # =====================================================

    if student_id is None:

        messagebox.showerror(
            "Student Portal",
            "Student database ID is missing."
        )

        return None

    # =====================================================
    # CREATE WINDOW
    # =====================================================

    window = StudentPortalWindow(
        parent=parent,
        student_id=student_id,
        student_data=student_data
    )

    try:

        window.deiconify()
        window.lift()
        window.focus_force()

    except Exception:
        pass

    return window


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    # =====================================================
    # CREATE MAIN APP
    # =====================================================

    app = ctk.CTk()

    app.withdraw()

    # =====================================================
    # FIND FIRST STUDENT AUTOMATICALLY
    # =====================================================

    try:

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM students ORDER BY id LIMIT 1"
        )

        result = cursor.fetchone()

        conn.close()

        if result:

            first_student_id = result[0]

            open_student_portal(
                student_id=first_student_id,
                parent=app
            )

        else:

            messagebox.showerror(
                "Student Portal",
                "No students were found in student.db."
            )

            app.destroy()

    except Exception as e:

        messagebox.showerror(
            "Student Portal Error",
            f"Unable to start Student Portal.\n\n{e}"
        )

        app.destroy()

    # =====================================================
    # MAIN LOOP
    # =====================================================

    app.mainloop()