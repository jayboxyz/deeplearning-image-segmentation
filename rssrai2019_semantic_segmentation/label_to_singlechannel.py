import cv2
import numpy as np
import datetime
import os

'''

水    田     	（R:0, G:200, B:0）       1
水 浇 地     	（R:150, G:250, B:0）     2
旱 耕 地     	（R:150, G:200, B:150）   3
园    地     	（R:200, G:0, B:200）     4
乔木林地     	（R:150, G:0, B:250）     5
灌木林地     	（R:150, G:150, B:250）   6
天然草地     	（R:250, G:200, B:0）     7
人工草地     	（R:200, G:200, B:0）     8
工业用地     	（R:200, G:0, B:0）       9
城市住宅     	（R:250, G:0, B:150）     10
村镇住宅     	（R:200, G:150, B:150）   11
交通运输     	（R:250, G:150, B:150）   12
河    流     	（R:0, G:0, B:200）       13
湖    泊     	（R:0, G:150, B:200）     14
坑    塘     	（R:0, G:200, B:250）     15
其他类别     	（R:0, G:0, B:0）         0

'''

def visual_to_number(label_img):
    label = np.zeros((label_img.shape[0], label_img.shape[1]), dtype=np.uint8)  #单通道label
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            if (label_img[i, j] == [0, 200, 0]).all():  # 水田
                label[i, j] = 1
            elif (label_img[i, j] == [150, 250, 0]).all():  # 水浇地
                label[i, j] = 2
            elif (label_img[i, j] == [150, 200, 150]).all():  # 旱耕地
                label[i, j] = 3
            elif (label_img[i, j] == [200, 0, 200]).all():
                label[i, j] = 4
            elif (label_img[i, j] == [150, 0, 250]).all():
                label[i, j] = 5
            elif (label_img[i, j] == [150, 150, 250]).all():
                label[i, j] = 6
            elif (label_img[i, j] == [250, 200, 0]).all():
                label[i, j] = 7
            elif (label_img[i, j] == [200, 200, 0]).all():
                label[i, j] = 8
            elif (label_img[i, j] == [200, 0, 0]).all():
                label[i, j] = 9
            elif (label_img[i, j] == [250, 0, 150]).all():
                label[i, j] = 10
            elif (label_img[i, j] == [200, 150, 150]).all():
                label[i, j] = 11
            elif (label_img[i, j] == [250, 150, 150]).all():
                label[i, j] = 12
            elif (label_img[i, j] == [0, 0, 200]).all():
                label[i, j] = 13
            elif (label_img[i, j] == [0, 150, 200]).all():
                label[i, j] = 14
            elif (label_img[i, j] == [0, 200, 250]).all():
                label[i, j] = 15
            elif (label_img[i, j] == [0, 0, 0]).all():
                label[i, j] = 0

    return label


if __name__ == '__main__':

    label_images = []
    g = os.walk("../dataset/train")
    for path, dir_list, file_list in g:
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            if "label" in os.path.join(path, file_name):
                label_images.append(os.path.join(path, file_name))


    for label in label_images:
        print(label)
        label_img = cv2.imread(label)
        label_img = cv2.cvtColor(label_img, cv2.COLOR_BGR2RGB)  # cv2默认为bgr顺序

        starttime = datetime.datetime.now()
        print(starttime)

        image = visual_to_number(label_img)

        endtime = datetime.datetime.now()
        print(endtime)
        print(endtime - starttime, "\n", (endtime - starttime).total_seconds())

        dot_index = label.rfind(".")
        cv2.imwrite(label[0:dot_index] + "_.png", image)





























