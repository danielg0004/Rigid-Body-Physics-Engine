# shapes.py

'''
Predefined shapes - can be easily extended
Define shapes relative to the point (0, 0, 0) and as lists where:
- The first element lists the vertices
- The second lists the edges as pairs of vertex indexes
- The third lists the faces as lists of vertex indexes (not neccesary as shown in the pyramid)
'''
shape_map = {"Cube": [[[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],[-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)], [[0,1,2,3], [1,5,6,2], [5,4,7,6],[4,0,3,7],[4,5,1,0],[3,2,6,7]]],
             "Pyramid": [[[0.5,-0.5,0.5],[0.5,-0.5,-0.5],[-0.5,-0.5,0.5],[-0.5,-0.5,-0.5],[0,0.5,0]],[(0,1),(0,2),(1,3),(2,3),(0,4),(1,4),(2,4),(3,4)], [[0,1,2,3],[0,1,4],[1,3,4],[2,3,4],[0,2,4]]]}
