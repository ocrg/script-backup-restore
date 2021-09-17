# Projet 6 et 9, sauvegarde wordpress.

# Les imports
import os
import shutil
import tarfile

# On fait une fonction.
def svg():
# Après les tests, le contenu du tableau files_to_save sera le commentaire ci-dessous :
#	'/var/www/html/www.ocr.tp/wp-config-sample.php', '/var/www/html/www.ocr.tp/wp-config.php','/var/www/html/www.ocr.tp/wp-content','/var/www/html/www.ocr.tp/.htaccess','extract sql'


	#############	OK	################
	# Création du dossier pour travailler dedans par simplicité.
	if os.path.exists('/home/rick/Backup_P6') == False:
		os.mkdir('/home/rick/Backup_P6')
	else:
		print("Le dossier 'Backup_P6' existe déjà.")

	# On met tous les fichiers dans le tableau et on fait de sa première entrée une variable.
	files_to_save = ['/home/rick/Bureau/ocr.tp', '/home/rick/Bureau/OCR', '/home/rick/Bureau/Chill.xspf', '/home/rick/Bureau/Améliorer Gnome sur Debian', '/home/rick/Bureau/Pognon.ods', '/home/rick/Bureau/Linux.odt']

	# Idem avec notre répertoire de sauvegarde.
	directory_where_save = '/home/rick/Backup_P6/'

	# Tant que le tableau n'est pas vide, on copie de l'entrée 0.
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

	print("C\'est terminé !")

	#############	OK	################

# mysqldump à mettre en python
mysqldump -u root -p wordpress --databases wordpress > /home/debian/svg.sql

# en argument le dossier Backup_P6 qui serai utilisé pour tarfile

########### Compression, c'est clé en main, à adapter.
#def make_tarfile(output_filename, source_dir):
#    with tarfile.open(output_filename, "w:gz") as tar:
#        tar.add(source_dir, arcname=os.path.basename(source_dir))

	def make_tarfile("Backup_P6.tar.gz", directory_where_save):
		with tarfile.open("Backup_P6.tar.gz", "w:gz") as tar:
        		tar.add(directory_where_save, arcname = os.path.basename(directory_where_save))


# Appel de la fonction.
svg()
