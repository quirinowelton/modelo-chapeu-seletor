#%%
import pandas as pd
pd.set_option('display.max_columns', None)


harrypotter = pd.read_csv('../Harry potter/harry_potter_characters.csv')
harrypotter.info()
#%% Como a base foi criada aleatóriamente com um prompt para IA, foi checado se existiam nulos ou duplicatas.
(harrypotter == ' ').any()
(harrypotter== '').any()
harrypotter.isnull().sum()
harrypotter.duplicated()


#%%


harrypotter['casa'] = harrypotter['casa'].replace({
                                                    'Gryffindor': 0,
                                                    'Slytherin': 1,
                                                    'Hufflepuff': 2,
                                                    'Ravenclaw': 3
                                                    })


#%%
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

X = harrypotter.drop(columns='casa')
y = harrypotter['casa']

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
#%%

num_cols = X.select_dtypes(include='Int64').columns
cat_cols = X.select_dtypes(include= 'object').columns

Xtranformer = ColumnTransformer( transformers = [
    ("cat", OneHotEncoder(drop= 'first', handle_unknown= 'ignore', sparse_output=True), cat_cols)
])

model = RandomForestClassifier(random_state=42, n_jobs=-1)

pipe = Pipeline(steps=[
                    ("preprocesso", Xtranformer),
                    ("model", model)
])

params = {
    "model__min_samples_leaf": [10, 20, 35, 50],
    "model__n_estimators": [100, 300, 600, 1000],
    "model__criterion": ["gini", "entropy", "log_loss"],
    "model__class_weight": [None, 'balanced'],
    }

pipe.fit(X_train,Y_train)
grid = GridSearchCV(pipe, param_grid=params, cv=3, scoring="roc_auc_ovr", verbose=2)
grid.fit(X_train, Y_train)


#%%
print("\nMelhores parâmetros encontrados:")
print(grid.best_params_)

#%%
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

# PREVISÃO
Y_test_predict = grid.predict(X_test)
Y_test_proba = grid.predict_proba(X_test)

# AUC MULTICLASS
auc_test = roc_auc_score(Y_test, Y_test_proba, multi_class="ovr")
print("AUC Teste:", auc_test)

# Treino
Y_train_predict = grid.predict(X_train)
Y_train_proba = grid.predict_proba(X_train)

auc_train = roc_auc_score(Y_train, Y_train_proba, multi_class="ovr")
print("AUC Treino:", auc_train)

# MATRIZ DE CONFUSÃO
print(confusion_matrix(Y_test, Y_test_predict))

# RELATÓRIO
print(classification_report(Y_test, Y_test_predict))