import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class ColorChangingBox(Widget):
    def __init__(self, **kwargs):
        super(ColorChangingBox, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 300)
        self.change_color()

    def change_color(self):
        with self.canvas:
            Color(random.random(), random.random(), random.random(), 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ColorChangingBox(Widget):
    def __init__(self, **kwargs):
        super(ColorChangingBox, self).__init__(**kwargs)
        self.change_color()

    def change_color(self):
        with self.canvas:
            Color(random.random(), random.random(), random.random(), 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ColorChangerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.color_boxes = []
        for i in range(4):
            color_box = ColorChangingBox()
            self.color_boxes.append(color_box)
            layout.add_widget(color_box)

        start_button = Button(text='Start')
        start_button.bind(on_press=self.start_changing_color)

        stop_button = Button(text='Stop')
        stop_button.bind(on_press=self.stop_changing_color)

        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        return layout

    def start_changing_color(self, instance):
        self.color_change_event = Clock.schedule_interval(
            self.change_box_color, 1)

    def stop_changing_color(self, instance):
        self.color_change_event.cancel()

    def change_box_color(self, dt):
        for color_box in self.color_boxes:
            color_box.change_color()


if __name__ == '__main__':
    ColorChangerApp().run()
