######################################################################
#                        Instructions                                #
#                                                                    #
#    In the 'Main parameter to tune' section change subdiv to        #
#    control the mesh density.                                       #
#    subdiv takes only integer value.                                #
#                                                                    #
#    verts_array stores the cartesian coordinates.                   #
#                                                                    #
######################################################################




from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
plt.rcParams.update({'font.size':15})
plt.rcParams['axes.labelweight'] = 'bold'
#plt.rcParams.update({'font.weight':'bold'})
plt.rcParams["font.family"] = "Times New Roman"

def vertex(x, y, z):
    """ Return vertex coordinates fixed to the unit sphere """

    length = sqrt(x**2 + y**2 + z**2)

    return [(i * scale) / length for i in (x,y,z)]
    
def middle_point(point_1, point_2):
    """ Find a middle point and project to the unit sphere """

    # We check if we have already cut this edge first
    # to avoid duplicated verts
    smaller_index = min(point_1, point_2)
    greater_index = max(point_1, point_2)

    key = '{0}-{1}'.format(smaller_index, greater_index)

    if key in middle_point_cache:
        return middle_point_cache[key]

    # If it's not in cache, then we can cut it
    vert_1 = verts[point_1]
    vert_2 = verts[point_2]
    middle = [sum(i)/2 for i in zip(vert_1, vert_2)]

    verts.append(vertex(*middle))

    index = len(verts) - 1
    middle_point_cache[key] = index

    return index
  
############# Main parameter to tune ###############
subdiv = 5
################################################  
  
scale = 1

middle_point_cache = {}

# Golden ratio
PHI = (1 + sqrt(5)) / 2

verts = [
          vertex(-1,  PHI, 0),
          vertex( 1,  PHI, 0),
          vertex(-1, -PHI, 0),
          vertex( 1, -PHI, 0),

          vertex(0, -1, PHI),
          vertex(0,  1, PHI),
          vertex(0, -1, -PHI),
          vertex(0,  1, -PHI),

          vertex( PHI, 0, -1),
          vertex( PHI, 0,  1),
          vertex(-PHI, 0, -1),
          vertex(-PHI, 0,  1),
        ]


faces = [
         # 5 faces around point 0
         [0, 11, 5],
         [0, 5, 1],
         [0, 1, 7],
         [0, 7, 10],
         [0, 10, 11],

         # Adjacent faces
         [1, 5, 9],
         [5, 11, 4],
         [11, 10, 2],
         [10, 7, 6],
         [7, 1, 8],

         # 5 faces around 3
         [3, 9, 4],
         [3, 4, 2],
         [3, 2, 6],
         [3, 6, 8],
         [3, 8, 9],

         # Adjacent faces
         [4, 9, 5],
         [2, 4, 11],
         [6, 2, 10],
         [8, 6, 7],
         [9, 8, 1],
        ]
for i in range(subdiv):
    faces_subdiv = []

    for tri in faces:
        v1 = middle_point(tri[0], tri[1])
        v2 = middle_point(tri[1], tri[2])
        v3 = middle_point(tri[2], tri[0])

        faces_subdiv.append([tri[0], v1, v3])
        faces_subdiv.append([tri[1], v2, v1])
        faces_subdiv.append([tri[2], v3, v2])
        faces_subdiv.append([v1, v2, v3])

    faces = faces_subdiv
    
    
face_index_data = np.asarray(faces)   
verts_array=np.asarray(verts)  

[row_face,col_face]=face_index_data.shape


'''
scatter plot of vertex
'''
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(projection='3d')
ax.scatter(verts_array[:,0], verts_array[:,1], verts_array[:,2], s=0.5,color='red')
ax.set_box_aspect([1,1,1])

'''
trianngular surface plot
'''
for i in range(row_face):
    ix=face_index_data[i,0]
    iy=face_index_data[i,1]
    iz=face_index_data[i,2]
    
    face_x=np.array([verts_array[ix,0],verts_array[iy,0],verts_array[iz,0]]) 
    face_y=np.array([verts_array[ix,1],verts_array[iy,1],verts_array[iz,1]]) 
    face_z=np.array([verts_array[ix,2],verts_array[iy,2],verts_array[iz,2]])
    
    line_x=np.array([verts_array[ix,0],verts_array[iy,0],verts_array[iz,0],verts_array[ix,0]])
    line_y=np.array([verts_array[ix,1],verts_array[iy,1],verts_array[iz,1],verts_array[ix,1]])
    line_z=np.array([verts_array[ix,2],verts_array[iy,2],verts_array[iz,2],verts_array[ix,2]])
    
    vertices = [list(zip(face_x,face_y,face_z))]
    poly = Poly3DCollection(vertices, alpha=0.5)
    ax.add_collection3d(poly)
    
    ax.plot(line_x,line_y,line_z,'k')
 
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.savefig('subdiv='+str(subdiv)+'_sphere.png', bbox_inches='tight', pad_inches=0.0)

plt.show()



