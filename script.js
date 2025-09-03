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

// Create image gallery
async function createImageGallery(images) {
    if (!images) return '';
    
    let galleryHtml = '';
    
    // Hero image
    if (images.hero && await imageExists(images.hero)) {
        galleryHtml += `
            <div class="project-hero-image">
                <img src="${images.hero}" alt="Project hero image" loading="lazy">
            </div>
        `;
    }
    
    // Demo image/gif
    if (images.demo && await imageExists(images.demo)) {
        galleryHtml += `
            <div class="project-demo">
                <img src="${images.demo}" alt="Project demo" loading="lazy">
            </div>
        `;
    }
    
    // Gallery images
    if (images.gallery && images.gallery.length > 0) {
        const galleryImages = [];
        for (const imgPath of images.gallery) {
            if (await imageExists(imgPath)) {
                galleryImages.push(imgPath);
            }
        }
        
        if (galleryImages.length > 0) {
            galleryHtml += `
                <div class="project-gallery">
                    <h5>Screenshots:</h5>
                    <div class="gallery-grid">
                        ${galleryImages.map(imgPath => `
                            <div class="gallery-item">
                                <img src="${imgPath}" alt="Project screenshot" loading="lazy" onclick="openModal('${imgPath}')">
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    return galleryHtml;
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

// Open image modal
function openModal(imageSrc) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <img src="${imageSrc}" alt="Full size image">
        </div>
    `;
    document.body.appendChild(modal);
    modal.style.display = 'flex';
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
        
        // GitHub link
        const githubLink = createSocialLink('github', data.github, 'GitHub');
        socialLinksElement.appendChild(githubLink);
        
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
        footerGithub.href = data.github;
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

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Add performance monitoring
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log(`Portfolio loaded in ${Math.round(loadTime)}ms`);
}); 