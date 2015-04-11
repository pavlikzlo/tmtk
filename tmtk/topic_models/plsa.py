import numpy as np

from utils import get_topic
from tmtk.utils.math import norn_mtx

from tmtk.collection.collection import bag_of_words

from tmtk.metrics.utils import estimate_teta_full

def plsa_model(train, test, wrd_count, num_topics=100, num_iter=10, metrics=None, verbose=False, F=None):
    bw_train, bw_test = bag_of_words(train), bag_of_words(test)

    doc_count = len(bw_train)

    if not F:
        F, T = norn_mtx(wrd_count, num_topics, axis='x'), norn_mtx(num_topics, doc_count, axis='y')
    else:
        T = estimate_teta_full(F, bw_train)

    for itter in xrange(num_iter):
        Nwt, Ntd = np.zeros((wrd_count, num_topics)), np.zeros((num_topics, doc_count))
        Nt, Nd = np.zeros(num_topics), np.zeros(doc_count)

        for d in xrange(doc_count):
            for w, ndw in bw_train[d]:
                ndwt = F[w, :] * T[:, d]
                ndwt *= ndw * (1.0 / ndwt.sum())

                Nwt[w] += ndwt
                Ntd[:, d] += ndwt
                Nt += ndwt
                Nd[d] += ndwt.sum()

        for w in xrange(wrd_count):
            F[w] = Nwt[w] / Nt

        for t in range(num_topics):
            T[t] = Ntd[t] / Nd

        print itter

        if metrics and verbose and itter % 2 == 1:
            metric_val = [metric(F, train, test) for metric in metrics]
            print 'iter %s: %s' % (str(itter).zfill(2), ' '.join(metric_val))

    if metrics:
        metric_val = [metric(F, train, test) for metric in metrics]
        print 'end: %s' % ' '.join(metric_val)

    return F, T

def print_topics(F, id_to_wrd, top=9):
    for i in xrange(F.shape[1]):
        print 'Topic %s: ' % i + ' '.join(map(lambda x: id_to_wrd[x], get_topic(F, i, top)))