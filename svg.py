#!/usr/bin/python3.9
# -*-coding:utf-8 -*

# Projet 6 et 9, sauvegarde wordpress.

# .yaml -> fichier de configuration.
# try: except: -> à mettre sur les commandes à tester.
# python3 svg.py fichier_de_conf

# Les imports.
import os
import shutil
import tarfile
import subprocess



# Fonction de sauvegarde.
def save(temp_dir_save):


	try :
		#	CONSTANTES DES CHEMINS
		# Chemin debian home.
		deb = '/home/debian/'
		# Variable du dossier temporaire.
		directory_where_save = deb + temp_dir_save + '/'
	except:
		exit("Problème : création des constantes des chemins.")


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
		exit("Problème : création du dossier temporaire.")


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
		print("Problème avec le bloque MySQLdump.")
		### ### ### MySQLdump, fin. ### ### ###


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
			if os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
				shutil.copytree(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
			elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
				shutil.copyfile(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
			elif os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
				print("Ce dossier existe déjà dans le dossier temporaire : " + file_or_dir)
			elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
				print("Ce fichier existe déjà dans le dossier temporaire : " + file_or_dir)			
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
		shutil.rmtree(directory_where_save)
		exit("Problème avec le bloque de suppression du dossier temporaire.")
























def restore(temp_dir_restore):

	# Chemin debian home.
	deb = '/home/debian/'

	# Création du dossier temporaire pour travailler dedans par simplicité.
	if os.path.exists(deb + temp_dir_restore) == False:
		os.mkdir(deb + temp_dir_restore)
	else:
		exit("Le dossier temporaire existe déjà ! Fin du script, aucune sauvegarde effectuée.")

	


	# Suppression du dossier temporaire.
	shutil.rmtree(directory_where_save)
	print("Backup terminée avec succès !")



# Appel de la fonction.
save('Backup_P9')

#restore('Backup_P6')
