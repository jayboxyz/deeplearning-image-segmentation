# Image_Segmentation

基于深度学习的图像分割。



## 语义分割模型

- FCN
- DeconvNet
- SegNet
- UNet
- PSPNet
- RefineNet
- GCN
- DeepLab（v1&v2&v3&v3+）
- PAN
- Auto-DeepLab
- NAS
- …

## 模型架构、代码复现等

### 语义分割论文

- [Semantic Segmentation | Zhang Bin's Blog](<https://zhangbin0917.github.io/2018/09/18/Semantic-Segmentation/>)
- [Segmentation - handong1587](<https://handong1587.github.io/deep_learning/2015/10/09/segmentation.html>)
- [语义分割 - Semantic Segmentation Papers - AIUAI](<https://www.aiuai.cn/aifarm62.html>)

### 模型和复现

- [mrgloom/awesome-semantic-segmentation](<https://github.com/mrgloom/awesome-semantic-segmentation>)
- [guanfuchen/semseg](<https://github.com/guanfuchen/semseg>) - 常用的语义分割架构结构综述以及代码复现
- [GeorgeSeif/Semantic-Segmentation-Suite](<https://github.com/GeorgeSeif/Semantic-Segmentation-Suite>) - Semantic Segmentation Suite in TensorFlow. Implement, train, and test new Semantic Segmentation models easily!
- [guanfuchen/DeepNetModel](<https://github.com/guanfuchen/DeepNetModel>) - 记录每一个常用的深度模型结构的特点（图和代码）
- [handong1587.github.io/2015-10-09-segmentation.md](<https://github.com/handong1587/handong1587.github.io/blob/master/_posts/deep_learning/2015-10-09-segmentation.md>)



### 计算机视觉论文

- [amusi/CVPR2019-Code: CVPR 2019 Paper with Code](<https://github.com/amusi/CVPR2019-Code>)
- [zziz/pwc: Papers with code. Sorted by stars](<https://github.com/zziz/pwc#2017>)
- [amusi/daily-paper-computer-vision](<https://github.com/amusi/daily-paper-computer-vision>)



## 代码实践

常看到代码中定义：

``` python
R = 103.939
G = 116.779
B = 123.68
```

什么意思？请看这里一个回答：https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3#gistcomment-1616734

> Also, there is no normalization done in the gist above. If you want accurate results, you better do those steps to any input image:
>
> ``` python
>     img = cv2.resize(cv2.imread('../../Downloads/cat2.jpg'), (224, 224))
> 
>      mean_pixel = [103.939, 116.779, 123.68]
>      img = img.astype(np.float32, copy=False)
>      for c in range(3):
>          img[:, :, c] = img[:, :, c] - mean_pixel[c]
>      img = img.transpose((2,0,1))
>      img = np.expand_dims(img, axis=0)
> ```
>
> The mean pixel values are taken from the VGG authors, which are the values computed from the training dataset.



## Update

- FDNet：学习全密集神经网络进行图像语义分割

  > 《Learning Fully Dense Neural Networks for Image Semantic Segmentation》(AAAI 2019)
  >
  > Date：2019  |  Author：香港科技大学&微软亚洲研究院
  >
  > arXiv：<https://128.84.21.199/abs/1905.08929>

- 基于MobileNetV3的DeepLab V3+语义分割

  > Mobile Deeplab-V3+ model for Segmentation
  >
  > This project is used for deploying people segmentation model to mobile device and learning. The people segmentation android project is here. The model is...
  >
  > arXiv：

- 遥感语义图像的边界损失

  > 《Boundary Loss for Remote Sensing Imagery Semantic Segmentation》
  >
  > Date:20190521  |  Author: Aeronet 
  >
  > arXiv：<https://arxiv.org/abs/1905.07852>

- HRNet：（告别低分辨率网络，微软提出高分辨率深度神经网络HRNet）

  > 《Deep High-Resolution Representation Learning for Human Pose Estimation》
  >
  > arXiv：<https://arxiv.org/abs/1902.09212>
  >
  > [1] Ke Sun, Bin Xiao, Dong Liu, Jingdong Wang: Deep High-Resolution Representation Learning for Human Pose Estimation. CVPR 2019
  >
  > [2] https://github.com/leoxiaobin/deep-high-resolution-net.pytorch
  >
  > [3] https://github.com/HRNet
  >
  > ——from：[CVPR 2019 | 告别低分辨率网络，微软提出高分辨率深度神经网络HRNet](https://mp.weixin.qq.com/s/R9eG3FvvBcl-bGgJEF1uoA)
  
  > 《Deep High-Resolution Representation Learning for Human Pose Estimation》的原作者不仅把这种高分辨率网络结构用于姿态估计，也在尝试用于其他方向。
  >
  > 不久前，作者在新论文《High-Resolution Representations for Labeling Pixels and Regions》中对网络结构进行了v2版本升级，给出了更多实验结果，更加验证了该网络结构的价值！
  >
  > 在计算机视觉目前最热门应用领域语义分割、目标检测、人脸特征点定位中，换用高分辨率网络结构的算法都获得了显著的精度提升！
  >
  > arXiv：<https://arxiv.org/abs/1904.04514>
  
  