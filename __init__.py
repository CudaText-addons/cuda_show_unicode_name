import os
import cudatext as app
from unicodedata import name

plugin_name = __name__
MYTAG = 101
BAR_H = app.app_proc(app.PROC_GET_MAIN_STATUSBAR, '')
enabled = True

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'plugins.ini')
section = 'show_unicode_name'


def bool_to_str(v): return '1' if v else '0'


def str_to_bool(s): return s=='1'


class Command:

    def __init__(self):
        global enabled

        # Read settings if config file exists. By default set to True
        if os.path.isfile(fn_config):
            enabled = str_to_bool(app.ini_read(fn_config, section, 'enabled', '1'))

        self.set_enabled()

    def on_caret(self, ed_self):
        self.process_unicode(ed_self)

    def on_start(self, ed_self):
        # Created to initilize this plugin config
        pass

    def msg(self, s):
        app.statusbar_proc(BAR_H, app.STATUSBAR_SET_CELL_TEXT, tag=MYTAG, value=s)

    def set_enabled(self):
        if enabled:
            app.statusbar_proc(BAR_H, app.STATUSBAR_ADD_CELL, index=0, tag=MYTAG)
            app.statusbar_proc(BAR_H, app.STATUSBAR_SET_CELL_AUTOSIZE, tag=MYTAG, value=True)
            app.app_proc(app.PROC_SET_EVENTS, plugin_name + ';' + 'on_caret,' + ';;')
            self.process_unicode(app.ed)
        else:
            app.statusbar_proc(BAR_H, app.STATUSBAR_DELETE_CELL, tag=MYTAG)

    def toggle_display(self):
        global enabled

        enabled = not enabled
        app.ini_write(fn_config, section, 'enabled', bool_to_str(enabled))

        self.set_enabled()

    def process_unicode(self, ed_self):
        x, y, x1, y1 = ed_self.get_carets()[0]
        cnt = ed_self.get_line_count()
        if 0<=y<cnt:
            s = ed_self.get_text_line(y, 2000) #limit max len
            if x>=len(s):
                return self.msg('')
            s = s[x]
            s = ('U+%04x'%ord(s)).upper() +', '+ name(s, '?')
            self.msg(s)