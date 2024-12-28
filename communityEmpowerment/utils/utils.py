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
        # Get the scheme by its unique id
        scheme = Scheme.objects.get(id=scheme_id)

        # Proceed with your recommendation logic using the fetched scheme
        scheme_index = scheme.id  # or any other logic to determine the index

        # Use cosine_sim or any other recommendation logic to get the top_n recommended schemes
        recommended_schemes = []  # Your recommendation logic goes here
        
        # Example: Assuming cosine_sim is a matrix, you can get the top N similar schemes
        # This is just a placeholder for your actual recommendation logic
        top_indices = cosine_sim[scheme_index].argsort()[-top_n:][::-1]  # Example logic for top N recommendations

        for index in top_indices:
            recommended_scheme = Scheme.objects.get(id=index)  # Assuming you can map indices to scheme ids
            recommended_schemes.append(recommended_scheme)

        return recommended_schemes

    except Scheme.DoesNotExist:
        return []  # Return an empty list if the scheme with the given id doesn't exist

