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

    parser.add_argument("--k_filename", type=str, default="K_fisheye.csv")
    parser.add_argument("--d_filename", type=str, default="d_fisheye.csv")

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
        cap = cv.VideoCapture(cap_device)
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
    pattern_points = np.zeros((1, np.prod(grid_intersection_size), 3),
                              np.float32)
    pattern_points[0, :, :2] = np.indices(grid_intersection_size).T.reshape(
        -1, 2)
    pattern_points *= square_side_length
    object_points = []
    image_points = []

    subpix_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30,
                       0.1)

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
            gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.cornerSubPix(gray_image, corner, (3, 3), (-1, -1),
                            subpix_criteria)
            image_points.append(corner)
            object_points.append(pattern_points)
            capture_count += 1
        if key == 27:  # ESC
            cap.release()
            cv.destroyAllWindows()
            break

    if len(image_points) > 0:
        # カメラ内部パラメータを計算
        print('fisheye.calibrate()')

        # calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv.fisheye.CALIB_CHECK_COND + cv.fisheye.CALIB_FIX_SKEW
        calibration_flags = cv.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv.fisheye.CALIB_FIX_SKEW

        K = np.zeros((3, 3))
        d = np.zeros((4, 1))
        rvecs = [
            np.zeros((1, 1, 3), dtype=np.float64)
            for i in range(len(image_points))
        ]
        tvecs = [
            np.zeros((1, 1, 3), dtype=np.float64)
            for i in range(len(image_points))
        ]
        rms, K, d, r, t = \
            cv.fisheye.calibrate(
                object_points,
                image_points,
                gray_image.shape[::-1],
                K,
                d,
                rvecs,
                tvecs,
                calibration_flags,
                (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
            )
        print("RMS = " + str(rms))
        print("Shape=" + str((frame.shape[:2])[::-1]))
        print("K = \n", K)
        print("d = " + str(d.ravel()))
        np.savetxt(k_filename, K, delimiter=',', fmt="%0.14f")  # 半径方向の歪み係数の保存
        np.savetxt(d_filename, d, delimiter=',', fmt="%0.14f")  # 円周方向の歪み係数の保存
    else:
        print("findChessboardCorners() not be successful once")

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
