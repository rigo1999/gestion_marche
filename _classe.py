import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math
from datetime import datetime
from bson import ObjectId


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
            mdetail_marchandarchand.afficher_informations()
    import matplotlib.pyplot as plt
# Autres méthodes de la classe ici...

    def generer_carte_interactive(self):
        """
        Génère une carte interactive des emplacements des marchands.
        """
        noms_marchands = []
        positions_x = []
        positions_y = []
        couleurs = []

        # Parcourir les positions des marchands
        for position, marchand in self.positions.items():
            if isinstance(marchand, Marchand):
                noms_marchands.append(marchand.nom)  # Ajouter le nom du marchand
                positions_x.append(position[0])  # Ajouter la coordonnée X
                positions_y.append(position[1])  # Ajouter la coordonnée Y

                # Calcul du stock total pour déterminer la couleur
                stock_total = sum(produit.quantite for produit in marchand.stock)
                if stock_total > 50:
                    couleurs.append("green")  # Stock élevé
                elif 20 <= stock_total <= 50:
                    couleurs.append("orange")  # Stock moyen
                else:
                    couleurs.append("red")  # Stock faible
            else:
                print(f"Erreur : La position {position} ne contient pas un objet 'Marchand'.")

        # Création du graphique Plotly
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
            title="Carte interactive des marchands",
            xaxis_title="Coordonnée X",
            yaxis_title="Coordonnée Y",
            showlegend=False
        )

        # Afficher la carte
        fig.show(renderer="browser")

        
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

    def optimiser_achats(self, position_client, liste_produits):
        """
        Optimise les achats d'un client en trouvant les marchands les plus adaptés.
        
        Args:
            position_client (tuple): Coordonnées (x, y) du client.
            liste_produits (list of dict): Liste des produits souhaités avec leur quantité.
                Exemple : [{"nom": "Pommes", "quantite": 10}, {"nom": "Bananes", "quantite": 5}]

        Returns:
            dict: Détails des marchands recommandés, coût total, et leurs coordonnées.
        """
        recommendations = []
        
        # Parcourir les marchands pour vérifier leur stock et calculer les distances
        
        for position, marchand in self.positions.items():
            total_cout = 0
            produits_disponibles = True

            for demande in liste_produits:
                produit_nom = demande["nom"]
                produit_quantite = demande["quantite"]

                # Vérifier si le marchand a le produit en stock
                produit = next((p for p in marchand.stock if p.nom == produit_nom), None)
                if produit and produit.quantite >= produit_quantite:
                    total_cout += produit.prix * produit_quantite
                else:
                    produits_disponibles = False
                    break

            if produits_disponibles:
                # Calculer la distance euclidienne entre le client et le marchand
                distance = math.sqrt((position[0] - position_client[0])**2 + (position[1] - position_client[1])**2)
                recommendations.append({
                    "marchand": marchand.nom,
                    "position": position,
                    "distance": distance,
                    "cout_total": total_cout
                })

        # Trier les marchands par coût total puis par distance
        recommendations.sort(key=lambda x: (x["cout_total"], x["distance"]))

        return recommendations
    
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

# Classe Transaction
class Transaction:
    """
    Classe pour représenter une transaction (vente).
    """
    def __init__(self, id_transaction, marchand, client, produits, total):
        self.id_transaction = id_transaction  # ID unique de la transaction
        self.marchand = marchand  # Marchand impliqué
        self.client = client  # Client impliqué
        self.produits = produits  # Liste des produits achetés
        self.total = total  # Montant total de la transaction

# Enregistrer cette transaction dans l'historique du marchand
        self.marchand.enregistrer_transaction(self)

    def afficher_details(self):
        """
        Affiche les détails de la transaction.
        """
        produits_details = ", ".join([produit.nom for produit in self.produits])
        return f"Transaction ID: {self.id_transaction}, Client: {self.client.identifiant}, Produits: {produits_details}, Total: {self.total:.2f}"

    def mettre_a_jour_stock(self):
        """
        Met à jour le stock du marchand après une transaction.
        """
        for produit in self.produits:
            # On vérifie si le produit existe dans le stock du marchand
            if produit.nom in self.marchand.stock:
                # Récupération des informations actuelles du stock
                stock_produit = self.marchand.stock[produit.nom]

                # Vérification de la quantité demandée
                if stock_produit["quantite"] >= produit.quantite:
                    # Réduction de la quantité en stock
                    self.marchand.stock[produit.nom]["quantite"] -= produit.quantite
                else:
                    print(f"Erreur : Stock insuffisant pour {produit.nom}.")
            else:
                print(f"Erreur : Le produit {produit.nom} n'est pas dans le stock du marchand.")


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

