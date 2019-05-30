import io
import os

import tensorflow as tf

from tensorflow import keras
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


class SimpleWordEmbeddingModel(object):

  def __init__(self, train_data, 
                     train_labels, 
                     test_data, 
                     test_labels,
                     word_index: dict, 
                     embedding_dimension: int=16,
                     vocabulary_size=10000,
                     input_max_length=500,
                     padding='post'):
    self.train_data = train_data
    self.train_labels = train_labels
    self.test_data = test_data
    self.test_labels = test_labels
    self.vocabulary_size = vocabulary_size
    self.input_max_length = input_max_length
    self.padding = padding
    self.embedding_dimension = embedding_dimension
    self.word_index = word_index
    self.reverse_word_index = None 
    self.model = self.build_model() 
    self.history = None

  @property
  def word_index(self):
    return self._word_index 

  @word_index.setter 
  def word_index(self, word_index: dict):
    self._word_index = {key: (value+3) for key, value in word_index.items()}
    self._word_index['<PAD>'] = 0 
    self._word_index['<START>'] = 1
    self._word_index['<UNK>'] = 2
    self._word_index['<UNUSED>'] = 3

  @property
  def reverse_word_index(self):
    return self._reverse_word_index

  @reverse_word_index.setter
  def reverse_word_index(self, value):
    self._reverse_word_index = {value: key for key, value in self.word_index.items()}

  def decode(self, text: str):
    return ' '.join([self.reverse_word_index.get(ii, '?') for ii in text])

  def pad_sequences(self, data, pad_value):
    return keras.preprocessing.sequence.pad_sequences(data,
                                                      value=pad_value,
                                                      padding=self.padding,
                                                      maxlen=self.input_max_length) 

  def build_model(self):
    model = keras.Sequential([
      keras.layers.Embedding(self.vocabulary_size, self.embedding_dimension, input_length=self.input_max_length),
      keras.layers.GlobalAveragePooling1D(),
      keras.layers.Dense(16, activation='relu'),
      keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    return model

  def fit(self):
    if self.history is None:
      self.train_data = self.pad_sequences(self.train_data, self.word_index['<PAD>'])
      self.history = self.build_model()\
                         .fit(self.train_data,
                              self.train_labels,
                              epochs=50,
                              batch_size=512,
                              validation_split=0.2)

    return self.history

  def plot(self):
    history_dict = history.history

    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']

    epochs = range(1, len(acc) + 1)

    plt.figure(figsize=(12,9))
    plt.plot(epochs, loss, label='Training loss')
    plt.plot(epochs, val_loss, label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    plt.figure(figsize=(12,9))
    plt.plot(epochs, acc, label='Training acc')
    plt.plot(epochs, val_acc, label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.ylim((0.5,1))
    plt.show()

  def output_weights(self, directory:str=None) -> None:
    if directory is None:
      directory = os.path.dirname(os.path.realpath(__file__))
    embedding_layer = self.get_embedding_layer() 
    weights = embedding_layer.get_weights()[0]

    with io.open('vecs.tsv', 'w', encoding='utf-8') as out_v, io.open('meta.tsv', 'w', encoding='utf-8') as out_m:
      for word_num in range(vocab_size):
        word = self.reverse_word_index[word_num]
        embeddings = weights[word_num]
        out_m.write(word + "\n")
        out_v.write('\t'.join([str(x) for x in embeddings]) + "\n")

  def get_embedding_layer(self):
    return self.model.layers[0]

  def get_word_embedding(self, word):
    embedding_layer = self.get_embedding_layer()
    weights = embedding_layer.get_weights()[0]
    word_index = self.word_index[word]
    return weights[word_index] 


if __name__ == '__main__':
  vocab_size = 10000
  (train_data, train_labels), (test_data, test_labels) = keras.datasets.imdb.load_data(num_words=vocab_size)
  word_index = keras.datasets.imdb.get_word_index()
  embedding_model = SimpleWordEmbeddingModel(train_data, 
                                             train_labels, 
                                             test_data, 
                                             test_labels, 
                                             word_index, 
                                             embedding_dimension=10, 
                                             vocabulary_size=vocab_size, 
                                             input_max_length=500,
                                             padding='post')
  history = embedding_model.fit()