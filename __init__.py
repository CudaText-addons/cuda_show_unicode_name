from cudatext import msg_status as msg
from unicodedata import name

class Command:
    
    def on_caret(self, ed_self):
        
        x, y, x1, y1 = ed_self.get_carets()[0]
        cnt = ed_self.get_line_count()
        if 0<=y<cnt:
            s = ed_self.get_text_line(y, 2000) #limit max len
            if x>=len(s):
                return msg('')
            s = s[x]
            s = ('U+%04x'%ord(s)).upper() +', '+ name(s, '?')
            msg(s)
