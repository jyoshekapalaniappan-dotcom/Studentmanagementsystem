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

def setup_events_database():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:

        # -------------------------------------------------
        # Check whether events table exists
        # -------------------------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='events'
        """)

        exists = cursor.fetchone()

        # -------------------------------------------------
        # If table does not exist, create correct table
        # -------------------------------------------------

        if not exists:

            cursor.execute("""
                CREATE TABLE events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    event_date TEXT NOT NULL,
                    event_time TEXT,
                    venue TEXT,
                    description TEXT
                )
            """)

        else:

            # -------------------------------------------------
            # Read existing columns
            # -------------------------------------------------

            cursor.execute(
                "PRAGMA table_info(events)"
            )

            columns_info = cursor.fetchall()

            columns = [
                row[1]
                for row in columns_info
            ]

            # -------------------------------------------------
            # Add missing columns
            # -------------------------------------------------

            if "title" not in columns:

                cursor.execute("""
                    ALTER TABLE events
                    ADD COLUMN title TEXT
                """)

            if "event_date" not in columns:

                cursor.execute("""
                    ALTER TABLE events
                    ADD COLUMN event_date TEXT
                """)

            if "event_time" not in columns:

                cursor.execute("""
                    ALTER TABLE events
                    ADD COLUMN event_time TEXT
                """)

            if "venue" not in columns:

                cursor.execute("""
                    ALTER TABLE events
                    ADD COLUMN venue TEXT
                """)

            if "description" not in columns:

                cursor.execute("""
                    ALTER TABLE events
                    ADD COLUMN description TEXT
                """)

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()


# =========================================================
# EVENTS WINDOW
# =========================================================

class EventsWindow(ctk.CTkToplevel):

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

        if student_mode:

            self.title(
                "Student Events & Meetings"
            )

        else:

            self.title(
                "Events & Meetings"
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

            setup_events_database()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to setup Events database.\n\n{e}",
                parent=self
            )

            self.destroy()

            return

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.create_ui()

        self.load_events()

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
            height=110,
            corner_radius=0,
            fg_color="#1E293B"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        if self.student_mode:

            title_text = "📅  My Events & Meetings"

            subtitle_text = (
                "View upcoming student events and meetings"
            )

        else:

            title_text = "📅  Events & Meetings"

            subtitle_text = (
                "Create and manage student events"
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
        # ADMIN FORM
        # =================================================

        if not self.student_mode:

            self.create_event_form()

        # =================================================
        # SEARCH
        # =================================================

        search_card = ctk.CTkFrame(
            self,
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
                "🔍 Search event, venue or description..."
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
            lambda event: self.search_events()
        )

        ctk.CTkButton(
            search_card,
            text="⟳ Refresh",
            width=120,
            height=45,
            corner_radius=8,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.load_events
        ).grid(
            row=0,
            column=1,
            padx=(0, 18),
            pady=15
        )

        # =================================================
        # EVENTS
        # =================================================

        self.events_area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.events_area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

    # =====================================================
    # CREATE FORM
    # =====================================================

    def create_event_form(self):

        card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=30,
            pady=20
        )

        card.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        ctk.CTkLabel(
            card,
            text="➕  Create New Event / Meeting",
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

        # TITLE

        self.title_entry = self.create_entry(
            card,
            "Event / Meeting Title *",
            1,
            0,
            "Example: Student Meeting"
        )

        # DATE

        self.date_entry = self.create_entry(
            card,
            "Date *",
            1,
            1,
            "DD-MM-YYYY"
        )

        # TIME

        self.time_entry = self.create_entry(
            card,
            "Time",
            2,
            0,
            "Example: 10:30 AM"
        )

        # VENUE

        self.venue_entry = self.create_entry(
            card,
            "Venue",
            2,
            1,
            "Example: Seminar Hall"
        )

        # DESCRIPTION

        description_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        description_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            description_frame,
            text="Description",
            text_color="#334155",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.description_entry = ctk.CTkTextbox(
            description_frame,
            height=90,
            corner_radius=8,
            border_width=1,
            border_color="#CBD5E1"
        )

        self.description_entry.pack(
            fill="x"
        )

        # BUTTONS

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            padx=25,
            pady=(10, 25)
        )

        ctk.CTkButton(
            button_frame,
            text="➕  Create Event",
            width=190,
            height=48,
            corner_radius=8,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=self.create_event
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
    # ENTRY
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
    # CREATE EVENT
    # =====================================================

    def create_event(self):

        if self.student_mode:

            messagebox.showwarning(
                "Permission Denied",
                "Students cannot create events or meetings.",
                parent=self
            )

            return

        # -------------------------------------------------
        # GET VALUES
        # -------------------------------------------------

        title = self.title_entry.get().strip()

        event_date = self.date_entry.get().strip()

        event_time = self.time_entry.get().strip()

        venue = self.venue_entry.get().strip()

        description = self.description_entry.get(
            "1.0",
            "end"
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not title:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the event / meeting title.",
                parent=self
            )

            self.title_entry.focus()

            return

        if not event_date:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the event date.",
                parent=self
            )

            self.date_entry.focus()

            return

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        conn = None

        try:

            setup_events_database()

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            # -------------------------------------------------
            # IMPORTANT
            # Use event_date / event_time because your existing
            # database expects these column names.
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO events
                (
                    title,
                    event_date,
                    event_time,
                    venue,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    title,
                    event_date,
                    event_time,
                    venue,
                    description
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Event / Meeting created successfully.",
                parent=self
            )

            self.clear_form()

            self.load_events()

        except Exception as e:

            if conn:

                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to create event.\n\n{e}",
                parent=self
            )

        finally:

            if conn:

                conn.close()

    # =====================================================
    # LOAD EVENTS
    # =====================================================

    def load_events(self):

        if not hasattr(
            self,
            "events_area"
        ):

            return

        self.clear_events()

        conn = None

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    event_date,
                    event_time,
                    venue,
                    description
                FROM events
                ORDER BY id DESC
                """
            )

            events = cursor.fetchall()

            if not events:

                self.show_empty_message(
                    "📅 No events or meetings available."
                )

                return

            for event in events:

                self.create_event_card(
                    event
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load events.\n\n{e}",
                parent=self
            )

        finally:

            if conn:

                conn.close()

    # =====================================================
    # SEARCH
    # =====================================================

    def search_events(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        self.clear_events()

        conn = None

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            if search_text:

                value = f"%{search_text}%"

                cursor.execute(
                    """
                    SELECT
                        id,
                        title,
                        event_date,
                        event_time,
                        venue,
                        description
                    FROM events
                    WHERE
                        title LIKE ?
                        OR event_date LIKE ?
                        OR event_time LIKE ?
                        OR venue LIKE ?
                        OR description LIKE ?
                    ORDER BY id DESC
                    """,
                    (
                        value,
                        value,
                        value,
                        value,
                        value
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        title,
                        event_date,
                        event_time,
                        venue,
                        description
                    FROM events
                    ORDER BY id DESC
                    """
                )

            events = cursor.fetchall()

            if not events:

                self.show_empty_message(
                    "No matching events or meetings found."
                )

                return

            for event in events:

                self.create_event_card(
                    event
                )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Unable to search events.\n\n{e}",
                parent=self
            )

        finally:

            if conn:

                conn.close()

    # =====================================================
    # EVENT CARD
    # =====================================================

    def create_event_card(
        self,
        event
    ):

        (
            event_id,
            title,
            event_date,
            event_time,
            venue,
            description
        ) = event

        card = ctk.CTkFrame(
            self.events_area,
            fg_color="white",
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        # -------------------------------------------------
        # TOP
        # -------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            top,
            text=f"📅  {title or 'Untitled Event'}",
            text_color="#0F172A",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            top,
            text=f"Event #{event_id}",
            text_color="#2563EB",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="right"
        )

        # -------------------------------------------------
        # LINE
        # -------------------------------------------------

        ctk.CTkFrame(
            card,
            height=1,
            fg_color="#E2E8F0"
        ).pack(
            fill="x",
            padx=20
        )

        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

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
            (0, 1, 2),
            weight=1
        )

        self.add_detail(
            details,
            "📅 Date",
            event_date,
            0,
            0
        )

        self.add_detail(
            details,
            "⏰ Time",
            event_time,
            0,
            1
        )

        self.add_detail(
            details,
            "📍 Venue",
            venue,
            0,
            2
        )

        # -------------------------------------------------
        # DESCRIPTION
        # -------------------------------------------------

        description_frame = ctk.CTkFrame(
            card,
            fg_color="#F8FAFC",
            corner_radius=10
        )

        description_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            description_frame,
            text="Description",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            description_frame,
            text=description or "-",
            text_color="#334155",
            justify="left",
            anchor="w",
            wraplength=850,
            font=ctk.CTkFont(
                size=13
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # STUDENT MODE
        # -------------------------------------------------

        if self.student_mode:

            ctk.CTkLabel(
                card,
                text="👁 View Only",
                text_color="#64748B",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                anchor="e",
                padx=20,
                pady=(0, 18)
            )

        # -------------------------------------------------
        # ADMIN DELETE
        # -------------------------------------------------

        else:

            action_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            action_frame.pack(
                fill="x",
                padx=20,
                pady=(0, 18)
            )

            ctk.CTkButton(
                action_frame,
                text="🗑 Delete",
                width=110,
                height=35,
                corner_radius=7,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda eid=event_id:
                self.delete_event(eid)
            ).pack(
                side="right"
            )

    # =====================================================
    # DETAIL
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
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            anchor="w",
            justify="left",
            wraplength=250
        ).pack(
            anchor="w",
            padx=12,
            pady=(2, 8)
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_event(
        self,
        event_id
    ):

        if self.student_mode:

            messagebox.showwarning(
                "Permission Denied",
                "Students cannot delete events or meetings.",
                parent=self
            )

            return

        conn = None

        try:

            conn = sqlite3.connect(
                DB_FILE
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT title
                FROM events
                WHERE id = ?
                """,
                (event_id,)
            )

            event = cursor.fetchone()

            if not event:

                messagebox.showwarning(
                    "Not Found",
                    "Event was not found.",
                    parent=self
                )

                return

            answer = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete:\n\n"
                f"{event[0]}\n\n"
                f"This action cannot be undone.",
                parent=self
            )

            if not answer:

                return

            cursor.execute(
                """
                DELETE FROM events
                WHERE id = ?
                """,
                (event_id,)
            )

            conn.commit()

            messagebox.showinfo(
                "Deleted",
                "Event / Meeting deleted successfully.",
                parent=self
            )

            self.load_events()

        except Exception as e:

            if conn:

                conn.rollback()

            messagebox.showerror(
                "Delete Error",
                f"Unable to delete event.\n\n{e}",
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

        self.time_entry.delete(
            0,
            "end"
        )

        self.venue_entry.delete(
            0,
            "end"
        )

        self.description_entry.delete(
            "1.0",
            "end"
        )

    # =====================================================
    # CLEAR EVENTS
    # =====================================================

    def clear_events(self):

        if not hasattr(
            self,
            "events_area"
        ):

            return

        for widget in self.events_area.winfo_children():

            widget.destroy()

    # =====================================================
    # EMPTY
    # =====================================================

    def show_empty_message(
        self,
        text
    ):

        ctk.CTkLabel(
            self.events_area,
            text=text,
            text_color="#64748B",
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            pady=60
        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close_window(self):

        self.destroy()

        if self.parent:

            try:

                self.parent.focus_force()

            except Exception:

                pass


# =========================================================
# ADMIN
# =========================================================

def open_events(
    parent=None
):

    window = EventsWindow(
        parent=parent,
        student_mode=False
    )

    window.focus_force()

    return window


# =========================================================
# STUDENT
# =========================================================

def open_student_events(
    parent=None
):

    window = EventsWindow(
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

    window = open_events(
        app
    )

    app.mainloop()