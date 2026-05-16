
let searchForm = document.querySelector('.search-form');
let shoppingcart = document.querySelector('.shopping-cart');
let loginForm = document.querySelector('.login-form');
let navbar = document.querySelector('.navbar');

// Safe event bindings
const searchBtn = document.querySelector('#search-btn');
if (searchBtn) {
    searchBtn.onclick = () => {
        searchForm && searchForm.classList.toggle('active');
        shoppingcart && shoppingcart.classList.remove('active');
        loginForm && loginForm.classList.remove('active');
        navbar && navbar.classList.remove('active');
    };
}

const cartBtn = document.querySelector('#cart-btn');
if (cartBtn) {
    cartBtn.onclick = () => {
        shoppingcart && shoppingcart.classList.toggle('active');
        searchForm && searchForm.classList.remove('active');
        loginForm && loginForm.classList.remove('active');
        navbar && navbar.classList.remove('active');
    };
}

const loginBtn = document.querySelector('#login-btn');
if (loginBtn) {
    loginBtn.onclick = () => {
        loginForm && loginForm.classList.toggle('active');
        searchForm && searchForm.classList.remove('active');
        shoppingcart && shoppingcart.classList.remove('active');
        navbar && navbar.classList.remove('active');
    };
}

const menuBtn = document.querySelector('#menu-btn');
if (menuBtn) {
    menuBtn.onclick = () => {
        navbar && navbar.classList.toggle('active');
        searchForm && searchForm.classList.remove('active');
        shoppingcart && shoppingcart.classList.remove('active');
        loginForm && loginForm.classList.remove('active');
    };
}

window.onscroll = () => {
    searchForm && searchForm.classList.remove('active');
    shoppingcart && shoppingcart.classList.remove('active');
    loginForm && loginForm.classList.remove('active');
    navbar && navbar.classList.remove('active');
};

// Toggle order items visibility

document.querySelectorAll('.toggle-order').forEach(icon => {
    icon.addEventListener('click', function(){
        const itemsList = this.parentElement.nextElementSibling; // ul
        if(itemsList.style.display === 'none' || itemsList.style.display === ''){
            itemsList.style.display = 'block';
            this.classList.remove('fa-chevron-down');
            this.classList.add('fa-chevron-up');
        } else {
            itemsList.style.display = 'none';
            this.classList.remove('fa-chevron-up');
            this.classList.add('fa-chevron-down');
        }
    });
});


