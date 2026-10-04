/**
 * @file General Robotics — site behaviour.
 *
 * The page works fully without this file. It adds four small conveniences:
 *   1. a hairline under the header once the page has scrolled;
 *   2. the open/close menu on narrow screens;
 *   3. sections rising into place as they scroll into view;
 *   4. a private preview of the four emblem colourways (?emblem=a|b|c|d).
 *
 * No libraries, no tracking, no network requests.
 */
(function () {
  'use strict';

  /**
   * Emblem colourways from the brand's colour study.
   * a: red and silver · b: green, cream and gold · c: royal red, cream and gold
   * d: green and silver. The colour choice is still tentative.
   * @type {ReadonlyArray<string>}
   */
  var EMBLEM_OPTIONS = ['a', 'b', 'c', 'd'];

  /**
   * Add a hairline and soft shadow to the header after the page scrolls.
   * @returns {void}
   */
  function initHeader() {
    var header = document.querySelector('[data-header]');
    if (!header) { return; }
    var update = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  /**
   * Wire up the menu button shown on narrow screens. The menu closes when a
   * link is chosen or Escape is pressed.
   * @returns {void}
   */
  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.querySelector('[data-nav]');
    if (!toggle || !nav) { return; }

    /** @param {boolean} open Whether the menu should be showing. */
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
    };

    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (event) {
      if (event.target instanceof Element && event.target.closest('a')) { setOpen(false); }
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  /**
   * Reveal elements marked .reveal as they enter the viewport. If the browser
   * lacks IntersectionObserver, everything is shown at once.
   * @returns {void}
   */
  function initReveals() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) { return; }
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { observer.observe(el); });
  }

  /**
   * Preview another emblem colourway by adding ?emblem=a, b, c or d to the
   * address. Nothing is saved; removing the parameter restores the default.
   * @returns {void}
   */
  function initEmblemPreview() {
    var choice = (new URLSearchParams(window.location.search).get('emblem') || '').toLowerCase();
    if (EMBLEM_OPTIONS.indexOf(choice) === -1) { return; }
    var file = 'assets/img/emblem-' + choice + '.svg';
    document.querySelectorAll('[data-emblem]').forEach(function (img) {
      img.setAttribute('src', file);
    });
    var icon = document.querySelector('[data-emblem-icon]');
    if (icon) { icon.setAttribute('href', file); }
  }

  /**
   * Keep the copyright year current.
   * @returns {void}
   */
  function initYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  initEmblemPreview();
  initHeader();
  initNav();
  initReveals();
  initYear();
}());
