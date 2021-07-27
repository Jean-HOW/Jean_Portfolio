# Portfolio

## 1. [GDP and Vaccination](https://github.com/Jean-HOW/Python_project/blob/main/gdp_vaccination/GDP_vaccination.ipynb)
The report is aimed to study the relationship between the population, GDP, vaccination rate in South-East Asian countries. There are three dataset provided which are `2019-GDP.csv`, `2020-Population.csv`, and `Vaccinations.csv`.

### 1.a Imported Libraries
numpy, pandas, and matplotlib



## 2. [Essay Estimator](https://github.com/Jean-HOW/Python_project/blob/main/essay_estimator/essay_estimator.ipynb)

The objective of this study is to perform predictive analysis throught supervised machine learning on Essay-Features.csv dataset. The dataset contains the students' essay scoring and features that might have correspondent effect on the essay scoring such as characters, words, punctuations, average word length, synonym words, and others.

### 2.a Imported Libraries
numpy, pandas, sklearn, and matplotlib

### 2.b Modified Data

#### Original Data Columns
| column names | Description |
| ------------- | ------------------------------------------------------ |
| essayid | a unique id to identify the essay |
| chars | number of characters in the essay, including spaces |
| words | number of words in the essay |
| commas | number of commas in the essay |
| apostrophes | number of apostrophes in the essay |
| punctuations | number of punctuations (other than commas, apostrophes, period, questions marks in the essay) |
| avg_word_length | the average length of the words in the essay |
| sentences | number of sentences in the essay, determined by the period (fullstops) |
| questions | number of questions in the essay, determined by the question marks |
| avg_word_sentence | the average number of words in a sentence in the essay |
| POS | total number of Part-of-Speech discovered |
| POS/total_words | fraction of the POS in the total number of words in the essay |
| prompt_words | words that are related to the essay topic |
| prompt_words/total_words | fraction of the prompt words in the total number of words in the essay |
| synonym_words | words that are synonymous |
| synonym_words/total_words | fraction of the synonymous words in the total number of words in the essay |
| unstemmed | number of words that were not stemmed in the essay |
| stemmed | number of words that were stemmed (cut to the based word) in the essay |
| score | the rating grade, ranging from 1 – 6 |

Calculate ratio of stemmed and unstemmed against the total_words iterate higher accuracy output.
```
df['stemmed/total_words'] = df['stemmed']/df['words']
df['unstemmed/total_words'] = df['unstemmed']/df['words']
df['related_words'] = df['prompt_words'] + df['POS'] + df['synonym_words']
```
### 2.c Supervised Learning
The `sklearn.model_selection.train_test_split()` is used to randomly split arrays or matrices into training and testing subsets, which are x_train, x_test, y_train, y_test. In this case, value of 0.25 is set as the test size, thus the 25% of dataset is splited as the test dataset and the remaining 75% are training dataset.

### 2.d Normalisation
When the distribution of data is unknown or the data doesn't not normally distributed, normalising data is important to leverage the numerical data without distorting the differences in the ranges of values. For instance, consider this df dataset containing two features, punctuations, and characters. Where punctuation ranges from 0 to 1, whereas character ranges from 236 to 4332. Thus, data normalisation allows to the variable to be at the same range.
```
sc = StandardScaler()
X_train = sc.fit_transform(X_train) 
X_test = sc.transform(X_test)
```
### 2.e Classification
RBF kernel SVM is applied in this report in order to target non-linear problems. Although RBF is a non-linear kernel, it utilises linear dicision region to generate non-linear combinations of the dataset's features to elevate the sample data onto a higher dimension space where linear hypersurface that partitions the underlying vector space into two sets, one for each class.
```
clf = svm.SVC(kernel = 'rbf',
              gamma = 'auto')
clf.fit(X_train,y_train)
pred_clf = clf.predict(X_test)
```
### 1.f Quadratic Weighted Kappa (QWK)
Quadratic weighted kappa (QWK) measures the agreement between two ratings. QWk typically changes from 0 to 1, which measures the agreement between raters from random to complete. When the metric go below 0, there is less agreement between the raters than expected by chance. The QWK is calculated between the scores which are expected and the predicted scores.
```
cohen_kappa_score(y_test, pred_clf, labels=None, weights= 'quadratic')
```
A perfect QWK score of 1.0 is granted when both the predictions and actuals are the same. Whereas, the least possible score is -1 which is given when the predictions are furthest away from actuals. The aim is to get as close to 1 as possible. This model shows a general QWK score of 0.667 which indicates high aggreement between the predicted and test score.

## 3. [2016 US Election (Obama vs Trump)](https://github.com/Jean-HOW/Python_project/tree/main/us_election)
The dataset is compressed file that contains Facebook posts from 15 of the top mainstream media sources (e.g., BBC, CNN, Fox News, etc.) from 2012 to 2016.


