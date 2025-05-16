
// ... 


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



// fonction pour l'affichage responsif de la barre de navigation 

const burger = document.getElementById("burger");
const navLinks = document.querySelector(".link");

burger.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

// fonction pour masquer les tableaux si il est vide 

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
        currentLimit += 20;
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


// from https://www.w3schools.com
// back to top
let mybutton = document.getElementById("myBtn");

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// dispartion nav bar si scroll 
let lastScrollTop = 0;

const titleElement = document.querySelector(".nav_bar");

window.addEventListener("scroll", function() {
     let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

     if (scrollTop > lastScrollTop) {
        // scroll down -> hide title
         titleElement.classList.add("hidden");
     } else {
         // scroll up -> show title
         titleElement.classList.remove("hidden");
     }
     lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});


// Simulation d'un temps de chargement artificiel (0.5 secondes)
const loader = document.getElementById('loading-screen');


window.addEventListener('load', () => {
    setTimeout(() => {
       // document.getElementById('loading-screen').classList.add('hidden');
       if (loader) {
        loader.classList.add('hidden');}
        console.log("chargement");
        document.getElementById('main-content').style.display = 'block';
    }, 500); // 0.5 secondes
});

// systeme pour voir le mot de passe (pas très D.R.Y mais solution la plus simple trouvée)

const toggleIcon = document.getElementById("togglePassword");

if (toggleIcon) {
    toggleIcon.addEventListener("click", function () {
        const passwordInput = document.getElementById("password");
        if (!passwordInput) return;

        const isPassword = passwordInput.type === "password";
        passwordInput.type = isPassword ? "text" : "password";

        this.classList.toggle("fa-eye");
        this.classList.toggle("fa-eye-slash");
    });
}


document.querySelectorAll('.password-wrapper_2 i').forEach(function(toggleIcon) {
    toggleIcon.addEventListener('click', function () {
        const passwordInput = this.previousElementSibling;
        if (!passwordInput) return;

        const isPassword = passwordInput.type === 'password' || passwordInput.type === 'text';
        passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';

        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
});

document.querySelectorAll('.password-wrapper3 i').forEach(function(toggleIcon) {
    toggleIcon.addEventListener('click', function () {
        const passwordInput = this.previousElementSibling;
        if (!passwordInput) return;

        const isPassword = passwordInput.type === 'password' || passwordInput.type === 'text';
        passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';

        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
});



// fonction pour l'affichage des infos, par exemples : erreurs lors de connexion

document.addEventListener("DOMContentLoaded", function () {
    const statusContainer = document.querySelector('.statut_container');
    if (statusContainer) {
        // Affiche pendant 5 secondes
        setTimeout(() => {
            statusContainer.classList.add('hidden');
        }, 5000);
        
    }
});

