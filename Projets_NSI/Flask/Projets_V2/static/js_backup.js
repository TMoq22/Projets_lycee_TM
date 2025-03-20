



// changement display si table vide 
document.addEventListener("DOMContentLoaded", function () {
    function checkResults() {
        let resultTable = document.querySelector("#resultats table tbody");
        let resultRows = resultTable.querySelectorAll("tr");
        
        // Vérifie si au moins une ligne de résultat est présente
        if (resultRows.length > 1) {
            document.getElementById("resultats").style.display = "table-cell";
        } else {
            document.getElementById("resultats").style.display = "none";
        }
    }
    checkResults(); // Vérification au chargement de la page
});

// // conserver pour le debug  
// document.getElementById('maxItemsInput').addEventListener('input', function(event) {
//     const maxItems = event.target.value;
//     console.log("Nouvelle valeur max_items envoyée:", maxItems);  // Debug
//     fetch('/update_max_items', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ max_items: maxItems })  
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('msg serveur:', data);
//         location.reload();
//     })
//     .catch(error => {
//         console.error('Erreur AJAX:', error);
//     });
// });


// Boutons afficher plus 
document.getElementById('loadMoreBtn').addEventListener('click', function() {
    let currentMaxItems = parseInt(localStorage.getItem('max_items')) || 10; // Récupérer depuis localStorage (ou 10 par défaut)
    const newMaxItems = currentMaxItems + 20; // Ajouter 20 à chaque clic

    console.log("Nouvelle valeur max_items envoyée:", newMaxItems);  // Debug
    console.log("ancienne valeur max_items:", currentMaxItems);  // Debug

    fetch('/update_max_items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ max_items: newMaxItems })  
    })
    .then(response => response.json())
    .then(data => {
        console.log('msg serveur:', data);
        localStorage.setItem('max_items', newMaxItems); // Stocker en local pour conserver la valeur après rechargement
        location.reload();  // Recharger la page pour afficher plus de résultats
    })
    .catch(error => {
        console.error('Erreur AJAX:', error);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const totalResultsElement = document.getElementById('totalResults');
    
    // Vérifier si l'élément existe avant d'accéder à ses données
    if (totalResultsElement) {
        const totalResults = parseInt(totalResultsElement.dataset.total);
        console.log("Total Results:", totalResults);
        
        // Continue avec ton code si l'élément est trouvé
        const maxItems = parseInt(localStorage.getItem('max_items')) || 10;
        
        if (maxItems < totalResults) {
            document.getElementById('loadMoreBtn').style.display = 'block'; // Afficher le bouton si nécessaire
        }
    } else {
        console.error("L'élément 'totalResults' n'a pas été trouvé !");
    }
});



// // Réinitialiser max_items si on arrive sur une nouvelle page
// window.addEventListener("load", function() {
//     localStorage.removeItem("max_items");
// });

window.addEventListener('locationchange', function () {
    
	let max_items = parseInt(localStorage.getItem('max_items')) ; 
	
	if (max_items > 10){
		localStorage.setItem('max_items', 10 )
	};
    console.log("L'utilisateur quitte la page !");
    console.log("localStorage" ,localStorage);
});


/* window.addEventListener("beforeunload", function(event){
	
	
    //max_items = 10; 

}); */
