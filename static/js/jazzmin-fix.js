// Corrige le décalage admin Jazzmin — force margin-left à 250px
(function() {
    function fix() {
        var w = document.querySelector('.content-wrapper');
        if (w && w.style.marginLeft && w.style.marginLeft !== '250px') {
            w.style.setProperty('margin-left', '250px', 'important');
        }
    }
    // Surveiller les changements de style sur .content-wrapper
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(m) {
            if (m.attributeName === 'style') fix();
        });
    });
    var wrapper = document.querySelector('.content-wrapper');
    if (wrapper) {
        observer.observe(wrapper, { attributes: true, attributeFilter: ['style'] });
    } else {
        // Si pas encore chargé, attendre
        window.addEventListener('DOMContentLoaded', function() {
            var w = document.querySelector('.content-wrapper');
            if (w) observer.observe(w, { attributes: true, attributeFilter: ['style'] });
        });
    }
    // Appliquer immédiatement + après délais
    fix();
    setTimeout(fix, 100);
    setTimeout(fix, 500);
    setTimeout(fix, 1000);
    setTimeout(fix, 2000);
})();