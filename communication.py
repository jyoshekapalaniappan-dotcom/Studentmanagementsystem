import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox
from datetime import datetime


# =========================================================
# SETTINGS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "student.db")

REFRESH_MS = 1000


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =========================================================
# DATABASE SETUP
# =========================================================

def setup_communication_database():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # =================================================
        # COMMUNICATION USERS
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communication_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                role TEXT NOT NULL,
                UNIQUE(username, role)
            )
        """)

        # =================================================
        # CHAT MESSAGES
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                sender TEXT NOT NULL,
                sender_role TEXT NOT NULL,

                receiver TEXT NOT NULL,
                receiver_role TEXT NOT NULL,

                message TEXT NOT NULL,

                sent_at TEXT NOT NULL
            )
        """)

        # =================================================
        # CALL HISTORY
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS call_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                caller TEXT NOT NULL,
                caller_role TEXT NOT NULL,

                receiver TEXT NOT NULL,
                receiver_role TEXT NOT NULL,

                call_type TEXT NOT NULL,
                call_status TEXT NOT NULL,

                call_time TEXT NOT NULL
            )
        """)

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


# =========================================================
# GET TABLE COLUMNS
# =========================================================

def get_table_columns(table_name):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            f'PRAGMA table_info("{table_name}")'
        )

        return [
            row[1]
            for row in cursor.fetchall()
        ]

    except Exception:

        return []

    finally:

        conn.close()


# =========================================================
# GET STUDENT NAMES
# =========================================================

def get_student_names():

    names = []

    conn = get_connection()
    cursor = conn.cursor()

    try:

        columns = get_table_columns("students")

        if not columns:
            return names

        # -------------------------------------------------
        # Possible student-name columns
        # -------------------------------------------------

        name_column = None

        for column in [
            "name",
            "student_name",
            "full_name",
            "username",
            "studentname"
        ]:

            if column in columns:

                name_column = column
                break

        if not name_column:
            return names

        query = f"""
            SELECT "{name_column}"
            FROM students
            WHERE "{name_column}" IS NOT NULL
            AND TRIM("{name_column}") != ''
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        for row in rows:

            if row[0]:

                name = str(row[0]).strip()

                if name and name not in names:

                    names.append(name)

    except Exception:

        pass

    finally:

        conn.close()

    return names


# =========================================================
# GET TEACHER / ADMIN USERS
# =========================================================

def get_teacher_users():

    users = []

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = [
            row[0]
            for row in cursor.fetchall()
        ]

        # -------------------------------------------------
        # Look for user/account table
        # -------------------------------------------------

        possible_tables = [
            "users",
            "user",
            "accounts",
            "login",
            "teachers"
        ]

        selected_table = None

        for table in possible_tables:

            if table in tables:

                selected_table = table
                break

        if not selected_table:

            return users

        columns = get_table_columns(
            selected_table
        )

        username_column = None
        role_column = None

        for column in [
            "username",
            "user",
            "name",
            "full_name"
        ]:

            if column in columns:

                username_column = column
                break

        for column in [
            "role",
            "user_role",
            "type"
        ]:

            if column in columns:

                role_column = column
                break

        # -------------------------------------------------
        # If role exists
        # -------------------------------------------------

        if username_column and role_column:

            query = f"""
                SELECT
                    "{username_column}",
                    "{role_column}"
                FROM "{selected_table}"
                WHERE LOWER("{role_column}") IN
                    ('teacher', 'admin')
            """

            cursor.execute(query)

            for row in cursor.fetchall():

                if row[0]:

                    users.append({
                        "username": str(row[0]),
                        "role": str(row[1]).title()
                    })

        # -------------------------------------------------
        # Teacher table without role
        # -------------------------------------------------

        elif username_column:

            query = f"""
                SELECT "{username_column}"
                FROM "{selected_table}"
            """

            cursor.execute(query)

            for row in cursor.fetchall():

                if row[0]:

                    users.append({
                        "username": str(row[0]),
                        "role": "Teacher"
                    })

    except Exception:

        pass

    finally:

        conn.close()

    return users


# =========================================================
# GET CONTACTS
# =========================================================

def get_contacts(username, role):

    contacts = []

    current_role = str(role).strip().lower()

    # =====================================================
    # STUDENT
    # =====================================================

    if current_role == "student":

        teachers = get_teacher_users()

        for teacher in teachers:

            if (
                teacher["username"].lower()
                != username.lower()
            ):

                contacts.append(
                    teacher
                )

        # -------------------------------------------------
        # If no teacher table was found,
        # show Admin as fallback
        # -------------------------------------------------

        if not contacts:

            if username.lower() != "admin":

                contacts.append({
                    "username": "Admin",
                    "role": "Admin"
                })

    # =====================================================
    # TEACHER / ADMIN
    # =====================================================

    else:

        students = get_student_names()

        for student in students:

            if (
                student.lower()
                != username.lower()
            ):

                contacts.append({
                    "username": student,
                    "role": "Student"
                })

    return contacts


# =========================================================
# COMMUNICATION WINDOW
# =========================================================

class CommunicationWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent=None,
        username="Admin",
        role="Admin"
    ):

        super().__init__(parent)

        self.parent = parent

        self.username = str(username)
        self.role = str(role)

        self.selected_contact = None

        self.refresh_job = None

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.title(
            "Calls & Chat"
        )

        self.geometry(
            "1200x760"
        )

        self.minsize(
            950,
            600
        )

        self.configure(
            fg_color="#F5F7FB"
        )

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        try:

            setup_communication_database()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to setup communication database.\n\n{e}",
                parent=self
            )

            self.destroy()
            return

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.create_ui()

        self.load_contacts()

        self.start_refresh()

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

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self,
            height=85,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📞  Calls & Chat",
            text_color="white",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=30
        )

        ctk.CTkLabel(
            header,
            text=f"👤 {self.username}   •   {self.role}",
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="right",
            padx=30
        )

        # =================================================
        # CONTENT
        # =================================================

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =================================================
        # CONTACT PANEL
        # =================================================

        contacts_card = ctk.CTkFrame(
            content,
            width=300,
            fg_color="white",
            corner_radius=15
        )

        contacts_card.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        contacts_card.pack_propagate(False)

        ctk.CTkLabel(
            contacts_card,
            text="👥 Contacts",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            contacts_card,
            text="Available communication contacts",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.contacts_area = ctk.CTkScrollableFrame(
            contacts_card,
            fg_color="transparent"
        )

        self.contacts_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # =================================================
        # CHAT CARD
        # =================================================

        chat_card = ctk.CTkFrame(
            content,
            fg_color="white",
            corner_radius=15
        )

        chat_card.pack(
            side="right",
            fill="both",
            expand=True
        )

        # =================================================
        # CHAT HEADER
        # =================================================

        chat_header = ctk.CTkFrame(
            chat_card,
            height=70,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        chat_header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        chat_header.pack_propagate(False)

        self.contact_label = ctk.CTkLabel(
            chat_header,
            text="Select a contact first",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.contact_label.pack(
            side="left",
            padx=15
        )

        self.call_button = ctk.CTkButton(
            chat_header,
            text="📞 Call",
            width=100,
            height=38,
            corner_radius=8,
            fg_color="#16A34A",
            hover_color="#15803D",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.start_call,
            state="disabled"
        )

        self.call_button.pack(
            side="right",
            padx=10
        )

        # =================================================
        # MESSAGES
        # =================================================

        self.messages_area = ctk.CTkScrollableFrame(
            chat_card,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        self.messages_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =================================================
        # INPUT
        # =================================================

        input_frame = ctk.CTkFrame(
            chat_card,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        input_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        input_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.message_entry = ctk.CTkEntry(
            input_frame,
            height=45,
            corner_radius=8,
            placeholder_text="Select a contact and type your message..."
        )

        self.message_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(10, 5),
            pady=10
        )

        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        self.send_button = ctk.CTkButton(
            input_frame,
            text="➤ Send",
            width=100,
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.send_message,
            state="disabled"
        )

        self.send_button.grid(
            row=0,
            column=1,
            padx=(5, 10),
            pady=10
        )

    # =====================================================
    # LOAD CONTACTS
    # =====================================================

    def load_contacts(self):

        for widget in self.contacts_area.winfo_children():

            widget.destroy()

        contacts = get_contacts(
            self.username,
            self.role
        )

        if not contacts:

            ctk.CTkLabel(
                self.contacts_area,
                text=(
                    "No contacts found.\n\n"
                    "Please check your student/user database."
                ),
                text_color="#64748B",
                justify="center",
                font=ctk.CTkFont(
                    size=13
                )
            ).pack(
                pady=50
            )

            return

        for contact in contacts:

            self.create_contact(
                contact
            )

    # =====================================================
    # CONTACT BUTTON
    # =====================================================

    def create_contact(self, contact):

        username = contact["username"]
        role = contact["role"]

        button = ctk.CTkButton(
            self.contacts_area,
            text=f"👤  {username}\n     {role}",
            height=65,
            corner_radius=10,
            fg_color="#F8FAFC",
            hover_color="#E2E8F0",
            text_color="#0F172A",
            anchor="w",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=lambda:
            self.select_contact(
                username,
                role
            )
        )

        button.pack(
            fill="x",
            padx=5,
            pady=4
        )

    # =====================================================
    # SELECT CONTACT
    # =====================================================

    def select_contact(
        self,
        username,
        role
    ):

        # -------------------------------------------------
        # BLOCK STUDENT TO STUDENT
        # -------------------------------------------------

        if (
            self.role.lower() == "student"
            and role.lower() == "student"
        ):

            messagebox.showwarning(
                "Not Allowed",
                "Student-to-student communication is not allowed.",
                parent=self
            )

            return

        self.selected_contact = {
            "username": username,
            "role": role
        }

        self.contact_label.configure(
            text=f"👤  {username}   •   {role}"
        )

        self.send_button.configure(
            state="normal"
        )

        self.call_button.configure(
            state="normal"
        )

        self.message_entry.configure(
            placeholder_text=f"Message {username}..."
        )

        self.load_messages()

        self.message_entry.focus()

    # =====================================================
    # LOAD MESSAGES
    # =====================================================

    def load_messages(self):

        if not self.selected_contact:
            return

        contact = self.selected_contact

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    id,
                    sender,
                    sender_role,
                    receiver,
                    receiver_role,
                    message,
                    sent_at
                FROM chat_messages

                WHERE
                (
                    LOWER(sender) = LOWER(?)
                    AND LOWER(receiver) = LOWER(?)
                )

                OR

                (
                    LOWER(sender) = LOWER(?)
                    AND LOWER(receiver) = LOWER(?)
                )

                ORDER BY id ASC
                """,
                (
                    self.username,
                    contact["username"],
                    contact["username"],
                    self.username
                )
            )

            messages = cursor.fetchall()

        except Exception as e:

            conn.close()

            messagebox.showerror(
                "Chat Error",
                f"Unable to load messages.\n\n{e}",
                parent=self
            )

            return

        finally:

            try:
                conn.close()
            except:
                pass

        # -------------------------------------------------
        # CLEAR
        # -------------------------------------------------

        for widget in self.messages_area.winfo_children():

            widget.destroy()

        # -------------------------------------------------
        # EMPTY
        # -------------------------------------------------

        if not messages:

            ctk.CTkLabel(
                self.messages_area,
                text=(
                    "💬 No messages yet.\n\n"
                    "Send the first message."
                ),
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=14
                )
            ).pack(
                pady=100
            )

            return

        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        for row in messages:

            (
                message_id,
                sender,
                sender_role,
                receiver,
                receiver_role,
                message,
                sent_at
            ) = row

            self.create_message_bubble(
                sender,
                sender_role,
                message,
                sent_at
            )

        self.after(
            50,
            self.scroll_to_bottom
        )

    # =====================================================
    # MESSAGE BUBBLE
    # =====================================================

    def create_message_bubble(
        self,
        sender,
        sender_role,
        message,
        sent_at
    ):

        is_me = (
            sender.lower()
            == self.username.lower()
        )

        row = ctk.CTkFrame(
            self.messages_area,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        if is_me:

            bubble = ctk.CTkFrame(
                row,
                fg_color="#2563EB",
                corner_radius=12
            )

            bubble.pack(
                side="right",
                padx=(100, 5)
            )

            name = "You"

            text_color = "white"
            time_color = "#DBEAFE"

        else:

            bubble = ctk.CTkFrame(
                row,
                fg_color="#E2E8F0",
                corner_radius=12
            )

            bubble.pack(
                side="left",
                padx=(5, 100)
            )

            name = sender

            text_color = "#0F172A"
            time_color = "#64748B"

        ctk.CTkLabel(
            bubble,
            text=f"{name}  •  {sender_role}",
            text_color=(
                "#DBEAFE"
                if is_me
                else "#475569"
            ),
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(8, 2)
        )

        ctk.CTkLabel(
            bubble,
            text=message,
            text_color=text_color,
            justify="left",
            anchor="w",
            wraplength=550,
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 5)
        )

        ctk.CTkLabel(
            bubble,
            text=sent_at,
            text_color=time_color,
            font=ctk.CTkFont(
                size=9
            )
        ).pack(
            anchor="e",
            padx=12,
            pady=(0, 8)
        )

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send_message(
        self,
        event=None
    ):

        # -------------------------------------------------
        # CONTACT CHECK
        # -------------------------------------------------

        if not self.selected_contact:

            messagebox.showwarning(
                "Select Contact",
                "Please select a contact first.",
                parent=self
            )

            return "break"

        message = (
            self.message_entry
            .get()
            .strip()
        )

        if not message:

            return "break"

        contact = self.selected_contact

        # -------------------------------------------------
        # STUDENT → STUDENT BLOCK
        # -------------------------------------------------

        if (
            self.role.lower() == "student"
            and contact["role"].lower() == "student"
        ):

            messagebox.showwarning(
                "Not Allowed",
                "Students cannot chat with other students.",
                parent=self
            )

            return "break"

        conn = get_connection()
        cursor = conn.cursor()

        try:

            sent_at = datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )

            cursor.execute(
                """
                INSERT INTO chat_messages
                (
                    sender,
                    sender_role,
                    receiver,
                    receiver_role,
                    message,
                    sent_at
                )
                VALUES
                (?, ?, ?, ?, ?, ?)
                """,
                (
                    self.username,
                    self.role,
                    contact["username"],
                    contact["role"],
                    message,
                    sent_at
                )
            )

            conn.commit()

            # -------------------------------------------------
            # CLEAR INPUT
            # -------------------------------------------------

            self.message_entry.delete(
                0,
                "end"
            )

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Send Message Error",
                f"Unable to send message.\n\n{e}",
                parent=self
            )

        finally:

            conn.close()

        # -------------------------------------------------
        # SHOW MESSAGE IMMEDIATELY
        # -------------------------------------------------

        self.load_messages()

        return "break"

    # =====================================================
    # CALL
    # =====================================================

    def start_call(self):

        if not self.selected_contact:

            messagebox.showwarning(
                "Select Contact",
                "Please select a contact first.",
                parent=self
            )

            return

        contact = self.selected_contact

        # -------------------------------------------------
        # STUDENT → STUDENT BLOCK
        # -------------------------------------------------

        if (
            self.role.lower() == "student"
            and contact["role"].lower() == "student"
        ):

            messagebox.showwarning(
                "Not Allowed",
                "Students cannot call other students.",
                parent=self
            )

            return

        # -------------------------------------------------
        # SAVE CALL
        # -------------------------------------------------

        conn = get_connection()
        cursor = conn.cursor()

        try:

            call_time = datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )

            cursor.execute(
                """
                INSERT INTO call_history
                (
                    caller,
                    caller_role,
                    receiver,
                    receiver_role,
                    call_type,
                    call_status,
                    call_time
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.username,
                    self.role,
                    contact["username"],
                    contact["role"],
                    "Voice",
                    "Calling",
                    call_time
                )
            )

            conn.commit()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Call Error",
                f"Unable to start call.\n\n{e}",
                parent=self
            )

            return

        finally:

            conn.close()

        # -------------------------------------------------
        # OPEN CALL SCREEN
        # -------------------------------------------------

        self.open_call_screen(
            contact
        )

    # =====================================================
    # CALL SCREEN
    # =====================================================

    def open_call_screen(
        self,
        contact
    ):

        call_window = ctk.CTkToplevel(
            self
        )

        call_window.title(
            "Voice Call"
        )

        call_window.geometry(
            "500x520"
        )

        call_window.resizable(
            False,
            False
        )

        call_window.configure(
            fg_color="#0F172A"
        )

        call_window.transient(
            self
        )

        # -------------------------------------------------
        # ICON
        # -------------------------------------------------

        ctk.CTkLabel(
            call_window,
            text="📞",
            text_color="white",
            font=ctk.CTkFont(
                size=70
            )
        ).pack(
            pady=(65, 15)
        )

        # -------------------------------------------------
        # NAME
        # -------------------------------------------------

        ctk.CTkLabel(
            call_window,
            text=contact["username"],
            text_color="white",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack()

        # -------------------------------------------------
        # ROLE
        # -------------------------------------------------

        ctk.CTkLabel(
            call_window,
            text=contact["role"],
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=5
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        status_label = ctk.CTkLabel(
            call_window,
            text="Calling...",
            text_color="#94A3B8",
            font=ctk.CTkFont(
                size=15
            )
        )

        status_label.pack(
            pady=15
        )

        # -------------------------------------------------
        # END CALL
        # -------------------------------------------------

        def end_call():

            conn = get_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE call_history
                    SET call_status = ?
                    WHERE caller = ?
                    AND receiver = ?
                    AND call_status = 'Calling'
                    """,
                    (
                        "Ended",
                        self.username,
                        contact["username"]
                    )
                )

                conn.commit()

            except Exception:

                pass

            finally:

                conn.close()

            call_window.destroy()

        ctk.CTkButton(
            call_window,
            text="🔴  End Call",
            width=190,
            height=50,
            corner_radius=25,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=end_call
        ).pack(
            pady=55
        )

    # =====================================================
    # AUTO REFRESH
    # =====================================================

    def start_refresh(self):

        try:

            if not self.winfo_exists():

                return

            if self.selected_contact:

                self.load_messages()

            self.refresh_job = self.after(
                REFRESH_MS,
                self.start_refresh
            )

        except Exception:

            pass

    # =====================================================
    # SCROLL TO BOTTOM
    # =====================================================

    def scroll_to_bottom(self):

        try:

            self.messages_area._parent_canvas.yview_moveto(
                1.0
            )

        except Exception:

            pass

    # =====================================================
    # CLOSE
    # =====================================================

    def close_window(self):

        try:

            if self.refresh_job:

                self.after_cancel(
                    self.refresh_job
                )

        except Exception:

            pass

        self.destroy()

        if self.parent:

            try:

                self.parent.focus_force()

            except Exception:

                pass


# =========================================================
# OPEN COMMUNICATION
# =========================================================

def open_communication(
    parent=None,
    username="Admin",
    role="Admin"
):

    window = CommunicationWindow(
        parent=parent,
        username=username,
        role=role
    )

    window.focus_force()

    return window


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    window = open_communication(
        parent=app,
        username="Admin",
        role="Admin"
    )

    app.mainloop()