from Scripts.functions import draw_component, get_settings
from Scripts.const import WIN_SIZE
import tkinter as tk

data = get_settings()

window = tk.Tk()
window.minsize(WIN_SIZE[0], WIN_SIZE[1])
window.maxsize(WIN_SIZE[0], WIN_SIZE[1])
window.title('Youtube video / playlist downloader')
window['bg'] = data['background_color']

if __name__ == '__main__':
    draw_component(window=window, path=data['DOWNLOAD_FOLDER'], bg_color=data['background_color'])
    window.mainloop()
