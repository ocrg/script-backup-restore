# Script de sauvegarde et de restauration de fichiers, de dossiers, et de BDD MySQL sous Debian.
[![license](https://img.shields.io/badge/license-CC0-green)](https://fr.wikipedia.org/wiki/Licence_Creative_Commons#Sept_licences_r%C3%A9guli%C3%A8rement_utilis%C3%A9es)

Ce script permet de faire un backup d'un site WordPress, de ses fichiers essentiels et de sa base de données MySQL.  
Il permet également de faire une restauration à partir de l'un des backups effectué. Autrement dit, il permet de repartir à zéro.


## Pour commencer

Le script fonctionne dans le contexte ci-dessous.


### Contexte

Sur une VM [Debian 11](https://www.debian.org) créée avec VirtualBox 6.1, le site est installé avec les programmes suivants :

- Apache2
- PHP 7
- mysql 8
- WordPress [téléchargé](https://fr.wordpress.org/download/)
- Python 3


### Quelques détails

Pour installer le site, on peut utiliser des tutoriels. En voici quelques-uns :
- [netpunet.fr](https://fr.wordpress.org/download/), surtout MySQL,
- [reportingbusiness](https://www.reportingbusiness.fr/blogging/installez-wordpress-sur-votre-ordinateur-en-moins-de-15-minutes-linux.html), surtout Apache2,
- [wordpress.org](https://fr.wordpress.org/support/article/how-to-install-wordpress/), surtout pour WordPress mais pas que.

Du reste il y a sur [OpenClassrooms](https://openclassrooms.com/fr/) les cours sur LAMP, MySQL, WordPress, Linux et la virtualisation.  
Une fois le site installé et fonctionnel, il faut le personnaliser en choisissant un thème, et en publiant quelques billets pour rendre le site un peu plus "vivant".


## Présentation du script

Le fichier svg.py est le script qui effectue l'opération voulue, avec les variables contenus dans fichier config.yaml.

Le fichier config.yaml est le fichier de configuration. Il contient notamment les variables, et l'opération à effectuer (voir plus bas) : un backup ou une restauration.

En somme, si le script est le moteur, son fichier de configuration est le conducteur.


### config.yaml

Le fichier de configuration, est divisé en 3 petites parties.

La première partie du fichier, le shebang et le bloc de commentaires, sont des indications propres au format YAML.

La seconde partie sont des précisions sur le langage du script, et surtout la version de python utilisée ainsi que l'OS et sa version.

La troisième concerne les constantes utilisées dans le script.
La dernière est particulière, il faut écrire ``backup`` si on veut qu'une backup soit effectuée, ou ``restore`` si on veut que ce soit une restauration. Par défaut, c'est une backup qui est effectuée.


### svg.py

Le meilleur moyen pour comprendre le fonctionnement du script est d'aller le regarder et d'y lire les commentaires. Le script est divisé en plusieurs grandes parties qui sont elles mêmes divisées en sous-parties.

Voici l'arborescence :
- le shebang ;
- les import ;
- fonction de lecture du fichier .yaml ;
- partie backup :
  - fonction de création d'un dossier temporaire ;
  - fonction de sauvegarde de la base de données dans le dossier temporaire ;
  - fonction de copie des fichiers à sauvegarder dans le dossier temporaire ;
  - fonction de compression du dossier temporaire, et qui supprime ensuite ce dossier ;
- partie restauration :
  - fonction de création d'un dossier temporaire ;
  - fonction qui supprime les fichiers à restaurer (simulation d'un crash) ;
  - fonction de décompression, tout est placé dans le dossier temporaire ;
  - fonction de restauration des fichiers et dossiers, les éléments sont copier du dossier temporaire au répertoire du site ;
  - fonction de restauration de la base de données MySQL, et qui supprime le dossier temporaire ;
- fonction backup (cette fonction lance les fonctions écrites dans la partie backup) ;
- fonction restauration (cette fonction lance les fonctions écrites dans la partie restauration) ;
- morceau de code qui remplie les constantes (il utilise vars et la fonction de lecture du fichier .yaml pour remplir lesdites constantes) ;
- lanceur du script.


## Utilisation

Une fois la configuration ajustée, on peut lancer le script. Ce dernier quant à lui n'a logiquement pas besoin d'être modifié.

Il faut ouvrir le terminal et écrire cette ligne de commande :  
``python3 svg.py config.yaml``


### Codes retour

En cas de bug, pour en connaître l'origine dans le script, il faut taper la commande suivante :  
``echo $?``

Voici la liste des différents code retour :
- Partie backup :
  - 1 : échec de la lecture du fichier .yaml. Il n'a pas les bons droits, son nom dans la ligne de commande est incorrect, une constante (ou une variable) y est absente ou mal écrite, ou autre. L'erreur 14 ressemble à l'erreur 1, cependant, l'erreur 14 se produit lorsque la lecture du fichier .yaml a réussie mais que le contenu en est invalide. Dans les 2 cas, le problème vient du fichier .yaml.
  - 2 : une archive .tar.bz2 du même nom existe déjà, le dossier temporaire n'a pas été créé.
  - 3 : problème lors de la sauvegarde de la BDD MySQL, dossier temporaire supprimé.
  - 4 : erreur lors de la copie des fichiers, dossier temporaire supprimé.
  - 5 : problème lors de la compression. La copie des fichiers et la sauvegarde de la BDD MySQL ont été réalisés et le dossier temporaire n'a pas été supprimé.
  - 6 : le dossier temporaire n'a pas été supprimé après la compression, mais l'archive est faite.
- Partie restauration :
  - 7 : l'archive à restaurer n'est pas présente.
  - 8 : la simulation d'un crash (suppression des fichiers à restaurer) n'a pas réussi, mais certains fichiers ou dossiers ont peut-être été supprimés. Dossier temporaire supprimé.
  - 9 : décompression en échec, dossier temporaire supprimé. Attention : le format de l'archive est en **bz2**, ce qui n'est pas le plus conventionnel.
  - 10 : erreur pendant la restauration des fichiers, le dossier temporaire n'a pas été supprimé.
  - 11 : problème pendant la restauration de la BDD MySQL, le dossier temporaire n'a pas été supprimé.
  - 12 : le dossier temporaire n'a pas été supprimé après la restauration. La restauration des fichiers et de la BDD à tout de même été faite.
  - 13 : erreur lors de la lecture du fichier suivant le script python *dans la ligne de commande*. La ligne de commande ne contient probablement pas le fichier .yaml.
  - 14 : problème de remplissage des variables lues dans le fichier .yaml. Ce dernier a cependant été lu, mais il contient une erreur. Voir le code retour 1.  


## F.A.Q.

**Il manque un fichier dans l'archive.**  
Le fichier .yaml est certainement mal remplie quant à ce fichier.  

**Un fichier n'a pas été remis lors de la restauration.**  
Est-il bien dans l'archive ?


## Outils utilisés :

**gedit 3.38.1** avec des greffons déjà présents.  
**Debian 11** avec Gnome en environnement de bureau.


## Version

Version actuelle stable : 1.0  
Écrite en 2021.  
Dernière mise à jour : voir les commits.  

Des mises à jour très mineures peuvent avoir lieu, mais très ponctuellement.  
Ce repository est utilisé à des fins personnelles dans le cadre d'une formation.
