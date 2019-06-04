import tensorflow_datasets as tfds
import tensorflow as tf

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


class UntrainedModel(Exception):
  pass


class RNNSimpleModel(object):
  def __init__(self, 
               training_data, 
               test_data, 
               tokenizer, 
               embedding_size=64):
    self.tokenizer = tokenizer 
    self.training_data = training_data
    self.test_data = test_data
    self.embedding_size = embedding_size
    self.model = None 

  @classmethod
  def pad_to_size(cls, vec: list, size: int):
    # Get the copy of the list in order not to modify the list that is being passed to 
    out = vec[:] 
    zeros = [0] * (size - len(out))
    out.extend(zeros)
    return out 

  def tokenizer_decode(self, sentence: str):
    return self.tokenizer.decode(sentence)

  def tokenizer_encode(self, sentence: str):
    return self.tokenizer.encode(sentence)

  @property
  def loss_function(self):
    return 'binary_crossentropy'

  @property
  def optimizer(self):
    return 'adam'

  @property
  def metrics(self):
    return ['accuracy']

  def build_model(self):
    model = tf.keras.Sequential([
      tf.keras.layers.Embedding(tokenizer.vocab_size, self.embedding_size),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(self.embedding_size)),
      tf.keras.layers.Dense(self.embedding_size, activation='relu'),
      tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss=self.loss_function,
                  optimizer=self.optimizer
                  metrics=self.metrics)

    return model

  def fit(self, epochs: int = 10):
    # Initialize the model in here in order to reuse
    self.model = self.build_model()
    return self.model\
               .fit(train_dataset, 
                    epochs=epochs,
                    validation_data=self.test_data)

  def evaluate(self):
    return self.model.evaluate(self.test_data)
  
  def predict(self, sentence: str, pad_size=64):
    if self.model is None:
      raise UntrainedModel("Model is not trained!")

    tokenized_sample_pred_text = self.tokenizer.encode(sentence)

    if pad_size is not None:
      tokenized_sample_pred_text = self.pad_to_size(tokenized_sample_pred_text, pad_size)

    return self.model.predict(tf.expand_dims(tokenized_sample_pred_text, 0))


class RNNBLSTMModel(RNNSimpleModel):
  def __init__(self, 
               training_data, 
               test_data, 
               tokenizer, 
               embedding_size=64):
    super().__init__(training_data, 
                     test_data, 
                     tokenizer, 
                     embedding_size=embedding_size)

  def build_model(self):
    half_embedding_size = self.embedding_size / 2
    model = tf.keras.Sequential([
      tf.keras.layers.Embedding(tokenizer.vocab_size, self.embedding_size),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(self.embedding_size, 
                                                         return_sequences=True)),
      tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(half_embedding_size)),
      tf.keras.layers.Dense(self.embedding_size, activation='relu'),
      tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss=self.loss_function,
                  optimizer=self.optimizer,
                  metrics=self.metrics)

    return model


if __name__ == '__main__':
  def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_{}'.format(string)])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_{}'.format(string)])
    plt.show()

  PAD_SIZE = 64
  EMBEDDING_SIZE = 64
  EPOCHS = 10
  BUFFER_SIZE = 10000
  BATCH_SIZE = 64

  dataset, info = tfds.load('imdb_reviews/subwords8k', 
                            with_info=True, 
                            as_supervised=True)
  train_dataset, test_dataset = dataset['train'], dataset['test']

  tokenizer = info.features['text'].encoder

  print('Vocabulary size: {}'.format(tokenizer.vocab_size))

  train_dataset = train_dataset.shuffle(BUFFER_SIZE)
  train_dataset = train_dataset.padded_batch(BATCH_SIZE, train_dataset.output_shapes)
  test_dataset = test_dataset.padded_batch(BATCH_SIZE, test_dataset.output_shapes)

  rnn_simple_model = RNNSimpleModel(train_dataset, 
                                    test_dataset, 
                                    tokenizer, 
                                    embedding_size=EMBEDDING_SIZE)

  history = rnn_simple_model.fit(epochs=EPOCHS)

  test_loss, test_acc = rnn_simple_model.evaluate()

  print('Test Loss: {}'.format(test_loss))
  print('Test Accuracy: {}'.format(test_acc))

  # predict on a sample text without padding.
  sample_pred_text = ('The movie was cool. The animation and the graphics '
                      'were out of this world. I would recommend this movie.')
  print('Predictions without padding={}'.format(rnn_simple_model.predict(sample_pred_text)))

  print('Predictions with padding={}'.format(rnn_simple_model.predict(sample_pred_text, 
                                                                      pad_size=PAD_SIZE)))

  plot_graphs(history, 'loss')
  plot_graphs(history, 'accuracy')

  rnn_blstm_model = RNNBLSTMModel(train_dataset, 
                                  test_dataset, 
                                  tokenizer, 
                                  embedding_size=EMBEDDING_SIZE)

  history = rnn_blstm_model.fit(epochs=EPOCHS)

  test_loss, test_acc = rnn_blstm_model.evaluate()

  print('Test Loss: {}'.format(test_loss))
  print('Test Accuracy: {}'.format(test_acc))

  # predict on a sample text without padding.
  sample_pred_text = ('The movie was not good. The animation and the graphics '
                      'were terrible. I would not recommend this movie.')
  print('Predictions without padding={}'.format(rnn_blstm_model.predict(sample_pred_text)))

  # predict on a sample text with padding
  print('Predictions with padding={}'.format(rnn_blstm_model.predict(rnn_blstm_model.predict(sample_pred_text), 
                                                                     pad_size=PAD_SIZE)))

  plot_graphs(history, 'loss')
  plot_graphs(history, 'accuracy')
