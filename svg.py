#!/usr/bin/python3.9
# -*-coding:utf-8 -*

# Projet 6 et 9, sauvegarde wordpress.

# Partie SQL_DUMP du Backup modifié, on a ajouté ça : --add-drop-table
# À voir si ça fonctionne, normalement ça marque dans le .sql que lors de la prochaine injection, il faut d'abord faire un raz de la table avant d'ajouter "ça", le contenu dudit .sql. On n'aura donc plus des .sql de 1.4mo par exemple, à vérifier.

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



# Les imports.
import os
import shutil
import tarfile
import yaml
# subprocess execute une ligne de commande comme dans un terminal.
import subprocess



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


with open("config.yaml", 'r') as stream:
	cfg = yaml.safe_load(stream)

print(cfg["constantes"]["deb"])

#def read_yaml(config):
	# Fonction yaml pour récupérer les données du fichier.
#	return config

#vars = read_yaml(stream)
#print(vars['constantes'])

# Les constantes.
# Constante du chemin de home.
deb = vars['constantes']['deb']
print(deb)
# Nom de la backup.
name_of_backup = vars['constantes']['name_of_backup']
print(name_of_backup)
# Constante du chemin du dossier temporaire.
temp_directory = deb + name_of_backup + '/'
print(temp_directory)
# Tableau qui contient les fichiers à sauvegarder ou supprimer selon la situation.
files_in_site = vars['constantes']['files_in_site']
print(files_in_site)
# Tableau qui contient les fichiers à remettre en place.
files_to_restore = [temp_directory + 'wp-config.php',temp_directory + 'wp-content',temp_directory + '.htaccess']
print(files_to_restore)

# Les constantes MySQL.
DB_HOST = vars['constantes']['DB_HOST']
print(DB_HOST)
DB_USER = vars['constantes']['DB_USER']
print(DB_USER)
DB_USER_PASSWORD = vars['constantes']['DB_USER_PASSWORD']
print(DB_USER_PASSWORD)
DB_NAME = vars['constantes']['DB_NAME']
print(DB_NAME)
BACKUP_PATH = deb + name_of_backup + '/'
print(BACKUP_PATH)

# Constante du chemin du dossier du site.
site_directory = vars['constantes']['site_directory']
print(site_directory)



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



### VÉRIFICATION ET DOSSIER TEMPORAIRE ###
def create_tmp_save(deb, name_of_backup, temp_directory):

	#	CONTRÔLE
	# S'il y a déjà une archive du même nom, exit. Sinon, on continue.
	if os.path.exists(deb + name_of_backup + '.tar.bz2') == True:
		print("L'archive " + name_of_backup + ".tar.bz2 semble déjà exister.")
		exit(1)
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
		# MySQLdump peut générer des erreurs mais poursuivre correctement malgré tout...
		print("Problème avec le bloque MySQLdump. Le script continue quand même.")



### COPIE DES FICHIERS ###
def copy(files_in_site, temp_directory):
	try:
		#	COPIE
		# On fait le tour du tableau avec la boucle for.
		print("")
		print("Début de la copie des fichiers...")
		for file_or_dir in files_in_site:
			# On contrôle si c'est un dossier ou un fichier. Un dossier = shutil.copytree(src, dst), un fichier = shutil.copyfile(src, dst).
			# En dst, on indique le chemin du dossier de destination (logique) + le nom du dossier ou fichier à copier (logique mais moins évident). D'où l'utilisation d'os.path.basename !
			# os.path.basename() nous renvoie le nom du dernier élément d'un chemin, et avec son extention. Donc ça nous donne 'wp-config.php' par exemple. Pratique !

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
		print("Fin de la copie des fichiers.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		exit("Problème avec le bloque de copie.")



### CRÉATION DU TAR.BZ2 ET NETTOYAGE DU DOSSIER TEMPORAIRE ###
def compress_clean(deb, temp_directory, name_of_backup):
	try:
		#	COMPRESSION
		# Compression. Instruction pour le tar.bz2.
		print("Début de la compression...")
		with tarfile.open(deb + name_of_backup + '.tar.bz2', "w:bz2") as tar:
			tar.add(temp_directory, os.path.basename(temp_directory))
		print("Compression terminée.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		exit("Problème avec le bloque tarfile.")


	try:
		#	SUPPRESSION DOSSIER TEMPORAIRE
		# Suppression du dossier temporaire.
		shutil.rmtree(temp_directory)
		print("Backup terminée avec succès !")
	except:
		exit("Problème avec le bloque de suppression du dossier temporaire.")



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###



### VÉRIFICATION ET DOSSIER TEMPORAIRE ###
def create_tmp_restore(deb, name_of_backup, temp_directory):

	#	CONTRÔLE
	# Y a-t-il déjà une archive du même nom ? Si on, exit. Sinon, c'est parfait, on continue.
	if not os.path.exists(deb + name_of_backup + '.tar.bz2'):
		print("L'archive " + name_of_backup + ".tar.bz2 ne semble pas exister.")
		exit(1)
	# Au besoin, on créer le dossier temporaire, s'il est déjà là on ne fait rien.
	if not os.path.exists(temp_directory):
		os.mkdir(temp_directory)



### FONCTION POUR SIMULER LE CRASH ###
def crash(files_in_site):
	try:
		# On fait le tour du tableau avec la boucle for.
		print("Début de la suppression des fichiers existants...")
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
				print("Ce fichier ou dossier semble avoir déjà été supprimé : " + os.path.basename(file_or_dir))
			# S'il y a anomalie :
			else:
				print("Il y a eu un problème avec " + file_or_dir)
		print("Fin de la suppression.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		exit("Problème avec le bloque de suppression.")



### EXTRATION ###
def extract(deb, name_of_backup, temp_directory):
	try:
		#	DÉCOMPRESSION
		# Décompression. Instruction pour le tar.bz2.
		print("Début de la décompression...")
		with tarfile.open(deb + name_of_backup + '.tar.bz2') as tar:
			tar.extractall(temp_directory)
		print("Décompression terminée.")
		print("")
	except:
		shutil.rmtree(temp_directory)
		exit("Problème lors de la décompression. Fin du script.")



### RESTAURATION ###
def restauration(files_to_restore, site_directory, temp_directory):
	try:
		#	RESTAURATION
		print("Début de la restauration des fichiers...")
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
		print("Fin de la restauration des fichiers.")
		print("")
	except:
		exit("Problème avec le bloque de restauration. Le script passe maintenant à la BDD.")



### SQL_DUMP ###
def sql_restore(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH):
	try:
		#	MYSQLDUMP
		print("Début de la restauration MySQL...")
		# La ligne de code qui sera exécutée par subprocess.
		dumpcmd = "mysql -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " < " + BACKUP_PATH + DB_NAME + ".sql"
		subprocess.run(dumpcmd, shell=True)
		# Un print pour voir ce qui est clairement saisie.
		print("Fin de la restauration MySQL.")
	except:
		# MySQLdump peut générer des erreurs mais poursuivre correctement malgré tout...
		print("Problème avec le bloque MySQLdump. Le script continue quand même.")


	shutil.rmtree(temp_directory)
	print("")
	print("Fin de la restauration.")
#	os.remove("/home/debian/svg.py")



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


# Appel de la fonction pour sauvegarder.
#create_tmp_save(deb, name_of_backup, temp_directory)
#sql_save(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH)
#copy(files_in_site, temp_directory)
#compress_clean(deb, temp_directory, name_of_backup)

# Appels des fonctions pour restaurer.
#create_tmp_restore(deb, name_of_backup, temp_directory)
#crash(files_in_site)
#extract(deb, name_of_backup, temp_directory)
#restauration(files_to_restore, site_directory, temp_directory)
#sql_restore(DB_HOST, DB_USER, DB_USER_PASSWORD, DB_NAME, BACKUP_PATH)
