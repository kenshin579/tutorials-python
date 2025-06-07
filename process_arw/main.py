#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import shutil
import sys

import cv2
import nltk
import numpy as np
import rawpy
from PIL import Image


# todo: xmp 생성이 안되는 이슈가 있음
# todo: 사람 얼굴 흐림 판단이 잘 안됨 - 실제로 실행해보기...

# 얼굴 감지 모듈 가져오기
try:
    from face_detection import detect_faces, analyze_face_sharpness
    FACE_DETECTION_AVAILABLE = True
    print("얼굴 감지 기능이 활성화되었습니다.")
except ImportError:
    print("얼굴 감지 모듈을 가져올 수 없습니다. 얼굴 감지 기능 비활성화.")
    FACE_DETECTION_AVAILABLE = False

# XMP 라이브러리 로딩 시도 - 실패해도 프로그램은 계속 실행
XMP_AVAILABLE = False

# OpenCV의 얼굴 감지기를 위한 기본 경로 설정
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

try:
    import libxmp
    from libxmp import XMPFiles, consts
    XMP_AVAILABLE = True
    print("XMP 메타데이터 태그 기능이 활성화되었습니다.")
except Exception as e:
    print(f"XMP 라이브러리를 로드할 수 없습니다: {str(e)}")
    print("XMP 태그 기능이 비활성화됩니다. 태그는 생성되지만 XMP 파일은 만들어지지 않습니다.")
    print("XMP 태그 기능을 사용하려면 다음 명령어로 Exempi 라이브러리를 설치하세요:")
    print("  brew install exempi")
    print("  pip install python-xmp-toolkit")

# NLTK 불용어 데이터 다운로드 시도
try:
    print("NLTK 데이터 다운로드 중...")
    nltk.download('stopwords', quiet=False)
except Exception as e:
    print(f"NLTK 데이터 다운로드 실패: {str(e)}")

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
except ImportError:
    print("transformers 라이브러리를 가져올 수 없습니다. 태그 생성 기능이 비활성화됩니다.")
    BlipProcessor = None
    BlipForConditionalGeneration = None

try:
    from nltk.corpus import stopwords
    # 영어 불용어 목록 로드 시도
    try:
        STOPWORDS = set(stopwords.words('english'))
        # 추가로 제거할 수 있는 일반적인 단어들
        ADDITIONAL_STOPWORDS = {'of', 'with', 'in', 'on', 'at', 'from', 'to', 'for'}
        STOPWORDS.update(ADDITIONAL_STOPWORDS)
    except LookupError:
        print("경고: NLTK stopwords 데이터를 로드할 수 없습니다.")
        # 기본 불용어 목록 제공
        STOPWORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                    'which', 'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than',
                    'such', 'when', 'who', 'how', 'where', 'why', 'of', 'with', 'in', 'on',
                    'at', 'from', 'to', 'for'}
except ImportError:
    print("NLTK 라이브러리를 가져올 수 없습니다. 기본 불용어 목록을 사용합니다.")
    STOPWORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                'which', 'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than',
                'such', 'when', 'who', 'how', 'where', 'why', 'of', 'with', 'in', 'on',
                'at', 'from', 'to', 'for'}


def detect_main_object(image):
    """
    이미지에서 주요 객체 영역을 감지합니다.
    간단한 방법으로 이미지를 격자로 나누고, 각 영역의 Laplacian 분산 값이 가장 높은 영역을
    주요 객체 영역으로 간주합니다.

    Args:
        image: 분석할 이미지

    Returns:
        tuple: 주요 객체 영역의 마스크, 선명도 점수
    """
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) > 2 else image

    # 이미지를 5x5 그리드로 나눕니다
    grid_h, grid_w = 5, 5
    cell_h, cell_w = height // grid_h, width // grid_w

    # 각 셀의 Laplacian 분산 계산
    cell_scores = np.zeros((grid_h, grid_w))
    for i in range(grid_h):
        for j in range(grid_w):
            y1, y2 = i * cell_h, (i + 1) * cell_h
            x1, x2 = j * cell_w, (j + 1) * cell_w

            # 이미지 크기에 맞게 조정
            y2 = min(y2, height)
            x2 = min(x2, width)

            cell = gray[y1:y2, x1:x2]
            lap_var = cv2.Laplacian(cell, cv2.CV_64F).var()
            cell_scores[i, j] = lap_var

    # 중심부 영역에 가중치 부여 (중심에 가까울수록 주요 객체일 가능성 높음)
    center_weight = np.zeros((grid_h, grid_w))
    center_y, center_x = grid_h // 2, grid_w // 2
    for i in range(grid_h):
        for j in range(grid_w):
            # 중심으로부터의 거리 계산
            dist = np.sqrt((i - center_y)**2 + (j - center_x)**2)
            # 거리에 반비례하는 가중치 (거리가 멀수록 가중치 감소)
            center_weight[i, j] = 1 / (1 + dist)

    # 분산 점수와 중심 가중치를 결합
    weighted_scores = cell_scores * center_weight

    # 상위 25% 점수를 가진 셀을 주요 객체 영역으로 간주
    threshold = np.percentile(weighted_scores, 75)
    main_object_cells = weighted_scores >= threshold

    # 주요 객체 마스크 생성
    mask = np.zeros((height, width), dtype=np.uint8)
    for i in range(grid_h):
        for j in range(grid_w):
            if main_object_cells[i, j]:
                y1, y2 = i * cell_h, (i + 1) * cell_h
                x1, x2 = j * cell_w, (j + 1) * cell_w

                # 이미지 크기에 맞게 조정
                y2 = min(y2, height)
                x2 = min(x2, width)

                mask[y1:y2, x1:x2] = 255

    # 주요 객체 영역의 Laplacian 분산 평균 계산
    main_object_score = np.mean(weighted_scores[main_object_cells])

    return mask, main_object_score


def is_main_object_blurry(image, blur_threshold=70.0):
    """
    주요 객체의 흐림 여부를 판단합니다.
    사람이 주요 객체인 경우에는 얼굴이 흔들렸는지를 우선적으로 확인합니다.

    Args:
        image: 분석할 이미지
        blur_threshold: 흐림 판단 임계값

    Returns:
        tuple: (is_blurry, main_object_score) - 흐림 여부와 선명도 점수
    """
    # 얼굴 감지 기능이 사용 가능한 경우
    if FACE_DETECTION_AVAILABLE:
        # 얼굴 감지
        faces = detect_faces(image)

        # 얼굴이 감지된 경우
        if len(faces) > 0:
            print(f"사람 얼굴이 {len(faces)}개 감지되었습니다.")

            # 얼굴 영역의 선명도 분석
            # 얼굴 영역은 중요하므로, 일반 기준보다 더 엄격한 임계값(1.3배) 적용
            face_blur_threshold = blur_threshold * 1.3
            # 함수가 3개의 값을 반환하므로 언패킹 방식 수정
            is_face_blurry, face_score, _ = analyze_face_sharpness(image, faces, face_blur_threshold)

            print(f"얼굴 선명도: {face_score:.2f}, 얼굴 흐림 임계값: {face_blur_threshold:.2f}")

            # 얼굴이 흐릿하면 전체 이미지가 흐릿한 것으로 판단
            if is_face_blurry:
                print("얼굴이 흐릿하여 흔들린 사진으로 판단합니다.")
                return True, face_score
            else:
                print("얼굴이 선명하여 정상 사진으로 판단합니다.")
                return False, face_score

    # 얼굴 감지 불가능하거나 얼굴이 감지되지 않은 경우: 일반적인 흐림 판단
    mask, main_object_score = detect_main_object(image)
    print(f"주요 객체 선명도: {main_object_score:.2f}, 일반 흐림 임계값: {blur_threshold:.2f}")

    # 주요 객체 영역이 임계값보다 낮으면 흐림으로 판단
    is_blurry = main_object_score < blur_threshold

    return is_blurry, main_object_score


def save_xmp_tags(image_path, tags):
    """
    이미지 파일에 대한 XMP 사이드카 파일을 생성하고 태그를 저장합니다.

    Args:
        image_path: 원본 이미지 파일 경로
        tags: 저장할 태그 목록
    """
    if not XMP_AVAILABLE:
        print(f"XMP 라이브러리가 없어 태그를 저장할 수 없습니다: {image_path}")
        return False

    try:
        # XMP 파일 경로 생성 (원본 파일명.xmp)
        xmp_path = f"{image_path}.xmp"

        # XMP 파일 생성
        xmpfile = XMPFiles(file_path=image_path, open_forupdate=True)

        # 기존 XMP 메타데이터 가져오기 또는 새로 생성
        xmp = xmpfile.get_xmp() if xmpfile.get_xmp() else libxmp.XMPMeta()

        # 태그를 DC(Dublin Core) 주제로 저장
        for i, tag in enumerate(tags):
            xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'subject', tag, {})

        # Microsoft Photo 태그 네임스페이스에도 저장
        for i, tag in enumerate(tags):
            xmp.append_array_item(libxmp.consts.XMP_NS_Microsoft, 'LastKeywordXMP', tag, {})

        # Adobe Lightroom 키워드에도 저장
        if tags:
            # 키워드 배열로 함께 저장
            keywords_str = ", ".join(tags)
            xmp.set_property(libxmp.consts.XMP_NS_Lightroom, 'hierarchicalSubject', keywords_str)

        # 변경사항 저장
        if xmpfile.can_put_xmp(xmp):
            xmpfile.put_xmp(xmp)
            xmpfile.close_file()

            # 사이드카 파일로 저장
            xmp.serialize_and_save(xmp_path)
            print(f"XMP 태그가 저장되었습니다: {xmp_path}")
            return True
        else:
            print(f"XMP 태그를 저장할 수 없습니다: {image_path}")
            return False

    except Exception as e:
        print(f"XMP 태그 저장 중 오류 발생: {str(e)}")
        return False


def process_arw(image_path, blur_threshold=100.0, model=None, processor=None):
    """
    ARW 파일을 처리하여 흐림 정도를 측정하고 태그를 생성합니다.

    Args:
        image_path (str): ARW 파일 경로
        blur_threshold (float): 흐림 판단 기준값
        model: 이미지 태깅에 사용할 모델
        processor: 이미지 전처리기

    Returns:
        dict: 처리 결과 (is_blurry, tags, lap_var)
    """
    # 1. ARW → RGB
    try:
        with rawpy.imread(image_path) as raw:
            rgb = raw.postprocess()
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

    # 2. 향상된 흐림 판단 - 주요 객체 중심으로 분석
    is_blurry, main_object_score = is_main_object_blurry(rgb, blur_threshold)

    # 전체 이미지에 대한 Laplacian 분산도 계산 (참고용)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 3. 흔들리지 않은 사진에 대해서만 태그 생성
    tags = []
    if not is_blurry and model is not None and processor is not None:
        try:
            image_pil = Image.fromarray(rgb)
            inputs = processor(image_pil, return_tensors="pt")
            out = model.generate(**inputs)
            caption = processor.decode(out[0], skip_special_tokens=True)

            # 불용어를 제외한 태그 생성
            words = caption.lower().split()
            filtered_words = [word for word in words if word not in STOPWORDS and len(word) > 1]
            tags = filtered_words[:5]  # 최대 5개 태그 추출

            if not tags:  # 필터링 후 태그가 없으면 기본 단어 사용
                tags = words[:5]

            print(f"Caption: '{caption}', Tags: {tags}")

            # 4. 태그를 XMP 파일로 저장
            if tags:
                save_xmp_tags(image_path, tags)

        except Exception as e:
            print(f"Error generating tags for {image_path}: {str(e)}")
    else:
        if is_blurry:
            print(f"{image_path}는 흔들린 이미지로 태그를 생성하지 않습니다.")
        elif model is None:
            print(f"태깅 모델이 로드되지 않아 태그를 생성할 수 없습니다.")

    return {
        "is_blurry": is_blurry,
        "tags": tags,
        "lap_var": laplacian_var,
        "main_object_score": main_object_score
    }


def load_model():
    """
    이미지 태깅을 위한 모델과 프로세서를 로드합니다.
    """
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return model, processor
    except Exception as e:
        print(f"Warning: Failed to load image tagging model: {str(e)}")
        print("Will proceed without tagging functionality.")
        return None, None


def main():
    parser = argparse.ArgumentParser(description="ARW 파일 처리 및 태깅 프로그램")
    parser.add_argument("--src", default="./raw_photos", help="처리할 RAW 파일이 있는 소스 폴더 경로 (기본값: ./raw_photos)")
    parser.add_argument("--threshold", type=float, default=70.0, help="흐림 판단 기준값 (기본값: 70.0)")
    args = parser.parse_args()

    # 소스 폴더 확인
    if not os.path.exists(args.src):
        print(f"Error: Source folder '{args.src}' does not exist.")
        return 1

    # src 폴더 아래에 deleted 폴더 경로 생성
    deleted_folder = os.path.join(args.src, "deleted")

    # 삭제된 이미지를 저장할 폴더 생성
    os.makedirs(deleted_folder, exist_ok=True)
    print(f"흔들린 사진은 {deleted_folder} 폴더로 이동됩니다.")

    # 모델 로드
    model, processor = load_model()

    # 처리할 파일 수 계산
    arw_files = [f for f in os.listdir(args.src) if f.lower().endswith('.arw')]
    total_files = len(arw_files)

    if total_files == 0:
        print(f"No ARW files found in {args.src}")
        return 0

    print(f"Processing {total_files} ARW files...")

    # 파일 처리
    processed = 0
    blurry = 0

    for filename in arw_files:
        full_path = os.path.join(args.src, filename)
        result = process_arw(full_path, args.threshold, model, processor)

        if result is None:
            continue

        processed += 1

        if result["is_blurry"]:
            blurry += 1
            shutil.move(full_path, os.path.join(deleted_folder, filename))
            print(f"🌫️  {filename}: Blurry image moved (Sharpness: {result['lap_var']:.2f})")
        else:
            tags_str = ", ".join(result['tags'])
            print(f"✅ {filename}: {tags_str} (Sharpness: {result['lap_var']:.2f})")

    # 요약 출력
    print(f"\nProcessed {processed} files. Moved {blurry} blurry images to {deleted_folder}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
