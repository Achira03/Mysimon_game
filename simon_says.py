from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from pathlib import Path
from kivy.uix.screenmanager import ScreenManager,Screen
import random

#สร้างคลาสสำหรับหน้าเลือกระดับความยาก
class DifficultyScreen(Screen):
    pass

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
    
    def create_buttons(self): #ฟังก์ชั่นสร้างปุ่มใหม่
        for i in range(self.total_buttons):
            btn_name = f"btn_{i}"
            if btn_name not in self.buttons:
                #กำหนดรูปแบบปุ่ม  
                btn = Button(
                    background_normal='',
                    background_color=[1, 1, 1, 1],
                    on_press=self.on_button_press
                )                                  #[1, 1, 1, 1] คือสีขาว
                btn.color_name = btn_name
                self.buttons[btn_name] = btn
                self.grid.add_widget(btn)

        # ปรับจำนวนคอลัมน์ตามจำนวนปุ่มเพื่อให้ดูสมดุล โดยใช้สแควรูท (**0.5)
        self.grid.cols = int(len(self.buttons) ** 0.5)
        
    def restart_game(self, instance):
        self.start_button.text = "Restart Game"
        self.sequence = []  # รีเซ็ทลำดับปุ่มเพื่อเริ่มใหม่
        self.user_sequence = [] #รีเซ็ทลำดับปุ่มที่ผู้เล่นเคยกดไว้
        self.score = 0
        self.speed = 0.5  
        self.score_label.text = "Score: 0"
        self.info_label.text = f"High Score: {self.high_score}"
        self.random_button()
        Clock.schedule_once(self.play_sequence, 1)
        
    def random_button(self): #สุ่มลำดับของปุ่ม
        btn_names = list(self.buttons.keys())
        self.sequence.append(random.choice(btn_names))
        
    def play_sequence(self, dt):  #ไว้สำหรับให้ผู้เล่นเริ่มหลังจากปุ่มลำดับกระพริบ
        self.user_sequence = []  
        delay = max(0.2, self.speed)  # ตั้งค่าdelayการกระพริบ
        for i, btn_name in enumerate(self.sequence):
            Clock.schedule_once(lambda dt, name=btn_name: self.flash_button(name), delay * (i + 1))
        Clock.schedule_once(lambda dt: self.start_user_turn(), delay * (len(self.sequence) + 1))

        
        #ไฟกระพริบสำหรับปุ่มที่ผู้เล่นต้องกด
    def flash_button(self, btn_name):
        btn = self.buttons[btn_name]
        original_color = btn.background_color
        btn.background_color = [1, 0, 0, 1]  # ไฟกระพิบสีแดง
        Clock.schedule_once(lambda dt: self.restore_button_color(btn, original_color), 0.3)
        
    def restore_button_color(self, btn, original_color):
        btn.background_color = original_color  # เปลี่ยนกลับเป็นสีเดิมหลังจาก flash_button ทำงาน
        
    
    def start_user_turn(self):
        self.info_label.text = "Your turn! Repeat the sequence!" #เริ่มต้นการเล่นของผู้เล่นโดยแสดงข้อความดังนี้
        self.is_user_turn = True
        
    def on_button_press(self, instance):
        if not self.is_user_turn: #ตรวจสอบว่าอยู่ในรอบการเล่นหรือไม่
            return

        self.user_sequence.append(instance.color_name) #บันทึกชื่อปุ่มลงใน user_sequence
        self.check_user_input()

        

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
            
    def next_round(self, dt):
        self.random_button()
        self.play_sequence(0)
            
    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))
            
    def load_high_score(self):
        file = Path('high_score.txt') 
        if file.exists():  # เช็คว่าไฟล์มีอยู่มั้ย
            return int(file.read_text()) 
        else:
            return 0  # ถ้าไม่มีไฟล์จะคืนค่า 0


if __name__ == "__main__":
    SimonSaysApp().run()