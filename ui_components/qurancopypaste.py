import time
import requests
import zipfile
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
        
        self.font_info = ft.Text(size=15, text_align=ft.TextAlign.CENTER)
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
        
        # variables for controlling, when user requests ayah-s in a range e.g. 2:5-17
        self.ayah_range_asked = False
        self.ayahs_in_range = []
        self.fonts_in_range = []
    
    def prep_font(self, font_name):
        self.page.fonts = {
            f'{font_name}': f'https://github.com/quran/quran.com-images/raw/master/res/fonts/{font_name}.TTF'
        }
        self.page.update()
        time.sleep(1.5)  # for the font to load (on my connection 😅)
    
    # add ellipses, when ayah text is too long
    def _shorten_arabic_text_container(self, ayah_arabic):
        self.quran_txt.value = ayah_arabic[:7]
        
        # self.quran_text_controls.controls[0] was self.quran_txt
        self.quran_txt_controls.controls[0] = ft.Row([
            ft.Text(value='...', size=25),
            self.quran_txt
        ], alignment=ft.MainAxisAlignment.CENTER)
    
    def show_ayah(self, e):
        # resetting values
        self.quran_txt.value = ''  # resetting the old values that were
        self.font_info.value = ''  # set by previous function calls
        self.quran_txt_controls.controls[0] = self.quran_txt  #
        self.quran_txt_controls.visible = False
        
        if '-' in self.textfield.value:
            self.ayah_range_asked = True
            
            ayah_texts = []
            fonts_list = []
            index_split = self.textfield.value.split(':')
            
            for i in range(int(index_split[1].split('-')[0]), int(index_split[1].split('-')[1])+1):
                ayah_data = surah_aya[f'{index_split[0]}:{i}']
                ayah_texts.append(ayah_data[0])
                fonts_list.append(ayah_data[1])
            
            ayah_text = ayah_texts[0]
            # remove repeating font names
            fonts_list = sorted(set(fonts_list))
            display_font = fonts_list[0]
            self.prep_font(display_font)
            
            self.ayahs_in_range = ayah_texts
            self.fonts_in_range = fonts_list
            
            self.quran_txt.value = ayah_text
            self.quran_txt.font_family = display_font
            self._shorten_arabic_text_container(ayah_text)  # adds to quran_txt automatically
            
            self.font_info.value = f'The fonts are: \n'
            for font in fonts_list:
                self.font_info.value += font + '.ttf '
            
            self.quran_txt_controls.visible = True
            self.update()
            return
        
        ayah_data = surah_aya[self.textfield.value]  # in surah:ayah form
        ayah_text = ayah_data[0]
        display_font = ayah_data[1]
        
        self.curr_font = display_font
            
        # prepare font family
        self.prep_font(display_font)
        
        self._shorten_arabic_text_container(ayah_text)  # adds to quran_txt automatically
        self.quran_txt.font_family = display_font
        self.font_info.value = f'The font is: {display_font}.ttf'
        self.quran_txt_controls.visible = True
        self.update()
    
    def copy(self, e):
        quran_txt = ''
        if self.ayah_range_asked:
            for ayah_text in self.ayahs_in_range:
                quran_txt += ayah_text
        else:
            quran_txt = self.quran_txt.value
        self.page.set_clipboard(quran_txt)
    
    def _save_font(self, e: ft.FilePickerResultEvent):
        if not self.ayah_range_asked:
            font_path = e.path
            if not (font_path is None):
                with open(font_path, 'wb') as font_file:
                    r = requests.get(f'https://github.com/quran/quran.com-images/raw/master/res/fonts/{self.curr_font}.TTF')
                    font_file.write(r.content)
            return
        
        fonts_zip_path = e.path
        
        if not (fonts_zip_path is None):
            fonts_zip_file = zipfile.ZipFile(fonts_zip_path, 'w')
            with zipfile.ZipFile(fonts_zip_path, 'w') as fonts_zip_file:
                for font in self.fonts_in_range:
                    r = requests.get(f'https://github.com/quran/quran.com-images/raw/master/res/fonts/{font}.TTF')
                    fonts_zip_file.writestr(f'{font}.ttf', r.content)
    
    def save_font_dialog(self, e):
        file_picker = ft.FilePicker(on_result=self._save_font)
        self.page.overlay.append(file_picker)
        self.page.update()
        if not self.ayah_range_asked:
            file_picker.save_file("Save Font", file_name=f'{self.curr_font}.ttf', allowed_extensions=['ttf'])
            return
        file_picker.save_file("Save Fonts", file_name='fonts.zip', allowed_extensions=['zip'])
    
    def build(self):
        return self
