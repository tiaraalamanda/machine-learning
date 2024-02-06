# -*- coding: utf-8 -*-
"""Kelompok 7_Proyek UAS

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KJ_KNTOlA4oERal5QO2TPsyYspt-QjcG

## Sentiment analysis using Algorithm
"""

import pandas as pd
df=pd.read_csv('Review Avengers Endgame.csv')
df.head(200)

import matplotlib.pyplot as plt

plt.hist(df.reviews_rating)
plt.show()

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud
import spacy

nlp = spacy.load('en', disable=['parser', 'ner'])

"""Transform into lowercase"""

df['reviews_text'] = df['reviews_text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['reviews_text'].head(150)

df['reviews_title'] = df['reviews_title'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['reviews_title'].head(150)

"""Remove Punctuation"""

df['reviews_text'] = df['reviews_text'].str.replace('[^\w\s]',' ')
df['reviews_text'].head(150)

df['reviews_title'] = df['reviews_title'].str.replace('[^\w\s]',' ')
df['reviews_title'].head(150)

"""Remove Angka"""

df['reviews_text']= df['reviews_text'].str.replace("\d+",'')
df['reviews_text'].head(150)

df['reviews_title']= df['reviews_title'].str.replace("\d+",'')
df['reviews_title'].head(150)

"""Remove Spasi berlebih"""

df['reviews_text'] = df['reviews_text'].str.replace('\s+',' ')
df['reviews_text'].head(150)

df['reviews_title'] = df['reviews_title'].str.replace('\s+',' ')
df['reviews_title'].head(150)

"""Remove Stopwords"""

stop = stopwords.words('english')
df['reviews_text'] = df['reviews_text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['reviews_text'].head(150)

df['reviews_title'] = df['reviews_title'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['reviews_title'].head(150)

textt = " ".join(review for review in df.reviews_text) #wordcloud review_text
wordcloud = WordCloud(background_color="white").generate(textt)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud11.png')
plt.show()

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(textt) #wordcloud review_text dengan pembatasan ukuran dan jumlah kata yang ditampilkan
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

wordcloud.to_file("first_review.png")

neutral_score = 5 #remove rating netral (kita ambil rating 5)
df = df[df['reviews_rating'] != neutral_score]
df.tail()
df['sentiment'] = df['reviews_rating'].apply(lambda rating : +1 if rating > neutral_score else -1)

df.head(150)

"""**Uji Statistik (Chi Square)**"""

import pandas as pd
from scipy.stats import chi2_contingency

ctab = pd.crosstab(df.reviews_rating, df.sentiment)
print(ctab)

# Chi-square test of independence.
c, p, dof, expected = chi2_contingency(ctab)
# Print the p-value
print(p)

res = stat
res.chisq(df = ctab)
print(res.summary)

"""**Cek Sentimen**"""

positive = df[df['sentiment'] == 1]
negative = df[df['sentiment'] == -1]

textt = " ".join(review for review in positive.reviews_text) #wordcloud review positif
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(textt)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

negative.dropna(subset = ["reviews_title"], inplace=True) #wordcloud review negatif
textt = " ".join(review for review in negative.reviews_text)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(textt)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

df['sentimentt'] = df['sentiment'].replace({-1 : 'negative'})
df['sentimentt'] = df['sentimentt'].replace({1 : 'positive'})
plt.hist(df.sentimentt)
plt.show()

"""**Split the Dataframe**"""

dfNew = df[['No','reviews_title','sentiment']]
dfNew.head(200)

"""#Naive Bayes"""

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(dfNew['reviews_title']).toarray()
y = dfNew['sentiment']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

"""**Build Machine Learning Model**"""

from sklearn.naive_bayes import GaussianNB
# Mengaktifkan/memanggil/membuat fungsi klasifikasi Naive Bayes
modelnb = GaussianNB()
# Memasukkan data training pada fungsi klasifikasi Naive Bayes
nbtrain = modelnb.fit(X_train, y_train)

# Menentukan hasil prediksi dari x_test
y_pred = nbtrain.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

import seaborn as sns

confusion_matrix= pd.crosstab(y_test, y_pred)
plt.figure(figsize=(12,8))
sns.heatmap(confusion_matrix, annot=True, cmap="YlGnBu")

"""#KNN"""

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=7)
classifier.fit(X_train, y_train) #membentuk model

y_pred = classifier.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

import seaborn as sns

confusion_matrix= pd.crosstab(y_test, y_pred)
plt.figure(figsize=(12,8))
sns.heatmap(confusion_matrix, annot=True, cmap="YlGnBu")

"""**Find the best K**"""

import numpy as np
error = []

# Calculating error for K values between 1 and 40
for i in range(1, 40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))

plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')
#beda beda karena data yang digunakan random maka nilai k nya beda beda