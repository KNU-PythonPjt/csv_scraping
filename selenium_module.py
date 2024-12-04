from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
import time
import os

def download_file_from_url(url: str, download_dir: str = "downloads"):
    """
    주어진 URL에서 파일을 다운로드하고 다운로드 완료를 기다립니다.
    
    :param url: 다운로드할 파일의 URL
    :param download_dir: 파일 다운로드 경로 (기본값은 'downloads')
    """
    # 다운로드 경로 설정
    download_dir = os.path.join(os.getcwd(), download_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Chrome 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir, # 다운로드 경로
        "download.prompt_for_download": False,       # 다운로드 시 저장 위치
        "safebrowsing.enabled": True,               # 안전 브라우징 활성화
    }

    chrome_options.add_experimental_option("prefs", prefs)

    # Chrome WebDriver 인스턴스 생성
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    #기존 downloads 폴더 기록
    initial_files = set(os.listdir(download_dir))

    # 페이지 이동
    driver.get(url)

    # 다운로드 버튼 클릭 실행
    try:
        download_button = driver.find_element(By.XPATH, "//a[contains(@onclick, 'fn_fileDataDown')]")
        driver.execute_script("arguments[0].click();", download_button)

        try:
            alert = Alert(driver)
            print(f"Alert detected with text: {alert.text}")
            alert.accept()  # 경고창 수락 (확인 버튼 클릭)
            print("Alert accepted.")
            time.sleep(5)  # 5초 대기

        except NoAlertPresentException:
            print("No alert present.")

    except UnexpectedAlertPresentException as e:
        print(f"Unexpected alert detected: {e.alert_text}")
        Alert(driver).accept()  # 경고창 수락
        print("Unexpected alert accepted.")

    # 다운로드 완료 감지 함수
    def wait_for_downloads(directory, timeout=1000)->str:
        """
        지정된 디렉토리에서 다운로드 완료를 대기.
        :param directory: 다운로드 디렉토리
        :param timeout: 최대 대기 시간
        :return: 다운로드된 파일 이름
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            files = set(os.listdir(directory))
            new_files = files - initial_files

            if new_files:
                for file in new_files:
                    if not file.endswith(".crdownload"):
                        return file

            print("Waiting for download...")
            time.sleep(1)  # 1초 대기
        return ""

    # 다운로드 완료 대기
    downloaded_file = wait_for_downloads(download_dir)
    if downloaded_file:
        print(f"파일 다운로드가 완료되었습니다: {downloaded_file}")
    else:
        print("다운로드가 지정된 시간 내에 완료되지 않았습니다.")
        downloaded_file

    # 브라우저 종료
    driver.quit()
    return downloaded_file

# 예시로 다른 파일에서 URL을 전달
if __name__ == "__main__":
    # url = 'https://www.data.go.kr/data/15083033/fileData.do'  
    url = "https://www.data.go.kr/data/15028160/fileData.do"

    downloaded_file = download_file_from_url(url)
    print(downloaded_file)
