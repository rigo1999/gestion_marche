import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient


# Toutes les classes et méthodes ensuite

# Classe Produit
class Produit:
    """
    Classe pour représenter un produit dans le marché.
    """
    def __init__(self, nom, prix, quantite,marchand_id: ObjectId):
        self.nom = nom  # Nom du produit
        self.prix = prix  # Prix unitaire du produit
        self.quantite = quantite  
        self.marchand_id = marchand_id 

    def afficher_details(self):
        """
        Retourne les détails du produit sous forme de texte.
        """
        return f"Produit: {self.nom}, Prix: {self.prix:.2f}, Quantité: {self.quantite}"

    def ajouter_quantite(self, quantite):
        """
        Ajoute une quantité au stock.
        """
        self.quantite += quantite

    def retirer_quantite(self, quantite):
        """
        Retire une quantité du stock si disponible.
        """
        if quantite > self.quantite:
            raise ValueError("Quantité demandée supérieure au stock disponible.")
        self.quantite -= quantite

# Classe Marchand
class Marchand:
    """
    Classe pour représenter un marchand dans le marché.
    """
    def __init__(self, nom, position,marchand_id: ObjectId):
        self.nom = nom  # Nom du marchand
        self.position = position  # Position du marchand dans la grille (x, y)
        self.stock = []  # Liste des produits du marchand
        self.historique_ventes = [] 
        self.marchand_id =marchand_id
        # Historique des transactions

    def ajouter_produit(self, produit):
        """
        Ajoute un produit au stock du marchand.
        """
        self.stock.append(produit)
    #enregistrer les transaction
    def enregistrer_transaction(self, transaction):
        """
        Enregistre une transaction dans l'historique des ventes.
        """
        self.historique_ventes.append(transaction)

    def afficher_historique_ventes(self):
        """
        Affiche l'historique des ventes du marchand.
        """
        if not self.historique_ventes:
            print(f"Historique des ventes pour le marchand {self.nom} : Aucun produit vendu.")
            return

        print(f"Historique des ventes pour le marchand {self.nom} :")
        for vente in self.historique_ventes:
            produit = vente["produit"]
            quantite = vente["quantite"]
            montant_total = vente["montant_total"]
            print(f"- Produit : {produit}, Quantité : {quantite}, Montant total : {montant_total:.2f} €")


    def statistiques(self):
        """
        Affiche les statistiques du marchand, y compris le total des ventes et les produits les plus vendus.
        """
        total_ventes = sum(vente["montant_total"] for vente in self.historique_ventes)
        produits_vendus = {}

        # Calcul des quantités vendues par produit
        for vente in self.historique_ventes:
            produit = vente["produit"]
            quantite = vente["quantite"]
            if produit in produits_vendus:
                produits_vendus[produit] += quantite
            else:
                produits_vendus[produit] = quantite

        # Trier les produits par quantités vendues (descendant)
        produits_tries = sorted(produits_vendus.items(), key=lambda x: x[1], reverse=True)

        print(f"Statistiques pour le marchand {self.nom} :")
        print(f"- Total des ventes : {total_ventes:.2f} €")
        print("- Produits les plus vendus :")
        for produit, quantite in produits_tries:
            print(f"  * {produit} : {quantite} unités")

    def afficher_informations(self):
        """
        Affiche les informations du marchand et son stock.
        """
        print(f"Marchand: {self.nom}, Position: {self.position}")
        print("Stock:")
        for produit in self.stock:
            print(f"  - {produit.afficher_details()}")

# Classe Marché
class Marche:
    """
    Classe pour représenter un marché 2D avec des marchands.
    """
    def __init__(self, nom_marche,taille_x, taille_y,marchand_id: ObjectId):
        self.nom_marce = nom_marche 
        self.taille_x = taille_x  # Largeur du marché
        self.taille_y = taille_y 
        # Longueur du marché
        self.marchand_id = marchand_id

        
        
          # Dictionnaire des positions des marchands
        #recuperer les postions des marchands dans le marche

    def recuperer_positions_marchands(db):
        # recuperer les postions des marchands dans le marche
        # recuperer les postions des marchands dans le marche
        return list(db["Marche"].find())
    
    def recuperer_tous_marchands(db):
        return list(db["marchands"].find())
    def ajouter_marchand(self, marchand,db):
        """
        Ajoute un marchand à une position unique dans le marché.
        """
        # Vérifie si l'objet est bien un marchand
        if not isinstance(marchand, Marchand):
            raise ValueError("L'objet ajouté doit être une instance de la classe 'Marchand'.")
        
        # Vérifie si la position est déjà occupée
        if marchand.position in self.positions:
            raise ValueError(f"Position {marchand.position} déjà occupée.")
        
        # Ajoute le marchand à la position
        self.positions[marchand.position] = marchand


    def afficher_marchands(self):
        """
        Affiche tous les marchands dans le marché.
        """
        if not self.positions:
            print("Aucun marchand dans le marché.")
        for position, marchand in self.positions.items():
            print(f"Position: {position}, Marchand: {marchand.nom}")
            detail_marchand.afficher_informations()
    import matplotlib.pyplot as plt
# Autres méthodes de la classe ici...

    def generer_carte_interactive(nom_marche):
        # Connexion à MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["market_bd"]
        collection = db["marches"]

        # Recherche du marché dans la base de données
        marche = collection.find_one({"nom_marce": nom_marche})

        if not marche:
            print(f"Le marché '{nom_marche}' n'existe pas.")
            return

        # Initialisation des listes pour les données
        noms_marchands = []
        positions_x = []
        positions_y = []
        couleurs = []

        # Vérifier si la clé 'marchands' existe dans le document    
        #get the marchands with the same marche id 
        marchands = collection.find({"marchand_id": marche["_id"]})

        if marchands:
            for marchand in marchands:
                noms_marchands.append(marchand["nom"])
                positions_x.append(marchand["position"][0])
                positions_y.append(marchand["position"][1])
                #get products with same marchand id
                produits = collection.find({"marchand_id": marchand["_id"]})

                # Déterminer la couleur en fonction du stock total
                stock_total = sum(produit["quantite"] for produit in produits)
                if stock_total > 50:
                    couleurs.append("green")  # Stock élevé
                elif 20 <= stock_total <= 50:
                    couleurs.append("orange")  # Stock moyen
                else:
                    couleurs.append("red")  # Stock faible
        else:
            print(f"Aucun marchand trouvé pour le marché '{nom_marche}'.")
            return

        # Création de la carte interactive avec Plotly
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
                line=dict(width=1, color="black")
            )
        ))

        fig.update_layout(
            title=f"Carte interactive des marchands du marché '{nom_marche}'",
            xaxis_title="Coordonnée X",
            yaxis_title="Coordonnée Y",
            showlegend=False
        )

        # Afficher la carte dans le navigateur
        fig.show(renderer="browser")

    # Exemple d'utilisation
    nom_marche = input("Nom du marché : ")
    generer_carte_interactive(nom_marche)
        
    def afficher_stock_graphique(self):
        """
        Affiche un graphique en barres montrant le stock total de chaque produit
        pour tous les marchands.
    """
    # Stock agrégé par produit
        stock_total = {}
        for marchand in self.positions.values():  # On récupère les marchands du dictionnaire des positions
            for produit in marchand.stock:
                if produit.nom in stock_total:
                    stock_total[produit.nom] += produit.quantite
                else:
                    stock_total[produit.nom] = produit.quantite

        # Préparation des données pour le graphique
        produits = list(stock_total.keys())
        quantites = list(stock_total.values())

        # Création du graphique avec Matplotlib
        plt.bar(produits, quantites, color='skyblue')
        plt.title("Stock total des produits")
        plt.xlabel("Produits")
        plt.ylabel("Quantité")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    def afficher_positions_marchands(self):
        """
        Affiche une carte interactive des positions des marchands.
        """
        print("Affichage des positions des marchands avec coloration...")

        # Préparer les données pour Plotly
        noms = [marchand.nom for marchand in self.positions.values()]
        positions_x = [marchand.position[0] for marchand in self.positions.values()]
        positions_y = [marchand.position[1] for marchand in self.positions.values()]
        couleurs = []  # Couleurs des points selon le stock

        # Déterminer la couleur des points en fonction de l'état du stock
        for marchand in self.positions.values():
            # Calcul du stock total en parcourant la liste des produits
            stock_total = sum(produit.quantite for produit in marchand.stock)
            if stock_total > 50:
                couleurs.append("green")  # Stock élevé
            elif 20 <= stock_total <= 50:
                couleurs.append("orange")  # Stock moyen
            else:
                couleurs.append("red")  # Stock faible

        # Création de la carte interactive avec Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=positions_x,
            y=positions_y,
            mode='markers+text',
            text=noms,
            textposition='top center',
            marker=dict(
                size=15,
                color=couleurs,  # Appliquer les couleurs dynamiques
                line=dict(width=1, color='black')  # Bordure noire pour les points
            )
        ))

        # Mise à jour de la mise en page
        fig.update_layout(
            title="Carte des positions des marchands",
            xaxis_title="Coordonnée X",
            yaxis_title="Coordonnée Y",
            showlegend=False
        )

        # Afficher la carte dans le navigateur
        fig.show(renderer="browser")
    # Autres méthodes...
    
    #affichage marchand recommandé sur carte
    def afficher_marchands_recommandes(self, recommendations):
        """
        Met à jour la carte pour afficher les marchands recommandés.
        """
        noms = [rec["marchand"] for rec in recommendations]
        positions_x = [rec["position"][0] for rec in recommendations]
        positions_y = [rec["position"][1] for rec in recommendations]
        couleurs = ["green"] * len(recommendations)  # Points verts pour les marchands recommandés

    # Création de la carte interactive
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=positions_x,
            y=positions_y,
            mode='markers+text',
            text=noms,
            textposition='top center',
            marker=dict(
                size=15,
                color=couleurs,
                line=dict(width=1, color='black')
            )
        ))

        fig.update_layout(
            title="Marchands recommandés pour vos achats",
            xaxis_title="Coordonnée X",
            yaxis_title="Coordonnée Y",
            showlegend=False
        )

        fig.show(renderer="browser")

        


# Classe Utilisateur
class Utilisateur:
    """
    Classe pour représenter un utilisateur du système.
    """
    def __init__(self, identifiant, role):
        self.identifiant = identifiant  # Identifiant unique de l'utilisateur
        self.role = role  # Rôle de l'utilisateur (Admin, Marchand, Client)

    def afficher_info(self):
        """
        Affiche les informations de l'utilisateur.
        """
        print(f"Utilisateur: {self.identifiant}, Rôle: {self.role}")


class Vente:
    def __init__(self, produit, montant, quantite, client="Inconnu"):
        self.produit = produit
        self.montant = montant
        self.quantite = quantite
        self.client = client
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "produit": self.produit,
            "montant": self.montant,
            "quantite": self.quantite,
            "client": self.client,
            "date": self.date
        }

    def __repr__(self):
        return f"Vente(produit={self.produit}, montant={self.montant}, quantite={self.quantite}, client={self.client}, date={self.date})"

class HistoriqueVentes:
    def __init__(self, produit, montant, quantite, date, client="Inconnu"):
          # Montant total de la transaction
        self.client = client  # Client ayant effectué la transaction
        self.date = date  # Date et heure de la transaction
        self.produit = produit  # Produit acheté
        self.prix = montant
        self.quantite = quantite
    
    
    def ajouter_vente(self, produit, montant, quantite, client="Inconnu"):
        vente = Vente(produit, montant, quantite, client)
        #Vente.insert_one(vente.to_dict())
        self.db["ventes"].insert_one(vente.to_dict())
        #add it to ventes

        
        #self.Ventes.insert_one(vente.to_dict())
        print(f"Vente ajoutée: {vente}")
    
    def afficher_historique(self):
        ventes = self.collection.find()
        if ventes.count() == 0:
            print("Aucune vente enregistrée.")
        else:
            for vente in ventes:
                print(vente)
    
    def total_ventes(self):
        return sum(vente["montant"] * vente["quantite"] for vente in self.collection.find())

# Classe Transaction
def notifier(message):
        """
        Système d'alerte simple pour afficher des notifications en temps réel.
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Notification : {message}")

def afficher_menu():
    """
    Affiche le menu principal pour l'utilisateur.
    """
    print("\n=== MENU PRINCIPAL ===")
    print("1. Créer un marché")
    print("2. Ajouter un marchand à un marché")
    print("3. Ajouter des produits à un marchand")
    print("4. Simuler un achat et optimiser le panier")
    print("5. Afficher les statistiques d'un marchand")
    print("6. Visualiser la carte des marchands d'un marché")
    print("7. Afficher le graphique des stocks d'un marché")
    print("8. Quitter")

