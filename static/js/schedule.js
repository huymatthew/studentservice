// Global functions for template use
function editSchedule(scheduleId) {
    // Redirect to edit page or open edit modal
    window.location.href = `/schedule/edit/${scheduleId}/`;
}

function deleteSchedule(scheduleId, subjectId) {
    console.log(`Deleting schedule with ID: ${scheduleId} and subject ID: ${subjectId}`);
    if (confirm('Bạn có chắc chắn muốn xóa môn học này?')) {
        // Create form and submit
        const form = document.createElement('form');
        form.method = 'POST';
        // Ensure subjectId is included in the URL
        form.action = `/schedule/delete/${scheduleId}/${subjectId}/`;
        
        // Add CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);
        
        document.body.appendChild(form);
        form.submit();
    }
}

// Utility functions
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
// Global zoom state
let currentZoom = 100;
const minZoom = 50;
const maxZoom = 200;
const zoomStep = 10;
function adjustHeight(scheduleBlocks){
    const ruler = document.querySelector("#schedule-canvas > table > tbody > tr");
    console.log("Ruler height:", ruler ? ruler.offsetHeight : "Not found");
    scheduleBlocks.forEach(block => {
        const start = Number(block.dataset.startPeriod);
        const end = Number(block.dataset.endPeriod);
        const rulerHeight = ruler ? ruler.offsetHeight : 40;
        block.style.height = ((end - start + 1) * rulerHeight) + 'px';
        console.log(`Block ${block.dataset.scheduleId} height set to ${block.style.height}`);
    });
}
function updateZoomDisplay() {
    const zoomDisplay = document.querySelector('.zoom-level');
    if (zoomDisplay) {
        zoomDisplay.textContent = currentZoom + '%';
    }
}
function applyZoom(zoomLevel) {
    const canvasContent = document.getElementById('schedule-canvas');
    if (canvasContent) {
        const scale = zoomLevel / 100;
        canvasContent.style.transform = `scale(${scale})`;
        canvasContent.style.transformOrigin = 'top left';
        
        // Adjust container to prevent overflow
        const container = canvasContent.parentElement;
        if (container) {
            container.style.overflow = scale > 1 ? 'auto' : 'visible';
        }
    }
    
    // Re-adjust schedule block heights after zoom
    localStorage.setItem('scheduleZoomLevel', zoomLevel);
    setTimeout(() => {
        const scheduleBlocks = document.querySelectorAll('.schedule-block');
        adjustHeight(scheduleBlocks);
    }, 100);
}
function zoomIn() {
    if (currentZoom < maxZoom) {
        currentZoom = Math.min(currentZoom + zoomStep, maxZoom);
        applyZoom(currentZoom);
        updateZoomDisplay();
        
        // Update button states
        updateZoomButtons();
        
        // Show feedback
        showZoomFeedback('Phóng to', 'zoom-in');
    }
}
function zoomOut() {
    if (currentZoom > minZoom) {
        currentZoom = Math.max(currentZoom - zoomStep, minZoom);
        applyZoom(currentZoom);
        updateZoomDisplay();
        
        // Update button states
        updateZoomButtons();
        
        // Show feedback
        showZoomFeedback('Thu nhỏ', 'zoom-out');
    }
}
function resetZoom() {
    currentZoom = 100;
    applyZoom(currentZoom);
    updateZoomDisplay();
    updateZoomButtons();
    showZoomFeedback('Đặt lại zoom', 'search');
}
function updateZoomButtons() {
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    
    if (zoomInBtn) {
        zoomInBtn.disabled = currentZoom >= maxZoom;
        zoomInBtn.style.opacity = currentZoom >= maxZoom ? '0.5' : '1';
    }
    
    if (zoomOutBtn) {
        zoomOutBtn.disabled = currentZoom <= minZoom;
        zoomOutBtn.style.opacity = currentZoom <= minZoom ? '0.5' : '1';
    }
}
function showZoomFeedback(message, iconType) {
    // Remove existing feedback
    const existingFeedback = document.querySelector('.zoom-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    // Create feedback element
    const feedback = document.createElement('div');
    feedback.className = 'zoom-feedback';
    feedback.innerHTML = `
        <i class="fas fa-${iconType}"></i>
        <span>${message}: ${currentZoom}%</span>
    `;
    feedback.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        z-index: 9999;
        pointer-events: none;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: zoomFadeInOut 1.5s ease-in-out;
    `;
    
    document.body.appendChild(feedback);
    
    // Auto remove
    setTimeout(() => {
        if (feedback.parentNode) {
            feedback.remove();
        }
    }, 1500);
}
// Keyboard shortcuts
function handleKeyboardShortcuts(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === '=') {
        e.preventDefault();
        zoomIn();
    }
    
    if ((e.ctrlKey || e.metaKey) && e.key === '-') {
        e.preventDefault();
        zoomOut();
    }
    
    if ((e.ctrlKey || e.metaKey) && e.key === '0') {
        e.preventDefault();
        resetZoom();
    }
}
document.addEventListener('DOMContentLoaded', function() {
    // Initialize schedule blocks
    const scheduleBlocks = document.querySelectorAll('.schedule-block');
    adjustHeight(scheduleBlocks);
    
    // Zoom controls
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const zoomLevel = document.querySelector('.zoom-level');
    
    if (zoomInBtn) {
        zoomInBtn.addEventListener('click', zoomIn);
    }
    
    if (zoomOutBtn) {
        zoomOutBtn.addEventListener('click', zoomOut);
    }
    
    // Make zoom level clickable for reset
    if (zoomLevel) {
        zoomLevel.style.cursor = 'pointer';
        zoomLevel.title = 'Click để reset zoom (100%)';
        zoomLevel.addEventListener('click', resetZoom);
    }
    // Load saved zoom level
    const savedZoomLevel = localStorage.getItem('scheduleZoomLevel');
    if (savedZoomLevel) {
        currentZoom = parseInt(savedZoomLevel, 10);
        applyZoom(currentZoom);
    }
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Mouse wheel zoom (optional)
    const scheduleCanvas = document.getElementById('schedule-canvas');
    if (scheduleCanvas) {
        scheduleCanvas.addEventListener('wheel', function(e) {
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                if (e.deltaY < 0) {
                    zoomIn();
                } else {
                    zoomOut();
                }
            }
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        adjustHeight(scheduleBlocks);
    });
    
    // Initialize zoom display and buttons
    updateZoomDisplay();
    updateZoomButtons();
});