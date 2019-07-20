import csv
import numpy
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
import pickle

#right_leaning = ['Breitbart', 'National Review', 'New York Post']
right_leaning = ['Breitbart']
left_leaning = ['Vox', 'Buzzfeed News']
data_list = ['all-the-news/articles1_cleaned.csv', 'all-the-news/articles2_cleaned.csv', 'all-the-news/articles3_cleaned.csv']

def load_data():
    left_list_cont = []
    left_list_bias = []
    right_list_cont = []
    right_list_bias = []
    
    for source in data_list: 
        with open(source, encoding='utf8', errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            red_count = 0
            for row in csv_reader:
                #reading only content rows
                if line_count !=0:
                    #checking if source is right leaning
                    if row[0] in right_leaning:
                        right_list_bias.append(1)
                        right_list_cont.append(row[1])
                        red_count += 1
                    #checking if source is left leaning
                    elif row[0] in left_leaning:
                        left_list_bias.append(2)
                        left_list_cont.append(row[1])
                line_count += 1

    print("Right leaning articles: " + str(len(right_list_bias)))
    print("Left leaning articles: " + str(len(left_list_bias)))
    bias_list_train = right_list_bias[:int(len(right_list_bias)*0.8)]
    bias_list_train.extend(left_list_bias[:int(len(left_list_bias)*0.8)])
    content_list_train = right_list_cont[:int(len(right_list_cont)*0.8)]
    content_list_train.extend(left_list_cont[:int(len(left_list_cont)*0.8)])
    bias_list_test = right_list_bias[int(len(right_list_bias)*0.8):]
    bias_list_test.extend(left_list_bias[int(len(left_list_bias)*0.8):])
    content_list_test = right_list_cont[int(len(right_list_cont)*0.8):]
    content_list_test.extend(left_list_cont[int(len(left_list_cont)*0.8):])

    # create the tokenizer from file
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    
    encoded_content_train = tokenizer.texts_to_sequences(content_list_train)
    encoded_content_test = tokenizer.texts_to_sequences(content_list_test)
    bias_list_train = to_categorical(bias_list_train)
    bias_list_test = to_categorical(bias_list_test)
    print(bias_list_test[0])
    #print(encoded_content_train[0])
    #print(type(encoded_content_train))

    content_train = numpy.array(encoded_content_train)
    bias_train = numpy.array(bias_list_train)
    content_test = numpy.array(encoded_content_test)
    bias_test = numpy.array(bias_list_test)
    
    #print(content_train)

    #print(arr)
    #print(type(content_train))
    #print(type(bias_train))
    #print(red_count)
    #print(len(content_train))
    #print(len(bias_train))
    #print(len(content_test))
    #print(len(bias_test))

    return (content_train, bias_train),(content_test,bias_test), tokenizer.num_words 

#load_data()