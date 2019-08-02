from sklearn.neighbors import NearestNeighbors

class knn_model:
    def __init__(self):
        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)

    def train(self, df_data):
        print("Training model for data size %f" % df_data.playlist_data.size)
        self.model_knn.fit(df_data.playlist_data.copy().drop(['playlist_uri'], axis=1))

    def recommend(self, df_data, df_user):
        distances, indices = self.model_knn.kneighbors(df_user, 10)
        recommendations = []
        for k in indices[0]:
            recommendations.append(df_data.playlist_names[k])

        print('Scores:')
        print(recommendations)
        return recommendations



