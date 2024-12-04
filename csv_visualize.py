import pandas as pd
from IPython.display import display
import os

def visualize (file_name):
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)

    # 다운로드된 파일 경로
    file_path = os.path.join(current_dir, "../downloads/"+file_name)

    df = pd.read_csv(file_path, encoding="euc-kr")

    # 데이터 테이블 출력
    display(df)

if __name__ == "__main__":
    filename =  "충청북도 제천시_민방위비상급수시설현황_20241202 (1).csv"
    visualize(filename)