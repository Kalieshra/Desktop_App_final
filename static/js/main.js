document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle
    var toggleBtn = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.querySelector('.main-content');

    if (toggleBtn && sidebar && mainContent) {
        toggleBtn.addEventListener('click', function () {
            if (window.innerWidth <= 768) {
                sidebar.classList.toggle('show');
            } else {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('expanded');
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });
});
