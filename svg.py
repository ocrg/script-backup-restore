#!/usr/bin/python3.9
# Projet 6 et 9, sauvegarde wordpress.



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



# Les imports.
import os
import shutil
import tarfile
# Permet de lire les .yaml
import yaml
import sys
# subprocess exécute une ligne de commande comme dans un terminal
import subprocess



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



### LECTURE DU FICHIER YAML ###
def readConf(file):
	try:
		with open(file, 'r') as Stream:
			return yaml.safe_load(Stream)
	except:
		print("Problème de lecture du fichier .yaml.")
		exit(1)



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CODE DE LA PARTIE BACKUP ###



### VÉRIFICATION ET CRÉATION DOSSIER TEMPORAIRE ###
def create_tmp_save(deb, name_of_backup, temp_directory):

	#	CONTRÔLE
	# S'il y a déjà une archive du même nom, exit. Sinon, on continue.
	if os.path.exists(deb + name_of_backup + '.tar.bz2') == True:
		print("L'archive " + name_of_backup + ".tar.bz2 semble déjà exister.")
		print("Erreur !")
		exit(2)
	# Si le chemin /home/debian/temp_directory n'existe pas, on créer le dossier temporaire.
	if not os.path.exists(temp_directory):
		os.mkdir(temp_directory)


### SQL_DUMP ###
def sql_save(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH):
	try:
		#	MYSQLDUMP
		# La ligne de code qui sera exécutée par subprocess.
		dumpcmd = "mysqldump --add-drop-table -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + BACKUP_PATH + DB_NAME + ".sql"
		subprocess.run(dumpcmd, shell=True)
	except:
		shutil.rmtree(temp_directory)
		print("Erreur !")
		exit(3)


### COPIE DES FICHIERS ###
def copy(files_in_site, temp_directory):
	try:
		#	COPIE
		# On fait le tour du tableau avec la boucle for.
		print("")
		print("Copie des fichiers...")
		for file_or_dir in files_in_site:
			# On contrôle si c'est un dossier ou un fichier.
			# Un dossier = shutil.copytree(src, dst) ; un fichier = shutil.copyfile(src, dst).
			# En dst, on indique le chemin du dossier de destination ET le nom du dossier ou fichier à copier. D'où l'utilisation d'os.path.basename.
			# os.path.basename() nous renvoie le nom du dernier élément d'un chemin et avec son extention. Donc ça nous donne 'wp-config.php' par exemple.

			# Si c'est un dossier et qu'il n'existe pas dans le dossier temporaire :
			if os.path.isdir(file_or_dir) == True and os.path.exists(temp_directory + os.path.basename(file_or_dir)) == False:
				shutil.copytree(file_or_dir, temp_directory + os.path.basename(file_or_dir))
			# Si c'est un fichier et qu'il n'existe pas dans le dossier temporaire :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(temp_directory + os.path.basename(file_or_dir)) == False:
				shutil.copyfile(file_or_dir, temp_directory + os.path.basename(file_or_dir))
			# Si c'est un dossier et qu'il existe déjà dans le dossier temporaire :
			elif os.path.isdir(file_or_dir) == True and os.path.exists(temp_directory + os.path.basename(file_or_dir)) == True:
				print("Ce dossier existe déjà dans le dossier temporaire : " + file_or_dir)
			# Si c'est un fichier et qu'il existe déjà dans le dossier temporaire :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(temp_directory + os.path.basename(file_or_dir)) == True:
				print("Ce fichier existe déjà dans le dossier temporaire : " + file_or_dir)			
			# Si anomalie :
			else:
				print("Il y a eu un problème avec" + file_or_dir)
		print("OK.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		print("Erreur !")
		exit(4)


### CRÉATION DU TAR.BZ2 ET NETTOYAGE DU DOSSIER TEMPORAIRE ###
def compress_clean(deb, temp_directory, name_of_backup):
	try:
		#	COMPRESSION
		# Instruction pour le tar.bz2.
		print("Compression...")
		with tarfile.open(deb + name_of_backup + '.tar.bz2', "w:bz2") as tar:
			tar.add(temp_directory, os.path.basename(temp_directory))
		print("OK.")
		print("")
	except:
		print("Erreur !")
		exit(5)


	try:
		#	SUPPRESSION DOSSIER TEMPORAIRE
		# Suppression du dossier temporaire.
		shutil.rmtree(temp_directory)
		print("Backup OK !")
	except:
		print("Erreur !")
		exit(6)



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CODE DE LA PARTIE RESTAURATION ###



### VÉRIFICATION ET DOSSIER TEMPORAIRE ###
def create_tmp_restore(deb, name_of_backup, temp_directory):

	#	CONTRÔLE
	# Y a-t-il déjà une archive du même nom ? Si non, exit. Si oui, on continue.
	if not os.path.exists(deb + name_of_backup + '.tar.bz2'):
		print("L'archive " + name_of_backup + ".tar.bz2 ne semble pas exister.")
		print("Erreur !")
		exit(7)
	# Au besoin, on créer le dossier temporaire, s'il est déjà là on ne fait rien.
	if not os.path.exists(temp_directory):
		os.mkdir(temp_directory)


### FONCTION POUR SIMULER LE CRASH ###
def crash(files_in_site):
	try:
		# On fait le tour du tableau avec la boucle for.
		print("Remise à zéro...")
		for file_or_dir in files_in_site:
			# On contrôle si c'est un dossier ou un fichier. Un dossier = shutil.rmtree(), un fichier = os.remove().
			# os.path.basename() nous renvoie le nom du dernier élément d'un chemin, et avec son extention. Donc ça nous donne 'wp-config.php' par exemple.
			# Si c'est un dossier et que ça existe, on le supprime dans /var :
			if os.path.isdir(file_or_dir) == True and os.path.exists(file_or_dir) == True:
				shutil.rmtree(file_or_dir)
				print("Dossier supprimé : " + os.path.basename(file_or_dir))
			# Si c'est un fichier et que ça existe, on le supprime dans /var :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(file_or_dir) == True:
				os.remove(file_or_dir)
				print("Fichier supprimé : " + os.path.basename(file_or_dir))
			# Si c'est un dossier ou un fichier mais qu'il n'existe pas dans /var, on fait un message :
			elif os.path.exists(file_or_dir) == False:
				print("Fichier ou dossier déjà supprimé : " + os.path.basename(file_or_dir))
			# S'il y a anomalie :
			else:
				print("Il y a eu un problème avec " + file_or_dir)
		print("OK.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		print("Erreur !")
		exit(8)


### EXTRATION ###
def extract(deb, name_of_backup, temp_directory):
	try:
		#	DÉCOMPRESSION
		# Décompression. Instruction pour le tar.bz2.
		print("Décompression...")
		with tarfile.open(deb + name_of_backup + '.tar.bz2') as tar:
			tar.extractall(temp_directory)
		print("OK.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		print("Erreur !")
		exit(9)


### RESTAURATION ###
def restauration(files_to_restore, site_directory, temp_directory):
	try:
		#	RESTAURATION
		print("Restauration...")
		for file_or_dir in files_to_restore:
			# On contrôle si c'est un dossier ou un fichier. Un dossier = shutil.rmtree(), un fichier = os.remove().
			# Si c'est un dossier et qu'il n'existe pas dans /var, on le met dans /var :
			if os.path.isdir(file_or_dir) == True and os.path.exists(site_directory + os.path.basename(file_or_dir)) == False:
				shutil.copytree(file_or_dir, site_directory + os.path.basename(file_or_dir))
				print("Dossier restauré : " + os.path.basename(file_or_dir))
			# Si c'est un fichier et qu'il n'existe pas dans /var, on le met dans /var :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(site_directory + os.path.basename(file_or_dir)) == False:
				shutil.copyfile(file_or_dir, site_directory + os.path.basename(file_or_dir))
				print("Fichier restauré : " + os.path.basename(file_or_dir))
			# Si c'est un dossier qui existe déjà dans /var, on fait un message :
			elif os.path.exists(file_or_dir) == False:
				print("Ce fichier ou dossier existe déjà dans www.ocr.tp : " + os.path.basename(file_or_dir))
			# S'il y a anomalie :
			else:
				print("Il y a eu un problème avec " + os.path.basename(file_or_dir))
		print("OK.")
		print("")
	except:
		print("Erreur !")
		exit(10)


### SQL_DUMP ###
def sql_restore(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH):
	try:
		#	MYSQLDUMP
		print("Restauration de la base MySQL...")
		# La ligne de code qui sera exécutée par subprocess.
		dumpcmd = "mysql -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " < " + BACKUP_PATH + DB_NAME + ".sql"
		subprocess.run(dumpcmd, shell=True)
		# Un print pour voir ce qui est clairement saisie.
		print("OK.")
		print("")
	except:
		# MySQLdump peut générer des erreurs mais poursuivre correctement malgré tout...
		print("Erreur !")
		exit(11)

	try:
		#	SUPPRESSION DOSSIER TEMPORAIRE
		# Suppression du dossier temporaire.
		shutil.rmtree(temp_directory)
		print("Restauration OK !")
	except:
		print("Erreur !")
		exit(12)



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



# Appel de la fonction pour sauvegarder.
def backup():
	create_tmp_save(deb, name_of_backup, temp_directory)
	sql_save(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH)
	copy(files_in_site, temp_directory)
	compress_clean(deb, temp_directory, name_of_backup)


# Appels des fonctions pour restaurer.
def restore():
	create_tmp_restore(deb, name_of_backup, temp_directory)
	crash(files_in_site)
	extract(deb, name_of_backup, temp_directory)
	restauration(files_to_restore, site_directory, temp_directory)
	sql_restore(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH)


# Premier point de départ du script. vars contiendra les constantes qui sont dans le fichier .yaml. 
if len(sys.argv) == 2:
	vars = readConf(sys.argv[1])
else:
	print("Erreur !")
	exit(13)


# Les constantes.
# Chemin de home.
deb = vars['constantes']['deb']
# Nom de la backup.
name_of_backup = vars['constantes']['name_of_backup']
# Chemin du dossier temporaire, on ne peut pas faire d'assemblage de variable dans un .yaml.
temp_directory = deb + name_of_backup + '/'
# Chemin du dossier du site.
site_directory = vars ['constantes']['site_directory']
# Tableau qui contient les fichiers à sauvegarder ou supprimer selon la situation.
files_in_site = vars['constantes']['files_in_site']
# Tableau qui contient les fichiers à remettre en place.
files_to_restore = [temp_directory + 'wp-config.php',temp_directory + 'wp-content',temp_directory + '.htaccess']
# Les constantes MySQL.
DB_HOST = vars['constantes']['DB_HOST']
DB_USER = vars['constantes']['DB_USER']
DB_USER_PASSWORD = vars['constantes']['DB_USER_PASSWORD']
DB_NAME = vars['constantes']['DB_NAME']
BACKUP_PATH = temp_directory


# Second point de départ du script. Tout commence par la variable "status".
if (vars['constantes']['status'] == 'restore'):
	restore()
else:
	backup()



