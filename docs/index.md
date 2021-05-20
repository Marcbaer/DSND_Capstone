# Predicting customer responsiveness for marketing offers

## Problem Introduction
Starbucks is trying to optimize its revenue and profit by sending out different types of offers in order to animate customers for additional purchases.
These offers include discounts once a customer reaches a certain benchmark, buy one / get one free (BOGO) vouchers or a simple advertisement for a drink (purely informational).
Every offer has a validity period before the offer expires.
As an example, a BOGO offer might be valid for only 5 days or a discount is only provided if a customer spends 30 dollars within a time period of 7 days.
Different customers react differently to specific offer types and therefore it is important for starbucks to understand, which customer segment is responsive to which offer type.
This allows the marketing team to target offer campaigns to a specific group of people and optimizes the outcome of each campaign.

This project deals with these customer reactions for specific marketing offers of starbucks.
The goal is to develope a model that predicts if a specific customer profile is responsive to a certaint type of offer.
The model can then be used by the business teams to decide wether an offer should be sent to a customer or not.


## Approach
 
The approach to takle down this challenge consists of three steps. First, the provided datasets were investigated and explored in a Exploratory Data Analysis in order to understand their potential to solve the challenge.
Second, the datasets were cleaned, processed, combined and feature engineering was applied where necessary.
This ensures optimal input information for the predictive model and allows robust and appropriate predictions.
In a third step, three different classification algorithms were modelled, trained and evaluated using the prepared input dataset. The used evaluation metrics are mean accuracy and f1 score.
The hyperparameters are tuned during training using Grid-Search and cross validation over a pre-defined parameter grid.
Finally, the results were analysed and the feature importance was measured in order to comment on the importance of each feature.

## Metrics

The final predictive algorithm is supposed to predict if a customer will complete an offer or not. Hence, this is a classification problem. Based on the nature of the problem mean accuracy and F1-score was used as evaluation metrics.
The F1-Score is a widely used metric for binary classification problems and combines the precision and recall of the model in one score.

## Exploratory Data Analysis

In order to gain an insightful understanding of the provided data and underlying customer segments, an Exploratory Data Analysis was conducted.
In a first step, the provided data attributes were analysed in an in-depth feature analysis. Three different datasets were analysed, the portfolio of offers at starbucks, customer profiles and transaction transcripts.
During the feature analysis and feature engineering process, the datasets were cleaned and transformed as required to ensure valuable inputs for the classification models.

The EDA showed, that most of the provided attributes are promising features for classification.


The following plot shows the distribution of the provided customer profiles. The majority of the provided customer profiles are males.

<img src="gender_dist.png">

The income distribution of the provided customer profiles is shown below. It can be observed, that the majority of incomes are distributed aroun 70'000.

<img src="income_dist.png">

The provided datasets were cleaned, processed and combined in order to provide an optimized input data set for the classfiers.

## Modelling

Three different classification algorithms were built in order to conduct model selection. The analyzed algorithms include a logistic regression model, a random forest classifier and a gradient boosting classifier.
These three approaches were choosen because of their known leading performance on a wide range of classification problems.
The models were built using scikit-learn.

## Hyperparameter Tuning

The hyperparameters were optimized by using grid search and cross validation. The tuned hyperparameters for the three models and the best found parameters are defined as followed:

- Logistic regression: 'penalty' and 'inverse regularization strength' (1 and L2)
- Random forest: 'number of estimators' and 'minimum number of samples required to split an internal node' (5 and 2)
- Gradient boosting: 'number of estimators' and 'learning rate' (50 and 1)

## Results
As a benchmark, the performance of a naive classifier was taken that predicts all offers as successfull. The evaluated mean accuracy of this naive classifier is 0.47 and the f1-score 0.64.
We expect our more sophisticated classifier to beat this benchmark significantly.
After training and hyperparameter tuning, the three classifiers performed well on the provided test dataset.

The logistic regression classifier reach a mean accuracy of 0.72 and a f1 score of 0.716 and the random forest classifier reached a mean accuracy of 0.69 and a f1 score of 0.714.
The gradient boosting classifier outperformed the other algorithms slightly with a mean accuracy of 0.728 and f1-score of 0.725.

From the provided data attributes, the income, offer duration, customer age and offer difficulty turned out to be the most important features for predicting offer success.
Other variables such as gender or member date have only a minor influence.
The importance of each provided feature is shown below.

<img src="feature_importance.png">

## Conclusion

The objective of the project was to provide accurate predictions if a specific customer profile will successfully react to a specific offer. 

After defining the business challenge and processing the provided datasets to optimize for the specified prediction problem, the resulting models performed well on the training and test data with an accuracy of around 73%.
The gradient boosting classifier outperforms the other algorithms slighlty in terms of mean accuracy and f1-score.
This is a significant improvement compared to a naive classifier which performs around 50%. 
Offer duration and difficulty are important features that influence wether an offer is successfull or not.
This provides interesting opportunities for the marketing team which can change the duration and difficulty of offers to optimize the success rate.

## Improvements
Suggestions for next steps and improvements include the collection of more data for model training because the given dataset reduced to only 66'501 rows after processing.
A larger training set could improve model performance and robusteness. It will be useful to collect more data before the model is deployed in production.
Furthermore, advanced hyperparameter tuning can be performed by renting more compute resources from a cloud provider and performing GridesearchCV over a larger parameter grid. With more available resources, more sophisticated approaches can also be investigated for hyperparameter tuning such as bayesian optimizers or the covariance matrix adaptation evolution strategy.
After leverage above two steps that ensure a well performing and robust classifier, the trained model can be deployed as a webservice to allow business teams to decide wether an offer should be sent to a specific customer or not.
