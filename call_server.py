# =========================================================
# call_server.py
# Student Management System
# Calls + Chat Server
# =========================================================

import socket
import threading
import json


# =========================================================
# SETTINGS
# =========================================================

HOST = "0.0.0.0"
PORT = 5000

MAX_CONNECTIONS = 50


# =========================================================
# CONNECTED USERS
# =========================================================
#
# Example:
#
# users = {
#     "Teacher1": {
#         "socket": client_socket,
#         "role": "Teacher"
#     },
#     "Student1": {
#         "socket": client_socket,
#         "role": "Student"
#     }
# }
#
# =========================================================

users = {}

users_lock = threading.Lock()


# =========================================================
# SEND MESSAGE
# =========================================================

def send_message(client_socket, data):

    try:

        message = json.dumps(
            data
        ) + "\n"

        client_socket.sendall(
            message.encode("utf-8")
        )

        return True

    except Exception as e:

        print(
            f"[SEND ERROR] {e}"
        )

        return False


# =========================================================
# REMOVE USER
# =========================================================

def remove_user(username):

    if not username:
        return

    with users_lock:

        user = users.pop(
            username,
            None
        )

    if user:

        try:

            user["socket"].shutdown(
                socket.SHUT_RDWR
            )

        except Exception:

            pass

        try:

            user["socket"].close()

        except Exception:

            pass

        print(
            f"[DISCONNECTED] {username}"
        )


# =========================================================
# GET ONLINE USERS
# =========================================================

def get_users():

    result = []

    with users_lock:

        for username, user in users.items():

            result.append(
                {
                    "username": username,
                    "role": user["role"]
                }
            )

    return result


# =========================================================
# SEND USER LIST TO EVERYONE
# =========================================================

def broadcast_user_list():

    message = {
        "type": "user_list",
        "users": get_users()
    }

    failed_users = []

    with users_lock:

        current_users = list(
            users.items()
        )

    for username, user in current_users:

        if not send_message(
            user["socket"],
            message
        ):

            failed_users.append(
                username
            )

    for username in failed_users:

        remove_user(
            username
        )


# =========================================================
# FIND USER
# =========================================================

def find_user(username):

    if not username:
        return None

    with users_lock:

        return users.get(
            username
        )


# =========================================================
# CHECK COMMUNICATION PERMISSION
# =========================================================

def can_communicate(
    caller_role,
    target_role
):

    caller_role = str(
        caller_role
    ).strip().title()

    target_role = str(
        target_role
    ).strip().title()

    # -----------------------------------------------------
    # STUDENT -> STUDENT
    # -----------------------------------------------------

    if (
        caller_role == "Student"
        and
        target_role == "Student"
    ):

        return False

    # -----------------------------------------------------
    # EVERYTHING ELSE
    # -----------------------------------------------------

    return True


# =========================================================
# HANDLE LOGIN
# =========================================================

def handle_login(
    client_socket,
    data
):

    username = str(
        data.get(
            "username",
            ""
        )
    ).strip()

    role = str(
        data.get(
            "role",
            "Student"
        )
    ).strip().title()

    # -----------------------------------------------------
    # USERNAME CHECK
    # -----------------------------------------------------

    if not username:

        send_message(
            client_socket,
            {
                "type": "error",
                "message": (
                    "Username is required."
                )
            }
        )

        return None

    # -----------------------------------------------------
    # ROLE CHECK
    # -----------------------------------------------------

    allowed_roles = (
        "Admin",
        "Teacher",
        "Student"
    )

    if role not in allowed_roles:

        send_message(
            client_socket,
            {
                "type": "error",
                "message": (
                    "Invalid role. "
                    "Use Admin, Teacher or Student."
                )
            }
        )

        return None

    # -----------------------------------------------------
    # DUPLICATE LOGIN CHECK
    # -----------------------------------------------------

    with users_lock:

        if username in users:

            send_message(
                client_socket,
                {
                    "type": "login_error",
                    "message": (
                        "This username is already "
                        "connected."
                    )
                }
            )

            return None

        # -------------------------------------------------
        # ADD USER
        # -------------------------------------------------

        users[username] = {
            "socket": client_socket,
            "role": role
        }

    # -----------------------------------------------------
    # LOGIN SUCCESS
    # -----------------------------------------------------

    send_message(
        client_socket,
        {
            "type": "login_success",
            "username": username,
            "role": role
        }
    )

    print(
        f"[CONNECTED] "
        f"{username} "
        f"({role})"
    )

    # -----------------------------------------------------
    # UPDATE USER LIST
    # -----------------------------------------------------

    broadcast_user_list()

    return username


# =========================================================
# HANDLE GET USERS
# =========================================================

def handle_get_users(
    client_socket
):

    send_message(
        client_socket,
        {
            "type": "user_list",
            "users": get_users()
        }
    )


# =========================================================
# HANDLE CHAT MESSAGE
# =========================================================

def handle_chat_message(
    sender_username,
    data
):

    target_username = str(
        data.get(
            "target",
            ""
        )
    ).strip()

    message = str(
        data.get(
            "message",
            ""
        )
    ).strip()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not target_username:

        return

    if not message:

        return

    # -----------------------------------------------------
    # FIND SENDER
    # -----------------------------------------------------

    sender = find_user(
        sender_username
    )

    if not sender:

        return

    # -----------------------------------------------------
    # FIND TARGET
    # -----------------------------------------------------

    target = find_user(
        target_username
    )

    if not target:

        send_message(
            sender["socket"],
            {
                "type": "chat_error",
                "message": (
                    f"{target_username} is not online."
                )
            }
        )

        return

    # -----------------------------------------------------
    # PERMISSION
    # -----------------------------------------------------

    if not can_communicate(
        sender["role"],
        target["role"]
    ):

        send_message(
            sender["socket"],
            {
                "type": "chat_error",
                "message": (
                    "Student-to-student chat "
                    "is not allowed."
                )
            }
        )

        return

    # -----------------------------------------------------
    # SEND TO TARGET
    # -----------------------------------------------------

    send_message(
        target["socket"],
        {
            "type": "chat_message",
            "from": sender_username,
            "from_role": sender["role"],
            "message": message
        }
    )

    # -----------------------------------------------------
    # SEND CONFIRMATION TO SENDER
    # -----------------------------------------------------

    send_message(
        sender["socket"],
        {
            "type": "chat_sent",
            "to": target_username,
            "message": message
        }
    )

    print(
        f"[CHAT] "
        f"{sender_username} -> "
        f"{target_username}: "
        f"{message}"
    )


# =========================================================
# HANDLE CALL REQUEST
# =========================================================

def handle_call_request(
    caller_username,
    data
):

    target_username = str(
        data.get(
            "target",
            ""
        )
    ).strip()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not target_username:

        return

    # -----------------------------------------------------
    # CALLER
    # -----------------------------------------------------

    caller = find_user(
        caller_username
    )

    if not caller:

        return

    # -----------------------------------------------------
    # TARGET
    # -----------------------------------------------------

    target = find_user(
        target_username
    )

    if not target:

        send_message(
            caller["socket"],
            {
                "type": "call_error",
                "message": (
                    f"{target_username} is not online."
                )
            }
        )

        return

    # -----------------------------------------------------
    # SAME USER
    # -----------------------------------------------------

    if (
        caller_username
        ==
        target_username
    ):

        send_message(
            caller["socket"],
            {
                "type": "call_error",
                "message": (
                    "You cannot call yourself."
                )
            }
        )

        return

    # -----------------------------------------------------
    # PERMISSION
    # -----------------------------------------------------

    if not can_communicate(
        caller["role"],
        target["role"]
    ):

        send_message(
            caller["socket"],
            {
                "type": "call_error",
                "message": (
                    "Student-to-student calls "
                    "are not allowed."
                )
            }
        )

        return

    # -----------------------------------------------------
    # SEND INCOMING CALL
    # -----------------------------------------------------

    send_message(
        target["socket"],
        {
            "type": "incoming_call",
            "from": caller_username,
            "from_role": caller["role"]
        }
    )

    # -----------------------------------------------------
    # SEND RINGING
    # -----------------------------------------------------

    send_message(
        caller["socket"],
        {
            "type": "call_ringing",
            "target": target_username
        }
    )

    print(
        f"[CALL] "
        f"{caller_username} -> "
        f"{target_username}"
    )


# =========================================================
# HANDLE CALL RESPONSE
# =========================================================

def handle_call_response(
    username,
    data
):

    target_username = str(
        data.get(
            "target",
            ""
        )
    ).strip()

    response = str(
        data.get(
            "response",
            ""
        )
    ).strip().lower()

    # -----------------------------------------------------
    # FIND USERS
    # -----------------------------------------------------

    responder = find_user(
        username
    )

    caller = find_user(
        target_username
    )

    if not responder or not caller:

        return

    # -----------------------------------------------------
    # ACCEPT
    # -----------------------------------------------------

    if response == "accepted":

        send_message(
            caller["socket"],
            {
                "type": "call_accepted",
                "by": username
            }
        )

        print(
            f"[CALL ACCEPTED] "
            f"{username} accepted "
            f"{target_username}"
        )

    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    elif response == "rejected":

        send_message(
            caller["socket"],
            {
                "type": "call_rejected",
                "by": username
            }
        )

        print(
            f"[CALL REJECTED] "
            f"{username} rejected "
            f"{target_username}"
        )


# =========================================================
# HANDLE HANGUP
# =========================================================

def handle_hangup(
    username,
    data
):

    target_username = str(
        data.get(
            "target",
            ""
        )
    ).strip()

    target = find_user(
        target_username
    )

    if not target:

        return

    send_message(
        target["socket"],
        {
            "type": "call_ended",
            "by": username
        }
    )

    print(
        f"[CALL ENDED] "
        f"{username} -> "
        f"{target_username}"
    )


# =========================================================
# HANDLE WEBRTC SIGNAL
# =========================================================
#
# Used later for:
#
# offer
# answer
# ice_candidate
#
# =========================================================

def handle_signal(
    username,
    data
):

    target_username = str(
        data.get(
            "target",
            ""
        )
    ).strip()

    sender = find_user(
        username
    )

    target = find_user(
        target_username
    )

    if not sender or not target:

        return

    # -----------------------------------------------------
    # PERMISSION
    # -----------------------------------------------------

    if not can_communicate(
        sender["role"],
        target["role"]
    ):

        send_message(
            sender["socket"],
            {
                "type": "signal_error",
                "message": (
                    "Student-to-student communication "
                    "is not allowed."
                )
            }
        )

        return

    # -----------------------------------------------------
    # ADD SENDER
    # -----------------------------------------------------

    signal_data = dict(
        data
    )

    signal_data["from"] = username

    # -----------------------------------------------------
    # FORWARD
    # -----------------------------------------------------

    send_message(
        target["socket"],
        signal_data
    )

    print(
        f"[SIGNAL] "
        f"{username} -> "
        f"{target_username} "
        f"({data.get('type')})"
    )


# =========================================================
# HANDLE PING
# =========================================================

def handle_ping(
    client_socket
):

    send_message(
        client_socket,
        {
            "type": "pong"
        }
    )


# =========================================================
# HANDLE CLIENT
# =========================================================

def handle_client(
    client_socket,
    address
):

    username = None

    print(
        f"[NEW CONNECTION] "
        f"{address}"
    )

    buffer = ""

    try:

        while True:

            # -------------------------------------------------
            # RECEIVE
            # -------------------------------------------------

            data = client_socket.recv(
                4096
            )

            if not data:

                break

            try:

                buffer += data.decode(
                    "utf-8"
                )

            except UnicodeDecodeError:

                send_message(
                    client_socket,
                    {
                        "type": "error",
                        "message": (
                            "Invalid data encoding."
                        )
                    }
                )

                continue

            # -------------------------------------------------
            # PROCESS COMPLETE MESSAGES
            # -------------------------------------------------

            while "\n" in buffer:

                line, buffer = buffer.split(
                    "\n",
                    1
                )

                line = line.strip()

                if not line:

                    continue

                # -------------------------------------------------
                # JSON
                # -------------------------------------------------

                try:

                    message = json.loads(
                        line
                    )

                except json.JSONDecodeError:

                    send_message(
                        client_socket,
                        {
                            "type": "error",
                            "message": (
                                "Invalid JSON message."
                            )
                        }
                    )

                    continue

                # -------------------------------------------------
                # MESSAGE TYPE
                # -------------------------------------------------

                message_type = message.get(
                    "type"
                )

                # =================================================
                # LOGIN
                # =================================================

                if message_type == "login":

                    if username is not None:

                        send_message(
                            client_socket,
                            {
                                "type": "error",
                                "message": (
                                    "You are already logged in."
                                )
                            }
                        )

                        continue

                    username = handle_login(
                        client_socket,
                        message
                    )

                    if username is None:

                        return

                # =================================================
                # REQUIRE LOGIN
                # =================================================

                elif username is None:

                    send_message(
                        client_socket,
                        {
                            "type": "error",
                            "message": (
                                "Please login first."
                            )
                        }
                    )

                # =================================================
                # GET USERS
                # =================================================

                elif message_type == "get_users":

                    handle_get_users(
                        client_socket
                    )

                # =================================================
                # CHAT
                # =================================================

                elif message_type == "chat_message":

                    handle_chat_message(
                        username,
                        message
                    )

                # =================================================
                # CALL REQUEST
                # =================================================

                elif message_type == "call_request":

                    handle_call_request(
                        username,
                        message
                    )

                # =================================================
                # CALL RESPONSE
                # =================================================

                elif message_type == "call_response":

                    handle_call_response(
                        username,
                        message
                    )

                # =================================================
                # HANGUP
                # =================================================

                elif message_type == "hangup":

                    handle_hangup(
                        username,
                        message
                    )

                # =================================================
                # WEBRTC OFFER
                # =================================================

                elif message_type == "offer":

                    handle_signal(
                        username,
                        message
                    )

                # =================================================
                # WEBRTC ANSWER
                # =================================================

                elif message_type == "answer":

                    handle_signal(
                        username,
                        message
                    )

                # =================================================
                # ICE CANDIDATE
                # =================================================

                elif message_type == "ice_candidate":

                    handle_signal(
                        username,
                        message
                    )

                # =================================================
                # PING
                # =================================================

                elif message_type == "ping":

                    handle_ping(
                        client_socket
                    )

                # =================================================
                # LOGOUT
                # =================================================

                elif message_type == "logout":

                    return

                # =================================================
                # UNKNOWN MESSAGE
                # =================================================

                else:

                    send_message(
                        client_socket,
                        {
                            "type": "error",
                            "message": (
                                "Unknown message type: "
                                f"{message_type}"
                            )
                        }
                    )

    except ConnectionResetError:

        print(
            f"[CONNECTION RESET] "
            f"{address}"
        )

    except BrokenPipeError:

        print(
            f"[BROKEN PIPE] "
            f"{address}"
        )

    except Exception as e:

        print(
            f"[CLIENT ERROR] "
            f"{address}: {e}"
        )

    finally:

        # -------------------------------------------------
        # REMOVE USER
        # -------------------------------------------------

        if username:

            remove_user(
                username
            )

            broadcast_user_list()

        # -------------------------------------------------
        # CLOSE SOCKET
        # -------------------------------------------------

        try:

            client_socket.close()

        except Exception:

            pass

        print(
            f"[CONNECTION CLOSED] "
            f"{address}"
        )


# =========================================================
# START SERVER
# =========================================================

def start_server():

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # -----------------------------------------------------
    # REUSE ADDRESS
    # -----------------------------------------------------

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    # -----------------------------------------------------
    # BIND
    # -----------------------------------------------------

    try:

        server_socket.bind(
            (
                HOST,
                PORT
            )
        )

    except OSError as e:

        print()
        print(
            "ERROR: Could not start server."
        )
        print()
        print(
            f"Port {PORT} may already be in use."
        )
        print()
        print(
            f"Details: {e}"
        )

        server_socket.close()

        return

    # -----------------------------------------------------
    # LISTEN
    # -----------------------------------------------------

    server_socket.listen(
        MAX_CONNECTIONS
    )

    # =====================================================
    # SERVER INFORMATION
    # =====================================================

    print()
    print("=" * 65)
    print(
        " STUDENT MANAGEMENT SYSTEM"
    )
    print(
        " CALL & CHAT SERVER"
    )
    print("=" * 65)
    print()
    print(
        f"Server address : {HOST}"
    )
    print(
        f"Server port    : {PORT}"
    )
    print()
    print(
        "Communication permissions:"
    )
    print(
        "  Teacher  -> Student : ALLOWED"
    )
    print(
        "  Student  -> Teacher : ALLOWED"
    )
    print(
        "  Teacher  -> Teacher : ALLOWED"
    )
    print(
        "  Admin    -> Teacher : ALLOWED"
    )
    print(
        "  Admin    -> Student : ALLOWED"
    )
    print(
        "  Student  -> Student : BLOCKED"
    )
    print()
    print(
        "Chat server : READY"
    )
    print(
        "Call signaling : READY"
    )
    print()
    print(
        "Waiting for users..."
    )
    print()
    print(
        "Press CTRL+C to stop the server."
    )
    print("=" * 65)
    print()

    # =====================================================
    # ACCEPT CONNECTIONS
    # =====================================================

    try:

        while True:

            client_socket, address = (
                server_socket.accept()
            )

            # -------------------------------------------------
            # CREATE THREAD
            # -------------------------------------------------

            client_thread = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    address
                ),
                daemon=True
            )

            client_thread.start()

    except KeyboardInterrupt:

        print()
        print(
            "Stopping server..."
        )

    except Exception as e:

        print()
        print(
            f"[SERVER ERROR] {e}"
        )

    finally:

        # =================================================
        # CLOSE ALL USERS
        # =================================================

        with users_lock:

            connected_users = list(
                users.values()
            )

            users.clear()

        for user in connected_users:

            try:

                user["socket"].shutdown(
                    socket.SHUT_RDWR
                )

            except Exception:

                pass

            try:

                user["socket"].close()

            except Exception:

                pass

        # =================================================
        # CLOSE SERVER
        # =================================================

        try:

            server_socket.close()

        except Exception:

            pass

        print()
        print(
            "Call server stopped."
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    start_server()