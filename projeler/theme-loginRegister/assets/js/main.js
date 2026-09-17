document.addEventListener("DOMContentLoaded", function () {

    const passwordButtons = document.querySelectorAll(".show-password");

    passwordButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const input = document.getElementById(button.getAttribute("data-target"));

            if (input.type === "password") {
                input.type = "text";
                button.textContent = "Gizle";
            } else {
                input.type = "password";
                button.textContent = "Göster";
            }
        });
    });

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = document.getElementById("loginEmail").value.trim();
            const password = document.getElementById("loginPassword").value.trim();
            const message = document.getElementById("loginMessage");

            if (email === "" || password === "") {
                message.textContent = "Lütfen e-posta ve şifre alanlarını doldurun.";
                return;
            }

            message.textContent = "Demo giriş başarılı. Gerçek sistem için backend bağlantısı gerekir.";
        });
    }

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const name = document.getElementById("registerName").value.trim();
            const email = document.getElementById("registerEmail").value.trim();
            const password = document.getElementById("registerPassword").value;
            const passwordAgain = document.getElementById("registerPasswordAgain").value;
            const terms = document.getElementById("terms").checked;
            const message = document.getElementById("registerMessage");

            if (name === "" || email === "" || password === "" || passwordAgain === "") {
                message.textContent = "Lütfen bütün alanları doldurun.";
                return;
            }

            if (password !== passwordAgain) {
                message.textContent = "Şifreler aynı değil.";
                return;
            }

            if (!terms) {
                message.textContent = "Devam etmek için şartları kabul etmelisiniz.";
                return;
            }

            message.textContent = "Demo kayıt başarılı. Backend bağlantısı eklenebilir.";
        });
    }

    const forgotPassword = document.getElementById("forgotPassword");

    if (forgotPassword) {
        forgotPassword.addEventListener("click", function (e) {
            e.preventDefault();
            alert("Şifre yenileme sayfası daha sonra eklenebilir.");
        });
    }
});
