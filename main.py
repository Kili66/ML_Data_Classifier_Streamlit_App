import streamlit as st 
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA 
import matplotlib.pyplot as plt 

st.title("Machine Learning Application in Healthcare")
st.write("""
        Explore Diffrent Classifiers
        which one is the best
         """
        )

dataset_name=st.sidebar.selectbox("Select Dataset", ("Iris", "breast_cancer", "wine dataset"))
#st.sidebar.slider("K", 1, 15)

st.write(dataset_name)

classifier_name=st.sidebar.selectbox("Select Classifier", ("KNN", "SVM", "Random Forest"))
#st.write(classifier_name)

def get_dataset(dataset_name):
    if dataset_name=="Iris":
        data= datasets.load_iris()
    elif dataset_name=="breast_cancer":
        data=datasets.load_breast_cancer()
    else:
        data= datasets.load_wine()
    X= data.data 
    y= data.target 
    
    return X, y 
    
X, y= get_dataset(dataset_name)
st.write("Shape of data", X.shape)  
st.write("number of unique classes", len(np.unique(y)))    
# st.write("number of classes", len(y))    
params= {}
def add_para(clf_name):
    
    if clf_name=="KNN":
        K=st.sidebar.slider("K", 1, 15)
        params["K"]=K
    elif clf_name=="SVM":
        C= st.sidebar.slider("C", 0.01, 10.0)
        params["C"]=C
    else:
        rf= st.sidebar.slider("max_depth", 2, 15)
        n_estimators= st.sidebar.slider("n_estimators", 1, 100)
        params["max_depth"]=rf
        params["n_estimators"]=n_estimators
    return params 
add_para(classifier_name)
    
def get_classifier(clf_name, params):
    if clf_name=="KNN":
        clf= KNeighborsClassifier(n_neighbors=params["K"])
    elif clf_name=="SVM":
        clf= SVC(C=params["C"])
    else:
        clf= RandomForestClassifier(n_estimators=params["n_estimators"], max_depth=params["max_depth"], random_state=1234)
    return clf

clf= get_classifier(classifier_name,params)
# split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.2, random_state=1234)
    
clf.fit(X_train, y_train)
y_pred= clf.predict(X_test)
acc= accuracy_score(y_test, y_pred)
st.write(f"classifier= {classifier_name} ")
st.write(f"Accuracy= {acc} ")

# Plot
pca= PCA(2)
X_projected= pca.fit_transform(X)
x1= X_projected[:, 0]
x2= X_projected[:, 1]
fig= plt.figure()
plt.scatter(x1, x2, c="g", alpha=0.8, cmap="viridis")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.colorbar()
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
