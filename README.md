                                                                                  
                                                    @@@@                        
                                                    @@@@                        
                                                    @@@@                        
                                                    @@@@                        
              @@@@@@@@@@@@@@       @@@@@@@@@@@      @@@@@@@@@@@@@@,             
           ,@@@@(       @@@@     @@@@               @@@@@       @@@@@           
          &@@@.         @@@@     @@@@               @@@@          @@@@          
          @@@@          @@@@      @@@@@@,           @@@@          #@@@          
          @@@@          @@@@          @@@@@@@,      @@@@           @@@          
          @@@@          @@@@               @@@@     @@@@          @@@@          
           &@@@@*      @@@@@               .@@@     @@@@         @@@@           
              @@@@@@@@@@@@@@     @@@@@@@@@@@@@      @@@@@@@@@@@@@@@             
                        @@@@        %%%%%                %%%%%                  
                       @@@@                                                     
           @@@@@@@@@@@@@@                                                       
           

# Frais - PPE 2 GSB
## ***Application client léger pour la gestion des frais des visiteurs GSB.***
  
Projet personnel encadré réalisé par **Thomas SANTONI** et **Thibault THOMAS**,  
étudiants en 2e année de **BTS Services informatiques aux organisations**.  

Professeur : Mme CHATAING  
Sup'Chassagnes - Oullins (69)  
 
---

## Sommaire
1. [Introduction](#1-introduction)   
  1.1. [Contexte](#11-contexte)  
  1.2. [L'existant - la nouvelle application](#12-lexistant--la-nouvelle-application)  
  1.3. [Technologies mises en oeuvre](#13-technologies-et-savoir-faire-mis-en-oeuvre)  
2. [Utiliser l'application](#2-utiliser-lapplication)  
  2.1. [Environnement logiciel requis](#21-environnement-logiciel-requis)  
  2.2. [Installation du projet (sur une machine de développement)](#22-installation-du-projet-sur-une-machine-de-d%C3%A9veloppement)  
  2.3. [Déploiement du projet sur un serveur de production](#23-d%C3%A9ploiement-du-projet-sur-un-serveur-de-production)
---

## 1. Introduction
### 1.1. Contexte
Le laboratoire a mis à disposition des visiteurs médicaux une application permettant de visualiser et saisir les frais engagés par les visiteurs lors des visites aux praticiens. Ces frais concernent les déplacements, la restauration et l’hébergement générés par l’activité de visite médicale.

Le remboursement de l'ensemble des frais engagés par les visiteurs s’organise mensuellement et donne lieu à une fiche de frais identifiée par le numéro du visiteur et le mois de l’année.

À chaque dépense type (hôtel, repas, ...) correspond un montant forfaitaire appliqué (on parle de frais "forfaitisé"). Le justificatif n’est pas demandé (les rapports de visite serviront de preuve) mais doivent être conservés pendant trois ans par les visiteurs. Des contrôles réguliers sont faits par les délégués régionaux qui peuvent donner lieu à des demandes de remboursement de trop perçu par le visiteur.

Pour toute dépense en dehors du forfait (repas en présence d'un spécialiste lors d'une animation, achat de fournitures, réservation de salle pour une conférence, etc), le visiteur enregistrera la date, le montant et le libellé de la dépense. Il doit fournir au service comptable une facture acquittée. Le système à produire doit lui indiquer le nombre de justificatifs pris en compte dans le remboursement.

### 1.2. L'existant / la nouvelle application
L’application de gestion des frais de visite actuelle est développée en PHP objet et respecte le pattern MVC.

**Une nouvelle application web, développée en Python avec le framework Django, doit être développée.
Elle est destinée aux visiteurs médicaux et doit leur permettre de consulter leurs états de frais.**

Une autre application sera développée dans un second temps pour permettre au personnel du service comptable de GSB de faire le suivi des états de frais des visiteurs médicaux jusqu'à leur règlement.

*Pour connaître l'intégralité du contexte et le cahier des charges, consulter la* [fiche des consignes](dossier_technique/consignes.pdf). 


### 1.3. Technologies et savoir-faire mis en oeuvre
+ Langage orienté objet (et multi-paradigmes) : Python
+ Développement web avec le framework Django 
  + patron de conception MVT (Modèle - Vue - Template)
  + ORM intégré et "database agnostic"
+ CSS avec le framework Bulma (responsive design)
+ JavaScript
+ Génération de fichiers PDF téléchargeables et au contenu dynamique grâce à un module Python
+ Système de contrôle de version : Git
+ Livraison incrémentale du projet grâce à la méthode Scrum
 
---

## 2. Utiliser l'application  
### 2.1. Environnement logiciel requis
+ Windows ou Linux avec Python 3.8 (MacOS non testé)
+ Un terminal pour configurer le projet et lancer les commandes d'administration de Django
+ Au choix, un simple éditeur de texte ou un IDE
+ Un navigateur web pour naviguer sur le site
  + de préférence autre que Internet Explorer, car le framework CSS Bulma n'est pas totalement compatible

### 2.2. Installation du projet (sur une machine de développement)
#### 2.2.1. Récupération du dépôt git
```
git clone https://github.com/th-thomas/gsb-frais/
```

#### 2.2.2. Création et activation de l'environnement Python virtuel 
Se placer dans le répertoire du projet, puis exécuter les commandes suivantes.
+ Sous Windows :
  ```shell
  virtualenv venv
  .\venv\Scripts\activate
  ```
+ Sous Linux :
  ```bash
  virtualenv venv
  source venv/bin/activate
  ```

#### 2.2.3. Installation des dépendances requises
```bash
python -m pip install -r requirements.txt
```

#### 2.2.4. Création et exécution des migrations
> Les migrations sont la manière par laquelle Django propage des modifications que vous apportez à des modèles (ajout d’un champ, suppression d’un modèle, etc.) dans un schéma de base de données.

Exécuter dans cet ordre les commandes :
```shell
python manage.py makemigrations
python manage.py migrate
```

##### Notes

*La commande* `migrate` *exécute les migrations. Cette fois-ci, elle a permis de créer la base de données (fichier SQLite`db.sqlite3`) et d'y créer les tables correspondant aux modèles.*

*La commande* `makemigrations` *est responsable de la création de nouvelles migrations en fonction des modifications apportées aux modèles.*

+ *Comme le projet contient déjà le fichier de migration initial, et qu'aucune modification n'a été apportée aux modèles, cette commande n'aura aucune incidence cette fois-ci.*  

+ *__Elle devra cependant être exécutée préalablement à la commande* `migrate` *chaque fois qu'une modification sera apportée aux modèles (`models.py`).__*

#### 2.2.5. Chargement du jeu de données initial dans la base de données
La base de données, désormais construite, est pour l'instant vide.  
Il faut lui ajouter des données grâce à la commande :
```
python manage.py load_data
```
qui génère des données en créant un visiteur médical et en lui attribuant des fiches de frais pour l'année courante et l'année précédente.  

À la fin de son exécution, **elle affiche également les identifiants nécessaires pour se connecter au site.**

##### Note
*D'une manière générale :*
+ *le __nom d'utilisateur__ d'un utilisateur (visiteur médical) est, en minuscules et sans accents, la chaîne de caractères formée par __la première lettre de son prénom suivie du nom.__*
+ *son __mot de passe__ par défaut est sa __date d'embauche au format jjmmaaaa.__*

#### 2.2.6. Démarrage du serveur de développement
Saisir la commande
```shell
python manage.py runserver
```
afin de démarrer le serveur de développement. Le serveur fonctionne sur le port 8000 à l'adresse 127.0.0.1.

Pour accéder au site, il faut donc saisir l'adresse suivante dans le navigateur web :
```
http://127.0.0.1:8000/
```
et, sur la page de connexion qui s'affiche, saisir les identifiants qui ont été donnés auparavant.

Voici, pour rappel, les identifiants du visiteur médical créé avec la commande `load_data` :  
+ Nom d'utilisateur : `jdupont`
+ Mot de passe : `31121999`

### 2.3. Déploiement du projet sur un serveur de production
Exemple de procédure de déploiement sur un serveur Ubuntu 20.04 avec Nginx, Gunicorn et une base de données PostgreSQL.

Nous reprenons [la démarche proposée par DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04-fr).

#### 2.3.1. Mise à jour des paquets installés et installation des paquets nécessaires
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

#### 2.3.2. Création de la base de données et de l'utilisateur PostgreSQL
Se connecter à une session interactive de Postgres en tapant :
```bash
sudo -u postgres psql
```

Un invite de commandes Postgres s'ouvre alors (`postgres=#` s'affiche à l'écran).

Dans cet invite, créer la base de données à l'aide de la commande :
```sql
CREATE DATABASE gsbdb;
```

Puis créer l'utilisateur qui sera utilisé par l'application Django :
```sql
CREATE USER gsbuser IDENTIFIED WITH PASSWORD 'gsbpwd';
```

Exécuter ensuite les commandes suivantes, [recommandées par la documentation Django](https://docs.djangoproject.com/en/3.0/ref/databases/#optimizing-postgresql-s-configuration) elle-même :
```sql
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

Enfin, il faut donner au nouvel utilisateur créé un accès pour administrer la nouvelle base de données :
```sql
GRANT ALL PRIVILEGES ON DATABASE gsbdb TO gsbuser;
```

Quitter l'invite PostgreSQL en tapant :
```
\q
```

#### 2.3.3. 






