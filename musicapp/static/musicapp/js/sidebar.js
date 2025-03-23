function toggleSidebar() {
      const sidebar = document.querySelector('.sidebar');
      sidebar.classList.toggle('open');
  }

  // Close sidebar when clicked outside
  window.addEventListener('click', function (e) {
      const sidebar = document.querySelector('.sidebar');
      const toggleBtn = document.querySelector('.sidebar-toggle-btn');
      if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
          sidebar.classList.remove('open');
      }
  });

  // Close the sidebar when close button is clicked
  function closeSidebar() {
      document.querySelector('.sidebar').classList.remove('open');
  }