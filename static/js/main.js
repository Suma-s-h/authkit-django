/* AuthKit JS */
document.addEventListener('DOMContentLoaded', function () {

    // ── Auto-dismiss alerts after 5 s ─────────────────────────────────────
    setTimeout(function () {
        document.querySelectorAll('.alert.fade.show').forEach(function (el) {
            bootstrap.Alert.getOrCreateInstance(el).close();
        });
    }, 5000);

    // ── Password show / hide toggle ───────────────────────────────────────
    document.querySelectorAll('[data-toggle-password]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var target = document.querySelector(this.dataset.togglePassword);
            if (!target) return;
            var isPassword = target.type === 'password';
            target.type = isPassword ? 'text' : 'password';
            var icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('bi-eye', !isPassword);
                icon.classList.toggle('bi-eye-slash', isPassword);
            }
        });
    });

    // ── Password strength meter (register page) ───────────────────────────
    var pwInput = document.querySelector('#id_password1');
    var strengthBar = document.getElementById('pwStrengthBar');
    var strengthFill = document.getElementById('pwStrengthFill');
    var strengthLabel = document.getElementById('pwStrengthLabel');

    if (pwInput && strengthBar) {
        pwInput.addEventListener('input', function () {
            var pw = this.value;
            if (!pw) {
                strengthBar.style.display = 'none';
                return;
            }
            strengthBar.style.display = 'block';

            var score = 0;
            if (pw.length >= 8) score++;
            if (pw.length >= 12) score++;
            if (/[A-Z]/.test(pw)) score++;
            if (/[0-9]/.test(pw)) score++;
            if (/[^A-Za-z0-9]/.test(pw)) score++;

            var levels = [
                { pct: 20, cls: 'bg-danger',  label: 'Very weak' },
                { pct: 40, cls: 'bg-danger',  label: 'Weak' },
                { pct: 60, cls: 'bg-warning', label: 'Fair' },
                { pct: 80, cls: 'bg-info',    label: 'Good' },
                { pct: 100, cls: 'bg-success', label: 'Strong' },
            ];
            var level = levels[Math.min(score, levels.length) - 1] || levels[0];

            strengthFill.style.width = level.pct + '%';
            strengthFill.className = 'progress-bar ' + level.cls;
            strengthLabel.textContent = level.label;
            strengthLabel.className = 'small ' + level.cls.replace('bg-', 'text-');
        });
    }

    // ── Avatar colour preview (profile page) ─────────────────────────────
    var colorInput = document.querySelector('input[type="color"][name="avatar_color"]');
    var avatarPreview = document.getElementById('avatarPreview');
    if (colorInput && avatarPreview) {
        colorInput.addEventListener('input', function () {
            avatarPreview.style.background = this.value;
        });
    }
});
