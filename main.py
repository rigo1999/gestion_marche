#fichier main
# Importation des classes et bibliotheques
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
from datetime import datetime

from pymongo import MongoClient
from _classe import  Produit
from _classe import Marchand
from _classe import Marche,Vente
from _classe import Utilisateur

#from _classe import BaseDeDonnees
from _classe import notifier
from _classe import afficher_menu

client = MongoClient("mongodb://localhost:27017/")


def trouver_marche(db):
    return input("Nom du marché : ")

def obtenir_position_client():
    lat = float(input("Votre position (latitude) : "))
    lon = float(input("Votre position (longitude) : "))
    return (lat, lon)

def obtenir_liste_produits(db):
    liste_produits = []
    while True:
        nom_produit = input("Nom du produit souhaité : ")
        produit = db["produits"].find_one({"nom": nom_produit})
        if not produit:
            print(f"Le produit '{nom_produit}' n'existe pas.")
            continue
        quantite = int(input(f"Quantité de {nom_produit} : "))
        liste_produits.append({"nom": nom_produit, "quantite": quantite})
        if input("Ajouter un autre produit ? (o/n) : ").lower() != "o":
            break
    return liste_produits

def verifier_disponibilite_marchands(db, liste_produits):
    collection_marchands = db["marchands"]
    collection_produits = db["produits"]
    
    for marchand in collection_marchands.find():
        marchand_id = marchand["_id"]
        produits_marchand = list(collection_produits.find({"marchand_id": marchand_id}))
        
        for produit in produits_marchand:
            if produit["nom"] in [p["nom"] for p in liste_produits]:
                print(f"Marchand : {marchand['nom']}")
                print(f"Produit : {produit['nom']}, Quantité : {produit['quantite']}, Prix : {produit['prix']:.2f} €")
                
                if input("Voulez-vous acheter ce produit ? (o/n) : ").lower() == "o":
                    quantite_demande = next(p["quantite"] for p in liste_produits if p["nom"] == produit["nom"])
                    if produit["quantite"] >= quantite_demande:
                        collection_produits.update_one({"_id": produit["_id"]}, {"$inc": {"quantite": -quantite_demande}})
                        vente = {
                            "nom_produit": produit["nom"],
                            "prix_total": produit["prix"] * quantite_demande,
                            "quantite": quantite_demande,
                            "marchand_id": marchand_id,
                            "date": datetime.now()
                        }
                        db["ventes"].insert_one(vente)
                        db["historiques_marchand"].insert_one(vente)
                        print(f"Achat réussi : {quantite_demande} {produit['nom']} pour {quantite_demande * produit['prix']:.2f} €.")
                    else:
                        print("Quantité insuffisante.")

def recommander_marchands(db, liste_produits, position_client):
    collection_marchands = db["marchands"]
    collection_produits = db["produits"]
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
    
    return recommendations



def afficher_statistiques_marche():
    """Affiche les statistiques d'un marché et de ses marchands."""
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["market_bd"]
    
    while True:
        nom_marche = input("Nom du marché : ")
        collection_marches = db["marches"]
        
        # Vérifier si le marché existe
        marche = collection_marches.find_one({"nom_marce": nom_marche})
        if not marche:
            print(f"❌ Le marché '{nom_marche}' n'existe pas. Réessayez.\n")
            continue
        
        print(f"\n=== 📊 Statistiques du marché : {nom_marche} ===\n")
        
        marche_id = marche["_id"]
        collection_marchands = db["marchands"]
        marchands = list(collection_marchands.find({"marchand_id": marche_id}))
        
        if not marchands:
            print("⚠ Aucun marchand trouvé dans ce marché.")
            continue
        
        collection_produits = db["produits"]
        collection_historiques = db["historiques_marchand"]

        for marchand in marchands:
            print(f"\n🔹 Marchand : {marchand['nom']}")
            
            # Obtenir les produits du marchand
            produits = list(collection_produits.find({"marchand_id": marchand["_id"]}))
            nb_produits = len(produits)

            # Obtenir les historiques de ventes du marchand
            historiques = list(collection_historiques.find({"marchand_id": marchand["_id"]}))
            nb_vendus = len(historiques)
            total_ventes = sum(t["prix_total"] for t in historiques)

            print(f"   🏪 Nombre de produits en stock : {nb_produits}")
            print(f"   🛍 Nombre total de produits vendus : {nb_vendus}")
            print(f"   💰 Chiffre d'affaires total : {total_ventes:.2f} €\n")

            # Afficher les détails des produits
            print("   📦 Détails des produits :")
            for produit in produits:
                print(f"      - {produit['nom']}: {produit['prix']:.2f} € (Stock: {produit['quantite']})")
            
            print("\n" + "-"*50)

        # Option de quitter ou continuer
        if input("\n🔄 Voulez-vous consulter un autre marché ? (o/n) : ").lower() != "o":
            continue
        else:
            break

#Main function
def main():
    # Stockage des marchés dans un dictionnaire (clé : nom du marché)
    marches = {}

    while True:
        afficher_menu()
        choix = input("Sélectionnez une option (1-8) : ")

        if choix == "1":
            Marche.creer_marche()

        elif choix == "2":
            print("\n=== Ajout d'un marchand ===")
            Marche.ajouter_marchand()
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
            Produit.ajouter_produit()

        elif choix == "4":
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]
            
            print("\n=== Simulation d'achat ===")
            nom_marche = trouver_marche(db)
            position_client = obtenir_position_client()
            liste_produits = obtenir_liste_produits(db)
            
            verifier_disponibilite_marchands(db, liste_produits)
            recommendations = recommander_marchands(db, liste_produits, position_client)
            print(recommendations)
            if input("\nSouhaitez-vous valider cet achat ? (o/n) : ").lower() == "o":
                for rec in recommendations:
                    marchand_id = db["marchands"].find_one({"nom": rec["marchand"]})["_id"]
                    
                    for demande in liste_produits:
                        produit = db["produits"].find_one({"nom": demande["nom"], "marchand_id": marchand_id})

                        if produit and produit["quantite"] >= demande["quantite"]:
                            # Mise à jour de la quantité du produit
                            db["produits"].update_one(
                                {"_id": produit["_id"]},
                                {"$inc": {"quantite": -demande["quantite"]}}
                            )

                            # Enregistrement de la vente
                            vente = {
                                "nom_produit": produit["nom"],
                                "prix_total": produit["prix"] * demande["quantite"],
                                "quantite": demande["quantite"],
                                "marchand_id": marchand_id,
                                "date": datetime.now()
                            }
                            db["ventes"].insert_one(vente)

                            # Ajout de l'historique du marchand
                            historique_vente = {
                                "nom_produit": produit["nom"],
                                "prix_total": produit["prix"] * demande["quantite"],
                                "quantite": demande["quantite"],
                                "marchand_id": marchand_id,
                                "date": datetime.now()
                            }
                            db["historiques_marchand"].insert_one(historique_vente)

                            print(f"✅ {demande['quantite']} {produit['nom']} achetés chez {rec['marchand']} pour {vente['prix_total']:.2f} €.")
                
                print("Transaction validée. Stock mis à jour.")
            else:
                print("Transaction annulée.")



        elif choix == "5":

            print("\n=== Statistiques des marchands ===")
            afficher_statistiques_marche()

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
            
            #Marche.generer_carte_interactive(nom_marche)
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]
            collection_marches = db["marches"]
            collection_marchands = db["marchands"]
            collection_produits = db["produits"]
             

            # Recherche du marché dans la base de données
            marche = collection_marches.find_one({"nom_marce": nom_marche})

            if not marche:
                print(f"Le marché '{nom_marche}' n'existe pas.")
                exit()

            # Initialisation des listes pour les données
            noms_marchands = []
            positions_x = []
            positions_y = []
            couleurs = []

            # Récupérer tous les marchands du marché
            marchands = list(collection_marchands.find({"marchand_id": marche["_id"]}))

            if not marchands:
                print("Aucun marchand trouvé.")
                exit()

            for marchand in marchands:
                print("Marchand:", marchand)

                noms_marchands.append(marchand["nom"])
                positions_x.append(marchand["position"][0])
                positions_y.append(marchand["position"][1])

                # Récupérer les produits du marchand
                produits = list(collection_produits.find({"marchand_id": marchand["_id"]}))
                stock_total = sum(produit["quantite"] for produit in produits)

                # Déterminer la couleur en fonction du stock total
                if stock_total > 50:
                    couleurs.append("green")  # Stock élevé
                elif 20 <= stock_total <= 50:
                    couleurs.append("orange")  # Stock moyen
                else:
                    couleurs.append("red")  # Stock faible

            # Création de la carte interactive avec Plotly
            client_x = float(input("Entrez votre position X : "))
            client_y = float(input("Entrez votre position Y : "))

            noms_marchands.append("Vous")
            positions_x.append(client_x)
            positions_y.append(client_y)
            couleurs.append("blue")

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=positions_x,
                y=positions_y,
                mode="markers+text",
                text=noms_marchands,
                textposition="top center",
                marker=dict(
                    size=15,
                    color=couleurs,
                    line=dict(width=2, color="black")
                )
            ))

            fig.update_layout(
                title=f"Carte interactive des marchands du marché '{nom_marche}'",
                xaxis_title="Coordonnée X",
                yaxis_title="Coordonnée Y",
                showlegend=False
            )
            fig.write_image("marche_map.png")
            fig.show()


        elif choix == "7":
            print("\n=== Affichage des stocks ===")
            nom_marche = input("Nom du marché : ")
            # Connexion à la base MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["market_bd"]

            # Chargement des collections
            marchands = list(db.marchands.find())
            produits = list(db.produits.find())
            marches = list(db.marches.find())

            # Convertir en DataFrame
            df_marchands = pd.DataFrame(marchands)
            df_produits = pd.DataFrame(produits)
            df_marches = pd.DataFrame(marches)
            # Compter le nombre de marchands par marché
            marchands_par_marche = df_marchands.groupby("marchand_id").size().reset_index(name="Nombre de marchands")


            # Fusionner avec les marchés pour avoir les noms
            marchands_par_marche = marchands_par_marche.merge(df_marches, left_on="marchand_id", right_on="_id")
            print("marchands_par_marche",marchands_par_marche)

            fig = px.bar(marchands_par_marche, x="nom_marce", y="Nombre de marchands", title="Nombre de marchands par marché", 
                        labels={"nom_marce": "Marché", "Nombre de marchands": "Nombre de Marchands"}, color="Nombre de marchands")
            #image show 
            fig.write_image("marchands_par_marche.png")
            fig.show()
            # Fermer la connexion   
            df_marchands["position_x"] = df_marchands["position"].apply(lambda pos: pos[0] if isinstance(pos, list) else None)
            df_marchands["position_y"] = df_marchands["position"].apply(lambda pos: pos[1] if isinstance(pos, list) else None)

            print("Poition",df_marchands["position"].head())


            fig = px.scatter(df_marchands, x="position_x", y="position_y", color="nom", hover_data=["nom"],
                 title="Répartition géographique des marchands")

            #image show
            fig.write_image("marchands_geographie.png")
            fig.show()
            # Stock total par produit
            stock_produit = df_produits.groupby("nom")["quantite"].sum().reset_index()

            fig = px.bar(stock_produit, x="nom_marce", y="quantite", title="Stock total par produit", 
                        labels={"nom": "Produit", "quantite": "Stock"}, color="quantite")
            #image show
            fig.write_image("stock_produit.png")
            fig.show()



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

   
