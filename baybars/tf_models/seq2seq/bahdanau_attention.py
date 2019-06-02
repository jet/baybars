
import unicodedata
import re
import numpy as np
import os
import io
import time

# 3rd Party Dependencies
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
plt.style.use('fivethirtyeight')


class Decoder(tf.keras.Model):
  def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
    super(Decoder, self).__init__()
    self.batch_sz = batch_sz
    self.dec_units = dec_units
    self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
    self.gru = tf.keras.layers.GRU(self.dec_units,
                                   return_sequences=True,
                                   return_state=True,
                                   recurrent_initializer='glorot_uniform')
    self.fc = tf.keras.layers.Dense(vocab_size)

    # used for attention
    self.attention = BahdanauAttention(self.dec_units)

  def call(self, x, hidden, enc_output):
    # enc_output shape == (batch_size, max_length, hidden_size)
    context_vector, attention_weights = self.attention(hidden, enc_output)

    # x shape after passing through embedding == (batch_size, 1, embedding_dim)
    x = self.embedding(x)

    # x shape after concatenation == (batch_size, 1, embedding_dim + hidden_size)
    x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=-1)

    # passing the concatenated vector to the GRU
    output, state = self.gru(x)

    # output shape == (batch_size * 1, hidden_size)
    output = tf.reshape(output, (-1, output.shape[2]))

    # output shape == (batch_size, vocab)
    x = self.fc(output)

    return x, state, attention_weights


class Encoder(tf.keras.Model):
  def __init__(self, vocab_size, embedding_dim, enc_units, batch_sz):
    super(Encoder, self).__init__()
    self.batch_sz = batch_sz
    self.enc_units = enc_units
    self.embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)
    self.gru = tf.keras.layers.GRU(self.enc_units,
                                   return_sequences=True,
                                   return_state=True,
                                   recurrent_initializer='glorot_uniform')

  def call(self, x, hidden):
    x = self.embedding(x)
    output, state = self.gru(x, initial_state = hidden)
    return output, state

  def initialize_hidden_state(self):
    return tf.zeros((self.batch_sz, self.enc_units))


class BahdanauAttention(tf.keras.Model):
  def __init__(self, units):
    super(BahdanauAttention, self).__init__()
    self.W1 = tf.keras.layers.Dense(units)
    self.W2 = tf.keras.layers.Dense(units)
    self.V = tf.keras.layers.Dense(1)

  def call(self, query, values):
    # hidden shape == (batch_size, hidden size)
    # hidden_with_time_axis shape == (batch_size, 1, hidden size)
    # we are doing this to perform addition to calculate the score
    hidden_with_time_axis = tf.expand_dims(query, 1)

    # score shape == (batch_size, max_length, hidden_size)
    score = self.V(tf.nn.tanh(
        self.W1(values) + self.W2(hidden_with_time_axis)))

    # attention_weights shape == (batch_size, max_length, 1)
    # we get 1 at the last axis because we are applying score to self.V
    attention_weights = tf.nn.softmax(score, axis=1)

    # context_vector shape after sum == (batch_size, hidden_size)
    context_vector = attention_weights * values
    context_vector = tf.reduce_sum(context_vector, axis=1)

    return context_vector, attention_weights


class BahdanauAttentionRunner(object):

  def __init__(self):
    pass

  @classmethod
  def unicode_to_ascii(cls, s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

  @classmethod 
  def preprocess_sentence(cls, w: str):
    w = cls.unicode_to_ascii(w.lower().strip())
    w = re.sub(r"([?.!,¿])", r" \1 ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
    w = w.rstrip().strip()
    w = '<start> ' + w + ' <end>'
    return w
  
  @classmethod
  def create_dataset(cls, path: str, num_examples: int) -> list:
    lines = io.open(path, encoding='UTF-8').read().strip().split('\n')

    word_pairs = [[cls.preprocess_sentence(w) for w in l.split('\t')]  
                  for l in lines[:num_examples]]

    return zip(*word_pairs)

  @classmethod
  def max_length(cls, tensor):
    return max(len(t) for t in tensor)

  @classmethod
  def tokenize(cls, lang):
    lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
    lang_tokenizer.fit_on_texts(lang)
    tensor = lang_tokenizer.texts_to_sequences(lang)
    tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor, padding='post')

    return tensor, lang_tokenizer

  @classmethod
  def load_dataset(cls, path, num_examples=None):
    # creating cleaned input, output pairs
    targ_lang, inp_lang = cls.create_dataset(path, num_examples)

    input_tensor, inp_lang_tokenizer = cls.tokenize(inp_lang)
    target_tensor, targ_lang_tokenizer = cls.tokenize(targ_lang)

    return input_tensor, target_tensor, inp_lang_tokenizer, targ_lang_tokenizer


if __name__ == '__main__':
  runner = BahdanauAttentionRunner()
  # Download the file
  path_to_zip = tf.keras.utils.get_file(
    'spa-eng.zip', origin='http://storage.googleapis.com/download.tensorflow.org/data/spa-eng.zip',
    extract=True)

  path_to_file = os.path.dirname(path_to_zip)+"/spa-eng/spa.txt"

  en, sp = BahdanauAttentionRunner.create_dataset(path_to_file, None)
  print(en[-1])
  print(sp[-1])

  # Try experimenting with the size of that dataset
  num_examples = 30000
  input_tensor, target_tensor, inp_lang, targ_lang = BahdanauAttentionRunner.load_dataset(path_to_file, num_examples)

  # Calculate max_length of the target tensors
  max_length_targ, max_length_inp = BahdanauAttentionRunner.max_length(target_tensor), BahdanauAttentionRunner.max_length(input_tensor)

  # Creating training and validation sets using an 80-20 split
  input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(input_tensor, target_tensor, test_size=0.2)

  # Show length
  len(input_tensor_train), len(target_tensor_train), len(input_tensor_val), len(target_tensor_val)

  def convert(lang, tensor):
    for t in tensor:
      if t!=0:
        print ("%d ----> %s" % (t, lang.index_word[t]))
  
  print ("Input Language; index to word mapping")
  convert(inp_lang, input_tensor_train[0])
  print ()
  print ("Target Language; index to word mapping")
  convert(targ_lang, target_tensor_train[0])

  BUFFER_SIZE = len(input_tensor_train)
  BATCH_SIZE = 64
  steps_per_epoch = len(input_tensor_train)//BATCH_SIZE
  embedding_dim = 256
  units = 1024
  vocab_inp_size = len(inp_lang.word_index)+1
  vocab_tar_size = len(targ_lang.word_index)+1

  dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)).shuffle(BUFFER_SIZE)
  dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

  example_input_batch, example_target_batch = next(iter(dataset))
  example_input_batch.shape, example_target_batch.shape

  encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)

  # sample input
  sample_hidden = encoder.initialize_hidden_state()
  sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
  print ('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))
  print ('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))

  attention_layer = BahdanauAttention(10)
  attention_result, attention_weights = attention_layer(sample_hidden, sample_output)

  print("Attention result shape: (batch size, units) {}".format(attention_result.shape))
  print("Attention weights shape: (batch_size, sequence_length, 1) {}".format(attention_weights.shape))

  decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)

  sample_decoder_output, _, _ = decoder(tf.random.uniform((64, 1)),
                                      sample_hidden, sample_output)

  print ('Decoder output shape: (batch_size, vocab size) {}'.format(sample_decoder_output.shape))

  optimizer = tf.keras.optimizers.Adam()
  
  loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')

  def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_object(real, pred)

    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask

    return tf.reduce_mean(loss_)

  checkpoint_dir = './training_checkpoints'
  checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
  checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                   encoder=encoder,
                                   decoder=decoder)

  checkpoint_dir = './training_checkpoints'
  checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
  checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                   encoder=encoder,
                                   decoder=decoder)

                        

  @tf.function
  def train_step(inp, targ, enc_hidden):
    loss = 0

    with tf.GradientTape() as tape:
      enc_output, enc_hidden = encoder(inp, enc_hidden)

      dec_hidden = enc_hidden

      dec_input = tf.expand_dims([targ_lang.word_index['<start>']] * BATCH_SIZE, 1)

      # Teacher forcing - feeding the target as the next input
      for t in range(1, targ.shape[1]):
        # passing enc_output to the decoder
        predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)

        loss += loss_function(targ[:, t], predictions)

        # using teacher forcing
        dec_input = tf.expand_dims(targ[:, t], 1)

    batch_loss = (loss / int(targ.shape[1]))

    variables = encoder.trainable_variables + decoder.trainable_variables

    gradients = tape.gradient(loss, variables)

    optimizer.apply_gradients(zip(gradients, variables))

    return batch_loss

  EPOCHS = 10

  for epoch in range(EPOCHS):
    start = time.time()

    enc_hidden = encoder.initialize_hidden_state()
    total_loss = 0

    for (batch, (inp, targ)) in enumerate(dataset.take(steps_per_epoch)):
      batch_loss = train_step(inp, targ, enc_hidden)
      total_loss += batch_loss

      if batch % 100 == 0:
          print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                      batch,
                                                      batch_loss.numpy()))
    # saving (checkpoint) the model every 2 epochs
    if (epoch + 1) % 2 == 0:
      checkpoint.save(file_prefix = checkpoint_prefix)

    print('Epoch {} Loss {:.4f}'.format(epoch + 1,
                                        total_loss / steps_per_epoch))
    print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))