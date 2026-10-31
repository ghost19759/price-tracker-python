from datetime import datetime
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

def save_to_excel(data, filename="products_prices.xlsx"):
  df_new = pd.DataFrame(data)

  if os.path.exists(filename):
    df_old = pd.read_excel(filename)
    df_final = pd.concat([df_new, df_old], ignore_index=True)
  else:
    df_final = df_new

  df_final.to_excel(filename, index=False)
  print(f"تم حفظ البيانات بنجاح في {filename}")


def fetch_real_data():
  print("جاري الاتصال بالموقع وجلب البيانات الحقيقية...")
  url = "http://books.toscrape.com/"

  try:
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")
      scraped_data = []
      products = soup.find_all("article", class_="product_pod")[:5]

      for product in products:
        title = product.h3.a["title"]
        price = product.find("p", class_="price_color").text

        scraped_data.append({
            "اسم المنتج": title,
            "السعر": price,
            "تاريخ الفحص": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

      return scraped_data
    else:
      print("فشل الاتصال بالموقع، رمز الخطأ:", response.status_code)
      return []

  except Exception as e:
    print("حدث خطأ أثناء الاتصال:", e)
    return []

#main 
if __name__ == "__main__":
  print("جاري تشغيل أداة تتبع الأسعار الذكية...")

  real_data = fetch_real_data()

  if real_data:
    save_to_excel(real_data)
  else:
    print("لم يتم جلب أي بيانات لحفظها.")
