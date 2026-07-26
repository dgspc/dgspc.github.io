(function () {
  "use strict";

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('stuck', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var rvs = document.querySelectorAll('.rv');
  if (rvs.length) {
    if (!('IntersectionObserver' in window) || reduce) {
      rvs.forEach(function (n) { n.classList.add('on'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
      rvs.forEach(function (n) { io.observe(n); });
    }
  }

  var burger = document.querySelector('.burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      if (links.style.display === 'flex') { links.style.display = ''; return; }
      links.style.display = 'flex';
      links.style.position = 'absolute';
      links.style.top = '70px';
      links.style.left = '0';
      links.style.right = '0';
      links.style.flexDirection = 'column';
      links.style.gap = '2px';
      links.style.background = '#0E1012';
      links.style.borderTop = '1px solid #24282C';
      links.style.borderBottom = '1px solid #24282C';
      links.style.padding = '18px var(--gut)';
    });
  }
})();
