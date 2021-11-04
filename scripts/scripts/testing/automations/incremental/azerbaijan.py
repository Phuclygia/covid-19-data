import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date


def main():
    data = pd.read_csv("automated_sheets/Azerbaijan.csv")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    source_url = "https://koronavirusinfo.az/az/page/statistika/azerbaycanda-cari-veziyyet"

    req = requests.get(source_url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    cumulative_total = int(
        soup.find_all("div", class_="gray_little_statistic")[5].find("strong").text.replace(",", "")
    )

    if cumulative_total > data["Cumulative total"].max():
        new = pd.DataFrame(
            {
                "Cumulative total": cumulative_total,
                "Date": date.today().strftime("%Y-%m-%d"),
                "Country": "Azerbaijan",
                "Units": "tests performed",
                "Source URL": source_url,
                "Source label": "Cabinet of Ministers of Azerbaijan",
            }
        )

        df = pd.concat([new, data], sort=False)
        df.to_csv("automated_sheets/Azerbaijan.csv", index=False)


if __name__ == "__main__":
    main()
