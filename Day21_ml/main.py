import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================================
# DAY 21 - ML FUNDAMENTALS & DATA PREPARATION
# Project: House Price Prediction
# ==========================================================


# ----------------------------------------------------------
# 1. LOAD DATASET
# ----------------------------------------------------------

df = pd.read_csv("data/modified_data.csv")

print("=" * 60)
print("              DATASET INFORMATION")
print("=" * 60)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])


# ----------------------------------------------------------
# 2. DISPLAY FIRST 5 ROWS
# ----------------------------------------------------------

print("\n----- FIRST 5 ROWS -----")
print(df.head())


# ----------------------------------------------------------
# 3. DISPLAY COLUMN NAMES
# ----------------------------------------------------------

print("\n----- COLUMN NAMES -----")
print(df.columns.tolist())


# ----------------------------------------------------------
# 4. DATASET INFORMATION
# ----------------------------------------------------------

print("\n----- DATASET INFORMATION -----")
df.info()


# ----------------------------------------------------------
# 5. CHECK MISSING VALUES
# ----------------------------------------------------------

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())


# ----------------------------------------------------------
# 6. DEFINE FEATURES AND TARGET
# ----------------------------------------------------------

features = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "sqft_above",
    "sqft_basement",
    "yr_built",
    "yr_renovated"
]

X = df[features]

y = df["price"]


# ----------------------------------------------------------
# 7. DISPLAY FEATURES AND TARGET
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("              FEATURES AND TARGET")
print("=" * 60)

print("\n----- FEATURES (X) -----")
print(X.head())

print("\nNumber of features:", X.shape[1])

print("\n----- TARGET (y) -----")
print(y.head())

print("\nTarget name:", y.name)


# ----------------------------------------------------------
# 8. TRAIN / TEST SPLIT
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ----------------------------------------------------------
# 9. DISPLAY TRAIN / TEST INFORMATION
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("                TRAIN / TEST SPLIT")
print("=" * 60)

print("Total records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining features shape:", X_train.shape)
print("Testing features shape:", X_test.shape)

print("Training target shape:", y_train.shape)
print("Testing target shape:", y_test.shape)


# ----------------------------------------------------------
# 10. CREATE LINEAR REGRESSION MODEL
# ----------------------------------------------------------

model = LinearRegression()


# ----------------------------------------------------------
# 11. TRAIN THE MODEL
# ----------------------------------------------------------

model.fit(X_train, y_train)

print("\n" + "=" * 60)
print("                MODEL TRAINING")
print("=" * 60)

print("Linear Regression model trained successfully.")


# ----------------------------------------------------------
# 12. MAKE PREDICTIONS
# ----------------------------------------------------------

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("\nPredictions generated successfully.")


# ----------------------------------------------------------
# 13. MODEL EVALUATION
# ----------------------------------------------------------

train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_test_pred)

train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)


# ----------------------------------------------------------
# 14. DISPLAY MODEL PERFORMANCE
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("                MODEL PERFORMANCE")
print("=" * 60)

print("\nTraining MAE: ₹{:,.2f}".format(train_mae))
print("Testing MAE: ₹{:,.2f}".format(test_mae))

print("\nTraining MSE:", train_mse)
print("Testing MSE:", test_mse)

print("\nTraining R2 Score:", train_r2)
print("Testing R2 Score:", test_r2)


# ----------------------------------------------------------
# 15. SAMPLE PREDICTIONS
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("                SAMPLE PREDICTIONS")
print("=" * 60)

results = pd.DataFrame({
    "Actual Price": y_test.values[:10],
    "Predicted Price": y_test_pred[:10]
})

results["Actual Price"] = results["Actual Price"].apply(
    lambda x: f"₹{x:,.2f}"
)

results["Predicted Price"] = results["Predicted Price"].apply(
    lambda x: f"₹{x:,.2f}"
)

print(results)


# ----------------------------------------------------------
# 16. PRICE DATA ANALYSIS
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("                 PRICE ANALYSIS")
print("=" * 60)

zero_prices = (df["price"] == 0).sum()
negative_prices = (df["price"] < 0).sum()

print("Number of zero prices:", zero_prices)
print("Number of negative prices:", negative_prices)

print("Minimum price: ₹{:,.2f}".format(df["price"].min()))
print("Maximum price: ₹{:,.2f}".format(df["price"].max()))

print("\nRows with zero price:")

zero_price_rows = df[df["price"] == 0]

if len(zero_price_rows) > 0:
    print(zero_price_rows)
else:
    print("No rows with zero price found.")