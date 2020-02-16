from django.db import models

# Create your models here.
from django.db.models import PROTECT


class Work(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    language = models.CharField(max_length=64)
    is_translated = models.BooleanField()
    original_title =  models.CharField(max_length=255)
    original_subtitle =  models.CharField(max_length=255)
    original_language = models.CharField(max_length=64)
    hidden = models.BooleanField()
    date_added = models.DateField()
    comment = models.CharField(max_length=1024)
    internal_comment = models.CharField(max_length=1024)
    signature_fragment = models.CharField(max_length=64)
    old_id = models.IntegerField(blank=True, null=True)  # The ID of the same thing, in the old system.


class Publication(Work):
    def is_simple_publication(self):
        return len(self.workinpublication_set) == 0


class Item(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    publication = models.ForeignKey(Publication, on_delete=PROTECT)
    sticker_code = models.CharField(max_length=64)


class SubWork(Work):
    def is_orphaned(self):
        return len(self.workinpublication_set) == 0

    def is_part_of_multiple(self):
        return len(self.workinpublication_set) > 1


class WorkInPublication(models.Model):
    publication = models.ForeignKey(Publication, on_delete=PROTECT)
    work = models.ForeignKey(SubWork, on_delete=PROTECT)
    number_in_publication = models.IntegerField()
    display_number_in_publication = models.CharField(max_length=64)


class Creator(models.Model):
    name = models.CharField(max_length=255)


class CreatorRole(models.Model):
    name = models.CharField(max_length=64, unique=True)


class CreatorToWork(models.Model):
    creator = models.ForeignKey(Creator, on_delete=PROTECT)
    work = models.ForeignKey(Work, on_delete=PROTECT)
    role = models.ForeignKey(CreatorRole, on_delete=PROTECT)
