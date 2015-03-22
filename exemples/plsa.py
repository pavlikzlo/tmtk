from tmtk.topic_models import plsa

from tmtk.metrics.metrics import preplexity
from tmtk.collection.collection import BagOfWordsCollections

collection_train = BagOfWordsCollections(
    path='/home/oem/Dropbox/projests/Python/tmtk/tmtk/corpa/bag_of_words/nips',
    name='nips_train'
).fill()

collection_test = BagOfWordsCollections(
    path='/home/oem/Dropbox/projests/Python/tmtk/tmtk/corpa/bag_of_words/nips',
    name='nips_test'
).fill()

F, T = plsa.plsa_model(collection_train.documents, collection_test.documents, metric=preplexity, num_iter=40)
#plsa.print_topics(F, collection_train.id_to_words)
