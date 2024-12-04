from selenium_module import download_file_from_url
from csv_visualize import visualize

url = "https://www.data.go.kr/data/15028160/fileData.do"

filename = download_file_from_url(url)

visualize(filename)