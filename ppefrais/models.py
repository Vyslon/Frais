from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from month.models import MonthField
from django.utils.text import slugify


class Visiteur(AbstractUser):
    adresse = models.CharField(max_length=30, blank=True)
    code_postal = models.CharField(max_length=5, blank=True)
    ville = models.CharField(max_length=30, blank=True)
    date_embauche = models.DateField(blank=True, default=timezone.now)

    class Meta:
        verbose_name = 'Visiteur médical'
        verbose_name_plural = 'Visiteurs médicaux'

    def save(self, *args, **kwargs):
        # Gives a username
        if not self.username:
            self.username = slugify(self.first_name[0] + self.last_name)
        # Gives a password
        # password is date_embauche formatted as ddmmyyyy (i.e 31121999 for December 31, 1999)
        if not self.password:
            self.set_password(self.date_embauche.strftime("%d%m%Y"))
        return super(Visiteur, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class FicheFrais(models.Model):
    class Etat(models.TextChoices):
        CLOTUREE = 'CL', _('Saisie clôturée')
        ENCOURS = 'CR', _('Fiche créée, saisie en cours')
        REMBOURSEE = 'RB', _('Remboursée')
        VALIDEE = 'VA', _('Validée et mise en paiement')

    etat = models.CharField(max_length=3, choices=Etat.choices, default=Etat.ENCOURS)
    visiteur = models.ForeignKey('Visiteur', on_delete=models.RESTRICT, default=None)
    mois = MonthField(null=False, blank=False)
    # nb_justificatifs = models.PositiveIntegerField(blank=True, default=0)
    # montant_valide = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    date_modif = models.DateField(blank=True, auto_now=True)

    def montant_valide(self):
        if (self.etat == FicheFrais.Etat.REMBOURSEE) or (self.etat == FicheFrais.Etat.VALIDEE):
            return self.total_frais_forfaitaires() + self.total_frais_horsforfait()
        else:
            return 0

    def nb_justificatifs(self):
        return self.lignefraishorsforfait_set.count()

    def total_frais_forfaitaires(self):
        total = 0
        for ligne in self.lignefraisforfait_set.all():
            total += ligne.total
        return total

    def total_frais_horsforfait(self):
        total = 0
        for ligne in self.lignefraishorsforfait_set.all():
            total += ligne.montant
        return total

    class Meta:
        verbose_name = 'Fiche de frais'
        verbose_name_plural = 'Fiches de frais'
        unique_together = (('mois', 'visiteur'),)

    def __str__(self):
        return str(self.mois) + ' ' + self.visiteur.__str__()

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(FicheFrais, self).save(*args, **kwargs)
        if is_new:
            LigneFraisForfait.objects.create(fiche=self, frais_forfait=LigneFraisForfait.FraisForfait.ETAPE)
            LigneFraisForfait.objects.create(fiche=self, frais_forfait=LigneFraisForfait.FraisForfait.FRAISKM)
            LigneFraisForfait.objects.create(fiche=self, frais_forfait=LigneFraisForfait.FraisForfait.NUITHOTEL)
            LigneFraisForfait.objects.create(fiche=self, frais_forfait=LigneFraisForfait.FraisForfait.RESTAU)

    def get_absolute_url(self):
        return reverse('une-fiche', args=[(self.mois.strftime('%Y%m'))])


class AbstractLigneFrais(models.Model):
    fiche = models.ForeignKey('FicheFrais', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.fiche.id) + str(self.id) + '(Abstr.)'

    class Meta:
        abstract = True


class LigneFraisHorsForfait(AbstractLigneFrais):
    libelle = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    montant = models.DecimalField(decimal_places=2, max_digits=10, blank=True, default=0)

    def __str__(self):
        return str(self.fiche.id) + str(self.id) + ' (H.F.)'

    def get_absolute_url(self):
        return reverse('une-fiche', args=[(self.fiche.mois.strftime('%Y%m'))])

    class Meta:
        verbose_name = 'Ligne de frais (hors forfait)'
        verbose_name_plural = 'Lignes de frais (hors forfait)'


class LigneFraisForfait(AbstractLigneFrais):
    class FraisForfait(models.TextChoices):
        ETAPE = 'ETP', _('Forfait étape')
        FRAISKM = 'KM', _('Frais kilométrique')
        NUITHOTEL = 'NUI', _('Nuitée hôtel')
        RESTAU = 'REP', _('Repas restaurant')

    frais_forfait = models.CharField(max_length=3, choices=FraisForfait.choices)
    quantite = models.PositiveIntegerField(blank=True, default=0)

    @property
    def total(self):
        return self.montant_unitaire() * self.quantite

    def montant_unitaire(self):
        if self.frais_forfait == 'ETP':
            return 110.00
        elif self.frais_forfait == 'KM':
            return 0.62
        elif self.frais_forfait == 'NUI':
            return 80.00
        elif self.frais_forfait == 'REP':
            return 25.00
        else:
            return 0.00

    def __str__(self):
        return str(self.fiche.id) + str(self.id)

    def get_absolute_url(self):
        return reverse('une-fiche', args=[(self.fiche.mois.strftime('%Y%m'))])

    class Meta:
        verbose_name = 'Ligne de frais'
        verbose_name_plural = 'Lignes de frais'
        unique_together = (('fiche', 'frais_forfait'),)
