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
# DASHBOARD
# =========================================================

class DashboardWindow(ctk.CTk):

    def __init__(self, username="Admin", role="Admin"):

        super().__init__()

        self.username = username
        self.role = role

        self.title("Student Management System")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.configure(
            fg_color="#F5F7FB"
        )

        self.create_ui()

        self.show_dashboard()

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_ui(self):

        # =================================================
        # SIDEBAR
        # =================================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#0F172A"
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # =================================================
        # LOGO
        # =================================================

        logo = ctk.CTkLabel(
            self.sidebar,
            text="🎓 Student\nManagement",
            text_color="white",
            justify="center",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        logo.pack(
            pady=(35, 30)
        )

        # =================================================
        # USER
        # =================================================

        user_label = ctk.CTkLabel(
            self.sidebar,
            text=f"👤 {self.username}",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        )

        user_label.pack(
            pady=(0, 20)
        )

        # =================================================
        # DASHBOARD
        # =================================================

        self.dashboard_button = self.create_sidebar_button(
            "🏠 Dashboard",
            self.show_dashboard
        )

        # =================================================
        # STUDENT MANAGEMENT
        # =================================================

        self.add_student_button = self.create_sidebar_button(
            "➕ Add Student",
            self.open_add_student
        )

        self.view_students_button = self.create_sidebar_button(
            "👥 View Students",
            self.open_view_students
        )

        self.update_student_button = self.create_sidebar_button(
            "✏️ Update Student",
            self.open_update_student
        )

        self.delete_student_button = self.create_sidebar_button(
            "🗑 Delete Student",
            self.open_delete_student
        )

        self.search_student_button = self.create_sidebar_button(
            "🔍 Search Student",
            self.open_search_student
        )

        # =================================================
        # ATTENDANCE
        # =================================================

        self.attendance_button = self.create_sidebar_button(
            "📅 Attendance",
            self.open_attendance
        )

        # =================================================
        # ATTENDANCE REPORT
        # =================================================

        self.attendance_report_button = self.create_sidebar_button(
            "📊 Attendance Report",
            self.open_attendance_report
        )

        # =================================================
        # EVENTS & MEETINGS
        # =================================================

        self.events_button = self.create_sidebar_button(
            "📅 Events & Meetings",
            self.open_events
        )

        # =================================================
        # ANNOUNCEMENTS
        # =================================================

        self.announcements_button = self.create_sidebar_button(
            "🔔 Announcements",
            self.open_announcements
        )

        # =================================================
        # COMMUNICATION
        # =================================================

        self.communication_button = self.create_sidebar_button(
            "📞 Calls & Chat",
            self.open_communication
        )

        # =================================================
        # LOGOUT
        # =================================================

        logout_button = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            height=45,
            corner_radius=8,
            fg_color="#7F1D1D",
            hover_color="#991B1B",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

        # =================================================
        # MAIN AREA
        # =================================================

        self.main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

    # =====================================================
    # SIDEBAR BUTTON
    # =====================================================

    def create_sidebar_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=43,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#E2E8F0",
            anchor="w",
            font=ctk.CTkFont(
                size=13
            ),
            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=3
        )

        return button

    # =====================================================
    # CLEAR MAIN
    # =====================================================

    def clear_main(self):

        for widget in self.main.winfo_children():

            widget.destroy()

    # =====================================================
    # DASHBOARD HOME
    # =====================================================

    def show_dashboard(self):

        self.clear_main()

        # =================================================
        # HEADER
        # =================================================

        title = ctk.CTkLabel(
            self.main,
            text="Welcome to Dashboard",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            pady=(5, 5)
        )

        subtitle = ctk.CTkLabel(
            self.main,
            text="Student Management System",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=14
            )
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 25)
        )

        # =================================================
        # STATISTICS
        # =================================================

        total_students, male, female, courses = (
            self.get_statistics()
        )

        stats_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x"
        )

        for column in range(4):

            stats_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.create_stat_card(
            stats_frame,
            0,
            "👥 Total Students",
            total_students
        )

        self.create_stat_card(
            stats_frame,
            1,
            "👨 Male Students",
            male
        )

        self.create_stat_card(
            stats_frame,
            2,
            "👩 Female Students",
            female
        )

        self.create_stat_card(
            stats_frame,
            3,
            "📚 Total Courses",
            courses
        )

        # =================================================
        # QUICK ACTIONS
        # =================================================

        quick_title = ctk.CTkLabel(
            self.main,
            text="Quick Actions",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        quick_title.pack(
            anchor="w",
            pady=(35, 15)
        )

        quick_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        quick_frame.pack(
            fill="x"
        )

        # 6 QUICK ACTION COLUMNS

        for column in range(6):

            quick_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =================================================
        # QUICK ACTION 1
        # =================================================

        self.create_quick_button(
            quick_frame,
            0,
            "➕ Add Student",
            self.open_add_student
        )

        # =================================================
        # QUICK ACTION 2
        # =================================================

        self.create_quick_button(
            quick_frame,
            1,
            "👥 View Students",
            self.open_view_students
        )

        # =================================================
        # QUICK ACTION 3
        # =================================================

        self.create_quick_button(
            quick_frame,
            2,
            "🔔 Announcements",
            self.open_announcements
        )

        # =================================================
        # QUICK ACTION 4
        # =================================================

        self.create_quick_button(
            quick_frame,
            3,
            "📅 Events",
            self.open_events
        )

        # =================================================
        # QUICK ACTION 5
        # =================================================

        self.create_quick_button(
            quick_frame,
            4,
            "📊 Attendance",
            self.open_attendance
        )

        # =================================================
        # QUICK ACTION 6
        # =================================================

        self.create_quick_button(
            quick_frame,
            5,
            "📞 Calls & Chat",
            self.open_communication
        )

        # =================================================
        # COMMUNICATION INFORMATION CARD
        # =================================================

        info = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15
        )

        info.pack(
            fill="x",
            pady=30
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            info,
            text="📢 Student Communication",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 8)
        )

        # -------------------------------------------------
        # DESCRIPTION
        # -------------------------------------------------

        ctk.CTkLabel(
            info,
            text=(
                "Teachers and students can communicate inside "
                "the system using Calls & Chat. No phone number "
                "is required. Student-to-student communication "
                "is restricted."
            ),
            text_color="#64748B",
            justify="left",
            wraplength=850,
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # -------------------------------------------------
        # OPEN COMMUNICATION BUTTON
        # -------------------------------------------------

        ctk.CTkButton(
            info,
            text="📞  Open Calls & Chat",
            width=200,
            height=42,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.open_communication
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # =====================================================
    # GET STATISTICS
    # =====================================================

    def get_statistics(self):

        conn = None

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            # -------------------------------------------------
            # TOTAL STUDENTS
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM students
            """)

            total_students = cursor.fetchone()[0]

            # -------------------------------------------------
            # MALE
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM students
                WHERE UPPER(gender) = 'MALE'
            """)

            male = cursor.fetchone()[0]

            # -------------------------------------------------
            # FEMALE
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM students
                WHERE UPPER(gender) = 'FEMALE'
            """)

            female = cursor.fetchone()[0]

            # -------------------------------------------------
            # COURSES
            # -------------------------------------------------

            cursor.execute("""
                SELECT COUNT(DISTINCT course)
                FROM students
                WHERE course IS NOT NULL
                AND course != ''
            """)

            courses = cursor.fetchone()[0]

            return (
                total_students,
                male,
                female,
                courses
            )

        except Exception:

            return (
                0,
                0,
                0,
                0
            )

        finally:

            if conn:

                conn.close()

    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value
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
            padx=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=(0, 20)
        )

    # =====================================================
    # QUICK BUTTON
    # =====================================================

    def create_quick_button(
        self,
        parent,
        column,
        text,
        command
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            height=55,
            corner_radius=10,
            fg_color="white",
            hover_color="#E2E8F0",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=command
        )

        button.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=4
        )

    # =====================================================
    # ADD STUDENT
    # =====================================================

    def open_add_student(self):

        try:

            import add_student

            add_student.open_add_student(
                self
            )

        except Exception as e:

            messagebox.showerror(
                "Add Student Error",
                f"Unable to open Add Student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # VIEW STUDENTS
    # =====================================================

    def open_view_students(self):

        try:

            import view_students

            view_students.open_view_students(
                self
            )

        except Exception as e:

            messagebox.showerror(
                "View Students Error",
                f"Unable to open View Students.\n\n{e}",
                parent=self
            )

    # =====================================================
    # UPDATE STUDENT
    # =====================================================

    def open_update_student(self):

        try:

            import update_student

            update_student.open_update_student(
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Update Student Error",
                f"Unable to open Update Student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # DELETE STUDENT
    # =====================================================

    def open_delete_student(self):

        try:

            import delete_student

            delete_student.open_delete_student(
                self
            )

        except Exception as e:

            messagebox.showerror(
                "Delete Student Error",
                f"Unable to open Delete Student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # SEARCH STUDENT
    # =====================================================

    def open_search_student(self):

        try:

            import search_student

            search_student.open_search_student(
                self
            )

        except Exception as e:

            messagebox.showerror(
                "Search Student Error",
                f"Unable to open Search Student.\n\n{e}",
                parent=self
            )

    # =====================================================
    # ATTENDANCE
    # =====================================================

    def open_attendance(self):

        try:

            import attendance

            if hasattr(
                attendance,
                "open_attendance"
            ):

                attendance.open_attendance(
                    self
                )

            else:

                messagebox.showwarning(
                    "Attendance",
                    "The open_attendance function "
                    "was not found in attendance.py.",
                    parent=self
                )

        except ModuleNotFoundError:

            messagebox.showwarning(
                "Attendance",
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
    # ATTENDANCE REPORT
    # =====================================================

    def open_attendance_report(self):

        try:

            import attendance_report

            attendance_report.open_attendance_report(
                self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Attendance Report Error",
                "attendance_report.py was not found.\n\n"
                "Make sure attendance_report.py is inside "
                "the StudentManagementSystem folder.",
                parent=self
            )

        except AttributeError:

            messagebox.showerror(
                "Attendance Report Error",
                "The function "
                "'open_attendance_report()' "
                "was not found in attendance_report.py.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Attendance Report Error",
                f"Unable to open Attendance Report.\n\n{e}",
                parent=self
            )

    # =====================================================
    # EVENTS & MEETINGS
    # =====================================================

    def open_events(self):

        try:

            import events

            events.open_events(
                self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Events Error",
                "events.py was not found.\n\n"
                "Please make sure events.py is inside "
                "the StudentManagementSystem folder.",
                parent=self
            )

        except AttributeError:

            messagebox.showerror(
                "Events Error",
                "The function "
                "'open_events()' "
                "was not found in events.py.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Events Error",
                f"Unable to open Events & Meetings.\n\n{e}",
                parent=self
            )

    # =====================================================
    # ANNOUNCEMENTS
    # =====================================================

    def open_announcements(self):

        try:

            import announcements

            announcements.open_announcements(
                self
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Announcements Error",
                "announcements.py was not found.\n\n"
                "Please make sure announcements.py "
                "is inside the StudentManagementSystem folder.",
                parent=self
            )

        except AttributeError:

            messagebox.showerror(
                "Announcements Error",
                "The function "
                "'open_announcements()' "
                "was not found in announcements.py.",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Announcements Error",
                f"Unable to open Announcements.\n\n{e}",
                parent=self
            )

    # =====================================================
    # COMMUNICATION
    # =====================================================

    def open_communication(self):

        try:

            import communication

            # -------------------------------------------------
            # CHECK FUNCTION
            # -------------------------------------------------

            if not hasattr(
                communication,
                "open_communication"
            ):

                messagebox.showerror(
                    "Communication Error",
                    "The function "
                    "'open_communication()' "
                    "was not found in communication.py.\n\n"
                    "Please check communication.py.",
                    parent=self
                )

                return

            # -------------------------------------------------
            # OPEN COMMUNICATION
            # -------------------------------------------------

            communication.open_communication(
                parent=self,
                username=self.username,
                role=self.role
            )

        except ModuleNotFoundError:

            messagebox.showerror(
                "Communication Error",
                "communication.py was not found.\n\n"
                "Please make sure communication.py is inside "
                "the StudentManagementSystem folder.",
                parent=self
            )

        except TypeError as e:

            messagebox.showerror(
                "Communication Error",
                "The open_communication() function in "
                "communication.py does not match the expected "
                "arguments.\n\n"
                "Expected:\n"
                "open_communication(parent, username, role)\n\n"
                f"Details:\n{e}",
                parent=self
            )

        except Exception as e:

            messagebox.showerror(
                "Communication Error",
                f"Unable to open Calls & Chat.\n\n{e}",
                parent=self
            )

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


# =========================================================
# OPEN DASHBOARD
# =========================================================

def open_dashboard(
    username="Admin",
    role="Admin"
):

    app = DashboardWindow(
        username=username,
        role=role
    )

    app.mainloop()


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    open_dashboard(
        username="Admin",
        role="Admin"
    )