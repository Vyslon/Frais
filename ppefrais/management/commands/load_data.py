from django.core.management import BaseCommand
from ppefrais.models import Visiteur, FicheFrais, LigneFraisForfait, LigneFraisHorsForfait
from datetime import datetime, date
import month, calendar
import random


class Command(BaseCommand):
    help = 'Charge un jeu de données initial dans la base de données.'

    def handle(self, *args, **options):
        # Création du visiteur
        date_embauche = date(1999, 12, 31)
        visiteur, vcreated = Visiteur.objects.get_or_create(
            first_name='Jacques',
            last_name='Dupont',
            date_embauche=date_embauche,
        )

        # Création des fiches de frais
        # On fixe la date à partir de laquelle on créé
        # les fiches à janvier de l'année précédente
        now = datetime.now()
        date_debut_fiches = datetime.strptime(str(now.year - 1) + '01', '%Y%m')

        # Une fiche par mois
        for i in range(1, 13 + now.month):
            # Mois
            if i < 13:
                mois_annee = date_debut_fiches.year
                mois_mois = i
                mois = month.Month(mois_annee, mois_mois)
            else:
                mois_annee = date_debut_fiches.year + 1
                mois_mois = i - 12
                mois = month.Month(mois_annee, mois_mois)
            # Etat
            if i == 12 + now.month:
                etat = FicheFrais.Etat.ENCOURS
            elif i == 11 + now.month:
                etat = FicheFrais.Etat.CLOTUREE
            elif i == 10 + now.month:
                etat = FicheFrais.Etat.VALIDEE
            else:
                etat = FicheFrais.Etat.REMBOURSEE

            fiche, fcreated = FicheFrais.objects.get_or_create(
                visiteur=visiteur,
                etat=etat,
                mois=mois,
            )

            if fcreated:
                # Ligne de frais forfaitisés
                quantite = random.randint(0, 999)
                ligne_km = LigneFraisForfait.objects.get(
                    fiche=fiche,
                    frais_forfait=LigneFraisForfait.FraisForfait.FRAISKM,
                )
                ligne_km.quantite = quantite
                ligne_km.save()

                quantite = random.randint(0, 20)
                ligne_etape = LigneFraisForfait.objects.get(
                    fiche=fiche,
                    frais_forfait=LigneFraisForfait.FraisForfait.ETAPE,
                )
                ligne_etape.quantite = quantite
                ligne_etape.save()

                quantite = random.randint(0, 20)
                ligne_restau = LigneFraisForfait.objects.get(
                    fiche=fiche,
                    frais_forfait=LigneFraisForfait.FraisForfait.RESTAU,
                )
                ligne_restau.quantite = quantite
                ligne_restau.save()

                quantite = random.randint(0, 20)
                ligne_hotel = LigneFraisForfait.objects.get(
                    fiche=fiche,
                    frais_forfait=LigneFraisForfait.FraisForfait.NUITHOTEL
                )
                ligne_hotel.quantite = quantite
                ligne_hotel.save()

                # Lignes de frais hors forfait
                frais = [
                    ('Location véhicule', random.randint(70, 450)),
                    ('Repas avec praticien', random.randint(33, 50)),
                    ('Achat de matériel de papèterie', random.randint(10, 50)),
                    ('Location salle conférence', random.randint(140, 700)),
                    ('Taxi', random.randint(20, 70)),
                    ('Frais vestimentaire / représentation', random.randint(30, 450)),
                    ('Traiteur, alimentation, boisson', random.randint(35, 450)),
                    ('Voyage SNCF', random.randint(30, 150)),
                    ('Rémunération intervenant / spécialiste', random.randint(250, 1200)),
                ]
                # On génère entre 3 et 5 lignes de frais hors forfait par mois
                for j in range(1, random.randint(3, 6)):
                    if mois_mois == 2 and calendar.isleap(mois_annee):
                        jour = random.randint(1, 28)
                    else:
                        if mois in [1, 3, 5, 7, 8, 10, 12]:
                            jour = random.randint(1, 31)
                        else:
                            jour = random.randint(1, 30)

                    ligne_hf = random.randint(1, len(frais)) - 1

                    LigneFraisHorsForfait.objects.create(
                        fiche=fiche,
                        libelle=frais[ligne_hf][0],
                        date=date(mois_annee, mois_mois, jour),
                        montant=frais[ligne_hf][1]
                    )

        self.stdout.write(
            self.style.SUCCESS(
                'Données créées avec succès.\n'
                f'Connectez-vous au site avec le compte du visiteur {visiteur.first_name} {visiteur.last_name}.\n'
                f'\tIdentifiant  :  {visiteur.username}\n'
                f'\tMot de passe :  {visiteur.date_embauche:%d%m%Y}'
            )
        )
