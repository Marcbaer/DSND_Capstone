# Starbucks Capstone Challenge

The following Section describes the objective of the project and the applied procedure.
In order to generate valuable insights from the provided datasets, the **CRISP-DM** Methodology (Cross-Industry Standard Process for Data Mining) is applied.

- **Business Understanding**:
    Starbucks tries to optimize its revenue and profit by leveraging targeted customer offers. The offer portfolio consists of three offer types. The Business challenge is to understand how certain customers react to a certain type of offer from the offering portfolio. The conducted analysis should provide insights into which offers should be sent to want customer group. The final challenge that is solved in this project, is to predict wether a customer will successfully complete a specific offer or not.


- **Data Understanding**:
    In order to understand the problem it is important to investigate the provided data attributes in details and conduct a sophisticated Exploratory Data Analysis.


- **Data Preparation**:
    The data is cleaned and processed in order to remove un-useful attributes and missing values.


- **Modeling**:
    The datasets are combined and processed to ensure and optimized the predictive model.Three different classifiers were built and trained on a training set.


- **Evaluation**:
    The three classifiers were compared against each other based on their performance on the test dataset. The used metrics are mean accuracy and F1 score. These metrics were choosen because they provide good measures of performance for a classfier. The feature importance is investigated in order to comment on the importance of the provided data attributes.


The Project consist of the following sections:

1. Exploratory Data Analysis
2. Data Cleaning
3. Feature Engineering
4. ML Model Selection
5. Evaluation & Feature Importance
6. Conclusion

Additional files: 

The project workspace contains the following 3 files relevant for the project:

- **[Starbucks_Capstone_notebook.ipynb] (Starbucks_Capstone_notebook.ipynb)**: Main notebook which contains the Analysis and Evaluation
- **[data_cleaning.py](data_cleaning.py)**: Python script that contains data processing functions used to generate the final dataset used for model training.
- **[model_evaluation.py](model_evaluation.py)**: Python script that contains a function to evaluate the trained classifiers.

Libraries:

- pandas
- numpy
- json
- matplotlib
- re
- seaborn
- sklearn


### Data Sets

The data is contained in three files:

* portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.)
* profile.json - demographic data for each customer
* transcript.json - records for transactions, offers received, offers viewed, and offers completed

Here is the schema and explanation of each variable in the files:

**portfolio.json**
* id (string) - offer id
* offer_type (string) - type of offer ie BOGO, discount, informational
* difficulty (int) - minimum required spend to complete an offer
* reward (int) - reward given for completing an offer
* duration (int) - time for offer to be open, in days
* channels (list of strings)

**profile.json**
* age (int) - age of the customer 
* became_member_on (int) - date when customer created an app account
* gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
* id (str) - customer id
* income (float) - customer's income

**transcript.json**
* event (str) - record description (ie transaction, offer received, offer viewed, etc.)
* person (str) - customer id
* time (int) - time in hours since start of test. The data begins at time t=0
* value - (dict of strings) - either an offer id or transaction amount depending on the record