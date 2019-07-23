from sklearn.neighbors import NearestNeighbors

class knn_model:
    def __init__(self):
        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)

    def train_and_recommend(self, df_data, df_user):
        print("Training model for data size %f" % df_data.playlist_data.size)
        print(df_data.playlist_data.head(10))
        self.model_knn.fit(df_data.playlist_data.drop(['playlist_uri'], axis=1))
        distances, indices = self.model_knn.kneighbors(df_user, 10)
        recommendations = []
        for k in indices[0]:
            recommendations.append(df_data.playlist_names[k])
            print(df_data.playlist_names[k])
        return recommendations


