from collections import Counter
import csv
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urlparse
import requests



# ETAPE 1
def compter_mots(texte):
    diviseur_mot = texte.split()
    occurrences = Counter(diviseur_mot)
    trier_mots = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)

    return trier_mots

texte = input('entrez votre texte : ')
resultat = compter_mots(texte)

print("Résultat initial :", resultat)
print("===============================================================================")



# ETAPE 2
def extraire_parasites(texte, parasites):
    mots_texte = texte.split()
    mots_parasites = [mot.lower() for mot in mots_texte if mot.lower() in parasites]
    return list(set(mots_parasites))  





# ETAPE 3
def enlever_parasites(structure_donnees, mots_parasites):
    # Filtrer les mots parasites de la structure de données
    structure_filtree = [(mot, occurrence) for mot, occurrence in structure_donnees if mot.lower() not in mots_parasites]

    return structure_filtree

# Exemple d'utilisation
resultat = compter_mots(texte)  # Utilisez la fonction précédente pour obtenir la structure de données
mots_parasites = ["le", "la", "les", "de", "il", "elle", "un", "une", "des", "ce", "cette"]

resultat_filtre = enlever_parasites(resultat, mots_parasites)

# Afficher la structure de données résultante après avoir enlevé les mots parasites




# ETAPE 4
def ecrire_mots_parasites(fichier_csv, mots_parasites):
    try:
        with open(fichier_csv, 'w', newline='', encoding='utf-8') as fichier:
            writer_csv = csv.writer(fichier)
            writer_csv.writerow(mots_parasites)
        print(f"Les mots parasites ont été écrits dans {fichier_csv}.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'écriture dans le fichier CSV : {e}")




# ETAPE 5
def lire_mots_parasites(fichier_csv):
    mots_parasites = []

    try:
        with open(fichier_csv, 'r', encoding='utf-8') as fichier:
            lecteur_csv = csv.reader(fichier)
            for ligne in lecteur_csv:
                # Assurez-vous que la ligne contient au moins un élément
                if ligne:
                    mots_parasites.extend(ligne)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier CSV : {e}")

    print("Contenu du fichier CSV :", mots_parasites)  # Ajout d'une impression de débogage
    return mots_parasites




parasites = ["le", "la", "les", "de", "il", "elle", "un", "une", "des", "ce", "cette", "d'un", "d'une", "du"]

resultat = compter_mots(texte)
mots_parasites_texte = extraire_parasites(texte, parasites)
resultat_filtre = enlever_parasites(resultat, parasites)

print("Résultat filtré :", resultat_filtre)

print("===============================================================================")

fichier_parasite = "parasite.csv"
ecrire_mots_parasites(fichier_parasite, mots_parasites_texte)

mots_parasites_lus = lire_mots_parasites(fichier_parasite)

print("Mots parasites lus depuis le fichier CSV :", mots_parasites_lus)
print("===============================================================================")





# ETAPE 6
def retirer_balises_html(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    texte_sans_balises = soup.get_text(separator=' ', strip=True)
    return texte_sans_balises

html_randomurl = "<p>Ceci est un <b>exemple</b> de texte <a href='#'>HTML</a>.</p>"
texte_sans_balises = retirer_balises_html(html_randomurl)
print("Texte sans balises HTML :", texte_sans_balises)


print("===============================================================================")





# ETAPE 7
def recup_valeur_attribut(html, nom_balise, nom_attribut):
    valeurs = []

    soup = BeautifulSoup(html, 'html.parser')
    balises = soup.find_all(nom_balise)

    for balise in balises:
        valeur_attribut = balise.get(nom_attribut)
        if valeur_attribut:
            valeurs.append(valeur_attribut)

    return valeurs

html_img_randomurl = """
<html>
  <body>
    <img src="image1.jpg" alt="Image 1">
    <img src="image2.jpg" alt="Image 2">
    <img src="image3.jpg" alt="Image 3">
  </body>
</html>
"""

valeurs_alt_img = recup_valeur_attribut(html_img_randomurl, "img", "alt")
print(f"Valeurs des attributs 'alt' pour les balises 'img': {valeurs_alt_img}")



print("===============================================================================")



html_a_randomurl = """
<html>
  <body>
    <a href="lien1">Lien 1</a>
    <a href="lien2">Lien 2</a>
    <a href="lien3">Lien 3</a>
  </body>
</html>
"""

valeurs_href_a = recup_valeur_attribut(html_a_randomurl, "a", "href")
print(f"Valeurs des attributs 'href' pour les balises 'a': {valeurs_href_a}")


print("===============================================================================")




# ETAPE 8
def extraire_nom_domaine(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


url_randomurl = "https://esiee-it.blackboard.com/ultra/course"
nom_domaine = extraire_nom_domaine(url_randomurl)

print(f"Nom de domaine de l'URL '{url_randomurl}': {nom_domaine}")

print("===============================================================================")





#ETAPE 9 
def tri_url(nom_domaine, liste_urls):
    urls_du_domaine = []
    urls_hors_domaine = []

    for url in liste_urls:
        parsed_url = urlparse(url)
        domaine_url = parsed_url.netloc

        if domaine_url == nom_domaine:
            urls_du_domaine.append(url)
        else:
            urls_hors_domaine.append(url)

    return urls_du_domaine, urls_hors_domaine


nom_domaine_exemple = "www.randomurl.com"
urls_exemple = [
    "https://www.randomurl.com/page1",
    "https://www.randomurl.com/page2",
    "https://www.randomurl.yop/page3",
    "https://www.domaineaupif.com/page4",
]

urls_du_domaine, urls_hors_domaine = tri_url(nom_domaine_exemple, urls_exemple)

print(f"URLs faisant partie du domaine '{nom_domaine_exemple}': {urls_du_domaine}")


print("===============================================================================")


print(f"URLs ne faisant pas partie du domaine '{nom_domaine_exemple}': {urls_hors_domaine}")


print("===============================================================================")




#ETAPE 10
def recup_html_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        html = response.text
        return html
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
        return None





# ETAPE 11
def audit(url):
    html_page = recup_html_page(url)

    if html_page:
        soup = BeautifulSoup(html_page, 'html.parser')

        # Compter le nombre de balises <a>
        balises_a = len(soup.find_all('a'))

        # Compter le nombre de balises <img>
        balises_img = len(soup.find_all('img'))

        print(f"Audit de la page {url} :")
        print("===============================================================================")

        print(f"Nombre de balises <a> : {balises_a}")
        print("===============================================================================")

        print(f"Nombre de balises <img> : {balises_img}")
    else:
        print("Impossible de récupérer le contenu HTML de la page.")

# Exemple d'utilisation
url_audite = "https://esiee-it.blackboard.com/ultra/course"
audit(url_audite)


