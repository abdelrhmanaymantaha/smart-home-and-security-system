document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
});
async function fetchSensorData() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
  try {
    let response = await fetch("/sensor-data", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    if (response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return;
    }

    let data = await response.json();

    document.getElementById(
      "living-room-temp"
    ).innerHTML = `${data.livingRoom.temperature} °C`;
    document.getElementById(
      "living-room-humidity"
    ).innerHTML = `${data.livingRoom.humidity} %`;

    document.getElementById(
      "kitchen-temp"
    ).innerHTML = `${data.kitchen.temperature} °C`;
    document.getElementById(
      "kitchen-humidity"
    ).innerHTML = `${data.kitchen.humidity} %`;
    document.getElementById("kitchen-gas").innerHTML = data.kitchen.gas;

    document.getElementById(
      "garden-temp"
    ).innerHTML = `${data.garden.temperature} °C`;
    document.getElementById(
      "garden-humidity"
    ).innerHTML = `${data.garden.humidity} %`;
    document.getElementById("garden-soil").innerHTML = `${data.garden.soil} %`;
  } catch (error) {
    console.error("Error fetching sensor data:", error);
  }
}

// تحديث البيانات كل 5 ثوانٍ
setInterval(fetchSensorData, 5000);

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
async function Return() {
  await navigateWithAuth("/dashboard");
}