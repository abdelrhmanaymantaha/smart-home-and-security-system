document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    Return;
  }
  document.querySelectorAll(".image-card").forEach((card, index) => {
    const imageId = card.dataset.imageId; // بنفترض إن image_id موجود في data-image-id
    if (imageId) {
      viewWarningImage(imageId, card.querySelector("img"));
    }
  });
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

async function viewWarningImage(imageId, imgElement) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }

  try {
    const response = await fetch(`/view_image/${imageId}`, {
      method: "GET",
      headers: {
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
      const errorText = await response.text();
      throw new Error(errorText || "Failed to load warning image");
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    imgElement.src = url;
  } catch (error) {
    console.error("View Warning Image Error:", error);
    imgElement.src = ""; // إزالة الصورة لو فشل التحميل
    imgElement.alt = "Failed to load image";
  }
}

// async function uploadWarningImage(event) {
//   event.preventDefault();
//   const token = localStorage.getItem("token");
//   if (!token || token.trim() === "") {
//     alert("Session expired. Please log in again.");
//     window.location.href = "/";
//     return;
//   }

//   const form = event.target;
//   const imageInput = form.querySelector("input[type='file']");
//   const submitButton = form.querySelector("button[type='submit']");
//   submitButton.disabled = true;
//   submitButton.textContent = "Uploading...";

//   try {
//     // قراءة الصورة وتحويلها لـ Base64
//     const file = imageInput.files[0];
//     if (!file) {
//       throw new Error("No image selected");
//     }
//     if (!file.type.startsWith("image/")) {
//       throw new Error("Please select an image file");
//     }

//     const reader = new FileReader();
//     const base64Promise = new Promise((resolve, reject) => {
//       reader.onload = () => resolve(reader.result.split(",")[1]); // إزالة الـ data:image/jpeg;base64,
//       reader.onerror = () => reject(new Error("Failed to read image"));
//       reader.readAsDataURL(file);
//     });

//     const base64Data = await base64Promise;

//     // إرسال الـ Base64 للـ backend
//     const response = await fetch("/upload_image", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         Authorization: `Bearer ${token}`,
//       },
//       body: JSON.stringify({ image_data: base64Data }),
//     });
//    if (response.status === 401) {
//   alert("Session expired. Please log in again.");
//   localStorage.removeItem("token");
//   window.location.href = "/";
//   return;
// }
//     if (!response.ok) {
//       const errorText = await response.text();
//       throw new Error(errorText || "Failed to upload warning image");
//     }

//     const data = await response.text();
//     alert(data); // مثلاً "Image uploaded successfully!"
//   } catch (error) {
//     console.error("Upload Warning Image Error:", error);
//     alert("An error occurred: " + error.message);
//   } finally {
//     submitButton.disabled = false;
//     submitButton.textContent = "Upload Warning Image";
//   }
// }
