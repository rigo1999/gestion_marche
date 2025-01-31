#fichier main
# Importation des classes et bibliotheques
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
from datetime import datetime

from pymongo import MongoClient
from _classe import Produit
from _classe import Marchand
from _classe import Marche
from _classe import Utilisateur
from _classe import Transaction
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
                    break


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
            print("\n=== Simulation d'achat ===")
            nom_marche = input("Nom du marché : ")
            #verifier si le marchan =t existe
            bd = client["market_bd"]
            collection = bd["marches"]
            marche = collection.find_one({"nom_marce": nom_marche})
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue
            position_client = (
                int(input("Position X du client : ")),
                int(input("Position Y du client : "))
            )
            liste_produits = []
            while True:
                nom_produit = input("Nom du produit souhaité : ")
                quantite = int(input(f"Quantité de {nom_produit} : "))
                liste_produits.append({"nom": nom_produit, "quantite": quantite})
                continuer = input("Ajouter un autre produit ? (o/n) : ").lower()
                if continuer != "o":
                    break
                else:
                    continue
                #find the marchand with the products
            marchand = db["marchands"].find()
            for marchand in marchand:
                marchand_id = marchand["_id"]
                produits = db["produits"].find({"marchand_id": marchand_id})
                for produit in produits:
                    if produit["nom"] in [produit["nom"] for produit in liste_produits]:
                        print(f"Marchand : {marchand['nom']}")
                        print(f"Produit : {produit['nom']}, Quantité : {produit['quantite']}, Prix : {produit['prix']:.2f} €")
                        #print(f"Nombre de ventes : {len([t for t in marchand['historique_ventes'] if t['produit'] == produit['nom']])}")
                        print()
                        continuer = input("Voulez-vous acheter ce produit ? (o/n) : ")
                        if continuer == "o":
                            #update the marchand's stock and the client's cart
                            db["marchands"].update_one({"_id": marchand_id}, {"$inc": {"stock": -quantite}})
                            #db["clients"].update_one({"_id": client_id}, {"$inc": {"cart": quantite}})
                            print(f"Vous avez acheté {quantite} {produit['nom']} pour {quantite * produit['prix']:.2f} €.")
                            break
                        else:
                            continue
                    else:
                        continue
               
                
                recommendations = marche.optimiser_achats(position_client, liste_produits)
            print("\n=== Marchands recommandés ===")
            for rec in recommendations:
                print(f"- {rec['marchand']} : Coût = {rec['cout_total']:.2f} €, Distance = {rec['distance']:.2f}")

            choix_validation = input("\nSouhaitez-vous valider cet achat ? (o/n) : ").lower()
            if choix_validation == "o":
                # Débit du stock
                for demande in liste_produits:
                    for rec in recommendations:
                        marchand = next((m for m in marche.positions.values() if m.nom == rec["marchand"]), None)
                        produit = next((p for p in marchand.stock if p.nom == demande["nom"]), None)
                        if produit:
                            produit.quantite -= demande["quantite"]
                print("Transaction validée. Stock mis à jour.")
            else:
                print("Transaction annulée.")

        elif choix == "5":
            print("\n=== Statistiques des marchands ===")
            nom_marche = input("Nom du marché : ")
            db = client["market_bd"]
            collection = db["marches"]
            marche = collection.find_one({"nom": nom_marche})
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue
            print("\n=== Statistiques ===")
            for marchand in marche["detail_marchand"]:
                print(f"Marchand : {marchand['nom']}")
                print(f"Nombre de produits : {len(marchand['stock'])}")
                print(f"Nombre de transactions : {len(marchand['historique_ventes'])}")
                print(f"Total des ventes : {sum([t['montant'] for t in marchand['historique_ventes']]):.2f} €")
                print()
                print("\n=== Statistiques des produits ===")
                for produit in marchand["stock"]:
                    print(f"Produit : {produit['nom']}, Quantité : {produit['quantite']}, Prix : {produit['prix']:.2f} €")
                    print(f"Nombre de ventes : {len([t for t in marchand['historique_ventes'] if t['produit'] == produit['nom']])}")


            marche = marches.get(nom_marche)  # Récupérer le marché sélectionné
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue

            nom_marchand = input("Nom du marchand : ")
            marchand = next((m for m in marche.positions.values() if m.nom == nom_marchand), None)
            if not marchand:
                print(f"Aucun marchand nommé '{nom_marchand}' trouvé dans le marché '{nom_marche}'.")
                continue

            # Afficher les statistiques du marchand
            marchand.afficher_historique_ventes()
            marchand.statistiques()

        elif choix == "6":
            print("\n=== Visualisation de la carte des marchands ===")
            nom_marche = input("Nom du marché : ")
            marche = marches.get(nom_marche)
            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                continue

            # Afficher la carte des marchands
            marche.generer_carte_interactive()


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

   
