from django.core.management import BaseCommand
from ppefrais.models import Visiteur, FicheFrais, LigneFraisForfait, LigneFraisHorsForfait
from datetime import datetime
import month
from random import randrange


class Command(BaseCommand):
    help = 'Charge un jeu de données initial dans la base de données.'

    def handle(self, *args, **options):
        # Création du visiteur
        date_embauche = datetime.strptime('1999-12-31', '%Y-%m-%d')
        vobj, vcreated = Visiteur.objects.get_or_create(
            first_name='Jacques',
            last_name='Dupont',
            date_embauche=date_embauche,
        )

        # Création des fiches de frais
        now = datetime.now()
        # On fixe la date à partir de laquelle on créé
        # les fiches à janvier de l'année précédente
        date_debut_fiches = datetime.strptime(str(now.year - 1) + '01', '%Y%m')
        vobj = Visiteur.objects.get(username=vobj.username)

        # Une fiche par mois
        for i in range(1, 13 + now.month):
            # Mois
            if i < 13:
                mois = month.Month(date_debut_fiches.year, i)
            else:
                mois = month.Month(date_debut_fiches.year + 1, i - 12)
            # Etat
            if i == 12 + now.month:
                etat = FicheFrais.Etat.ENCOURS
            elif i == 11 + now.month:
                etat = FicheFrais.Etat.CLOTUREE
            elif i == 10 + now.month:
                etat = FicheFrais.Etat.VALIDEE
            else:
                etat = FicheFrais.Etat.REMBOURSEE

            fobj, fcreated = FicheFrais.objects.get_or_create(
                visiteur=Visiteur.objects.get(username=vobj.username),
                etat=etat,
                mois=mois,
            )

        # if fcreated:
        #     rand = randrange(20, 600)
        #     LigneFraisForfait.objects.create(
        #         fiche=FicheFrais.objects.get(id=fobj.id),
        #         frais_forfait=LigneFraisForfait.FraisForfait.FRAISKM,
        #         quantite=rand
        #     )

        self.stdout.write(
            self.style.SUCCESS(
                'Données créées avec succès.\n'
                f'Connectez-vous au site avec le compte du visiteur {vobj.first_name} {vobj.last_name}.\n'
                f'\tIdentifiant  :  {vobj.username}\n'
                f'\tMot de passe :  {vobj.date_embauche:%d%m%Y}'
            )
        )
