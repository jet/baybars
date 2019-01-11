
# 3rd Party
from baybars.timber import get_logger
import numpy as np
import tensorflow as tf 

LABEL_MAP = {
  0: 'T-shirt/top',
  1: 'Trouser',
  2: 'Pullover',
  3: 'Dress',
  4: 'Coat',
  5: 'Sandal',
  6: 'Shirt',
  7: 'Sneaker',
  8: 'Bag',
  9: 'Ankle boot',
}


class UnsupportedModeException(Exception):
  pass


MODEL_DIR = "models/fashion_model"
tf.logging.set_verbosity(tf.logging.INFO)


class FashionMNISTCNN(object):

  def __init__(self, features, labels, mode, batch_size:int =500, num_epochs:int =100, learning_rate:float =0.01, dropout_rate:float=0.4):
    self.features = features 
    self.labels = labels
    self.mode = mode
    self.logger = get_logger(str(self.__class__))
    self.batch_size = batch_size
    self.num_epochs = num_epochs
    self.learning_rate = learning_rate
    self.dropout_rate = dropout_rate
  
  def build_network(self):
    first_convolution_layer = self.cnn_2d_layer_relu(self.input_layer)
    second_convolution_layer = self.cnn_2d_layer_relu(first_convolution_layer)
    first_max_pooling_layer = self.max_pool_2d_layer(second_convolution_layer) 
    third_convolution_layer = self.cnn_2d_layer_relu(first_max_pooling_layer)
    fourth_convolution_layer = self.cnn_2d_layer_relu(third_convolution_layer)
    second_max_pooling_layer = self.max_pool_2d_layer(fourth_convolution_layer)
    reshaped_layer = self.reshape_layer(second_max_pooling_layer)
    first_dense_layer = self.dense_layer(reshaped_layer)
    first_dropout_layer = self.dropout_layer(first_dense_layer)
    second_dense_layer = self.dense_layer(first_dropout_layer)
    second_dropout_layer = self.dropout_layer(second_dense_layer)
    out_layer = self.logit_layer(second_dropout_layer)

    return out_layer

  @property
  def batch_size(self) -> int:
    return self._batch_size

  @batch_size.setter
  def batch_size(self, value) -> None:
    self._batch_size = value
  
  @property
  def num_epochs(self) -> int:
    return self._num_epochs

  @num_epochs.setter
  def num_epochs(self, value) -> None:
    self._num_epochs = value

  @property
  def dropout_rate(self) -> int:
    return self._dropout_rate

  @dropout_rate.setter
  def dropout_rate(self, value) -> None:
    self._dropout_rate = value

  @property
  def is_training(self):
    return self.mode == tf.estimator.ModeKeys.TRAIN 

  @property
  def is_evaluate(self):
    return self.mode == tf.estimator.ModeKeys.EVAL

  @property
  def is_predict(self):
    return self.mode == tf.estimator.ModeKeys.PREDICT
  
  @property
  def one_hot_labels(self):
    return tf.one_hot(indices=tf.cast(self.labels, tf.int32), depth=10)

  def loss(self, layer):
    return tf.losses.softmax_cross_entropy(onehot_labels=self.one_hot_labels, 
                                           logits=layer) 

  @property
  def prediction_structure(self, inputs):
    return {
      "classes": tf.argmax(input=inputs, axis=1),
      "probabilities": tf.nn.softmax(inputs, name="softmax_tensor"),
    }

  def predict(self):
    out = None
    if self.is_predict:
      out_layer = self.build_network()
      out = tf.estimator.EstimatorSpec(mode=self.mode, predictions=self.prediction_structure)

    return out

  def train(self, features=None, labels=None, mode=None):
    out = None
    if self.is_training:
      out_layer = self.build_network()
      loss = self.loss(out_layer)
      optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate)
      train_op = optimizer.minimize(loss=loss,
                                    global_step=tf.train.get_global_step())
      tf.summary.scalar('loss', loss)
      measure = tf.equal(tf.argmax(out_layer, 1), 
                         tf.argmax(self.one_hot_labels, 1))
      accuracy = tf.reduce_mean(tf.cast(measure, tf.float32))
      tf.summary.scalar('accuracy', accuracy)
      out = tf.estimator.EstimatorSpec(mode=self.mode, loss=loss, train_op=train_op)
    
    return out

  def train_model(self, train_data, train_labels, eval_data, eval_labels):
    # Might be better to make these into functions to get the training data and labels
    train_fn = tf.estimator.inputs.numpy_input_fn(x={"x": train_data},
                                                  y=train_labels,
                                                  batch_size=self.batch_size,
                                                  num_epochs=None,
                                                  shuffle=True)

    evaluation_fn = tf.estimator.inputs.numpy_input_fn(x={"x": eval_data},
                                                       y=eval_labels,
                                                       num_epochs=1,
                                                       shuffle=False)
    for ii in range(self.num_epochs):
      self.estimator.train(input_fn=train_fn, steps=100)
      eval_results = self.estimator.evaluate(input_fn=evaluation_fn)
      predictions = list(self.estimator.predict(input_fn=evaluation_fn))
      self.logger.info('epoch={} eval_results={} and predictions={}'.format(ii, eval_results, predictions))

    return self.estimator

  @property
  def estimator(self):
    out = None
    if self.is_training:
      out = tf.estimator.Estimator(model_fn=self.train, model_dir=MODEL_DIR)
    elif self.is_evaluate:
      out = tf.estimator.Estimator(model_fn=self.evaluate, model_dir=MODEL_DIR)
    elif self.is_predict:
      out = tf.estimator.Estimator(model_fn=self.predict, model_dir=MODEL_DIR)
    else:
      raise UnsupportedModeException("Mode: {} is not supported for building estimation".format(self.mode))
      
    return out
  
  def evaluate(self, features=None, labels=None, mode=None):
    out = None 
    if self.is_evaluate:
      out_layer = self.build_network()
      loss = self.loss(out_layer)
      evaluation_metric = {
        "accuracy": tf.metrics.accuracy(labels=self.labels, 
                                        predictions=self.prediction_structure["classes"])
      }
      out = tf.estimator.EstimatorSpec(mode=self.mode, 
                                       loss=loss, 
                                       eval_metric_ops=evaluation_metric)

    return out

  @classmethod
  def activation_layer(cls):
    return tf.nn.relu

  @classmethod
  def dense_layer(cls, inputs):
    return tf.layers.dense(inputs=inputs, 
                           units=128, 
                           activation=cls.activation_layer())

  @property
  def input_layer(self):
    return tf.reshape(self.features, [-1, 28, 28, 1])

  @classmethod
  def cnn_2d_layer_relu(cls, inputs):
    return tf.layers.conv2d(inputs=inputs, 
                            filters=64, 
                            kernel_size=[5, 5], 
                            padding="same", 
                            activation=cls.activation_layer())
  
  @classmethod
  def max_pool_2d_layer(cls, inputs):
    return tf.layers.max_pooling2d(inputs=inputs,
                                   pool_size=[2, 2],
                                   strides=2)
  @classmethod
  def reshape_layer(cls, inputs):
    return tf.reshape(inputs, [-1, 7 * 7 * 64])

  def dropout_layer(self, inputs):
    return tf.layers.dropout(inputs=inputs, rate=self.dropout_rate, training=self.is_training)

  @classmethod
  def logit_layer(cls, inputs):
    return tf.layers.dense(inputs=inputs, units=10)

  @property
  def features(self):
    return self._features

  @features.setter
  def features(self, value):
    self._features = value 

  @property
  def labels(self):
    return self._labels

  @labels.setter
  def labels(self, value):
    self._labels = value 

  @property
  def mode(self):
    return self._mode

  @mode.setter
  def mode(self, value):
    self._mode = value 

 
def _main():
  DATA_DIR = 'data'
  from tensorflow.examples.tutorials.mnist import input_data
  from sklearn.utils import shuffle
  mnist = input_data.read_data_sets(DATA_DIR, one_hot=False, validation_size=0)
  train_data = mnist.train.images  
  print('train data is loaded')
  train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
  print('train labels is loaded')
  train_data, train_labels = shuffle(train_data, train_labels)
  print('eval data is loaded')
  eval_data = mnist.test.images  
  eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)
  eval_data, eval_labels = shuffle(eval_data, eval_labels)
  fashion_mnist_cnn = FashionMNISTCNN(train_data, train_labels, tf.estimator.ModeKeys.TRAIN)
  training = fashion_mnist_cnn.train_model(train_data, train_labels, eval_data, eval_labels)

  return fashion_mnist_cnn, training


if __name__ == '__main__':
  cnn, out = _main()