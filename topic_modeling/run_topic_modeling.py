from commons import exec_lda_modeling, exec_dmr_modeling, get_topic_labeler, dmr_topic_scoring
import os
import pandas as pd
import numpy as np

def exec_topic_modeling(datasets_path, target_name, method_name, num_topics):
    preprocessed_path = os.path.join(datasets_path, target_name + '.pkl')
    model_save_path = os.path.join('./models', target_name + '_' + method_name + '.bin')
    topic_keywords_save_path = os.path.join('./results', target_name + '_' + method_name + '_topic_keywords.csv')
    topic_score_save_path = os.path.join('./results', target_name + '_' + method_name + '_topic_score.csv')

    df_datasets = pd.read_pickle(preprocessed_path)
    timestamps = df_datasets['date'].astype(str).values.tolist()
    documents = df_datasets['text'].values.tolist()

    if method_name == 'lda':
        model = exec_lda_modeling(documents, num_topics)
    elif method_name == 'dmr':
        model = exec_dmr_modeling(documents, timestamps, num_topics)
    model.save(model_save_path, True)

    # topic label, keyword
    labeler = get_topic_labeler(model)
    df_topic_keywords = pd.DataFrame(columns=['topic number', 'label', 'keywords'])
    for index, topic_number in enumerate(range(model.k)):
        label = ' '.join(label for label, score in labeler.get_topic_labels(topic_number, top_n=5))
        keywords = ' '.join(keyword for keyword, prob in model.get_topic_words(topic_number))
        df_topic_keywords.loc[index] = [topic_number, label, keywords]
    df_topic_keywords.to_csv(topic_keywords_save_path, encoding='utf-8-sig')

    if method_name == 'dmr':
        df_topic_score = dmr_topic_scoring(model)
        print(df_topic_score)
        df_topic_score.to_csv(topic_score_save_path, encoding='utf-8-sig')

def dmr_topic_scoring(model):
    try:
        # Attempt to convert to list if it behaves like a dict
        column_names = list(model.metadata_dict)
    except TypeError:
        # Fallback if the above conversion does not work
        # You may need to adjust this part based on the actual structure of model.metadata_dict
        column_names = [f"Feature {i}" for i in range(len(model.lambdas[0]))]

    df_topic_score = pd.DataFrame()
    for topic_number in range(model.k):
        print('Topic #{}'.format(topic_number))
        lambdas = model.lambdas[topic_number]
        median_val = np.median(lambdas)
        max_val = np.max(lambdas)
        min_val = np.min(lambdas)
        features = [abs(max_val) + lambdas[i] + abs(median_val) for i in range(len(lambdas))]
        
        # Create a DataFrame for this topic's scores
        temp_df = pd.DataFrame([features], columns=column_names)
        df_topic_score = pd.concat([df_topic_score, temp_df], ignore_index=True)

        print("Median: " + str(median_val) + ", Max: " + str(max_val) + ", Min: " + str(min_val))
        for word, prob in model.get_topic_words(topic_number):
            print('\t', word, prob, sep='\t')

    return df_topic_score

    
if __name__ == '__main__':
    datasets_path = os.path.abspath('../_datasets')
    exec_topic_modeling(datasets_path, 'patent', 'dmr', 12)
