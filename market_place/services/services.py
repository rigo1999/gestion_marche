
from config import get_db_connection

db = get_db_connection()
marche_collection = db["marches"]

def ajouter_marche(nom, emplacement):
    marche = {"nom": nom, "emplacement": emplacement}
    marche_collection.insert_one(marche)
    print("Marché ajouté avec succès.")

# services/marchand_service.py
marchand_collection = db["marchands"]
 
def ajouter_marchand(nom, produit, prix, marche):
    marchand = {"nom": nom, "produit": produit, "prix": prix, "marche": marche}
    marchand_collection.insert_one(marchand)
    print("Marchand ajouté avec succès.")

# services/produit_service.py
produit_collection = db["produits"]

def ajouter_produit(nom, categorie):
    produit = {"nom": nom, "categorie": categorie}
    produit_collection.insert_one(produit)
    print("Produit ajouté avec succès.")

# services/achat_service.py
historique_collection = db["historique"]

def enregistrer_achat(marchand, produit, quantite, date):
    vente = {"marchand": marchand, "produit": produit, "quantite": quantite, "date": date}
    historique_collection.insert_one(vente)
    print("Achat enregistré avec succès.")