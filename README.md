# ocr.tp
Projet 6

### ### ###	### ### ###	### ### ###

		OBJECTIF DU SCRIPT

### ### ###	### ### ###	### ### ###

Ce script permet de faire un backup au format .taz.bz2 des fichiers contenus dans le tableau, ainsi que de la base de donnée MySQL.
Il permet aussi de faire une restauration à partir de l'un de ces backups.



### ### ###	### ### ###	### ### ###

		UTILISATION

### ### ###	### ### ###	### ### ###

Pour faire fonctionner le script, il faut utiliser le terminal et entrer la commande suivante :

python3 svg.py config.yaml


Le fichier config.yaml est le fichier de configuration. Il contient notamment les variables, et l'opération à effectuée (voir plus bas).

Le fichier svg.py est le script qui effectue l'opération voulue, avec les variables contenus dans fichier config.yaml.



### ### ###	### ### ###	### ### ###

		config.yaml

### ### ###	### ### ###	### ### ###

Le fichier de configuration est divisé en 3 petites parties.

La première partie du fichier, le bloque de commentaires, sont des indications propres au format YAML.

La seconde partie sont des précisions sur le langage du script, et surtout la version de python utilisée ainsi que l'OS et sa version.

La troisième concerne les constantes utilisées dans le script.
La dernière est particulière, il faut écrire "backup" si on veut qu'une backup soit effectuée, ou "restore" si on veut que ce soit une restauration. Par défaut, c'est une backup qui est effectuée.



### ### ###	### ### ###	### ### ###

		svg.py

### ### ###	### ### ###	### ### ###

