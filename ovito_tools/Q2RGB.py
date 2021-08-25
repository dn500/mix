from ovito.data import *
import math
import numpy as np
  
def elementwise_multiplication(a, b):
 
    a[:,0] = np.multiply(a[:,0], b)
    a[:,1] = np.multiply(a[:,1], b)
    a[:,2] = np.multiply(a[:,2], b)
     
def project_quaternions_into_rodrigues_space(qs):
 
    if len(qs.shape) != 2:
        raise Exception("qs must be a 2-dimensional array")
 
    if qs.shape[1] != 4:
        raise Exception("qs must be a n x 4 dimensional array")
         
    rs = np.copy(qs[:,:3])
    elementwise_multiplication(rs, 1 / qs[:,3])
    return rs
 
def quaternions_to_colors(qs):
 
    if len(qs.shape) != 2:
        raise Exception("qs must be a 2-dimensional array")
 
    if qs.shape[1] != 4:
        raise Exception("qs must be a n x 4 dimensional array")
 
    m1 = math.radians(62.8)
    m0 = -m1
 
    rs = project_quaternions_into_rodrigues_space(qs)
    rr = np.linalg.norm(rs, axis=1)
    rr = np.maximum(rr, 1E-9)    #hack
 
    elementwise_multiplication(rs, 1 / rr)
 
    theta = 2 * np.arctan(rr)
    elementwise_multiplication(rs, theta)
    rs -= m0
 
    elementwise_multiplication(rs, 1 / (m1 - m0))
    return rs
	
def modify(frame, input, output):
	color_property = output.create_particle_property(ParticleProperty.Type.Color)
	color_property.marray[:] = quaternions_to_colors(input.particle_properties.orientation.array)