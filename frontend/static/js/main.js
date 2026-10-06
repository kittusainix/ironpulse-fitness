/**
 * IRONPULSE FITNESS - MAIN CLIENT SCRIPT
 * Handles responsive navigation, modals, cart drawer, and UI interactions
 */

document.addEventListener("DOMContentLoaded", () => {
  // Sticky Navbar on Scroll
  const navbar = document.querySelector(".navbar");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 25) {
      navbar?.classList.add("scrolled");
    } else {
      navbar?.classList.remove("scrolled");
    }
  });

  // Responsive Mobile Menu Drawer Setup
  const mobileToggle = document.getElementById("mobileMenuToggleBtn");
  const navDrawer = document.getElementById("mainNavLinks");
  const navBackdrop = document.getElementById("mobileNavBackdrop");
  const drawerCloseBtn = document.getElementById("mobileDrawerCloseBtn");

  function openMobileNav() {
    navDrawer?.classList.add("active");
    navBackdrop?.classList.add("active");
    document.body.classList.add("mobile-nav-open");
  }

  function closeMobileNav() {
    navDrawer?.classList.remove("active");
    navBackdrop?.classList.remove("active");
    document.body.classList.remove("mobile-nav-open");
  }

  mobileToggle?.addEventListener("click", () => {
    if (navDrawer?.classList.contains("active")) {
      closeMobileNav();
    } else {
      openMobileNav();
    }
  });

  drawerCloseBtn?.addEventListener("click", closeMobileNav);
  navBackdrop?.addEventListener("click", closeMobileNav);

  // Close mobile nav when clicking any nav link (e.g. #bmiSection or page switch)
  navDrawer?.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 992) {
        closeMobileNav();
      }
    });
  });

  // Handle Escape key to close any active overlay (modal, cart drawer, mobile nav)
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeMobileNav();
      document.querySelectorAll(".modal-overlay.active").forEach((m) => {
        m.classList.remove("active");
        document.body.style.overflow = "auto";
      });
      document.getElementById("cartDrawer")?.classList.remove("active");
    }
  });

  // Toast Auto-Dismiss
  const toasts = document.querySelectorAll(".toast");
  toasts.forEach((t) => {
    setTimeout(() => {
      t.style.opacity = "0";
      t.style.transform = "translateX(100%)";
      t.style.transition = "all 0.4s ease";
      setTimeout(() => t.remove(), 400);
    }, 4500);
  });

  // Global Modal Opener / Closer
  window.openModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add("active");
      document.body.style.overflow = "hidden";
    }
  };

  window.closeModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove("active");
      document.body.style.overflow = "auto";
    }
  };

  // Close modals when clicking backdrop
  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("active");
        document.body.style.overflow = "auto";
      }
    });
  });

  // Cart Drawer open/close
  const cartBtn = document.getElementById("cartToggleBtn");
  const cartDrawer = document.getElementById("cartDrawer");
  const cartClose = document.getElementById("cartDrawerClose");

  if (cartBtn && cartDrawer) {
    cartBtn.addEventListener("click", () => {
      cartDrawer.classList.add("active");
      document.body.classList.add("cart-open");
    });
  }

  if (cartClose && cartDrawer) {
    cartClose.addEventListener("click", () => {
      cartDrawer.classList.remove("active");
      document.body.classList.remove("cart-open");
    });
  }
});
