const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

function showMessage(element, message, isError = false) {
    if (!element) {
        return;
    }

    element.textContent = message;
    element.style.color = isError ? "#c62828" : "#2e7d32";
}

function getErrorMessage(data) {
    if (data.detail) {
        return data.detail;
    }

    if (data.errors) {
        for (const field in data.errors) {
            if (data.errors[field] && data.errors[field].length > 0) {
                return data.errors[field][0];
            }
        }
    }

    return "Something went wrong.";
}

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("loginMessage");

        showMessage(message, "Logging in...");

        try {
            const response = await fetch("/api/user/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage(message, getErrorMessage(data), true);
                return;
            }

            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            localStorage.setItem("user", JSON.stringify(data.user));

            showMessage(message, data.message || "Login successful.");
        } catch (error) {
            showMessage(message, "Server connection error.", true);
        }
    });
}

if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const message = document.getElementById("registerMessage");

        showMessage(message, "Registering...");

        try {
            const response = await fetch("/api/user/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                showMessage(message, getErrorMessage(data), true);
                return;
            }

            showMessage(message, data.message || "User created successfully.");
            registerForm.reset();
        } catch (error) {
            showMessage(message, "Server connection error.", true);
        }
    });
}
