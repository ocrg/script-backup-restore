# Projet 6 et 9, sauvegarde wordpress.

# Les imports
import os
import shutil
import tarfile
import pipes

# On fait une fonction.
def svg():

	# Création du dossier pour travailler dedans par simplicité.
	if os.path.exists('/home/debian/Backup_P6') == False:
		os.mkdir('/home/debian/Backup_P6')
	else:
		print("Le dossier 'Backup_P6' existe déjà.")

	# Variable du dossier.
	directory_where_save = '/home/debian/Backup_P6/'

	DB_HOST = 'localhost' 
	DB_USER = 'root'
	DB_USER_PASSWORD = 'debian'
	DB_NAME = 'wordpress'
	BACKUP_PATH = '/home/debian/Backup_P6/'

	dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " > " + pipes.quote(BACKUP_PATH) + "/" + DB_NAME + ".sql"

	print(dumpcmd)
	os.system(dumpcmd)

	print ("La BDD a été sauvegardée ici : " + BACKUP_PATH)

	# On met tous les fichiers à sauvegarder dans un tableau.
	files_to_save = ['/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess', '/home/debian/Backup_P6/' + DB_NAME + '.sql']

	# On fait le tour du tableau.
	print("Début de la copie.")
	for file_or_dir in files_to_save:
		# On contrôle si c'est un dossier ou un fichier.
		if os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
			shutil.copytree(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
		elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == False:
			shutil.copyfile(file_or_dir, directory_where_save + os.path.basename(file_or_dir))
		elif os.path.isdir(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
			print("Ce dossier existe déjà dans le dossier de destination.")
		elif os.path.isfile(file_or_dir) == True and os.path.exists(directory_where_save + os.path.basename(file_or_dir)) == True:
			print("Ce fichier existe déjà dans le dossier de destination.")			
		else:
			print("Il y a eu un problème avec", file_or_dir)
	print("Fin de la copie.")

# mysqldump à mettre en python
# mysqldump -u root -p wordpress --databases wordpress > /home/debian/svg.sql

# en argument le dossier Backup_P6 qui serai utilisé pour tarfile

# Compression, c'est clé en main, à adapter.
# def make_tarfile(output_filename, source_dir):
#    with tarfile.open(output_filename, "w:gz") as tar:
#        tar.add(source_dir, arcname=os.path.basename(source_dir))

	output_filename = 'Backup_P6.tar.gz'
	print("Début de la compression.")
	if os.path.isfile('/home/debian/' + output_filename) == True:
		print("Le fichier existe déjà.")
	else:
		# Instruction pour le tar.gz.
		with tarfile.open('/home/debian/' + output_filename, "w:gz") as tar:
			tar.add(directory_where_save, os.path.basename(directory_where_save))
	print("Compression terminée.")

	shutil.rmtree(directory_where_save)
	print("Backup terminée avec succès")

# Appel de la fonction.
svg()
