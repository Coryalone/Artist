let columnHeights = [0, 0, 0];

function lazyLoaded(event) {
    const image = event.target.parentElement;
    let minColumn = columnHeights
            .reduce((acc, cur, index) => {
                return cur < acc.height ? {index, height:cur} : acc
            }, {index:-1, height: Infinity})
            .index;
    const imageGallery = document.querySelectorAll('.gallery');
    imageGallery[minColumn].append(image);
    columnHeights[minColumn] += image.clientHeight;
    image.classList.add('emerge');
    checkPhotosToEmerge();
}

function intitializeLazyLoading() {
    const lazyloadImages = document.querySelectorAll('.lazy');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    const image = entry.target;
                    image.src = image.dataset.src;
                    image.removeAttribute('data-src');
                    image.classList.remove('lazy');
                    imageObserver.unobserve(image);
                    image.addEventListener('load', lazyLoaded);
                }
            });
        });

        lazyloadImages.forEach(function (image) {
            imageObserver.observe(image);
        });
    } else {
        function lazyload() {
            const scrollTop = window.pageYOffset;
            lazyloadImages.forEach(function (img) {
                const isLowEnough = img.offsetTop < window.innerHeight + scrollTop;
                const notAlreadyReplaced = img.classList.contains('lazy');
                if (isLowEnough && notAlreadyReplaced) {
                    console.log(1);
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.classList.remove('lazy');
                    img.addEventListener('load', lazyLoaded);
                }
            });
            if (lazyloadImages.length == 0) {
                document.removeEventListener('scroll', lazyload);
                window.removeEventListener('resize', lazyload);
                window.removeEventListener('orientationChange', lazyload);
            }
        }

        document.addEventListener('scroll', lazyload);
        window.addEventListener('resize', lazyload);
        window.addEventListener('orientationChange', lazyload);

        lazyload();
    }
}

function checkPhotosToEmerge(event) {
    document.querySelectorAll('.emerge').forEach(function (img) {
        const rect = img.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            setTimeout(() => {
                img.style.opacity = 1;
                img.style.transform = 'translateY(0)';
                img.classList.remove('emerge');
            }, Math.random() * 3000);
        }
    })
}

function initializeMergeUp() {

    document.addEventListener('scroll', checkPhotosToEmerge);
    window.addEventListener('resize', checkPhotosToEmerge);
    window.addEventListener('orientationChange', checkPhotosToEmerge);

    checkPhotosToEmerge();
}

initializeMergeUp()