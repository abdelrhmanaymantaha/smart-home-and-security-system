document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
});

document
  .getElementById("register-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // منع إعادة تحميل الصفحة

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("error-message");
    const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
    try {
      let response = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ username, password }),
      });
      if (response.status === 401) {
        alert("Session expired. Please log in again.");
        localStorage.removeItem("token");
        window.location.href = "/";
        return;
      }
      let data = await response.json();
      if (data.success) {
       localStorage.removeItem("token"); //remove token
        window.location.href = data.redirect; // login page
      } else {
        errorMessage.textContent = data.message;
        errorMessage.style.display = "block"; // عرض الخطأ
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });

document.getElementById("username").addEventListener("input", function () {
  document.getElementById("error-message").style.display = "none";
});
document.getElementById("password").addEventListener("input", function () {
  document.getElementById("error-message").style.display = "none";
});
document.getElementById("Back-to-login").addEventListener("click", function(event){
  event.preventDefault();
  localStorage.removeItem("token");
  window.location.href = "/";
})
