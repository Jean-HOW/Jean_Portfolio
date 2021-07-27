# Portfolio

## Data analysis and visualization:

### 1. GDP_vaccination
The objective of this study is to perform predictive analysis throught supervised machine learning on Essay-Features.csv dataset. The dataset contains the students' essay scoring and features that might have correspondent effect on the essay scoring such as characters, words, punctuations, average word length, synonym words, and others.

### 1.A Imported Libraries
pandas, sklearn, and matplotlib

#### Original Data Columns
• essayid - a unique id to identify the essay
• chars - number of characters in the essay, including spaces
• words - number of words in the essay
• commas - number of commas in the essay
• apostrophes - number of apostrophes in the essay
• punctuations - number of punctuations (other than commas, apostrophes, period, questions marks in the essay
• avg_word_length - the average length of the words in the essay
• sentences - number of sentences in the essay, determined by the period (fullstops)
• questions - number of questions in the essay, determined by the question marks
• avg_word_sentence - the average number of words in a sentence in the essay
• POS - total number of Part-of-Speech discovered
• POS/total_words - fraction of the POS in the total number of words in the essay
• prompt_words - words that are related to the essay topic
• prompt_words/total_words - fraction of the prompt words in the total number of words in the essay
• synonym_words - words that are synonymous
• synonym_words/total_words - fraction of the synonymous words in the total number of words in the essay
• unstemmed - number of words that were not stemmed in the essay
• stemmed - number of words that were stemmed (cut to the based word) in the essay
• score - the rating grade, ranging from 1 – 6

### 1.B Modified Data
Calculate ratio of stemmed and unstemmed against the total_words iterate higher accuracy output.
```
df['stemmed/total_words'] = df['stemmed']/df['words']
df['unstemmed/total_words'] = df['unstemmed']/df['words']
df['related_words'] = df['prompt_words'] + df['POS'] + df['synonym_words']
```
### 1.C Supervised Learning
Supervised machine learning also known as supervised learning can be intepreted by the manipulation of labeled datasets to train algorithms that are able to categorise data or accurately predict results. In this df1 dataset, x is the input data and y is the labeled data. Data labeling is an important in data preprocessing for supervised machine learning, where both input and output data are labeled for classification to provide a learning basis for future data processing.

The implementation of training set on test set is crucial to validate the model built. The models generated are to predict the unknown score which is named as the test set. The `sklearn.model_selection.train_test_split()` is used to randomly split arrays or matrices into training and testing subsets, which are x_train, x_test, y_train, y_test. In this case, value of 0.25 is set as the test size, thus the 25% of dataset is splited as the test dataset and the remaining 75% are training dataset.

### 1.D Normalisation
When the distribution of data is unknown or the data doesn't not normally distributed, normalising data is important to leverage the numerical data without distorting the differences in the ranges of values. For instance, consider this df dataset containing two features, punctuations, and characters. Where punctuation ranges from 0 to 1, whereas character ranges from 236 to 4332. Thus, data normalisation allows to the variable to be at the same range.
```
sc = StandardScaler()
X_train = sc.fit_transform(X_train) 
X_test = sc.transform(X_test)
```

### 1.E Classification
Binary classification are tasks where specimens are assigned only one of two classes. For instance, logistic Regression, Support Vector Machines (SVM), and more are algorithms designed for binary classification problems. In this study, binary classification is applied.

#### - Support Vector Machine (SVM)
Support vector machines (SVM) is a linear model consists a set of supervised learning techniques used for classification, regression, and outliers identification. There are specialised SVMs such as support vector regression (SVR) and support vector classification (SVC) designed to tackle particular machine learning problems. There are two different types of SVMs, one is the simple SVM generally applied for linear regression and classification problems .

Besides, SVMs also use Kernel functions to systematically find support vector classifiers in higher dimensions as it provides more flexibility for non-linear data so that more features can be added to fit a hyperplane instead of a two-dimensional space. The functions include linear, polynomial, Gaussian Radial Basis Function (RBF), Sigmoid, and others.

RBF kernel SVM is applied in this report in order to target non-linear problems. Although RBF is a non-linear kernel, it utilises linear dicision region to generate non-linear combinations of the dataset's features to elevate the sample data onto a higher dimension space where linear hypersurface that partitions the underlying vector space into two sets, one for each class.
```
clf = svm.SVC(kernel = 'rbf',
              gamma = 'auto')
clf.fit(X_train,y_train)
pred_clf = clf.predict(X_test)
```
### 1.F Quadratic Weighted Kappa (QWK)
Quadratic weighted kappa (QWK) measures the agreement between two ratings. QWk typically changes from 0 to 1, which measures the agreement between raters from random to complete. When the metric go below 0, there is less agreement between the raters than expected by chance. The QWK is calculated between the scores which are expected and the predicted scores.
```
cohen_kappa_score(y_test, pred_clf, labels=None, weights= 'quadratic')
```
A perfect QWK score of 1.0 is granted when both the predictions and actuals are the same. Whereas, the least possible score is -1 which is given when the predictions are furthest away from actuals. The aim is to get as close to 1 as possible. This model shows a general QWK score of 0.667 which indicates high aggreement between the predicted and test score.

### 1.G Prediction on Kaggle Dataset


2. obama_trump

## Data Science Project:
1. essay_estimator
2. 
