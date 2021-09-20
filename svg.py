# Projet 6 et 9, sauvegarde wordpress.

# Les imports.
import os
import shutil
import tarfile
import subprocess

# Fonction de sauvegarde.
def save(temp_dir):

	# Création du dossier temporaire pour travailler dedans par simplicité.
	if os.path.exists('/home/debian/' + temp_dir + '.tar.gz') == True:
		exit("L'archive " + temp_dir + ".tar.gz existe déjà ! Fin du script, aucune sauvegarde effectuée.")
	elif os.path.exists('/home/debian/' + temp_dir) == False:
		os.mkdir('/home/debian/' + temp_dir)
	else:
		exit("Le dossier temporaire existe déjà ! Fin du script, aucune sauvegarde effectuée.")

	# Variable du dossier temporaire.
	directory_where_save = '/home/debian/' + temp_dir + '/'

	### MySQLdump, début. ###
	# Les constantes
	DB_HOST = 'localhost' 
	DB_USER = 'root'
	DB_USER_PASSWORD = 'debian'
	DB_NAME = 'wordpress'
	BACKUP_PATH = '/home/debian/' + temp_dir + '/'

	# La ligne de code.
	dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + BACKUP_PATH + DB_NAME + ".sql"
	os.system(dumpcmd)
#	subprocess.run(dumpcmd)

	# Un print pour voir ce qui est clairement saisie.
	print(dumpcmd)
	### MySQLdump, fin. ###

	# On met tous les fichiers à sauvegarder dans un tableau.
	files_to_save = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess']

	# On fait le tour du tableau.
	print("")
	print("Début de la copie.")
	for file_or_dir in files_to_save:
		# On contrôle si c'est un dossier ou un fichier.
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
	output_filename = temp_dir + '.tar.gz'

	if os.path.isfile('/home/debian/' + output_filename) == True:
		print("Le fichier existe déjà.")
	else:
		# Instruction pour le tar.gz.
		print("Début de la compression.")
		with tarfile.open('/home/debian/' + output_filename, "w:gz") as tar:
			tar.add(directory_where_save, os.path.basename(directory_where_save))
		print("Compression terminée.")
		print("")

	# Suppression du dossier temporaire.
	shutil.rmtree(directory_where_save)
	print("Backup terminée avec succès !")

# .yaml -> fichier de configuration.
# tryexcept -> à mettre sur les commandes à tester.
# python3 svg.py fichier_de_conf

# Appel de la fonction.
save('Backup_P6')

# restore()
