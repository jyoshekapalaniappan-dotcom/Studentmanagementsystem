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
# DATABASE SETUP
# =========================================================

def setup_announcements_database():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                announcement_date TEXT,
                message TEXT
            )
        """)

        cursor.execute(
            "PRAGMA table_info(announcements)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        if "title" not in columns:

            cursor.execute("""
                ALTER TABLE announcements
                ADD COLUMN title TEXT
            """)

        if (
            "announcement_date" not in columns
            and "date" not in columns
        ):

            cursor.execute("""
                ALTER TABLE announcements
                ADD COLUMN announcement_date TEXT
            """)

        if (
            "message" not in columns
            and "description" not in columns
        ):

            cursor.execute("""
                ALTER TABLE announcements
                ADD COLUMN message TEXT
            """)

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


# =========================================================
# GET DATE COLUMN
# =========================================================

def get_date_column():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:

        cursor.execute(
            "PRAGMA table_info(announcements)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        if "announcement_date" in columns:
            return "announcement_date"

        if "date" in columns:
            return "date"

        return "announcement_date"

    finally:

        conn.close()


# =========================================================
# GET MESSAGE COLUMN
# =========================================================

def get_message_column():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:

        cursor.execute(
            "PRAGMA table_info(announcements)"
        )

        columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        if "message" in columns:
            return "message"

        if "description" in columns:
            return "description"

        return "message"

    finally:

        conn.close()


# =========================================================
# ANNOUNCEMENTS WINDOW
# =========================================================

class AnnouncementsWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent=None,
        student_mode=False
    ):

        super().__init__(parent)

        self.parent = parent
        self.student_mode = student_mode

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        if self.student_mode:

            self.title(
                "Student Announcements"
            )

        else:

            self.title(
                "Announcements"
            )

        self.geometry(
            "1100x750"
        )

        self.minsize(
            900,
            600
        )

        self.configure(
            fg_color="#F5F7FB"
        )

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        try:

            setup_announcements_database()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to setup Announcements database.\n\n{e}",
                parent=self
            )

            self.destroy()

            return

        # -------------------------------------------------
        # CREATE UI
        # -------------------------------------------------

        self.create_ui()

        # -------------------------------------------------
        # LOAD
        # -------------------------------------------------

        self.load_announcements()

        # -------------------------------------------------
        # PARENT
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
            height=110,
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

        if self.student_mode:

            title_text = "📢  My Announcements"

            subtitle_text = (
                "View latest student announcements"
            )

        else:

            title_text = "📢  Announcements"

            subtitle_text = (
                "Create and manage student announcements"
            )

        ctk.CTkLabel(
            header,
            text=title_text,
            text_color="white",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=40
        )

        ctk.CTkLabel(
            header,
            text=subtitle_text,
            text_color="#CBD5E1",
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            side="left"
        )

        # =================================================
        # FULL PAGE SCROLL
        # =================================================

        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="#F5F7FB",
            corner_radius=0,
            scrollbar_button_color="#64748B",
            scrollbar_button_hover_color="#475569"
        )

        self.main_scroll.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # ADMIN FORM
        # =================================================

        if not self.student_mode:

            self.create_announcement_form()

        # =================================================
        # SEARCH
        # =================================================

        self.create_search_section()

        # =================================================
        # ANNOUNCEMENT AREA
        # =================================================

        self.announcements_area = ctk.CTkFrame(
            self.main_scroll,
            fg_color="transparent"
        )

        self.announcements_area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 30)
        )

        # -------------------------------------------------
        # MOUSE SCROLL
        # -------------------------------------------------

        self.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    # =====================================================
    # MOUSE WHEEL
    # =====================================================

    def on_mousewheel(self, event):

        try:

            self.main_scroll._parent_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        except Exception:

            pass

    # =====================================================
    # SEARCH SECTION
    # =====================================================

    def create_search_section(self):

        search_card = ctk.CTkFrame(
            self.main_scroll,
            fg_color="white",
            corner_radius=12
        )

        search_card.pack(
            fill="x",
            padx=30,
            pady=20
        )

        search_card.grid_columnconfigure(
            0,
            weight=1
        )

        self.search_entry = ctk.CTkEntry(
            search_card,
            height=45,
            corner_radius=8,
            placeholder_text=(
                "🔍 Search announcement or message..."
            )
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(18, 10),
            pady=15
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event:
            self.search_announcements()
        )

        ctk.CTkButton(
            search_card,
            text="⟳ Refresh",
            width=120,
            height=45,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.load_announcements
        ).grid(
            row=0,
            column=1,
            padx=(0, 18),
            pady=15
        )

    # =====================================================
    # CREATE FORM
    # =====================================================

    def create_announcement_form(self):

        create_card = ctk.CTkFrame(
            self.main_scroll,
            fg_color="white",
            corner_radius=15
        )

        create_card.pack(
            fill="x",
            padx=30,
            pady=20
        )

        create_card.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        ctk.CTkLabel(
            create_card,
            text="➕  Create New Announcement",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(25, 20)
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        self.title_entry = self.create_entry(
            create_card,
            "Announcement Title *",
            1,
            0,
            "Example: Student Orientation Programme"
        )

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        self.date_entry = self.create_entry(
            create_card,
            "Date *",
            1,
            1,
            "DD-MM-YYYY"
        )

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        message_frame = ctk.CTkFrame(
            create_card,
            fg_color="transparent"
        )

        message_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            message_frame,
            text="Announcement Message *",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.message_entry = ctk.CTkTextbox(
            message_frame,
            height=110,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        self.message_entry.pack(
            fill="x"
        )

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            create_card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(10, 25)
        )

        ctk.CTkButton(
            button_frame,
            text="➕  Create Announcement",
            width=240,
            height=48,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.create_announcement
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            button_frame,
            text="Clear",
            width=120,
            height=48,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.clear_form
        ).pack(
            side="left"
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
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text=label_text,
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        entry = ctk.CTkEntry(
            frame,
            height=45,
            corner_radius=8,
            placeholder_text=placeholder
        )

        entry.pack(
            fill="x"
        )

        return entry

    # =====================================================
    # CREATE ANNOUNCEMENT
    # =====================================================

    def create_announcement(self):

        if self.student_mode:

            messagebox.showwarning(
                "Permission Denied",
                "Students cannot create announcements.",
                parent=self
            )

            return

        title = self.title_entry.get().strip()

        announcement_date = (
            self.date_entry.get().strip()
        )

        message = (
            self.message_entry
            .get("1.0", "end")
            .strip()
        )

        if not title:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement title.",
                parent=self
            )

            self.title_entry.focus()

            return

        if not announcement_date:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement date.",
                parent=self
            )

            self.date_entry.focus()

            return

        if not message:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement message.",
                parent=self
            )

            self.message_entry.focus()

            return

        conn = None

        try:

            date_column = get_date_column()
            message_column = get_message_column()

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            query = f"""
                INSERT INTO announcements
                (
                    title,
                    {date_column},
                    {message_column}
                )
                VALUES (?, ?, ?)
            """

            cursor.execute(
                query,
                (
                    title,
                    announcement_date,
                    message
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Announcement created successfully.",
                parent=self
            )

            self.clear_form()

            self.load_announcements()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to create announcement.\n\n{e}",
                parent=self
            )

        finally:

            if conn:
                conn.close()

    # =====================================================
    # LOAD ANNOUNCEMENTS
    # =====================================================

    def load_announcements(self):

        if not hasattr(
            self,
            "announcements_area"
        ):
            return

        self.clear_announcements()

        conn = None

        try:

            date_column = get_date_column()
            message_column = get_message_column()

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            query = f"""
                SELECT
                    id,
                    title,
                    {date_column},
                    {message_column}
                FROM announcements
                ORDER BY id DESC
            """

            cursor.execute(query)

            announcements = cursor.fetchall()

            if not announcements:

                self.show_empty_message(
                    "📢 No announcements available."
                )

                return

            for announcement in announcements:

                self.create_announcement_card(
                    announcement
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load announcements.\n\n{e}",
                parent=self
            )

        finally:

            if conn:
                conn.close()

    # =====================================================
    # SEARCH
    # =====================================================

    def search_announcements(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        self.clear_announcements()

        conn = None

        try:

            date_column = get_date_column()
            message_column = get_message_column()

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            if search_text:

                value = f"%{search_text}%"

                query = f"""
                    SELECT
                        id,
                        title,
                        {date_column},
                        {message_column}
                    FROM announcements
                    WHERE
                        title LIKE ?
                        OR {date_column} LIKE ?
                        OR {message_column} LIKE ?
                    ORDER BY id DESC
                """

                cursor.execute(
                    query,
                    (
                        value,
                        value,
                        value
                    )
                )

            else:

                query = f"""
                    SELECT
                        id,
                        title,
                        {date_column},
                        {message_column}
                    FROM announcements
                    ORDER BY id DESC
                """

                cursor.execute(query)

            announcements = cursor.fetchall()

            if not announcements:

                self.show_empty_message(
                    "No matching announcements found."
                )

                return

            for announcement in announcements:

                self.create_announcement_card(
                    announcement
                )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Unable to search announcements.\n\n{e}",
                parent=self
            )

        finally:

            if conn:
                conn.close()

    # =====================================================
    # ANNOUNCEMENT CARD
    # =====================================================

    def create_announcement_card(
        self,
        announcement
    ):

        (
            announcement_id,
            title,
            announcement_date,
            message
        ) = announcement

        # -------------------------------------------------
        # CARD
        # -------------------------------------------------

        card = ctk.CTkFrame(
            self.announcements_area,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=5,
            pady=10
        )

        # =================================================
        # TOP
        # =================================================

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=25,
            pady=(25, 12)
        )

        # -------------------------------------------------
        # BIG TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            top,
            text=f"📢  {title or 'Untitled Announcement'}",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            anchor="w",
            justify="left",
            wraplength=750
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

        # -------------------------------------------------
        # ID
        # -------------------------------------------------

        ctk.CTkLabel(
            top,
            text=f"Announcement #{announcement_id}",
            text_color="#2563EB",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="right",
            padx=(10, 0)
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
            padx=25
        )

        # =================================================
        # DATE
        # =================================================

        date_frame = ctk.CTkFrame(
            card,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        date_frame.pack(
            fill="x",
            padx=25,
            pady=18
        )

        ctk.CTkLabel(
            date_frame,
            text="📅  Announcement Date",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            date_frame,
            text=announcement_date or "-",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        # =================================================
        # MESSAGE
        # =================================================

        message_frame = ctk.CTkFrame(
            card,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        message_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 18)
        )

        ctk.CTkLabel(
            message_frame,
            text="📢  Announcement Message",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 5)
        )

        ctk.CTkLabel(
            message_frame,
            text=message or "-",
            text_color="#334155",
            font=ctk.CTkFont(
                size=15
            ),
            anchor="w",
            justify="left",
            wraplength=900
        ).pack(
            anchor="w",
            fill="x",
            padx=18,
            pady=(0, 18)
        )

        # =================================================
        # STUDENT MODE
        # =================================================

        if self.student_mode:

            ctk.CTkLabel(
                card,
                text="👁  View Only",
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                anchor="e",
                padx=25,
                pady=(0, 20)
            )

        # =================================================
        # ADMIN ACTION BUTTONS
        # =================================================

        else:

            action_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            action_frame.pack(
                fill="x",
                padx=25,
                pady=(0, 20)
            )

            # -------------------------------------------------
            # DELETE
            # -------------------------------------------------

            ctk.CTkButton(
                action_frame,
                text="🗑 Delete",
                width=110,
                height=38,
                corner_radius=7,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda aid=announcement_id:
                self.delete_announcement(aid)
            ).pack(
                side="right",
                padx=(10, 0)
            )

            # -------------------------------------------------
            # EDIT
            # -------------------------------------------------

            ctk.CTkButton(
                action_frame,
                text="✏ Edit",
                width=110,
                height=38,
                corner_radius=7,
                fg_color="#F59E0B",
                hover_color="#D97706",
                command=lambda aid=announcement_id:
                self.edit_announcement(aid)
            ).pack(
                side="right"
            )

    # =====================================================
    # EDIT ANNOUNCEMENT
    # =====================================================

    def edit_announcement(
        self,
        announcement_id
    ):

        if self.student_mode:

            messagebox.showwarning(
                "Permission Denied",
                "Students cannot edit announcements.",
                parent=self
            )

            return

        conn = None

        try:

            date_column = get_date_column()
            message_column = get_message_column()

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            query = f"""
                SELECT
                    id,
                    title,
                    {date_column},
                    {message_column}
                FROM announcements
                WHERE id = ?
            """

            cursor.execute(
                query,
                (announcement_id,)
            )

            announcement = cursor.fetchone()

            if not announcement:

                messagebox.showwarning(
                    "Not Found",
                    "Announcement was not found.",
                    parent=self
                )

                return

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load announcement.\n\n{e}",
                parent=self
            )

            return

        finally:

            if conn:
                conn.close()

        # =================================================
        # EDIT WINDOW
        # =================================================

        edit_window = ctk.CTkToplevel(self)

        edit_window.title(
            "Edit Announcement"
        )

        edit_window.geometry(
            "700x600"
        )

        edit_window.minsize(
            600,
            500
        )

        edit_window.configure(
            fg_color="#F5F7FB"
        )

        edit_window.transient(self)

        edit_window.grab_set()

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            edit_window,
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
            text="✏  Edit Announcement",
            text_color="white",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=30
        )

        # =================================================
        # CONTENT
        # =================================================

        content = ctk.CTkFrame(
            edit_window,
            fg_color="white",
            corner_radius=15
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        content.grid_columnconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            content,
            text="Announcement Title *",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 5)
        )

        edit_title = ctk.CTkEntry(
            content,
            height=45,
            corner_radius=8
        )

        edit_title.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 15)
        )

        edit_title.insert(
            0,
            announcement[1] or ""
        )

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        ctk.CTkLabel(
            content,
            text="Announcement Date *",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=25,
            pady=(5, 5)
        )

        edit_date = ctk.CTkEntry(
            content,
            height=45,
            corner_radius=8
        )

        edit_date.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 15)
        )

        edit_date.insert(
            0,
            announcement[2] or ""
        )

        # -------------------------------------------------
        # MESSAGE
        # -------------------------------------------------

        ctk.CTkLabel(
            content,
            text="Announcement Message *",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=25,
            pady=(5, 5)
        )

        edit_message = ctk.CTkTextbox(
            content,
            height=130,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        edit_message.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 20)
        )

        edit_message.insert(
            "1.0",
            announcement[3] or ""
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        button_frame.grid(
            row=6,
            column=0,
            sticky="e",
            padx=25,
            pady=(0, 25)
        )

        # -------------------------------------------------
        # CANCEL
        # -------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            height=45,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=edit_window.destroy
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="✓ Update Announcement",
            width=210,
            height=45,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=lambda:
            self.update_announcement(
                announcement_id,
                edit_title,
                edit_date,
                edit_message,
                edit_window
            )
        ).pack(
            side="left"
        )

        edit_title.focus()

    # =====================================================
    # UPDATE ANNOUNCEMENT
    # =====================================================

    def update_announcement(
        self,
        announcement_id,
        title_entry,
        date_entry,
        message_entry,
        edit_window
    ):

        title = (
            title_entry
            .get()
            .strip()
        )

        announcement_date = (
            date_entry
            .get()
            .strip()
        )

        message = (
            message_entry
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not title:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement title.",
                parent=edit_window
            )

            title_entry.focus()

            return

        if not announcement_date:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement date.",
                parent=edit_window
            )

            date_entry.focus()

            return

        if not message:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the announcement message.",
                parent=edit_window
            )

            message_entry.focus()

            return

        conn = None

        try:

            date_column = get_date_column()
            message_column = get_message_column()

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            query = f"""
                UPDATE announcements
                SET
                    title = ?,
                    {date_column} = ?,
                    {message_column} = ?
                WHERE id = ?
            """

            cursor.execute(
                query,
                (
                    title,
                    announcement_date,
                    message,
                    announcement_id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Found",
                    "Announcement was not found.",
                    parent=edit_window
                )

                return

            messagebox.showinfo(
                "Updated",
                "Announcement updated successfully.",
                parent=edit_window
            )

            edit_window.destroy()

            self.load_announcements()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Update Error",
                f"Unable to update announcement.\n\n{e}",
                parent=edit_window
            )

        finally:

            if conn:
                conn.close()

    # =====================================================
    # DELETE
    # =====================================================

    def delete_announcement(
        self,
        announcement_id
    ):

        if self.student_mode:

            messagebox.showwarning(
                "Permission Denied",
                "Students cannot delete announcements.",
                parent=self
            )

            return

        conn = None

        try:

            conn = sqlite3.connect(DB_FILE)

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT title
                FROM announcements
                WHERE id = ?
                """,
                (announcement_id,)
            )

            announcement = cursor.fetchone()

            if not announcement:

                messagebox.showwarning(
                    "Not Found",
                    "Announcement was not found.",
                    parent=self
                )

                return

            answer = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete:\n\n"
                f"{announcement[0]}\n\n"
                f"This action cannot be undone.",
                parent=self
            )

            if not answer:

                return

            cursor.execute(
                """
                DELETE FROM announcements
                WHERE id = ?
                """,
                (announcement_id,)
            )

            conn.commit()

            if cursor.rowcount > 0:

                messagebox.showinfo(
                    "Deleted",
                    "Announcement deleted successfully.",
                    parent=self
                )

                self.load_announcements()

            else:

                messagebox.showwarning(
                    "Not Found",
                    "Announcement was not found.",
                    parent=self
                )

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Delete Error",
                f"Unable to delete announcement.\n\n{e}",
                parent=self
            )

        finally:

            if conn:
                conn.close()

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        if self.student_mode:
            return

        self.title_entry.delete(
            0,
            "end"
        )

        self.date_entry.delete(
            0,
            "end"
        )

        self.message_entry.delete(
            "1.0",
            "end"
        )

    # =====================================================
    # CLEAR ANNOUNCEMENTS
    # =====================================================

    def clear_announcements(self):

        if not hasattr(
            self,
            "announcements_area"
        ):
            return

        for widget in (
            self.announcements_area.winfo_children()
        ):

            widget.destroy()

    # =====================================================
    # EMPTY MESSAGE
    # =====================================================

    def show_empty_message(
        self,
        text
    ):

        ctk.CTkLabel(
            self.announcements_area,
            text=text,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=18
            )
        ).pack(
            pady=60
        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close_window(self):

        try:

            self.unbind_all(
                "<MouseWheel>"
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
# ADMIN OPEN FUNCTION
# =========================================================

def open_announcements(
    parent=None
):

    window = AnnouncementsWindow(
        parent=parent,
        student_mode=False
    )

    window.focus_force()

    return window


# =========================================================
# STUDENT OPEN FUNCTION
# =========================================================

def open_student_announcements(
    parent=None
):

    window = AnnouncementsWindow(
        parent=parent,
        student_mode=True
    )

    window.focus_force()

    return window


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    app = ctk.CTk()

    app.withdraw()

    window = open_announcements(
        app
    )

    app.mainloop()