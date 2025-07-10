document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
});

async function navigateWithAuth(route) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }

  try {
    const response = await fetch(route, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return;
    }
    if (!response.ok) {
      throw new Error("Failed to load page");
    }

    const pageHtml = await response.text();
    document.open();
    document.write(pageHtml);
    document.close();
  } catch (error) {
    console.error("Navigation Error:", error);
  }
}

async function Return() {
  await navigateWithAuth("/dashboard");
}

async function goToGallery(event) {
  event.preventDefault();
  const username = document.getElementById("gallery_username").value;
  if (!username) {
    alert("Please enter a username!");
    return;
  }
  await navigateWithAuth("/gallery/" + encodeURIComponent(username));
}

async function uploadImages(event) {
  event.preventDefault();
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }

  const form = event.target;
  const formData = new FormData(form);
  const submitButton = form.querySelector("button[type='submit']");
  submitButton.disabled = true;
  submitButton.textContent = "Uploading...";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });
    if (response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return;
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Upload failed");
    }

    const data = await response.text();
    alert(data); // الرسالة من الـ backend زي "Images saved successfully"
  } catch (error) {
    console.error("Upload Error:", error);
    alert("An error occurred: " + error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Upload Images";
  }
}

async function loadUserImage(username, filename) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }

  try {
    const response = await fetch(
      `/Uploads/${encodeURIComponent(username)}/${encodeURIComponent(
        filename
      )}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return;
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Failed to load image");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const img = document.createElement("img");
    img.src = url;

    // إضافة الصورة للصفحة
    const container = document.querySelector(".container") || document.body;
    container.appendChild(img);
  } catch (error) {
    console.error("Load User Image Error:", error);
    alert("Failed to load image: " + error.message);
  }
}

// ربط الأحداث
document
  .querySelector("form[action='/upload']")
  ?.addEventListener("submit", uploadImages);
document
  .querySelector("form[action='/gallery/']")
  ?.addEventListener("submit", goToGallery);
document.getElementById("return")?.addEventListener("click", Return);
