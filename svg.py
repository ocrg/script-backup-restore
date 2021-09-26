#!/usr/bin/python3.9
# -*-coding:utf-8 -*

# Projet 6 et 9, sauvegarde wordpress.

# .yaml -> fichier de configuration.
# python3 svg.py fichier_de_conf

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Les imports.
import os
import shutil
import tarfile
import subprocess

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Fonction de sauvegarde.
def save(temp_dir_save):


	try :
		#	CONSTANTES DES CHEMINS
		# Constante du chemin de home.
		deb = '/home/debian/'
		# Constante du chemin du dossier temporaire.
		directory_where_save = deb + temp_dir_save + '/'
	except:
		exit("Problème avec la création des constantes des chemins.")


	try:
		#	CRÉATION DOSSIER TEMPORAIRE
		# Création du dossier temporaire pour travailler dedans par simplicité.
		if os.path.exists(deb + temp_dir_save + '.tar.gz') == True:
			exit("L'archive " + temp_dir_save + ".tar.gz existe déjà ! Fin du script, aucune sauvegarde effectuée.")
		elif os.path.exists(deb + temp_dir_save) == False:
			os.mkdir(deb + temp_dir_save)
		else:
			exit("Le dossier temporaire existe déjà ! Fin du script, aucune sauvegarde effectuée.")
	except:
		shutil.rmtree(directory_where_save)
		exit("Problème avec la création du dossier temporaire.")


	try:
		#	CONSTANTES MYSQL
		# Les constantes
		DB_HOST = 'localhost'
		BACKUP_PATH = deb + temp_dir_save + '/'
		DB_USER = 'root'
		DB_USER_PASSWORD = 'debian'
		DB_NAME = 'wordpress'
	except:
		print("Problème dans la création des constantes de MySQLdump.")


	try:
		#	MYSQLDUMP
		# La ligne de code qui sera exécutée par subprocess.
		dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + BACKUP_PATH + DB_NAME + ".sql"
		# os.system(dumpcmd) fonctionne aussi, mais c'est une commande qui sera bientôt obsolète.
		subprocess.run(dumpcmd, shell=True)

		# Un print pour voir ce qui est clairement saisie.
		print(dumpcmd)
	except:
		# MySQLdump peut générer des erreurs mais poursuivre correctement malgré tout...
		print("Problème avec le bloque MySQLdump. Le script continue quand même.")


	try:
		#	COPIE
		# On met tous les fichiers à sauvegarder dans un tableau.
		files_to_save = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess']

		# On fait le tour du tableau avec la boucle for.
		print("")
		print("Début de la copie.")
		for file_or_dir in files_to_save:
			# On contrôle si c'est un dossier ou un fichier. Un dossier = shutil.copytree(src, dst), un fichier = shutil.copyfile(src, dst).
			# En dst, on indique le chemin du dossier de destination (logique) + le nom du dossier ou fichier à copier (logique mais moins évident). D'où l'utilisation d'os.path.basename !
			# os.path.basename() nous renvoie le nom du dernier élément d'un chemin, et avec son extention. Donc ça nous donne 'wp-config.php' par exemple. Pratique !

			# Si c'est un dossier et qu'il n'existe pas dans le dossier temporaire :
			if os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
				shutil.copytree(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
			# Si c'est un fichier et qu'il n'existe pas dans le dossier temporaire :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
				shutil.copyfile(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
			# Si c'est un dossier et qu'il existe déjà dans le dossier temporaire :
			elif os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
				print("Ce dossier existe déjà dans le dossier temporaire : " + file_or_dir)
			# Si c'est un fichier et qu'il existe déjà dans le dossier temporaire :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
				print("Ce fichier existe déjà dans le dossier temporaire : " + file_or_dir)			
			# Si anomalie :
			else:
				print("Il y a eu un problème avec" + file_or_dir)
		print("Fin de la copie.")
		print("")
	except:
		shutil.rmtree(directory_where_save)
		exit("Problème avec le bloque de copie.")


	try:
		#	COMPRESSION
		# Compression. Instruction pour le tar.gz.
		print("Début de la compression.")
		with tarfile.open(deb + temp_dir_save + '.tar.gz', "w:gz") as tar:
			tar.add(directory_where_save, os.path.basename(directory_where_save))
		print("Compression terminée.")
		print("")
	except:
		shutil.rmtree(directory_where_save)
		exit("Problème avec le bloque tarfile.")


	try:
		#	SUPPRESSION DOSSIER TEMPORAIRE
		# Suppression du dossier temporaire.
		shutil.rmtree(directory_where_save)
		print("Backup terminée avec succès !")
	except:
		exit("Problème avec le bloque de suppression du dossier temporaire.")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def restore(temp_dir_restore):


	try:
		#	CONSTANTES DES CHEMINS
		# Chemin debian home.
		deb = '/home/debian/'
		directory_where_restore = deb + temp_dir_restore + '/'
	except:
		exit("Problème avec la création des constantes.")


	try:
		#	CRÉATION DU DOSSIER TEMPORAIRE
		# Création du dossier temporaire pour travailler dedans par simplicité.
		if os.path.exists(directory_where_restore) == False:
			os.mkdir(directory_where_restore)
		else:
			exit("Le dossier temporaire existe déjà ! Fin du script.")
	except:
		exit("Problème avec la création du dossier, il semble qu'il existe déjà.")


	try:
		#	DÉCOMPRESSION
		# Décompression. Instruction pour le tar.gz.
		print("Début de la décompression...")
		with tarfile.open(deb + temp_dir_restore + '.tar.gz') as tar:
			tar.extractall(directory_where_restore)
		print("Décompression terminée.")
		print("")
	except:
		shutil.rmtree(directory_where_restore)
		exit("Problème lors de la décompression. Fin du script.")


	try:
		#	SUPPRESSION
		# Tableau des fichiers existants sur le serveur et qui seront supprimé.
		# Ce tableau sera ensuite utilisé pour replacer les fichiers de l'archive à leur place sur le serveur.
		files_to_delete = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess']

		# On fait le tour du tableau avec la boucle for.
		print("Début de la suppression des fichiers existants...")
		for file_or_dir in files_to_delete:
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
				print("Ce fichier ou dossier semble avoir été supprimé : " + os.path.basename(file_or_dir))
			# S'il y a anomalie :
			else:
				print("Il y a eu un problème avec " + file_or_dir)
		print("Fin de la suppression.")
		print("")
	except:
		shutil.rmtree(directory_where_restore)
		exit("Problème avec le bloque de suppression.")


	try:
		#	REPLACEMENT
		# On fait un tableau qui contient les fichiers à remettre en place.
		files_to_copy = [directory_where_restore + 'wp-config.php',directory_where_restore + 'wp-content',directory_where_restore + '.htaccess']
		# Constante du chemin du dossier du site.
		site_directory = '/var/www/html/www.ocr.tp/'

		print("Début des replacements...")
		for file_or_dir in files_to_copy:
			# On contrôle si c'est un dossier ou un fichier. Un dossier = shutil.rmtree(), un fichier = os.remove().

			print("0")
			# Si c'est un dossier et qu'il n'existe pas dans /var, on le met dans /var :
			if os.path.isdir(file_or_dir) == True and os.path.exists(file_or_dir) == False:
				print("1")
				shutil.copytree(file_or_dir, site_directory + os.path.basename(file_or_dir))
				print("Dossier replacé : " + file_or_dir)
			# Si c'est un fichier et qu'il n'existe pas dans /var, on le met dans /var :
			elif os.path.isfile(file_or_dir) == True and os.path.exists(file_or_dir) == False:
				print("2")
				shutil.copyfile(directory_where_restore + os.path.basename(file_or_dir), site_directory + os.path.basename(file_or_dir))
				print("Fichier replacé : " + file_or_dir)
			# Si c'est un dossier qui existe déjà dans /var, on fait un message :
			elif os.path.exists(file_or_dir) == False:
				print("3")
				print("Ce fichier ou dossier semble avoir été supprimé : " + os.path.basename(file_or_dir))
			# S'il y a anomalie :
			else:
				print("4")
				print("Il y a eu un problème avec " + file_or_dir)

		print("Fin des replacements.")
		print("")
	except:
		print("Problème avec le bloque de replacement. Le script passe maintenant à la BDD.")

	shutil.rmtree(directory_where_restore)
	os.remove(deb + "svg.py")

#	try:
		#	CONSTANTES MYSQL
		# Les constantes
#		DB_HOST = 'localhost'
#		BACKUP_PATH = deb + temp_dir_save + '/'
#		DB_USER = 'root'
#		DB_USER_PASSWORD = 'debian'
#		DB_NAME = 'wordpress'
#	except:
#		print("Problème dans la création des constantes de MySQLdump.")


#	try:
		#	MYSQLDUMP
		# La ligne de code qui sera exécutée par subprocess.
#		dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + BACKUP_PATH + DB_NAME + ".sql"
		# os.system(dumpcmd) fonctionne aussi, mais c'est une commande qui sera bientôt obsolète.
#		subprocess.run(dumpcmd, shell=True)

		# Un print pour voir ce qui est clairement saisie.
#		print(dumpcmd)
#	except:
		# MySQLdump peut générer des erreurs mais poursuivre correctement malgré tout...
#		print("Problème avec le bloque MySQLdump. Le script continue quand même.")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

# Appel de la fonction. 

#save('Backup_P9')

restore('Backup_P9')
