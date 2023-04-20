import threading
import time
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader


KV = '''
BoxLayout:
    orientation: "vertical"
    padding: "20dp"
    spacing: "20dp"
    
    MDBoxLayout:
        orientation: "horizontal"
        spacing: "20dp"
        
        MDRaisedButton:
            id: beat_box_1
            text: "1"
            theme_text_color: "Primary"
            size_hint: None, None
            size: "50dp", "50dp"

        MDRaisedButton:
            id: beat_box_2
            text: "2"
            theme_text_color: "Primary"
            size_hint: None, None
            size: "50dp", "50dp"

        MDRaisedButton:
            id: beat_box_3
            text: "3"
            theme_text_color: "Primary"
            size_hint: None, None
            size: "50dp", "50dp"

        MDRaisedButton:
            id: beat_box_4
            text: "4"
            theme_text_color: "Primary"
            size_hint: None, None
            size: "50dp", "50dp"
    
    MDLabel:
        text: "Beats Per Minute:"
        halign: "center"
        theme_text_color: "Secondary"

    MDLabel:  # Add this new label to display the BPM value
        id: bpm_value_label
        text: "60"  # Default value of the slider
        halign: "center"
        theme_text_color: "Primary"    
        
    MDSlider:
        id: bpm_slider
        min: 10
        max: 300
        value: 60
        step: 1
        orientation: "horizontal"
        on_value: app.update_bpm_label(self.value)
    
    MDLabel:  # Add this new label to display the timer
        id: timer_label
        text: "00:00"
        halign: "center"
        theme_text_color: "Primary"
    
    MDBoxLayout:  # Add this new box layout for the buttons
        orientation: "horizontal"
        spacing: "10dp"
    
        MDRaisedButton:
            text: "Start Metronome"
            on_release: app.start_metronome()
            size_hint: None, None
            size: "150dp", "40dp"

        MDRaisedButton:  # Add this new button for stopping the metronome
            text: "Stop Metronome"
            on_release: app.stop_metronome()
            size_hint: None, None
            size: "150dp", "40dp"   
'''

class MetronomeApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False

    beat = NumericProperty(-1)
    click_sound = SoundLoader.load('metronomesound1.wav')

    def build(self):
        return Builder.load_string(KV)

    def update_bpm_label(self, value):
        self.root.ids.bpm_value_label.text = str(int(value))
    
    def on_stop(self):
        self.stop_metronome()

    def start_metronome(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.metronome_thread = threading.Thread(target=self._metronome_loop)
            self.metronome_thread.start()
            self.update_timer()

    def stop_metronome(self):
        self.is_running = False
        if self.metronome_thread:
            self.metronome_thread.join()

    def update_timer(self):
        if self.is_running:
            elapsed_time = int(time.time() - self.start_time)
            Clock.schedule_once(self._update_timer_label(elapsed_time), 0)
            Clock.schedule_once(lambda dt: self.update_timer(), 1)

    def _update_timer_label(self, elapsed_time):
        def update_label(dt):
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.root.ids.timer_label.text = f"{minutes:02d}:{seconds:02d}"
        return update_label

    def _metronome_loop(self):
        while self.is_running:
            self.beat = (self.beat + 1) % 4
            Clock.schedule_once(self._highlight_beat_box, 0)
            time.sleep(60 / self.root.ids.bpm_slider.value)

    def _highlight_beat_box(self, dt):
        self.click_sound.play()  # Play the sound
        for i, beat_box_id in enumerate(["beat_box_1", "beat_box_2", "beat_box_3", "beat_box_4"], start=1):
            beat_box = self.root.ids[beat_box_id]
            if i == self.beat + 1:
                beat_box.md_bg_color = (1, 0, 0, 1)
            else:
                beat_box.md_bg_color = (1, 1, 1, 1)

if __name__ == "__main__":
    MetronomeApp().run()
