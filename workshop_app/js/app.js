/* workshop_app/static/workshop_app/js/app.js */

(function () {
  'use strict';

  /* ── 1. Prevent double-submit on all forms ── */
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.tagName !== 'FORM') return;
    var btn = form.querySelector('button[type="submit"]:not([data-no-loading])');
    if (!btn) return;
    if (btn.disabled) { e.preventDefault(); return; }
    var originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML =
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>' +
      '&nbsp;' + (btn.dataset.loadingText || 'Please wait…');
    // safety reset after 10s
    setTimeout(function () {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }, 10000);
  });

  /* ── 2. Active nav link ── */
  var path = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && href !== '/' && path.indexOf(href) === 0) {
      link.classList.add('active-page');
    } else if (href === '/' && path === '/') {
      link.classList.add('active-page');
    }
  });

  /* ── 3. Auto-dismiss flash alerts after 5s ── */
  document.querySelectorAll('.alert[role="alert"]:not(.alert-permanent)').forEach(function (el) {
    setTimeout(function () {
      if (el.parentNode) {
        el.style.transition = 'opacity .4s';
        el.style.opacity = '0';
        setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 400);
      }
    }, 5000);
  });

  /* ── 4. Accept-workshop modal: set href & name ── */
  document.addEventListener('show.bs.modal', function (e) {});

  var acceptModal = document.getElementById('acceptModal');
  if (acceptModal) {
    acceptModal.addEventListener('show.bs.modal', function (e) {
      var btn = e.relatedTarget;
      var wid  = btn && btn.getAttribute('data-workshop-id');
      var name = btn && btn.getAttribute('data-workshop-name');
      var nameEl = document.getElementById('acceptWorkshopName');
      var link   = document.getElementById('acceptConfirmLink');
      if (nameEl) nameEl.textContent = name || '';
      if (link && wid) {
        link.href = link.getAttribute('data-base-url').replace('__ID__', wid);
      }
    });
  }

  /* ── 5. Propose-workshop: set native date min/max ── */
  var dateInput = document.getElementById('id_date');
  if (dateInput) {
    var today = new Date();
    var minD  = new Date(today); minD.setDate(today.getDate() + 3);
    var maxD  = new Date(today); maxD.setFullYear(today.getFullYear() + 1);
    function iso(d) {
      return d.getFullYear() + '-' +
        String(d.getMonth() + 1).padStart(2, '0') + '-' +
        String(d.getDate()).padStart(2, '0');
    }
    dateInput.min = iso(minD);
    dateInput.max = iso(maxD);
  }

  /* ── 6. T&C AJAX fetch ── */
  var tncTrigger = document.getElementById('disp_tnc');
  if (tncTrigger) {
    tncTrigger.addEventListener('click', function (e) {
      e.preventDefault();
      var typeSelect = document.getElementById('id_workshop_type');
      var contentEl  = document.getElementById('tncContent');
      if (!typeSelect || !contentEl) return;

      if (!typeSelect.value) {
        contentEl.innerHTML =
          '<p class="text-danger"><i class="fa fa-exclamation-circle"></i> Please select a workshop type first.</p>';
        $('#tncModal').modal('show');
        return;
      }

      contentEl.innerHTML =
        '<div style="text-align:center;padding:32px">' +
        '<span class="spinner-border" role="status"></span></div>';
      $('#tncModal').modal('show');

      fetch('/workshop/type_tnc/' + typeSelect.value + '/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          contentEl.innerHTML =
            '<p style="font-size:14px;line-height:1.8;white-space:pre-wrap">' +
            (data.tnc || 'No terms available.') + '</p>';
        })
        .catch(function () {
          contentEl.innerHTML =
            '<p class="text-danger">Could not load terms. Please try again.</p>';
        });
    });
  }

})();
