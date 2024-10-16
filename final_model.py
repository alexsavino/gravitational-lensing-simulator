#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Importing necessary packages...
import math as m
import itertools
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import re
import time
import turtle
from turtle import *


#Important constants... 
c = 2.9979e8 #[m/s]
G = 6.6743e-11 #[m^3/kg^1*s^2]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Introducing the user to the program...
print("Hello! Welcome to the Gravitational Lensing Simulator (by Alex Savino hahah)!")

print("""\n   This simulation includes two objects - a black hole (in solid blue) that acts
as a foreground lens and a background star (in unfilled orange) whose light is bent
due to the presence of the black hole as seen by the observer. The source is moved
across the sky horizontally at a constant speed to allow the user to best visualize
the deflection the light rays from the star experience at given points during the
star's transit. The position of the deflected photons (in yellow) at each point
during the physical star's transit are saved and continually displayed throughout
the transit, resulting in the creation of a yellow streak.
      """)

#Allowing the user to choose if they'd like a brief overview of gravitational lensing...
while True:
  information_request = input("\nWould you like to learn a little bit about gravitational lensing?: ")
  stripped_input = information_request.strip(" ,'")
  split_input = re.split('[ ,.]',stripped_input)
  if (len(split_input)==1):
    if (stripped_input.upper()=="YES"):
      print("\nSounds good!")
      print("""\n   In 1915, Albert Einstein published his theory of general relativity
      that concerned how gravity affects the fabric of space-time; it was
      in this paper that he put forth his prediction of 'gravitational lensing.'
      (Since then, scientists have documented many examples of gravitational
      lensing, confirming this prediction.) Similar to the way a bowling ball
      on a trampoline causes the trampoline to bend, a massive object in space
      causes *space itself* to bend! This effect has a lot of consequences
      including bending the path of photons, (light particles) that travel near
      said massive object similar to a lens. This light-bending effect *is*
      gravitational lensing, and it's how scientists are able to do a range of
      analyses, from determining the mass of hard-to-observe lenses (like black
      holes) or to observing faint background objects whose light by nature of
      traveling near a lens is magnified to an observable level...
      """)
      print("\n(Case in point, gravitational lensing is both cool *and* useful!)")
      print("Now for the fun stuff!...")
      break
    elif (stripped_input.upper()=="NO"):
      print("\nNo worries! Let's go right to the fun stuff...")
      break
    else:
        print("Sorry! Please input 'Yes' or 'No'...")
        continue
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Allowing the user to set values for allowed parameters...
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#1: BH mass...
while True:
  raw_bh_mass = input("\nEnter a MASS for your black hole between 0.5 and 20.0 solar masses?: ")
  stripped_input = raw_bh_mass.strip(" ,'")
  split_input = re.split('[ ,]',stripped_input)
  if (len(split_input)==1):
    try:
      value = int(raw_bh_mass)
      if (value>=0.5 and value<=20.0):
        break
      else:
        print("Sorry! It looks like your request is out of range...")
        pass
    except ValueError:
      try:
        value = round(float(raw_bh_mass),2)
        if (value>=0.5 and value<=20.0):
          break
        else:
          print("Sorry! It looks like your request is out of range!...")
          pass
      except ValueError:
        print("Sorry! It looks like you entered a word... \nPlease print a single number below... ")
  else:
    print("Sorry! It looks like you entered more than one word... \nPlease print a single number below... ")

try:
    raw_bh_mass = int(raw_bh_mass)
except:
    raw_bh_mass = float(raw_bh_mass)
    
#Calculating user-input BH radius...
bh_radius = (2*G*raw_bh_mass)/(c**2) #[m]
print("This mass means that your black hole's radius is ", bh_radius, ".\n", sep='')
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#2: Star radius...
while True:
  raw_physical_star_radius = input("Enter a RADIUS for your star between 5.00e15m and 8.00e15m?: ")
  stripped_input = raw_physical_star_radius.strip(" ,'m") #,'
  split_input = re.split('[ ,]',stripped_input)
  if (len(split_input)==1):
    try:
      value = float(stripped_input)
      if (value>=5.00e15 and value<=8.00e15):
        break
      else:
        print("Sorry! It looks like your request is out of range...")
    except ValueError:
      print("Sorry! It looks like you entered a word... \nPlease print a single number below... ")
  else:
    print("Sorry! It looks like you entered more than one word... \nPlease print a single number below... ")
raw_physical_star_radius = float(stripped_input)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#3: Star height along y-axis...
while True:
    user_height_percentage = input("\nHow high along the y-axis would you like your background star to be (in a percent)?: ")
    stripped_input = user_height_percentage.strip(" ,%'")
    #print(stripped_input)
    split_input = re.split('[ ,%]',stripped_input)
    if (len(split_input)==1):
        try:
            percent = int(stripped_input)
            if (percent>=0 and percent<=100):
                break
            else:
                print("Sorry! Please print a number between 0 and 100 below... ")
                continue
        except ValueError:
            try:
                percent = float(stripped_input),2
                if (percent>=0.00 or percent<=100.00):
                    break
                else:
                    print("Sorry! Please print a number between 0 and 100 below... ")
                continue
            except ValueError:
              print("Sorry! It looks like you entered a word... \nPlease print a number between 0 and 100 below... ")
              continue
    else:
        print("Sorry! It looks like you entered more than one word... \nPlease print a single number between 0 and 100 below... ")

user_height_percentage = float(stripped_input)
user_height_percentage /= 100

total_number_of_y_axis_pixels = 350
physical_star_height = (350*(user_height_percentage))-175
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#4: Allowing the user to name their simulation...
user_name = input("\nLastly, please enter your name for it to appear on top of your simulation!: ")
user_title = user_name.upper() + "'s Gravitational Lensing Simulation"
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Defining projection functions for each object...
def draw_physical_star(x,y,radius):
    diameter = (2*radius)
    pensize = diameter/20
    turtle.hideturtle()
    turtle.penup()
    turtle.setposition(x,(y-radius))
    turtle.pendown()
    turtle.pensize(pensize)
    turtle.color("orange")
    turtle.circle(radius)
    
def draw_black_hole(x,y,radius):
    diameter = (2*radius)
    try:
        circumference = m.pi*int(diameter)
    except:
        circumference = m.pi*float(diameter)

    number_of_lines = int(circumference/2)
    turtle.penup()
    turtle.setposition(x,y)
    turtle.pendown()
    turtle.color("blue")
    turtle.dot(diameter)

def draw_einstein_ring(radius):
    circumference = (2*m.pi*radius)
    number_of_lines = 30
    step_angle = 360/number_of_lines
    length_of_line = circumference/(number_of_lines*3)
    for i in range(0,(number_of_lines+1)):
        turtle.color("red")
        turtle.hideturtle()
        turtle.pensize(2)
        turtle.penup()
        turtle.left(i*step_angle)
        turtle.forward(radius)
        turtle.left(90)
        turtle.pendown()
        turtle.forward(length_of_line)
        turtle.penup()
        turtle.setposition(0,0)
        turtle.home()
        turtle.pendown()

#To display the seen_star...
def draw_yellow_dot(x_position,y_position):
    turtle = Turtle()
    turtle.hideturtle()
    turtle.penup()
    turtle.setposition(x_position, y_position)
    turtle.pendown()
    turtle.color("yellow")
    turtle.dot(3)
    return turtle

def instantiate_seen_star(x,y,max_radius,step_angle):
    seen_star_turtles_list = []
    radius = 0
    while True:
        diameter = (2*radius)
        try:
            circumference = m.pi*int(diameter)
        except:
            circumference = m.pi*float(diameter)
        number_of_points = int(circumference/2)
        for i in range(0,number_of_points):
            x_position = x+radius*m.cos(m.radians(step_angle))
            y_position = y+radius*m.sin(m.radians(step_angle))
            step_angle += (360/number_of_points)
            seen_star_turtles_list.append([x_position,y_position])
        radius += 1
        if (radius>max_radius):
            return seen_star_turtles_list
            break
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Setting distance constants...
d_S = 9.75e17 #[m]
d_L = 5.00e11 #[m]
d_LS = (d_S-d_L) #[m]

#Adjusting η for y-axis shift and establishing m-to-pixels and vice versa projection ratio...
center_η_x = 1.50e15 #[m] #*constant*
pixels_to_m = (center_η_x/400) #[m/pixels]
m_to_pixels = (400/center_η_x) #[pixels/m]
center_η_y = physical_star_height*pixels_to_m

#Determining the sign of the y-axis user input...
if (center_η_y!=0):
    center_η_y_sign = (abs(physical_star_height)/physical_star_height)
else:
    center_η_y_sign = 1

#Establishing the physical_star triangle...
center_η = (center_η_x**2+center_η_y**2)**(1/2)*center_η_y_sign
β = m.atan(center_η/d_S)
d_r = (d_S/m.cos(β))

#Establishing ρ...
x_axis_vector = [1,0]
center_η_vector = [center_η_x,center_η_y]
x_axis_vector /= np.linalg.norm(x_axis_vector)
center_η_vector /= np.linalg.norm(center_η_vector)
dot_product = np.dot(x_axis_vector,center_η_vector)
ρ = np.arccos(dot_product)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Physical star projection calculations...
physical_star_ϕ = m.atan(raw_physical_star_radius/d_r)
physical_star_radius = raw_physical_star_radius*m.sin(physical_star_ϕ)
physical_star_radius *= m_to_pixels
        
#BH projection calculations...
raw_bh_mass /= (5.00e-31) #(solar masses -> kg)
raw_bh_radius = (2*G*raw_bh_mass/c**2)
bh_ϕ = m.atan(raw_bh_radius/d_L)
bh_radius = raw_bh_radius*m.sin(bh_ϕ)
bh_radius *= m_to_pixels


#Einstein radius projection calculations...
θ_E = (4*G*raw_bh_mass*d_LS/(d_L*d_S*c**2))**(1/2)
raw_e_radius = m.tan(θ_E)*d_S
e_radius = raw_e_radius*m_to_pixels
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Establishing the Turtle screen and its dimensions...
#Designing an N-body simulator to create gridlines...

#Translating user-input BH mass to proportional N-body-simulator-friendly mass...
raw_bh_mass *= ((5.00e-31))
raw_bh_mass_lower_limit = 0.5 #[solar masses]
raw_bh_mass_upper_limit = 20.0 #[solar masses]
raw_bh_mass_range = (raw_bh_mass_upper_limit-raw_bh_mass_lower_limit)
raw_bh_mass_in_range = (raw_bh_mass-raw_bh_mass_lower_limit)
raw_bh_mass_percent = (raw_bh_mass_in_range/raw_bh_mass_range)

n_body_bh_mass_lower_limit = 1.00e3 #[kg]
n_body_bh_mass_upper_limit = 1.00e4 #[kg]
n_body_bh_mass_range = (n_body_bh_mass_upper_limit-n_body_bh_mass_lower_limit)
n_body_bh_mass_percent = raw_bh_mass_percent
n_body_bh_mass_in_range = (n_body_bh_mass_range*raw_bh_mass_percent)+n_body_bh_mass_lower_limit


#Creating system and object classes...
class SystemComponent(turtle.Turtle):
  def __init__(self,lensing_system,mass,position,velocity):
    super().__init__()
    self.penup()
    self.hideturtle()
    self.mass = mass
    self.setposition(position)
    self.velocity = velocity
    lensing_system.append_component(self)
  def create_dot(self):
    self.clear()
    if isinstance(self, BlackHole):
      self.dot(1)
    if isinstance(self, Photon):
      self.dot(1)
      self.speed(1)
  def move(self):
    self.setx(self.xcor() + self.velocity[0])
    self.sety(self.ycor() + self.velocity[1])
class LensingSystem:
  def __init__(self):
    self.lensing_system = turtle.Screen()
    self.lensing_system.setup(950,350)
    self.lensing_system.bgcolor("black")
    self.lensing_system.title(user_title)
    self.lensing_system.tracer(0)
    self.components = []
  def append_component(self,component):
    self.components.append(component)
  def remove_component(self,component):
    self.components.remove(component)
  def system_update(self):
    for i in self.components:
      i.move()
      i.create_dot()
    self.lensing_system.update()
  def apply_gravity(self,m1,m2):
    theta = m1.towards(m2)
    force = (m1.mass*m2.mass)/(m1.distance(m2)**2)
    orientation = 1
    objects = [m1, m2]
    for i in objects:
      acceleration = (force/i.mass)
      x_acceleration = (acceleration*m.cos(m.radians(theta)))
      y_acceleration = (acceleration*m.sin(m.radians(theta)))
      x_velocity = ((x_acceleration*orientation)+i.velocity[0])
      y_velocity = ((y_acceleration*orientation)+i.velocity[1])
      i.velocity = (x_velocity, y_velocity)
      orientation *= -1
  def calculate_all_body_interactions(self):
    components_copy = self.components.copy()
    for idx, m1 in enumerate(components_copy):
      for m2 in components_copy[idx + 1:]:
        self.apply_gravity(m1,m2) 
class BlackHole(SystemComponent):
  def __init__(self,lensing_system,mass):
    position = (0,0)
    velocity = (0,0)
    super().__init__(lensing_system,mass,position,velocity)
    self.color("blue")     
class Photon(SystemComponent):
  def __init__(self,lensing_system,mass,position,velocity):
    super().__init__(lensing_system,mass,position,velocity)
    self.color("grey")


#Instantiating the system...
lensing_system = LensingSystem()
n_body_bh = BlackHole(lensing_system,mass=n_body_bh_mass_in_range)

'''
#Creating a list of photon objects and recording their coordinates...
photons = []
original_photon_x_positions = []
original_photon_y_positions = []
for i in range(15):
  y_position = 162-(i*22.62)
  photon = Photon(lensing_system,1e-30,(-457,y_position),(0,0))
  photons.append(photon)
  original_photon_x_positions.append(photon.xcor())
  original_photon_y_positions.append(photon.ycor())
  for j in range(40):
    x_position = -434.38+(j*22.62)
    photon = Photon(lensing_system,1e-30,(x_position,y_position),(0,0))
    photons.append(photon)
    original_photon_x_positions.append(photon.xcor())
    original_photon_y_positions.append(photon.ycor())

    
#Creating a line-drawing function...
def draw_line(current_photon,photons_behind):
  line = turtle.Turtle()
  line.hideturtle()
  line.pensize(1)
  line.color("grey")
  line.penup()
  line.setposition(photons[current_photon].xcor(),photons[current_photon].ycor())
  turtle.tracer(100000)
  line.pendown()
  line.goto(photons[photons_behind].xcor(),photons[photons_behind].ycor())

#Drawing lines between photons... (*the 'magic numbers' below are arbitrary gridline spacings!*)
def draw_specific_lines():
  for i in range(15):
    if (i==0):
      pass
    else:
      current_photon = (i*41)
      photons_behind = ((i-1)*41)
      draw_line(current_photon,photons_behind)
    for j in range(40):
      current_photon = (i*41+j+1)
      photons_behind = (i*41+j)
      draw_line(current_photon,photons_behind)
      if (i==0):
        pass
      else:
        current_photon = (i*41+j+1)
        photons_behind = ((i-1)*41+j+1)
        draw_line(current_photon,photons_behind)

#Letting the N-body simulator run for 0.2 seconds...        
turtle.tracer(0)
end_time = time.time() + 0.2
while (time.time()<=end_time):
  lensing_system.calculate_all_body_interactions()
  lensing_system.system_update()

#Relocating photons that have deviated from their initial position "too much" to the origin...
inside_photons = []
j=0
for i in photons:
  original_x = original_photon_x_positions[j]
  original_y = original_photon_y_positions[j]
  current_x = i.xcor()
  current_y = i.ycor()
  if (((abs(current_x-original_x)>=10) and (abs(current_y-original_y)>=10)) or (current_x**2+current_y**2<=bh_radius)):
    inside_photons.append(i)
    i.hideturtle()
    i.clear()
    i.setposition(0,0)
  j+=1

#Calling the grid-creating function...
draw_specific_lines()
draw_line(614,(614-41))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Adding stars in the *far background* purely for decoration...
number_of_arbitrary_background_stars = 15
turtle.tracer(1)
for i in range(1,(number_of_arbitrary_background_stars+1)):
    bg_star = turtle.Turtle()
    x_position = rand.randint(-475,475)
    y_position = rand.randint(-175,175)
    bg_star.speed(0)
    bg_star.hideturtle()
    bg_star.penup()
    bg_star.setposition(x_position,y_position)
    bg_star.pendown()
    bg_star.dot(3, "white")
turtle.tracer(0)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Creating a list of mutable (η_x,η_y) pairs to be evaluated for relative deflection...
seen_star_turtles_list = instantiate_seen_star(center_η_x*m_to_pixels,physical_star_height,physical_star_radius,0)
seen_star_position_pairs = []

for i in seen_star_turtles_list:
    position_pair = [i[0]*pixels_to_m,i[1]*pixels_to_m]
    seen_star_position_pairs.append(position_pair)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Calculating image angles and projection positions for each (η_x,η_y) pair in the seen_star...
for i in seen_star_position_pairs:
    η_x = i[0] #[m] #*constant*
    η_y = i[1]
    if (η_y!=0):
        η_y_sign = (abs(η_y)/η_y)
    else:
        η_y_sign = 1
    η = (η_x**2+η_y**2)**(1/2)*η_y_sign
    β = m.atan(η/d_S)
    d_r = (d_S/m.cos(β))

    #Estiablishing ρ...
    x_axis_vector = [1,0]
    η_vector = [η_x,η_y]
    x_axis_vector /= np.linalg.norm(x_axis_vector)
    η_vector /= np.linalg.norm(η_vector)
    dot_product = np.dot(x_axis_vector, η_vector)
    ρ = np.arccos(dot_product)
    
    #Calculating/approximating the impact parameter...
    θ_1 = (abs(β)+(abs(β)**2+4*θ_E**2)**(1/2))/2*η_y_sign
    θ_2 = (abs(β)-(abs(β)**2+4*θ_E**2)**(1/2))/2*η_y_sign

    #Calculating the shift in position between the physical_star and seen_star...
    θ_1_b = m.tan(θ_1)*d_S*η_y_sign
    θ_1_b_x = m.cos(ρ)*θ_1_b
    θ_1_b_y = m.sin(ρ)*θ_1_b    
    θ_2_b = m.tan(θ_2)*d_S*η_y_sign
    θ_2_b_x = m.cos(ρ)*θ_2_b
    θ_2_b_y = m.sin(ρ)*θ_2_b

    #Initial position condition for the seen_star...
    θ_1_seen_star_x_position = θ_1_b_x*m_to_pixels
    θ_1_seen_star_y_position = θ_1_b_y*m_to_pixels
    θ_2_seen_star_x_position = θ_2_b_x*m_to_pixels
    θ_2_seen_star_y_position = θ_2_b_y*m_to_pixels
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
a = 0
#Initial position condition for the physical_star...
physical_star_x_position = 400 #[pixels]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



turtle_list = [] #[turtle.Turtle]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def GENERAL_ANIMATE():
    global physical_star_x_position,physical_star_height,physical_star_radius,a
    global θ_1_seen_star_x_position,θ_1_seen_star_y_position
    global θ_2_seen_star_x_position,θ_2_seen_star_y_position
    global d_S,d_L,d_LS,d_r
    global ξ,center_η_x,center_η_y,center_η,center_η_y_sign
    global pixels_to_m,m_to_pixels
    global β,ρ
    global θ_1_b,θ_1_b_x,θ_1_b_y
    global θ_2_b,θ_2_b_x,θ_2_b_y
    global turtle_list
    global seen_star_position_pairs

    turtle.clear()
    for t in turtle_list:
        t.clear()
    
    #To move/re-project the physical_star...
    dx_in_physical_star_x_position = 3.99 #(This is an arbitrary number...)
    physical_star_x_position -= dx_in_physical_star_x_position
    
    #To recalculate the projected radius of the physical_star...
    d_r = (d_S/m.cos(β))
    physical_star_ϕ = m.atan(d_r/physical_star_radius)
    physical_star_radius *= m.sin(physical_star_ϕ)

    #*Objects ordered from first to be printed to last...*
    draw_physical_star(physical_star_x_position,physical_star_height,physical_star_radius)

    #Calculating image angles and projection positions for each (η_x,η_y) pair in the seen_star...

    turtle_list = []
    for i in seen_star_position_pairs:
        #print(i)
        
        i[0] -= (dx_in_physical_star_x_position * pixels_to_m)
    
        η_x = i[0]
        η_y = i[1]
        
        if (η_y!=0):
            η_y_sign = (abs(η_y)/η_y)
        else:
            η_y_sign = 1

        η = (η_x**2+η_y**2)**(1/2)*η_y_sign
        β = m.atan(η/d_S)

        #To update ρ...
        x_axis_vector = [1,0]
        η_vector = [η_x,η_y]
        x_axis_vector /= np.linalg.norm(x_axis_vector)
        η_vector /= np.linalg.norm(η_vector)
        dot_product = np.dot(x_axis_vector,η_vector)
        ρ = np.arccos(dot_product)*η_y_sign

        #To move/re-project the seen_star...
        θ_1 = (abs(β)+(abs(β)**2+4*θ_E**2)**(1/2))/2*η_y_sign
        θ_2 = (abs(β)-(abs(β)**2+4*θ_E**2)**(1/2))/2*η_y_sign

        #Calculating the shift in position between the physical_star and seen_star...
        θ_1_b = m.tan(θ_1)*d_S*η_y_sign
        θ_1_b_x = m.cos(ρ)*θ_1_b
        θ_1_b_y = m.sin(ρ)*θ_1_b
        θ_2_b = m.tan(θ_2)*d_S*η_y_sign
        θ_2_b_x = m.cos(ρ)*θ_2_b
        θ_2_b_y = m.sin(ρ)*θ_2_b

        #Calculating seen_star position...
        θ_1_seen_star_x_position = θ_1_b_x*m_to_pixels
        θ_1_seen_star_y_position = θ_1_b_y*m_to_pixels
        θ_2_seen_star_x_position = θ_2_b_x*m_to_pixels
        θ_2_seen_star_y_position = θ_2_b_y*m_to_pixels

        turtle_1 = draw_yellow_dot(θ_1_seen_star_x_position,θ_1_seen_star_y_position)
        turtle_2 = draw_yellow_dot(θ_2_seen_star_x_position,θ_2_seen_star_y_position)
        turtle_list.append(turtle_1)
        turtle_list.append(turtle_2)

    
    draw_black_hole(0,0,bh_radius)
    draw_einstein_ring(e_radius)

    turtle.update()
    
    if (physical_star_x_position<-400): return

    counter = 5
    while counter <= 5:
      ontimer(GENERAL_ANIMATE,50)
      counter += 1
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

GENERAL_ANIMATE()
print("\nThank you for using the simulation! Have a good one... :)")

