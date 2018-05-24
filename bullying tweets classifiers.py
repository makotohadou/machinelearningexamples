import pandas
import numpy as np
import sys,time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from nltk.corpus import stopwords
from matplotlib import pyplot as plt


####### PARAMETERS #######

grams_inicio = 1
grams_fim = 2

sws = stopwords.words('portuguese')
pattern = '(?u)\\b\\w+\\b'


def start(c):
    resultSet = []
    data = pandas.read_csv("finalFileWholeDataset.csv",encoding='utf-8')
    #filtered = data[( data['Papel(vitima, bully ou relator)'] != "n/a")]
    #texts = filtered["Texto"]
    texts = data["Texto"]
    #Y = filtered['Papel(vitima, bully ou relator)']
    Y = data['Bullying?(Sim ou Nao)']
    print Y.unique()


    vectorizer = CountVectorizer(ngram_range=(grams_inicio,grams_fim),stop_words=None,token_pattern= pattern)
    X = vectorizer.fit_transform(texts)
    print len(vectorizer.vocabulary_)


    final_precision = 0
    final_recall = 0
    final_fscore = 0
    final_acc = 0
    final_support = 0
    
    classificador = c
    
    for a in range(0,30):

        
        X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size=300, train_size=1700, stratify=Y)
        print X_train.shape[0],X_train.shape[1]

        
        classificador.fit(X_train.toarray(), y_train)
        predicted = classificador.predict(X_test.toarray())
        precision, recall, fscore, support = score(y_test, predicted)
        final_acc += accuracy_score(y_test, predicted)
        final_precision+=precision
        final_recall+=recall
        final_fscore+=fscore
        final_support+=support
    
    print('Accuracy: {}'.format(final_acc/30))
    print('precision: {}'.format(final_precision/30))
    print('recall: {}'.format(final_recall/30))
    print('fscore: {}'.format(final_fscore/30))
    print('support: {}'.format(final_support/30))




def plot_confusion_matrix(cm, target_names, title='Matriz de Confusao', cmap=plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()

    width, height = cm.shape

    for x in xrange(width):
        for y in xrange(height):
            plt.annotate(str(cm[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')
    plt.ylabel('Classe Real')
    plt.xlabel('Classe Prevista')
    plt.show()

#classificador = GaussianNB()
#classificador = svm.SVC(kernel='linear')
classificador = svm.SVC(C = 3.75, gamma = 0.005)
#classificador = LogisticRegression()
start(classificador)
#plot_confusion_matrix(np.array([[0,9,6],[0,87,6],[0,14,51]]), ['Bully', 'Vitima', 'Relator'])
