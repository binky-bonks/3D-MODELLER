from PIL import Image
import math
from geometry import vector
#making this from gabriel gambetta's on comp. graphics
    
class light:
   def __init__(self,intensity):
      self.intensity = float(intensity)
class ambient_light(light):
   pass
class point_light(light):
   def __init__(self, intensity, position):
      super().__init__(intensity)
      self.position = position
class directional_light(light):
   def __init__(self, intensity, direction):
      super().__init__(intensity)
      self.direction = direction

class sphere:
   def __init__(self, centre, radius, color, specular,reflective):
      self.centre = centre
      self.radius = radius
      self.color = color
      self.specular = specular
      self.reflective = reflective

camera_origin = vector(0.0 ,0.0 ,0.0)

def main():
   img = Image.new("RGB", (canvas_width, canvas_height), bg_color)
   pixels = img.load()

   for cx in range(-canvas_width//2, canvas_width//2):
      for cy in range(-canvas_height//2, canvas_height//2):
         direction = canvas_to_vp(cx, cy)
         color = trace_ray(camera_origin, direction, t_max = math.inf , t_min = (1.0), recursion_depth=3)

         sx = (canvas_width//2) + cx
         sy = (canvas_height//2)-1-cy
         pixels[sx, sy] = color

   img.show()
   img.save("raytracingstuff.png")
 
scene_lights = [
   ambient_light(intensity=0.2),
   point_light(intensity=0.6, position=vector(2,1,0)),
   directional_light(intensity=0.2, direction=vector(1,4,4))
]
scene_spheres = [
   sphere(centre=vector(0,-5001,0), radius=5000, color=(255,255,0), specular=1000, reflective=0.5),
   sphere(centre=vector(0, -1, 3), radius=1, color=(255,0,0), specular=500, reflective=0.2),
   sphere(centre=vector(2, 0, 4), radius=1, color=(0,0,255), specular=500, reflective=0.3),
   sphere(centre=vector(-2,0,4), radius=1, color=(0,255,0), specular = 10, reflective=0.4)
]

canvas_width = 500
canvas_height = 500
view_width = 1.0
view_height = 1.0
projection_plane_d = 1.0
bg_color = (0,0,0)

def canvas_to_vp(cx, cy):
   vx, vy = cx*(view_width/canvas_width), cy*(view_height/canvas_height)
   return vector(vx, vy, projection_plane_d)

def intersectRaySphere(origin, direction, sphere):
   r = sphere.radius
   co = origin - sphere.centre
   a = vector.dot(direction, direction)
   b = vector.dot(co, direction)*2
   c = vector.dot(co,co)-(r*r)

   discriminant = (b**2) - (4*a*c)
   if discriminant < 0:
      return math.inf, math.inf
   t1 = (-b+math.sqrt(discriminant))/(2.0*a)
   t2 = (-b-math.sqrt(discriminant))/(2.0*a) 
   return t1, t2
def reflect_ray(R, N):
   return (N * 2.0 * vector.dot(N,R))-R
def compute_lighting(P,N,V,s):
   i = 0
   for light in scene_lights:
      if isinstance(light,ambient_light):
         i += light.intensity
         continue
    
      if isinstance(light, point_light):
         L = light.position - P
         t_max = 1
      elif isinstance(light, directional_light):
         L = light.direction
         t_max = math.inf
      #shadow check
      shadow_sphere, _ = closest_intersection(P, L, t_max, 0.0001)
      if shadow_sphere != None:
         continue
      #diffuse reflection
      n_dot_l = vector.dot(N, L)
      if n_dot_l>0:
       i += light.intensity * n_dot_l/(vector.magnitude(N)*vector.magnitude(L))
      #specular reflection
      if s!=-1:
         R = (N * 2.0 * vector.dot(N,L))-L    
         r_dot_v = vector.dot(R,V)
         if r_dot_v > 0:
            specular_factor = (r_dot_v/(vector.magnitude(R)*vector.magnitude(V)))
            i += light.intensity * (specular_factor**s)
   return i
def closest_intersection(origin, direction, t_max, t_min):
    closest_t = math.inf
    closest_sphere = None
    for sphere in scene_spheres:
      t1, t2 = intersectRaySphere(origin, direction, sphere)
      if t_min <= t1 <= t_max and t1 < closest_t:
        closest_t = t1
        closest_sphere = sphere
      if t_min <= t2 <= t_max and t2 < closest_t:
        closest_t = t2
        closest_sphere = sphere
    return closest_sphere, closest_t

def trace_ray(origin, direction, t_max, t_min, recursion_depth):
    closest_sphere, closest_t = closest_intersection(origin, direction, t_max, t_min)
    if closest_sphere == None:
       return bg_color
    P = camera_origin + direction * closest_t
    N = (P - closest_sphere.centre)
    N = vector.normalise(N)
    intensity = compute_lighting(P, N, vector.negative(direction), closest_sphere.specular)
    r = int(min(255, max(0, closest_sphere.color[0] * intensity)))
    g = int(min(255, max(0, closest_sphere.color[1] * intensity)))
    b = int(min(255, max(0, closest_sphere.color[2] * intensity))) 
    reflectiveness = closest_sphere.reflective
    #if recurison depth is zero or reflectivness of the sphere is 0 then we are done
    if recursion_depth <= 0 or reflectiveness <= 0:
       return (r, g, b)
    #To compute reflected ray
    R = reflect_ray(vector.negative(direction), N)
    reflected_color = trace_ray(P, R, math.inf, 0.0001, recursion_depth=recursion_depth-1)
    r = int(r * (1-reflectiveness) + (reflected_color[0] * reflectiveness))
    b = int(b * (1-reflectiveness) + (reflected_color[1] * reflectiveness))
    g = int(g * (1-reflectiveness) + (reflected_color[2] * reflectiveness))
    return (r, g, b)
if __name__ == "__main__":
      main()