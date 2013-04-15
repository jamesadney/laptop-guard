class SessionManager(object):
    def __init__(self, bus_name, object_path, interface):
        self.bus_name = bus_name
        self.object_path = object_path
        self.interface = interface

SESSION_MANAGERS = [
    # GNOME
    SessionManager("org.gnome.SessionManager", "/org/gnome/SessionManager",
        "org.gnome.SessionManager"),

    # MATE
    SessionManager("org.mate.SessionManager", "/org/mate/SessionManager",
        "org.mate.SessionManager"),
]