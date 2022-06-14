from gi.repository import Gtk, Gio, Gdk
from terlik.widgets.terminal import Terminal
from uuid import uuid4
from rich.console import Console

class TabContainer(Gtk.Notebook):
    __pages: dict[str, int] = {}

    def __int__(self, *args, **kwargs):
        Gtk.Notebook.__init__(self, *args, **kwargs)

    def add_terminal(self):
        page = Terminal()
        page.set_border_width(0)
        idx = self.append_page(page, tab_label=Gtk.Label(f"... [{len(self.__pages)}]"))
        self.__pages[page.id] = idx
        self.show_all()

    def set_terminal_title(self, terminal: Terminal, title: str):
        idx = self.__pages.get(terminal.id)
        tab = self.get_nth_page(idx)
        console = Console(record=True)
        console.print(title)

        self.set_tab_label(child=tab, tab_label=Gtk.Label(console.export_text()))


class MainWindow(Gtk.Window):
    __pages: dict[str, int] = {}
    __id: str = ""

    def __init__(self, app, title: str = "tERlik"):
        Gtk.Window.__init__(self, application=app)
        self.notebook = TabContainer()
        self.set_title(title)
        self.add(self.notebook)
        self.set_default_size(1000, 800)
        self.add_terminal()

    def add_terminal(self):
        self.notebook.add_terminal()

    @property
    def id(self) -> str:
        if not self.__id:
            self.__id = uuid4().hex
        return self.__id
