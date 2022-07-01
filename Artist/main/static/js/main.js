/* Footer Appear */

const footerNav = document.querySelector('.footer__items');

window.addEventListener('scroll', footerAppear);

function footerAppear() {
    if (window.scrollY >= 200) {
        footerNav.classList.add('footer__nav_visible');
    } else {
        footerNav.classList.remove('footer__nav_visible');
    }
}

/* Navigation Mobile */

const navItems = document.querySelectorAll('.header__item-mobile_active');
const navGroup = document.querySelector('.header__item-group-mobile');

navGroup.addEventListener('click', navItemsMobileAppear);

function navItemsMobileAppear() {
    navItems.forEach((i) => i.classList.toggle('header__item-mobile_hidden'));
}

/* Image Zoom */

mediumZoom('.gallery__item img');
