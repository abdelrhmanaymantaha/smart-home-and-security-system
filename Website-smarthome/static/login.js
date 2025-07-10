document.addEventListener("DOMContentLoaded", function () {
  let loginForm = document.getElementById("login-form");
  let errorMessage = document.getElementById("error-message");

  if (!loginForm) {
    console.error("Login form not found!");
    return;
  }

  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent page reload

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    // Clear previous errors
    if (errorMessage) errorMessage.style.display = "none";

    // Validate inputs
    if (!username || !password) {
      if (errorMessage) {
        errorMessage.textContent = "Please enter both username and password";
        errorMessage.style.display = "block";
      }
      return;
    }
    try {
      let response = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
      });
  
      let data = await response.json();
      console.log("Login Response:", data);
  
      if (!response.ok || !data.success) {
          throw new Error(data.message || "Login failed");
      }
  
      if (!data.token) {
          throw new Error("No token received from server");
      }
  
      // Store token in localStorage
      localStorage.setItem("token", data.token);
      console.log("Stored Token:", localStorage.getItem("token"));
  
      // Fetch the dashboard page with the token
      let dashboardResponse = await fetch("/dashboard", {
          method: "GET",
          headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${data.token}`,
          },
      });
  
      if (!dashboardResponse.ok) {
          throw new Error("Failed to load dashboard");
      }
  
      let dashboardHtml = await dashboardResponse.text();
      document.open();
      document.write(dashboardHtml); // Render the dashboard page
      document.close();
  
  } catch (error) {
      if (errorMessage) {
          errorMessage.textContent = error.message;
          errorMessage.style.display = "block";
      }
  }
  
  });
});
