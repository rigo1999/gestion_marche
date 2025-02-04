class Marche:
    def __init__(self, nom, emplacement):
        self.nom = nom
        self.emplacement = emplacement

# models/marchand.py
class Marchand:
    def __init__(self, nom, produit, prix, marche):
        self.nom = nom
        self.produit = produit
        self.prix = prix
        self.marche = marche

# models/produit.py
class Produit:
    def __init__(self, nom, categorie):
        self.nom = nom
        self.categorie = categorie

# models/historique.py
class HistoriqueVentes:
    def __init__(self, marchand, produit, quantite, date):
        self.marchand = marchand
        self.produit = produit
        self.quantite = quantite
        self.date = date
#vente
class Vente:
    def __init__(self, marchand, produit, quantite, date):
        self.marchand = marchand
        self.produit = produit
        self.quantite = quantite
        self.date = date