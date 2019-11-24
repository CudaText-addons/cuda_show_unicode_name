import cudatext as app
from unicodedata import name

MYTAG = 101

class Command:

    def __init__(self):

        app.statusbar_proc('main', app.STATUSBAR_ADD_CELL, tag=MYTAG)
        app.statusbar_proc('main', app.STATUSBAR_SET_CELL_AUTOSIZE, tag=MYTAG, value=True)

    def on_caret(self, ed_self):

        x, y, x1, y1 = ed_self.get_carets()[0]
        cnt = ed_self.get_line_count()
        if 0<=y<cnt:
            s = ed_self.get_text_line(y, 2000) #limit max len
            if x>=len(s):
                return self.msg('')
            s = s[x]
            s = ('U+%04x'%ord(s)).upper() +', '+ name(s, '?')
            self.msg(s)

    def msg(self, s):

        app.statusbar_proc('main', app.STATUSBAR_SET_CELL_TEXT, tag=MYTAG, value=s)
