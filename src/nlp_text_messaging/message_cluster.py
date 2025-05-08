from bertopic import BERTopic
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


from sklearn.feature_extraction.text import CountVectorizer
from nlp_text_messaging.message_gui import display_messages

from openai import OpenAI
import nltk
from nltk.tokenize import word_tokenize
from sklearn.neighbors import KNeighborsClassifier

from dotenv import load_dotenv

required_resources = ['punkt', 'punkt_tab']

for resource in required_resources:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)
load_dotenv()


def normalize_unix_timestamp(df, column_name):
    # Extract the column
    column_values = df[column_name]
    
    # Min-Max normalization
    min_value = column_values.min()
    df[column_name + '_norm'] = (column_values - min_value)

    return df

def fix_cluster_names(clusters):
    renamed_clusters = []   
    seen = set()
    replace = 0
    for value in clusters:
        if value in seen:
            renamed_clusters.append(replace)
        else:
            seen.add(value)
            replace += 1
            renamed_clusters.append(replace)
    return renamed_clusters

def representative_string(df, topic, max_tokens):
    # Tokenize message_content and count tokens
    df['num_tokens'] = df['message_content'].apply(lambda x: len(word_tokenize(x)))
    
    # Filter based on maximum tokens and highest topic_prob for topic k
    filtered_df  = df[(df['topic'] == topic)]
    filtered_df = filtered_df.sort_values(by='topic_prob', ascending=False)

    accumulated_rows = []
    total_tokens = 0
    for index, row in filtered_df.iterrows():
        tokens_in_row = len(word_tokenize(row['message_content']))
        if total_tokens + tokens_in_row <= max_tokens:
            accumulated_rows.append(row)
            total_tokens += tokens_in_row
        else:
            break
    # print(total_tokens)
    # Remove num_tokens column
        
    new_df = pd.DataFrame(accumulated_rows)
    new_df = new_df.sort_values(by='time_norm')
    concatenated_text = new_df['message_content'].str.cat(sep='\n')

    return concatenated_text



class message_cluster:
    def __init__(self,path, api_key, sep = 1, n_neighbors=3):
        self.path = path
        self.df = pd.read_csv(path,encoding='latin-1')
        self.df = normalize_unix_timestamp(self.df, 'time')
        self.df = self.df.dropna(subset=['message_content'])
        self.generate_topics(sep,n_neighbors)

        self.openai_client = OpenAI(api_key=api_key)

    def generate_topics(self,sep,n_neighbors):
        # concatenate  
        
        # Concatenate near by messages
        times = np.array(self.df['time_norm']).reshape(-1,1)
        distance_threshold =  sep# the amount of seconds in a day
        model = AgglomerativeClustering(n_clusters = None, distance_threshold=distance_threshold, linkage='single')
        clusters = model.fit_predict(times)
        self.df['cluster'] = clusters

        self.clustered_df = self.df.groupby('cluster')['message_content'].apply(lambda x: ' '.join(x)).reset_index()

        # generate topics
        vectorizer_model = CountVectorizer(stop_words="english")
        self.topic_model = BERTopic(vectorizer_model=vectorizer_model)

        docs = self.clustered_df['message_content']
        self.topics, self.probs = self.topic_model.fit_transform(docs)

        self.clustered_df['topic'] = self.topics
        self.clustered_df['prob'] = self.probs

        self.df['topic'] = self.df.apply(
            lambda row: self.clustered_df.loc[row['cluster'] == self.clustered_df['cluster'], 'topic'].values[0] if row['cluster'] in self.clustered_df['cluster'].values else None, axis=1)
        self.df['topic_prob'] = self.df.apply(
            lambda row: self.clustered_df.loc[row['cluster'] == self.clustered_df['cluster'], 'prob'].values[0] if row['cluster'] in self.clustered_df['cluster'].values else None, axis=1)
        temp = self.topic_model.get_topic_info() #['Topic', 'Name']
        self.df = pd.merge(self.df, temp[['Topic', 'Name']], left_on='topic', right_on='Topic',how='left')
        self.df.drop("Topic",axis=1)

        # classify outlier messages
        filtered_df = self.df[self.df['topic'] != -1] #[['time_norm'],['topic']]
        if len(filtered_df) != 0:
            X_train = np.array(filtered_df['time_norm']).reshape(-1, 1)
            y_train = filtered_df['topic']
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            knn.fit(X_train,y_train)
            predicted_topics = knn.predict(self.df.loc[self.df['topic'] == -1, ['time_norm']])
            self.df.loc[self.df['topic'] == -1, 'topic_prob'] = 0
            self.df.loc[self.df['topic'] == -1, 'topic'] = predicted_topics

    def generate_topic_summary(self,topic):
        max_tokens = 9000
        rep_string = representative_string(self.df,topic,max_tokens)

        response = self.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a summarization tool. When given a series of lines breifly explain what the text is about in 5 sentences."},
            {"role": "user", "content": "Text to sumarize: " + rep_string},
        ]
        )

        return response.choices[0].message.content
    def generate_topic_name(self,topic):
        max_tokens = 9000
        rep_string = representative_string(self.df,topic,max_tokens)

        response = self.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a summarization tool. When given a series of lines reply with a short title that summarizes the content."},
            {"role": "user", "content": "Text to sumarize: " + rep_string},
        ]
        )

        return response.choices[0].message.content
# #temp = message_cluster('cap2.csv',5)