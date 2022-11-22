import sys

# import cv2
import extcolors
# from colormap import rgb2hex
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

def rgb_to_hex(r,g,b):
      return '#%02x%02x%02x' % (r, g, b)

def find_neighbours(value, df, colname):
    exactmatch = df[df[colname] == value]
    if not exactmatch.empty:
        return exactmatch.index
    else:
        if sum(list(df[colname]) < value) and sum(list(df[colname]) > value):
            lowerneighbour_ind = df[df[colname] < value][colname].idxmax()
            upperneighbour_ind = df[df[colname] > value][colname].idxmin()
            return [lowerneighbour_ind, upperneighbour_ind] 
        elif sum(list(df[colname]) < value):
            lowerneighbour_ind = df[df[colname] < value][colname].idxmax()
            return [lowerneighbour_ind]
        elif sum(list(df[colname]) > value):
            upperneighbour_ind = df[df[colname] > value][colname].idxmin()
            return [upperneighbour_ind] 

def justprint():
     print('hello');
     x = Image.open(r"./uploads/images.jpeg")
     img = extcolors.extract_from_image(x)
     print(img)
     rf= img[0]
     kf = [i[0] for i in rf]
     r = [i[0] for i in kf]
     g = [i[1] for i in kf]
     b = [i[2] for i in kf]
     hex = [rgb_to_hex(r,g,b) for r,g,b in zip(r,g,b)]
     df = pd.DataFrame()
     df['red'] = r
     df["green"] = g
     df["blue"] = b
     df["hex"] = hex
     print(df.head())
    #  x = x.save("newpic.jpeg")
    #  plt.imshow(x)
    #  plt.savefig("newpig.jpeg")
    #  plt.show()
     list_color = list(df["hex"])
     fig, ax = plt.subplots(figsize=(200,150),dpi=10)
     fig.set_facecolor('white')
     plt.savefig('bg.png')
     plt.close(fig)

# create color palette
     bg = plt.imread('bg.png')
     fig = plt.figure(figsize=(90, 90), dpi = 10)
     ax = fig.add_subplot(1,1,1)
     x_posi, y_posi, y_posi2 = 320, 25, 25
     for c in list_color:
        if  list_color.index(c) <= 5:
          y_posi += 125
          rect = patches.Rectangle((x_posi, y_posi), 290, 115, facecolor = c)
          ax.add_patch(rect)
          ax.text(x = x_posi+360, y = y_posi+80, s = c, fontdict={'fontsize': 150})
        else:
          y_posi2 += 125
          rect = patches.Rectangle((x_posi + 800, y_posi2), 290, 115, facecolor = c)
          ax.add_artist(rect)
          ax.text(x = x_posi+1160, y = y_posi2+80, s = c, fontdict={'fontsize': 150})     
     ax.axis('off')
     plt.imshow(bg)
     plt.tight_layout()
     plt.savefig('result.png')
     pantone = pd.read_excel("Project/Pantome.xlsx")
     print(pantone.head())
     print(pantone.columns)
     print(pantone.info())
     final = pd.DataFrame()
     for i in range(df.shape[0]):
         idx = find_neighbours(df.red.iloc[i],pantone,"RED")
         idx2 = find_neighbours(df.green.iloc[i],pantone.loc[idx],"GREEN")
         idx3 = find_neighbours(df.blue.iloc[i],pantone.loc[idx2],"BLUE")
         if pantone.loc[idx3].shape[0] <=1:
             final = final.append(pantone.loc[idx3])
         else:
             c = pantone.loc[idx3]
             c = c["BLUE"].sub(df.blue.iloc[i]).abs().idxmin()
             final = final.append(pantone.loc[c])
     print(final.to_dict(orient="records"))
     ex = final.HEXACODE
     ex = ["#"+str(i) for i in ex]
     #create color palette
     bg = plt.imread('bg.png')
     fig = plt.figure(figsize=(90, 90), dpi = 10)
     ax = fig.add_subplot(1,1,1)

     x_posi, y_posi, y_posi2 = 320, 25, 25
     for c in ex:
         if  ex.index(c) <= 8:
             y_posi += 125
             rect = patches.Rectangle((x_posi, y_posi), 290, 115, facecolor = c)
             ax.add_patch(rect)
             ax.text(x = x_posi+360, y = y_posi+80, s = c, fontdict={'fontsize': 150})
         else:
             y_posi2 += 125
             rect = patches.Rectangle((x_posi + 800, y_posi2), 290, 115, facecolor = c)
             ax.add_artist(rect)
             ax.text(x = x_posi+1160, y = y_posi2+80, s = c, fontdict={'fontsize': 150})
       
     ax.axis('off')
     plt.imshow(bg)
     plt.savefig("hi.png")
     plt.tight_layout()
     sys.stdout.flush()

justprint()