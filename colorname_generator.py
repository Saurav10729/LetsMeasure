import cv2
import pandas as pd

global cname
<<<<<<< HEAD
=======
csv_path = 'CSV/colors.csv'
>>>>>>> 21c3336a0a9d5866f9362d11f0c6ec80cdc11b72
clicked = False
r = g = b = x_pos = y_pos = 0
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)


def get_color_name(R, G, B):
<<<<<<< HEAD
    # global cname
    # minimum = 1000
    # for i in range(len(df)):
    #     d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
    #     if d <= minimum:
    #         minimum = d
    #         cname = df.loc[i, 'color_name']
    #
    return None
=======
    global cname
    minimum = 1000
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']

    return cname
>>>>>>> 21c3336a0a9d5866f9362d11f0c6ec80cdc11b72
