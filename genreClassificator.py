from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score
from skmultilearn.problem_transform import BinaryRelevance
import pandas
import numpy as np
from collections import Counter

pattern = '(?u)\\b\\w+\\b'

#Hentai, Music, Kids and Dementia were removed from the classifying genres because they lack representation
classifying_genres = ["Comedy", "Action", "Fantasy", "Adventure", "Drama", "Sci-Fi",
                      "Shounen", "Romance", "School", "Supernatural", "Slice of Life"]

def start(c,s):

    classificador = c
        
    data = pandas.read_csv("animeDatabase with LYRICS in ROMAJI CLEAN.csv",encoding='utf-8')
    filtered = data[( data['opening'] != "not applicable")]
    texts = filtered["opening"]
    genres = filtered['Genres']
    genres = [genre.split(',') for genre in genres]
    Y = []
    for i,j in enumerate(genres):
        stripped = [instance.strip() for instance in j if isClassifying(instance.strip()) ]
        if s in stripped:
            Y.append(1)
        else:
            Y.append(0)

    Y = np.array(Y)

    vectorizer = CountVectorizer(ngram_range=(1,1),stop_words=None,token_pattern= pattern)
    X = vectorizer.fit_transform(texts)
    print len(vectorizer.vocabulary_)

    X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size=51, train_size=550, stratify = Y)

    classificador.fit(X_train.toarray(), y_train)
    predicted = classificador.predict(X_test.toarray())
    precision, recall, fscore, support = score(y_test, predicted)
    acc = accuracy_score(y_test, predicted)
    print"\n\n\n****"+s+"****"
    print('Accuracy: {}'.format(acc))
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('fscore: {}'.format(fscore))
    print('support: {}'.format(support))
    show_most_informative_features(vectorizer, classificador, n=20)

def isClassifying(s):
    return s in classifying_genres

def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2)
    print "\n\n\n\n\n\n"


def cleantexts(s):
    return

#classificador = GaussianNB()
#classificador = svm.SVC(kernel='linear')
#classificador = svm.SVC(C = 3.75, gamma = 0.005)
classificador = LogisticRegression()
#classificador = DecisionTreeClassifier()
for s in classifying_genres:
    start(classificador,s)
#plot_confusion_matrix(np.array([[0,9,6],[0,87,6],[0,14,51]]), ['Bully', 'Vitima', 'Relator'])
