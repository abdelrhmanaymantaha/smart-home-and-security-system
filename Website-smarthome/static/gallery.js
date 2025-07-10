document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Session expired. Please log in again.");
      window.location.href = "/";
    }});
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
    if(HtmlResponse.status===401){
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return ;}
  
    if (!HtmlResponse.ok) {
      throw new Error("Failed to load dashboard");
    }
  
    let pageHtml = await HtmlResponse.text();
    document.open();
    document.write(pageHtml); // Render the dashboard page
    document.close();
  }
  
  // Navigation functions
 
  
  async function goToUpload() {
    await navigateWithAuth("/upload");
  }