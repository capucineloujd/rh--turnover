# RH turnover

## Contexte et objectif :
Ce projet est le quatrième dans la cadre de ma formation IA d'OpenClassroom. Dans le cadre d'une problématique de turnover, nous analysons les données RH de l'entreprise pour identifier objectivement les causes de démission. Trois sources de données sont disponibles : le SIRH (profil et informations contractuelles des employés), le système d'évaluation annuelle (notes de performance et satisfaction), et un sondage bien-être annuel (incluant  un indicateur de départ).
## Instructions d'installation :
* Ce projet utilise uv pour gérer les dépendances.
* Pour cloner le repo : git clone https://github.com/capucineloujd/rh--turnover.git
* Pour installer les dépendances : uv sync
* Pour lancer le notebook : jupyter notebook notebook/notebook.ipynb
## Convention des branches : 
* `feature/nom` : ajout d'une nouvelle fonctionnalité (dont readme.md)
* `data/nom` : travail sur les données
## Résultat principal :
Nous avons trouvé que le principal facteur de démission était les heures supplémentaires.