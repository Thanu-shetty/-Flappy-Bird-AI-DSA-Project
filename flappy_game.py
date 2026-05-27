# flappy_game.py - Fixed version that runs properly
import tkinter as tk
import random
import time
import math

class FlappyBirdGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flappy Bird AI + DSA Challenges")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Prevent window from stealing focus aggressively
        self.root.attributes('-topmost', False)
        
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg='light blue')
        self.canvas.pack()
        
        # Game variables
        self.bird_x = 200
        self.bird_y = 350
        self.bird_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.pipes = []
        self.pipe_speed = 5
        self.pipe_frequency = 1500  # ms
        self.last_pipe_time = 0
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_started = False
        self.dsa_challenge_active = False
        self.current_challenge = None
        self.temp_message = ""
        self.temp_message_color = ""
        self.temp_message_time = 0
        
        # DSA questions database
        self.dsa_questions = [
            {
                "question": "What is the time complexity of Binary Search?",
                "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                "answer": 1,
                "type": "complexity"
            },
            {
                "question": "Which data structure uses LIFO principle?",
                "options": ["Queue", "Stack", "Array", "Tree"],
                "answer": 1,
                "type": "data_structure"
            },
            {
                "question": "What does BST stand for?",
                "options": ["Binary Search Tree", "Best Sorting Technique", "Binary Sort Tree", "Basic Search Tree"],
                "answer": 0,
                "type": "terminology"
            },
            {
                "question": "Which algorithm is NOT a sorting algorithm?",
                "options": ["Quick Sort", "Bubble Sort", "Dijkstra", "Merge Sort"],
                "answer": 2,
                "type": "algorithms"
            },
            {
                "question": "What is the worst-case time complexity of Bubble Sort?",
                "options": ["O(n log n)", "O(n)", "O(n²)", "O(log n)"],
                "answer": 2,
                "type": "complexity"
            },
            {
                "question": "Which data structure uses FIFO principle?",
                "options": ["Stack", "Queue", "Tree", "Graph"],
                "answer": 1,
                "type": "data_structure"
            },
            {
                "question": "What is the time complexity of accessing an element in an array?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
                "answer": 2,
                "type": "complexity"
            },
            {
                "question": "Which algorithm uses divide and conquer strategy?",
                "options": ["Bubble Sort", "Merge Sort", "Linear Search", "Insertion Sort"],
                "answer": 1,
                "type": "algorithms"
            }
        ]
        
        # Bind keys
        self.root.bind('<space>', self.jump)
        self.root.bind('r', self.restart_game)
        self.root.bind('1', lambda e: self.answer_question(0))
        self.root.bind('2', lambda e: self.answer_question(1))
        self.root.bind('3', lambda e: self.answer_question(2))
        self.root.bind('4', lambda e: self.answer_question(3))
        self.root.bind('m', self.return_to_menu)
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Start with menu
        self.show_menu()
        
    def show_menu(self):
        self.game_started = False
        self.game_over = False
        self.canvas.delete("all")
        
        # Draw background
        self.draw_background()
        
        # Title
        self.canvas.create_text(500, 100, text="Flappy Bird AI + DSA", 
                               font=("Arial", 48, "bold"), fill="dark blue")
        self.canvas.create_text(500, 160, text="Learn Data Structures & Algorithms through AI Gaming", 
                               font=("Arial", 18), fill="dark green")
        
        # Menu buttons
        button_width, button_height = 300, 60
        center_x = 500 - button_width // 2
        
        # Start Game button
        self.canvas.create_rectangle(center_x, 250, center_x + button_width, 250 + button_height, 
                                   fill="blue", outline="white", width=3, tags="start_btn")
        self.canvas.create_text(500, 250 + button_height // 2, text="Start Game", 
                               font=("Arial", 24), fill="white", tags="start_text")
        
        # DSA Challenge Mode button
        self.canvas.create_rectangle(center_x, 330, center_x + button_width, 330 + button_height, 
                                   fill="green", outline="white", width=3, tags="dsa_btn")
        self.canvas.create_text(500, 330 + button_height // 2, text="DSA Challenge Mode", 
                               font=("Arial", 24), fill="white", tags="dsa_text")
        
        # AI Training button (simulated)
        self.canvas.create_rectangle(center_x, 410, center_x + button_width, 410 + button_height, 
                                   fill="purple", outline="white", width=3, tags="ai_btn")
        self.canvas.create_text(500, 410 + button_height // 2, text="AI Training (Coming Soon)", 
                               font=("Arial", 20), fill="white", tags="ai_text")
        
        # Exit button
        self.canvas.create_rectangle(center_x, 490, center_x + button_width, 490 + button_height, 
                                   fill="red", outline="white", width=3, tags="exit_btn")
        self.canvas.create_text(500, 490 + button_height // 2, text="Exit", 
                               font=("Arial", 24), fill="white", tags="exit_text")
        
        # High score
        self.canvas.create_text(500, 580, text=f"High Score: {self.high_score}", 
                               font=("Arial", 24), fill="dark red")
        
        # Instructions
        self.canvas.create_text(500, 630, text="Press SPACE to jump • R to restart • M for menu • 1-4 to answer DSA questions", 
                               font=("Arial", 12), fill="gray")
        
        # Bind click events
        self.canvas.tag_bind("start_btn", "<Button-1>", lambda e: self.start_game(False))
        self.canvas.tag_bind("start_text", "<Button-1>", lambda e: self.start_game(False))
        self.canvas.tag_bind("dsa_btn", "<Button-1>", lambda e: self.start_game(True))
        self.canvas.tag_bind("dsa_text", "<Button-1>", lambda e: self.start_game(True))
        self.canvas.tag_bind("ai_btn", "<Button-1>", lambda e: self.show_ai_message())
        self.canvas.tag_bind("ai_text", "<Button-1>", lambda e: self.show_ai_message())
        self.canvas.tag_bind("exit_btn", "<Button-1>", lambda e: self.root.quit())
        self.canvas.tag_bind("exit_text", "<Button-1>", lambda e: self.root.quit())
    
    def show_ai_message(self):
        self.canvas.delete("all")
        self.draw_background()
        self.canvas.create_rectangle(300, 300, 700, 400, fill="white", outline="black", width=3)
        self.canvas.create_text(500, 330, text="AI Training Mode", font=("Arial", 24, "bold"), fill="purple")
        self.canvas.create_text(500, 370, text="Requires Pygame installation\nTry the DSA Challenge mode instead!", 
                               font=("Arial", 14), fill="black", justify="center")
        self.root.after(2000, self.show_menu)
    
    def draw_background(self):
        # Sky
        self.canvas.create_rectangle(0, 0, 1000, 600, fill="light blue", outline="")
        
        # Ground
        self.canvas.create_rectangle(0, 600, 1000, 700, fill="green", outline="")
        
        # Clouds
        for x, y in [(100, 100), (300, 150), (700, 80), (900, 120)]:
            self.canvas.create_oval(x, y, x + 80, y + 40, fill="white", outline="")
    
    def start_game(self, dsa_mode):
        self.dsa_challenge_active = dsa_mode
        self.bird_x = 200
        self.bird_y = 350
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.game_started = True
        self.current_challenge = None
        self.last_pipe_time = time.time() * 1000
        self.temp_message = ""
        
        self.game_loop()
    
    def jump(self, event=None):
        if self.game_started and not self.game_over and not self.current_challenge:
            self.bird_velocity = self.jump_strength
    
    def restart_game(self, event=None):
        if self.game_over:
            self.start_game(self.dsa_challenge_active)
    
    def return_to_menu(self, event=None):
        self.show_menu()
    
    def create_pipe(self):
        gap_y = random.randint(150, 450)
        gap_size = 200
        self.pipes.append({
            'x': 1000,
            'top_height': gap_y - gap_size // 2,
            'bottom_y': gap_y + gap_size // 2,
            'passed': False,
            'width': 80
        })
    
    def update_pipes(self):
        current_time = time.time() * 1000
        
        # Create new pipes
        if current_time - self.last_pipe_time > self.pipe_frequency:
            self.create_pipe()
            self.last_pipe_time = current_time
        
        # Move pipes and remove off-screen ones
        for pipe in self.pipes[:]:
            pipe['x'] -= self.pipe_speed
            if pipe['x'] < -pipe['width']:
                self.pipes.remove(pipe)
            
            # Check scoring
            if not pipe['passed'] and pipe['x'] + pipe['width'] < self.bird_x:
                pipe['passed'] = True
                self.score += 1
                
                # Trigger DSA challenge every 3 points in challenge mode
                if self.dsa_challenge_active and self.score % 3 == 0:
                    self.current_challenge = random.choice(self.dsa_questions)
    
    def check_collision(self):
        bird_radius = 15
        bird_rect = [self.bird_x - bird_radius, self.bird_y - bird_radius,
                    self.bird_x + bird_radius, self.bird_y + bird_radius]
        
        # Ground and ceiling collision
        if self.bird_y > 600 - bird_radius or self.bird_y < bird_radius:
            return True
        
        # Pipe collision
        for pipe in self.pipes:
            # Top pipe
            top_pipe = [pipe['x'], 0, pipe['x'] + pipe['width'], pipe['top_height']]
            # Bottom pipe
            bottom_pipe = [pipe['x'], pipe['bottom_y'], pipe['x'] + pipe['width'], 700]
            
            if (self.rect_intersect(bird_rect, top_pipe) or 
                self.rect_intersect(bird_rect, bottom_pipe)):
                return True
        
        return False
    
    def rect_intersect(self, rect1, rect2):
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or 
                   rect1[3] < rect2[1] or rect1[1] > rect2[3])
    
    def answer_question(self, answer_index):
        if self.current_challenge:
            if answer_index == self.current_challenge["answer"]:
                self.score += 10  # Bonus points for correct answer
                self.show_message("Correct! +10 points", "green")
            else:
                correct_answer = self.current_challenge["answer"]
                correct_text = self.current_challenge["options"][correct_answer]
                self.show_message(f"Wrong! Correct: {correct_text}", "red")
            self.current_challenge = None
    
    def show_message(self, message, color):
        self.temp_message = message
        self.temp_message_color = color
        self.temp_message_time = time.time()
    
    def draw_game(self):
        self.canvas.delete("all")
        
        # Draw background
        self.draw_background()
        
        # Draw pipes
        for pipe in self.pipes:
            # Top pipe
            self.canvas.create_rectangle(pipe['x'], 0, pipe['x'] + pipe['width'], pipe['top_height'], 
                                       fill="dark green", outline="black", width=2)
            # Bottom pipe
            self.canvas.create_rectangle(pipe['x'], pipe['bottom_y'], pipe['x'] + pipe['width'], 700, 
                                       fill="dark green", outline="black", width=2)
        
        # Draw bird
        self.draw_bird()
        
        # Draw score
        self.canvas.create_text(50, 30, text=f"Score: {self.score}", 
                               font=("Arial", 24, "bold"), fill="black", anchor="w")
        
        mode_text = "DSA Challenge Mode" if self.dsa_challenge_active else "Normal Mode"
        self.canvas.create_text(50, 60, text=mode_text, 
                               font=("Arial", 16), fill="dark blue", anchor="w")
        
        # Draw DSA challenge if active
        if self.current_challenge:
            self.draw_dsa_challenge()
        
        # Draw temporary message
        if self.temp_message and time.time() - self.temp_message_time < 2:
            self.canvas.create_rectangle(400, 300, 600, 360, fill="white", outline="black", width=2)
            self.canvas.create_text(500, 330, text=self.temp_message, 
                                   font=("Arial", 16), fill=self.temp_message_color)
        
        # Game over screen
        if self.game_over:
            self.draw_game_over()
    
    def draw_bird(self):
        # Bird body
        self.canvas.create_oval(self.bird_x - 15, self.bird_y - 15, 
                               self.bird_x + 15, self.bird_y + 15, 
                               fill="yellow", outline="black", width=2)
        
        # Bird eye
        self.canvas.create_oval(self.bird_x + 5, self.bird_y - 8, 
                               self.bird_x + 10, self.bird_y - 3, 
                               fill="black")
        
        # Bird beak
        self.canvas.create_polygon(self.bird_x + 15, self.bird_y - 5,
                                  self.bird_x + 25, self.bird_y,
                                  self.bird_x + 15, self.bird_y + 5,
                                  fill="orange", outline="black", width=1)
        
        # Bird wing (animated based on velocity)
        wing_offset = math.sin(time.time() * 10) * 3 if self.bird_velocity < 0 else 0
        self.canvas.create_oval(self.bird_x - 10, self.bird_y - 5 + wing_offset,
                               self.bird_x, self.bird_y + 10 + wing_offset,
                               fill="orange", outline="black", width=1)
    
    def draw_dsa_challenge(self):
        # Challenge background
        self.canvas.create_rectangle(200, 150, 800, 500, fill="light yellow", outline="black", width=4)
        
        # Title
        self.canvas.create_text(500, 180, text="🎓 DSA CHALLENGE! 🎓", 
                               font=("Arial", 24, "bold"), fill="dark blue")
        
        # Question
        self.canvas.create_text(500, 230, text=self.current_challenge["question"], 
                               font=("Arial", 16, "bold"), fill="black", width=500)
        
        # Options
        for i, option in enumerate(self.current_challenge["options"]):
            y_pos = 280 + i * 50
            self.canvas.create_rectangle(250, y_pos - 20, 750, y_pos + 20, 
                                       fill="white", outline="blue", width=2)
            self.canvas.create_text(500, y_pos, text=f"{i+1}. {option}", 
                                   font=("Arial", 14), fill="black")
        
        # Instructions
        self.canvas.create_text(500, 460, text="Press 1-4 to answer • Get +10 points for correct answer!", 
                               font=("Arial", 12, "bold"), fill="dark green")
    
    def draw_game_over(self):
        # Overlay
        self.canvas.create_rectangle(0, 0, 1000, 700, fill="black", stipple="gray50")
        
        # Game over box
        self.canvas.create_rectangle(300, 200, 700, 450, fill="white", outline="red", width=4)
        
        # Game over text
        self.canvas.create_text(500, 250, text="GAME OVER", 
                               font=("Arial", 36, "bold"), fill="red")
        
        # Score
        self.canvas.create_text(500, 300, text=f"Final Score: {self.score}", 
                               font=("Arial", 24), fill="black")
        
        # High score update
        if self.score > self.high_score:
            self.high_score = self.score
            self.canvas.create_text(500, 330, text="New High Score! 🏆", 
                                   font=("Arial", 20, "bold"), fill="gold")
        
        # Restart button
        self.canvas.create_rectangle(400, 370, 600, 420, fill="green", outline="white", width=2)
        self.canvas.create_text(500, 395, text="Press R to Restart", 
                               font=("Arial", 16, "bold"), fill="white")
        
        # Menu button
        self.canvas.create_text(500, 430, text="Press M for Menu", 
                               font=("Arial", 14), fill="blue")
    
    def game_loop(self):
        if self.game_started and not self.game_over:
            # Update physics
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity
            
            # Update pipes
            self.update_pipes()
            
            # Check collisions
            if self.check_collision():
                self.game_over = True
            
            # Draw everything
            self.draw_game()
            
            # Continue game loop (approximately 60 FPS)
            self.root.after(16, self.game_loop)  # ~60 FPS
        elif self.game_over:
            self.draw_game()

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Game ended: {e}")

# Run the game
if __name__ == "__main__":
    print("🚀 Starting Flappy Bird AI + DSA Game...")
    print("=" * 50)
    print("🎮 CONTROLS:")
    print("   SPACE  - Jump")
    print("   R      - Restart game")
    print("   M      - Return to menu")
    print("   1-4    - Answer DSA questions")
    print("   ESC    - Exit game")
    print("   Click  - Menu buttons")
    print("=" * 50)
    print("🎯 FEATURES:")
    print("   • Complete Flappy Bird gameplay")
    print("   • DSA Challenge Mode with bonus points")
    print("   • 8 different DSA questions")
    print("   • Score tracking & high scores")
    print("   • Beautiful graphics & animations")
    print("=" * 50)
    
    game = FlappyBirdGame()
    game.run()