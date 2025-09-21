document.addEventListener('DOMContentLoaded', () => {

    const products = [
        // --- iPhone 14 Series ---
        {
            id: 1, name: 'iPhone 14 Pro Max 128Go', price: 750, category: 'iPhone 14',
            image: 'images/iphone-14-pro-max.png',
            description: "Passez au Pro. Capturez des détails incroyables avec un appareil photo principal de 48 Mpx. Vivez une nouvelle expérience iPhone avec Dynamic Island et l'écran Toujours activé."
        },
        {
            id: 2, name: 'iPhone 14 128Go', price: 620, category: 'iPhone 14',
            image: 'images/iPhone 14 128Go Starlight.jpeg',
            description: "Un appareil photo avancé pour des photos plus belles par toute lumière. Un mode Cinématique désormais en 4K Dolby Vision. Une autonomie record. C'est grand."
        },
        
        // --- iPhone 13 Series ---
        {
            id: 3, name: 'iPhone 13 Pro 256Go', price: 580, category: 'iPhone 13',
            image: 'images/iphone-13-pro.png',
            description: "Une optimisation photo et vidéo phénoménale. La puce A15 Bionic, la plus rapide au monde sur smartphone. Un design robuste et la meilleure autonomie jamais vue sur iPhone."
        },
        {
            id: 4, name: 'iPhone 13 128Go', price: 380, category: 'iPhone 13',
            image: 'images/iphone-13.png',
            description: "Votre nouveau superpouvoir. Un double appareil photo plus avancé, une puce fulgurante qui distance la concurrence et une autonomie qui change la donne."
        },
        {
            id: 7, name: 'iPhone 13 mini 128Go', price: 320, category: 'iPhone 13',
            image: 'images/iphone-13-mini.png',
            description: "Le concentré de puissance de la série 13, dans un format ultra-compact. Idéal pour ceux qui préfèrent une utilisation à une main."
        },
        
        // --- iPhone 12 Series ---
        {
            id: 5, name: 'iPhone 12 Pro Max 256Go', price: 480, category: 'iPhone 12',
            image: 'images/iphone-12-pro-by-apple.jpg',
            description: "Un bond en avant spectaculaire. Le système photo Pro atteint des sommets de performances en conditions de faible éclairage, et la 5G ultra-rapide ouvre des possibilités inédites."
        },
        {
            id: 8, name: 'iPhone 12 128Go', price: 390, category: 'iPhone 12',
            image: 'images/iphone-12.png',
            description: "Le modèle standard de la série 12, avec une puce A14 Bionic ultra-rapide et la compatibilité 5G, offrant d'excellentes performances."
        },
        
        // --- iPhone 11 Series ---
        {
            id: 6, name: 'iPhone 11 128Go', price: 230, category: 'iPhone 11',
            image: 'images/11mini.png',
            description: "Juste ce qu'il faut de tout. Un double appareil photo pour élargir vos horizons. La puce la plus rapide jamais intégrée à un smartphone et une autonomie d'une journée."
        },
        {
            id: 9, name: 'iPhone 11 Pro 256Go', price: 280, category: 'iPhone 11',
            image: 'images/iphone-11-pro.png',
            description: "Un système à triple appareil photo pour des clichés professionnels, une puce A13 Bionic et une autonomie améliorée."
        },

        // --- iPhone X Series ---
        {
            id: 10, name: 'iPhone XR 128Go', price: 180, category: 'iPhone X',
            image: 'images/iphone-xr.png',
            description: "Un excellent rapport qualité-prix. Un écran Liquid Retina, la puce A12 Bionic et un appareil photo unique pour de superbes portraits."
        },
        {
            id: 11, name: 'iPhone X 64Go', price: 150, category: 'iPhone X',
            image: 'images/iphone-x.png',
            description: "Le modèle qui a révolutionné l'iPhone avec son écran bord à bord OLED et Face ID. Un design emblématique et toujours performant."
        }
    ];

    let cart = [];
    const phoneNumber = '+243845370370';
    const whatsappNumber = phoneNumber.replace('+', '');

    const productGrid = document.getElementById('product-grid');
    const productsTitle = document.getElementById('products-title');
    const navLinks = document.getElementById('nav-links');
    const footerLinks = document.getElementById('footer-links');
    const searchBar = document.getElementById('search-bar');
    const cartIcon = document.getElementById('cart-icon');
    const cartCount = document.getElementById('cart-count');
    const productModal = document.getElementById('product-detail-modal');
    const cartModal = document.getElementById('cart-modal');
    const closeModalButtons = document.querySelectorAll('.close-modal-btn');
    const modalProductContent = document.getElementById('modal-product-content');

    function showProductDetail(productId) {
        const product = products.find(p => p.id === productId);
        const whatsappMessage = `Bonjour, je suis intéressé(e) par le produit suivant : ${product.name} ($${product.price}).`;
        const whatsappLink = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;

        modalProductContent.innerHTML = `
            <div class="product-detail-layout">
                <div class="product-detail-image"><img src="${product.image}" alt="${product.name}"></div>
                <div class="product-detail-info">
                    <h2>${product.name}</h2>
                    <div class="price">$${product.price}</div>
                    <p>${product.description}</p>
                    <div class="detail-actions">
                         <a href="tel:${phoneNumber}" class="btn call-btn"><i class="fa-solid fa-phone"></i> Appeler</a>
                         <a href="${whatsappLink}" target="_blank" class="btn whatsapp-detail-btn"><i class="fab fa-whatsapp"></i> WhatsApp</a>
                         <button class="btn add-to-cart-btn" data-product-id="${product.id}"><i class="fa-solid fa-cart-plus"></i> Panier</button>
                    </div>
                </div>
            </div>`;
        openModal(productModal);
    }
    
    function setupNavigation() {
        const categories = ['Tous', ...new Set(products.map(p => p.category))];
        navLinks.innerHTML = ''; 
        footerLinks.innerHTML = '';
        categories.forEach(category => {
            const linkHTML = `<li><a href="#" class="nav-category-link" data-category="${category}">${category}</a></li>`;
            navLinks.innerHTML += linkHTML;
            if (category !== 'Tous') { 
                footerLinks.innerHTML += linkHTML; 
            }
        });
        document.querySelector('.nav-category-link[data-category="Tous"]').classList.add('active');
    }

    function renderProducts(productsToRender) {
        productGrid.innerHTML = '';
        if (productsToRender.length === 0) {
            productGrid.innerHTML = `<p class="cart-empty-message">Aucun produit ne correspond à votre recherche.</p>`; 
            return;
        }
        productsToRender.forEach(product => {
            productGrid.innerHTML += `
                <div class="product-card">
                    <img src="${product.image}" alt="${product.name}" class="product-image" data-product-id="${product.id}">
                    <h3>${product.name}</h3>
                    <div class="price">$${product.price}</div>
                    <div class="product-actions">
                        <button class="view-details-btn" data-product-id="${product.id}">Voir les détails</button>
                        <button class="add-to-cart-btn" data-product-id="${product.id}"><i class="fa-solid fa-cart-plus"></i> Ajouter au panier</button>
                    </div>
                </div>`;
        });
    }

    document.body.addEventListener('click', event => {
        const target = event.target;
        if (target.matches('.product-image') || target.matches('.view-details-btn')) {
            const productId = parseInt(target.dataset.productId);
            showProductDetail(productId);
        }
        if (target.closest('.add-to-cart-btn')) {
            const productId = parseInt(target.closest('.add-to-cart-btn').dataset.productId);
            cartFunctions.addToCart(productId);
            if(productModal.classList.contains('active')) closeModal();
        }
        if (target.matches('.nav-category-link')) {
            event.preventDefault();
            const category = target.dataset.category;
            
            // Logique pour masquer/afficher l'accueil
            const heroSection = document.querySelector('.hero');
            if (category !== 'Tous') {
                heroSection.classList.add('hidden');
            } else {
                heroSection.classList.remove('hidden');
            }

            document.querySelectorAll('.nav-category-link').forEach(link => link.classList.remove('active'));
            target.classList.add('active');
            if (category === 'Tous') {
                renderProducts(products); 
                productsTitle.textContent = "Tous nos modèles";
            } else {
                const filteredProducts = products.filter(p => p.category === category);
                renderProducts(filteredProducts); 
                productsTitle.textContent = `Série ${category}`;
            }
        }
    });

    searchBar.addEventListener('input', () => {
        const searchTerm = searchBar.value.toLowerCase();
        const filteredProducts = products.filter(p => p.name.toLowerCase().includes(searchTerm));
        renderProducts(filteredProducts);
        productsTitle.textContent = searchTerm ? `Résultats pour "${searchBar.value}"` : "Tous nos modèles";
    });
    
    let cartFunctions = {
        addToCart: function(productId) {
            const productToAdd = products.find(p => p.id === productId);
            if (productToAdd) { 
                cart.push(productToAdd); 
                this.updateCart(); 
            }
        },
        removeFromCart: function(productIndex) {
            cart.splice(productIndex, 1); 
            this.updateCart();
        },
        updateCart: function() {
            const cartItemsContainer = document.getElementById('cart-items-container');
            const cartTotalPriceEl = document.getElementById('cart-total-price');
            const orderWhatsAppBtn = document.getElementById('order-whatsapp-btn');
            cartCount.textContent = cart.length;
            if (cart.length === 0) {
                cartItemsContainer.innerHTML = '<p class="cart-empty-message">Votre panier est vide.</p>';
                orderWhatsAppBtn.disabled = true;
            } else {
                cartItemsContainer.innerHTML = cart.map((item, index) => `
                    <div class="cart-item">
                        <img src="${item.image}" alt="${item.name}" class="cart-item-img">
                        <div class="cart-item-info"><h4>${item.name}</h4><span class="cart-item-price">$${item.price}</span></div>
                        <button class="remove-from-cart-btn" data-item-index="${index}">&times;</button>
                    </div>`).join('');
                orderWhatsAppBtn.disabled = false;
            }
            const totalPrice = cart.reduce((total, item) => total + item.price, 0);
            cartTotalPriceEl.textContent = `$${totalPrice}`;
        },
        setupCartEventListeners: function() {
            document.body.addEventListener('click', event => {
                if (event.target.classList.contains('remove-from-cart-btn')) {
                    this.removeFromCart(parseInt(event.target.dataset.itemIndex));
                }
            });
            document.getElementById('order-whatsapp-btn').addEventListener('click', () => {
                if (cart.length === 0) return;
                const totalPrice = cart.reduce((total, item) => total + item.price, 0);
                let message = `Bonjour iPhone Store,\n\nJe souhaite commander les articles suivants :\n`;
                cart.forEach(item => { message += `\n- ${item.name} ($${item.price})`; });
                message += `\n\n*Total : $${totalPrice}*\\n\nMerci de m'indiquer la suite.`;
                window.open(`https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`, '_blank');
            });
        }
    };
    
    function openModal(modal) { 
        modal.classList.add('active'); 
    }
    
    function closeModal() {
        productModal.classList.remove('active');
        cartModal.classList.remove('active');
    }

    cartIcon.addEventListener('click', () => openModal(cartModal));
    closeModalButtons.forEach(btn => btn.addEventListener('click', closeModal));

    setupNavigation();
    renderProducts(products);
    cartFunctions.updateCart();
    cartFunctions.setupCartEventListeners();
});