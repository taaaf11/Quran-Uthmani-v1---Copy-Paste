from ui_components import QuranCopyPaste
import flet as ft


def main(page: ft.Page):
    page.title = 'Quran Usmani Script v1 Copy Paste'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    home_page = QuranCopyPaste()
    
    page.add(home_page)

ft.app(target=main)
