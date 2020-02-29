import datetime

import mysql.connector

from django.core.management.base import BaseCommand, CommandError

from bellettrie_library_system.settings import OLD_DB
from series.models import Series, WorkInSeries, SeriesNode, CreatorToSeries
from works.models import Work, WorkInPublication, Publication, SubWork, Creator, CreatorRole, CreatorToWork


def get_name(x):
    vn = x.get("voornaam")
    if len(vn) == 0:
        return x.get("naam")
    return vn + " " + x.get("naam")


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    @staticmethod
    def handle_author(publication, tree, finder):
        data = finder.get(publication)

    @staticmethod
    def handle_matching(sub_work, tree, finder):
        data = finder.get(sub_work)

    def handle(self, *args, **options):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database=OLD_DB
        )
        mycursor = mydb.cursor(dictionary=True)

        mycursor.execute("SELECT * FROM betrokkenheid")

        links = dict()
        list = []
        for x in mycursor:
            creator_role, updated = CreatorRole.objects.get_or_create(name=x.get("rol"))
            links[x.get("rol")] = creator_role
            list.append(x)

        print(links)

        for x in list:
            if len(Creator.objects.filter(old_id=x.get("persoonnummer")))> 0:
                a = Creator.objects.get(old_id=x.get("persoonnummer"))
                if len(Work.objects.filter(old_id=x.get("publicatienummer"))) > 0:
                    w = Work.objects.get(old_id=x.get("publicatienummer"))
                    role = links.get(x.get("rol"))
                    CreatorToWork.objects.get_or_create(work=w, creator=a, role=role)
                else:
                    if len(Series.objects.filter(old_id=x.get("publicatienummer"))) > 0:
                        w = Series.objects.get(old_id=x.get("publicatienummer"))

                        role = links.get(x.get("rol"))
                        CreatorToSeries.objects.get_or_create(series=w, creator=a, role=role)
                    else:
                        print(x.get("publicatienummer"))