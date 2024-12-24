import os
import sys

sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

SCRAP_INITIAL_URL: str = os.getenv('SCRAP_INITIAL_URL')
SCRAP_LOGIN_URL: str = os.getenv('SCRAP_LOGIN_URL')
SCRAP_LOGIN_USER_ID: str = os.getenv('SCRAP_LOGIN_USER_ID')
SCRAP_LOGIN_USER_PW: str = os.getenv('SCRAP_LOGIN_USER_PW')

SCRAP_DETAIL_SAMPLE_URL: str = os.getenv('SCRAP_DETAIL_SAMPLE_URL')
SCRAP_DETAIL_CORP_FIELD_XPATH: str = os.getenv('SCRAP_DETAIL_CORP_INFO_XPATH')
SCRAP_DETAIL_INVESTMENT_SELECTOR: str = os.getenv('SCRAP_DETAIL_INVESTMENT_SELECTOR')

from selenium.webdriver.chrome.options import Options

GUI_BASE_X: int = int(os.getenv('GUI_BASE_X'))
GUI_BASE_Y: int = int(os.getenv('GUI_BASE_Y'))
GUI_BASE_WIDTH: int = int(os.getenv('GUI_BASE_WIDTH'))
GUI_BASE_HEIGHT: int = int(os.getenv('GUI_BASE_HEIGHT'))

driver_options = Options()
driver_options.add_argument(f"--window-position={GUI_BASE_X},{GUI_BASE_Y}")
driver_options.add_argument(f"--window-size={GUI_BASE_WIDTH},{GUI_BASE_HEIGHT}")
