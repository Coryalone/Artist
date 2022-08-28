const imgURL = 'http://127.0.0.1:8000/api/category?n=2';
const imageGallery = document.querySelectorAll('.gallery');

function renderImage(imageURL, imageTitle, imageDescription) {
    const wrapper = document.createElement('div');
    wrapper.classList.add('gallery__item');

    const img = document.createElement('img');
    img.setAttribute('data-src', imageURL);
    img.alt = imageTitle;
    img.classList.add('lazy');

    const headerMobile = document.createElement('h2');
    headerMobile.classList.add('gallery_item-headline_mobile');
    headerMobile.textContent = imageTitle;

    const imgDetails = document.createElement('div');
    imgDetails.classList.add('gallery__item-details');

    const about = document.createElement('div');
    about.classList.add('gallery__item-info');

    const title = document.createElement('h2');
    title.classList.add('gallery__item-headline');
    if (imageTitle === '') {
        title.textContent = 'Картина';
        img.alt = 'Картина';
    } else {
        title.textContent = imageTitle;
    }

    const description = document.createElement('p');
    description.classList.add('gallery__item-description');
    description.textContent = imageDescription;

    if (imageTitle === '' && imageDescription === '') {
        imgDetails.remove();
        about.append(title, description);
        imgDetails.append(about);
        wrapper.append(img, headerMobile);
    } else {
        about.append(title, description);
        imgDetails.append(about);
        wrapper.append(img, headerMobile, imgDetails);
    }

    return [wrapper];
}

async function renderImagestoGallery() {
    const responce = await fetch(imgURL);
    const data = await responce.json();

    const images = [];

    data.forEach((image) => {
        const [elem] = renderImage(image.url_small, image.name, image.description);
        images.push(elem);
    });

    images.forEach((image, i) => {
        if (i % 3 === 0) {
            imageGallery[0].append(image);
        } else if (i % 3 === 1) {
            imageGallery[1].append(image);
        } else {
            imageGallery[2].append(image);
        }
    });

    intitializeLazyLoading();

    mediumZoom('.gallery__item img');

    const imagesRendered = document.querySelectorAll('.gallery__item img');

    imagesRendered.forEach((image) => {
        image.addEventListener('click', () => {
            const intersection = data.find((imgFromURL) => image.src === imgFromURL.url_small);
            if (intersection) {
                image.src = intersection.url_big;
            }
        });
    });
}

renderImagestoGallery();
