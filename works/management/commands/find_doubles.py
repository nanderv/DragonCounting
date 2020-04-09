import mysql.connector

from django.core.management.base import BaseCommand

def get_name(x):
    vn = x.get("voornaam")
    if len(vn) == 0:
        return x.get("naam")
    return vn + " " + x.get("naam")


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="oldsystem2"
        )
        mycursor = mydb.cursor(dictionary=True)

        persons = dict()

        mycursor.execute("SELECT * FROM band where signatuur like '%H-88-l%'")
        for x in mycursor:
            print(x)
