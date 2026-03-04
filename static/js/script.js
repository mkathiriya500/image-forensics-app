// Client-side interactions
document.addEventListener('DOMContentLoaded', function() {
    console.log('Image Forensics Tool loaded');
    
    // Add clipboard paste functionality
    document.addEventListener('paste', function(e) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const blob = items[i].getAsFile();
                const reader = new FileReader();
                reader.onload = function(event) {
                    // Trigger image upload
                    uploadImageFromClipboard(event.target.result);
                };
                reader.readAsDataURL(blob);
            }
        }
    });
});

function uploadImageFromClipboard(imageData) {
    // Send image data to Streamlit
    const event = new CustomEvent('clipboardImage', { detail: imageData });
    window.dispatchEvent(event);
}

// Add loading animation
function showLoading() {
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.remove();
    }
}

// Progress tracking
let progressInterval;
function startProgressTracking() {
    let progress = 0;
    progressInterval = setInterval(() => {
        progress += 5;
        if (progress <= 90) {
            updateProgress(progress);
        }
    }, 1000);
}

function stopProgressTracking() {
    clearInterval(progressInterval);
    updateProgress(100);
    setTimeout(() => {
        hideProgress();
    }, 500);
}

function updateProgress(value) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = value + '%';
        progressBar.setAttribute('aria-valuenow', value);
    }
}

function hideProgress() {
    const progressContainer = document.querySelector('.progress');
    if (progressContainer) {
        progressContainer.style.display = 'none';
    }
}

// Add tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-custom';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    tooltip.style.left = e.pageX + 'px';
    tooltip.style.top = (e.pageY - 30) + 'px';
    document.body.appendChild(tooltip);
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip-custom');
    if (tooltip) {
        tooltip.remove();
    }
}

// Image preview functionality
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image-preview');
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Export results
function exportResults(data, format = 'json') {
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analysis_results.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Share functionality
function shareResults(platform, data) {
    const shareUrls = {
        twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(data)}`,
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(data)}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(data)}`
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
    }
}