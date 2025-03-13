document.addEventListener('DOMContentLoaded', function() {
    animateElements();
    
    setupFeatureCards();
    
    setupAuthButtons();
});

function animateElements() {
    const elementsToAnimate = [
        document.querySelector('.welcome-text h1'),
        document.querySelector('.welcome-text h2'),
        document.querySelector('.welcome-text p'),
        document.querySelector('.feature-points'),
        document.querySelector('.auth-panel'),
        ...document.querySelectorAll('.feature-card')
    ];
    
    elementsToAnimate.forEach((element, index) => {
        if (element) {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            element.style.transitionDelay = `${index * 0.1}s`;
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100);
        }
    });
}

function setupFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach(card => {
        const icon = card.querySelector('.feature-icon');
        
        card.addEventListener('mouseenter', () => {
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
                icon.style.backgroundColor = 'rgba(47, 85, 79, 0.2)';
                icon.style.transition = 'all 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
                icon.style.backgroundColor = 'rgba(47, 85, 79, 0.1)';
            }
        });
    });
}

function setupAuthButtons() {
    const authButtons = document.querySelectorAll('.auth-button');
    
    authButtons.forEach(button => {
        button.addEventListener('mousedown', () => {
            button.style.transform = 'scale(0.97)';
        });
        
        button.addEventListener('mouseup', () => {
            button.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('focus', () => {
            button.style.boxShadow = '0 0 0 3px rgba(47, 85, 79, 0.3)';
        });
        
        button.addEventListener('blur', () => {
            button.style.boxShadow = 'none';
        });
    });
}

let lastScrollPosition = 0;

window.addEventListener('scroll', () => {
    const currentScrollPosition = window.pageYOffset;
    const backgroundOverlay = document.querySelector('.background-overlay');
    
    if (backgroundOverlay) {
        backgroundOverlay.style.transform = `translateY(${currentScrollPosition * 0.1}px)`;
    }
    
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        const speed = 0.03 + (index * 0.01);
        card.style.transform = `translateY(${(lastScrollPosition - currentScrollPosition) * speed}px)`;
    });
    
    lastScrollPosition = currentScrollPosition;
});