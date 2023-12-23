from ui_components import QuranCopyPaste
import flet as ft


def main(page: ft.Page):
    page.title = 'Quran Usmani Script v1 Copy Paste'
    
    page.theme = ft.Theme(color_scheme_seed='#01666f')  # pine green
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def navigate_to_page(e):
        selected_page = e.control.selected_index
        if selected_page == 0:
            home_page.visible = True
            help_page.visible = False
        elif selected_page == 1:
            home_page.visible = False
            help_page.visible = True
        page.update()
    
    page.appbar = ft.AppBar(title=ft.Text('Quran Usmani v1 Copy/Paste'))
    page.drawer = ft.NavigationDrawer(controls=[
        ft.NavigationDrawerDestination(
            icon=ft.icons.HOME_OUTLINED,
            label='Home',
            selected_icon=ft.icons.HOME_ROUNDED
        ),
        ft.NavigationDrawerDestination(
            icon=ft.icons.HELP_OUTLINE_OUTLINED,
            label='Help',
            selected_icon=ft.icons.HELP_ROUNDED
        )],
        selected_index=0, on_change=navigate_to_page
    )
    
    home_page = QuranCopyPaste()
    help_page = ft.Column([
        ft.Text(value=
        '• Submit the index of Ayah you want in the form:\n\
        Surah:Ayah\n\n\
        • If you want to get Ayah in range, like first third Ayah-s of Surah Baqarah,\n\
        Submit the index as:\n\
        2:1-3\n\n\
        • After submitting the index, you will get the Ayah text,\n\
        then, you can copy the text and also download the fonts related to the text',
        text_align=ft.TextAlign.CENTER, size=20),
        ft.Text('\n'),
        ft.OutlinedButton(icon=ft.icons.LINK_ROUNDED, text='Source code',
                          on_click=lambda _:page.launch_url(''))  # add github repo url
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, visible=False)
    
    page.add(home_page, help_page)

ft.app(target=main)
