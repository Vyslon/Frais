                                                                                  
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
  1.1. [Présentation de l'application](#11-pr%C3%A9sentation-de-lapplication)  
  1.2. [Technologies mises en oeuvre](#12-technologies-et-savoir-faire-mis-en-oeuvre)  
2. [Utiliser l'application](#2-utiliser-lapplication)  
  2.1. [Environnement logiciel requis](#21-environnement-logiciel-requis)  
  2.2. [Création de la base de données et de son utilisateur](#22-cr%C3%A9ation-de-la-base-de-donn%C3%A9es-et-de-son-utilisateur)  
  2.3. [Configuration de l'application pour la connexion à la base de données](#23-configuration-de-lapplication-pour-la-connexion-%C3%A0-la-base-de-donn%C3%A9es)   
  2.4. [Authentification dans l'application (formulaire de connexion)](#24-authentification-dans-lapplication-formulaire-de-connexion)   
  2.5. [Navigation entre les formulaires](#25-navigation-entre-les-formulaires)
3. [Annexes](#3-annexes)  
  3.1. [Migrer les données de Access vers MySQL](#31-migrer-les-donn%C3%A9es-de-access-vers-mysql)  
  3.2. [Modèle conceptuel de données](#32-mod%C3%A8le-conceptuel-de-donn%C3%A9es)  
  3.3. [Diagramme de classes](#33-diagramme-de-classes)  
4. [Remerciements](#4-remerciements)  

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

*Pour connaître l'intégralité du contexte et le cahier des charges, consulter la* [fiche des consignes](consignes.pdf). 


### 1.3. Technologies et savoir-faire mis en oeuvre
+ Langage orienté objet (et multi-paradigmes) : Python
+ Développement web avec le framework Django 
  + patron de conception MVT (Modèle - Vue - Template)
  + ORM intégré et "database agnostic"
+ Design des pages web avec le framework CSS Bulma
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

### 2.2. Installation du projet
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
La commande `migrate` exécute les migrations. Cette fois-ci, elle a permis de créer la base de données (fichier SQLite `db.sqlite3`) et d'y créer les tables correspondant aux modèles.

La commande `makemigrations` est responsable de la création de nouvelles migrations en fonction des modifications apportées aux modèles.

+ Comme le projet contient déjà le fichier de migration initial, et qu'aucune modification n'a été apportée aux modèles, cette commande n'aura aucune incidence cette fois-ci.  

+ **Elle devra cependant être exécutée préalablement à la commande `migrate` chaque fois qu'une modification sera apportée aux modèles (`models.py`).**

#### 2.2.5. Chargement du jeu de données initial dans la base de données
La base de données, désormais construite, est pour l'instant vide.  
Il faut lui ajouter des données grâce à la commande :
```
python manage.py load_data
```
qui génère des données en créant un visiteur médical et en lui attribuant des fiches de frais pour l'année courante et l'année précédente.  

À la fin de son exécution, **elle affiche également les identifiants nécessaires pour se connecter au site.**

