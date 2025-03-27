from flask import Flask, render_template, request, session, redirect, url_for, flash ,jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'key' # là car sinon marche pas 



#note :


# - correction bug systeme "afficher plus"
# - probleme ordre de la requete info_cpu et info _gpu
# correction css




# si possible et si temps  : 
# icon svg a remplacer
# faire syteme de favoris 



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

def view_favoris(user):
    favoris_list = None   
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT name_item FROM Favoris WHERE id_user == ?""", (user,))
    favoris_list = cursor.fetchall()
    conn.close()
    return [ fl[0] for fl in favoris_list]

 
def name_column(database,table):
    # reduperation des nom des colonnes des tables de la base de donnée
    columns = None
    connection = sqlite3.connect(database)
    try:
        cursor = connection.cursor()
        # Exécution de la requête PRAGMA pour obtenir les colonnes de la table
        cursor.execute(f"PRAGMA table_info ({table}) ;")
        
        columns = [column[1] for column in cursor.fetchall()]
        #print(columns)

    finally: #exécuter un code qui doit absolument s'exécuter qu'une erreur se produise ou non dans le bloc try
        connection.close()
        
    return columns
        


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route index pour l'accueil 
@app.route('/')
def index() :
    
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
    
    
    resultats1 = None  
    conn1 = sqlite3.connect("cpu_db.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""SELECT Manufacturer.name,Modele.model
                        FROM Modele JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                        WHERE Modele.year NOT NULL ORDER BY Modele.year DESC ;""")  
    resultats1 = cursor1.fetchall()
    
    conn1.close()
    
    #if session['user_id'] is not None :
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None 

    return render_template("index.html" ,resultats=resultats[:5] if resultats else None,resultats1=resultats1[:5] if resultats1 else None,favoris_list = favoris_list)


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route index pour les contacts 
@app.route('/contact')
def contact():
    return render_template("contact.html")


#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
#route pour de connexion
@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/connexion')
def connexion() :
    return render_template('connexion.html')


@app.route('/check_login', methods=['GET', 'POST'])
def check_login() :
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, pseudo, id_autorisation FROM Utilisateur WHERE pseudo = ? AND password = ?", (pseudo, password))
        user = cursor.fetchone()
        conn.close()        
        if user:
            flash('Connexion réussie!', 'success')
            session['user_id'] = user[0]
            session['pseudo'] = user[1]            
            session['autorisation'] = user[2]
            return redirect(url_for('index'))
            print('succes')
        else:
            print('Echec')
            flash('Pseudo ou mot de passe incorrect', 'danger')

    return render_template('login.html')

@app.route('/disconnect')
def disconnect() :
    session.pop('pseudo', None)
    session.pop('user_id', None)
    session.pop('autorisation', None)
    print("out")
    print(session)
    return redirect(url_for('index'))



@app.route('/inscription')
def inscription() :
    return render_template('inscription.html')

@app.route("/check_signin", methods=['POST', 'GET'])
def check_signin():
    if 'pseudo' in session :
        flash("Vous êtes déjà inscrit·e !")
        return redirect(url_for('index'))
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        user = cursor.fetchone()
        conn.close()
        if user :
            flash("Le pseudo est déjà utilisé")
            return render_template('inscription.html')
        if password != password2 :
            flash("Les mots de passe ne correspondent pas")
            return render_template('inscription.html')
        if len(password)<10 :
            flash("le mot de passe doit être au moins de longueur 10")
            return render_template('inscription.html')            
        conn = sqlite3.connect('chat.db')
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Utilisateur(pseudo, password, email, id_autorisation) VALUES (?, ?, ?, 1) ;""", (pseudo, password,email,))
        conn.commit()
        conn.close()
        flash("Vous êtes inscrit·e. Veuillez vous connecter !")
        return redirect(url_for("login"))
        
        
    return render_template('inscription.html')


@app.route('/delete')
def delete() :
    return render_template('delete.html')

@app.route('/administrateur')
def administrateur() :
    return render_template('administrateur.html')



#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#
# routes pour les differentes recherches possibles 
# CPU #

@app.route('/searchCPU') # page de base 
def searchCPU():
    
    marques = requetes_marques_cpu()
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
        
    return render_template("searchCPU.html", marques=marques,filtres = ['',''],favoris_list = favoris_list)

@app.route('/check_filtre', methods=['GET', 'POST']) #requete sql
def check_filtre():
    resultats = None
    max_items = 0  
    filtre = "" 
    if request.method == 'POST':
        filtre = request.form.get('filtre', '')  
        
        if not filtre:  
            flash('Veuillez remplir tous les champs.', 'warning')
        else:
            conn = sqlite3.connect("cpu_db.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Manufacturer.name,model,year,cores,socket FROM Modele JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id WHERE Modele.model LIKE (?); " , ('%'+filtre+'%',))  #Manufacturer.nom LIKE (?) and '%'+filtre1+'%',
            resultats = cursor.fetchall()
            conn.close()
            if not resultats:
                flash('Aucun résultat trouvé pour votre recherche.', 'warning')
                
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
    # marque dispo 
    marques = requetes_marques_cpu()
    return render_template('searchCPU.html', resultats=resultats if resultats else None, filtres = [filtre], max_items=max_items,marques=marques, favoris_list = favoris_list ) 


@app.route('/info_cpu/<producter>/<item_name>')# route qui permet d'avoir toute les infos disponible sur le composant choisi
def info_cpu(item_name,producter):
    
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
    return render_template("info_cpu.html",resultats=resultats if resultats else None,producter = producter, columns=columns )


# GPU #
@app.route('/searchGPU')# page de base 
def searchGPU():
    marques = requetes_marques_gpu()
    
    try :
        favoris_list = view_favoris(session['user_id'])
    except :
        favoris_list = None
        
    return render_template("searchGPU.html",filtres =['',''] ,marques=marques ,favoris_list =favoris_list )


@app.route('/check_filtre_gpu', methods=['GET', 'POST'])#requete sql en fonction du/des filtres passés en argument 
def check_filtre_gpu():
    resultats_gpu = None
    max_items = 0 
    filtre = "" 
    if request.method == 'POST':
       
        filtre = request.form.get('filtre', '')  
       
        if not filtre:
            flash('Veuillez remplir tous les champs.', 'warning')
        else:
            conn = sqlite3.connect("gpu_db.db")
            cursor = conn.cursor()
            if filtre :
                requete = """SELECT Modele.name,releaseYear,gpuChip,Manufacturer.name
                            FROM Modele
                            JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                
                            where Modele.name like ? ;"""
            else:
                flash("Option invalide pour le filtre.", "warning")
                
                return render_template('searchGPU.html', resultats_gpu =None,filtres =[filtre])
            
            cursor.execute(requete, ('%'+ filtre +'%',))
            resultats_gpu  = cursor.fetchall()
            conn.close()
            if not resultats_gpu :
                flash('Aucun résultat trouvé pour votre recherche.', 'warning') 
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
    return render_template('searchGPU.html', resultats_gpu = resultats_gpu if resultats_gpu else None,filtres =[filtre],max_items=max_items,marques = marques,favoris_list=favoris_list)


@app.route('/info_gpu/<item_id>')  # route qui permet d'avoir toutes les infos disponibles sur le composant choisi
def info_gpu(item_id):
    resultats = None
    columns = None  # Variable pour stocker les noms des colonnes
    conn = sqlite3.connect("gpu_db.db")
    cursor = conn.cursor()
    requete = """SELECT Modele.id, Manufacturer.name, Modele.name, releaseYear, memSize, memBusWidth, gpuClock, memClock, unifiedShader, tmu, rop, pixelShader, vertexShader, igp, bus, memType, gpuChip, RTcore
                FROM Modele
                JOIN Manufacturer ON Modele.manufacturer = Manufacturer.id
                WHERE Modele.name == ? ;"""
    cursor.execute(requete, (item_id,))

    resultats = cursor.fetchall()
    columns = [description[0] for description in cursor.description]  # Récupère les noms des colonnes
    conn.close()

    return render_template("info_gpu.html", resultats=resultats if resultats else None, columns=columns)



@app.route('/toggle_favorite/<item_name>', methods=['POST'])
def toggle_favorite(item_name):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour ajouter/supprimer des favoris.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    # Vérifiez si l'article est déjà dans les favoris
    cursor.execute("SELECT * FROM Favoris WHERE id_user = ? AND name_item = ?", (user_id, item_name))
    favorite_item = cursor.fetchone()

    if favorite_item:
       
        cursor.execute("DELETE FROM Favoris WHERE id_user = ? AND name_item = ?", (user_id, item_name))
        flash(f'{item_name} a été supprimé des favoris', 'success')
    else:
       
        cursor.execute("INSERT INTO Favoris (id_user, name_item) VALUES (?, ?)", (user_id, item_name))
        flash(f'{item_name} a été ajouté aux favoris', 'success')

    conn.commit()
    conn.close()

    # Redirection vers la page sur laquelle se trouvait l'utilisateur
    return redirect(request.referrer)  



#/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\##/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\/|\#

@app.route('/add_cpu')
def add_cpu():
    
    list_name_column = name_column('cpu_db.db','Modele')
    print(list_name_column)
    return render_template("add_cpu.html",list_name_column=list_name_column)

@app.route('/add_gpu')
def add_gpu():
    return render_template("add_gpu.html")

@app.route('/check_insert_value', methods=['GET', 'POST'])
def check_insert_value():
    pass
    return redirect(url_for('add_cpu'))
    




if __name__ == "__main__" :
    app.run(port=5558)
