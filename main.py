from functions import *
from const import *
import tkinter as tk

window = tk.Tk()
window.minsize(WIN_SIZE[0], WIN_SIZE[1])
window.maxsize(WIN_SIZE[0], WIN_SIZE[1])
window.title('Youtube video / playlist downloader')
window['bg'] = BG_COLOR

if __name__ == '__main__':
    draw_component(window=window)
    window.mainloop()
