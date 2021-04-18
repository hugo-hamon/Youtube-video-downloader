from Scripts.functions import draw_component
from Scripts.const import WIN_SIZE, BG_COLOR
import tkinter as tk

window = tk.Tk()
window.minsize(WIN_SIZE[0], WIN_SIZE[1])
window.maxsize(WIN_SIZE[0], WIN_SIZE[1])
window.title('Youtube video / playlist downloader')
window['bg'] = BG_COLOR

if __name__ == '__main__':
    draw_component(window=window)
    window.mainloop()
