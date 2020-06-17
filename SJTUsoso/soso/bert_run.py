import tensorflow as tf
import sys
import os
sys.path.append('../bert-utils-master/')
import similar as sml


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.logging.set_verbosity(tf.logging.ERROR)
sim = sml.BertSim()
print("Model Loaded")
sim.set_mode(tf.estimator.ModeKeys.PREDICT)


def get_similarity(qry, con):
    predict = sim.predict(qry, con)
    sml = int(predict[0][1] * 1000)
    print(con, sml)
    return sml
