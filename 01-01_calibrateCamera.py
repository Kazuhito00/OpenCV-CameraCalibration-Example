#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import cv2 as cv
import numpy as np


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--file", type=str, default=None)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=360)

    parser.add_argument("--square_len", type=float, default=23.0)
    parser.add_argument("--grid_size", type=str, default="10,7")

    parser.add_argument("--k_filename", type=str, default="K.csv")
    parser.add_argument("--d_filename", type=str, default="d.csv")

    parser.add_argument("--interval_time", type=int, default=500)
    parser.add_argument('--use_autoappend', action='store_true')

    args = parser.parse_args()

    return args


def main():
    # コマンドライン引数
    args = get_args()

    cap_device = args.device
    filepath = args.file
    cap_width = args.width
    cap_height = args.height

    # カメラ準備
    cap = None
    if filepath is None:
        cap = cv.VideoCapture(cap_device, cv.CAP_DSHOW)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    else:
        cap = cv.VideoCapture(filepath)

    square_side_length = args.square_len  # チェスボード内の正方形の1辺のサイズ(mm)
    grid_intersection_size = eval(args.grid_size)  # チェスボード内の格子数

    k_filename = args.k_filename
    d_filename = args.d_filename

    interval_time = args.interval_time
    use_autoappend = args.use_autoappend
    if use_autoappend is False:
        interval_time = 10

    # チェスボードコーナー検出情報 保持用変数
    pattern_points = np.zeros((np.prod(grid_intersection_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(grid_intersection_size).T.reshape(-1, 2)
    pattern_points *= square_side_length
    object_points = []
    image_points = []

    camera_mat, dist_coef = [], []

    capture_count = 0
    while (True):
        ret, frame = cap.read()

        # チェスボードのコーナーを検出
        found, corner = cv.findChessboardCorners(frame, grid_intersection_size)

        if found:
            print('findChessboardCorners() : True')
            cv.drawChessboardCorners(frame, grid_intersection_size, corner,
                                     found)
        else:
            print('findChessboardCorners() : False')

        cv.putText(frame,
                   "Enter:Capture Chessboard(" + str(capture_count) + ")",
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv.putText(frame, "ESC :Completes Calibration Photographing", (10, 55),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
        cv.imshow('original', frame)

        key = cv.waitKey(interval_time) & 0xFF
        if ((use_autoappend is True) and found) or (
            (use_autoappend is False and key == 13) and found):  # Enter
            # チェスボードコーナー検出情報を追加
            image_points.append(corner)
            object_points.append(pattern_points)
            capture_count += 1
        if key == 27:  # ESC
            cap.release()
            cv.destroyAllWindows()
            break

    if len(image_points) > 0:
        # カメラ内部パラメータを計算
        print('calibrateCamera()')
        rms, K, d, r, t = cv.calibrateCamera(object_points, image_points,
                                             (frame.shape[1], frame.shape[0]),
                                             None, None)
        print("RMS = " + str(rms))
        print("K = \n", K)
        print("d = " + str(d.ravel()))
        np.savetxt(k_filename, K, delimiter=',', fmt="%0.14f")  # 半径方向の歪み係数の保存
        np.savetxt(d_filename, d, delimiter=',', fmt="%0.14f")  # 円周方向の歪み係数の保存

        camera_mat = K
        dist_coef = d

        # 再投影誤差による評価
        mean_error = 0
        for i in range(len(object_points)):
            image_points2, _ = cv.projectPoints(object_points[i], r[i], t[i],
                                                camera_mat, dist_coef)
            error = cv.norm(image_points[i], image_points2,
                            cv.NORM_L2) / len(image_points2)
            mean_error += error
        print("total error: " +
              str(mean_error / len(object_points)))  # 0に近い値が望ましい
    else:
        print("findChessboardCorners() not be successful once")

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
