# blackmist-professor-announce-generator
Générateur du texte d'annonce des cours du RP Black Mist

## Exécuter le script
### Prérequis
- Python 3.12.3+
- Les modules présents dans `requirements.txt`

Pour les installer, exécutez la commande suivante. Veillez à vous trouver dans le bon chemin d'accès.

```
pip install -r requirements.txt
```
### Lancer le script

Comme tout bon script Python, il faut ouvrir un terminal, évidemment dans le bon dossier, puis exécuter la commande suivante.
```
python main.py
```

## Fonctionnement du script

Par souci de finances, le script ne se base pas sur l'API Google mais une fonctionnalité de Google Sheet qui permet de partager le classeur sous divers formats, dont le CSV. 
Chaque feuille du classeur peut être convertie en un fichier CSV accessible via une URL et dont le contenu se met automatiquement à jour en fonction des modifications apportées au classeur. Bien pratique !

> [!NOTE]
> Le script se base sur le jour courant lors qu'il est exécuté. Si on est samedi, il prendra la colonne SAMEDI.

Le script commence par lister toutes les feuilles sur lesquelles travailler, chacune correspondant à une année de l'université. Un travail d'analyse des CSV m'a permis de déterminer quelles sont les colonnes qui étaient les plus intéressantes. Ensuite, pour chaque feuille, le programme va regarder s'il y a un cours de renseigné. Il se base uniquement sur le fait qu'une matière soit renseignée.
Puis, s'il trouve un cours, il se contente simplement d'extraire les données puis de les mettre en forme dans une variable textuelle, pour finalement l'afficher dans la console et même en copier le contenu dans le presse-papier.

> [!IMPORTANT]
> Le script n'est pas parfait. Un survol du texte généré est primordial pour vérifier que tout soit en ordre avant de balancer l'annonce sur le serveur Discord Black Mist.

## Mettre à jour le script
### Ajouter ou modifier une feuille
Ajoutez les années au script en faisant *Fichier > Partager > Publier sur le web*.

Ensuite, sélectionnez la feuille de l'année souhaitée puis demandez le lien de partage en tant que fichier CSV séparé par des virgules.

Enfin, dans le fichier `main.py`, modifiez la variable `planning_urls` en conséquence, soit en ajoutant une ligne, soit en modifiant la valeur d'une clé.

Il faut évidemment ajouter une feuille lorsqu'une nouvelle année se crée. Aux dernières nouvelles, les joueurs élèves ne sont réparties que sur deux années.