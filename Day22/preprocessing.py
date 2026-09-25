import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("data/messy_house_listings.csv")

print("Shape:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print()
print("Nulls per column:")
print(df.isnull().sum())
print()
df.info()
print()
print("Unique city values:", df["city"].nunique())
print(df["city"].value_counts(dropna=False))
print()
print(df.describe())

# ---------- STEP 3: FIX STRUCTURE ----------

# 1. Duplicates
df = df.drop_duplicates()
print("After removing duplicates:", df.shape)

# 2. price: text like "$450,000" -> number
df["price"] = (df["price"]
               .str.replace("$", "", regex=False)
               .str.replace(",", "", regex=False))
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 3. sqft_living: text like "1,850 sqft" -> number
df["sqft_living"] = (df["sqft_living"].astype(str)
                     .str.replace(" sqft", "", regex=False)
                     .str.replace(",", "", regex=False))
df["sqft_living"] = pd.to_numeric(df["sqft_living"])

# 4. Date: text -> real date
df["listing_date"] = pd.to_datetime(df["listing_date"])

# 5. City: one spelling per city
df["city"] = df["city"].str.strip().str.title()

# ---------- CHECK ----------
print(df.dtypes)
print("Unique cities:", df["city"].nunique())
print("Price nulls:", df["price"].isnull().sum())
print("Price == 0:", (df["price"] == 0).sum())
print(df[["price", "sqft_living"]].describe())


# ---------- STEP 4: BAD PRICES + IMPOSSIBLE VALUES ----------

# 1. Price: treat 0 and absurd values as missing, then drop those rows
df["price"] = df["price"].replace(0, np.nan)
df.loc[df["price"] > 10_000_000, "price"] = np.nan

before = len(df)
df = df.dropna(subset=["price"])
print("Rows dropped for bad price:", before - len(df))
print("Shape now:", df.shape)

# 2. Impossible feature values -> turn into NaN (we fill them in Step 5)
print("bedrooms == 0:", (df["bedrooms"] == 0).sum())
print("yr_built > 2024:", (df["yr_built"] > 2024).sum())
print("sqft_lot > 1,000,000:", (df["sqft_lot"] > 1_000_000).sum())

df.loc[df["bedrooms"] == 0, "bedrooms"] = np.nan
df.loc[df["yr_built"] > 2024, "yr_built"] = np.nan
df.loc[df["sqft_lot"] > 1_000_000, "sqft_lot"] = np.nan

print(df.isnull().sum())
print(df[["price", "bedrooms", "sqft_lot", "yr_built"]].describe())

# ---------- STEP 5: SPLIT FIRST, THEN FILL NULLS ----------

# 1. Split (80% train, 20% test)
train, test = train_test_split(df, test_size=0.2, random_state=42)
train, test = train.copy(), test.copy()
print("Train:", train.shape, "| Test:", test.shape)

# 2. Learn the fill values from TRAIN only
fill_cols = ["bedrooms", "bathrooms", "sqft_lot", "condition", "yr_built"]
medians = train[fill_cols].median()
print(medians)

# 3. Apply the same fill values to both sets
train[fill_cols] = train[fill_cols].fillna(medians)
test[fill_cols] = test[fill_cols].fillna(medians)

# 4. City is text, so mark missing ones honestly
train["city"] = train["city"].fillna("Unknown")
test["city"] = test["city"].fillna("Unknown")

print("Nulls left in train:", train.isnull().sum().sum())
print("Nulls left in test:", test.isnull().sum().sum())

# ---------- STEP 6: FEATURE SCALING ----------

# Columns to scale. Left out on purpose:
#   price      -> it's the target, keep it in real dollars
#   waterfront -> already 0/1
#   city, listing_id, listing_date -> not numeric features
scale_cols = ["bedrooms", "bathrooms", "sqft_living", "sqft_lot",
              "floors", "condition", "yr_built"]

# BEFORE stats (train only)
before = train[scale_cols].describe().T[["mean", "std", "min", "max"]]

# Learn from train only
std_scaler = StandardScaler().fit(train[scale_cols])
mm_scaler = MinMaxScaler().fit(train[scale_cols])

# Apply to train and test
train_std = pd.DataFrame(std_scaler.transform(train[scale_cols]),
                         columns=scale_cols, index=train.index)
test_std = pd.DataFrame(std_scaler.transform(test[scale_cols]),
                        columns=scale_cols, index=test.index)

train_mm = pd.DataFrame(mm_scaler.transform(train[scale_cols]),
                        columns=scale_cols, index=train.index)
test_mm = pd.DataFrame(mm_scaler.transform(test[scale_cols]),
                       columns=scale_cols, index=test.index)

# AFTER stats
after_std = train_std.describe().T[["mean", "std", "min", "max"]]
after_mm = train_mm.describe().T[["mean", "std", "min", "max"]]

print("BEFORE scaling:\n", before.round(2), "\n")
print("AFTER StandardScaler:\n", after_std.round(2), "\n")
print("AFTER MinMaxScaler:\n", after_mm.round(2), "\n")
print("sqft_lot median after MinMax:", train_mm["sqft_lot"].median().round(3))


y_train, y_test = train["price"], test["price"]

sets = {
    "Unscaled": (train[scale_cols], test[scale_cols]),
    "Standard": (train_std, test_std),
    "MinMax": (train_mm, test_mm),
}

def get_mae(model, X_train, X_test):
    try:
        pred = model.fit(X_train, y_train).predict(X_test)
        return round(mean_absolute_error(y_test, pred))
    except Exception:
        return "diverged"

for name, (X_train, X_test) in sets.items():
    knn = get_mae(KNeighborsRegressor(n_neighbors=5), X_train, X_test)
    sgd = get_mae(SGDRegressor(max_iter=2000, tol=1e-6, random_state=0), X_train, X_test)
    print(f"{name:9} | KNN error: {knn:>8} | SGD error: {sgd:>20}")