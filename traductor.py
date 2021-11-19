import numpy as np
from keras_transformer import decode, get_model
import pandas as pd
np.random.seed(0)

# Leer set de entrenamiento
# drive.mount('/content/drive/')
#ruta = '/content/drive/My Drive/ProyectoCurso-GPI/Mapudungun/v2'
# print('%s/mapudungun2.csv'%ruta)
# generar dataset
dataset = pd.read_csv('mapudungun2.csv', sep=';')

dataset.head()

# dataset a lista
dataset_lst = dataset.to_numpy().tolist()
# print(dataset_lst[0])

# Crear "tokens"
#source_tokens = []
# for sentence in dataset_lst[:,0]:
#  source_tokens.append(sentence.split(' '))
# print(source_tokens[0])

#target_tokens = []
# for sentence in dataset_lst[:,1]:
#  target_tokens.append(sentence.split(' '))
# print(target_tokens[0])

source_tokens = []
target_tokens = []

for sentence in dataset_lst:
    source_tokens.append(sentence[0].split(' '))
    target_tokens.append(sentence[1].split(' '))

# print(source_tokens[0])
# print(target_tokens[0])


def build_token_dict(token_list):
    token_dict = {
        '<PAD>': 0,
        '<START>': 1,
        '<END>': 2
    }
    for tokens in token_list:
        for token in tokens:
            if token not in token_dict:
                token_dict[token] = len(token_dict)
    return token_dict


source_token_dict = build_token_dict(source_tokens)
target_token_dict = build_token_dict(target_tokens)
target_token_dict_inv = {v: k for k, v in target_token_dict.items()}


# Agregar start, end y pad a cada frase del set de entrenamiento
encoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in source_tokens]
decoder_tokens = [['<START>'] + tokens + ['<END>'] for tokens in target_tokens]
output_tokens = [tokens + ['<END>'] for tokens in target_tokens]

source_max_len = max(map(len, encoder_tokens))
target_max_len = max(map(len, decoder_tokens))

encoder_tokens = [tokens + ['<PAD>'] *
                  (source_max_len-len(tokens)) for tokens in encoder_tokens]
decoder_tokens = [tokens + ['<PAD>'] *
                  (target_max_len-len(tokens)) for tokens in decoder_tokens]
output_tokens = [tokens + ['<PAD>'] *
                 (target_max_len-len(tokens)) for tokens in output_tokens]


# print(encoder_tokens[120000])


encoder_input = [list(map(lambda x: source_token_dict[x], tokens))
                 for tokens in encoder_tokens]
decoder_input = [list(map(lambda x: target_token_dict[x], tokens))
                 for tokens in decoder_tokens]
output_decoded = [list(map(lambda x: [target_token_dict[x]], tokens))
                  for tokens in output_tokens]

# print(encoder_input[120000])


# Crear la red transformer
model = get_model(
    token_num=max(len(source_token_dict), len(target_token_dict)),
    embed_dim=32,
    encoder_num=2,
    decoder_num=2,
    head_num=4,
    hidden_dim=128,
    dropout_rate=0.05,
    use_same_embed=False,
)
model.compile('adam', 'sparse_categorical_crossentropy')
model.summary()

# cargado
model.load_weights('modelo entrenado.h5')


def translate(sentence):
    sentence_tokens = [tokens + ['<END>', '<PAD>']
                       for tokens in [sentence.split(' ')]]
    # print("source_token_dict:",source_token_dict)

    # esto de aqui esta muy challa por si alguien pudiera mejorar este algoritmo se agradeceria
    # basicamente esto reemplaza las palabras que no conoce el modelo, por espacios en blanco ''
    for idx, tokens in enumerate(sentence_tokens):
        for idy, token in enumerate(tokens):
            if token == '<END>' or token == '<PAD>':
                continue
            elif token not in source_token_dict:
                sentence_tokens[idx][idy] = ''
    #print('sentence_tokens:', sentence_tokens)
    ###########

    tr_input = [list(map(lambda x: source_token_dict[x], tokens))
                for tokens in sentence_tokens][0]
    #print("tr_input:", tr_input)
    decoded = decode(
        model,
        tr_input,
        start_token=target_token_dict['<START>'],
        end_token=target_token_dict['<END>'],
        pad_token=target_token_dict['<PAD>']
    )

    print('Frase original: {}'.format(sentence))
    return '{}'.format(' '.join(map(lambda x: target_token_dict_inv[x], decoded[1:-1])))


'''
while True:
    texto=input()
    translate(texto)
'''
