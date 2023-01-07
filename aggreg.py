#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importation des modules sys,feedparser,yaml,datetime et os.path
import feedparser
import sys
import yaml
import os.path as op
from datetime import datetime


def charger(url):
    """
    Cette fonction charge un document RSS a partir d'une URL.
    """
    return feedparser.parse(url)


def charge_urls(liste_url):
    """
    Cette fonction recupere des documents RSS charges a partir d'URLs
    saisis en arguments sur la ligne de commandes. Ces documents RSS
    sont ensuite tries dans une liste (None si URL inaccessible)
    qui est renvoyee.
    """
    # On cree une liste de documents RSS
    res = []

    # Pour chaque URL
    for url in liste_url:

        # On charge le document RSS
        try:
            res.append(charger(url))

        # Si erreur, on ajoute None
        except:
            res.append(None)

    return res


def fusion_flux(liste_url, liste_flux, tri_chrono):
    """
    Cette fonction recupere la liste d'URLs et une liste de documents RSS
    (par exemple produite par la fonction charge_urls). La sortie est une
    liste dont chaque element est un dictionnaire decrivant un evenement
    d'un des sites (Les evenements sont triés selon la valeur de tri_chrono).
    """

    res = []

    # Pour chaque flux RSS
    for flux in range(len(liste_flux)):

        # Definition nom serveur
        serveur = liste_url[flux].split("/")[2]

        for i in range(len(liste_flux[flux].entries)):

            item = liste_flux[flux].entries[i]

            # On recupere les evenements et si un des elements n'est pas assigne on affiche "Not an event"
            try:
                res.append({"titre": item.title,
                            "categorie": item.category,
                            "serveur": serveur,
                            "date_publi": item.published,
                            "lien": item.link,
                            "description": item.description})
            except:
                print("Not an event")

    # Triage de la liste par date du la plus récente a la plus ancienne
    res = sort_list_dict_datetimes(res, tri_chrono)
    return res


def sort_list_dict_datetimes(list, tri_chrono):
    """
    Cette fonction renvoie une liste de dictionnaires triée a partir d'une liste
    de dictionnaires contenant des date au format rfc822 sans la timezone de la date
    la plus recente a la plus ancienne ou l'inverse selon tri_chrono
    """
    # Definition de notre cle qui contient chaque date
    cle_date = "date_publi"

    # Pour chaque dico
    for dico in range(len(list)):

        # Conversion de chaque date en element de type datetime pour les trier
        list[dico][cle_date] = datetime.strptime(
            list[dico][cle_date], "%a, %d %b %Y %H:%M")

    # Triage sur le critere de la date puis inversion du sens
    return sorted(list, key=lambda x: x[cle_date], reverse=tri_chrono)


def yaml_to_dict_config(yaml_config):
    """
    Cette fonction charge le fichier de configuration YAML et renvoie le dictionnaire correspondant
    """
    with open(yaml_config, "r") as conf:
        return yaml.safe_load(conf)

def scriptjs(path):
    """
    Cette fonction produit un fichier script.js dans le dossier de destination
    """
    with open(path+"script.js", "w") as js:
        js.write("""
    function pause(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    }
    async function afficherDate() {
      while (true) {
        await pause(1000);
        var cejour = new Date();
        var options = {
          weekday: "long",
          year: "numeric",
          month: "long",
          day: "2-digit",
        };
        var date = cejour.toLocaleDateString("fr-FR", options);
        var heure =
          ("0" + cejour.getHours()).slice(-2) +
          ":" +
          ("0" + cejour.getMinutes()).slice(-2) +
          ":" +
          ("0" + cejour.getSeconds()).slice(-2);
        var dateheure = date + " " + heure;
        var dateheure = dateheure.replace(
          /(^\w{1})|(\s+\w{1})/g,
          (lettre) => lettre.toUpperCase()
        );
        document.getElementById("current_date").innerHTML = dateheure;
      }
    }
    afficherDate();
""")

def stylecss(path):
    """
    Cette fonction produit un fichier feed.css dans le dossier de destination
    """
    with open(path+"feed.css", "w") as css:
        css.write("""body{
    margin: 0;
    padding: 0;
    background-color: #001330;
}

#top_header{
    width: 100%;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* background-image: linear-gradient(#000b1b, #002152); */
    background-color: #00398F;
}

h1 {
    margin: 0;
    font-size: 2em;
    font-family: "calibri", sans-serif;
    text-align: center;
    color: #fff;
}

#current_date{
    margin: 10px 0;
    font-size: 1.35em;
    font-family: "calibri", sans-serif;
    text-align: center;
    color: #fff;
}

a {
    text-decoration: underline;
    color: #0096c7;

}

a:hover {
    font-weight: bold;
    cursor: pointer;
}

.container{
    height: auto;
    width: 100%;
    padding: 50px 0;
    display: grid;
    grid-template-columns: repeat(auto-fit,400px);
    grid-gap: 30px;
    justify-content: center;
}

    article{
        width: 100%;
        background-color: #001e4a;
        /* overflow: hidden; */
        border-radius: 5px;
    }

        article > header{
            width: 100%;
            padding: 10px 0;
            background-color: #00398F;
            /* box-shadow: 0 0 5px 1px #000; */
            border-radius: 5px;
        }

            h2{
                margin: 0;
                font-size: 1.5em;
                font-family: "calibri", sans-serif;
                text-align: center;
                color: #fff;
            }

        p{
            margin: 10px 30px;
            font-size: 1em;
            font-family: "calibri", sans-serif;
            text-align: left;
            color: #fff;
        }


""")

def genere_html(liste_evenements, chemin_html):
    """
    Cette fonction produit un fichier html dans chemin_html contenant les evenements de
    la liste d'evenements
    """
    chemin_html+="index.html"
    with open(chemin_html, "w") as out:
        out.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Events log</title>
    <link rel="stylesheet" href="feed.css" type="text/css" />
  </head>
  <body>
    <div>
      <header id="top_header">
        <h1>Events log</h1>
      </header>

      <p id="current_date">...</p>

      <!-- importation script.js -->
      <script src="script.js" type="text/javascript"></script>
      
      <!-- liste des evenements (items du flux RSS). Un bloc <article> par item dans le flux -->
      <div class="container">""")

    with open(chemin_html, "a") as out:

        # Pour chaque event log   
        for event in liste_evenements:

            # Definition couleur pour balise css color
            color = ""
            category = event["categorie"]
            if category == "MINOR":
                color = 'green;">'
            elif category == "MAJOR":
                color = 'orange;">'
            else:
                color = 'red;">'

            # Ecriture du bloc <article>
            contenu = f"""<article>
            <header>
            <h2>{event['titre']}</h2>
            </header>
            <p>from: {event['serveur']}</p>
            <p>{event['date_publi']}</p>
            <p style="color:{color}{category}</p>

            <p><a href="{event['lien']}" target="blank">{event['lien']}</a></p>

            <p>{event['description']}</p>
            </article>"""

            out.write(contenu)

    # Fermeture des balises html
    with open(chemin_html, 'a') as out:
        out.write("""</div>
        </body>
    </html>""")

def correction_url(url):
    """
    Cette fonction corrige l'url pour qu'elle soit valide
    """
    # Si l'url ne contient / final, on l'ajoute
    if url[-1] != "/":
        url += "/"

    # remplace les \ par des / dans l'url
    url = url.replace("\\", "/")

    return url
def creation_config():
    """
    Cette fonction permet de creer un fichier de configuration pas a pas pour la premiere utilisation
    """
    # Si le fichier de configuration n'existe pas
    if not op.exists("config.yaml"):

        # On cree un fichier de configuration
        print("Vous n'avez pas de fichier config.yaml, creation du fichier en cours...")
        with open("config.yaml", "w") as conf:

            # On ecrit le fichier de configuration
            nbr_url = int(input("Combien de sources URL avez vous ?: "))
            conf.write("sources:\n")

            for i in range(nbr_url):
                # Ajout du / en fin d'url si absent
                url = input("Saisissez votre URL "+str(i+1)+": ")

                # Correction de l'url
                url=correction_url(url)
                
                # Ecriture de l'url dans la config yaml
                conf.write("\n- "+url)

            conf.write("\nrss-name: " +
                       input("Saisissez votre nom de fichier rss-name: "))

            destination = input(
                "Saisissez le chemin de destination du fichier html (ne pas inclure le fichier): ")
            
            # Correction du chemin de destination
            destination=correction_url(destination)

            conf.write(
                "\ndestination: "+destination)

            tri_chrono = input("Saisissez tri-chrono[true/false]: ")
            while tri_chrono not in ("true", "false"):
                print("Saisissez true ou false")
                tri_chrono = input("Saisissez tri-chrono[true/false]: ").lower()

            conf.write("\ntri-chrono: "+tri_chrono)


def main():
    """
    Cette fonction est appelee lors du lancement du programme.
    Elle affiche les documents RSS chargees a partir des URLs
    saisies en arguments sur la ligne de commandes.
    """
    # On recupere les arguments de la ligne de commande
    #liste_url = []
    # for arg in sys.argv[1:]:

    # On ajoute l'URL a la liste
    # liste_url.append(arg)

    # On charge les documents RSS
    #liste_rss = charge_urls(liste_url)

    # On affiche les documents RSS
    # for rss in liste_rss:
    #     if rss != None:
    #         print(rss)


    # Chargement de la config YAML
    if len(sys.argv)==2: 
        #Si l'utilisateur spécifie un fichier config
        config=yaml_to_dict_config(sys.argv[-1])
    else:
        #Sinon le fichier config par défaut est utilisé 
        config = yaml_to_dict_config("/etc/config.yaml") 

    liste_url = config["sources"]
    rss_name = config["rss-name"]
    destination = config["destination"]
    tri_chrono=config["tri-chrono"]
    liste_rss = []

    # Preparation de la liste des doc RSS
    for i in range(len(liste_url)):

        # Construction des liens vers les docs (URL+Nom_RSS)
        liste_rss.append(liste_url[i]+rss_name)

    # Chargement de chaque flux RSS dans la liste
    liste_rss = charge_urls(liste_rss)

    # generation des fichiers js, css et html
    scriptjs(destination)
    stylecss(destination)
    genere_html(fusion_flux(liste_url, liste_rss, tri_chrono), destination)


main()
