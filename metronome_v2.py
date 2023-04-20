import threading
from time import sleep, time
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

Builder.load_string("""
<BeatBox>:
    canvas.before:
        Color:
            rgba: self.color
        Rectangle:
            pos: self.pos
            size: self.size
""")

class BeatBox(Widget):
    color = ListProperty([1, 1, 1, 1])

class MetronomeApp(App):
    bpm = NumericProperty(60)
    timer_text = StringProperty("00:00")

    def build(self):
        self.metronome_thread = None
        self.timer_thread = None
        self.metronome_running = False
        self.timer_running = False
        self.start_time = 0

        root = BoxLayout(orientation="vertical")
        controls = GridLayout(cols=4, size_hint_y=0.2)

        bpm_label = Label(text="BPM:")
        controls.add_widget(bpm_label)

        self.bpm_input = TextInput(text=str(self.bpm), input_filter="int", multiline=False)
        controls.add_widget(self.bpm_input)

        start_button = Button(text="Start", on_press=self.start_metronome)
        controls.add_widget(start_button)

        stop_button = Button(text="Stop", on_press=self.stop_metronome)
        controls.add_widget(stop_button)

        root.add_widget(controls)

        self.beat_boxes = []
        beats_grid = GridLayout(cols=4, size_hint_y=0.7)
        for i in range(4):
            beat_box = BeatBox()
            beats_grid.add_widget(beat_box)
            self.beat_boxes.append(beat_box)
        root.add_widget(beats_grid)

        timer_label = Label(text=self.timer_text, font_size=14, size_hint_y=0.1)
        root.add_widget(timer_label)

        return root

    def start_metronome(self, _):
        if not self.metronome_running:
            self.bpm = int(self.bpm_input.text)
            self.metronome_running = True
            self.start_time = time()
            self.metronome_thread = threading.Thread(target=self.run_metronome)
            self.metronome_thread.start()
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.start()

    def stop_metronome(self, _):
        self.metronome_running = False
        self.timer_running = False

    def run_metronome(self):
        while self.metronome_running:
            beats_per_second = self.bpm / 60
            beat_interval = 1 / beats_per_second

            for i in range(4):
                if not self.metronome_running:
                    break

                self.beat_boxes[i].color = [1, 0, 0, 1]
                elapsed_time = time()
                sleep_duration = max(beat_interval - elapsed_time, 0)
                sleep(sleep_duration)
                self.beat_boxes[i].color = [1, 1, 1, 1]

    def update_timer(self):
        self.timer_running = True
        while self.timer_running and self.metronome_running:
            elapsed_time = int(time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_text = "{:02d}:{:02d}".format(minutes, seconds)
            sleep(1)

if __name__ == "__main__":
    MetronomeApp().run()

