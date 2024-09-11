document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  const compareButton = document.getElementById("compare-button");
  const compareBadgesContainer = document.getElementById("compare-badges");
  const compareCheckboxes = document.querySelectorAll(".compare-checkbox");
  const addToCompareBtn = document.getElementById("add-to-compare");

  const MIN_COMPARE_PRODUCTS = 2;
  const MAX_COMPARE_PRODUCTS = 4;

  function updateCompareUI() {
    console.log("Updating Compare UI");
    const compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    console.log("Compare products:", compareProducts);

    if (compareButton) {
      compareButton.style.display =
        compareProducts.length >= MIN_COMPARE_PRODUCTS ? "block" : "none";
      compareButton.disabled = compareProducts.length < MIN_COMPARE_PRODUCTS;
    }

    compareCheckboxes.forEach((checkbox) => {
      const isChecked = compareProducts.some(
        (product) =>
          (typeof product === "string" && product === checkbox.value) ||
          (typeof product === "object" && product.id === checkbox.value)
      );
      checkbox.checked = isChecked;
      checkbox.disabled =
        !isChecked && compareProducts.length >= MAX_COMPARE_PRODUCTS;
    });

    if (compareBadgesContainer) {
      compareBadgesContainer.innerHTML = "";
      compareProducts.forEach((product) => {
        const productId = typeof product === "string" ? product : product.id;
        const productName =
          typeof product === "string" ? `Product ${product}` : product.name;
        const badge = document.createElement("div");
        badge.className = "compare-badge";
        badge.innerHTML = `
          <span>${productName}</span>
          <button class="remove-compare" data-product-id="${productId}">&times;</button>
        `;
        compareBadgesContainer.appendChild(badge);
      });
    }

    if (addToCompareBtn) {
      const productId = addToCompareBtn.dataset.productId;
      const isInCompare = compareProducts.some(
        (product) =>
          (typeof product === "string" && product === productId) ||
          (typeof product === "object" && product.id === productId)
      );
      addToCompareBtn.textContent = isInCompare
        ? "Remove from Compare"
        : "Add to Compare";
      addToCompareBtn.disabled =
        !isInCompare && compareProducts.length >= MAX_COMPARE_PRODUCTS;
    }
  }

  function toggleCompareProduct(productId, productName) {
    let compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    const index = compareProducts.findIndex(
      (product) =>
        (typeof product === "string" && product === productId) ||
        (typeof product === "object" && product.id === productId)
    );

    if (index > -1) {
      compareProducts.splice(index, 1);
      console.log(`Removed product ${productId} from compare list`);
    } else if (compareProducts.length < MAX_COMPARE_PRODUCTS) {
      compareProducts.push({ id: productId, name: productName });
      console.log(`Added product ${productId} to compare list`);
    } else {
      console.log(`Cannot add product ${productId}. Compare list is full.`);
      alert(
        `You can compare up to ${MAX_COMPARE_PRODUCTS} products at a time. Please remove a product before adding a new one.`
      );
      return;
    }

    localStorage.setItem("compareProducts", JSON.stringify(compareProducts));
    updateCompareUI();
  }

  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("compare-checkbox")) {
      const productCard = e.target.closest(".product-card");
      const productName = productCard
        ? productCard.querySelector(".product-title").textContent.trim()
        : `Product ${e.target.value}`;
      toggleCompareProduct(e.target.value, productName);
    }

    if (e.target.id === "add-to-compare") {
      const productName = document
        .querySelector(".product-title")
        .textContent.trim();
      toggleCompareProduct(e.target.dataset.productId, productName);
    }

    if (e.target.classList.contains("remove-compare")) {
      toggleCompareProduct(e.target.dataset.productId);
    }
  });

  updateCompareUI();
  console.log("Initial compare UI update completed");
});

// --- Filter Functionality ---
const filterForm = document.getElementById("filter-form");
const searchInput = document.getElementById("search-input");

if (filterForm) {
  filterForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData(filterForm);
    const searchParams = new URLSearchParams(formData);
    window.location.href = `${filterForm.action}?${searchParams.toString()}`;
  });

  if (searchInput) {
    searchInput.addEventListener(
      "input",
      debounce(function () {
        filterForm.submit();
      }, 300)
    );
  }

  const filterInputs = filterForm.querySelectorAll(
    "select, input[type='checkbox']"
  );
  filterInputs.forEach((input) => {
    input.addEventListener("change", function () {
      filterForm.submit();
    });
  });
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// --- Image Zoom Functionality ---
const productImage = document.querySelector(".product-image img");
if (productImage) {
  productImage.addEventListener("mousemove", function (e) {
    const { left, top, width, height } = this.getBoundingClientRect();
    const x = ((e.clientX - left) / width) * 100;
    const y = ((e.clientY - top) / height) * 100;
    this.style.transformOrigin = `${x}% ${y}%`;
  });

  productImage.addEventListener("mouseenter", function () {
    this.style.transform = "scale(1.5)";
  });

  productImage.addEventListener("mouseleave", function () {
    this.style.transform = "scale(1)";
    this.style.transformOrigin = "center center";
  });
}
