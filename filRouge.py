import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
from pyspark.sql.functions import col
from pyspark.sql.functions import year
from pyspark.sql.functions import month
from pyspark.sql.functions import countDistinct
from pyspark.sql.functions import count
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def create_spark_session():
    os.environ['PYSPARK_PYTHON'] = 'python'
    return SparkSession.builder \
        .appName("fil rouge") \
        .config("spark.master", "local") \
        .config("spark.driver.extraClassPath", "C:/Program Files/JDBC_PostgreSQL/postgresql-42.7.4.jar") \
        .config("spark.executor.extraClassPath", "C:/Program Files/JDBC_PostgreSQL/postgresql-42.7.4.jar") \
        .getOrCreate()

def main():
    # Créer une session Spark
    spark = create_spark_session()

    # URL JDBC et propriétés de connexion
    jdbcUrl = "jdbc:postgresql://localhost:5432/fil_rouge"
    connectionProperties = {
        "user": "postgres",
        "password": "root"
    }

    #1 Chargement des tables dans les DataFrames
    listingsDF = spark.read.jdbc(jdbcUrl, "public.listings", properties=connectionProperties)
    reviewsDF = spark.read.jdbc(jdbcUrl, "public.reviews", properties=connectionProperties)

    #2 Afficher le schéma des DataFrames

    listingsDF.printSchema()

    reviewsDF.printSchema()

    #3 listings avec une disponibilité> à 30 jours
    listings_dispo = listingsDF.filter(listingsDF['availability_365'] > 30)
    listings_dispo.show()

    #4 la moyenne des prix des listings pour chaque type de chambre

    avg_price_room = listingsDF.groupBy("room_type").agg(avg("price_clean").alias("average_price"))
    avg_price_room.show()

    #5 Extraire le mois à partir de la colonne date_review
    reviews_month = reviewsDF.withColumn("month", month(col("date_review")))
    reviews_month.show()

    #6 : Extraire l'année
    reviews_year = reviewsDF.withColumn("year", year(col("date_review")))
    reviews_year.show()

    #7 Filtrer les listings avec disponibilité > 30 jours et prix < 100 euros
    listings_filtered = listingsDF.filter((col("availability_365") > 30) & (col("price_clean") < 100))
    listings_filtered.show()

    #8 Ajout de colonne price_per_room
    listingsDF_clean = listingsDF.filter(col("price_clean").isNotNull() & col("bedrooms").isNotNull())

    price_per_room = listingsDF_clean.withColumn("price_per_room", col("price_clean") /col("bedrooms"))
    price_per_room.show()

    #9 Remplacer les valeurs nulles par 0
    listingsDF_fillna = listingsDF.fillna({"reviews_per_month": 0})
    listingsDF_fillna.select("reviews_per_month").show()


    #10 Calculer la moyenne de 'review_scores_rating'
    average_review_scores_rating = listingsDF.select(avg("review_scores_rating")).first()[0]

    # Remplacer les valeurs nulles par la moyenne
    listingsDF_repl = listingsDF.fillna({"review_scores_rating": average_review_scores_rating})

    listingsDF_repl.select("review_scores_rating").show()

    #11 Calcule de la moyenne de review_scores_rating

    average_review_scores_rating = listingsDF.select(avg("review_scores_rating"))
    average_review_scores_rating.show()

    #12 Calcule de la moyenne des prix pour chaque type de logement
    average_price_property_type = listingsDF.groupBy("property_type").agg(avg(col("price_clean")))
    average_price_property_type.show()

    #13 Calcule le nombre total de types de chambre dans chaque zone voisine
    room_neighborhood = listingsDF.groupBy("neighbourhood").agg(countDistinct("room_type"))
    room_neighborhood.show()

    #14 la corrélation entre le nombre de nuits disponibles et le prix des listings
    correlation = listingsDF.corr("availability_365", "price_clean")
    print({correlation})

    #15 5 meilleurs quartiers avec le plus grand nombre de logements
    top_neighborhoods = listingsDF.groupBy("neighbourhood").agg(count("id").alias("nombre_listing")) \
        .orderBy(col("nombre_listing").desc()) \
        .limit(5)
    top_neighborhoods.show()

    #16 sql
    listingsDF.createOrReplaceTempView("listings")
    reviewsDF.createOrReplaceTempView("reviews")
    total_listings = spark.sql("""
    SELECT neighbourhood_cleansed AS ville, COUNT(*) AS total_listings
    FROM listings
    GROUP BY neighbourhood_cleansed
    """)
    total_listings.show()

    #17 Les disponibilités et les prix moyens par quartier

    avg_availability_price = spark.sql("""
    SELECT neighbourhood_cleansed AS city, 
           AVG(availability_365) AS avg_availability, 
           AVG(price_clean) AS avg_price
    FROM listings
    GROUP BY neighbourhood_cleansed
    """)
    avg_availability_price.show()

    #18 Le nombre total d'avis
    total_reviews = spark.sql("SELECT COUNT(*) AS total_reviews FROM reviews")
    total_reviews.show()

    #19 Date de review le plus récent
    latest_review = spark.sql("SELECT MAX(date_review) AS latest_review_date FROM reviews")
    latest_review.show()

    #20 5 utilisateurs ayant le plus grand nombre d'avis
    top5_reviewers = spark.sql("""
    SELECT reviewer_name, COUNT(*) AS total_reviews
    FROM reviews
    GROUP BY reviewer_name
    ORDER BY total_reviews DESC
    LIMIT 5
    """)
    top5_reviewers.show()

    # 21 nombre d'hotes uniques
    unique_hosts = spark.sql("SELECT COUNT(DISTINCT host_id) AS unique_hosts FROM listings")
    unique_hosts.show()

    # 22 Ajouter une colonne "is_premium" et créer une nouvelle table
    premium_listings = spark.sql("""
    SELECT 
        *,
        CASE 
            WHEN price_clean >= 700 THEN 'Yes'
            ELSE 'No'
        END AS is_premium
    FROM listings
    """)

    premium_listings.show()

    premium_listings.write \
        .mode("overwrite") \
        .jdbc(jdbcUrl, "public.premium_listings", properties=connectionProperties)

    # 23 Calculer le nombre moyen de nuits disponibles pour chaque hôte et crée la table
    avg_nights_host = spark.sql("""
    SELECT 
        host_id,
        AVG(availability_365) AS avg_nights_available
    FROM listings
    GROUP BY host_id
    """)


    avg_nights_host.show()

    # Sauvegarder les résultats dans une nouvelle table PostgreSQL
    avg_nights_host.write \
        .mode("overwrite") \
        .jdbc(jdbcUrl, "public.avg_nights_host", properties=connectionProperties)



    # Bar Plot
    avg_price_roomtype = listingsDF.groupBy("room_type").agg(avg("price_clean").alias("average_price"))


    avg_price_roomtype_pandas = avg_price_roomtype.toPandas()

    # Créer un graphique en barres
    plt.figure(figsize=(10, 6))
    plt.bar(avg_price_roomtype_pandas["room_type"], avg_price_roomtype_pandas["average_price"], color='skyblue')

    # Ajouter les titres et les étiquettes
    plt.title("Prix moyen par type de chambre", fontsize=14)
    plt.xlabel("Type de chambre", fontsize=12)
    plt.ylabel("Prix moyen (en euros)", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    # Afficher le graphique
    plt.savefig("bar_plot.png")
    plt.close()

# Line Plot
    reviews_month = reviewsDF.withColumn("month", month(col("date_review")))
    comments_by_month = reviews_month.groupBy("month").count().orderBy("month")

    comments_by_month_pandas = comments_by_month.toPandas()

    plt.figure(figsize=(10, 6))
    plt.plot(comments_by_month_pandas["month"], comments_by_month_pandas["count"], marker='o', linestyle='-', color='skyblue')

    plt.title("Nombre de commentaires par mois", fontsize=14)
    plt.xlabel("Mois de l'année", fontsize=12)
    plt.ylabel("Nombre total de commentaires", fontsize=12)
    plt.xticks(range(1, 13), [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ], rotation=45, fontsize=10)
    plt.tight_layout()

    plt.savefig("line_plot.png")
    plt.close()

if __name__ == "__main__":
        main()
