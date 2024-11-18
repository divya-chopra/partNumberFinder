from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, Rectangle  # Import Color and Rectangle for drawing
import pandas as pd

def load_name_list_from_excel(file_path, sheet_name, column_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        name_list = df[column_name].dropna().tolist()
        return name_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

class PartNumberApp(App):
    def build(self):
        # Set window background color
        Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Light gray background
        
        # Load data
        self.name_list = load_name_list_from_excel(
            'data/part_number_app_data.xlsx', 
            'Sheet1', 
            'NAME LIST'
        )
        
        # Main layout with increased padding
        main_layout = BoxLayout(
            orientation='vertical', 
            padding=20,  # Increased padding
            spacing=15   # Increased spacing between widgets
        )
        
        # Large search input with custom styling
        self.part_number_input = TextInput(
            hint_text="Enter Part Number Description",
            size_hint=(1, None),
            height=80,
            font_size=24,
            padding=[20, 20],
            multiline=False,
            background_color=(1, 1, 1, 1),
            cursor_color=(0, 0, 0, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        
        # Search button with custom styling
        search_button = Button(
            text="Search",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        search_button.bind(on_press=self.search_part_number)
        
        # ScrollView for displaying results
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            bar_width=10,
            bar_color=(0.3, 0.3, 0.3, 0.9),
            bar_inactive_color=(0.5, 0.5, 0.5, 0.2),
            effect_cls='ScrollEffect'
        )
        
        # Results layout
        self.results_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=[10, 10]
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        # Add widgets to main layout and scroll view
        self.scroll_view.add_widget(self.results_layout)
        main_layout.add_widget(self.part_number_input)
        main_layout.add_widget(search_button)
        main_layout.add_widget(self.scroll_view)
        
        self.selected_label = None  # Track currently selected label
        
        return main_layout

    def search_part_number(self, instance):
        query = self.part_number_input.text.strip().lower()
        self.results_layout.clear_widgets()
        
        if '/' in query:
            substrings = query.split('/')
            matches = [
                entry for entry in self.name_list 
                if any(substring in entry.lower() for substring in substrings)
            ]
        else:
            substrings = query.split()
            matches = [
                entry for entry in self.name_list 
                if all(substring in entry.lower() for substring in substrings)
            ]
        
        # Display results with enhanced styling
        if matches:
            for match in matches:
                result_label = Label(
                    text=match,
                    size_hint_y=None,
                    height=60,
                    font_size=18,
                    halign="left",
                    valign="middle",
                    text_size=(self.scroll_view.width - 40, None),
                    color=(0, 0, 0, 1),
                    padding=(15, 15)
                )
                result_label.bind(on_touch_down=self.copy_to_clipboard)  
                result_label.bind(on_touch_down=self.highlight_label)  
                self.results_layout.add_widget(result_label)
                
        else:
            no_match_label = Label(
                text="No matches found",
                size_hint_y=None,
                height=60,
                font_size=18,
                color=(0.7, 0, 0, 1)  
            )
            self.results_layout.add_widget(no_match_label)

    def copy_to_clipboard(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            Clipboard.copy(instance.text)   # Copy text to clipboard
            print(f"Copied '{instance.text}' to clipboard")   # Optional: Print confirmation

    def highlight_label(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            if self.selected_label:
                # Reset previously selected label's background color
                self.selected_label.canvas.before.clear()
            
            # Highlight the currently selected label
            with instance.canvas.before:
                Color(0.4, 0.8, 0.4, 1)  # Set highlight color (green)
                Rectangle(pos=instance.pos, size=instance.size) 

            self.selected_label = instance   # Update selected label reference

if __name__ == '__main__':
    PartNumberApp().run()