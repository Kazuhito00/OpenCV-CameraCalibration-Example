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

    parser.add_argument("--k_new_param", type=float, default=1.0)

    parser.add_argument("--k_filename", type=str, default="K.csv")
    parser.add_argument("--d_filename", type=str, default="d.csv")

    args = parser.parse_args()

    return args


def main():
    # コマンドライン引数
    args = get_args()

    cap_device = args.device
    filepath = args.file
    cap_width = args.width
    cap_height = args.height

    k_new_param = args.k_new_param

    k_filename = args.k_filename
    d_filename = args.d_filename

    # カメラ準備
    cap = None
    if filepath is None:
        cap = cv.VideoCapture(cap_device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    else:
        cap = cv.VideoCapture(filepath)

    # キャリブレーションデータの読み込み
    camera_mat = np.loadtxt(k_filename, delimiter=',')
    dist_coef = np.loadtxt(d_filename, delimiter=',')

    new_camera_mat = camera_mat.copy()
    new_camera_mat[(0, 1), (0, 1)] = k_new_param * new_camera_mat[(0, 1),
                                                                  (0, 1)]

    while (True):
        ret, frame = cap.read()
        undistort_image = cv.undistort(
            frame,
            camera_mat,
            dist_coef,
            new_camera_mat,
        )

        cv.imshow('original', frame)
        cv.imshow('undistort', undistort_image)

        key = cv.waitKey(1) & 0xFF
        if key == 27:  # ESC
            cap.release()
            cv.destroyAllWindows()
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
