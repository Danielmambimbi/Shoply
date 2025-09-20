import mysql.connector
import mysql.connector
from flask import Flask, request,render_template,jsonify,send_file,send_from_directory
from PIL import Image, ImageOps
from flask_cors import CORS
from io import BytesIO
import os
import uuid
import mimetypes
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import random
from email.header import Header
import cloudinary
import cloudinary.uploader
import io
from flask import request

cloudinary.config(
  cloud_name="djujkd5k4",
  api_key="626697798174445",
  api_secret="JUXSx0YqNWUrZIT_4e3cOfnDOYU",
  secure=True
)


UPLOAD_FOLDER=""
unique_filename=""
# role 426800
def con_BDD():
    # Connexion à la base de données MySQL
    conn = mysql.connector.connect(
        host="mysql-danielmambimbi.alwaysdata.net",
        user="417759_ecom1",  # Remplace par ton utilisateur MySQL
        password="0896966760",  # Mets ton mot de passe MySQL
        database="danielmambimbi_ecommerce1",
        port=3306
    )
    return conn

# Mail lorsque un client crée un compte 

def mail_to_new_user(username,email):
    heure_actuelle = datetime.now().hour

    # Déterminer la salutation
    if 5 <= heure_actuelle < 12:
        salutation = "Bonjour"
    elif 12 <= heure_actuelle < 18:
        salutation = "Bon après-midi"
    elif 18 <= heure_actuelle < 22:
        salutation = "Bonsoir"
    else:
        salutation = "Salut"
    corps_message=[
        f"""{salutation} {username},
        
Bienvenue chez Shoply 🎉
Votre compte a été créé avec succès.
Vous pouvez dès maintenant vous connecter et profiter de nos services.

Merci pour votre confiance,  
L’équipe Shoply 🛒
""",
        f"""{salutation} {username} 👋
Bienvenue dans l’aventure Shoply 🛒
Ton compte est prêt, tu peux maintenant commander facilement et profiter d’avantages réservés à nos membres.

Merci pour votre confiance,  
L’équipe Shoply 🛒
"""
    ]
    objet_message=[
        f"""Bienvenue chez Shoply 🎉""",
        f"""Votre compte chez Shoply est prêt ✅""",
        f"""Merci {username}, votre inscription est confirmée !""",
        f"""Bienvenue dans la famille Shoply 🛒""",
        f"""Votre espace client Shoply 🛒 est activé"""
    ]

    corps_message=random.choice(corps_message)
    objet_message=random.choice(objet_message)

    # Infos d'expéditeur et destinataire
    expediteur = "shoply862@gmail.com"
    mot_de_passe = "flwm ecmw rvsy dkrs"  # ⚠️ Évite de le mettre en clair dans le code
    # destinataire = "danielmambimbi@gmail.com"

    # Création du message
    message = MIMEMultipart()
    message["From"] = str(Header("Shoply 🛒 <{}>".format(expediteur), "utf-8"))
    message["To"] = email
    message["Subject"] = Header(objet_message)
    
    # Corps du mail
    corps = corps_message
    message.attach(MIMEText(corps, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(expediteur, mot_de_passe)
            serveur.sendmail(expediteur, email, message.as_string())
        print(f"✅ Email de bienvenue envoyé à {email}")
    except Exception as e:
        print(f"❌ Erreur envoi email: {e}")
        # Connexion au serveur SMTP (ici Gmail)
        serveur = smtplib.SMTP("smtp.gmail.com", 587)
        serveur.starttls()  # Sécurise la connexion
        serveur.login(expediteur, mot_de_passe)  # Authentification
        serveur.sendmail(expediteur, email, message.as_string())
        serveur.quit()
        print("✅ Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur : {e}")

# Mail lorsque un client crée un compte 

# Mail lorsque le client passe une commande 

def mail_client_com(destinataire=False,id_commande="",username="",info_com=False,produits=False):
    # Récupérer l'heure actuelle
    heure_actuelle = datetime.now().hour

    # Déterminer la salutation
    if 5 <= heure_actuelle < 12:
        salutation = "Bonjour"
    elif 12 <= heure_actuelle < 18:
        salutation = "Bon après-midi"
    elif 18 <= heure_actuelle < 22:
        salutation = "Bonsoir"
    else:
        salutation = "Salut"
    id_commande=f"""n°{id_commande}"""
    
    corps_message=[
        f"""
{salutation} {username},

Merci pour votre commande chez Shoply 🎉  
Votre commande {id_commande} a bien été enregistrée et sera bientôt préparée.  
Nous vous informerons dès son expédition. 

Merci pour votre confiance,  
L’équipe Shoply 🛒
        """,
        

        
        f"""
Bonjour {username},

Bonne nouvelle ! Nous avons bien reçu votre commande {id_commande}.  
Notre équipe la prépare avec soin et vous tiendra informé(e) de son expédition 🚚  

Merci pour votre confiance,  
L’équipe Shoply 🛒 

        """,
        f"""
Cher(e) {username},

Votre commande {id_commande} est confirmée ✅  
Nous mettons tout en œuvre pour qu’elle vous parvienne dans les meilleurs délais.  

Merci pour votre confiance,  
L’équipe Shoply 🛒

        """,
        f"""
Bonjour {username},

Votre commande {id_commande} a été validée avec succès ! 🎊  
Vous recevrez bientôt un mail de suivi dès qu’elle sera expédiée.  
Merci pour votre achat chez Shoply 🛒.  

Merci pour votre confiance,  
L’équipe Shoply 🛒

        """,
        f"""
Salut {username},

Nous avons bien reçu ta commande {id_commande} 🙌  
Elle est maintenant en attente de préparation.  
Nous t’enverrons un message dès qu’elle partira en livraison. 

Merci pour votre confiance,  
L’équipe Shoply 🛒 

        """,
        f"""
Bonjour {username},

Merci pour votre commande chez Shoply 🎉
Votre commande {id_commande} a été confirmée et est en cours de préparation.
Nous vous tiendrons informé dès son expédition.

Merci de votre confiance,
L’équipe Shoply 🛒
        """
    ]
    
    objet_message=[
        f"""Votre commande {id_commande} a été confirmée ✅""",
        f"""Merci pour votre commande chez Shoply !""",
        f"""Commande {id_commande} enregistrée avec succès 🎉""",
        f"""Confirmation de votre achat chez Shoply""",
        f"""On s’occupe de votre commande {id_commande}""",
        f"""Votre commande est en cours de traitement"""
    ]
    
    corps_message=random.choice(corps_message)
    objet_message=random.choice(objet_message)
    
    # Infos d'expéditeur et destinataire
    expediteur = "shoply862@gmail.com"
    mot_de_passe = "flwm ecmw rvsy dkrs"  # ⚠️ Évite de le mettre en clair dans le code
    # destinataire = "danielmambimbi@gmail.com"

    # Création du message
    message = MIMEMultipart()
    message["From"] = str(Header("Shoply 🛒 <{}>".format(expediteur), "utf-8"))
    message["To"] = destinataire
    message["Subject"] = Header(objet_message)

    # Corps du mail
    corps = corps_message
    message.attach(MIMEText(corps, "plain"))

    try:
        # Connexion au serveur SMTP (ici Gmail)
        serveur = smtplib.SMTP("smtp.gmail.com", 587)
        serveur.starttls()  # Sécurise la connexion
        serveur.login(expediteur, mot_de_passe)  # Authentification
        serveur.sendmail(expediteur, destinataire, message.as_string())
        serveur.quit()
        print("✅ Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        
        
    # Alert chez Shoply
    destinataires=["danielmambimbi@gmail.com","shoply862@gamil.com"]
    detail_produit=""
    for produit in produits:
        detail_produit+=produit["nom_produit"]+"  Q: "+produit["quantite_produit"]+"  P.U :"+produit["prix_produit"]+"\n\t"
    
    corps_message=[
            f"""Nouvelle commande : le client {username} ({destinataire}) a passé la commande {id_commande}
            
- - - - - Détail de la commande - - - - -
    Nombre de produits : {info_com["nombre_produits"]}
    Sous_total : {info_com["sous_total"]}
    Prix_reduction : {info_com["prix_reduction"]}
    Prix de la livraison : {info_com["prix_livraison"]}
    Prix total de la commande : {info_com["prix_total"]}
    Username : {info_com["username"]}
    Prenom : {info_com["prenom"]}
    Nom : {info_com["nom"]}
    Adresse : {info_com["adresse"]}
    Référence : {info_com["reference"]}
    Ville : {info_com["ville"]}
    Postalcode : {info_com["postalcode"]}
    Pays : {info_com["pays"]}
    Tel : {info_com["tel"]}
    Tel whatsapp : {info_com["tel_what"]}
    Email : {info_com["email"]}

- - - - - Détail de(s) produit(s) commandés - - - - -
    {detail_produit}
            """,
            f"""Attention équipe : commande {id_commande} reçue de {username}

- - - - - Détail de la commande - - - - -
    Nombre de produits : {info_com["nombre_produits"]}
    Sous_total : {info_com["sous_total"]}
    Prix_reduction : {info_com["prix_reduction"]}
    Prix de la livraison : {info_com["prix_livraison"]}
    Prix total de la commande : {info_com["prix_total"]}
    Username : {info_com["username"]}
    Prenom : {info_com["prenom"]}
    Nom : {info_com["nom"]}
    Adresse : {info_com["adresse"]}
    Référence : {info_com["reference"]}
    Ville : {info_com["ville"]}
    Postalcode : {info_com["postalcode"]}
    Pays : {info_com["pays"]}
    Tel : {info_com["tel"]}
    Tel whatsapp : {info_com["tel_what"]}
    Email : {info_com["email"]}

- - - - - Détail de(s) produit(s) commandés - - - - -
    {detail_produit}
            """,
            f"""Alerte vente : {username} a passé une commande
            
- - - - - Détail de la commande - - - - -
    Nombre de produits : {info_com["nombre_produits"]}
    Sous_total : {info_com["sous_total"]}
    Prix_reduction : {info_com["prix_reduction"]}
    Prix de la livraison : {info_com["prix_livraison"]}
    Prix total de la commande : {info_com["prix_total"]}
    Username : {info_com["username"]}
    Prenom : {info_com["prenom"]}
    Nom : {info_com["nom"]}
    Adresse : {info_com["adresse"]}
    Référence : {info_com["reference"]}
    Ville : {info_com["ville"]}
    Postalcode : {info_com["postalcode"]}
    Pays : {info_com["pays"]}
    Tel : {info_com["tel"]}
    Tel whatsapp : {info_com["tel_what"]}
    Email : {info_com["email"]}

- - - - - Détail de(s) produit(s) commandés - - - - -
    {detail_produit}
            """
        ]
    corps_message=random.choice(corps_message)
    for destinataire in destinataires:
        
        
        message = MIMEMultipart()
        message["From"] = str(Header("Shoply 🛒 <{}>".format(expediteur), "utf-8"))
        message["To"] = destinataire
        message["Subject"] = Header("Alert vente 🎉 !!!")

        # Corps du mail
        corps = corps_message
        message.attach(MIMEText(corps, "plain"))

        try:
            # Connexion au serveur SMTP (ici Gmail)
            serveur = smtplib.SMTP("smtp.gmail.com", 587)
            serveur.starttls()  # Sécurise la connexion
            serveur.login(expediteur, mot_de_passe)  # Authentification
            serveur.sendmail(expediteur, destinataire, message.as_string())
            serveur.quit()
            print("✅ Email envoyé avec succès !")
        except Exception as e:
            print(f"❌ Erreur : {e}")
    
    # Alert chez Shoply





# Enregistrement images produits 

def enre_img_produit(image):
    response={}
    filename=[]
    public_id=[]
    # return "image[0].filename"
    # === Paramètres ===
    # image = input_img          # ton image d'origine
    # Exemple : gauche=60, haut=45, droite=60, bas=45
    target_size = (750, 650)       # dimensions voulues pour l'image
    bordures = (60, 45, 60, 45)               # épaisseur de la bordure blanche
    fill=(255, 192, 203)  # rose clair (équivalent à pink)
    
    # === 1) Ouvrir et redimensionner ===
    # img = Image.open(image)
    # img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

    # === 2) Ajouter la bordure blanche ===
    # img_with_border = ImageOps.expand(img_resized, border=bordures, fill="white")

    # === 3) Sauvegarder ===
    # output_path = "22.jpg"
    # img_with_border.save(output_path)
    # print(f"✅ Fichier créé : {output_path}")
    
    # image=request.files.getlist("image")
    UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/products"
    os.makedirs("products", exist_ok=True)
    try:
        for img in image:    
            # extension = os.path.splitext(img.filename)[1]  # garde .jpg, .png, etc.
            # unique_filename = str(uuid.uuid4()) + extension # ex: '88b3c7e2-31f5-4c91-89e6-b27b1e4b4b30.jpg'
            # file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            img= Image.open(img)
            img_resize = img.resize(target_size, Image.Resampling.LANCZOS)
            # Ajouter la bordure blanche
            # img_border = ImageOps.expand(img_resize, border=bordures, fill="white")
            img_border = img_resize
            
            buffer = io.BytesIO()
            img_border.save(buffer, format="JPEG")
            buffer.seek(0)


            upload_result = cloudinary.uploader.upload(buffer)
            image_url = upload_result['secure_url']
            public_ids = upload_result["public_id"]
            
            # img_border.save(file_path)
            filename.append(image_url)
            public_id.append(public_ids)
            # filename=unique_filename    
    except:
        filename.append("none")
        public_id.append("none")
    response={
        "url_image":filename,
        "public_id":public_id
    }
    return response

# Enregistrement images produits 

# Add br

def add_br(texte):
    response=""
    response=texte.replace("\r\n ", "<br>")
    response=texte.replace("\n ", "<br>")
    response=texte.replace("\n", "<br>")
    return response

# Add br

# login user
# login user
def login(user_name, pass_word):
    conn = con_BDD()
    cursor = conn.cursor(dictionary=True)  # 🔥 fetch en dict direct
    response = {}

    query = """
        SELECT * 
        FROM logins 
        WHERE (username = %s AND password = %s) 
           OR (email = %s AND password = %s)
    """
    cursor.execute(query, (user_name, pass_word, user_name, pass_word))
    result = cursor.fetchone()  # Un seul utilisateur

    if result:
        response = {
            "message": "connexion réussie",
            "username": result["username"],
            "profil": result["profil"]
        }
    else:
        response = {
            "message": "Nom d'utilisateur ou mot de passe incorrect",
            "username": "none",
            "profil": "none"
        }

    conn.close()
    return response

# login user

# new user
def New_user(elements=[]):
    conn=con_BDD()
    cursor=conn.cursor()
    user_name=elements[0]
    user_nom=elements[1]
    user_post_nom=elements[2]
    user_prenom=elements[3]
    user_tel=elements[4]
    user_email=elements[5]
    user_password=elements[6]
    user_profil=elements[7]

    query = "SELECT * FROM info_users WHERE Username = %s"
    cursor.execute(query, (user_name,))
    result = cursor.fetchone()

    if result:
        response="Le username exite déjà"
    else:
        try:
            query = "INSERT INTO logins (username,password,profil,email) values (%s,%s,%s,%s)"
            cursor.execute(query, (user_name,user_password,user_profil,user_email))
            conn.commit()
            # Vérifier les identifiants dans la base de données
            query = "INSERT INTO info_users (nom,postnom,prenom,tel,email,username) values (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (user_nom,user_post_nom,user_prenom,user_tel,user_email,user_name))
            conn.commit()
            response="Enregistrement reussi"
        except:
            response="Enregistrement a echoué"
    cursor.close()
    conn.close()
    return response
# new user

# chargement mse
def look_mse():
    conn=con_BDD()
    cursor=conn.cursor()
    conn2=con_BDD()
    cursor2=conn.cursor()
    error="error"
    try:
        query = "SELECT * FROM produits"
        cursor.execute(query)
        results = cursor.fetchall()  # Toutes les lignes du résultat

        if results:
            column_names = [desc[0] for desc in cursor.description]  # Récupérer les noms des colonnes
            produits = [dict(zip(column_names, row)) for row in results]  # Liste de dictionnaires

            # Affichage console (facultatif)
            # print(f"Succès : {len(produits)} produit(s) récupéré(s) !")
            # for produit in produits:
            #     # print("-" * 30)
            #     for key, value in produit.items():
            #         print(f"{key} : {value}")

            produits=produits
            
            # images produits
            i=0
            t=len(produits)
            while(i<t):
                id=produits[i]
                id=id["id"]
                query2 = "SELECT url_image FROM images_produits WHERE produit_id=%s ORDER BY est_principale DESC"
                cursor2.execute(query2,(id,))
                results2 = cursor2.fetchall()
                if results2:
                    b=[]
                    for a in results2:
                        b.append((a[0]))
                    produits[i]["image"]=b
                else: 
                   produits[i]["image"]=[] 
                i=i+1
            
            # images produits
            
            
        else:
            # print("Erreur : Aucun produit trouvé.")
            produits=[]
        error="none"
    except:
        error="error"
    response={
        "error":error,
        "produits":produits
    }
    cursor.close()
    conn.close()
    return response
# chargement mse   
  
# Updata mse    
def update(element):
    conn=con_BDD()
    cursor=conn.cursor()
    mse_id=element["id"]
    mse_nom=element["nom"]
    mse_des=element["description"]
    mse_prix=element["prix"]
    mse_stock=element["stock"]
    mse_cat=element["categorie"]
    mse_stat=element["statut"]
    mse_fsseur=element["fournisseur"]
    tel_fsseur=element["tel_fsseur"]
    try:
        query = "Update produits SET nom=%s,description=%s,prix=%s,stock=%s,categorie=%s,statut=%s,fournisseur=%s,tel_fsseur=%s where id=%s"
        cursor.execute(query, (mse_nom,mse_des,mse_prix,mse_stock,mse_cat,mse_stat,mse_fsseur,tel_fsseur,mse_id))
        conn.commit()
        response="update reussi"
    except:
        response="update a echoué"
    cursor.close()
    conn.close()
    return response
# Updata mse 

# New mse
def New_mse(element):
    conn=con_BDD()
    cursor=conn.cursor()
    mse_nom=element["nom"]
    mse_des=element["description"]
    mse_prix=element["prix"]
    mse_stock=element["stock"]
    mse_cat=element["categorie"]
    mse_stat=element["statut"]
    mse_fsseur=element["fournisseur"]
    tel_fsseur=element["tel_fsseur"]
    mse_images=element["image"]
    public_id=element["public_id"]
    try:
        query = "INSERT INTO produits (nom,description,prix,stock,categorie,statut,fournisseur,tel_fsseur) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (mse_nom,mse_des,mse_prix,mse_stock,mse_cat,mse_stat,mse_fsseur,tel_fsseur))
        conn.commit()
        last_mse=look_mse()
        last_mse=last_mse["produits"]
        last_mse=last_mse[len(last_mse) - 1]
        mse_id=last_mse["id"]
        i=0
        t=len(mse_images)
        est_principale=True
        while (i<t):
            if i==0:
               est_principale=True
            else :
                est_principale=False 
            query = "INSERT INTO images_produits (produit_id,url_image,est_principale,public_id) values (%s,%s,%s,%s)"
            cursor.execute(query, (mse_id,mse_images[i],est_principale,public_id[i]))
            conn.commit()
            i=i+1
        response="Enregistrement reussi"
    except:
        response="Enregistrement a echoué"
    cursor.close()
    conn.close()
    return response
# New mse

# supprimer mse
def sup(element):
    conn=con_BDD()
    cursor=conn.cursor()
    id=element["id"]
    try:
        
        query = "SELECT public_id FROM images_produits WHERE produit_id=%s"
        cursor.execute(query, (id,))
        results = cursor.fetchall()
        if results:
            for url in results:
                url=url[0]
                result = cloudinary.uploader.destroy(url)
                   
        query = "DELETE FROM produits WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        response="Suppression reussi"
    except:
        response="Suppression a echoué"
    cursor.close()
    conn.close()
    return response
# supprimer mse

# Add element to cart   
def add_el_cart(username,produit_id,quantite,add_ele):
    conn=con_BDD()
    cursor=conn.cursor()
    username=username
    produit_id=produit_id
    quantite=quantite
    add_ele=add_ele
    try:
        if (add_ele=='true'):
            query = "INSERT INTO cart (username,produit_id,quantite) values (%s,%s,%s)"
            cursor.execute(query, (username,produit_id,quantite,))
        else:
            query = "Update cart SET quantite=%s where username=%s AND produit_id=%s"
            cursor.execute(query, (quantite,username,produit_id))
        conn.commit()
        response="Enregistrement reussi"
    except:
        response="Enregistrement a echoué"
    cursor.close()
    conn.close()
    return response
# Add element to cart   

# chargement produit du cart   
def look_cart(username):
    conn = con_BDD()
    cursor = conn.cursor()
    error = "error"
    produits = []

    try:
        query = """
    SELECT
    c.id               AS cart_id,
    c.quantite,
    p.id               AS produit_id,
    p.nom,
    p.description,
    p.prix,
    img.url_image            AS image_url          -- image position = 1 (principale)
    FROM cart            AS c
    JOIN produits        AS p   ON p.id  = c.produit_id
    LEFT JOIN images_produits AS img
        ON img.produit_id = p.id
        AND img.est_principale   = 1
    WHERE c.username = %s;
        """
        cursor.execute(query, (username,))
        rows = cursor.fetchall()

        if rows:
            column_names = [desc[0] for desc in cursor.description]
            produits = [dict(zip(column_names, row)) for row in rows]
            error = "none"
        else:
            produits = []
            error = "none"

    except Exception as e:
        error = str(e)
        produits = []

    finally:
        cursor.close()
        conn.close()

    return {
        "error": error,
        "produits": produits
    }
# chargement produit du cart  

# supprimer element du cart
def del_ele_cart(username,produit_id,all):
    conn=con_BDD()
    cursor=conn.cursor()
    try:
        if (all=="false"):
            query = "DELETE FROM cart WHERE username = %s AND produit_id = %s"
            cursor.execute(query, (username,produit_id,))
        else:
            query = "DELETE FROM cart WHERE username = %s"
            cursor.execute(query, (username,)) 
        conn.commit()
        response="Suppression reussi"
    except:
        response="Suppression a echoué"
    cursor.close()
    conn.close()
    return response
# supprimer element du cart

# info de base de commandes de users
def info_base_com(info):
    response=""
    conn=con_BDD()
    cursor=conn.cursor()
    try:
        query = "SELECT * FROM info_base_com WHERE Username = %s"
        cursor.execute(query, (info["username"],))
        result = cursor.fetchone()
        if result:
            query = "UPDATE info_base_com Set prenom=%s,nom=%s,adresse=%s,reference_adresse=%s,ville=%s,pays=%s,code_postal=%s,email=%s,tel=%s,tel_whatsapp=%s WHERE Username = %s"
            cursor.execute(query, (info["prenom"],info["nom"],info["adresse"],info["reference"],info["ville"],info["pays"],info["postalcode"],info["email"],info["tel"],info["tel_what"],info["username"]))
            conn.commit()
        else:
            query = "INSERT INTO info_base_com (username,prenom,nom,adresse,reference_adresse,ville,pays,code_postal,email,tel,tel_whatsapp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (info["username"],info["prenom"],info["nom"],info["adresse"],info["reference"],info["ville"],info["pays"],info["postalcode"],info["email"],info["tel"],info["tel_what"]))
            conn.commit()
        response="reussi"
    except:
        response="error"
    cursor.close()
    conn.close()
    return response
# info de base de commandes de users

# resume commandes

def commandes_resume(info,produits):
    response=""
    conn=con_BDD()
    cursor=conn.cursor()
    try:
        query = "INSERT INTO commandes_resume (username,nombre_produits,sous_total,prix_livraison,prix_reduction,prix_total,prenom,nom,adresse,reference_adresse,ville,pays,code_postal,email,tel,tel_whatsapp) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (info["username"],info["nombre_produits"],info["sous_total"],info["prix_livraison"],info["prix_reduction"],info["prix_total"],info["prenom"],info["nom"],info["adresse"],info["reference"],info["ville"],info["pays"],info["postalcode"],info["email"],info["tel"],info["tel_what"]))
        id_commande = cursor.lastrowid
        
        for produit in produits:
            cursor.execute("""
                INSERT INTO produits_commande (id_commande, id_produit, quantite, prix_unitaire)
                VALUES (%s, %s, %s, %s)
            """, (id_commande, produit["id_produit"], produit["quantite_produit"], produit["prix_produit"]))
        
        conn.commit()
        response=["reussi",id_commande]
    except:
        response=response=["error",id_commande]
    
    
    cursor.close()
    conn.close()
    return response

# resume commandes

app=Flask(__name__)
app.secret_key="Daniel mambimbi@1"
CORS(app)

# defaut
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
@app.route('/')
def home():
    return "bienvenue"
# defaut

# login user
@app.route('/login',methods=["POST","GET"])
def logins():
    response=""
    # operation=request.form["operation"]
    user_name=request.form["login_user_name_value"]
    pass_word=request.form["login_pass_word_value"]
    response=login(user_name,pass_word)
    return response
# login user

# New user
@app.route('/New_user',methods=["POST","GET"])
def New_users():
    response="fdsfddsf"
    filename=""
    # # operation=request.form["operation"]
    user_name=request.form["user_name"]
    user_nom=request.form["user_nom"]
    user_post_nom=request.form["user_post_nom"]
    user_prenom=request.form["user_prenom"]
    user_tel=request.form["user_tel"]
    user_email=request.form["user_email"]
    user_password=request.form["user_password"]
    try:
        user_profil=request.form["user_profil"]
        filename="none"
    except:
        try:
            user_profil=request.files["user_profil"]
            # UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/Profil_users"
            # os.makedirs("Profil_users", exist_ok=True)
            # extension = os.path.splitext(user_profil.filename)[1]  # garde .jpg, .png, etc.
            # unique_filename = str(uuid.uuid4()) + extension # ex: '88b3c7e2-31f5-4c91-89e6-b27b1e4b4b30.jpg'
            # file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            # user_profil.save(file_path)
            # filename=unique_filename
            
            img=Image.open(user_profil)
            # unique_filename = str(uuid.uuid4())+".jpg"
            if img.mode!="RGB":
                img=img.convert("RGB")
            img_redim=img.resize((700,900),Image.LANCZOS)
            # filename=unique_filename
            
            buffer = io.BytesIO()
            img_redim.save(buffer, format="JPEG")
            buffer.seek(0)
            upload_result = cloudinary.uploader.upload(buffer)
            image_url = upload_result['secure_url']
            filename=image_url
            
        except:
            filename="none"
    
    # if filename!="none":
        
    #     buffer = io.BytesIO()
    #     img_redim.save(buffer, format="JPEG")
    #     buffer.seek(0)
    #     upload_result = cloudinary.uploader.upload(buffer)
    #     image_url = upload_result['secure_url']
    #     filename=image_url
        
        # img_redim.save(UPLOAD_FOLDER+"/"+unique_filename,format="jpeg",quality=80)
        # os.remove(file_path)
    # mim=mimetypes.guess_type(unique_filename)
    
    element=[user_name,user_nom,user_post_nom,user_prenom,user_tel,user_email,user_password,filename]
    response=New_user(element)
    return response
# New user

# New mse
@app.route('/New_mse',methods=["POST","GET"])
def New_mses():
    response="fdsfddsf"
    # # operation=request.form["operation"]
    macharndise=request.form["macharndises"]
    operation=request.form["operation"]
    macharndise=json.loads(macharndise)
    if operation=="Ajouter":
        response=New_mse(macharndise)
    elif operation=="Mettre à jour":
        response=update(macharndise)
    elif operation=="Supprimer":
        response=sup(macharndise)
    return response
# New mse

# delete element to cart
@app.route('/del_ele_cart',methods=["POST","GET"])
def del_ele_carts():
    response="fdsfddsf"
    # # operation=request.form["operation"]
    username=request.form["username"]
    produit_id=request.form["produit_id"]
    all=request.form["all"]
    response=del_ele_cart(username,produit_id,all)
    return response
# delete element to cart

# add element to cart
@app.route('/add_el_cart',methods=["POST","GET"])
def add_el_carts():
    response="fdsfddsf"
    # # operation=request.form["operation"]
    username=request.form["username"]
    add_ele=request.form["add_ele"]
    produit_id=request.form["produit_id"]
    quantite=request.form["quantite"]
    response=add_el_cart(username,produit_id,quantite,add_ele)
    return response
# add element to cart

# enregistrement image produit
@app.route('/enre_img_produit',methods=["POST","GET"])
def enre_img_produits():
    image=request.files.getlist("image")
    response=enre_img_produit(image)
    
    return response
# enregistrement image produit

# chargement mse
@app.route('/look_mse',methods=["POST","GET"])
def look_mses():
    return look_mse()
# chargement mse

# chargement mse du cart 
@app.route('/look_cart',methods=["POST","GET"])
def look_carts():
    username=request.form["username"]
    return look_cart(username)
# chargement mse du cart 

# Image mse or profil user
@app.route('/profil/<filename>')
def uploaded_file(filename):
    UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/Profil_users"
    
    if not (os.path.exists(UPLOAD_FOLDER+"/"+filename)):
        UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__))+"/products"
        
    return send_from_directory(UPLOAD_FOLDER,filename)
# Image mse or profil user

@app.route("/info_base_com",methods=["POST","GET"])
def info_base_coms():
    response=""
    response1=""
    response2=""
    info_com=request.form["info_com"]
    info_com=json.loads(info_com)
    produits=request.form["produits"]
    produits=json.loads(produits)
    produits=produits["produits"]
    enr_info_base=info_com["enr_info_base"]
    if(enr_info_base=="oui"):
        response1=info_base_com(info_com)
    response2=commandes_resume(info_com,produits)
    
    response={
        "response1":response1,
        "response2":response2[0],
        "id_commande":response2[1]
    }
    return response
@app.route("/send_mail",methods=["POST","GET"])
def send_mail():
    response=""
    type_mail=request.form["type_mail"]
    try:
        info_com=request.form["info_com"]
        info_com=json.loads(info_com)
        produits=request.form["produits"]
        produits=json.loads(produits)
        produits=produits["produits"]
        id_commande=request.form["id_commande"]
    except:
        response=""
    try:
        username=request.form["username"]
        email=request.form["email"]
    except:
       response=""
    
    if(type_mail=="com_re"):
        response=""
        conn=con_BDD()
        cursor=conn.cursor()
        try:
            info_bdd=False
            query = "SELECT prenom,nom,email FROM info_users WHERE username = %s"
            cursor.execute(query, (info_com["username"],))
            result = cursor.fetchone()

            if result:
                info_bdd={
                    "prenom":result[0],
                    "nom":result[1],
                    "email":result[2]
                    }
        except:
            info_bdd=False
        
        if(info_bdd):
            nom_client=f"""{info_bdd["prenom"]} {info_bdd["nom"]}"""
            mail_client_com(info_bdd["email"],id_commande,info_com["username"],info_com,produits)
        
        if (info_bdd["email"]!=info_com["email"]):
            mail_client_com(info_com["email"],id_commande,info_com["username"],info_com,produits)

    if (type_mail=="mail_to_new_user"):
        mail_to_new_user(username,email)
    return response

@app.route('/add_br',methods=["POST"])
def add_brs():
    message=request.form["message"]
    message=add_br(message)
    return message


# if __name__=="__main__":
#     app.run(host='0.0.0.0')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
