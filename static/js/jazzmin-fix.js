// Corrige le décalage admin Jazzmin
// Jazzmin applique un margin-left dynamique après chargement
// Ce script le réinitialise après 500ms
window.addEventListener('load', function() {
    setTimeout(function() {
        var wrapper = document.querySelector('.content-wrapper');
        if (wrapper) {
            wrapper.style.marginLeft = '';
        }
    }, 500);
});