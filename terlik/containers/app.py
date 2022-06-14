from gi.repository import Gtk, Gio, Gdk
from terlik.containers.main import MainWindow

if settings := Gtk.Settings.get_default():
    settings.set_property("gtk-application-prefer-dark-theme", True)

MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.new</attribute>
        <attribute name="label" translatable="yes">New tab</attribute>
        <attribute name="accel">&lt;Primary&gt;t</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class App(Gtk.Application):
    __window: MainWindow = None

    def __init__(self, *args, **kwargs):
        Gtk.Application.__init__(self, *args, application_id="net.cacko.terlik", **kwargs)

    def do_activate(self):
        self.__window = MainWindow(self)
        self.__window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_new)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.__window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        print("quit")
        self.quit()

    def on_new(self, action, param):
        self.__window.add_terminal()
