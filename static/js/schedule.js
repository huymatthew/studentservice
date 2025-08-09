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

// Auto-adjust end period when start period changes
document.addEventListener('DOMContentLoaded', function() {
    const startPeriodSelect = document.getElementById('start_period');
    const endPeriodSelect = document.getElementById('end_period');
    
    if (startPeriodSelect && endPeriodSelect) {
        startPeriodSelect.addEventListener('change', function() {
            const startValue = parseInt(this.value);
            endPeriodSelect.value = startValue; // Default to same period
        });
    }
});
