import pickle
from communityEmpowerment.models import Scheme
import os

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

