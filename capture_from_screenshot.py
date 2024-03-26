# Import the necessary libraries
from PIL import Image
import pytesseract, time
import pyautogui, webbrowser
import matplotlib.pyplot as plt

ticker = 'AMAT'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
url = "https://stockrow.com/" + ticker
x = webbrowser.open(url)
time.sleep(2)
myScreenshot = pyautogui.screenshot()
screenshotpath = r"C:\Users\OHAD\Google Drive\QualityInvetments\stockrow_excels\\" + ticker + ".png"
myScreenshot.save(screenshotpath)
# Open the image file
# replace 'test.png' with your image file
img = Image.open(screenshotpath)
img_target_price = img.crop((1300, 200, 1600, 1000))
plt.imshow(img_target_price)
plt.show()

# target_prices = pytesseract.image_to_string(img_target_price)

img_ratios = img.crop((0, 500, 450, 1000))
plt.imshow(img_ratios)
plt.show()
line_height = 50
img_height = img_ratios.size[1]
img_width = img_ratios.size[0]
lines = int(img_height / line_height)
for i in range(lines):
    line = img_ratios.crop((0, i * line_height, img_width, (i + 1) * line_height))
    plt.imshow(line)
    plt.show()
    text = pytesseract.image_to_string(line)
    text = text.replace("\n", "")
    if "Market Cap" in text:
        market_cap = text.split("Market Cap. ")[1]
        market_cap = float(market_cap.replace(",", ""))
    elif "Next 5Y EPS Growth" in text:
        FiveY_GR = text.split("Next 5Y EPS Growth ")[1]

    str = text.split("\n")

offset = int(len(str) / 2)
for i in range(offset):
    print(f"{str[i]} : {str[i + offset]}")

print(text)