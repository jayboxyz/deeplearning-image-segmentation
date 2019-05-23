Image_Segmentation
===

基于深度学习的图像分割。



## 语义分割

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
> 	img = cv2.resize(cv2.imread('../../Downloads/cat2.jpg'), (224, 224))
> 
>  mean_pixel = [103.939, 116.779, 123.68]
>  img = img.astype(np.float32, copy=False)
>  for c in range(3):
>  	img[:, :, c] = img[:, :, c] - mean_pixel[c]
>  img = img.transpose((2,0,1))
>  img = np.expand_dims(img, axis=0)
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
