import cv2
import numpy as np
import math
map_image_path = "/home/saleeq/Desktop/new_map_planning.png"
imgae = cv2.imread(map_image_path,cv2.IMREAD_GRAYSCALE)
cv2.imshow("Original Image",imgae)
grid_size =15#more than 15 required
img_dims = imgae.shape
img_x_len = img_dims[1]
img_y_len = img_dims[0]
print(f'x_size:{img_x_len}')
print(f'y_size:{img_y_len}')
n_x =math.ceil(img_x_len/grid_size)
n_y =math.ceil(img_y_len/grid_size)
res_x = grid_size*n_x
res_y = grid_size*n_y
begin_x =0# (res_x - img_x_len)//2
begin_y = 0#(res_y - img_y_len)//2
print(f'resutlant size:{res_x}')
print(f'resutlant size:{res_y}')
padding_img = np.ones((res_x,res_y),dtype=np.uint8).T*255
padding_img[begin_y:img_y_len+begin_y,begin_x:img_x_len+begin_x] =imgae
cv2.imshow("padded image",padding_img)
grid = grid_size
padded_map = padding_img
print(padded_map.shape)

image_bgr = cv2.cvtColor(padded_map, cv2.COLOR_GRAY2BGR)
for cell_y in range(n_y):
    for cell_x in range(n_x):
        start_x =cell_x*grid
        start_y =cell_y*grid
        end_x =(cell_x+1)*grid
        end_y =(cell_y+1)*grid
        if np.sum(padded_map[start_y:end_y,start_x:end_x]) >(255*grid*grid*0.89):
            #allowed cells
            cv2.rectangle(image_bgr,(start_x,start_y),(end_x,end_y),(0,100,0),1)
            #state_matrix[cell_x,cell_y]=1
        else:
            cv2.rectangle(image_bgr,(start_x,start_y),(end_x,end_y),(0,0,100),1)
            #no need to do anything unless plotting rectangles since initialized with 0s.
            pass

cv2.imshow("grid",image_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows
