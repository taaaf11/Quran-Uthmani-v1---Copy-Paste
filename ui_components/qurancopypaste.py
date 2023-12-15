from .input import Input
import flet as ft


class QuranCopyPaste(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textfield = ft.TextField(hint_text='Surah:Ayah', width=200)
        self.sub_button = ft.IconButton(icon=ft.icons.CHECK_SHARP, on_click=self.get_data)
        self.input_controls = [self.textfield, self.sub_button]
        self.quran_txt = ft.Text()
        self.controls = [
            ft.Row(self.input_controls, alignment=ft.MainAxisAlignment.CENTER),
            self.quran_txt
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def get_data(self, e):
        self.quran_txt.value = self.textfield.value
        self.update()
    
    def build(self):
        return self
