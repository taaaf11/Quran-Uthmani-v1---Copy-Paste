import time
import flet as ft
from .aya_dict import surah_aya


class QuranCopyPaste(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textfield = ft.TextField(label='Index', hint_text='Surah:Ayah', width=350)
        self.sub_button = ft.IconButton(icon=ft.icons.CHECK_SHARP, on_click=self.show_ayah)
        self.copy_buttom = ft.IconButton(icon=ft.icons.COPY_SHARP, on_click=self.copy)
        self.button = [self.sub_button, self.copy_buttom]
        self.quran_txt = ft.Text(size=48, text_align=ft.TextAlign.CENTER)
        self.quran_txt_cont = ft.Container(self.quran_txt,
                                           margin=ft.Margin(200, 10, 200, 0))
        self.controls = [
            self.textfield,
            ft.Row(self.button, alignment=ft.MainAxisAlignment.CENTER),
            self.quran_txt_cont
        ]
        
        # No matter what, this vertical alignment of column have no effect.
        # Page has vertical alignment option, columns follow them.
        
        # self.alignment = ...
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def prep_font(self, font_name):
        self.page.fonts = {
            f'{font_name}': f'https://github.com/quran/quran.com-images/raw/master/res/fonts/{font_name}.TTF'
        }
        self.page.update()
        time.sleep(1.5)  # for the font to load (on my connection 😅)
    
    def show_ayah(self, e):
        self.quran_txt.value = ''  # resetting value set by previous function calls
        ayah_data = surah_aya[self.textfield.value]  # in surah:ayah form
        ayah_text = ayah_data[0]
        font = ayah_data[1]

        self.prep_font(font)
        
        self.quran_txt.font_family = font
        self.quran_txt.value = ayah_text
        
        self.update()
    
    def copy(self, e):
        self.page.set_clipboard(self.quran_txt.value)
    
    def build(self):
        return self
