# --------------
#Importing header files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(path)

loan_status = data['Loan_Status'].value_counts(ascending=False)
loan_status.plot(kind = 'bar')
plt.show()

#Code starts here


# --------------
#Code starts here


#plt.xlabel('Types')

property_and_loan = data.groupby(['Property_Area','Loan_Status']).size().unstack()
property_and_loan.plot(kind = 'bar', stacked = False)
plt.xlabel('Property Area')
plt.ylabel('Loan Status')
plt.xticks(rotation = 45)


# --------------
#Code starts here




education_and_loan = data.groupby(['Education','Loan_Status']).size().unstack()
education_and_loan.plot(kind = 'bar', stacked = True)
plt.xlabel('Education Status')
plt.ylabel('Loan Status')
plt.xticks(rotation = 45)


# --------------
#Code starts here


graduate = data[data['Education'] == 'Graduate']
not_graduate = data[data['Education'] == 'Not Graduate']

graduate['LoanAmount'].plot(kind = 'density', label = 'Graduate')
not_graduate['LoanAmount'].plot(kind = 'density', label = 'Not Graduate')


#Code ends here

#For automatic legend display
plt.legend()


# --------------
#Code starts here

#plt.subplots(1,2, figsize=(20,10))
#electric.plot.scatter(x = 'HP', y = 'Attack')
#res = df.groupby(['Generation','Legendary']).size().unstack()
#res.plot(kind='bar', stacked=True, ax=ax_1)
#ax_1.set_title('Stacked bar-chart with counts')

fig ,(ax_1,ax_2,ax_3) = plt.subplots(3,1,figsize=(20,10))
data.plot.scatter(x = 'ApplicantIncome', y = 'LoanAmount', ax = ax_1)
ax_1.set_title('Applicant Income')
data.plot.scatter(x = 'CoapplicantIncome', y = 'LoanAmount', ax = ax_2)
ax_2.set_title('Coapplicant Income')
data['TotalIncome'] = data['ApplicantIncome'] + data['CoapplicantIncome']
data.plot.scatter(x = 'TotalIncome', y = 'LoanAmount', ax = ax_3)
ax_3.set_title('Total Income')


