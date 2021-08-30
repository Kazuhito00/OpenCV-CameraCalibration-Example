# OpenCV-CameraCalibration-Example
https://user-images.githubusercontent.com/37477845/122794701-8086b900-d2f7-11eb-8651-ce4e300e8a83.mp4

OpenCVを用いたカメラキャリブレーションのサンプルです<br>
2021/06/21時点でPython実装のある以下3種類について用意しています。
* 通常カメラ向け
* 魚眼レンズ向け(fisheyeモジュール)
* 全方位カメラ向け(omnidirモジュール)<br>
全方位カメラは以下のような構造のカメラを想定しています。<br>
<img src="https://user-images.githubusercontent.com/37477845/122723516-067e1200-d2ae-11eb-8ce4-6ca891111160.png" width="50%"><br>
画像はWikipediaの[Omnidirectional (360-degree) camera](https://en.wikipedia.org/wiki/Omnidirectional_(360-degree)_camera)から引用<br>



# Requirement 
* opencv-python 4.5.2.54 or later
* opencv-contrib-python 4.5.2.54 or later ※omnidirモジュールを使用する場合のみ

# Calibration Pattern
サンプルでは以下の7×10のチェスボード型のキャリブレーションパターンを使用します。
* http://opencv.jp/sample/pics/chesspattern_7x10.pdf

他の行列数のキャリブレーションパターンを使用したい場合は、以下を参照して作成or入手してください。
* https://docs.opencv.org/master/da/d0d/tutorial_camera_calibration_pattern.html
* https://github.com/opencv/opencv/blob/master/doc/pattern.png

また、以下のようなサークル型のパターンやセクターベース型のパターンのサンプルは用意していません。
* https://github.com/opencv/opencv/blob/master/doc/acircles_pattern.png
* https://docs.opencv.org/4.5.2/checkerboard_radon.png
  
# Usage
<img src="https://user-images.githubusercontent.com/37477845/122718897-6d98c800-d2a8-11eb-8d18-18cb6d2f0468.png" width="90%">
calibrateCameraのサンプルでキャリブレーションパラメータをcsvに保存し、<br>
undistortのサンプルで歪み補正を実施してください。

#### 01.calibrateCamera
```bash
python 01-01_calibrateCamera.py
python 02-01_fisheyeCalibrateCamera.py
python 03-01_omnidirCalibrateCamera.py
```
キャリブレーションパターン検出時にEnterを押すことで撮影します。<Br>
ESCを押すことでプログラムを終了し、キャリブレーションパラメータを保存します。<Br>

実行時には、以下のオプションが指定可能です。
<details>
<summary>オプション指定</summary>
   
* --device<br>
カメラデバイス番号の指定<br>
デフォルト：
    * 01-01_calibrateCamera：0
    * 02-01_fisheyeCalibrateCamera.py：0
    * 03-01_omnidirCalibrateCamera.py：0
* --file<br>
動画ファイル名の指定 ※指定時はカメラデバイスより優先し動画を読み込む<br>
デフォルト：
    * 01-01_calibrateCamera：None
    * 02-01_fisheyeCalibrateCamera.py：None
    * 03-01_omnidirCalibrateCamera.py：None
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：
    * 01-01_calibrateCamera：640
    * 02-01_fisheyeCalibrateCamera.py：640
    * 03-01_omnidirCalibrateCamera.py：640
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：
    * 01-01_calibrateCamera：360
    * 02-01_fisheyeCalibrateCamera.py：360
    * 03-01_omnidirCalibrateCamera.py：360
* --square_len<br>
キャリブレーションパターン(チェスボード)の1辺の長さ(mm)<br>
デフォルト：
    * 01-01_calibrateCamera：23.0
    * 02-01_fisheyeCalibrateCamera.py：23.0
    * 03-01_omnidirCalibrateCamera.py：23.0
* --grid_size<br>
キャリブレーションパターン(チェスボード)の行列数(カンマ区切り指定)<br>
デフォルト：
    * 01-01_calibrateCamera：10,7
    * 02-01_fisheyeCalibrateCamera.py：10,7
    * 03-01_omnidirCalibrateCamera.py：10,7
* --k_filename<br>
半径方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：
    * 01-01_calibrateCamera：K.csv
    * 02-01_fisheyeCalibrateCamera.py：K_fisheye.csv
    * 03-01_omnidirCalibrateCamera.py：K_omni.csv
* --d_filename<br>
円周方向の歪み係数の保存ファイル名(csv)<br>
デフォルト：
    * 01-01_calibrateCamera：d.csv
    * 02-01_fisheyeCalibrateCamera.py：d_fisheye.csv
    * 03-01_omnidirCalibrateCamera.py：d_omni.csv
* --xi_filename<br>
Mei'sモデルパラメータxiの保存ファイル名(csv)<br>
デフォルト：
    * 03-01_omnidirCalibrateCamera.py：xi_omni.csv
* --use_autoappend<br>
キャリブレーションパターン検出時に自動で撮影するか否か(指定しない場合はEnterで明示的に撮影)<br>
デフォルト：
    * 01-01_calibrateCamera：指定なし
    * 02-01_fisheyeCalibrateCamera.py：指定なし
    * 03-01_omnidirCalibrateCamera.py：指定なし
* --interval_time<br>
use_autoappend指定時の撮影間隔(ms)<br>
デフォルト：
    * 01-01_calibrateCamera：500
    * 02-01_fisheyeCalibrateCamera.py：500
    * 03-01_omnidirCalibrateCamera.py：500
</details>
  
#### 02.undistort
```bash
python 01-02_undistort.py
python 02-02_fisheyeUndistort.py
python 03-02_omnidirUndistort.py
```

実行時には、以下のオプションが指定可能です。
<details>
<summary>オプション指定</summary>
   
* --device<br>
カメラデバイス番号の指定<br>
デフォルト：
    * 01-01_calibrateCamera：0
    * 02-01_fisheyeCalibrateCamera.py：0
    * 03-01_omnidirCalibrateCamera.py：0
* --file<br>
動画ファイル名の指定 ※指定時はカメラデバイスより優先し動画を読み込む<br>
デフォルト：
    * 01-01_calibrateCamera：None
    * 02-01_fisheyeCalibrateCamera.py：None
    * 03-01_omnidirCalibrateCamera.py：None
* --width<br>
カメラキャプチャ時の横幅<br>
デフォルト：
    * 01-01_calibrateCamera：640
    * 02-01_fisheyeCalibrateCamera.py：640
    * 03-01_omnidirCalibrateCamera.py：640
* --height<br>
カメラキャプチャ時の縦幅<br>
デフォルト：
    * 01-01_calibrateCamera：360
    * 02-01_fisheyeCalibrateCamera.py：360
    * 03-01_omnidirCalibrateCamera.py：360
* --k_filename<br>
半径方向の歪み係数の読み込みファイル名(csv)<br>
デフォルト：
    * 01-01_calibrateCamera：K.csv
    * 02-01_fisheyeCalibrateCamera.py：K_fisheye.csv
    * 03-01_omnidirCalibrateCamera.py：K_omni.csv
* --d_filename<br>
円周方向の歪み係数の読み込みファイル名(csv)<br>
デフォルト：
    * 01-01_calibrateCamera：d.csv
    * 02-01_fisheyeCalibrateCamera.py：d_fisheye.csv
    * 03-01_omnidirCalibrateCamera.py：d_omni.csv
* --xi_filename<br>
Mei'sモデルパラメータxiの読み込みファイル名(csv)<br>
デフォルト：
    * 03-01_omnidirCalibrateCamera.py：xi_omni.csv
* --k_new_param<br>
Knewパラメータ指定時のスケール<br>
デフォルト：
    * 01-01_calibrateCamera：1.0
    * 02-01_fisheyeCalibrateCamera.py：0.9
    * 03-01_omnidirCalibrateCamera.py：0.5
</details>
  
# Reference
* [OpenCV Camera Calibration Tutorial](https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html)
* [OpenCV Camera Calibration and 3D Reconstruction](https://docs.opencv.org/master/d9/d0c/group__calib3d.html)
* [OpenCV Fisheye camera model](https://docs.opencv.org/master/db/d58/group__calib3d__fisheye.html)
* [OpenCV Omnidirectional Camera Calibration](https://docs.opencv.org/master/dd/d12/tutorial_omnidir_calib_main.html)

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
OpenCV-CameraCalibration-Example is under [Apache-2.0 License](LICENSE).
