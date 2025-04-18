from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageOps

# --- STEP 1: Read keywords from Excel ---
excel_path = "/Users/donglinxiong/Downloads/Resume_Keywords_Weighted_Template.xlsx"
df = pd.read_excel(excel_path)

# Replace 'Keyword' with your actual column name if different
keywords_list = df['Keyword'].dropna().astype(str).tolist()
text = ' '.join(keywords_list)

# --- STEP 2: Load and preprocess the mask image ---
mask_path = "/Users/donglinxiong/Downloads/Resume_WordCloud.png"
image = Image.open(mask_path).convert("L")
image = ImageOps.invert(image)
mask_array = np.array(image)

# --- STEP 3: Generate word cloud ---
wordcloud = WordCloud(
    background_color="white",
    max_words=500,
    mask=mask_array,
    contour_color='black',
    contour_width=1,
    colormap='viridis'
).generate(text)

# --- STEP 4: Plot and Save ---
plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.show()

# --- Save Output ---
wordcloud.to_file("/Users/donglinxiong/Downloads/Resume_WordCloud_From_Excel.png")
