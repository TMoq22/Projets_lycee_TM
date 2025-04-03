/* il est possible que les lignes de couleurs qui sont à gauche et
 à droite du titre ne soi pas correctement affichées  */

/*masque la zone de jeu et affiche le menu principal*/
document.getElementById("bienvenue").style.display = 'block';
document.getElementById("jeu").style.display = 'none';

/*récupere les données entrées par le joueur pour le jeu*/
window.addEventListener('load',()=>{
const Carac = document.getElementById("Carac");

document.getElementById("salaire_output").textContent = 'Salaire : '+(20-Carac.value);
document.getElementById("temps_output").textContent = 'Temps : '+(20+parseInt(Carac.value));

Carac.addEventListener("input", function () {
    document.getElementById("salaire_output").textContent = 'Salaire : '+(20-Carac.value);
    document.getElementById("temps_output").textContent = 'Temps : '+(20+parseInt(Carac.value));
});

});

/*variable pour les maisons*/
var maison = {
    1 : 0,
	2 : 0,
	3 : 0,
	4 : 0,
	5 : 0,
};

/* fonction pour revenir à la page d'accueil elle reset la progression du jeu  */
function home(){
    
    document.getElementById("bienvenue").style.display = 'block';
    document.getElementById("jeu").style.display = 'none';
	document.getElementById("Easter_egg").style.display = 'none';

}


/* Creation d'une variable contenant les caracteristiques du personnage */
var perso = {
    nom: "Skywalker",
	prenom: "Anakin ",
    sexe: "masculin",
    salaire : 20 ,
    temps : 20 ,
	argent : 0,
	score_fin : 0,
	
};

/* récupération des données de bases du personnage */
function get_carac(){
	perso.prenom = document.getElementById("perso_prenom").value;
    perso.nom = document.getElementById("perso_nom").value;
    perso.salaire = 20-parseInt(document.getElementById("Carac").value);
    perso.temps = 20+parseInt(document.getElementById("Carac").value);
    
    document.getElementById("bienvenue").style.display = 'none';
    document.getElementById("jeu").style.display = 'block';
    levels = generate_levels();
    set_level(0);
    
}




/*variable de niveau*/

var niveau={
	1:2,
	2:5,
	3:8,
	4:10,
	5:11,
}

/*variable pour les maps*/
let levels = new Map();



/* Utilisation des niveaux , difinie les levels avec des carteristiques et choix differents pour le jeu*/
function generate_levels(){
	
		/*Texte fin : Abondonner le travail*/
	levels.set(100,{
        action : [["cache_info",10]],
		text : ["TU AS PERDU ",
		"Tu as abandonné ton travail !"],
		choices : [["Aller à l'acceuil",69]], 
        });
		
	/*Texte fin : Livrer toutes les pizza*/
	levels.set(101,{
        action : [["cache_info",10]],
		text : ["TU AS GAGNER",
		"Tu as livré toutes les pizza !"],
		choices : [["Aller à l'acceuil",69]], 
        });
	
	/*Texte fin : Plus d'argent*/
	levels.set(102,{
        action : [["cache_info",10]],
		text : [" TU AS PERDU",
		"Tu as perdu tout ton argent !"],
		choices : [["Aller à l'acceuil",69]], 
        });
	
	/*Texte fin : Temps dépassé*/
	levels.set(103,{
        action : [["cache_info",10]],
		text : ["TU AS PERDU ",
		" Tu as mis trop de temps à livrer les pizza"],
		choices : [["Aller à l'acceuil",69]], 
        });
		
	
		
		/*Retourne à l'acceuil*/
	levels.set(69,{
        action : [["reset",10]],
		text : ["GG"],
		choices : [["Recommencer",0]], 
        });
		/*reste des leveles*/
    levels.set(0,{
        action : [["montre_info",10]],
        text : ['Bienvenue dans la pizzeria '+perso.prenom+'. Tu as un temps de '+perso.temps+' min.',
        " Tu dois livrer le maximum de pizza dans le temps imparti.",
        " Que veux-tu faire ?"],
        choices : [["Avancer", 1],
                ["Abandonner", 100]]
        });

    levels.set(1,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
		
        choices : [["Aller à droite", 14],
				["Aller à gauche", 2],
				["Aller en bas", 0]]
        });

    levels.set(2,{
        action : [['visite_maison',1]],
        text : livraison(1),
        choices : [["Aller en haut", 3],
                    ["Aller à droite", 1]]
        });

    levels.set(3,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller à droite", 10],
					["Aller à gauche", 4],
                    ["Aller en bas", 2]]
        });

    levels.set(4,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller en haut", 6],
					["Aller à droite", 3],
                    ["Aller à gauche", 5]]
    });
	
	levels.set(5,{
        action : [['visite_maison',2]],
        text : livraison(2),
        choices : [["Aller à droite", 4]]
    });
	
	levels.set(6,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller en haut", 7],
					["Aller à droite", 8],
                    ["Aller à gauche", 4]]
    });
	
	levels.set(7,{
        action : [['perte_argent', perso.salaire]],
        text : ["Oh non ! Tu t'es fait volé 1 pizza . Tu as perdu "+perso.salaire+" €."],
        choices : [["Aller en bas", 6]]
    });
	
	levels.set(8,{
        action : [['visite_maison',3]],
        text : livraison(3),
        choices : [["Aller à gauche", 6],
                    ["Aller à droite", 9]]
    });
	
	levels.set(9,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller à gauche", 10],
					["Aller en haut", 8],
					["Aller en bas", 14],
                    ["Aller à droite", 11]]
    });
	
	levels.set(10,{
        action : [['visite_maison',4]],
        text : livraison(4),
        choices : [["Aller à droite", 9],
					["Aller à gauche", 3]
                    ]
    });
	
	levels.set(11,{
        action : [['visite_maison',5]],
        text : livraison(5),
        choices : [["Aller à gauche", 9],
                    ["Aller en bas", 12]]
    });
	
	levels.set(12,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller en haut", 11],
					["Aller à gauche", 14],
					["Aller en bas", 13]]
    });
	
	levels.set(13,{
        action : [['perte_argent', perso.salaire]],
        text : ["Oh non ! Tu t'es fait volé 1 pizza . Tu as perdu "+perso.salaire+" €."
	],
        choices : [["Aller en haut", 12]]
    });
	
	levels.set(14,{
        action : null,
        text : ['Après quelques mètres de progression, devant toi se trouve plusieurs chemins.',
        " Que veux tu faire ?"],
        choices : [["Aller en haut", 9],
		["Aller à droite", 12],
		["Aller à gauche", 1]]
    });

    return levels;
}
/*fonction qui génere les niveaux à partir de la fonction génerate_levels */
function set_level(n){
    if (n==8){
        levels = generate_levels();
    }    
    
    if (levels.has(n)){
        
        level = levels.get(n);
        if (level.action != null){
            do_things(level.action);
        }
		
				/*Si on a visité toutes les maisons mettre le nv de fin*/
        if ((n!=101) && (maison[1]+maison[2]+maison[3]+maison[4]+maison[5] == 5)){
            set_level(101);
        }
		/*Si l'argent<0 mettre le nv de fin*/
        if ((n!=102) && (perso.argent<0)){
            set_level(102);
        }
		/*Si le temps<=0 mettre le nv de fin*/
        if ((n!=103) && (perso.temps<=0)){
            set_level(103);
        }
	
        fill_text(level.text);
        fill_choices(level.choices);
        document.getElementById("nom").innerText = perso.nom;
		document.getElementById("prenom").innerText = perso.prenom;
        document.getElementById("salaire").innerText = perso.salaire;
        document.getElementById("temps").innerText = perso.temps;
		document.getElementById("argent").innerText = perso.argent;
		document.getElementById("pizzaland").src = "pizzaland_"+n+".png";
		perso.temps -= 1;
		document.getElementById("maison_total").innerText = maison[1]+maison[2]+maison[3]+maison[4]+maison[5];  
		
    }
    else{
        document.getElementById("text").innerHTML = "<p>Unknown level</p>";
        document.getElementById("choices").replaceChildren();
        
    }
    
}
/*fonction qui créé les élements <p> pour ajouter les zones de texte pour les differents choix possibles   */
function fill_text(texts){

    let n = texts.length;
    let txt_zone = document.getElementById("text");
    txt_zone.replaceChildren();

    for(var i=0; i<n; i=i+1){
        let new_p = txt_zone.appendChild(document.createElement("p"));
        new_p.innerText = texts[i];
    }
};
/*fonction qui créé des bouttons à partir du texte a afficher selon les niveaux*/
function fill_choices(choices){
    let n = choices.length;
    let choices_zone = document.getElementById("choices");
    choices_zone.replaceChildren();
    for(var i=0; i<n; i=i+1){
        let new_p = choices_zone.appendChild(document.createElement("p"));
        let new_b = new_p.appendChild(document.createElement("button"));
        new_b.innerText = choices[i][0];
        new_b.id="tolevel_"+choices[i][1];
        let target=choices[i][1];
        
        new_b.onclick = () => {

            set_level(target);};
    }

};
/*fonction pour le calcul des differents caracteristiques du personnage au fils du temps*/
function do_things(todo){

    for (var i =0; i<todo.length; i=i+1){
        switch (todo[i][0]){
            case "perte_argent": /* si dans " action " perte_argent apparait l'argent du joueur diminue de i qui depend du niveau auquel le joueur se trouve */
                perso.argent -= todo[i][1]; 
                break;
            case "gain_argent" :
                perso.argent += todo[i][1];
                break;
            case "perte_temps" :
                perso.temps -= todo[i][1];
                break;
            case "gain_temps" :
                perso.temps += todo[i][1];
                break;
			case "visite_maison" :
				visite_maison(todo[i][1]);
				break;
			case "reset" :
				reset_game();
				maison[1] = 0;
				maison[2] = 0;
				maison[3] = 0;
				maison[4] = 0;
				maison[5] = 0;
				perso.argent = 0;
				break;/*cache_info et montre_info servent a afficher ou non les infos sur le joueur , elle sont masquées lors de la mort par exemple*/
			case "cache_info" :
				cache_info();
				break;
			case "montre_info" :
				montre_info();
				break;
        }
        
        
    }

}


/*fonction pour la livraison des pizzas */
function livraison(i){
	if (maison[i] == 0){
		return ["Tu as livré une pizza, tu as eu "+perso.salaire+"€.",
			" Tu continue ton chemin.",
			" Que veux tu faire ?"];
	} else {
		return ["Tu as déjà livré une pizza dans cette maison.",
		" Tu continue ton chemin.",
		" Que veux tu faire ?"];
	}
}

/*fonction qui indique si on à deja livré une pizza */
function visite_maison(i){
	
	
	if (maison[i] == 0){
		maison[i] = 1;
		perso.argent += perso.salaire;
		
		
	}else{
		levels.get(niveau[i]).text=livraison(i);
		maison[i]  = 1;
	}
	
	
	
}
	
/*fonction pour le reinitialisement du jeux */
function reset_game(){
    document.getElementById("bienvenue").style.display = 'block';
    document.getElementById("jeu").style.display = 'none';
	document.getElementById("Easter_egg").style.display = 'none';

}

/*fonctions qui masquent ou affichent la zone contenant les information sur le personnage*/
function cache_info(){
    document.getElementById("perso").style.display = 'none';
    document.getElementById("map").style.display = 'none';

}
function montre_info(){
    document.getElementById("perso").style.display = 'block';
    document.getElementById("map").style.display = 'block';

}
/*Easter_egg : petit  Rickroll   */
let texte = document.querySelector('p1');
texte.addEventListener('click',easter_egg);

function easter_egg(){
	document.getElementById("bienvenue").style.display = 'none';
    document.getElementById("jeu").style.display = 'none';
	document.getElementById("Easter_egg").style.display = 'block';
}

/*Titouan Moquet / Erwann Piocelle-Morand /          */