document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
  }

  // بدء البولينج لجلب حالات الأجهزة
  startPolling();
});

// دالة البولينج
function startPolling() {
  const pollInterval = 5000; // كل 5 ثوانٍ
  setInterval(() => {
    fetchDeviceStatus();
  }, pollInterval);
  fetchDeviceStatus(); // جلب الحالة فورًا عند التحميل
}

// جلب حالات الأجهزة من الخادم
function fetchDeviceStatus() {
  sendRequest("/api/device-status", "GET")
    .then((data) => {
      updateUI(data);
    })
    .catch((error) => console.error("Error fetching device status:", error));
}

// تحديث واجهة المستخدم بناءً على البيانات
function updateUI(data) {
  // تحديث الأضواء
  updateLightUI("living room", data["living room"].light);
  updateLightUI("kitchen", data["kitchen"].light);
  updateLightUI("garden", data["garden"].light);

  // تحديث المراوح
  updateFanUI("living room", data["living room"].fan);
  updateFanUI("kitchen", data["kitchen"].fan);
}

function updateLightUI(room, state) {
  const normalizedRoom = room === "living room" ? "livingroom" : room;
  const checkbox = document.getElementById(`${normalizedRoom}Light`);
  const normalizedState = state.toUpperCase();
  if (checkbox) {
    checkbox.checked = normalizedState === "ON";
    updateTable(room, "Light", normalizedState);
  }
}

function updateFanUI(room, speed) {
  const normalizedRoom = room === "living room" ? "livingroom" : room;
  const checkbox = document.getElementById(`${normalizedRoom}Fan`);
  const speedSlider = document.getElementById(`${normalizedRoom}Speed`);
  const speedValue = speedSlider.nextElementSibling;
  if (checkbox && speedSlider && speedValue) {
    const isOn = speed !== "0";
    checkbox.checked = isOn;
    speedSlider.value = speed;
    speedValue.textContent = speed;
    speedSlider.disabled = !isOn;
    speedSlider.title = isOn ? "" : "Turn on the fan to adjust speed";
    updateTable(room, "Fan", isOn ? "ON" : "OFF");
    updateTable1(room, "Fan", speed);
  }
}

// دوال فتح وإغلاق النماذج
function openLivingRoomModal() {
  document.getElementById("LivingRoomModal").style.display = "block";
  document.getElementById("KitchenModal").style.display = "none";
  document.getElementById("GardenModal").style.display = "none";
  document.getElementById("deviceModal").style.display = "none";
}

function closeLivingRoomModal() {
  document.getElementById("LivingRoomModal").style.display = "none";
}

function openKitchenModal() {
  document.getElementById("KitchenModal").style.display = "block";
  document.getElementById("LivingRoomModal").style.display = "none";
  document.getElementById("GardenModal").style.display = "none";
  document.getElementById("deviceModal").style.display = "none";
}

function closeKitchenModal() {
  document.getElementById("KitchenModal").style.display = "none";
}

function openGardenModal() {
  document.getElementById("GardenModal").style.display = "block";
  document.getElementById("KitchenModal").style.display = "none";
  document.getElementById("LivingRoomModal").style.display = "none";
  document.getElementById("deviceModal").style.display = "none";
}

function closeGardenModal() {
  document.getElementById("GardenModal").style.display = "none";
}

function open4Modal() {
  document.getElementById("deviceModal").style.display = "block";
  document.getElementById("KitchenModal").style.display = "none";
  document.getElementById("LivingRoomModal").style.display = "none";
  document.getElementById("GardenModal").style.display = "none";
}

function close4Modal() {
  document.getElementById("deviceModal").style.display = "none";
}

// تحديث الجداول
function updateTable(room, device, state) {
  const normalizedRoom = room === "living room" ? "livingroom" : room;
  const cellId = `${normalizedRoom}${device}State`;
  const cell = document.getElementById(cellId);
  if (cell) {
    cell.textContent = state.toUpperCase();
  } else {
    console.error(`Cell with ID '${cellId}' not found`);
  }
}

function updateTable1(room, device, speed) {
  const normalizedRoom = room === "living room" ? "livingroom" : room;
  const cellId = `${normalizedRoom}${device}Value`;
  const cell = document.getElementById(cellId);
  if (cell) {
    cell.textContent = speed;
  } else {
    console.error(`Cell with ID '${cellId}' not found`);
  }
}

// إعداد أحداث السلايدر
document.addEventListener("DOMContentLoaded", () => {
  const livingroomSpeed = document.getElementById("livingroomSpeed");
  const livingroomSpeedValue = livingroomSpeed.nextElementSibling;
  const livingroomFanCheckbox = document.getElementById("livingroomFan");

  const kitchenSpeed = document.getElementById("kitchenSpeed");
  const kitchenSpeedValue = kitchenSpeed.nextElementSibling;
  const kitchenFanCheckbox = document.getElementById("kitchenFan");

  function updateSliderState() {
    livingroomSpeed.disabled = !livingroomFanCheckbox.checked;
    kitchenSpeed.disabled = !kitchenFanCheckbox.checked;
    livingroomSpeed.title = livingroomSpeed.disabled ? "Turn on the fan to adjust speed" : "";
    kitchenSpeed.title = kitchenSpeed.disabled ? "Turn on the fan to adjust speed" : "";
  }

  updateSliderState();
  livingroomFanCheckbox.addEventListener("change", updateSliderState);
  kitchenFanCheckbox.addEventListener("change", updateSliderState);

  livingroomSpeed.addEventListener("input", () => {
    livingroomSpeedValue.textContent = livingroomSpeed.value;
  });

  kitchenSpeed.addEventListener("input", () => {
    kitchenSpeedValue.textContent = kitchenSpeed.value;
  });
});

// دالة إرسال الطلبات
function sendRequest(url, method, body = {}) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return Promise.reject("no token");
  }

  return fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: method !== "GET" ? JSON.stringify(body) : undefined,
  }).then((response) => {
    if (response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token");
      window.location.href = "/";
      return Promise.reject("token expired");
    }
    return response.json();
  });
}

// التحكم بالأضواء
function toggleLight(room) {
  const normalizedRoom = room === "livingroom" ? "living room" : room;
  const checkbox = document.getElementById(`${room}Light`);
  const state = checkbox.checked ? "ON" : "OFF";

  sendRequest("/api/lights", "POST", { room: normalizedRoom, state })
    .then((data) => {
      console.log(data.message);
      checkbox.checked = data.state.toUpperCase() === "ON";
      updateTable(normalizedRoom, "Light", data.state);
    })
    .catch((error) => console.error("Error:", error));
}

// التحكم بالمراوح
function toggleFan(room) {
  const normalizedRoom = room === "livingroom" ? "living room" : room;
  const checkbox = document.getElementById(`${room}Fan`);
  if (!checkbox) {
    console.error("element not found");
    return;
  }
  const state = checkbox.checked ? "255" : "0";

  sendRequest("/api/fans/state", "POST", { room: normalizedRoom, state })
    .then((data) => {
      const uiRoom = normalizedRoom === "living room" ? "livingroom" : normalizedRoom;
      console.log(data.message);
      checkbox.checked = data.state === "255";
      updateTable(normalizedRoom, "Fan", data.state === "255" ? "ON" : "OFF");
      if (data.state === "0") {
        document.getElementById(`${uiRoom}Speed`).value = 0;
        document.getElementById(`${uiRoom}Speed`).nextElementSibling.textContent = "0";
        updateTable1(normalizedRoom, "Fan", "0");
      } else {
        document.getElementById(`${uiRoom}Speed`).value = 255;
        document.getElementById(`${uiRoom}Speed`).nextElementSibling.textContent = "255";
        updateTable1(normalizedRoom, "Fan", "255");
      }
    })
    .catch((error) => console.error("Error:", error));
}

// التحكم بسرعة المراوح
function adjustFanSpeed(room, speed) {
  const normalizedRoom = room === "livingroom" ? "living room" : room;
  sendRequest("/api/fans/speed", "POST", { room: normalizedRoom, speed })
    .then((data) => {
      console.log(data.message);
      const uiRoom = normalizedRoom === "living room" ? "livingroom" : normalizedRoom;
      document.getElementById(`${uiRoom}Speed`).value = data.speed;
      document.getElementById(`${uiRoom}Speed`).nextElementSibling.textContent = data.speed;
      updateTable1(normalizedRoom, "Fan", data.speed);
    })
    .catch((error) => console.error("Error:", error));
}

async function navigateWithAuth(route) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Session expired. Please log in again.");
    window.location.href = "/";
    return;
  }
  let HtmlResponse = await fetch(route, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
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
  document.write(pageHtml);
  document.close();
}

// العودة إلى لوحة التحكم
async function Return() {
  await navigateWithAuth("/dashboard");
}