from gi.repository import Gtk, Vte, GLib, Pango
from os import environ
from uuid import uuid4


class Terminal(Gtk.Box):
    __terminal: Vte.Terminal = None
    __id: str = None
    __cmd: str = ""

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.__terminal = Vte.Terminal()
        self.__terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__terminal.set_cursor_shape(Vte.CursorShape.IBEAM)
        font = Pango.FontDescription()
        font.set_family("MesloLGS NF")
        font.set_size(15 * Pango.SCALE)

        self.__terminal.set_font(font)
        pty = Vte.Pty.new_sync(Vte.PtyFlags.DEFAULT)
        self.__terminal.set_pty(pty)
        self.__terminal.connect('commit', self.on_commit)

        pty.spawn_async(
            None,
            [environ.get("SHELL", "/bin/sh")],
            None,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None
        )

        scroller = Gtk.ScrolledWindow()
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(self.__terminal)
        self.pack_start(scroller, False, True, 0)

    def on_commit(self, vte, text: str, size: int, user_data=None):
        self.__cmd += text
        notebook = self.get_parent()
        if text == "\r":
            notebook.set_terminal_title(self, self.__cmd)
            self.__cmd = ""

    @property
    def current_directory(self) -> str:
        return self.__terminal.get_current_directory_uri()

    @property
    def id(self) -> str:
        if not self.__id:
            self.__id = uuid4().hex
        return self.__id
