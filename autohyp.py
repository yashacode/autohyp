import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
from statsmodels.stats.weightstats import CompareMeans as cm


def process(file):
  df = pd.read_excel(file)
  df = df.applymap(lambda x: pd.to_numeric(x, errors='coerce'))

  #categorize each col
  categorical = []
  normal = []
  non_normal = [] 
  for col in df.columns:
    if is_binary(df, col):
      categorical.append(col)
    elif normality(df, col, 0.0001):
      normal.append(col)
    else:
      non_normal.append(col)

  #get user input to split the data into 2 groups for comparison
  print("columns: ")
  for col in df.columns:
    print(col)
  comparison = input("\nenter the column used for comparison:")
  if comparison in categorical:
    group1 = df[df[comparison] == 0]
    group1_name = comparison + "=0"
    group2 = df[df[comparison] == 1]
    group2_name = comparison + "=1"
  else:
    split = int(input("enter the value of " + comparison + " for which to split the data:"))
    group1 = df[df[comparison] <= split]
    group1_name = comparison + "<=" + str(split) 
    group2 = df[df[comparison] > split]
    group2_name = comparison + ">" + str(split)

  categorical_data = compare(categorical, group1, group2, df, group1_name=group1_name, group2_name=group2_name)

  normal_data = compare_means(normal, group1, group2, df, group1_name=group1_name, group2_name=group2_name)

  non_normal_data = compare_medians(non_normal, group1, group2, df, group1_name=group1_name, group2_name=group2_name)

  file_path = 'output.xlsx'

  # Use ExcelWriter to save DataFrames to separate sheets
  with pd.ExcelWriter(file_path) as writer:
      categorical_data.to_excel(writer, sheet_name='categorical variables', index=False)
      normal_data.to_excel(writer, sheet_name='normal variables', index=False)
      non_normal_data.to_excel(writer, sheet_name='non normal variables', index=False)


# returns true if col only contains 0 and 1
def is_binary(df, col):
  unique = df[col].unique()
  return set(unique).issubset({0,1})

#determines normality
def normality(df, col, alpha):
  x = df[col].dropna()

  #removes outliers (>3 stdevs)
  z_scores = stats.zscore(x)
  filtered = x[abs(z_scores) <= 3]

  statistic, p = stats.shapiro(filtered)
  return p > alpha

def mean_sdev(series):
  x = pd.to_numeric(series, errors='coerce').dropna()
  return x.mean(), x.std()

def median_iqr(series):
  x = pd.to_numeric(series, errors='coerce').dropna()
  return x.median(), (x.quantile(.25), x.quantile(.75))

def n_percent(series, target=1, not_this=False):
  if not_this:
    occurances = (series!=target).sum()
  else:
    occurances = (series==target).sum()
    if ((series==target).sum() + (series!=target).sum() != len(series)):
      print('Fuck')
  return occurances, series.size

def bootstrap_ci(data1, data2, num_samples=1000, alpha=0.05):
    n1 = len(data1)
    n2 = len(data2)
    diff = np.zeros(num_samples)
    for i in range(num_samples):
        # Sample with replacement
        sample1 = np.random.choice(data1, n1, replace=True)
        sample2 = np.random.choice(data2, n2, replace=True)
        diff[i] = np.median(sample1) - np.median(sample2)
    # Calculate confidence interval
    lower_bound = np.percentile(diff, 100 * alpha / 2)
    upper_bound = np.percentile(diff, 100 * (1 - alpha / 2))
    return lower_bound, upper_bound

# 2 proportiontest for descrete variables
def compare (columns, group1, group2, df, group1_name="group1", group2_name="group2"):

  columns_discrete = ['category', 'all patients', group1_name, group2_name, 'difference', 'confdence interval 95%', 'p-value']
  categorical = pd.DataFrame(columns=columns_discrete)

  for col in columns:
    o1, p1 = n_percent(df[col])
    o2, p2 = n_percent(group1[col])
    o3, p3 = n_percent(group2[col])
    data = [(o1, round(o1/p1, 2)),(o2, round(o2/p2, 2)),(o3, round(o3/p3, 2))]
    stat, p_value = proportions_ztest([o2, o3], [p2, p3])
    ci = confint_proportions_2indep(o2,p2,o3,p3)
    entry = {'category': col, 'all patients': str(data[0][0]) + '('+str(data[0][1])+')',
             group1_name: str(data[1][0]) + '('+str(data[1][1])+')',
             group2_name: str(data[2][0]) + '('+str(data[2][1])+')',
            'difference': round(data[1][1]-data[2][1],2), 'confdence interval 95%': (round(ci[0],2),round(ci[1],2)) ,
            'p-value': round(p_value, 2)}
    categorical.loc[len(categorical)] = entry
  return categorical

# t-test for normally distributed continuous variables
def compare_means (columns, group1, group2, df, group1_name="group1", group2_name="group2"):

  columns_discrete = ['category', 'all patients', group1_name, group2_name, 'difference', 'confdence interval 95%', 'p-value']
  categorical = pd.DataFrame(columns=columns_discrete)

  for col in columns:
    o1, p1 = mean_sdev(df[col].dropna())
    o2, p2 = mean_sdev(group1[col].dropna())
    o3, p3 = mean_sdev(group2[col].dropna())
    data = [((round(o1, 2)), round(p1, 2)),((round(o2, 2)), round(p2, 2)),((round(o3, 2)), round(p3, 2))]
    x = cm.from_data(group1[col].dropna(), group2[col].dropna())
    tstat, p_value, dof = x.ttest_ind()
    ci = x.tconfint_diff()
    entry = {'category': col, 'all patients': str(data[0][0]) + '['+str(data[0][1])+']',
             group1_name: str(data[1][0]) + '['+str(data[1][1])+']',
             group2_name: str(data[2][0]) + '['+str(data[2][1])+']',
            'difference': round(data[1][0]-data[2][0],2), 'confdence interval 95%': (round(ci[0],2),round(ci[1],2)) ,
            'p-value': round(p_value, 2)}
    categorical.loc[len(categorical)] = entry
  return categorical
# mann-whitney test for skewed continuous variables
def compare_medians (columns, group1, group2, df, group1_name="group1", group2_name="group2"):

  columns_discrete = ['category', 'all patients', group1_name, group2_name, 'difference', 'confdence interval 95%', 'p-value']
  categorical = pd.DataFrame(columns=columns_discrete)

  for col in columns:
    if len(group1[col].dropna()) == 0:
      print(col)
      continue
    o1, p1 = median_iqr(df[col].dropna())
    o2, p2 = median_iqr(group1[col].dropna())
    o3, p3 = median_iqr(group2[col].dropna())
    data = [((round(o1, 2)), ((round(p1[0],2)), round(p1[1],2))),
     ((round(o2, 2)), ((round(p2[0],2)), round(p2[1],2))),
      ((round(o3, 2)), ((round(p3[0],2)), round(p3[1],2)))]
    U_stat, p_value = stats.mannwhitneyu(group1[col].dropna(), group2[col].dropna(), True, "two-sided")
    ci = bootstrap_ci(group1[col].dropna(), group2[col].dropna())
    entry = {'category': col, 'all patients': str(data[0][0]) + '['+str(data[0][1][0]) + '-' + str(data[0][1][1]) +']',
             group1_name: str(data[1][0]) + '['+str(data[1][1][0]) + '-' + str(data[1][1][1])+']',
             group2_name: str(data[2][0]) + '['+str(data[2][1][0]) + '-' + str(data[2][1][1])+']',
            'difference': round(data[1][0]-data[2][0],2), 'confdence interval 95%': (round(ci[0],2),round(ci[1],2)) ,
            'p-value': round(p_value, 2)}
    categorical.loc[len(categorical)] = entry
  return categorical

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_excel.py <excel_file>")
        sys.exit(1)

    excel_file = sys.argv[1]
    process(excel_file)