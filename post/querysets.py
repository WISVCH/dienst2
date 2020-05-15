from django.db.models import QuerySet, Count


class ItemQuerySet(QuerySet):
    def group_by_description(self):
        return self.values("description").annotate(Count("id")).order_by("description")
