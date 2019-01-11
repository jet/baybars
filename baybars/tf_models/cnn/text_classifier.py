
import tensorflow as tf


# Some constants.
MIN_PROB = 1e-10
MAX_PROB = 1.0
CONV_STRIDS = [1, 1, 1, 1]
POOL_STRIDS = [1, 1, 1, 1]
PADDING = 'VALID'


class TextClassifier:
    def __init__(self, sequence_len: int, label_set_size: int, vocab_size: int, 
                 embedding_dim: int, num_filters: int, filter_sizes: list,
                 keep_prob: float, beta: float, dtype: tf.DType=tf.float32):
        self.sequence_len = sequence_len
        self.label_set_size = label_set_size
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.num_filters = num_filters
        self.filter_sizes = filter_sizes
        self.keep_prob = keep_prob
        self.beta = beta
        self.dtype = dtype

        with tf.variable_scope('Embedding', reuse=tf.AUTO_REUSE):
            tf.get_variable('E',
                            [self.vocab_size, self.embedding_dim],
                            dtype=self.dtype)

        for i, filter_size in enumerate(self.filter_sizes):
            with tf.variable_scope('ConvPool-{}'.format(filter_size), reuse=tf.AUTO_REUSE):
                tf.get_variable('W',
                                [filter_size, self.embedding_dim, 1, self.num_filters],
                                dtype=self.dtype,
                                initializer=tf.truncated_normal_initializer(.0, .1))

                tf.get_variable('b',
                                [self.num_filters],
                                dtype=self.dtype,
                                initializer=tf.constant_initializer(.1))

        with tf.variable_scope('Proj', reuse=tf.AUTO_REUSE):
            tf.get_variable('W',
                            [len(self.filter_sizes) * self.num_filters, self.label_set_size],
                            dtype=self.dtype,
                            initializer=tf.truncated_normal_initializer(.0, .1))

            tf.get_variable('b',
                            [self.label_set_size],
                            self.dtype,
                            initializer=tf.constant_initializer(.1))

    def embed(self, sequence):
      with tf.variable_scope('Embedding', reuse=tf.AUTO_REUSE):
        embeddings = tf.nn.embedding_lookup(self.get('E'), sequence)
      return embeddings

    def conv(self, embeddings):
      embeddings = tf.expand_dims(embeddings, -1)

      features = []
      for i, filter_size in enumerate(self.filter_sizes):
        with tf.variable_scope('ConvPool-{}'.format(filter_size), reuse=tf.AUTO_REUSE):
          conved = tf.nn.conv2d(embeddings,
                                self.get('W'),
                                strides=CONV_STRIDS,
                                padding=PADDING)

          conved = tf.nn.relu(tf.nn.bias_add(conved, self.get('b')))

          pooled = tf.nn.max_pool(conved,
                                  [1, self.sequence_len - filter_size + 1, 1, 1],
                                  strides=POOL_STRIDS,
                                  padding=PADDING)

          features.append(pooled)

      return tf.squeeze(tf.concat(features, 3), axis=[1, 2])

    def proj(self, feature_vec):
      with tf.variable_scope('Proj', reuse=tf.AUTO_REUSE):
        logits = tf.matmul(feature_vec, self.get('W')) + self.get('b')
      return logits

    def get(self, variable_name: str, *args, **kwargs):
      return tf.get_variable(variable_name, *args, **kwargs)

    def predict(self, sequence, training):
      feature_vec = self.conv(self.embed(sequence))

      if training:
        feature_vec = tf.nn.dropout(feature_vec, self.keep_prob)

      logits = self.proj(feature_vec)
      probs = tf.nn.softmax(logits)
      return logits, probs

    def forward(self, sequence, target_vec, training=True):
      logits, probs = self.predict(sequence, training)

      cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits,
                                                                  labels=target_vec)

      if self.beta > 0:
        log_probs = tf.log(tf.clip_by_value(probs, MIN_PROB, MAX_PROB))
        entropy = -tf.reduce_sum(probs * log_probs, axis=[1])
        cross_entropy = cross_entropy - self.beta * entropy

      return probs, tf.reduce_mean(cross_entropy)
