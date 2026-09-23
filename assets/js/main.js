/* What the Phage v2.0 — landing page interactions */

(function () {
    'use strict';

    /* ---------- Sticky nav background ---------- */
    const nav = document.getElementById('nav');

    /* ---------- Mobile menu ---------- */
    const burger = document.getElementById('nav-burger');
    const links = document.getElementById('nav-links');

    if (burger && links) {
        burger.addEventListener('click', function () {
            links.classList.toggle('open');
        });
        links.querySelectorAll('a').forEach(function (a) {
            a.addEventListener('click', function () {
                links.classList.remove('open');
            });
        });
    }

    /* ---------- Scroll reveal ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        revealEls.forEach(function (el) { io.observe(el); });
    } else {
        revealEls.forEach(function (el) { el.classList.add('visible'); });
    }

    /* ---------- Animated counters ---------- */
    const counters = document.querySelectorAll('[data-count]');
    if (counters.length && 'IntersectionObserver' in window) {
        const animate = function (el) {
            const target = parseInt(el.getAttribute('data-count'), 10) || 0;
            const duration = 1200;
            const start = performance.now();
            const tick = function (now) {
                const p = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.round(eased * target);
                if (p < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
        };
        const cio = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animate(entry.target);
                    cio.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(function (el) { cio.observe(el); });
    }

    /* ---------- Copy-to-clipboard buttons ---------- */
    document.querySelectorAll('.copy-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const text = btn.getAttribute('data-copy') || '';
            const done = function () {
                btn.classList.add('copied');
                const orig = btn.textContent;
                btn.textContent = 'Copied!';
                setTimeout(function () {
                    btn.classList.remove('copied');
                    btn.textContent = orig;
                }, 1600);
            };
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(done, function () {
                    fallbackCopy(text, btn, done);
                });
            } else {
                fallbackCopy(text, btn, done);
            }
        });
    });

    function fallbackCopy(text, btn, done) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand('copy');
            done();
        } catch (e) {
            /* ignore */
        }
        document.body.removeChild(ta);
    }
})();