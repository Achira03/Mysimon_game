from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

# สร้างคลาส SimonSays
class SimonSaysApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sequence = []  
        self.user_sequence = []  
        self.score = 0  
        self.high_score = self.load_high_score()  
        self.is_user_turn = False  
        self.speed = 0.5  
        self.total_buttons = 4  

        # Layout หลัก
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # พื้นที่คะแนนและข้อความ
        self.info_label = Label(text=f"Welcome to Simon Says! High Score: {self.high_score}", font_size=24, size_hint=(1, 0.2))
        self.score_label = Label(text="Score: 0", font_size=20, size_hint=(1, 0.2))
        self.root.add_widget(self.info_label)
        self.root.add_widget(self.score_label)

        # GridLayout สำหรับปุ่ม
        self.grid = GridLayout(cols=2, spacing=5)  # เริ่มต้นจะมีจำนวนปุ่มแบบ 2x2
        self.buttons = {}
        self.create_buttons()  # สร้างปุ่มเริ่มต้น
        self.root.add_widget(self.grid)

        # สำหรับสร้างปุ่มเริ่มเกม
        self.start_button = Button(text="Start Game", size_hint=(1, 0.2), font_size=20)
        self.start_button.bind(on_press=self.start_game)
        self.root.add_widget(self.start_button)
        
    def build(self):
        #ใช้return __init__
        return self.root
        
        #ไฟกระพริบสำหรับปุ่มที่ผู้เล่นต้องกด
    def flash_button(self, btn_name):
        btn = self.buttons[btn_name]
        original_color = btn.background_color
        btn.background_color = [1, 0, 0, 1]  # ไฟกระพิบสีแดง
        Clock.schedule_once(lambda dt: self.restore_button_color(btn, original_color), 0.3)
        
    #ฟังก์ชั่นสำหรับเช็คว่าผู้เล่นกดปุ่มถูกต้องตามลำดับมั้ย    
    def check_user_input(self):
        for i in range(len(self.user_sequence)):
            if self.user_sequence[i] != self.sequence[i]:
                self.info_label.text = f"Game Over! You scored: {self.score}"
                self.is_user_turn = False
                if self.score > self.high_score:  # บันทึกคะแนนสูงสุดใหม่
                    self.high_score = self.score
                    self.save_high_score()
                return

        if len(self.user_sequence) == len(self.sequence):
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.info_label.text = "Good job! Watch the next sequence!"
            self.is_user_turn = False

            # เพิ่มความเร็ว
            self.speed = max(0.2, self.speed - 0.02)

            # เพิ่มปุ่ม +2 ทุกๆ 5 คะแนน
            if self.score % 5 == 0:  
                self.total_buttons += 2
                self.create_buttons()

            #สำหรับเริ่มรอบใหม่
            Clock.schedule_once(self.next_round, 1)
