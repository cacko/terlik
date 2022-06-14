from gi.repository import Gtk
from terlik.containers.app import App
import sys

if settings := Gtk.Settings.get_default():
    settings.set_property("gtk-application-prefer-dark-theme", True)

application = App()
exit_status = application.run(sys.argv)
sys.exit(exit_status)
