import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Fbo, ClearBuffers, ClearColor


class ColorChangingBox(Widget):
    def __init__(self, **kwargs):
        super(ColorChangingBox, self).__init__(**kwargs)
        self.color = Color(0.5, 0.5, 0.5, 1)
        self.fbo = Fbo(size=self.size)
        with self.fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.fbo.texture)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.fbo.size = self.size
        self.rect.pos = self.pos
        self.rect.size = self.size

    def change_color(self):
        self.color.r = 1
        with self.fbo:
            ClearColor(0, 0, 0, 1)
            ClearBuffers()
            Color(*self.color.rgba)
            Rectangle(pos=self.pos, size=self.size)



class ColorChangerApp(App):
    def build(self):
        root_layout = BoxLayout(orientation='vertical')

        color_boxes_layout = BoxLayout(orientation='vertical')
        self.color_boxes = []
        for i in range(4):
            color_box = ColorChangingBox()
            self.color_boxes.append(color_box)
            color_boxes_layout.add_widget(color_box)

        root_layout.add_widget(color_boxes_layout)

        buttons_layout = BoxLayout(size_hint=(1, 0.2))
        start_button = Button(text='Start')
        start_button.bind(on_press=self.start_changing_color)
        buttons_layout.add_widget(start_button)

        stop_button = Button(text='Stop')
        stop_button.bind(on_press=self.stop_changing_color)
        buttons_layout.add_widget(stop_button)

        root_layout.add_widget(buttons_layout)

        return root_layout

    def start_changing_color(self, instance):
        self.color_index = 0
        self.color_change_event = Clock.schedule_interval(self.change_box_color, 0.5)

    def stop_changing_color(self, instance):
        self.color_change_event.cancel()

    def change_box_color(self, dt):
        if self.color_index < len(self.color_boxes):
            self.color_boxes[self.color_index].change_color()
            self.color_index += 1
        else:
            self.color_index = 0


if __name__ == '__main__':
    ColorChangerApp().run()
