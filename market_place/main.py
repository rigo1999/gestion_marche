from services.services import ajouter_marche
from services.services import ajouter_marchand
from services.services import ajouter_produit
from services.services import enregistrer_achat

def main():
    while True:
        print("\n1. Ajouter un marché")
        print("2. Ajouter un marchand")
        print("3. Quitter")
        choix = input("Choisissez une option : ")
        
        if choix == "1":
            nom = input("Nom du marché : ")
            localisation = input("Localisation : ")
            ajouter_marche(nom, localisation)
        elif choix == "2":
            nom_marche = input("Nom du marché : ")
            nom_marchand = input("Nom du marchand : ")
            produit = input("Produit vendu : ")
            prix = float(input("Prix du produit : "))
            ajouter_marchand(nom_marche, nom_marchand, produit, prix)
        elif choix == "3":
            print("Au revoir!")
            break
        else:
            print("Option invalide, essayez encore.")

if __name__ == "__main__":
    main()
