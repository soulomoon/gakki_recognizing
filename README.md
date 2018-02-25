# 获取并且识别gakki老婆的图片(Just for fun)

## Requirement
* python 3.6
* pipenv

## 使用方式
##### 下载repo
* `pip install https://github.com/soulomoon/gakki_recognizing.git`
* `cd gakki_recognizing`
##### 安装依赖
* `pip install pipenv`
* `pipenv install`
##### 爬取图片
* `pipenv run python scrap.py`
##### 识别图片并且归类
* `pipenv run python recognize.py`

## 爬取gakki图片

### selenium
由于百度搜图使用了瀑布流的图片显示方式，需要滚动浏览滑轮到才能加载图片，  
所以需要能加载js代码才能加载到所有图片，这里选用简单的selenium控制firefox。

### 图片文件夹
爬取gakki图片后存放在data/img


## 人脸识别gakki

### 识别引擎
非常简单并且已经训练好模型的线程的库 [ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)

### 为什么要gakki
老婆好

### 识别后的处理逻辑
结果显示在data文件夹里面  
识别后将图片的symlinks到对应的文件夹
