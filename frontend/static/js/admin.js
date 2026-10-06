/**
 * IRONPULSE FITNESS - ADMIN DASHBOARD & CONTROLS
 * ("admin sab control kr sake and sab bata sake")
 */

document.addEventListener("DOMContentLoaded", () => {
  // Tab switcher
  const tabBtns = document.querySelectorAll(".dash-tab-btn");
  const tabPanes = document.querySelectorAll(".dash-tab-pane");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabPanes.forEach((p) => (p.style.display = "none"));

      btn.classList.add("active");
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.style.display = "block";
    });
  });

  // User Filter by Status
  const userFilterSelect = document.getElementById("adminUserStatusFilter");
  const userSearchInput = document.getElementById("adminUserSearch");
  const userRows = document.querySelectorAll(".user-row");

  function filterUsers() {
    const statusVal = userFilterSelect ? userFilterSelect.value.toLowerCase() : "all";
    const query = userSearchInput ? userSearchInput.value.toLowerCase().trim() : "";

    userRows.forEach((row) => {
      const rowStatus = row.dataset.status ? row.dataset.status.toLowerCase() : "";
      const rowText = row.innerText.toLowerCase();

      const matchesStatus = statusVal === "all" || rowStatus === statusVal;
      const matchesSearch = query === "" || rowText.includes(query);

      if (matchesStatus && matchesSearch) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    });
  }

  if (userFilterSelect) userFilterSelect.addEventListener("change", filterUsers);
  if (userSearchInput) userSearchInput.addEventListener("input", filterUsers);
});

// Quick Extend Subscription via AJAX
async function quickExtendSub(userId, extraDays) {
  if (!confirm(`Are you sure you want to add +${extraDays} days to this user's membership?`)) {
    return;
  }

  const formData = new FormData();
  formData.append("user_id", userId);
  formData.append("extra_days", extraDays);

  try {
    const res = await fetch("/admin/extend-sub", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    if (data.success) {
      alert(`Success: ${data.message}`);
      window.location.reload();
    } else {
      alert(`Error: ${data.message || "Failed to extend subscription"}`);
    }
  } catch (err) {
    alert("Network error: Could not reach the server.");
  }
}

// Edit Product Modal population
function populateEditProduct(prod) {
  document.getElementById("editProductId").value = prod.id;
  document.getElementById("editProdName").value = prod.name;
  document.getElementById("editProdBrand").value = prod.brand;
  document.getElementById("editProdCategory").value = prod.category_id;
  document.getElementById("editProdPrice").value = prod.price;
  document.getElementById("editProdOrigPrice").value = prod.original_price || "";
  document.getElementById("editProdStock").value = prod.stock_quantity;
  document.getElementById("editProdImageUrl").value = prod.image_url;
  document.getElementById("editProdSpecs").value = prod.serving_specs || "";
  document.getElementById("editProdFlavor").value = prod.flavor_variant || "";
  document.getElementById("editProdDesc").value = prod.description;
  document.getElementById("editProdFeatured").checked = prod.is_featured === 1;

  window.openModal("editProductModal");
}

window.quickExtendSub = quickExtendSub;
window.populateEditProduct = populateEditProduct;
