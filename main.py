from flipcart_extraction import SmartPhone
import pandas as pd

bot = SmartPhone()
data = bot.data_collect(total_pages=50)
bot.quit()

flipcart_data = {
    "Image_url": data["image_urls"],
    "Rating": data["ratings"],
    "Phone Title": data["titles"],
    "Specs": data["specs"],
    "Price Without Discount": data["price_without_discount"],
    "Price With Discount": data["price_with_discount"]
}


df = pd.DataFrame(flipcart_data)
print("Successfully collected data")
print(df.shape)

df['Specs'] = df['Specs'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else x)

memory_store = {}
memory_store['flipkart_data'] = df


