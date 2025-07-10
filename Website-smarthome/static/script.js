// Ensure the user is logged in when the page loads
document.addEventListener("DOMContentLoaded", function () {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/"; // Redirect to login page
  }

  // Sidebar functionality
  const menuBtn = document.getElementById("menu-btn");
  const closeBtn = document.getElementById("close-btn");
  const sidebar = document.querySelector(".sidebar");
  const overlay = document.querySelector(".menu-overlay");

  // Show the sidebar
  menuBtn.addEventListener("click", () => {
    sidebar.classList.add("visible");
    overlay.classList.add("visible");
  });

  // Hide the sidebar
  closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("visible");
    overlay.classList.remove("visible");
  });

  // Hide the sidebar when clicking on the overlay
  overlay.addEventListener("click", () => {
    sidebar.classList.remove("visible");
    overlay.classList.remove("visible");
  });
});

// Sign out functionality
document.addEventListener("DOMContentLoaded", function () {
  const signOutBtn = document.getElementById("signOutBtn");
  const confirmModal = document.getElementById("confirmModal");
  const confirmYes = document.getElementById("confirmYes");
  const confirmNo = document.getElementById("confirmNo");

  signOutBtn.addEventListener("click", function () {
    confirmModal.style.display = "block"; // Show the modal
  });

  confirmYes.addEventListener("click", function () {
    localStorage.removeItem("token"); // Remove the token
    window.location.href = "/"; // Redirect to login page
  });

  confirmNo.addEventListener("click", function () {
    confirmModal.style.display = "none"; // Close the modal
  });
});

// Centralized function to validate token and navigate
async function navigateWithAuth(route) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
  // Fetch the dashboard page with the token
  let HtmlResponse = await fetch(route, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  if (HtmlResponse.status === 401) {
    alert("Session expired. Please log in again.");
    localStorage.removeItem("token");
    window.location.href = "/";
    return;
  }
  if (!HtmlResponse.ok) {
    throw new Error("Failed to load dashboard");
  }

  let pageHtml = await HtmlResponse.text();
  document.open();
  document.write(pageHtml); // Render the dashboard page
  document.close();
}

// Navigation functions
async function goToControl() {
  await navigateWithAuth("/control");
}

async function goToUpload() {
  await navigateWithAuth("/upload");
}

async function goToMonitor() {
  await navigateWithAuth("/monitor");
}
async function goToWarning() {
  await navigateWithAuth("/warning");
}
async function goToRegister() {
  await navigateWithAuth("/register");
}

