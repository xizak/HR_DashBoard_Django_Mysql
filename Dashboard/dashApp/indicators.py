import datetime
import pymysql
from datetime import date


def calculer_effectif_total(departement=0):
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )

        cursor = db.cursor()
        if departement == 0:
            sql = "SELECT COUNT(*) FROM Employe"
            cursor.execute(sql)

            effectif_total = cursor.fetchone()[0]

            db.close()

            return effectif_total
        else:
            sql = "SELECT COUNT(*) FROM Employe WHERE employe.Departement = %s "
            cursor.execute(sql, (departement))

            effectif_total = cursor.fetchone()[0]

            db.close()

            return effectif_total
    except Exception as e:
        print(f"Erreur lors du calcul de l'effectif total : {str(e)}")
        return 0


def repartition_par_genre(departement=0):
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )
        cursor = db.cursor()
        if departement == 0:
            sql = "SELECT Genre, COUNT(*) as Nombre FROM Employe GROUP BY Genre"
            cursor.execute(sql)
        else:
            sql = """SELECT Genre, COUNT(*) as Nombre FROM Employe 
                     WHERE Employe.departement = %s 
                     GROUP BY Genre"""
            cursor.execute(sql, (departement))

        resultats = cursor.fetchall()
        db.close()
        return resultats

    except Exception as e:
        print(f"Erreur lors de la récupération de la répartition par genre : {str(e)}")
        return 0


def repartition_par_departement():
    try:
        # Créer une connexion à la base de données
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )

        # Créer un curseur
        cursor = db.cursor()

        # Exécuter la requête SQL pour obtenir la répartition par épartement
        sql = """SELECT Departement.NomDepartement, COUNT(*) as Nombre FROM 
                 Employe , departement WHERE employe.Departement = departement.ID_Departement
                 GROUP BY Departement;"""
        cursor.execute(sql)

        # Récupérer les résultats de la requête
        resultats = cursor.fetchall()

        # Fermer la connexion à la base de données
        db.close()

        return resultats

    except Exception as e:
        print(
            f"Erreur lors de la récupération de la répartition par département : {str(e)}"
        )
        return 0


def calculer_age(date_naissance):
    aujourdhui = date.today()
    annee_naissance = date_naissance.year
    annee_actuelle = aujourdhui.year
    age = annee_actuelle - annee_naissance
    return age


def repartition_par_age(departement=0):
    try:
        # Créer une connexion à la base de données
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )
        cursor = db.cursor()

        if departement == 0:
            sql = "SELECT DateNaissance FROM Employe"
            cursor.execute(sql)
        else:
            sql = "SELECT DateNaissance FROM Employe WHERE Employe.departement = %s"
            cursor.execute(sql, (departement))
        dates_naissance = cursor.fetchall()

        ages = [calculer_age(date_naissance[0]) for date_naissance in dates_naissance]

        db.close()

        tranches_age = [20, 30, 40, 50, 60]

        repartition_age = {f"{tranche}-{tranche+9} ans": 0 for tranche in tranches_age}

        for age in ages:
            for i, tranche in enumerate(tranches_age):
                if age >= tranche and age <= tranche + 9:
                    cle = f"{tranche}-{tranche+9} ans"
                    repartition_age[cle] += 1
                    break

        return repartition_age

    except Exception as e:
        print(f"Erreur lors de la récupération de la répartition par âge : {str(e)}")
        return 0


def calculer_rotation_personnel(annee, departement=0):
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )

        cursor = db.cursor()
        if departement == 0:
            # la liste des employés ayant quitté l'entreprise pendant l'année spécifiée
            sql = "SELECT COUNT(*) FROM HistoriqueEmployes WHERE YEAR(DateDepart) = %s"
            cursor.execute(sql, (annee,))

            # le nombre d'employés ayant quitté l'entreprise pendant l'année spécifiée
            nombre_depart = cursor.fetchone()[0]
            # l'effectif total de l'entreprise pendant l'année spécifiée
            sql = """SELECT COUNT(*) FROM Employe
                     WHERE YEAR(DateEmbauche) <= %s"""
            cursor.execute(sql, (annee,))
            # l'effectif total de l'entreprise pendant l'année spécifiée
            effectif_total = cursor.fetchone()[0]
        else:
            # la liste des employés ayant quitté l'entreprise pendant l'année spécifiée
            sql = """SELECT COUNT(*) FROM HistoriqueEmployes
                     WHERE YEAR(DateDepart) = %s AND 
                     HistoriqueEmployes.departement = %s"""
            cursor.execute(sql, (annee, departement))

            # le nombre d'employés ayant quitté l'entreprise pendant l'année spécifiée
            nombre_depart = cursor.fetchone()[0]
            # l'effectif total de l'entreprise pendant l'année spécifiée
            sql = """SELECT COUNT(*) FROM Employe
                     WHERE YEAR(DateEmbauche) <= %s AND 
                     Employe.departement = %s"""

            cursor.execute(sql, (annee, departement))
            # l'effectif total de l'entreprise pendant l'année spécifiée
            effectif_total = cursor.fetchone()[0]

        # le taux de rotation du personnel
        taux_rotation = (nombre_depart / effectif_total) * 100

        db.close()

        return taux_rotation

    except Exception as e:
        print(f"Erreur lors du calcul du taux de rotation du personnel : {str(e)}")
        return 0


"""for annee_calcul in range(2019, 2024):
    taux_rotation = calculer_rotation_personnel(annee_calcul, departement=3)

    if taux_rotation is not 0:
        print(f"Taux de rotation du personnel en {annee_calcul} : {taux_rotation}%")
    else:
        print("Impossible de calculer le taux de rotation du personnel.")
"""


# TODO: regler le probmlem de taux fix des departement
def calculer_taux_absenteisme(debut_periode, fin_periode, departement=0):
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )

        cursor = db.cursor()

        # Define a base SQL query
        base_sql = """SELECT SUM(DATEDIFF(DateFinConge, DateDebutConge) + 1) 
                      FROM Conges , Employe
                      WHERE DateDebutConge BETWEEN %s AND %s
                      AND conges.StatutConge = 'Approuvé'"""

        if departement is not 0:
            base_sql += " AND Employe.departement = %s"

        # Calculate total days of absence
        cursor.execute(base_sql, (debut_periode, fin_periode, departement))
        jours_absence = cursor.fetchone()[0]

        # Calculate total workforce
        if departement is not 0:
            sql_total_employees = (
                "SELECT COUNT(*) FROM Employe WHERE Employe.departement = %s"
            )
            cursor.execute(sql_total_employees, (departement,))
        else:
            sql_total_employees = "SELECT COUNT(*) FROM Employe"
            cursor.execute(sql_total_employees)

        effectif_total = cursor.fetchone()[0]

        # Calculate total workdays in the period
        jours_travail_prevus = (fin_periode - debut_periode).days + 1

        # Calculate absenteeism rate in percentage
        taux_absenteisme = (
            jours_absence / (effectif_total * jours_travail_prevus)
        ) * 100

        # Close the database connection
        db.close()

        return taux_absenteisme

    except Exception as e:
        print(f"Erreur lors du calcul du taux d'absentéisme : {str(e)}")
        return 0


"""debut_periode = date(2023, 1, 1)  # Date de début de la période
fin_periode = date(2023, 12, 31)  # Date de fin de la période
taux = calculer_taux_absenteisme(debut_periode, fin_periode,departement=7)

if taux is not 0:
    print(f"Taux d'absentéisme pour la période {debut_periode} à {fin_periode}: {taux:.2f}%")
else:
    print("Impossible de calculer le taux d'absentéisme.")"""


def calculer_duree_moyenne_recrutement(debut_periode, fin_periode, departement=0):
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )

        cursor = db.cursor()

        if departement == 0:
            sql = (
                "SELECT DateEmbauche FROM Employe WHERE DateEmbauche BETWEEN %s AND %s"
            )
            cursor.execute(sql, (debut_periode, fin_periode))
        else:
            sql = "SELECT DateEmbauche FROM Employe WHERE DateEmbauche BETWEEN %s AND %s AND Employe.departement = %s"
            cursor.execute(sql, (debut_periode, fin_periode, departement))

        resultats = cursor.fetchall()

        durees_recrutement = []

        # Calculer la durée de recrutement pour chaque nouvel employé
        for row in resultats:
            date_embauche = row[0]
            duree_recrutement = (date_embauche - debut_periode).days
            durees_recrutement.append(duree_recrutement)

        # Calculer la durée moyenne de recrutement
        if len(durees_recrutement) > 0:
            duree_moyenne = sum(durees_recrutement) / len(durees_recrutement)
        else:
            duree_moyenne = 0

        # Fermer la connexion à la base de données
        db.close()

        return duree_moyenne

    except Exception as e:
        print(f"Erreur lors du calcul de la durée moyenne de recrutement : {str(e)}")
        return 0


"""
debut_periode = date(2022, 1, 1)
fin_periode = date(2022, 12, 31)
duree_moyenne_recrutement = calculer_duree_moyenne_recrutement(debut_periode, fin_periode, departement=2)

if duree_moyenne_recrutement is not 0:
    print(f"Durée moyenne de recrutement pour la période spécifiée : {duree_moyenne_recrutement} jours")
else:
    print("Impossible de calculer la durée moyenne de recrutement.")
"""

import json
import pymysql


def distribution_par_genre_par_departement():
    try:
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )
        cursor = db.cursor()

        sql = """
            SELECT
                d.NomDepartement AS Departement,
                CAST(SUM(CASE WHEN e.Genre = 'Male' THEN 1 ELSE 0 END) AS UNSIGNED) AS Male,
                CAST(SUM(CASE WHEN e.Genre = 'Female' THEN 1 ELSE 0 END) AS UNSIGNED) AS Female
            FROM
                Employe e
            JOIN
                departement d ON e.Departement = d.ID_Departement
            GROUP BY
                d.NomDepartement;
        """

        cursor.execute(sql)
        resultats = cursor.fetchall()
        db.close()

        resultats_groupe = {}
        for departement, male, female in resultats:
            resultats_groupe[departement] = {"Male": male, "Female": female}

        return resultats_groupe

    except Exception as e:
        print(
            f"Erreur lors du calcul de la répartition par genre dans chaque département : {str(e)}"
        )
        return {}


def repartition_par_age_departement():
    try:
        # Créer une connexion à la base de données
        db = pymysql.connect(
            host="localhost", user="root", password="", db="entreprise"
        )
        cursor = db.cursor()

        sql = """
              SELECT employe.DateNaissance , departement.NomDepartement
              FROM employe , departement 
              WHERE employe.Departement = departement.ID_Departement;"""
        cursor.execute(sql)
        data = cursor.fetchall()

        db.close()

        tranches_age = [20, 30, 40, 50, 60]

        repartition_age_departement = {}

        for date_naissance, nom_departement in data:
            age = calculer_age(date_naissance)

            if nom_departement not in repartition_age_departement:
                repartition_age_departement[nom_departement] = {f"{tranche}-{tranche+9} ans": 0 for tranche in tranches_age}

            for tranche in tranches_age:
                if age >= tranche and age <= tranche + 9:
                    cle = f"{tranche}-{tranche+9} ans"
                    repartition_age_departement[nom_departement][cle] += 1
                    break

        return repartition_age_departement

    except Exception as e:
        print(f"Erreur lors de la récupération de la répartition par âge : {str(e)}")
        return 0


