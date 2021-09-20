# Projet 6 et 9, sauvegarde wordpress.

# .yaml -> fichier de configuration.
# tryexcept -> à mettre sur les commandes à tester.
# python3 svg.py fichier_de_conf

# Les imports.
import os
import shutil
import tarfile
import subprocess

# Fonction de sauvegarde.
def save(temp_dir_save):

	# Chemin debian home.
	deb = '/home/debian/'

	# Création du dossier temporaire pour travailler dedans par simplicité.
	if os.path.exists(deb + temp_dir_save + '.tar.gz') == True:
		exit("L'archive " + temp_dir_save + ".tar.gz existe déjà ! Fin du script, aucune sauvegarde effectuée.")
	elif os.path.exists(deb + temp_dir_save) == False:
		os.mkdir(deb + temp_dir_save)
	else:
		exit("Le dossier temporaire existe déjà ! Fin du script, aucune sauvegarde effectuée.")

	# Variable du dossier temporaire.
	directory_where_save = deb + temp_dir_save + '/'

	### ### ### MySQLdump, début. ### ### ###
	# Les constantes
	DB_HOST = 'localhost' 
	DB_USER = 'root'
	DB_USER_PASSWORD = 'debian'
	DB_NAME = 'wordpress'
	BACKUP_PATH = deb + temp_dir_save + '/'

	# La ligne de code qui sera exécutée par subprocess.
	dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + BACKUP_PATH + DB_NAME + ".sql"
	# os.system(dumpcmd) fonctionne aussi, mais c'est une commande qui sera bientôt obsolète.
	subprocess.run(dumpcmd, shell=True)

	# Un print pour voir ce qui est clairement saisie.
	print(dumpcmd)
	### ### ### MySQLdump, fin. ### ### ###

	# On met tous les fichiers à sauvegarder dans un tableau.
	files_to_save = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess']

	# On fait le tour du tableau avec la boucle for.
	print("")
	print("Début de la copie.")
	for file_or_dir in files_to_save:
		# On contrôle si c'est un dossier ou un fichier. Si c'est un dossier on utilise shutil.copytree(src, dst), si c'est un fichier on utilise copyfile(src, dst). En dst, on prend le chemin du dossier temporaire + le nom du dossier ou fichier à copier. On doit donner chemin de destination ainsi qu'un nom d'élément une fois copier, sinon on perd 4 jours sur cette commande !
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

	# La compression.
	output_filename = temp_dir_save + '.tar.gz'
	# La condition permet seulement de savoir si le dossier existe déjà. Si oui, on aura un bug !
	if os.path.isfile(deb + output_filename) == True:
		print("Le fichier existe déjà.")
	else:
		# Instruction pour le tar.gz.
		print("Début de la compression.")
		with tarfile.open(deb + output_filename, "w:gz") as tar:
			tar.add(directory_where_save, os.path.basename(directory_where_save))
		print("Compression terminée.")
		print("")

	# Suppression du dossier temporaire.
	shutil.rmtree(directory_where_save)
	print("Backup terminée avec succès !")





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
save('Backup_P6')
#restore('Backup_P6')
