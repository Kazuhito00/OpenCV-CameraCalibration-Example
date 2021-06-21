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

    parser.add_argument("--k_new_param", type=float, default=0.5)

    parser.add_argument("--k_filename", type=str, default="K_omni.csv")
    parser.add_argument("--d_filename", type=str, default="d_omni.csv")
    parser.add_argument("--xi_filename", type=str, default="xi_omni.csv")

    parser.add_argument(
        "--flag",
        type=int,
        help=
        '1:RECTIFY_PERSPECTIVE 2:RECTIFY_CYLINDRICAL 3:RECTIFY_LONGLATI 4:RECTIFY_STEREOGRAPHIC',
        default=1)

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
    xi_filename = args.xi_filename

    flag = args.flag

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
    xi = np.loadtxt(xi_filename, delimiter=',')

    new_camera_mat = camera_mat.copy()
    new_camera_mat[(0, 1), (0, 1)] = k_new_param * new_camera_mat[(0, 1),
                                                                  (0, 1)]

    # 参考：https://docs.opencv.org/master/dd/d12/tutorial_omnidir_calib_main.html
    if flag == 1:
        flags = cv.omnidir.RECTIFY_PERSPECTIVE
    elif flag == 2:
        flags = cv.omnidir.RECTIFY_CYLINDRICAL
    elif flag == 3:
        flags = cv.omnidir.RECTIFY_LONGLATI
    elif flag == 4:
        flags = cv.omnidir.RECTIFY_STEREOGRAPHIC
    else:
        flags = cv.omnidir.RECTIFY_PERSPECTIVE

    while (True):
        ret, frame = cap.read()
        unconstraint_image = cv.omnidir.undistortImage(
            frame,
            camera_mat,
            D=dist_coef,
            xi=xi,
            Knew=new_camera_mat,
            flags=flags,
        )

        cv.imshow('original', frame)
        cv.imshow('unConstraint', unconstraint_image)

        key = cv.waitKey(1) & 0xFF
        if key == 27:  # ESC
            cap.release()
            cv.destroyAllWindows()
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
