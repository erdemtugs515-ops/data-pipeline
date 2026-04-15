import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches


try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class RocketToMoonSimulation:
    def __init__(self):
        self.moon_position = np.array([5.0, 9.5])
        self.moon_radius = 0.3

        self.rocket1_start = np.array([3.0, 0.5])
        self.rocket2_start = np.array([7.0, 0.5])
        
        self.rocket1_pos = self.rocket1_start.copy()
        self.rocket2_pos = self.rocket2_start.copy()
        
        self.rocket_speed = 0.05
        self.min_distance = 0.8
        self.rocket_radius = 0.2
        
        self.countdown_value = 5
        self.simulation_started = False
        self.rocket1_landed = False
        self.rocket2_landed = False
        self.notification_shown = False
        
        self.frame = 0

        self.setup_plot()
        self.setup_music()
    
    def setup_music(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
            self.create_simple_music()
    
    def create_simple_music(self):
        if PYGAME_AVAILABLE:
            try:
                sample_rate = 44100
                duration = 0.3
                frequency = 440
                
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                tone = np.sin(frequency * t * 2 * np.pi)     
                audio = (tone * 32767).astype(np.int16)
                stereo_audio = np.column_stack((audio, audio))
        
                self.beep_sound = pygame.sndarray.make_sound(stereo_audio)
            except Exception as e:
                self.beep_sound = None
    
    def play_countdown_beep(self):
        if PYGAME_AVAILABLE and hasattr(self, 'beep_sound') and self.beep_sound:
            try:
                self.beep_sound.play()
            except:
                pass
    
    def play_success_sound(self):
        if PYGAME_AVAILABLE:
            try:
                sample_rate = 44100
                duration = 0.5
                
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                tone = (np.sin(523 * t * 2 * np.pi) + 
                       np.sin(659 * t * 2 * np.pi) + 
                       np.sin(784 * t * 2 * np.pi)) / 3
                
                fade = np.linspace(1, 0, len(t))
                tone = tone * fade
                
                audio = (tone * 32767).astype(np.int16)
                stereo_audio = np.column_stack((audio, audio))
                
                success_sound = pygame.sndarray.make_sound(stereo_audio)
                success_sound.play()
            except:
                pass
    
    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.patch.set_facecolor("#040423")
        self.ax.set_facecolor('#040423')
        
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        
        self.ax.set_xlabel('Distance (units)', color='white', fontsize=12)
        self.ax.set_ylabel('Altitude (units)', color='white', fontsize=12)
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_color('white')
        

        self.moon = plt.Circle(self.moon_position, self.moon_radius, 
                               color="#d3d3d3", ec="#acacac", linewidth=2)
        self.ax.add_patch(self.moon)

        self.ax.annotate('MOON', self.moon_position + np.array([0, 0.7]),
                        ha='center', fontsize=14, color='#f5f5dc', fontweight='bold')
        
        self.rocket1_plot, = self.ax.plot([], [], marker='^', markersize=20, 
                                          color="#ff0000", label="Ernest's rocket",
                                          markeredgecolor='white', markeredgewidth=1)
        self.rocket2_plot, = self.ax.plot([], [], marker='^', markersize=20, 
                                          color="#0000ff", label="Kernest's rocket",
                                          markeredgecolor='white', markeredgewidth=1)
        

        self.trail1_x, self.trail1_y = [], []
        self.trail2_x, self.trail2_y = [], []
        self.trail1_line, = self.ax.plot([], [], 'r-', alpha=0.3, linewidth=2)
        self.trail2_line, = self.ax.plot([], [], 'b-', alpha=0.3, linewidth=2)
        
        self.countdown_text = self.ax.text(5, 5, '', ha='center', va='center',
                                           fontsize=40, color='white', fontweight='bold')
        
        self.status_text = self.ax.text(5, 0.2, '', ha='center', va='bottom',
                                        fontsize=12, color='white')
        

        self.notification_text = self.ax.text(5, 8.5, '', ha='center', va='center',
                                              fontsize=16, color="#ffffff", fontweight='bold',
                                              bbox=dict(boxstyle='round', facecolor='#003300', 
                                                       edgecolor="#ffffff", alpha=0.8))
        
        self.ax.legend(loc='upper left', facecolor='#1a1a4e', edgecolor='white',
                      labelcolor='white', fontsize=10)

        self.ax.set_title('Ernest and Kernest travel to the moon', 
                         color='white', fontsize=16, fontweight='bold', pad=20)
        
    def calculate_rocket_velocities(self):
        dir1 = self.moon_position - self.rocket1_pos
        dir2 = self.moon_position - self.rocket2_pos
        
        dist1 = np.linalg.norm(dir1)
        dist2 = np.linalg.norm(dir2)
        
        if dist1 > 0:
            dir1 = dir1 / dist1
        if dist2 > 0:
            dir2 = dir2 / dist2

        rocket_distance = np.linalg.norm(self.rocket2_pos - self.rocket1_pos)
        
        if rocket_distance < self.min_distance and rocket_distance > 0:
            avoid_dir = self.rocket1_pos - self.rocket2_pos
            avoid_dir = avoid_dir / np.linalg.norm(avoid_dir)

            perp1 = np.array([-avoid_dir[1], avoid_dir[0]])
            perp2 = np.array([avoid_dir[1], -avoid_dir[0]])

            avoidance_strength = (self.min_distance - rocket_distance) / self.min_distance
            
            dir1 = dir1 + avoid_dir * avoidance_strength * 2 + perp1 * avoidance_strength
            dir2 = dir2 - avoid_dir * avoidance_strength * 2 + perp2 * avoidance_strength

            dir1 = dir1 / np.linalg.norm(dir1)
            dir2 = dir2 / np.linalg.norm(dir2)

        speed1 = self.rocket_speed * (1 + 0.1 * np.sin(self.frame * 0.1))
        speed2 = self.rocket_speed * (1 + 0.1 * np.cos(self.frame * 0.1))
        
        return dir1 * speed1, dir2 * speed2
    
    def check_moon_collision(self, pos):
        distance = np.linalg.norm(pos - self.moon_position)
        return distance < (self.moon_radius + self.rocket_radius)
    
    def update(self, frame):
        self.frame = frame

        if not self.simulation_started:
            if frame < 50:
                self.countdown_text.set_text('Simulation starting')
                return self.rocket1_plot, self.rocket2_plot, self.countdown_text
            
            countdown_frame = (frame - 50) // 30
            
            if countdown_frame < 5:
                count = 5 - countdown_frame
                self.countdown_text.set_text(str(count))
                
                if (frame - 50) % 30 == 0:
                    self.play_countdown_beep()
            elif countdown_frame == 5:
                self.countdown_text.set_text('Launch')
                self.play_countdown_beep()
            else:
                self.countdown_text.set_text('')
                self.simulation_started = True
            self.rocket1_plot.set_data([self.rocket1_pos[0]], [self.rocket1_pos[1]])
            self.rocket2_plot.set_data([self.rocket2_pos[0]], [self.rocket2_pos[1]])
            
            return (self.rocket1_plot, self.rocket2_plot, self.countdown_text,
                   self.trail1_line, self.trail2_line, self.status_text, self.notification_text)
        
        vel1, vel2 = self.calculate_rocket_velocities()   
        if not self.rocket1_landed:
            self.rocket1_pos = self.rocket1_pos + vel1
            self.trail1_x.append(self.rocket1_pos[0])
            self.trail1_y.append(self.rocket1_pos[1])
            
            if self.check_moon_collision(self.rocket1_pos):
                self.rocket1_landed = True
                self.play_success_sound()
        
        if not self.rocket2_landed:
            self.rocket2_pos = self.rocket2_pos + vel2
            self.trail2_x.append(self.rocket2_pos[0])
            self.trail2_y.append(self.rocket2_pos[1])
            
            if self.check_moon_collision(self.rocket2_pos):
                self.rocket2_landed = True
                self.play_success_sound()
        
        self.rocket1_plot.set_data([self.rocket1_pos[0]], [self.rocket1_pos[1]])
        self.rocket2_plot.set_data([self.rocket2_pos[0]], [self.rocket2_pos[1]])
        
        self.trail1_line.set_data(self.trail1_x, self.trail1_y)
        self.trail2_line.set_data(self.trail2_x, self.trail2_y)

        dist_between = np.linalg.norm(self.rocket2_pos - self.rocket1_pos)
        self.status_text.set_text(f'Distance between rockets: {dist_between:.2f} units')

        if self.rocket1_landed and self.rocket2_landed and not self.notification_shown:
            self.notification_text.set_text('Both rockets landed on the moon')
            self.notification_shown = True
        
        return (self.rocket1_plot, self.rocket2_plot, self.countdown_text,
               self.trail1_line, self.trail2_line, self.status_text, self.notification_text)
    
    def run(self):
        self.anim = FuncAnimation(self.fig, self.update, frames=500,
                                  interval=50, blit=False, repeat=False)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    print("Ernest and Kernest travel to the moon")
    print("\nStarting simulation...")
    sim = RocketToMoonSimulation()
    sim.run()

