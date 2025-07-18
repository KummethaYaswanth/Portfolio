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
    dashboard: '📈',
    analyzer: '💬',
    predictor: '🌤️',
    default: '🚀'
};

// Get icon for project based on title keywords
function getProjectIcon(title) {
    const titleLower = title.toLowerCase();
    if (titleLower.includes('stock') || titleLower.includes('dashboard')) return icons.dashboard;
    if (titleLower.includes('text') || titleLower.includes('sentiment')) return icons.analyzer;
    if (titleLower.includes('weather') || titleLower.includes('predictor')) return icons.predictor;
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

// Create project card element
function createProjectCard(project) {
    const card = document.createElement('div');
    card.className = 'project-card';
    
    const icon = getProjectIcon(project.title);
    
    card.innerHTML = `
        <h3 class="project-title">
            <span>${icon}</span>
            ${project.title}
        </h3>
        <p class="project-description">${project.description}</p>
        <a href="${project.url}" target="_blank" rel="noopener noreferrer" class="project-link">
            <span>🚀</span>
            <span>View Project</span>
        </a>
    `;
    
    return card;
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
        
        data.projects.forEach(project => {
            const projectCard = createProjectCard(project);
            projectsGridElement.appendChild(projectCard);
        });
        
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

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close any open modals or overlays
        const overlay = document.querySelector('.loading-overlay');
        if (overlay && !overlay.classList.contains('hidden')) {
            overlay.classList.add('hidden');
        }
    }
});

// Add performance monitoring
window.addEventListener('load', () => {
    const loadTime = performance.now();
    console.log(`Portfolio loaded in ${Math.round(loadTime)}ms`);
}); 