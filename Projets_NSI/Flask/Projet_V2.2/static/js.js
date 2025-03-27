
// changement display si table vide 

document.addEventListener("DOMContentLoaded", function () {
    function checkResults() {
        let resultTable = document.querySelector("#resultats table tbody");

        // Vérifie si la table existe avant de continuer
        if (!resultTable) {
            console.log("Aucun tableau de résultats trouvé.");
            return;
        }

        let resultRows = resultTable.querySelectorAll("tr");

        if (resultRows.length > 1) {
            document.getElementById("resultats").style.display = "table-cell";
        } else {
            document.getElementById("resultats").style.display = "none";
        }
    }

    checkResults();
});

// fait en grande partie avec chat gpt :( ,car je n'y arrivais pas 





document.addEventListener("DOMContentLoaded", function () {
    let totalResultsElement = document.getElementById("totalResults");
    let currentLimitElement = document.getElementById("currentLimit");
    let loadMoreBtn = document.getElementById("loadMoreBtn");

    // Vérifie si les éléments existent avant de les utiliser
    if (!totalResultsElement || !currentLimitElement || !loadMoreBtn) {
        console.log("Aucun résultat trouvé, le script est arrêté.");
        return; // Arrête le script ici si pas de résultats
    }

    let totalResults = parseInt(totalResultsElement.dataset.total, 10);
    let currentLimit = parseInt(currentLimitElement.dataset.limit, 10);


    function updateVisibility() {
        if (currentLimit >= totalResults) {
            loadMoreBtn.style.display = "none";
        } else {
            loadMoreBtn.style.display = "block";
        }
    }

    loadMoreBtn.addEventListener("click", function () {
        currentLimit += 10;
        currentLimitElement.dataset.limit = currentLimit;

        let rows = document.querySelectorAll("#resultats tbody tr");
        for (let i = 0; i < rows.length; i++) {
            if (i < currentLimit) {
                rows[i].style.display = "table-row";
            }
        }

        updateVisibility();
    });

    let rows = document.querySelectorAll("#resultats tbody tr");
    rows.forEach((row, index) => {
        if (index >= currentLimit) {
            row.style.display = "none";
        }
    });

    updateVisibility();
    
    console.log("Total Results:", totalResults);
    console.log("Current Limit:", currentLimit);

});
