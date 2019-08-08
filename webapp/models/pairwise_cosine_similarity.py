from sklearn.metrics.pairwise import cosine_similarity

class pairwise_cosine_similarity:
    def __init__(self):
        print("Initializing pairwise_cosine_similarity")

    @staticmethod
    def recommend(df_data, df_user, top_n):
        print("user informations dataframe")
        print(df_user)
        rec_matrix = cosine_similarity(df_user.copy().drop(['playlist_uri'], axis=1), df_data.playlist_data.copy().drop(['playlist_uri'], axis=1))

        # sort list descending (top similar first)
        rec_index_list = (-rec_matrix[0]).argsort()

        recommendations = []

        if len(rec_index_list) < top_n:
            top_n = len(rec_index_list)

        for k in range(0, top_n):
            recommendations.append(df_data.playlist_names[rec_index_list[k]])

        print('Scores:')
        print(recommendations)
        return recommendations



