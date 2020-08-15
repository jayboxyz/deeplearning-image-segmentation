# rssrai2019_semantic_segmentation

2019年遥感图像稀疏表征与智能分析竞赛 - 遥感图像语义分割比赛地址：<http://rscup.bjxintong.com.cn/#/theme/3>

> 评分规则：比赛初赛算法评价主要采用 Kappa 系数指标。比赛初赛最终成绩由大赛评委会专家根据Kappa系数作为得分进行排名，Kappa系数越高，遥感图像语义分割结果越准确，排名越靠前。比赛决赛成绩将基于算法模型精度、效率、规模等指标加权，对算法模型性能进行综合评估与排名。

数据下载地址：https://pan.baidu.com/s/1gx4Si7S17Uqe3bt_cVkULw  [提取码: v785]

数据下载完，可以发现图像都是 7200x6800 大小。训练集、验证集和测试集位深度都是 32 位，是个 4 通道图像。

这是官方给出的数据格式说明：（注：以下`数据格式说明`是后来官方更新的。）

``` xml
数据源：高分二号MSS影像
分辨率：4米
数据格式：TIF
影像尺寸：7200x6800像素
波段排序：NIR R G B

注意：
原始影像是用ENVI classic做的预处理，可能由于版本太老，导致不兼容。
如果使用GDAL，openCV，ArcGIS，以及新版本的ENVI读取，第四个波段会出错。
推荐使用ENVI classic，matlab，IDL读取影像，或用python的libtiff库，及PIL库的CMYK模式、再转为numpy array进行处理。

语义类别及标注信息：
水      田 RGB: 0 200 0
水  浇 地 RGB: 150 250 0
旱  耕 地 RGB: 150 200 150

园      地 RGB: 200 0 200
乔木林地 RGB: 150 0 250
灌木林地 RGB: 150 150 250

天然草地 RGB: 250 200 0
人工草地 RGB: 200 200 0

工业用地 RGB: 200 0 0
城市住宅 RGB: 250 0 150
村镇住宅 RGB: 200 150 150
交通运输 RGB: 250 150 150

河      流 RGB: 0 0 200
湖      泊 RGB: 0 150 200
坑      塘 RGB: 0 200 250
其他类别 RGB: 0 0 0
```



---



使用 envi5.3.1 软件打开，可以看到第 4 波段数值都是 255。有些人发现了同样问题，我们很好奇怎么回事？我通过和一位大佬请教和交流，我差不多有了理解。以下为我的理解和实践的结果：

首先官方给出的数据格式说数据的波段的顺序为 NIR、R、G、B 顺序，它这里这么说没有错，但为什么我们在 envi 软件打开是第4 波段全为 255 呢？大概的原因是，通俗讲，就是采用了错误或不兼容的解码方式，把原本 4 波段数据给解码成了 3 波段，但头文件又指定了 4 个波段，而第 4 波段本身又是透明度波段，所以就全部补为 255 默认值了。属于错误解码。

> 补充一点：国际上，波段顺序普遍采用的是 b g r nir。

可以看到**使用 opencv、gdal 库，以及 envi、arcgis 软件都无法正确打开**，都是显示第四波段为 255，但使用 **idl、libtiff库 和 matlab 可以正确打开**，即可以看到正常的第四波段像素。

我小结出来的猜测和理解：原因应该就是 opencv、gdal、envi、arcgis 采用了错误或说不兼容的解码方式。

> 注：这里的 idl 可以理解为类似于 Python 一样的解释型语言，安装了 envi 软件，就可以打开运行。
>
> 这段 idl 代码我放在了该仓库下，文件名为 `rssrai2019_preproc.pro`。如安装了 envi 软件，则可以直接打开该文件运行代码，可以把原图像转换成正常的，**即用 idl 代码转换后，opencv、gdal 等打开第四波段是正常数值。**
>
> 参数输入类似如下：
>
> ```  xml
> rssrai_preproc,'E:\qian','tif','E:\hou','tif'
> ```
>
> 如上，可以把 qian 文件夹下的原图像转换，转换后的图像放在 hou 文件夹下。
>
> 因为 libtiff 可以正常打开原图，那么我们可以使用 libtiff 和 opencv 分别打开原图和用 idl 代码转换后的图来对比，下面是打印出的第四波段数值：
>
> ![](https://img-1256179949.cos.ap-shanghai.myqcloud.com/20190627153855.png)
>
> 可以看到结果是一致的。然后本人也亲测了：使用 gdal 库去打开 idl 代码转换后的图像，得到的数值也是正常的。
>
> 注意：opencv 读取和写入都是按照“BGR”顺序的，所以需要交换下第一和第三通道进行比较。

综上，所以如果要用上遥感图像第 4 波段信息进行训练，可以采用如下方式进行：

1. 可以使用 libtiff 等库读取，这样可以读取到正常的第 4 波段数值，然后保存的时候，比如需要保存下来随机裁剪的小图，可以使用 opencv 保存：

   ``` python
   img1 = TIFF.open(r"G:\test.tif", mode="r")
   img1 = img1.read_image(img1) # img1顺序： hir r g b
   
   hir, r, g, b = cv2.split(img1)
   im2 = cv2.merge((g,r,hir,b)) #顺序 g r hir b
   cv2.imwrite("test2.tiff", im2) #顺序 hir r g b
   ```

   注意：因为官方原图是 hir、r、g、b 顺序， tiff 是可以正常读取，那么返回的也是 hir、r、g、b 顺序，然而如果直接使用：`cv2.imwriter("test2.tiff", img2)` 得到的图像通道顺序是：g、r、hir、b，因为 opencv 的读取和写入都是按“BRG”顺序，所以这里需要：`im3 = cv2.merge((g,r,hir,b))` 交换下顺序，然后使用 imwrite 写入，这样保存下来的顺序就还是：hir、r、g、b 顺序了。当然了你也可以使用 scipy 的 misc 保存 ，下面有亲测实验。

2. 或者使用 idl 转换后，再使用 opencv、gdal 读取。

注意：在 windows 上可以看到转换后的或者 libtiff 读取后再用 opencv 保存下来的图像，都会有一种透明度的感觉，我的猜测是，windows 把第四通道当做 alpha 通道导致这样，关于 alpha 通道可以看看：[一个也许很傻的问题,在图像处理中alpha到底是什么？](http://bbs.csdn.net/topics/60421021)。（也只是我的猜测）

对于上面的方式 1，本人有亲测做实验，对原图使用 tiff 读取，然后再使用 opencv 保存：

``` python
from libtiff import TIFF
import cv2

img1 = TIFF.open(r"G:\rssrai2019_semantic_segmentation\dataset\test\GF2_PMS1__20150902_L1A0001015646-MSS1 (2).tif", mode="r")
img2 = img1.read_image(img1)

hir, r, g, b = cv2.split(img2)
im3 = cv2.merge((g,r,hir,b))
cv2.imwrite("test.tiff", im3)


# from libtiff import TIFF
# from scipy import misc
#
# ##tiff文件解析成图像序列
# ##tiff_image_name: tiff文件名；
# ##out_folder：保存图像序列的文件夹
# ##out_type：保存图像的类型，如.jpg、.png、.bmp等
# def tiff_to_image_array(tiff_image_name, out_folder, out_type):
#     tif = TIFF.open(tiff_image_name, mode="r")
#     idx = 0
#     for im in list(tif.iter_images()):
#         #
#         im_name = out_folder + str(idx) + out_type
#         misc.imsave(im_name, im)
#         print(im_name, 'successfully saved!!!')
#         idx = idx + 1
#     return
#
# if __name__ == '__main__':
#     path = r"G:\rssrai2019_semantic_segmentation\dataset\test\GF2_PMS1__20150902_L1A0001015646-MSS1 (2).tif"
#     out_folder =  "./"
#     out_type = ".tiff"
#     tiff_to_image_array(path, out_folder, out_type)
```

如上代码，对 test 文件夹下的的一张原图，先用 tiff 读取，然后使用 opencv 保存下来。我就不贴图了。实际中，可以看到保存下来的图像，和使用 idl 代码转换原图得到图像在电脑上显示出来是一致的。并且再用 opencv 读取保持下来的：

``` python
import cv
image1 = cv2.imread(r"test.tiff", -1)   # 读取刚才保存下来的图。flag=-1 时，8位深度，原通道
image2 = cv2.imread("hou.tiff", -1) 	# idl转换后的图
print((image1==image2).all())
```

打印结果为：True。



---



## 图像预处理

### 上色label转单数值的label

官方给的遥感图像 label 数据都是已经上色了的 RGB 三通道图像，在我们实际训练过程中，我们需要单数值 label 数据，即我们首先需要把上色了 label 图像还原为单数值 label 数据。

1、方法一

我想到笨方法是，把每个颜色赋数值，从 0 到 16。

``` python
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
            elif (label_img[i, j] == [0, 0, 0]).all():	#其他类别
                label[i, j] = 0

    return label
```

以上代码是可行，但是转换需要很长的时间，转换一张都起码需要一个多小时。o(╥﹏╥)o

2、方法二

我看在讨论群里有人提到使用这样的方法，大概的意思是：

> 可以把每个通道值除以 50，然后三个通道乘以三个不同索引值相加可以得到单数值的 label，具体可以自行设置。
>
> 比如每个通道都除以 50，`r*1`、`b*8`、`g*10`、16 个类别的值分别是 0、32、43、65、44、53、77、37、36、4、35、58、59、40、64、82。

3、方法三

还有人先把上色的 label 图像转为单通道灰度图像（RGB 转灰度图公式为 `Grey = 0.299*R + 0.587*G + 0.114*B`），得到如下：

![](https://img-1256179949.cos.ap-shanghai.myqcloud.com/20190627205805.png)

但发现有两个类别转换后灰度值是一样的。（我感觉这方法不行）

### 数据增强？



### 训练





### 后处理

对于预测的时候拼接痕迹明细的问题，看到大家讨论有这么做，大概意思：

> 缩小切割时的步伐，比如我们把切割步伐改为裁剪步长的一半，那么拼接时就会有一般的图像发生重叠，这样做可以尽可能地减少拼接痕迹。





## 补充：遥感影像知识



- [几何校正，正射校正，影像配准，辐射定标，辐射校正，大气校正，地形校正概念详解](<https://blog.csdn.net/lucky51222/article/details/48625991>)
- [遥感影像图中真彩色，假彩色，伪彩色是怎样定义的？为什么要分这些类？ - 知乎](https://www.zhihu.com/question/37163449)



1、遥感图形分辨率？

遥感卫星的飞行高度一般在400km～600km之间，图像分辨率一般从1 km～1m之间。图像分辨率是什么意思呢？可以这样理解，一个像元，代表地面的面积是多少。像元是什么意思呢？像元相当于电视屏幕上的一个点（电视是由若干个点组成的图像画面），相当于计算机显示屏幕上的一个象素，相当于一群举着不同色板拼成画图的人中的一个。

当分辨率为1km时，一个像元代表地面1kmX1km的面积，即1km^2；当分辨率为30m时，一个像元代表地面30m×30m的面积；当分辨率为1m时，也就是说，图像上的一个像元相当于地面1m x 1m的面积，即1m^2。

注：亚米级高分辨率卫星影像指的是能达到 1 米以下分辨率的卫星影像。国内亚米级高分辨卫星影像：高分二号卫星，全色影像分辨率0.8m。



2、高斯噪声、胡椒噪声、盐噪声和椒盐噪声？

**高斯噪声：**

高斯噪声，顾名思义是指服从高斯分布（正态分布）的一类噪声，通常是因为不良照明和高温引起的传感器噪声。通常在RGB图像中，显现比较明显。

**椒盐噪声：**

椒盐噪声，通常是由图像传感器，传输信道，解压处理等产生的黑白相间的亮暗点噪声（椒-黑，盐-白）。通常出现在灰度图中。

——from：<https://blog.csdn.net/firstlai/article/details/77675344>

图像加入椒盐噪声开始，椒盐噪声其实就是**使图像的一些随机的像素为黑色（0）或者白色（255）**：

- **盐噪声**又称**白噪声**，在图像中添加一些随机的白色像素点（255）；
- **胡椒噪声**是在图像中添加一些随机的黑色像素点（0）；
- **盐椒噪声**是在图像中既有白色像素点，又有黑色像素点。



## 代码实现

参考：

- <https://github.com/TachibanaYoshino/Remote-sensing-image-semantic-segmentation>

