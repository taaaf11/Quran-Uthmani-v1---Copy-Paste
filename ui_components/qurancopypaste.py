import time
import requests
import flet as ft
from .aya_dict import surah_aya


class QuranCopyPaste(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # text input
        self.textfield = ft.TextField(label='Index', hint_text='Surah:Ayah', width=350, on_submit=self.show_ayah)
        
        # buttons
        self.sub_button = ft.TextButton(icon=ft.icons.CHECK_SHARP, on_click=self.show_ayah)
        self.copy_button = ft.ElevatedButton(icon=ft.icons.COPY_SHARP, text='Copy text', on_click=self.copy)
        self.save_font_button = ft.ElevatedButton(icon=ft.icons.DOWNLOAD_SHARP, text='Download font', on_click=self.save_font_dialog)
        
        self.input_controls = ft.Row([self.textfield, self.sub_button], alignment=ft.MainAxisAlignment.CENTER)
        self.arabic_controls = ft.Row([self.copy_button, self.save_font_button], alignment=ft.MainAxisAlignment.CENTER)
        
        self.font_info = ft.Text(size=15)
        self.quran_txt = ft.Text(size=42, text_align=ft.TextAlign.CENTER)
        self.quran_txt_controls = ft.Column([self.quran_txt,
                                             self.font_info,
                                             self.arabic_controls],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)
        
        self.quran_txt_controls_container = ft.Container(content=self.quran_txt_controls,
                                                         margin=ft.Margin(left=200, top=10,
                                                                right=200, bottom=20))
        self.curr_font = None
        self.controls = [
            self.input_controls,
            self.quran_txt_controls
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
        # resetting values
        self.quran_txt.value = ''  # resetting the old values that were
        self.font_info.value = ''  # set by previous function calls
        self.quran_txt_controls.controls[0] = self.quran_txt  #
        self.quran_txt_controls.visible = False
        
        # getting data
        ayah_data = surah_aya[self.textfield.value]  # in surah:ayah form
        ayah_text = ayah_data[0]
        font = ayah_data[1]
        
        # prepare font family
        self.prep_font(font)
        
        # set fonts
        self.quran_txt.font_family = font
        self.curr_font = font
        
        if len(ayah_text) > 6:  # the solution is to save the old state of container content(s)
            self.quran_txt.value = ayah_text[:7]
            # self.quran_text_controls.controls[0] was self.quran_txt
            self.quran_txt_controls.controls[0] = ft.Row([
                ft.Text(value='...', size=25),
                self.quran_txt
            ], alignment=ft.MainAxisAlignment.CENTER)
            self.quran_txt_controls.visible = True
            self.font_info.value = f'The font is: {font}.ttf'
            self.update()
            return
        
        self.quran_txt.value = ayah_text
        self.font_info.value = f'The font is: {font}.ttf'
        self.quran_txt_controls.visible = True
        self.update()
    
    def copy(self, e):
        self.page.set_clipboard(self.quran_txt.value)
    
    def _save_font(self, e: ft.FilePickerResultEvent):
        font_path = e.path
        if not (font_file is None):
            with open(font_path, 'wb') as font_file:
                r = requests.get(f'https://github.com/quran/quran.com-images/raw/master/res/fonts/{self.curr_font}.TTF')
                font_file.write(r.content)
        return
    
    def save_font_dialog(self, e):
        file_picker = ft.FilePicker(on_result=self._save_font)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.save_file("Save Font", file_name=f'{self.curr_font}.ttf', allowed_extensions=['ttf'])
    
    def build(self):
        return self
