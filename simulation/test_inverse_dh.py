import numpy as np



a1 = 1
a2 = 1
a3 = 1
a4=1
a5=1
a6=1

d1=1
d2=1
d3=1
d4=1
d5=1
d6=1

d_h_table = np.array([[np.deg2rad(90), np.deg2rad(90), 0, a1+d1],
                    [np.deg2rad(90), np.deg2rad(-90), 0, a2+d2],
                    [0,0,0,d1+d3]])

# homegen_0_1 = np.array([[np.cos(d_h_table[0][0]), -np.sin(d_h_table[0][0])*np.cos(d_h_table[0][1]), np.sin(d_h_table[0][0])*np.sin(d_h_table[0][1]), d_h_table[0][2]*np.cos(d_h_table[0][0]) ],
# [np.sin(d_h_table[0][0]), np.cos(d_h_table[0][0])*np.cos(d_h_table[0][1]), -np.cos(d_h_table[0][0])*np.sin(d_h_table[0][1]), d_h_table[0][2]*np.sin(d_h_table[0][0]) ],
# [0, np.sin(d_h_table[0][1]), np.cos(d_h_table[0][1]), d_h_table[0][3] ],
# [0,0,0,1]
# ])


dh_matrices = []

for i in range(6):

    dh_matrices.append( np.array([[np.cos(d_h_table[i][0]), -np.sin(d_h_table[i][0])*np.cos(d_h_table[i][1]), np.sin(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.cos(d_h_table[i][0]) ],
    [np.sin(d_h_table[i][0]), np.cos(d_h_table[i][0])*np.cos(d_h_table[i][1]), -np.cos(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.sin(d_h_table[i][0]) ],
    [0, np.sin(d_h_table[i][1]), np.cos(d_h_table[i][1]), d_h_table[i][3] ],
    [0,0,0,1]
    ]))

print(dh_matrices)

# i=0
# homegen_0_1 = np.array([[np.cos(d_h_table[i][0]), -np.sin(d_h_table[i][0])*np.cos(d_h_table[i][1]), np.sin(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.cos(d_h_table[i][0]) ],
# [np.sin(d_h_table[i][0]), np.cos(d_h_table[i][0])*np.cos(d_h_table[i][1]), -np.cos(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.sin(d_h_table[i][0]) ],
# [0, np.sin(d_h_table[i][1]), np.cos(d_h_table[i][1]), d_h_table[i][3] ],
# [0,0,0,1]
# ])

# i=1
# homegen_1_2 = np.array([[np.cos(d_h_table[i][0]), -np.sin(d_h_table[i][0])*np.cos(d_h_table[i][1]), np.sin(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.cos(d_h_table[i][0]) ],
# [np.sin(d_h_table[i][0]), np.cos(d_h_table[i][0])*np.cos(d_h_table[i][1]), -np.cos(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.sin(d_h_table[i][0]) ],
# [0, np.sin(d_h_table[i][1]), np.cos(d_h_table[i][1]), d_h_table[i][3] ],
# [0,0,0,1]
# ])
# i=2
# homegen_2_3 = np.array([[np.cos(d_h_table[i][0]), -np.sin(d_h_table[i][0])*np.cos(d_h_table[i][1]), np.sin(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.cos(d_h_table[i][0]) ],
# [np.sin(d_h_table[i][0]), np.cos(d_h_table[i][0])*np.cos(d_h_table[i][1]), -np.cos(d_h_table[i][0])*np.sin(d_h_table[i][1]), d_h_table[i][2]*np.sin(d_h_table[i][0]) ],
# [0, np.sin(d_h_table[i][1]), np.cos(d_h_table[i][1]), d_h_table[i][3] ],
# [0,0,0,1]
# ])


homegen_0_3 = homegen_0_1 @ homegen_1_2 @ homegen_2_3

print(d_h_table)
print(homegen_0_1)
print(homegen_1_2)
print(homegen_2_3)
print(homegen_0_3)