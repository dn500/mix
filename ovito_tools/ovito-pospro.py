from ovito.data import *
from ovito.vis import *
from ovito.data import *
from ovito.pipeline import *
from ovito.modifiers import *
from ovito.io import *

import math
import numpy as np
import matplotlib.pyplot as plt



def quaternions_to_colors(qs):
    """ Takes a list of quaternions (Nx4 array) and returns a list of corresponding RGB colors (Nx3 array) """
 
    if len(qs.shape) != 2:
        raise RuntimeError("qs must be a 2-dimensional array")
 
    if qs.shape[1] != 4:
        raise RuntimeError("qs must be a n x 4 dimensional array")
 
    # Project quaternions into Rodrigues space: rs = (qs.X/qs.W, qs.Y/qs.W, qs.Z/qs.W)
    # Note that the qs.W may be zero for particles for which no lattice orientation
    # could be computed by the PTM modifier.
    rs = np.zeros_like(qs[:,:3])
    np.divide(qs[:,0], qs[:,3], out=rs[:,0], where=qs[:,3] != 0)
    np.divide(qs[:,1], qs[:,3], out=rs[:,1], where=qs[:,3] != 0)
    np.divide(qs[:,2], qs[:,3], out=rs[:,2], where=qs[:,3] != 0)

    # Compute vector lengths rr = norm(rs)
    rr = np.linalg.norm(rs, axis=1)
    rr = np.maximum(rr, 1e-9) # hack
 
    # Normalize Rodrigues vectors.
    rs[:,0] /= rr
    rs[:,1] /= rr
    rs[:,2] /= rr
 
    theta = 2 * np.arctan(rr)
    rs[:,0] *= theta
    rs[:,1] *= theta
    rs[:,2] *= theta
    
    # Normalize values.
    rs += math.radians(62.8)
    rs[:,0] /= 2*math.radians(62.8)
    rs[:,1] /= 2*math.radians(62.8)
    rs[:,2] /= 2*math.radians(62.8)
    
    return rs

def modify(frame,input):
    nparticles = input.number_of_particles
    fcc_count = input.attributes['PolyhedralTemplateMatching.counts.FCC']
    bcc_count = input.attributes['PolyhedralTemplateMatching.counts.BCC']
    hcp_count = input.attributes['PolyhedralTemplateMatching.counts.HCP']
    
    # print(input.number_of_particles)
    # print(input.attributes.keys())
    # input.particle_properties.append(PolyhedralTemplateMatching)
    # print(input.particle_properties.keys())
    # print('N =',nparticles)
    print('FCC =',fcc_count)
    print('BCC =',bcc_count)
    print('HCP =',hcp_count)

    # Input
    # orientations = input.particles['Orientation']
    # print(quaternions_to_colors(orientations))
    # print(type(quaternions_to_colors(orientations)))
    # Qrgb=quaternions_to_colors(orientations)
    # save_to_color_map(input.particles['Position'],Qrgb)
    # Output:
    # input.particles_.create_property('Color', data=quaternions_to_colors(orientations))

pip = import_file('/home/david/Simulations/Ag-nc-E.dump.comp.45000')



pip.modifiers.append(PolyhedralTemplateMatchingModifier(output_orientation=True))
pip.compute()

# print(pip.compute().attributes.keys())

# pip.modifiers.append(SelectParticleTypeModifier(StructureType==0))
pip.modifiers.append(SelectParticleTypeModifier(property="Structure Type",type=0))


for d in np.linspace(-10,780,3):
    pip.modifiers.append(SliceModifier(normal=(1,0,0),distance=d,slab_width=15.0))

    pip.add_to_scene()
    vp = Viewport()
    vp.camera_pos = (800, 0, 0)
    vp.camera_dir = (-1, 0, 0)

    rs = RenderSettings(size=(800,600), filename="verticecut/image"+str(d)+".png")
    vp.render(rs)