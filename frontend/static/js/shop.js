/**
 * IRONPULSE FITNESS - SHOPPING CART & PRODUCT INTERACTIONS
 */

let cart = [];

try {
  const savedCart = localStorage.getItem("ironpulse_cart");
  if (savedCart) {
    cart = JSON.parse(savedCart);
  }
} catch (e) {
  cart = [];
}

function saveCart() {
  localStorage.setItem("ironpulse_cart", JSON.stringify(cart));
  updateCartUI();
}

function addToCart(productId, name, unitPrice, imageUrl) {
  const existing = cart.find((item) => item.product_id === productId);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      product_id: productId,
      name: name,
      unit_price: parseFloat(unitPrice),
      image_url: imageUrl,
      quantity: 1
    });
  }
  saveCart();

  // Open cart drawer
  const cartDrawer = document.getElementById("cartDrawer");
  if (cartDrawer) cartDrawer.classList.add("active");

  showCartToast(`Added ${name} to cart!`);
}

function changeQty(productId, delta) {
  const item = cart.find((i) => i.product_id === productId);
  if (item) {
    item.quantity += delta;
    if (item.quantity <= 0) {
      cart = cart.filter((i) => i.product_id !== productId);
    }
    saveCart();
  }
}

function removeFromCart(productId) {
  cart = cart.filter((i) => i.product_id !== productId);
  saveCart();
}

function clearCart() {
  cart = [];
  saveCart();
}

function updateCartUI() {
  const badge = document.getElementById("cartBadgeCount");
  const container = document.getElementById("cartItemsList");
  const totalAmountEl = document.getElementById("cartTotalAmount");
  const checkoutBtn = document.getElementById("cartCheckoutBtn");
  const cartDataInput = document.getElementById("cartDataInput");

  const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
  const totalAmount = cart.reduce((sum, item) => sum + item.unit_price * item.quantity, 0);

  if (badge) badge.innerText = totalQty;
  if (totalAmountEl) totalAmountEl.innerText = `₹${totalAmount.toLocaleString('en-IN')}`;

  if (cartDataInput) {
    cartDataInput.value = JSON.stringify(cart);
  }

  if (checkoutBtn) {
    checkoutBtn.disabled = cart.length === 0;
  }

  if (container) {
    if (cart.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--text-muted);">
          <i class="fa-solid fa-cart-shopping" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
          <p>Your gym cart is empty.</p>
          <a href="/shop" class="btn btn-outline btn-sm" style="margin-top: 1rem;">Explore Supplements</a>
        </div>
      `;
    } else {
      container.innerHTML = cart
        .map(
          (item) => `
          <div class="cart-item">
            <img src="${item.image_url}" alt="${item.name}">
            <div class="cart-item-details">
              <div class="cart-item-title">${item.name}</div>
              <div class="cart-item-price">₹${(item.unit_price * item.quantity).toLocaleString('en-IN')}</div>
              <div class="cart-qty-ctrl">
                <button type="button" class="cart-qty-btn" onclick="changeQty(${item.product_id}, -1)">-</button>
                <span style="font-size: 0.85rem; font-weight: 700;">${item.quantity}</span>
                <button type="button" class="cart-qty-btn" onclick="changeQty(${item.product_id}, 1)">+</button>
                <button type="button" onclick="removeFromCart(${item.product_id})" style="background: none; border: none; color: #ef4444; font-size: 0.8rem; cursor: pointer; margin-left: 0.5rem;">
                  <i class="fa-solid fa-trash"></i>
                </button>
              </div>
            </div>
          </div>
        `
        )
        .join("");
    }
  }
}

function showCartToast(msg) {
  const container = document.querySelector(".toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast toast-success";
  toast.innerHTML = `<i class="fa-solid fa-check-circle" style="color: #10b981;"></i> <span>${msg}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

document.addEventListener("DOMContentLoaded", () => {
  updateCartUI();

  // Instant Checkout modal opener
  const checkoutBtn = document.getElementById("cartCheckoutBtn");
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", () => {
      if (cart.length === 0) return;
      const cartDrawer = document.getElementById("cartDrawer");
      if (cartDrawer) cartDrawer.classList.remove("active");
      
      const modal = document.getElementById("checkoutModal");
      const checkoutTotalVal = document.getElementById("checkoutTotalVal");
      const totalAmount = cart.reduce((sum, item) => sum + item.unit_price * item.quantity, 0);
      if (checkoutTotalVal) checkoutTotalVal.innerText = `₹${totalAmount.toLocaleString('en-IN')}`;
      if (modal) modal.classList.add("active");
    });
  }
});

window.addToCart = addToCart;
window.changeQty = changeQty;
window.removeFromCart = removeFromCart;
window.clearCart = clearCart;
