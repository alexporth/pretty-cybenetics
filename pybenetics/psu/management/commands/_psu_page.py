import datetime
import re
import urllib.parse

from bs4 import BeautifulSoup, Tag as Bs4Tag, ResultSet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.models import Brand, EfficiencyCertification, NoiseCertification
from psu.models import PsuEntry, Voltage, Tag, FormFactor, Wattage


class PsuPage:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        + "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    base_url = "https://www.cybenetics.com/"
    tag_voltage_dictionary = {
        1: {"tag": "ETA & LAMBDA", "voltage": 115},
        2: {"tag": "ETA & LAMBDA", "voltage": 230},
        3: {"tag": "ETA Redundant", "voltage": 230},
        4: {"tag": "ATX V3.0", "voltage": 115},
        5: {"tag": "ATX V3.0", "voltage": 230},
        6: {"tag": "ATX V3.1", "voltage": 115},
        7: {"tag": "ATX V3.1", "voltage": 230},
    }
    code_capture = re.compile(r"load\(\"(.+?)\"")

    def __init__(self, brand: str, url: str):
        self.brand, created = Brand.objects.get_or_create(name=brand)
        self.initial_url = url

    def build_url_list(self):
        split_initial_url = self.initial_url.split(",")
        brand_number = split_initial_url[-1]
        psu_url_list = []
        for tab_number in self.tag_voltage_dictionary:
            psu_url_list.append(
                (
                    tab_number,
                    f"https://www.cybenetics.com/index.php?option=database&params={tab_number},0,{brand_number}",
                )
            )
        return psu_url_list

    def parse(self):
        driver = webdriver.Chrome()
        for tab_number, url in self.build_url_list():
            driver.get(url)
            try:
                _ = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "mytable.sub"))  # This is a dummy element
                )
                soup = BeautifulSoup(driver.page_source, "html.parser")
                base_table = soup.find("table", class_="mytable")
                table = base_table.find("table")
                for table_parts in table.find_all("tbody"):
                    rows = table_parts.find_all("tr")
                    brand_name = self.extract_brand(rows[0])
                    if brand_name != self.brand.name:
                        raise ValueError(f"Brands {brand_name} and {self.brand.name} do not match")
                    for data_row in rows[3:]:
                        data = data_row.find_all("td")
                        model_name = data[0].text
                        if model_name == "No records found":
                            break
                        voltage_tag_entry = self.tag_voltage_dictionary[tab_number]
                        voltage, created_v = Voltage.objects.get_or_create(value=voltage_tag_entry["voltage"])
                        tag, created_t = Tag.objects.get_or_create(name=voltage_tag_entry["tag"])
                        try:
                            psu_entry = PsuEntry.objects.get(brand=self.brand, name=model_name, voltage=voltage)
                            psu_entry.tags.add(tag)
                            continue
                        except PsuEntry.DoesNotExist:
                            print(f"Creating entry for {brand_name} - {model_name} - {voltage.value}")
                        form_factor, created_f = FormFactor.objects.get_or_create(name=data[1].text)
                        wattage, created_w = Wattage.objects.get_or_create(value=data[2].text)
                        average_efficiency = float(data[3].text)
                        average_efficiency_5vsb = float(data[4].text)
                        vampire_power = float(data[5].text)
                        average_power_factor = float(data[6].text)
                        ano = data[7].text
                        average_noise_output = None if ano == "-" else float(ano)
                        model_efficiency_rating = data[8].text
                        efficiency_rating = None
                        if model_efficiency_rating:
                            efficiency_rating = EfficiencyCertification.objects.get(name=model_efficiency_rating)
                        model_noise_rating = data[9].text
                        noise_rating = None
                        if model_noise_rating:
                            noise_rating = NoiseCertification.objects.get(name=model_noise_rating)
                        date_text = data[10].text
                        if date_text.split("-")[-1] == "00":
                            date_text = date_text.replace("00", "01")
                        date = datetime.date.fromisoformat(date_text)
                        short_report, normal_report = self.get_reports(data)
                        psu_entry = PsuEntry.objects.create(
                            brand=self.brand,
                            name=model_name,
                            voltage=voltage,
                            form_factor=form_factor,
                            wattage=wattage,
                            average_efficiency=average_efficiency,
                            average_efficiency_5vsb=average_efficiency_5vsb,
                            vampire_power=vampire_power,
                            average_power_factor=average_power_factor,
                            average_noise_output=average_noise_output,
                            efficiency_rating=efficiency_rating,
                            noise_rating=noise_rating,
                            date=date,
                            report_short=short_report,
                            report=normal_report,
                        )
                        psu_entry.tags.add(tag)
            finally:
                pass
        driver.quit()

    def get_reports(self, data: ResultSet):
        def get_report(report_link):
            s_report = None
            n_report = None
            if report_link:
                report_url = urllib.parse.urljoin(self.base_url, report_link.get("href"))
                if report_url == self.base_url:
                    return s_report, n_report
                if report_link.text == "SHORT":
                    s_report = report_url
                else:
                    n_report = report_url
            return s_report, n_report

        sr_11, nr_11 = get_report(data[11].find("a"))
        sr_12, nr_12 = get_report(data[12].find("a"))
        short_report = sr_11 if sr_11 else sr_12
        normal_report = nr_11 if nr_11 else nr_12
        return short_report, normal_report

    @staticmethod
    def extract_brand(brand_row: Bs4Tag):
        brand_headers = brand_row.find_all("th")
        brand_header = brand_headers[0]
        return brand_header.text
