import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date


def main():
    data = pd.read_csv("automated_sheets/Lebanon.csv")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    source_url = "https://corona.ministryinfo.gov.lb/"

    req = requests.get(source_url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    cumulative_total = int(soup.find("h1", class_="s-counter3").text)

    if cumulative_total > data["Cumulative total"].max():
        new = pd.DataFrame(
            {
                "Cumulative total": cumulative_total,
                "Date": date.today().strftime("%Y-%m-%d"),
                "Country": "Lebanon",
                "Units": "tests performed",
                "Source URL": source_url,
                "Source label": "Lebanon Ministry of Health",
            }
        )

        df = pd.concat([new, data], sort=False)
        df.to_csv("automated_sheets/Lebanon.csv", index=False)


if __name__ == "__main__":
    main()
