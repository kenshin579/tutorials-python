#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
얼굴 감지 및 선명도 분석을 위한 유틸리티 모듈
"""

import cv2
import numpy as np

def detect_faces(image, cascade_path=None):
    """
    이미지에서 얼굴을 감지합니다.

    Args:
        image: 분석할 RGB 이미지
        cascade_path: Haar 캐스케이드 XML 파일 경로 (기본값: OpenCV 내장 경로)

    Returns:
        list: 감지된 얼굴의 좌표 (x, y, w, h) 리스트
    """
    try:
        # 얼굴 감지기 로드
        if cascade_path is None:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

        face_cascade = cv2.CascadeClassifier(cascade_path)

        # 이미지가 RGB 형식이면 그레이스케일로 변환
        if len(image.shape) > 2:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image

        # 얼굴 감지 수행
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) > 0:
            print(f"{len(faces)}개의 얼굴이 감지되었습니다.")
        return faces

    except Exception as e:
        print(f"얼굴 감지 중 오류 발생: {str(e)}")
        return []


def analyze_face_sharpness(image, faces, face_blur_threshold=100.0):
    """
    감지된 얼굴 영역의 선명도를 분석합니다.

    Args:
        image: 원본 이미지
        faces: 감지된 얼굴의 좌표 리스트 [(x, y, w, h), ...]
        face_blur_threshold: 얼굴 흐림 판단 임계값

    Returns:
        tuple: (얼굴_흐림_여부, 얼굴_선명도_점수, 각_얼굴_점수_목록)
    """
    if len(faces) == 0:
        return False, 0.0, []

    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    face_sharpness_scores = []

    # 각 얼굴 영역의 라플라시안 분산 계산
    for (x, y, w, h) in faces:
        # 얼굴 영역 추출
        face_roi = gray[y:y+h, x:x+w]

        # 얼굴 영역의 라플라시안 분산 계산 (선명도 점수)
        lap_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        face_sharpness_scores.append(lap_var)
        print(f"얼굴 영역 선명도: {lap_var:.2f}")

    # 모든 얼굴 영역의 평균 선명도 점수
    avg_face_sharpness = np.mean(face_sharpness_scores) if face_sharpness_scores else 0.0

    # 얼굴 선명도가 기준보다 낮으면 흐림으로 판단
    is_face_blurry = avg_face_sharpness < face_blur_threshold

    return is_face_blurry, avg_face_sharpness, face_sharpness_scores


def is_face_image_blurry(image, general_blur_threshold=70.0, face_blur_threshold=100.0):
    """
    이미지에 얼굴이 있는지 확인하고, 있다면 얼굴의 흐림 여부를 판단합니다.
    없다면 일반적인 흐림 판단을 수행합니다.

    Args:
        image: 분석할 이미지
        general_blur_threshold: 일반 흐림 판단 임계값
        face_blur_threshold: 얼굴 흐림 판단 임계값

    Returns:
        tuple: (is_blurry, sharpness_score, has_faces, face_score)
    """
    # 얼굴 감지
    faces = detect_faces(image)
    has_faces = len(faces) > 0

    # 일반적인 흐림 판단
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) > 2 else image
    general_sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

    if has_faces:
        # 얼굴이 감지된 경우, 얼굴 영역의 선명도 분석
        is_face_blurry, face_score, _ = analyze_face_sharpness(image, faces, face_blur_threshold)

        # 얼굴이 흐릿하면 전체 이미지가 흐릿한 것으로 판단
        return is_face_blurry, general_sharpness, has_faces, face_score
    else:
        # 얼굴이 없는 경우, 일반적인 흐림 판단
        is_blurry = general_sharpness < general_blur_threshold
        return is_blurry, general_sharpness, has_faces, 0.0
