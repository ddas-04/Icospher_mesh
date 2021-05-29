# Icospher_mesh

Here 'subdiv' parameter controls the mesh quality.

'verts_array' denotes the vertex coordinates. verts_array=[n,3], where n=number of vertex and 3 denotes x,y,z coordinates

Here face is a triangle. 
'face_index_data' is a kX3 matrix such as 
array([[ 0, 12, 14],
       [11, 13, 12],
             .
             .
             .
       [ 1, 23, 30],
       [41, 30, 23]])

Here each row denotes information about the single triangle and column values for a each row denotes 3 indices of (i.e. row number) of verts_array. For example, face_index_data[0,0]=[0,12,14] denotes the triangle consists of 3 points whose cordinates are verts_array[0,:], verts_array[12,:], and verts_array[14,:]

Vertices are plotted with red marker
Each face is colored in blue(default).

For each face, i.e. the triangle consists of three lines. For face in the above example, 
Line_1=joining verts_array[0,:] to verts_array[12,:], 
Line_2=joining verts_array[12,:] to verts_array[14,:], 
Line_3=joining verts_array[14,:] to verts_array[0,:], 


