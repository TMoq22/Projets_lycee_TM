
## Présentation du projet Flask
Ce projet a été réalisé dans le cadre de la spécialité NSI. Il consiste en la création d'une application web le module Python : Flask.

> [!NOTE] <!-- block visible depuis le GitHub -->
> Note du projet (à venir)

## 🔨 Technologies utilisées
- **Langages** : Python (Flask), HTML, CSS, JavaScript  
- **Base de données** : SQLite, SQL  
- **Outils** : Flask, Jinja2

## Fonctionnalités principales
- Page d'accueil dynamique  
- Système de gestion des utilisateurs (inscription, connexion, modification de mot de passe)  
- Stockage et affichage de données  

## 🚫 Fonctionnalités abandonnées
__Fonctionnalités que j'aurais aimé réaliser ou abandonnées pour des contraintes techniques__ :
- Modification de la base de données depuis le site (abandonnée)  
- Système de tri des tableaux  
- Modification de la base de données pour y ajouter des éléments comme des images ou des informations (abandonnée)  
- Hachage des mots de passe pour un système plus sécurisé  
- Transmission des données via `jsonify`  
- Pouvoir simplement taper le nom de la marque et afficher les derniers processeurs sortis  

## 📄 Notes
- Je me suis rendu compte après coup du fonctionnement du système `flash` de Flask, donc il n’est utilisé que pour une seule page (la page admin). J’ai fait un système alternatif qui fonctionne aussi bien, voire mieux dans mon cas, car il me permet de modifier le CSS en fonction des informations à transmettre.  
- La page __AMD__ a, je pense, été l’une des plus compliquées à faire au niveau du CSS. Le CSS se trouve dans un autre fichier pour des raisons de praticité. Cette page est fortement inspirée et copiée du site d’[AMD](https://www.amd.com/fr.html).  
- Concernant le JavaScript, j’ai principalement trouvé ces codes sur Internet et je les ai adaptés à mon projet.  

## 📄 Notes 2
- Quasiment toutes les versions du projet sont disponibles sur le GitHub et donc accessibles à tout moment : [Le GitHub](https://github.com/TMoq22/Projets_lycee_TM/)  
> Pour le GitHub : les versions intermédiaires sont dans la branche `updates`. La dernière version se trouve dans le dossier `/Projets_NSI/Flask`, accessible [ici](https://github.com/TMoq22/Projets_lycee_TM/tree/main/Projets_NSI/Flask).  
- Un serveur Discord est également disponible via ce lien : [Le Discord](https://discord.gg/ceg7zHeX7c), sur lequel vous pouvez m’envoyer des messages.  
- Le fichier `release_notes` fournit des informations sur les différentes mises à jour.  

## À propos du code
- J’ai essayé de commenter la plupart des parties importantes du code (Python, JS, CSS et certaines pages comme `base`, etc.). Il peut rester quelques fautes, j’ai fait au mieux.  
- Certaines parties ne respectent pas totalement le principe D.R.Y (Don't Repeat Yourself), notamment le JS pour les fonctions `toggleIcon`, mais cette solution me semblait plus simple.  

ℹ️ Des modifications pourront être apportées après l’évaluation, juste pour le fun.

## Installation et exécution
1. Executer : main.py
2. Accéder à l'application via `http://127.0.0.1:5559` ou `http://192.168.1.48:5559` 
> grâce a la 2ème URL vous pouver vous connecter au site depuis un autre ordinateur local a condition que le programme soit executé

## ©️ Crédits
- Développement : Titouan Moquet 
- Année scolaire : Term 2024-2025

> Version actuel : V2.4 Beta2.5.8 (voir release note)  
> Version final : V2.5 

<!-- je peux fournir toute les versions que je possède sur demande -->
<!-- désolé s'il reste des fautes dans les commentaires ou les readmes :) -->
<!-- last editing 13/05/2025 -->
