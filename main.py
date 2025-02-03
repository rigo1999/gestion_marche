#fichier main
# Importation des classes et bibliotheques
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
from datetime import datetime

from pymongo import MongoClient
from _classe import HistoriqueVentes, Produit
from _classe import Marchand
from _classe import Marche
from _classe import Utilisateur

#from _classe import BaseDeDonnees
from _classe import notifier
from _classe import afficher_menu

client = MongoClient("mongodb://localhost:27017/")


def main():
    # Stockage des marchés dans un dictionnaire (clé : nom du marché)
    marches = {}

    while True:
        afficher_menu()
        choix = input("Sélectionnez une option (1-8) : ")

        if choix == "1":
            print("\n=== Création de marchés ===")
            while True:
                nom_marche = input("Entrez le nom du marché : ")
                taille_x = int(input("Entrez la largeur du marché : "))
                taille_y = int(input("Entrez la longueur du marché : "))
                
                #instance of marche
                marche = Marche(nom_marche, taille_x, taille_y,marchand_id=None) 
                #insert marche in db
                db = client["market_bd"]
                collection = db["marches"]
                collection.insert_one(marche.__dict__)

                #marches[nom_marche] = Marche(taille_x, taille_y)
                print(f"Marché '{nom_marche}' créé avec succès.")

                # Demander à l'utilisateur s'il souhaite ajouter un autre marché
                continuer = input("Voulez-vous créer un autre marché ? (o/n) : ").lower()
                if continuer != "o":
                    break
                

        elif choix == "2":
            print("\n=== Ajout d'un marchand ===")

            #nom_marche = input("Nom du marché : ")
            #obtenir marche
            #choose the market where to add the marchand
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]
            
            collection = db["marches"]
            
            #  listemarche disponible
            print("Les marchés disponibles sont :")
            for doc in collection.find():
                i=1
                print(f"{i}. {doc['nom_marce']}")
                i+=1
            #choose the market
            nom_marche = input("Entrer le nom du marche du marchand : ")
            #obtenir marche
            db = client["market_bd"]
            collection = db["marches"]
            marche = collection.find_one({"nom_marce": nom_marche})
            print(marche)
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue
            marche_id = marche["_id"]
            nom_marchand = input("Nom du marchand : ")
            position_x = int(input("Position X du marchand : "))
            position_y = int(input("Position Y du marchand : "))
            marchand = Marchand(nom_marchand, (position_x, position_y), marche_id)

            #add marchand to the marchand
            marchand_id = db["marchands"].insert_one(marchand.__dict__).inserted_id
            detail_marchand = {"nom": nom_marchand, "position": (position_x, position_y),"marchand_id": marchand_id}
            #add marchand  detail_marchand in marche in db
            db["marches"].update_one(
            {"nom_marce": nom_marche},  # Query to find the document
            {"$set": {f"detail_marchand.{nom_marchand}": detail_marchand}} )
       
        
            #marche.ajouter_marchand(marchand)
            notifier(f"Marchand '{nom_marchand}' ajouté au marché '{nom_marche}'.")
            #voulez vous ajouter des produit pour ce marchand
            choix_produit = input("Voulez-vous ajouter des produits pour ce marchand ? (o/n) : ").lower()
            if choix_produit == "o":
                while True:
                    
                    nom_produit = input("Nom du produit : ")
                    prix = float(input(f"Prix de {nom_produit} : "))
                    quantite = int(input(f"Quantité de {nom_produit} : "))
                    produit = Produit(nom_produit, prix, quantite, marchand_id)
                    db["produits"].insert_one(produit.__dict__)
                    
                    notifier(f"Produit '{nom_produit}' ajouté au stock de '{nom_marchand}'.")

                    continuer = input("Ajouter un autre produit ? (o/n) : ").lower()
                    if continuer != "o":
                        break
                    else:
                        continue
            else:
                continue


        elif choix == "3":
            print("\n=== Ajout de produits ===")

            db = client["market_bd"]
            collection = db["marches"]
            #  listemarche disponible
            print("Les marchés disponibles sont :")
            for doc in collection.find():
                i=1
                print(f"{i}. {doc['nom_marce']}")
                i+=1
            #choose the market
            nom_marche = input("Nom du marché : ")
            #verifier si le marchan =t existe

            marche = collection.find_one({"nom_marce": nom_marche})
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue
            nom_marchand = input("Nom du marchand : ")
            #verifier si le marchand existe
            marchand = db["marchands"].find_one({"nom": nom_marchand})
            #get the id of the marchand

            if not marchand:
                print(f"Aucun marchand nommé '{nom_marchand}' trouvé dans le marché '{nom_marche}'.")
                continue
            while True:
                nom_produit = input("Nom du produit : ")
                prix = float(input(f"Prix de {nom_produit} : "))
                quantite = int(input(f"Quantité de {nom_produit} : "))
                produit = Produit(nom_produit, prix, quantite, marchand["_id"])
                db["produits"].insert_one(produit.__dict__)
                
                notifier(f"Produit '{nom_produit}' ajouté au stock de '{nom_marchand}'.")

                continuer = input("Ajouter un autre produit ? (o/n) : ").lower()
                if continuer != "o":
                    break
                else:
                        continue

        elif choix == "4":
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]

            print("\n=== Simulation d'achat ===")
            nom_marche = input("Nom du marché : ")

            # Vérifier si le marché existe
            collection_marches = db["marches"]
            marche = collection_marches.find_one({"nom_marce": nom_marche})
            print('marche',marche)
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
            else:
                position_client = (
                    int(input("Position X du client : ")),
                    int(input("Position Y du client : "))
                )
                liste_produits = []
                while True:
                    nom_produit = input("Nom du produit souhaité : ")
                    #check if the product exists in the db
                    produit = db["produits"].find_one({"nom": nom_produit})
                    if not produit:
                        print(f"Le produit '{nom_produit}' n'existe pas.")
                        continue
                    quantite = int(input(f"Quantité de {nom_produit} : "))
                    liste_produits.append({"nom": nom_produit, "quantite": quantite})
                    continuer = input("Ajouter un autre produit ? (o/n) : ").lower()
                    if continuer != "o":
                        break

                # Trouver les marchands et vérifier la disponibilité des produits
                collection_marchands = db["marchands"]
                collection_produits = db["produits"]
                
                for marchand in collection_marchands.find():
                    marchand_id = marchand["_id"]
                    produits_marchand = list(collection_produits.find({"marchand_id": marchand_id}))
                    
                    for produit in produits_marchand:
                        if produit["nom"] in [p["nom"] for p in liste_produits]:
                            print(f"Marchand : {marchand['nom']}")
                            print(f"Produit : {produit['nom']}, Quantité : {produit['quantite']}, Prix : {produit['prix']:.2f} €")
                            
                            acheter = input("Voulez-vous acheter ce produit ? (o/n) : ").lower()
                            if acheter == "o":
                                quantite_demande = next(p["quantite"] for p in liste_produits if p["nom"] == produit["nom"])
                                print("Requested quantity:", quantite_demande)
                                if produit["quantite"] >= quantite_demande:
                                    collection_produits.update_one({"_id": produit["_id"]}, {"$inc": {"quantite": -quantite_demande}})
                                    historique_vente = {
                                        "nom_produit": produit["nom"],
                                        "prix_total": produit["prix"] * quantite_demande,
                                        "quantite": quantite_demande,
                                        "marchand_id": marchand_id,
                                        "date": datetime.now()
                                    }
                                    db["historiques_marchand"].insert_one(historique_vente)
                                    print(f"Vous avez acheté {quantite_demande} {produit['nom']} pour {quantite_demande * produit['prix']:.2f} €.")
                                else:
                                    print("Quantité insuffisante.")

                # Recommandations
                recommendations = []
                for marchand in collection_marchands.find():
                    marchand_id = marchand["_id"]
                    total_cout = 0
                    produits_disponibles = True

                    for demande in liste_produits:
                        produit = collection_produits.find_one({"nom": demande["nom"], "marchand_id": marchand_id})
                        if produit and produit["quantite"] >= demande["quantite"]:
                            total_cout += produit["prix"] * demande["quantite"]
                        else:
                            produits_disponibles = False
                            break

                    if produits_disponibles:
                        distance = math.sqrt((marchand["position"][0] - position_client[0])**2 + (marchand["position"][1] - position_client[1])**2)
                        recommendations.append({
                            "marchand": marchand["nom"],
                            "position": marchand["position"],
                            "distance": distance,
                            "cout_total": total_cout
                        })

                recommendations.sort(key=lambda x: (x["cout_total"], x["distance"]))
                print("\n=== Marchands recommandés ===")
                for rec in recommendations:
                    print(f"- {rec['marchand']} : Coût = {rec['cout_total']:.2f} €, Distance = {rec['distance']:.2f}")

                choix_validation = input("\nSouhaitez-vous valider cet achat ? (o/n) : ").lower()
                if choix_validation == "o":
                    print("Transaction validée. Stock mis à jour.")
                else:
                    print("Transaction annulée.")



        elif choix == "5":

            print("\n=== Statistiques des marchands ===")

            while True:
                nom_marche = input("Nom du marché : ")
                client = MongoClient("mongodb://localhost:27017/")
                db = client["market_bd"]
                collection = db["marches"]
                
                marche = collection.find_one({"nom_marce": nom_marche})  # Corrected key name
                print("marche", nom_marche)
                
                if not marche:
                    print(f"Le marché '{nom_marche}' n'existe pas.")
                    continue
                
                print("\n=== Statistiques ===") 
                marche_id = marche["_id"]
                
                collection_marchands = db["marchands"]
                marchands = list(collection_marchands.find({"marchand_id": marche_id}))
                
                if not marchands:
                    print("Aucun marchand trouvé dans ce marché.")
                    continue
                
                for marchand in marchands:
                    print(f"Marchand : {marchand['nom']}")
                    #get the all the products with the marchand_id
                    collection_produits = db["produits"]
                    produits = list(collection_produits.find({"marchand_id": marchand["_id"]}))
                    print(f"Nombre de produits : {len(produits)}")
                    #get al the products in historiques_marchands with the marchand_id
                    collection_historiques = db["historiques_marchands"]
                    historiques = list(collection_historiques.find({"marchand_id": marchand["_id"]}))
                    print(f"Nombre de produits vendu : {len(historiques)}")
                    # get the total of the prix_total
                    total_ventes = sum(t["prix_total"] for t in historiques)
                    print(f"Total des ventes : {total_ventes:.2f} €")
                  
                    print()
                    
                    print("\n=== Statistiques des produits ===")
                    pr = list(collection_produits.find({"marchand_id": marchand["_id"]}))
                    for produit in pr:
                        print(f"Produit : {produit['nom']}, Prix : {produit['prix']:.2f} €, Quantité : {produit['quantite']}")
                    print("-------------------------------------------------")
                    
                        
                
        elif choix == "6":
            print("\n=== Visualisation de la carte des marchands ===")
            nom_marche = input("Nom du marché : ")
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]
            collection = db["marches"]
            marche = collection.find_one({"nom_marce": nom_marche})
            print(marche)
         
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue

            # Afficher la carte des marchands
            
            Marche.generer_carte_interactive(nom_marche)


        elif choix == "7":
            print("\n=== Affichage des stocks ===")
            nom_marche = input("Nom du marché : ")
            marche = marches.get(nom_marche)
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue
            marche.afficher_stock_graphique()

        elif choix == "8":
            print("Merci d'avoir utilisé l'application. À bientôt !")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()

   
