import csv

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load ingredients data to Database"

    def handle(self, *args, **options):
        with open("assets/ingredients.csv", encoding="utf-8") as f:
            file_reader = csv.reader(f)
            for row in file_reader:
                name, unit = row
                try:
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=unit
                    )
                except Exception as exception:
                    return exception
        return _("Data was successfully loaded to the database")
