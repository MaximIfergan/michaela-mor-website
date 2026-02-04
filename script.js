// ===== PAGE TRANSITION EFFECT =====
document.addEventListener('DOMContentLoaded', function() {
    // Add click listeners to all internal links
    const links = document.querySelectorAll('a[href^="index.html"], a[href^="gallery.html"], a[href^="about.html"], a[href^="contact.html"], a[href^="exhibition"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Only handle internal links
            if (href && !this.hasAttribute('target')) {
                e.preventDefault();

                // Add fade-out class
                document.body.classList.add('fade-out');

                // Navigate after fade
                setTimeout(() => {
                    window.location.href = href;
                }, 80);
            }
        });
    });
});

// ===== LIGHTBOX FUNCTIONALITY =====
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxTitle = document.getElementById('lightbox-title');
const lightboxInfo = document.getElementById('lightbox-info');
const lightboxClose = document.querySelector('.lightbox-close');

// Open lightbox when gallery item is clicked
const galleryItems = document.querySelectorAll('.gallery-item');
galleryItems.forEach(item => {
    item.addEventListener('click', function() {
        const img = this.querySelector('img');
        const title = this.getAttribute('data-title');
        const year = this.getAttribute('data-year');
        const medium = this.getAttribute('data-medium');

        lightbox.style.display = 'block';
        lightboxImg.src = img.src;
        lightboxTitle.textContent = title;
        lightboxInfo.textContent = `${year} | ${medium}`;

        // Prevent body scroll when lightbox is open
        document.body.style.overflow = 'hidden';
    });
});

// Close lightbox
if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
}

if (lightbox) {
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
}

function closeLightbox() {
    lightbox.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close lightbox with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && lightbox && lightbox.style.display === 'block') {
        closeLightbox();
    }
});

// ===== SMOOTH SCROLLING FOR INTERNAL LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
