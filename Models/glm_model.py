import pandas as pd
import sqlalchemy
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os

current_script_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_script_path)
project_root = os.path.dirname(current_directory)
if project_root not in sys.path:
    sys.path.append(project_root)
from Utils.db_connect import get_connection


try:
  engine = get_connection()
  print("Connection to the database was successful.")
except Exception as e:
  print(f"An error occurred while connecting to the database: {e}")
  
   
# Queries
query= '''
SELECT age, bmi, children, smoker, charges FROM dbo.Medical_Cost
'''
df = pd.read_sql(query, engine)

# Preprocessing
# GLMs need numeric inpuits. Convert 'smoker' (yes/no) to binary (1/0)
df['smoker'] = df['smoker'].apply(lambda x: 1 if x == 'yes' else 0)
df['const'] = 1

# Defining X (features) and y (target)
X = df[['const', 'age', 'bmi', 'children', 'smoker']]
y = df['charges']

# Model A: Linear Regression / OLS
print("Fitting OLS model...")
model_ols = sm.OLS(y, X).fit()
# This assumes data is normally distributed (bell curve), which costs are not.

# Model B: Generalized Linear Model (GLM)
print("Fitting GLM model...")
model_glm = sm.GLM(y, X, family=sm.families.Gamma(link=sm.families.links.log())).fit()
# Gamma distribution is more appropriate for cost data, which is positive and right-skewed.

# Comparing Results
print("\n=== OLS Summary (Truncated) ===")
print(model_ols.summary().tables[1])

print("\n=== GLM Summary (Truncated) ===")
print(model_glm.summary().tables[1])

# Visualization
pred_ols = model_ols.predict(X)
pred_glm = model_glm.predict(X)

plt.figure(figsize=(10, 5))
sns.scatterplot(x=y, y=pred_ols, label='OLS Predictions', alpha=0.5)
sns.scatterplot(x=y, y=pred_glm, label='GLM Predictions', alpha=0.5, color='orange')
plt.plot([0, 50000], [0, 50000], 'r--', label='Perfect Prediction') # Diagnosis line
plt.xlabel('Actual Charges')
plt.ylabel('Predicted Charges')
plt.title('Why GLM Wins: OLS predicts negative costs for low risk users!')
plt.legend()
plt.show()