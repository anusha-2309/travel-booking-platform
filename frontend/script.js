let token = localStorage.getItem("token") || "";

/* =========================
   SIMPLE ALERT FUNCTION
========================= */
function showMessage(msg, success = true) {
    alert(msg); // (Later we can replace with toast notification)
}

/* =========================
   REGISTER
========================= */
async function register() {
    const res = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("reg-name").value,
            email: document.getElementById("reg-email").value,
            password: document.getElementById("reg-password").value
        })
    });

    const data = await res.json();
    showMessage(data.message || data.error);
}

/* =========================
   LOGIN
========================= */
async function login() {
    const res = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("login-email").value,
            password: document.getElementById("login-password").value
        })
    });

    const data = await res.json();

    if (data.access_token) {
        token = data.access_token;
        localStorage.setItem("token", token);
        showMessage("Login successful 🚀");
    } else {
        showMessage(data.error || "Login failed", false);
    }
}

/* =========================
   LOGOUT
========================= */
function logout() {
    localStorage.removeItem("token");
    token = "";
    showMessage("Logged out successfully 👋");
}

/* =========================
   LOAD PACKAGES (CARD VIEW)
========================= */
async function getPackages() {
    const res = await fetch("http://localhost:5000/packages");
    const data = await res.json();

    const container = document.getElementById("packages");
    container.innerHTML = "";

    data.forEach(pkg => {
        container.innerHTML += `
            <div class="package-card">
                <h3>${pkg.title}</h3>
                <p><strong>Destination:</strong> ${pkg.destination}</p>
                <p><strong>Duration:</strong> ${pkg.duration}</p>
                <p><strong>Price:</strong> ₹${pkg.price}</p>
                <button onclick="bookPackage('${pkg.id}')">
                    Book Now
                </button>
            </div>
        `;
    });
}

/* =========================
   BOOK PACKAGE
========================= */
async function bookPackage(id) {

    if (!token) {
        showMessage("Please login first ❗", false);
        return;
    }

    const res = await fetch("http://localhost:5000/book", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ package_id: id })
    });

    const data = await res.json();
    showMessage(data.message || data.error);
}

/* =========================
   GET MY BOOKINGS
========================= */
async function getBookings() {

    if (!token) {
        showMessage("Please login first ❗", false);
        return;
    }

    const res = await fetch("http://localhost:5000/my-bookings", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await res.json();

    const list = document.getElementById("bookings");
    list.innerHTML = "";

    data.forEach(pkg => {
        list.innerHTML += `
            <li>
                ${pkg.title} - ₹${pkg.price}
            </li>
        `;
    });
}