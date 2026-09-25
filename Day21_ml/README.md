# Day 21 - ML Fundamentals

## Project: House Price Prediction

### Overview

In Day 21, I worked on Machine Learning fundamentals using a real house-price dataset from Kaggle.

I explored the dataset, identified the features and target variable, performed an 80/20 train-test split, and implemented a basic Linear Regression model.

## What I Did

- Loaded the house-price dataset using Pandas.
- Explored the dataset and checked its rows, columns, data types, and missing values.
- Identified **12 features** such as bedrooms, bathrooms, living area, lot size, floors, etc.
- Selected **price** as the target variable.
- Divided the data into:
  - **80% Training Data → 3680 records**
  - **20% Testing Data → 920 records**
- Used `train_test_split()` from Scikit-learn for splitting the dataset.
- Implemented a **Linear Regression** Machine Learning model.
- Trained the model using the training data.
- Generated predictions using the testing data.
- Evaluated the model using:
  - MAE (Mean Absolute Error)
  - MSE (Mean Squared Error)
  - R² Score
- Displayed sample actual prices and predicted prices.
- Identified **49 records with zero price** during data analysis.

## Technologies Used

- Python
- Pandas
- Scikit-learn
- Linear Regression
- Kaggle Dataset
- PyCharm

## ML Workflow

```text
House Price Dataset
        ↓
Data Exploration
        ↓
Features (X) + Target (y)
        ↓
80/20 Train-Test Split
        ↓
Linear Regression Model
        ↓
Model Training
        ↓
Predictions
        ↓
MAE, MSE, R² Evaluation