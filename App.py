import tkinter as tk
import random

class PacManGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man")

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='black')
        self.canvas.pack()

        self.pacman = self.canvas.create_oval(180, 180, 220, 220, fill='yellow')
        self.ghosts = []
        self.pellets = []
        self.power_ups = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.pacman_direction = (0, 0)
        self.power_up_active = False
        self.power_up_time = 0

        self.create_ghosts()
        self.create_pellets()
        self.create_power_ups()
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.move_pacman()
        self.move_ghosts()
        self.update_score()

    def create_ghosts(self):
        for _ in range(3):
            x = random.randint(0, 380)
            y = random.randint(0, 380)
            ghost = self.canvas.create_oval(x, y, x + 20, y + 20, fill='red')
            self.ghosts.append(ghost)

    def create_pellets(self):
        for _ in range(10):
            x = random.randint(20, 380)
            y = random.randint(20, 380)
            pellet = self.canvas.create_oval(x, y, x + 10, y + 10, fill='white')
            self.pellets.append(pellet)

    def create_power_ups(self):
        for _ in range(2):
            x = random.randint(20, 380)
            y = random.randint(20, 380)
            power_up = self.canvas.create_oval(x, y, x + 15, y + 15, fill='blue')
            self.power_ups.append(power_up)

    def move_pacman(self):
        if self.game_over:
            return

        if self.pacman_direction != (0, 0):
            self.canvas.move(self.pacman, self.pacman_direction[0], self.pacman_direction[1])
            self.check_boundaries()

        self.check_collisions()
        if self.power_up_active:
            self.power_up_time -= 1
            if self.power_up_time <= 0:
                self.power_up_active = False
                self.canvas.itemconfig(self.pacman, fill='yellow')  # Pac-Man turns back to yellow

        self.root.after(100, self.move_pacman)

    def move_ghosts(self):
        if self.game_over:
            return

        for ghost in self.ghosts:
            gx1, gy1, gx2, gy2 = self.canvas.coords(ghost)
            px1, py1, px2, py2 = self.canvas.coords(self.pacman)

            # Move ghosts towards Pac-Man
            if abs(px1 - gx1) > abs(py1 - gy1):
                if px1 < gx1:
                    self.canvas.move(ghost, -5, 0)
                else:
                    self.canvas.move(ghost, 5, 0)
            else:
                if py1 < gy1:
                    self.canvas.move(ghost, 0, -5)
                else:
                    self.canvas.move(ghost, 0, 5)

            self.check_boundaries()

        self.check_collisions()
        self.root.after(500, self.move_ghosts)

    def key_press(self, event):
        if event.keysym == 'Left':
            self.pacman_direction = (-10, 0)
        elif event.keysym == 'Right':
            self.pacman_direction = (10, 0)
        elif event.keysym == 'Up':
            self.pacman_direction = (0, -10)
        elif event.keysym == 'Down':
            self.pacman_direction = (0, 10)

    def key_release(self, event):
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
            self.pacman_direction = (0, 0)

    def check_boundaries(self):
        x1, y1, x2, y2 = self.canvas.coords(self.pacman)
        if x1 < 0:
            self.canvas.move(self.pacman, 400, 0)
        elif x2 > 400:
            self.canvas.move(self.pacman, -400, 0)
        elif y1 < 0:
            self.canvas.move(self.pacman, 0, 400)
        elif y2 > 400:
            self.canvas.move(self.pacman, 0, -400)

    def check_collisions(self):
        if self.game_over:
            return

        pacman_coords = self.canvas.coords(self.pacman)
        for pellet in self.pellets[:]:
            pellet_coords = self.canvas.coords(pellet)
            if (pacman_coords[0] < pellet_coords[2] and pacman_coords[2] > pellet_coords[0] and
                pacman_coords[1] < pellet_coords[3] and pacman_coords[3] > pellet_coords[1]):
                self.canvas.delete(pellet)
                self.pellets.remove(pellet)
                self.score += 10
                self.update_score()

        for power_up in self.power_ups[:]:
            power_up_coords = self.canvas.coords(power_up)
            if (pacman_coords[0] < power_up_coords[2] and pacman_coords[2] > power_up_coords[0] and
                pacman_coords[1] < power_up_coords[3] and pacman_coords[3] > power_up_coords[1]):
                self.canvas.delete(power_up)
                self.power_ups.remove(power_up)
                self.power_up_active = True
                self.power_up_time = 50  # Power-up lasts for 50 cycles
                self.canvas.itemconfig(self.pacman, fill='blue')  # Pac-Man turns blue

        for ghost in self.ghosts:
            ghost_coords = self.canvas.coords(ghost)
            if (pacman_coords[0] < ghost_coords[2] and pacman_coords[2] > ghost_coords[0] and
                pacman_coords[1] < ghost_coords[3] and pacman_coords[3] > ghost_coords[1]):
                if not self.power_up_active:
                    self.game_over = True
                    self.canvas.create_text(200, 200, text="Game Over", fill='red', font=('Arial', 24))
                else:
                    self.canvas.delete(ghost)
                    self.ghosts.remove(ghost)
                    self.score += 50  # Extra points for eating a ghost
                    self.update_score()

        if not self.pellets:
            self.level += 1
            self.canvas.create_text(200, 200, text=f"Level {self.level}", fill='white', font=('Arial', 24))
            self.root.after(2000, self.reset_level)

    def reset_level(self):
        self.canvas.delete('all')
        self.pacman = self.canvas.create_oval(180, 180, 220, 220, fill='yellow')
        self.ghosts = []
        self.pellets = []
        self.power_ups = []
        self.create_ghosts()
        self.create_pellets()
        self.create_power_ups()
        self.update_score()

    def update_score(self):
        self.canvas.delete('score')
        self.canvas.create_text(10, 10, anchor='nw', text=f"Score: {self.score}", fill='white', font=('Arial', 12), tags='score')

# Create the main window
root = tk.Tk()
app = PacManGame(root)
root.mainloop()
