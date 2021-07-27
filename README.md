# Portfolio

## Data analysis and visualization:
1. GDP_vaccination

The objective of this study is to perform predictive analysis throught supervised machine learning on Essay-Features.csv dataset. The dataset contains the students' essay scoring and features that might have correspondent effect on the essay scoring such as characters, words, punctuations, average word length, synonym words, and others.

### Imported Libraries
pandas, sklearn, and matplotlib

### Modified Data

essayid	chars	words	commas apostrophes	punctuations	avg_word_length	sentences	questions	avg_word_sentence	POS	POS/total_words	prompt_words	prompt_words/total_words	synonym_words	synonym_words/total_words	unstemmed	stemmed	score

### Modified Data
```
df1['stemmed/total_words'] = df1['stemmed']/df1['words']
df1['unstemmed/total_words'] = df1['unstemmed']/df1['words']
df1['related_words'] = df1['prompt_words'] + df1['POS'] + df1['synonym_words']
```

Supervised Learning
Normalisation
Classification
Support Vector Machine (SVM)
Quadratic Weighted Kappa (QWK)
Kaggle Dataset
Conclusion
References


2. obama_trump

## Data Science Project:
1. essay_estimator
2. 
