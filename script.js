// DOM elements
const nameElement = document.getElementById('name');
const bioElement = document.getElementById('bio');
const socialLinksElement = document.getElementById('social-links');
const projectsGridElement = document.getElementById('projects-grid');
const avatarElement = document.getElementById('avatar');
const loadingOverlay = document.getElementById('loading-overlay');
const footerEmail = document.getElementById('footer-email');
const footerGithub = document.getElementById('footer-github');
const footerLinkedin = document.getElementById('footer-linkedin');

// Icons for social links and projects
const icons = {
    email: '✉️',
    phone: '📱',
    github: '🔗',
    linkedin: '💼',
    ml: '🤖',
    ai: '🧠',
    data: '📊',
    analytics: '📈',
    default: '🚀'
};

// Get icon for project based on title keywords
function getProjectIcon(title) {
    const titleLower = title.toLowerCase();
    if (titleLower.includes('ml') || titleLower.includes('machine learning')) return icons.ml;
    if (titleLower.includes('ai') || titleLower.includes('artificial intelligence')) return icons.ai;
    if (titleLower.includes('data') || titleLower.includes('analytics')) return icons.data;
    if (titleLower.includes('analysis') || titleLower.includes('dashboard')) return icons.analytics;
    return icons.default;
}

// Create avatar initials
function createAvatar(name) {
    const initials = name
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .join('');
    return initials;
}

// Create social link element
function createSocialLink(type, url, text) {
    const link = document.createElement('a');
    link.href = url;
    link.className = 'social-link';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    
    link.innerHTML = `
        <span>${icons[type]}</span>
        <span>${text}</span>
    `;
    
    return link;
}

// Check if image exists
async function imageExists(src) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = src;
    });
}

// Create adaptive image carousel
async function createImageGallery(images) {
    if (!images) return '';
    
    const allImages = [];
    
    // Collect all available images
    if (images.hero && await imageExists(images.hero)) {
        allImages.push({ src: images.hero, type: 'hero', alt: 'Project hero image' });
    }
    
    if (images.demo && await imageExists(images.demo)) {
        allImages.push({ src: images.demo, type: 'demo', alt: 'Project demo' });
    }
    
    if (images.gallery && images.gallery.length > 0) {
        for (const imgPath of images.gallery) {
            if (await imageExists(imgPath)) {
                allImages.push({ src: imgPath, type: 'gallery', alt: 'Project screenshot' });
            }
        }
    }
    
    // If we have images, create an adaptive carousel
    if (allImages.length > 0) {
        const carouselId = `carousel-${Math.random().toString(36).substr(2, 9)}`;
        
        return `
            <div class="project-image-carousel" id="${carouselId}">
                <div class="carousel-header">
                    <h5>Project Gallery (${allImages.length} images)</h5>
                    <div class="carousel-controls">
                        <button class="carousel-btn prev" onclick="prevImage('${carouselId}')" ${allImages.length <= 1 ? 'disabled' : ''}>‹</button>
                        <span class="carousel-counter">
                            <span class="current-image">1</span> / ${allImages.length}
                        </span>
                        <button class="carousel-btn next" onclick="nextImage('${carouselId}')" ${allImages.length <= 1 ? 'disabled' : ''}>›</button>
                    </div>
                </div>
                <div class="carousel-container">
                    <div class="carousel-track" style="transform: translateX(0%)">
                        ${allImages.map((img, index) => `
                            <div class="carousel-slide ${index === 0 ? 'active' : ''}" data-type="${img.type}">
                                <img src="${img.src}" alt="${img.alt}" loading="lazy" onclick="openCarouselModal('${carouselId}', ${index})">
                                <div class="image-type-badge">${img.type}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="carousel-thumbnails ${allImages.length <= 4 ? 'center-thumbnails' : ''}">
                    ${allImages.map((img, index) => `
                        <div class="thumbnail ${index === 0 ? 'active' : ''}" onclick="goToImage('${carouselId}', ${index})">
                            <img src="${img.src}" alt="${img.alt}">
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    return '';
}

// Create project card element
async function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    
    const icon = getProjectIcon(project.title);
    
    // Create technologies badges if available
    let technologiesHtml = '';
    if (project.technologies && project.technologies.length > 0) {
        technologiesHtml = `
            <div class="project-technologies">
                ${project.technologies.map(tech => `<span class="tech-badge">${tech}</span>`).join('')}
            </div>
        `;
    }
    
    // Create highlights if available
    let highlightsHtml = '';
    if (project.highlights && project.highlights.length > 0) {
        highlightsHtml = `
            <div class="project-highlights">
                <h4>Key Features:</h4>
                <ul>
                    ${project.highlights.map(highlight => `<li>${highlight}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Create image gallery
    const imageGalleryHtml = await createImageGallery(project.images);
    
    card.innerHTML = `
        <h3 class="project-title">
            <span>${icon}</span>
            ${project.title}
        </h3>
        <p class="project-description">${project.description}</p>
        ${technologiesHtml}
        ${imageGalleryHtml}
        ${highlightsHtml}
        <a href="${project.url}" target="_blank" rel="noopener noreferrer" class="project-link">
            <span>🚀</span>
            <span>Explore Project</span>
        </a>
    `;
    
    return card;
}

// Carousel navigation functions
function prevImage(carouselId) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const track = carousel.querySelector('.carousel-track');
    const slides = carousel.querySelectorAll('.carousel-slide');
    const thumbnails = carousel.querySelectorAll('.thumbnail');
    const currentImage = carousel.querySelector('.current-image');
    
    const activeSlide = carousel.querySelector('.carousel-slide.active');
    const activeIndex = Array.from(slides).indexOf(activeSlide);
    const prevIndex = activeIndex === 0 ? slides.length - 1 : activeIndex - 1;
    
    updateCarousel(carousel, prevIndex, slides, thumbnails, track, currentImage);
}

function nextImage(carouselId) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const track = carousel.querySelector('.carousel-track');
    const slides = carousel.querySelectorAll('.carousel-slide');
    const thumbnails = carousel.querySelectorAll('.thumbnail');
    const currentImage = carousel.querySelector('.current-image');
    
    const activeSlide = carousel.querySelector('.carousel-slide.active');
    const activeIndex = Array.from(slides).indexOf(activeSlide);
    const nextIndex = activeIndex === slides.length - 1 ? 0 : activeIndex + 1;
    
    updateCarousel(carousel, nextIndex, slides, thumbnails, track, currentImage);
}

function goToImage(carouselId, index) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const track = carousel.querySelector('.carousel-track');
    const slides = carousel.querySelectorAll('.carousel-slide');
    const thumbnails = carousel.querySelectorAll('.thumbnail');
    const currentImage = carousel.querySelector('.current-image');
    
    updateCarousel(carousel, index, slides, thumbnails, track, currentImage);
}

function updateCarousel(carousel, index, slides, thumbnails, track, currentImage) {
    // Update active slide
    slides.forEach(slide => slide.classList.remove('active'));
    slides[index].classList.add('active');
    
    // Update active thumbnail
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    thumbnails[index].classList.add('active');
    
    // Update track position
    const translateX = -index * 100;
    track.style.transform = `translateX(${translateX}%)`;
    
    // Update counter
    currentImage.textContent = index + 1;
}

// Open carousel modal
function openCarouselModal(carouselId, imageIndex) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    
    const slides = carousel.querySelectorAll('.carousel-slide');
    const images = Array.from(slides).map(slide => ({
        src: slide.querySelector('img').src,
        alt: slide.querySelector('img').alt,
        type: slide.dataset.type
    }));
    
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-counter">${imageIndex + 1} / ${images.length}</span>
                <span class="modal-close" onclick="closeModal()">&times;</span>
            </div>
            <div class="modal-carousel">
                <button class="modal-nav prev" onclick="modalPrevImage()" ${images.length <= 1 ? 'disabled' : ''}>‹</button>
                <div class="modal-image-container">
                    <img src="${images[imageIndex].src}" alt="${images[imageIndex].alt}" id="modal-image">
                    <div class="modal-image-type">${images[imageIndex].type}</div>
                </div>
                <button class="modal-nav next" onclick="modalNextImage()" ${images.length <= 1 ? 'disabled' : ''}>›</button>
            </div>
        </div>
    `;
    
    // Store images data for modal navigation
    modal.dataset.images = JSON.stringify(images);
    modal.dataset.currentIndex = imageIndex;
    
    document.body.appendChild(modal);
    modal.style.display = 'flex';
}

// Modal navigation
function modalPrevImage() {
    const modal = document.querySelector('.image-modal');
    if (!modal) return;
    
    const images = JSON.parse(modal.dataset.images);
    const currentIndex = parseInt(modal.dataset.currentIndex);
    const newIndex = currentIndex === 0 ? images.length - 1 : currentIndex - 1;
    
    updateModalImage(modal, images, newIndex);
}

function modalNextImage() {
    const modal = document.querySelector('.image-modal');
    if (!modal) return;
    
    const images = JSON.parse(modal.dataset.images);
    const currentIndex = parseInt(modal.dataset.currentIndex);
    const newIndex = currentIndex === images.length - 1 ? 0 : currentIndex + 1;
    
    updateModalImage(modal, images, newIndex);
}

function updateModalImage(modal, images, newIndex) {
    const img = modal.querySelector('#modal-image');
    const counter = modal.querySelector('.modal-counter');
    const typeLabel = modal.querySelector('.modal-image-type');
    
    img.src = images[newIndex].src;
    img.alt = images[newIndex].alt;
    counter.textContent = `${newIndex + 1} / ${images.length}`;
    typeLabel.textContent = images[newIndex].type;
    
    modal.dataset.currentIndex = newIndex;
}

// Close image modal
function closeModal() {
    const modal = document.querySelector('.image-modal');
    if (modal) {
        modal.remove();
    }
}

// Add loading animation
function addLoadingAnimation() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Load and populate portfolio data
async function loadPortfolioData() {
    try {
        const response = await fetch('config.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Populate header information
        nameElement.textContent = data.name;
        bioElement.textContent = data.bio;
        avatarElement.textContent = createAvatar(data.name);
        
        // Clear and populate social links
        socialLinksElement.innerHTML = '';
        
        // Email link
        const emailLink = createSocialLink('email', `mailto:${data.email}`, 'Email');
        socialLinksElement.appendChild(emailLink);
        
        // Phone link (if available)
        if (data.phone) {
            const phoneLink = createSocialLink('phone', `tel:${data.phone}`, 'Phone');
            socialLinksElement.appendChild(phoneLink);
        }
        
        // GitHub link (if available)
        if (data.github) {
            const githubLink = createSocialLink('github', data.github, 'GitHub');
            socialLinksElement.appendChild(githubLink);
        }
        
        // LinkedIn link
        const linkedinLink = createSocialLink('linkedin', data.linkedin, 'LinkedIn');
        socialLinksElement.appendChild(linkedinLink);
        
        // Clear and populate projects
        projectsGridElement.innerHTML = '';
        
        // Create project cards asynchronously
        for (const project of data.projects) {
            const projectCard = await createProjectCard(project);
            projectsGridElement.appendChild(projectCard);
        }
        
        // Update footer links
        footerEmail.href = `mailto:${data.email}`;
        if (data.github && footerGithub) {
            footerGithub.href = data.github;
        }
        footerLinkedin.href = data.linkedin;
        
        // Add loading animation to cards
        setTimeout(addLoadingAnimation, 100);
        
        // Hide loading overlay
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 800);
        
    } catch (error) {
        console.error('Error loading portfolio data:', error);
        
        // Show error message
        nameElement.textContent = 'Error Loading Portfolio';
        bioElement.textContent = 'Unable to load portfolio data. Please check the config.json file.';
        avatarElement.textContent = '⚠️';
        
        // Hide loading overlay
        setTimeout(() => {
            loadingOverlay.classList.add('hidden');
        }, 1000);
    }
}

// Smooth scrolling for internal links
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    }
});

// Add parallax effect to header
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const header = document.querySelector('.header');
    
    if (header) {
        const speed = scrolled * 0.5;
        header.style.transform = `translateY(${speed}px)`;
    }
});

// Initialize portfolio when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadPortfolioData();
});

// Enhanced keyboard navigation for modal and carousel
document.addEventListener('keydown', (e) => {
    const modal = document.querySelector('.image-modal');
    
    if (modal) {
        // Modal is open - handle modal navigation
        if (e.key === 'Escape') {
            closeModal();
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            modalPrevImage();
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            modalNextImage();
        }
    } else {
        // Modal is closed - handle carousel navigation if focused
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            const activeElement = document.activeElement;
            const carousel = activeElement.closest('.project-image-carousel');
            
            if (carousel) {
                e.preventDefault();
                const carouselId = carousel.id;
                
                if (e.key === 'ArrowLeft') {
                    prevImage(carouselId);
                } else {
                    nextImage(carouselId);
                }
            }
        }
    }
});

// Add performance monitoring
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log(`Portfolio loaded in ${Math.round(loadTime)}ms`);
}); 