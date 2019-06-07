# --------------
# Import packages
import numpy as np
import pandas as pd
from scipy.stats import mode 
 
# code starts here
bank = pd.read_csv(path)
categorical_var = bank.select_dtypes(include = 'object')
print(categorical_var)

numerical_var = bank.select_dtypes(include = 'number')
print(numerical_var)

# code ends here


# --------------
# code starts here

banks = bank.drop(['Loan_ID'], axis = 1)

#print(banks.isnull().sum())

#bank_mode = banks.mode()
#print('Bank mode is : \n', bank_mode)

#for column in banks.columns:
    #banks[column].fillna(banks[column].mode()[0], inplace=True)

bank_mode= banks.mode()
for x in banks.columns.values:
        banks[x]=banks[x].fillna(value=bank_mode[x].iloc[0])

#banks = banks.fillna(value = bank_mode, axis = 1)
print(banks)

#code ends here


# --------------
# Code starts here




avg_loan_amount = pd.pivot_table(banks, index = ['Gender', 'Married', 'Self_Employed'], values = 'LoanAmount')
print(avg_loan_amount)

# code ends here



# --------------
# code starts here




#single_type_legendary = len(df[df['Type 2'].isnull() & df['Legendary'] == True])
#highest_legendary = df[df['Legendary'] ==True]['Type 1'].value_counts().idxmax()

loan_approved_se = len(banks[(banks['Self_Employed'] == 'Yes') & (banks['Loan_Status'] == 'Y')])
loan_approved_nse = len(banks[(banks['Self_Employed'] == 'No') & (banks['Loan_Status'] == 'Y')])

percentage_se = (loan_approved_se * 100/614)
print(percentage_se)

percentage_nse = (loan_approved_nse * 100/614)
print(percentage_nse)
# code ends here


# --------------
# code starts here

#df['Type 1'] = df['Type 1'].apply(lambda x: x.lower())
loan_term = banks['Loan_Amount_Term'].apply(lambda x: int(x)/12)

#single_type_legendary = len(df[df['Type 2'].isnull() & df['Legendary'] == True])
big_loan_term = len(loan_term[ loan_term >= 25])
print(big_loan_term)
# code ends here


# --------------
# code starts here




#fastest_type = df.groupby('Type 1').agg({'Speed':'median'}).sort_values(by='Speed',ascending=False).index[0].lower()

loan_groupby = banks.groupby('Loan_Status')
loan_groupby = loan_groupby['ApplicantIncome', 'Credit_History']
mean_values = loan_groupby.mean()
print(mean_values)

# code ends here


