from django.core.management.base import BaseCommand
from communityEmpowerment.models import Tag

class Command(BaseCommand):
    help = "Categorize existing tags into SC, ST, OBC, and Minority"

    def handle(self, *args, **kwargs):
        sc_keywords = ["sc", "scheduled caste"]
        st_keywords = ["st", "scheduled tribe"]
        obc_keywords = ["obc", "other backward classes"]
        minority_keywords = ["minority", "muslim", "christian", "sikh", "buddhist", "jain", "parsi"]

        for tag in Tag.objects.all():
            tag_lower = tag.name.lower()

            if any(keyword in tag_lower for keyword in sc_keywords):
                tag.category = "sc"
            elif any(keyword in tag_lower for keyword in st_keywords):
                tag.category = "st"
            elif any(keyword in tag_lower for keyword in obc_keywords):
                tag.category = "obc"
            elif any(keyword in tag_lower for keyword in minority_keywords):
                tag.category = "minority"
            else:
                tag.category = "general"

            tag.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated all tags with correct categories!"))
