import os
import cudatext as app
from unicodedata import name

plugin_name = __name__
MYTAG = app.app_proc(app.PROC_GET_UNIQUE_TAG, '')
BAR_H = app.app_proc(app.PROC_GET_MAIN_STATUSBAR, '')

fn_config = os.path.join(app.app_path(app.APP_DIR_SETTINGS), 'plugins.ini')
section = 'show_unicode_name'

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    enabled = True

    def __init__(self):
        if os.path.isfile(fn_config):
            self.enabled = str_to_bool(app.ini_read(fn_config, section, 'enabled', '1'))

        self.set_enabled()

    def on_caret(self, ed_self):
        self.process_unicode(ed_self)

    def on_focus(self, ed_self):
        self.process_unicode(ed_self)

    def on_start(self, ed_self):
        # Created to initilize this plugin config
        pass

    def msg(self, s):
        app.statusbar_proc(BAR_H, app.STATUSBAR_SET_CELL_TEXT, tag=MYTAG, value=s)

    def set_enabled(self):
        if self.enabled:
            app.statusbar_proc(BAR_H, app.STATUSBAR_ADD_CELL, index=0, tag=MYTAG)
            app.statusbar_proc(BAR_H, app.STATUSBAR_SET_CELL_AUTOSIZE, tag=MYTAG, value=True)
            app.app_proc(app.PROC_SET_EVENTS, plugin_name + ';' + 'on_caret,on_focus' + ';;')
            self.process_unicode(app.ed)
        else:
            app.statusbar_proc(BAR_H, app.STATUSBAR_DELETE_CELL, tag=MYTAG)

    def toggle_display(self):
        self.enabled = not self.enabled
        app.ini_write(fn_config, section, 'enabled', bool_to_str(self.enabled))

        self.set_enabled()

    def process_unicode(self, ed_self: app.Editor):
        x, y, x1, y1 = ed_self.get_carets()[0]
        cnt = ed_self.get_line_count()
        if 0<=y<cnt:
            nlen = ed_self.get_line_len(y)
            if x >= nlen:
                return self.msg('')
            s = ed_self.get_text_substr(x, y, x+2, y)
            if s:
                s = s[0]

            s = ('U+%04x'%ord(s)).upper() +', '+ name(s, '?')
            self.msg(s)
