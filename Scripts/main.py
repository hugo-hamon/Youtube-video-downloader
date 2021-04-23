from functions import draw_component, get_settings
from const import WIN_SIZE
import tkinter as tk

data = get_settings()

window = tk.Tk()
window.minsize(WIN_SIZE[0], WIN_SIZE[1])
window.maxsize(WIN_SIZE[0], WIN_SIZE[1])
window.title('Youtube video / playlist downloader')
window['bg'] = data['BACKGROUND_COLOR']

if __name__ == '__main__':
    draw_component(window=window)
    window.mainloop()
