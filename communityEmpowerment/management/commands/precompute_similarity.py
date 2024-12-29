from django.core.management.base import BaseCommand
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from communityEmpowerment.models import Scheme
import pickle

class Command(BaseCommand):
    help = 'Precompute scheme similarity'

    def handle(self, *args, **kwargs):
        schemes = Scheme.objects.all()

        scheme_data = []
        for scheme in schemes:
            tags = " ".join([tag.name for tag in scheme.tags.all()])
            description = scheme.description if scheme.description else ""
            combined = tags + " " + description
            scheme_data.append(combined)

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(scheme_data)

        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        with open('cosine_sim_matrix.pkl', 'wb') as f:
            pickle.dump(cosine_sim, f)

        self.stdout.write(self.style.SUCCESS('Successfully precomputed and saved similarity matrix!'))
