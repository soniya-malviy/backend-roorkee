import pickle
from communityEmpowerment.models import Scheme, UserInteraction
import os
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
import numpy as np
import pandas as pd

def load_cosine_similarity():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cosine_sim_path = os.path.join(base_dir,'..','..', 'cosine_sim_matrix.pkl')

    with open(cosine_sim_path, 'rb') as f:
        return pickle.load(f)

def recommend_schemes(scheme_id, cosine_sim, top_n=5):
    try:
        scheme = Scheme.objects.get(id=scheme_id)
        scheme_index = scheme.id

        recommended_schemes = [] 
        
        top_indices = cosine_sim[scheme_index].argsort()[-top_n:][::-1]

        for index in top_indices:
            recommended_scheme = Scheme.objects.get(id=index)
            recommended_schemes.append(recommended_scheme)

        return recommended_schemes

    except Scheme.DoesNotExist:
        return []


def collaborative_recommendations(user_id, top_n=5):
    # Fetch user-scheme interactions
    interactions = UserInteraction.objects.values('user_id', 'scheme_id', 'interaction_value')
    
    if not interactions:
        return []  # Return empty if no interactions exist

    # Create a DataFrame
    df = pd.DataFrame(interactions)

    # Map user and scheme IDs to categorical indices
    user_categories = df['user_id'].astype('category')
    scheme_categories = df['scheme_id'].astype('category')
    user_ids = user_categories.cat.codes
    scheme_ids = scheme_categories.cat.codes

    # Create User-Scheme Interaction Matrix
    interaction_matrix = csr_matrix((df['interaction_value'], (user_ids, scheme_ids)))

    num_schemes = interaction_matrix.shape[1]
    n_components = min(50, num_schemes) 

    # Perform SVD
    svd = TruncatedSVD(n_components=n_components)  # Reduce dimensionality
    latent_matrix = svd.fit_transform(interaction_matrix)

    # Get the user's latent vector
    try:
        user_idx = user_categories.cat.categories.get_loc(user_id)
    except KeyError:
        return []  # Return empty if user_id is not found in the dataset

    user_vector = latent_matrix[user_idx]

    # Compute similarity scores for schemes
    scheme_latent_matrix = latent_matrix.T  # Transpose to align with schemes
    scores = scheme_latent_matrix.T.dot(user_vector)

    # Get top N recommended scheme indices
    recommended_indices = np.argsort(scores)[-top_n:][::-1]

    # Map indices back to scheme IDs
    scheme_ids = scheme_categories.cat.categories
    recommended_scheme_ids = [scheme_ids[idx] for idx in recommended_indices]

    # Fetch Scheme objects for recommendations
    return list(Scheme.objects.filter(id__in=recommended_scheme_ids))