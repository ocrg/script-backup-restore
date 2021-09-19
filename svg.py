# Projet 6 et 9, sauvegarde wordpress.

# en argument le dossier Backup_P6 qui serai utilisé pour tarfile

# Les imports
import os
import shutil
import tarfile
import pipes

# On fait une fonction.
def svg(temp_dir):

	# Création du dossier temporaire pour travailler dedans par simplicité.
	if os.path.exists('/home/debian/Backup_P6') == False:
		os.mkdir('/home/debian/Backup_P6')
	else:
		print("Le dossier temporaire 'Backup_P6' existe déjà.")

	# Variable du dossier temporaire.
	directory_where_save = '/home/debian/Backup_P6/'

	### MySQLdump, début. ###
	# La ligne ci-dessous produit le même résultat si on la saisie : mysqldump -u root -p wordpress --databases wordpress > /home/debian/svg.sql
	# Les constantes
	DB_HOST = 'localhost' 
	DB_USER = 'root'
	DB_USER_PASSWORD = 'debian'
	DB_NAME = 'wordpress'
	BACKUP_PATH = '/home/debian/Backup_P6/'

	# La ligne de code.
	dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + pipes.quote(BACKUP_PATH) + DB_NAME + ".sql"
	os.system(dumpcmd)
	# Un print pour voir ce qui est clairement saisie.
	print(dumpcmd)
	### MySQLdump, fin. ###

	# On met tous les fichiers à sauvegarder dans un tableau. Le fichier SQL est déjà dans le dossier temporaire.
	files_to_save = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess']

	# On fait le tour du tableau.
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

	# La compression.
	output_filename = 'Backup_P6.tar.gz'

	if os.path.isfile('/home/debian/' + output_filename) == True:
		print("Le fichier existe déjà.")
	else:
		# Instruction pour le tar.gz.
		print("Début de la compression.")
		with tarfile.open('/home/debian/' + output_filename, "w:gz") as tar:
			tar.add(directory_where_save, os.path.basename(directory_where_save))
		print("Compression terminée.")

	# Suppression du dossier temporaire.
	shutil.rmtree(directory_where_save)
	print("Backup terminée avec succès !")

# Appel de la fonction.
svg()
