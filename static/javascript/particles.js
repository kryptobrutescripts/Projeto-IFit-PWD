(function () {
    var canvas = document.getElementById('particles');
    if (!canvas) return;
    var ctx = canvas.getContext('2d', { alpha: true });
    var width = 0;
    var height = 0;
    var particles = [];
    var particleCount = 42;
    var maxDistance = 120;
    var maxDistanceSquared = maxDistance * maxDistance;
    var mouse = { x: -1000, y: -1000, radius: 120 };
    var particleColor = '#000000';
    var lineColor = 'rgba(0,0,0,0.15)';
    var animationFrame = 0;
    var pageVisible = true;
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function resize() {
        var nextWidth = window.innerWidth;
        var nextHeight = window.innerHeight;
        if (nextWidth === width && nextHeight === height) return;
        width = nextWidth;
        height = nextHeight;
        canvas.width = width;
        canvas.height = height;
        initParticles();
    }
    function updateColors() {
        var rootStyle = getComputedStyle(document.documentElement);
        particleColor = rootStyle.getPropertyValue('--particle-color').trim() || '#000000';
        lineColor = rootStyle.getPropertyValue('--particle-line-color').trim() || 'rgba(0,0,0,0.15)';
    }
    function Particle() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.45;
        this.vy = (Math.random() - 0.5) * 0.45;
        this.size = Math.random() * 1.8 + 0.8;
    }
    Particle.prototype.update = function () {
        var dx = this.x - mouse.x;
        var dy = this.y - mouse.y;
        var distSquared = dx * dx + dy * dy;
        if (distSquared < mouse.radius * mouse.radius && distSquared > 1) {
            var dist = Math.sqrt(distSquared);
            var force = (mouse.radius - dist) / mouse.radius;
            this.vx += (dx / dist) * force * 0.12;
            this.vy += (dy / dist) * force * 0.12;
        }
        this.x += this.vx;
        this.y += this.vy;
        this.vx *= 0.992;
        this.vy *= 0.992;
        if (this.x <= 0 || this.x >= width) { this.vx *= -1; this.x = Math.max(0, Math.min(width, this.x)); }
        if (this.y <= 0 || this.y >= height) { this.vy *= -1; this.y = Math.max(0, Math.min(height, this.y)); }
    };
    Particle.prototype.draw = function () {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = particleColor;
        ctx.fill();
    };
    function initParticles() {
        particles = [];
        for (var i = 0; i < particleCount; i += 1) particles.push(new Particle());
    }
    function drawLines() {
        ctx.strokeStyle = lineColor;
        ctx.lineWidth = 0.45;
        for (var i = 0; i < particles.length; i += 1) {
            for (var j = i + 1; j < particles.length; j += 1) {
                var dx = particles[i].x - particles[j].x;
                var dy = particles[i].y - particles[j].y;
                if (dx * dx + dy * dy < maxDistanceSquared) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }
    function animate() {
        animationFrame = requestAnimationFrame(animate);
        if (!pageVisible || reducedMotion) return;
        ctx.clearRect(0, 0, width, height);
        for (var i = 0; i < particles.length; i += 1) {
            particles[i].update();
            particles[i].draw();
        }
        drawLines();
    }
    var resizeTimer = 0;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resize, 100);
    }, { passive: true });
    window.addEventListener('mousemove', function (event) {
        mouse.x = event.clientX;
        mouse.y = event.clientY;
    }, { passive: true });
    window.addEventListener('mouseleave', function () {
        mouse.x = -1000;
        mouse.y = -1000;
    }, { passive: true });
    document.addEventListener('visibilitychange', function () {
        pageVisible = document.visibilityState === 'visible';
    });
    window.particlesUpdate = function () {
        updateColors();
    };
    resize();
    updateColors();
    if (!reducedMotion) animate();
})();
