from tkinter import *
import math

class Root(Tk):
	def __init__(self):
		super().__init__()
		self.title("3D Rotating Cube")
		self.state("zoomed")
	
		self.can = Canvas(self, bg="#FCFCFC")
		self.can.pack(fill=BOTH, expand=1)
		self.can.update()
		
		self.scale = 1500
		
		self.distance = 8
		
		self.cube_points = [
			[-1, -1, -1], 
			[1, -1, -1],  # 1
			[1, 1, -1],   # 2
			[-1, 1, -1],  # 3
			[-1, -1, 1],  # 4
			[1, -1, 1],   # 5
			[1, 1, 1],    # 6
			[-1, 1, 1],   # 7
		]
		
		self.cube_edges = [
			[0, 1], 
			[1, 2], 
			[2, 3], 
			[3, 0],
			[4, 5],
			[5, 6],
			[6, 7],
			[7, 4],
			[0, 4],
			[1, 5],
			[2, 6],
			[3, 7],
		]
		
		#Rotation Angles
		self.angle_x = 0
		self.angle_y = 0
		self.angle_z = 0
		
		self.animate_cube()
		
	def project_point(self, x, y, z):
		factor = self.scale / (self.distance - z)
		
		px = x * factor + self.can.winfo_width() / 2
		py = y * factor + self.can.winfo_height() / 2
		
		return int(px), int(py)
		
	def rotate_x(self, x, y, z, angle):
		rad = math.radians(angle)
		
		cosa, sina = math.cos(rad), math.sin(rad)
		
		y_new = y * cosa - z * sina
		z_new = y * sina + z * cosa
		
		return x, y_new, z_new
		
	def rotate_y(self, x, y, z, angle):
		rad = math.radians(angle)
		
		cosa, sina = math.cos(rad), math.sin(rad)
		
		x_new = x * cosa + z * sina
		z_new = -x * sina + z * cosa
		
		return x_new, y,  z_new
		
	def rotate_z(self, x, y, z, angle):
		rad = math.radians(angle)
		
		cosa, sina = math.cos(rad), math.sin(rad)
		
		x_new = x * cosa - y * sina
		y_new = x * sina + y * cosa
		
		return x_new, y_new, z
		
	def draw_cube(self):
		self.can.delete("all")
		
		rotated_points = []
		
		for x,y,z in self.cube_points:
			x, y, z = self.rotate_x(x, y, z, self.angle_x)
			x, y, z = self.rotate_y(x, y, z, self.angle_y)
			x, y, z = self.rotate_z(x, y, z, self.angle_z)
			
			rotated_points.append((x, y, z))
		
		projected_points = [self.project_point(x, y, z) for x, y, z in rotated_points]
		
		for edge in self.cube_edges:
			p1 = projected_points[edge[0]]
			p2 = projected_points[edge[1]]  
			
			self.can.create_line(p1[0], p1[1], p2[0], p2[1], fill="black", width=2)
		
	def animate_cube(self):
		self.angle_x += 1
		self.angle_y += 1
		self.angle_z += 1
		
		self.draw_cube()
		
		self.after(50, self.animate_cube)
		
if __name__ == "__main__":
	root = Root()
	root.mainloop()