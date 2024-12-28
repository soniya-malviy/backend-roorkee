from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from communityEmpowerment.models import Scheme
import pickle

class Command(BaseCommand):
    help = 'Precompute scheme similarity'

    def handle(self, *args, **kwargs):
        # Fetch all schemes
        schemes = Scheme.objects.all()

        # Combine tags and descriptions for each scheme
        scheme_data = []
        for scheme in schemes:
            print("scheme", scheme)

            tags = " ".join([tag.name for tag in scheme.tags.all()])
            description = scheme.description if scheme.description else ""
            combined = tags + " " + description
            scheme_data.append(combined)
            print("Comb", combined)

        # Use TF-IDF to vectorize the data
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(scheme_data)

        # Compute the cosine similarity matrix

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Save the similarity matrix for later use (e.g., in a pickle file)
        with open('cosine_sim_matrix.pkl', 'wb') as f:
            pickle.dump(cosine_sim, f)

        self.stdout.write(self.style.SUCCESS('Successfully precomputed and saved similarity matrix!'))
