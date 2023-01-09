# Heart_diesease_prediction
Primary Goal: : To achieve a webapplication which takes 14 heart attributes as an input and predict that a person have a heart disease or not.

Solution: Data for 1025 peoples are collected from kaggle.com. It Contains 14 attributes related to heart like age,sex etc.

Dataset: We Have a dataset of 1025 files which contains a person heart related attributes like age,cholestrol etc. This data is taken from kaggle.com and the ssource of this dataset is come from university of califorina.


![ezgif com-gif-maker (1)](https://user-images.githubusercontent.com/87935713/211139753-31b99a3f-14b6-4212-b276-7ec4d4bdbfa2.gif)

Please Ignore UI 😅😅.

Procedure To Train the model:

Step 1: Load the dataset from CSV file and check the entries in dataset.

Step 2: Now do Exploratory data analysis of data like number of null values, categorical data, missing values etc.In ouw dadtaset we have nothing to do this it is already cleaned data.

Step 3: Now split the dataset into dependent and independent variable. Dependent variables are those which we need to predict in our case we have target column which contains a person have a heart disease or not. Independent variables are those which helps us to predict the target and model mainly ffound corelation between independent variables.

Step 4: Now do the train test split so that we train our model andd test our model on different datasets.

Step 5: Now make the model of Logistic Regression class and do training this model on train data.

Step 6: Save the state of this module using Pickle module.

Step 7: Use this save state in your flask framework mainly building the webapplication.



Now at last we Successfully created a webapp which predict a person has a heart disease or not. 

Steps to run Webapp:

1. Download this whole code in your pc and open VS editor.
2. Download the required libraries which are needed to run webapplication.
3. Run the code of app1.py file , after that a URL is shown on your terminal copy it and paste it in your browser and enjoy your webapp with ml model.
