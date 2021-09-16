import math , pygame , sys 
pygame.init()
WIDTH,HEIGHT = 900,600
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
FONT = pygame.font.Font("freesansbold.ttf",20) 
RADIUS = 100 
MASS = RADIUS/5 
OMEGA = 37
RECOIL_ALPHA = 2.7
# it is the angular acceleration of the torque provided by the axis of rotation on rotating ,
# it can be considered equivalent to friction

WHEEL_X,WHEEL_Y = WIDTH//2 - RADIUS , HEIGHT//2 - RADIUS
TIME = 0.5

class Start_btn:
	def __init__(self):
		self.width,self.height = 100,50 
		self.x,self.y = WIDTH - self.width,HEIGHT - self.height 

	def should_start(self):
		m_pos,m_pressed = pygame.mouse.get_pos(),pygame.mouse.get_pressed() 
		if self.x+self.width>=m_pos[0]>=self.x and self.y+self.height>=m_pos[1]>=self.y : 
			pygame.draw.rect(SCREEN,(0,255,0),pygame.Rect(self.x,self.y,self.width,self.height))
			if True in m_pressed:
				return True  
		else:
			pygame.draw.rect(SCREEN,(0,128,0),pygame.Rect(self.x,self.y,self.width,self.height))

		return False 


class Wheel:
	def __init__(self,radius,mass,recoil_alpha,time,moment_of_inertia):
		self.radius = radius
		self.mass = mass
		self.recoil_alpha = recoil_alpha
		self.time = time 
		self.moment_of_inertia = moment_of_inertia


	def rotate(self,wheel_img,omega):
		new_omega = omega - self.recoil_alpha*time #w = w_original + alpha * time  
		rotating_angle = new_omega*time - 0.5*self.recoil_alpha*(time)**2  # theta = w*t + 0.5*alpha*time^2
		wheel_img = pygame.transform.rotate(wheel_img,rotating_angle)
		new_wheel_x,new_wheel_y = WIDTH//2 - radius - int(wheel_img.get_width()/2),HEIGHT//2 - radius - int(wheel_img.get_height()/2) 

		#defining other quantities
		self.angular_momentum = self.moment_of_inertia * omega
		#angular momentum = moment of inertia * omega = Force * radius X  velocity || cross product of radius and velocity 
		#here the force is acting tangential to the rigid body so the cos(90) = 1 so angular momentum = force * raidus * velocity
		
		self.angular_momentum_font = FONT.render("Angular Momentum : " + str(self.angular_momentum),True,(0,0,0))
		self.omega_font = FONT.render("Angular Velocity : " + str(omega),True,(0,0,0)) 

		return [wheel_img,new_omega,new_wheel_x,new_wheel_y,self.angular_momentum_font,self.omega_font]



if __name__ == '__main__':
	radius = RADIUS
	mass = radius/5  # mass follows the realtion => mass = f(radius) =  radius/5 
	omega = OMEGA
	recoil_alpha = RECOIL_ALPHA
	wheel_img = pygame.transform.scale(pygame.image.load("wheel.png"),(2*radius,2*radius))
	wheel_x,wheel_y = WHEEL_X,WHEEL_Y
	time = TIME
	moment_of_inertia = mass*(radius)**2/2 
	#moment of inertia of a disc if axis of rotation is the center = MR^2/2; obtained by integrating the 
	#moment of inertia of ring which is MR^2 as in a ring all masses are at a distance of radius from the 
	#centre if the axis of rotation is the center
	
	recoil_torque = moment_of_inertia * recoil_alpha
	#torque = force X radius (cross product of force and raidus)

	moi_font = FONT.render("Moment Of Inertia : " + str(moment_of_inertia),True,(0,0,0))
	recoil_torque_font = FONT.render("Recoil Torque : " + str(recoil_torque),True,(0,0,0))

	start = False 
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				pygame.quit()
				sys.exit()

		wheel = Wheel(radius,mass,recoil_alpha,time,moment_of_inertia) 
		fonts = [moi_font,recoil_torque_font]

		if start :  
			if omega > 0 : 
				temp = wheel.rotate(wheel_img,omega)
				wheel_img,omega,wheel_x,wheel_y = temp[0],temp[1],temp[2],temp[3]
				fonts.append(temp[4])
				fonts.append(temp[5]) 
			else:
				fonts.append(FONT.render("Angular Momentum : 0 ",True,(0,0,0)))
				fonts.append(FONT.render("Angular Velocity : 0 ",True,(0,0,0)))
				start = False 

				omega = OMEGA
				wheel_img = pygame.transform.scale(pygame.image.load("wheel.png"),(2*radius,2*radius))
				wheel_x,wheel_y = WHEEL_X,WHEEL_Y


			SCREEN.fill((255,255,255))
			SCREEN.blit(wheel_img,(wheel_x,wheel_y))
			fy =  0 
			for i in fonts:
				SCREEN.blit(i,(0,fy))
				fy += 30 
		else:
			SCREEN.fill((255,255,255))
			SCREEN.blit(wheel_img,(wheel_x,wheel_y))
			btn = Start_btn()
			start = btn.should_start() 


		pygame.time.Clock().tick(time*60) 
		pygame.display.update()




