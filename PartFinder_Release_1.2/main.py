from flask import Flask, render_template, request, session, redirect, url_for, flash ,jsonify,abort
import sqlite3
import requests
import markdown
import re

#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#


# pour plus d'informations, consulter le README.md


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#

app = Flask(__name__)
app.secret_key = 'keyapp' # là car sinon marche pas 

Version = "Release 1.2"

#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#fonctions utiles

def requetes_marques_cpu():
    marques = None   
    conn = sqlite3.connect("cpu_db.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT name
            FROM manufacturer;""")
    marques = cursor.fetchall()
    conn.close()
    return marques
    
def requetes_marques_gpu():
    marques = None   
    conn = sqlite3.connect("gpu_db.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT name
            FROM manufacturer;""")
    marques = cursor.fetchall()
    conn.close()
    return marques

# fonction pour la visualisation des favoris (type_item sert pour la page login car il y a 2 bases de données) 
def view_favoris(user,iflogin = False):
    favoris_list = None   
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT name_item,type_item FROM Favoris WHERE id_user == ?""", (user,))
    favoris_list = cursor.fetchall()
    conn.close()
    # système pour soit renvoyer une liste avec seulement les noms des items, soit le nom et le type (utile pour la page login pour les liens "voir") 
    if iflogin : 
        return favoris_list
    else :
        return [ fl[0] for fl in favoris_list]
   

# reduperation des nom des colonnes des tables de la base de donnée
def name_column(database,table):
    columns = None
    connection = sqlite3.connect(database)
    try:
        cursor = connection.cursor()
        # Exécution de la requête PRAGMA pour obtenir les colonnes de la table
        cursor.execute(f"PRAGMA table_info ({table}) ;")
        columns = [column[1] for column in cursor.fetchall()]
    finally: #exécuter un code qui doit absolument s'exécuter qu'une erreur se produise ou non dans le bloc try
        connection.close() 
    return columns
        


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route index pour l'accueil 
@app.route('/')
def index() :

    print(Version)

    # visualisation des items les plus recents
    # 1
    resultats = None   
    conn = sqlite3.connect("gpu_db.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT Manufacturer.name AS manufacturer,Modele.name AS name ,Modele.releaseYear
                        FROM Modele
                        JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                        WHERE Modele.releaseYear IS NOT NULL AND Modele.releaseYear <> ''
                        ORDER BY Modele.releaseYear DESC;""")
    resultats = cursor.fetchall()
    conn.close()
    # 2
    resultats1 = None  
    conn1 = sqlite3.connect("cpu_db.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""SELECT Manufacturer.name,Modele.model
                        FROM Modele JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                        WHERE Modele.year NOT NULL ORDER BY Modele.year DESC ;""")  
    resultats1 = cursor1.fetchall()
    conn1.close()
    # 3
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None 
    # 4
    return render_template("index.html" ,resultats=resultats[:5] if resultats else None,resultats1=resultats1[:5] if resultats1 else None,favoris_list = favoris_list, show_loader=False)


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route pour les contacts 

# récupération du README qui fait office de Release note global
MARKDOWN_URL = 'https://raw.githubusercontent.com/TMoq22/Projets_lycee_TM/refs/heads/updates/README.md'

@app.route('/contact')
def contact():
    try:
        # Récupérer le Markdown brut depuis GitHub
        response = requests.get(MARKDOWN_URL)
        response.raise_for_status()
        contenu_markdown = response.text

        # Trouver toutes les sections qui commencent par "## Version"
        pattern = r'(##\s+Version\s+[^\n]+?\n(?:.+?\n)*?)(?=\n##|\Z)'
        matches = re.findall(pattern, contenu_markdown, flags=re.DOTALL)

        if not matches:
            derniere_version_html = "<p>Aucune version trouvée.</p>"
        else:
            # Prendre la première trouvée (car la plus récente est en haut)
            derniere_version_markdown = matches[0].strip()
            derniere_version_html = markdown.markdown(derniere_version_markdown)

    except Exception as e:
        derniere_version_html = f"<p>Erreur : {e}</p>"

    return render_template("contact.html", version=Version, show_loader=False, contenu_markdown=derniere_version_html)


#return # render_template("contact.html",version=Version, show_loader=False)

# route pour la liste de toute les pages indexées 
@app.route('/site_map')
def site_map():
    return render_template("site_map.html", show_loader=False)

# route pour les CGU 
@app.route('/cgu')
def cgu():
    return render_template("cgu.html", show_loader=False)


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#

# route pour la page amd
@app.route('/amd_data_base')
def amd_data_base():
    #Toutes les images, données, logos et noms sont la propriété d'© Advanced Micro Devices, Inc.
    return render_template("amd_data_base.html", show_loader=False)



#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route page de connexion
@app.route('/login')
def login():
    #1
    try :
        if session['user_id'] :
            favoris_list = view_favoris(session['user_id'],True)
            # recupere le type des items en plus des noms pour pouvoir construire les bon liens pour la page 'info...' correspondant
            # car 2 bases de données et donc 2 recherches diffentes
    except :
        favoris_list = None    
    #2
    message = ("","")
    return render_template("login.html",favoris_list = favoris_list, show_loader=False,message = message)
    
# verification pseudo et mot de passe
@app.route('/check_login', methods=['GET', 'POST'])
def check_login() :
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, pseudo, id_autorisation FROM Utilisateur WHERE pseudo = ? AND password = ?", (pseudo, password))
        user = cursor.fetchone()
        conn.close()        
        if user:
          
            session['user_id'] = user[0]
            session['pseudo'] = user[1]            
            session['autorisation'] = user[2]
          
            return render_template('login.html', show_loader=False,message =("Connexion réussie!","vert"),favoris_list = None)
          
    return render_template('login.html', show_loader=False,message =("Pseudo ou mot de passe incorrect","rouge"),favoris_list = None)

# route de deconnection 
@app.route('/disconnect')
def disconnect() :
    session.pop('pseudo', None)
    session.pop('user_id', None)
    session.pop('autorisation', None)
    return redirect(url_for('index'))

# route d'inscription 
@app.route('/inscription')
def inscription() :
    if 'pseudo' in session :
        return render_template('login.html', show_loader=False,message =("vous êtes déjà connecté !","rouge"))
    
    return render_template('inscription.html',message = ("",""))
# verification pseudo et mot de passe pour inscription (copier/coller du tuto)
@app.route("/check_signin", methods=['POST', 'GET'])
def check_signin():
    if 'pseudo' in session :
        return redirect(url_for('index'))
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        user = cursor.fetchone()
        conn.close()
        if user :
            return render_template('inscription.html',message =("Le pseudo est déjà utilisé","rouge"))
        if password != password2 :
            return render_template('inscription.html',message =("Les mots de passe ne correspondent pas","rouge"))
        if len(password)<10 :
            return render_template('inscription.html',message =("le mot de passe doit être au moins de longueur 10","rouge"))            
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Utilisateur(pseudo, password, email, id_autorisation) VALUES (?, ?, ?, 1) ;""", (pseudo, password,email,))
        conn.commit()
        conn.close()
   
        
        return render_template('login.html', show_loader=False,message =("Vous êtes inscrit·e. Veuillez vous connecter !","vert"))
    return render_template('inscription.html', show_loader=False,message =("",""))


# route modification mot de passe
@app.route('/update_account')
def update_account():
    return render_template('update_account.html ',show_loader=False,message =("",""))

@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    if 'pseudo' in session:
        if request.method == 'POST':
            pseudo = session['pseudo']
            oldpassword = request.form['password']
            newpassword = request.form['password2']
            newpassword2 = request.form['password3']

            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM Utilisateur WHERE pseudo = ?", (pseudo,))
            result = cursor.fetchone()
            conn.close()

            if result is None or oldpassword != result[0]:
                return render_template('update_account.html', show_loader=False, message=("mot de passe incorrect", "rouge"))

            if len(newpassword) < 10:
                return render_template('update_account.html', show_loader=False, message=("le mot de passe doit être au moins de longueur 10", "rouge"))

            if newpassword != newpassword2:
                return render_template('update_account.html', show_loader=False, message=("nouveau mot de passe incorrect", "rouge"))

            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Utilisateur
                SET password = ?
                WHERE pseudo = ?
            """, (newpassword, pseudo))
            conn.commit()
            conn.close()

            session.clear()
            return render_template('login.html', show_loader=False, message=("Votre mot de passe est bien modifié !", "vert"))

        return render_template('update_account.html', show_loader=False)

    return render_template('login.html', show_loader=False, message=("Vous devez être connecté pour modifier votre mot de passe !", "rouge"))

# route de suppression du compte
@app.route('/delete')
def delete() :
    
    return render_template('delete.html', show_loader=False,message=("",""))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Récupérer le pseudo depuis la session
    pseudo = session.get('pseudo')
    if not pseudo:
        return render_template('login.html', show_loader=False,message=("Vous devez être connecté pour supprimer votre compte !","rouge"))

    # Récupérer le mot de passe entré par l'utilisateur
    password = request.form.get('password')
    
    # Connexion à la base de données
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    # Récupérer les infos utilisateur
    cursor.execute("SELECT id, password FROM Utilisateur WHERE pseudo like ?", (pseudo,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
 
        # Vérifier que le mot de passe est correct
        if password == user[1]:
            # Supprimer les favoris de l'utilisateur
            cursor.execute("DELETE FROM Favoris WHERE id = ?", (user_id,))
            # Supprimer l'utilisateur lui-même
            cursor.execute("DELETE FROM Utilisateur WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()

            # Nettoie la session et redirige
            session.clear()
            print("clear")
     
            return redirect(url_for("index"))
        else:
            return render_template('delete.html', show_loader=False,message=("Mot de passe incorrect.","rouge"))
    else:
        return render_template('delete.html', show_loader=False,message=("Utilisateur introuvable.","rouge"))

    
    return redirect(url_for("delete"))
    
    


# route addministration 
@app.route('/administrateur')
def administrateur() :
    if 'user_id' not in session :
        abort(403, "Cette operation n'est pas autorisee")
    else:
        if session['autorisation'] == 0 :
            users = None
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, pseudo, email, id_autorisation FROM Utilisateur")
            users = cursor.fetchall()
            conn.close()        
            return render_template('administrateur.html',users=users, show_loader=False)
        else :
            abort(403, "Cette operation n'est pas autorisee")
            


@app.route('/delete_account_admin', methods=['POST'])
def delete_account_admin():
     
     # Récupérer le mot de passe entré par l'utilisateur
    user_id= request.form.get('id_account')
     
    # Connexion à la base de données
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
  
    if user_id != 0 :
        # Supprimer les favoris de l'utilisateur
        cursor.execute("DELETE FROM Favoris WHERE id = ?", (user_id,))
        # Supprimer l'utilisateur lui-même
        cursor.execute("DELETE FROM Utilisateur WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        flash("Compte supprimé avec succès.")
        print("Compte supprimé avec succès.")
        return redirect(url_for("administrateur"))
        
    else:
        flash("Utilisateur introuvable.")
        print("Utilisateur introuvable.")

    conn.close()
    return redirect(url_for("administrateur"))
    


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
# routes pour les differentes recherches possibles ( CPU / GPU )
# CPU #

@app.route('/searchCPU') # page de base (cpu)
def searchCPU():
    marques = requetes_marques_cpu()

    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
        
    return render_template("searchCPU.html", marques=marques,filtres = ['',''],favoris_list = favoris_list, show_loader=False,message=("",""))

@app.route('/check_filtre', methods=['GET', 'POST']) #requete sql
def check_filtre():
    resultats = None
    max_items = 0  
    filtre = ""
    message = ("","")
    if request.method == 'POST':
        filtre = request.form.get('filtre', '')  

        if filtre:  
            conn = sqlite3.connect("cpu_db.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Manufacturer.name,model,year,cores,socket FROM Modele JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id WHERE Modele.model LIKE (?); " , ('%'+filtre+'%',))  #Manufacturer.nom LIKE (?) and '%'+filtre1+'%',
            resultats = cursor.fetchall()
            conn.close()
       
        # max item 
        if resultats is not None:
            max_items=len(resultats)
        else :
            max_items= 0
    # liste favoris
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
    
    
    if resultats is None or resultats == []:
        message = ("aucun resultats","rouge")
    else :
        message = ("","")
        
    # marque dispo
    marques = requetes_marques_cpu()
    return render_template('searchCPU.html', resultats=resultats if resultats else None, filtres = [filtre], max_items=max_items,marques=marques, favoris_list = favoris_list , show_loader=True,message=message) 


@app.route('/info_cpu/<item_name>')# route qui permet d'avoir toute les infos disponible sur le composant choisi
def info_cpu(item_name):
    resultats = None
    conn = sqlite3.connect("cpu_db.db")
    cursor = conn.cursor()      
    cursor.execute("""SELECT 
                    Modele.id , Manufacturer.name AS manufacturer, model,microarch,Family.family_name AS family ,Codename.name AS codename,fab,frequency,L2_units,L2_unit_size,L2_total,L3_Cache,Cores,Threads,TDPMin,TDPMax,socket,
                    year,Part_Number,X86_64,PAE,MMX,_3DNow,SSE,SSE2,SSE3,SSSE3,SSE4a,SSE4_1,SSE4_2,AVX,AVX2,NX_bit,AES,RDRAND,VT,HT,TB,GPU_present,GPU_Microarch,
                    GPU_Model,DirectX,OpenGL,OpenCL,Vulkan,Video_Decode,MPEG_2,MPEG_4,VC1,H_264,H_265,VP9,JPEG
                    FROM Modele                   
                    JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                    JOIN Codename ON Modele.codename = Codename.id
                    JOIN Family ON Modele.family = Family.id
                    WHERE Modele.model LIKE (?); """, (item_name,))
    
    resultats = cursor.fetchall()
    columns = [description[0] for description in cursor.description]  # Récupère les noms des colonnes
    conn.close()
    return render_template("info_cpu.html",resultats=resultats if resultats else None, columns=columns, show_loader=True)


# GPU #
@app.route('/searchGPU')# page de base (gpu)
def searchGPU():
    marques = requetes_marques_gpu()
   
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
        
    return render_template("searchGPU.html",filtres =['',''] ,marques=marques ,favoris_list =favoris_list, show_loader=False,message = ("",""))


@app.route('/check_filtre_gpu', methods=['GET', 'POST'])#requete sql en fonction du/des filtres passés en argument 
def check_filtre_gpu():
    resultats_gpu = None
    max_items = 0 
    filtre = ""
    message = ("","")
    if request.method == 'POST':
        filtre = request.form.get('filtre', '')
        
        if filtre:
       
            conn = sqlite3.connect("gpu_db.db")
            cursor = conn.cursor()
            if filtre :
                requete = """SELECT Modele.name,releaseYear,gpuChip,Manufacturer.name
                            FROM Modele
                            JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                            where Modele.name like ? ;"""

            cursor.execute(requete, ('%'+ filtre +'%',))
            resultats_gpu  = cursor.fetchall()
            conn.close()
            

        # max item         
        if resultats_gpu is not None:
            max_items=len(resultats_gpu)
        else :
            max_items= 0
    # liste favoris
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
    # marques dispo
    marques = requetes_marques_gpu()
    
    if resultats_gpu is None or resultats_gpu == []:
        message = ("aucun resultats","rouge")
    else :
        message = ("","")

    return render_template('searchGPU.html', resultats_gpu = resultats_gpu if resultats_gpu else None,filtres =[filtre],max_items=max_items,marques = marques,favoris_list=favoris_list, show_loader=True,message = message)


@app.route('/info_gpu/<item_name>')  # route qui permet d'avoir toutes les infos disponibles sur le composant choisi
def info_gpu(item_name):
    resultats = None
    columns = None  # Variable pour stocker les noms des colonnes
    conn = sqlite3.connect("gpu_db.db")
    cursor = conn.cursor()
    requete = """SELECT Modele.id, Manufacturer.name, Modele.name, releaseYear, memSize, memBusWidth, gpuClock, memClock, unifiedShader, tmu, rop, pixelShader, vertexShader, igp, bus, memType, gpuChip, RTcore,CUDA_ZLUCDA,tensor_core
                FROM Modele
                JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                WHERE Modele.name == ? ;"""
    cursor.execute(requete, (item_name,))
    resultats = cursor.fetchall()
    columns = [description[0] for description in cursor.description]  # Récupère les noms des colonnes
    conn.close()
    return render_template("info_gpu.html", resultats=resultats if resultats else None, columns=columns, show_loader=True)

# ajoute suppression favoris 
@app.route('/toggle_favorite/<item_name>/<type_item>', methods=['POST'])
def toggle_favorite(item_name,type_item):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour ajouter/supprimer des favoris.", "danger")
        return redirect(url_for('login'))
    user_id = session['user_id']
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    # Vérifiez si l'article est déjà dans les favoris
    cursor.execute("SELECT * FROM Favoris WHERE id_user = ? AND name_item = ?", (user_id, item_name))
    favorite_item = cursor.fetchone()
    if favorite_item:
        cursor.execute("DELETE FROM Favoris WHERE id_user = ? AND name_item = ?", (user_id, item_name))
        flash(f'{item_name} a été supprimé des favoris', 'success')
    else:
        cursor.execute("INSERT INTO Favoris (id_user, name_item,type_item) VALUES (?, ?, ?)", (user_id, item_name, type_item))
        flash(f'{item_name} a été ajouté aux favoris', 'success')
    conn.commit()
    conn.close()
    # Redirection vers la page sur laquelle se trouvait l'utilisateur
    return redirect(request.referrer)  



#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
# routes d'ajout d'items
# /!\ /!\  fonctionnalité abandonnée /!\ /!\
@app.route('/add_cpu')
def add_cpu():
    if 'user_id' not in session :
        abort(403, "Cette operation n'est pas autorisee")
    else:
        if session['autorisation'] == 0 :
            list_name_column = name_column('cpu_db.db','Modele')
            return render_template("add_cpu.html",list_name_column=list_name_column, show_loader=False)
        else :
            abort(403, "Cette operation n'est pas autorisee")


@app.route('/add_gpu')
def add_gpu():
    if 'user_id' not in session :
        abort(403, "Cette operation n'est pas autorisee")
    else:
        if session['autorisation'] == 0 :
            return render_template("add_gpu.html", show_loader=False)
        else :
            abort(403, "Cette operation n'est pas autorisee")
    

@app.route('/check_insert_value', methods=['GET', 'POST'])
def check_insert_value():
    item_list = []
    list_name_column = name_column('cpu_db.db','Modele')
    if request.method == 'POST':  
        for column in list_name_column :
            
            if request.form.get(column, '') is None :
                item_list.append(None)
            else :
                item_list.append((column,request.form.get(column, '')))

        print(item_list[2][1])
        print(item_list)
        
    return redirect(url_for('add_cpu'))

#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
# pages d'erreurs 
@app.errorhandler(404)
def not_found(e):
    return render_template('error_page.html',error = 404, show_loader=True),404

@app.errorhandler(403)
def forbidden(n):
    return render_template('error_page.html',error = 403, show_loader=True),403


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
# lance l'app
if __name__ == "__main__" :
    #app.run(port=5559)
    app.run(host='0.0.0.0', port=5559)
    
#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#

#Credits :
#Titouan Moquet
#Term NSI 2024~2025
    