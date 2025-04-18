import pandas as pd
import spacy
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
# Load data first (replace with your actual file path)
data = pd.read_excel('victim_narratives.xlsx')

# Download stopwords only if not already done
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

# Preprocessing function
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return " ".join(tokens)

# Apply preprocessing
data['Processed_Quote'] = data['Direct Quote'].apply(preprocess_text)

# Check your result
print(data[['Direct Quote', 'Processed_Quote']].head())




# Plot frequencies of Themes
plt.figure(figsize=(10,5))
sns.countplot(y='Theme', data=data, order=data['Theme'].value_counts().index)
plt.title("Frequency of Themes")
plt.xlabel("Count")
plt.ylabel("Theme")
plt.tight_layout()
plt.show()
#save the plot as a png file in the current directory
plt.savefig('theme_freq.png')


# Plot frequencies of Sub-themes
plt.figure(figsize=(10,7))
sns.countplot(y='Sub-theme', data=data, order=data['Sub-theme'].value_counts().index)
plt.title("Frequency of Sub-Themes")
plt.xlabel("Count")
plt.ylabel("Sub-theme")
plt.tight_layout()
plt.show()
#save the plot as a png file in the current directory
plt.savefig('subtheme_freq.png')

from wordcloud import WordCloud

text = " ".join(data['Processed_Quote'])

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Commonly Mentioned Terms")
plt.show()
#save the plot as a png file in the current directory

plt.savefig('wordcloud.png')