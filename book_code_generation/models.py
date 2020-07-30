import unidecode as unidecode
from django.db import models

# Create your models here.

import re
import unicodedata


class BookCode(models.Model):
    class Meta:
        abstract = True
    location_part = models.CharField(max_length=8)  # Where in the library is it?
    grouping_part = models.CharField(max_length=8)  # in most cases, this is the author
    identifying_part = models.CharField(max_length=12)  # which object is it?
    full_string = models.CharField(max_length=64)

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """

    return unidecode.unidecode(text)


class CutterCodeRange(models.Model):
    from_affix = models.CharField(max_length=16)
    to_affix = models.CharField(max_length=16)
    number = models.CharField(max_length=16)
    generated_affix = models.CharField(max_length=20)

    @staticmethod
    def get_cutter_number(name: str):
        cutters = CutterCodeRange.objects.all().order_by("from_affix")
        result = None
        for cutter in cutters:
            if result is None:
                result = cutter
            if strip_accents(name.upper()) < cutter.from_affix:
                return result
            result = cutter
        return result


def generate_code_from_author(item):
    pub = item.publication
    auth = pub.get_authors()
    if len(auth) > 0:
        author = auth[0].creator.name
        return item.location.category.code + "-" + CutterCodeRange.get_cutter_number(author).generated_affix + "-"
    else:
        pass


def generate_code_from_author_translated(item):
    pub = item.publication
    prefix = "N"
    if pub.is_translated:
        prefix = "V"
    auth = item.publication.get_authors()
    if len(auth) > 0:
        author = auth[0].creator.name
        return prefix + "-" + CutterCodeRange.get_cutter_number(author).generated_affix + "-"
    else:
        pass


def generate_code_from_title(item):
    title = item.publication.title[0:4]
    if item.location.category.code == "":
        return title + "-"
    else:
        return item.location.category.code + "-" + title + "-"
