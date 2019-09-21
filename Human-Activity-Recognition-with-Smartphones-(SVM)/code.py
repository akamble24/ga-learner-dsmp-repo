# --------------
import pandas as pd
from collections import Counter

# Load dataset
data = pd.read_csv(path)
print(data.isnull().sum())
print(data.describe())



# --------------
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style(style='darkgrid')

# Store the label values 
label = data.iloc[:,-1]
# plot the countplot
sns.countplot(x=label)
plt.xticks(rotation=90)


# --------------
# make the copy of dataset
data_copy = data.copy()

# Create an empty column 
data_copy['duration'] = ''

# Calculate the duration

duration_df = data_copy.groupby([label[(label == 'WALKING_UPSTAIRS') | (label == 'WALKING_DOWNSTAIRS')], 'subject'])['duration'].count() * 1.28
duration_df = pd.DataFrame(duration_df)

# Sort the values of duration
plot_data = duration_df.reset_index().sort_values('duration',ascending=False)
plot_data['Activity'] = plot_data['Activity'].map({'WALKING_UPSTAIRS':'Upstairs','WALKING_DOWNSTAIRS':'Downstairs'})

plt.figure(figsize=(14,4))
sns.barplot(data=plot_data, x='subject', y='duration', hue='Activity')
plt.show()






# --------------
#exclude the Activity column and the subject column
feature_cols = data.select_dtypes(exclude=['object','int']).columns

#Calculate the correlation values
correlated_values = data[feature_cols].corr()

#stack the data and convert to a dataframe

correlated_values = correlated_values.stack().to_frame().reset_index().rename(columns={'level_0': 'Feature_1', 'level_1': 'Feature_2', 0:'Correlation_score'})

#create an abs_correlation column
correlated_values['abs_correlation'] = abs(correlated_values.iloc[:,2])

#Picking most correlated features without having self correlated pairs
s_corr_list = correlated_values.sort_values(by =['abs_correlation'], ascending=False)

top_corr_fields = s_corr_list[(s_corr_list['Feature_1'] != s_corr_list['Feature_2'])&(s_corr_list['abs_correlation']>0.8)]


print(top_corr_fields.head())



# --------------
# importing neccessary libraries
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support as error_metric
from sklearn.metrics import confusion_matrix, accuracy_score,precision_score,f1_score

# Encoding the target variable
le = LabelEncoder()
data['Activity'] = le.fit_transform(data['Activity'])

# split the dataset into train and test
X = data.iloc[:,:-1]
y = data['Activity']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=40)
# Baseline model 
classifier = SVC()
clf = classifier.fit(X_train,y_train)
y_pred = clf.predict(X_test)
precision = precision_score(y_test,y_pred,average = 'weighted')
print(precision)
accuracy = accuracy_score(y_test,y_pred)
print(accuracy)
f1_score = f1_score(y_test,y_pred,average = 'weighted')
print(f1_score)
model1_score = accuracy
f_score = f1_score



# --------------
# importing libraries
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel


lsvc = LinearSVC(C=0.01,penalty='l1',dual=False,random_state=42).fit(X_train,y_train)

# Feature selection using Linear SVC
model_2 = SelectFromModel(lsvc,prefit=True)
new_train_features = model_2.transform(X_train)
new_test_features = model_2.transform(X_test)

# model building on reduced set of features
classfier_2 = SVC()
clf_2 = classfier_2.fit(new_train_features,y_train)
y_pred_new = clf_2.predict(new_test_features)

precision, recall, f_score, support = error_metric(y_test,y_pred_new,average='weighted')
print(precision, recall, f_score, support)

model2_score = accuracy_score(y_test,y_pred_new)
print(model2_score)


# --------------
# Importing Libraries
from sklearn.model_selection import GridSearchCV

# Set the hyperparmeters
parameters = {'kernel': ['linear', 'rbf'], 'C': [100, 20, 1, 0.1]}
selector = GridSearchCV(classfier_2,parameters,scoring='accuracy')

# Usage of grid search to select the best hyperparmeters
selector.fit(new_train_features,y_train)
params = selector.best_params_
print(params)
means = selector.cv_results_['mean_test_score']
print(means)
stds = selector.cv_results_['std_test_score']
print(stds)
# Model building after Hyperparameter tuning
classifier_3 = SVC(C= 20, kernel= 'rbf')
clf_3 = classifier_3.fit(new_train_features,y_train)
y_pred_final = clf_3.predict(new_test_features)

precision, recall, f_score, support = error_metric(y_test,y_pred_final,average='weighted')
print(precision, recall, f_score, support)

model3_score = accuracy_score(y_test,y_pred_final)
print(model3_score)



