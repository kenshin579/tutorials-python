# 딥러닝 기초 시리즈

PyTorch와 FashionMNIST를 활용한 딥러닝 기초 학습 노트북입니다.

## 노트북 구성

| 노트북 | 주제 |
|---|---|
| `01_image_and_nn_basics.ipynb` | 이미지의 디지털 표현과 신경망 첫걸음 |
| `02_fc_nn_fashionmnist.ipynb` | 완전연결 신경망으로 FashionMNIST 분류 |
| `03_cnn_fashionmnist.ipynb` | CNN으로 이미지 분류 |
| `04_gan_fashionmnist.ipynb` | GAN으로 이미지 생성 |

## 실행 방법

```bash
pip install -e .
jupyter notebook
```

## 데이터셋

[FashionMNIST](https://github.com/zalandoresearch/fashion-mnist) - 28x28 그레이스케일 패션 아이템 이미지 (10 클래스)

| 레이블 | 클래스 |
|---|---|
| 0 | T-shirt/top |
| 1 | Trouser |
| 2 | Pullover |
| 3 | Dress |
| 4 | Coat |
| 5 | Sandal |
| 6 | Shirt |
| 7 | Sneaker |
| 8 | Bag |
| 9 | Ankle boot |
