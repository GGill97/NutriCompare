document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  const compareButton = document.getElementById("compare-button");
  const compareBadgesContainer = document.getElementById("compare-badges");
  const compareCheckboxes = document.querySelectorAll(".compare-checkbox");
  const compareContainer = document.getElementById("compare-container");
  const addToCompareButton = document.getElementById("add-to-compare");

  console.log("Compare button:", compareButton);
  console.log("Compare badges container:", compareBadgesContainer);
  console.log("Compare checkboxes:", compareCheckboxes.length);
  console.log("Compare container:", compareContainer);
  console.log("Add to Compare button:", addToCompareButton);

  const MIN_COMPARE_PRODUCTS = 2;
  const MAX_COMPARE_PRODUCTS = 4;

  function updateCompareUI() {
    console.log("Updating Compare UI");
    const compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    console.log("Compare products:", compareProducts);

    if (compareContainer) {
      compareContainer.style.display =
        compareProducts.length > 0 ? "block" : "none";
      console.log("Compare container display:", compareContainer.style.display);
    } else {
      console.error("Compare container not found");
    }

    if (compareButton) {
      compareButton.disabled =
        compareProducts.length < MIN_COMPARE_PRODUCTS ||
        compareProducts.length > MAX_COMPARE_PRODUCTS;
      console.log("Compare button disabled:", compareButton.disabled);
    } else {
      console.error("Compare button not found");
    }

    compareCheckboxes.forEach((checkbox) => {
      const isChecked = compareProducts.some(
        (product) => product.id === checkbox.value
      );
      checkbox.checked = isChecked;
      checkbox.disabled =
        !isChecked && compareProducts.length >= MAX_COMPARE_PRODUCTS;
      console.log(
        `Checkbox ${checkbox.value}: checked=${checkbox.checked}, disabled=${checkbox.disabled}`
      );
    });

    if (addToCompareButton) {
      const productId = addToCompareButton.dataset.productId;
      const isInCompare = compareProducts.some(
        (product) => product.id === productId
      );
      addToCompareButton.textContent = isInCompare
        ? "Remove from Compare"
        : "Add to Compare";
      addToCompareButton.disabled =
        !isInCompare && compareProducts.length >= MAX_COMPARE_PRODUCTS;
    }

    if (compareBadgesContainer) {
      compareBadgesContainer.innerHTML = "";
      compareProducts.forEach((product) => {
        const badge = document.createElement("div");
        badge.className = "compare-badge";
        badge.innerHTML = `
          <span>${product.name}</span>
          <button class="remove-compare" data-product-id="${product.id}">&times;</button>
        `;
        compareBadgesContainer.appendChild(badge);
        console.log(`Added badge for product: ${product.name}`);
      });
    } else {
      console.error("Compare badges container not found");
    }
  }

  function toggleCompareProduct(productId, productName) {
    console.log(`Toggling compare for product: ${productId} - ${productName}`);
    let compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    const index = compareProducts.findIndex(
      (product) => product.id === productId
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
    console.log(
      "Updated localStorage:",
      localStorage.getItem("compareProducts")
    );
    updateCompareUI();
  }

  document.addEventListener("click", function (e) {
    console.log("Click event on:", e.target);

    if (e.target.classList.contains("compare-checkbox")) {
      const productCard = e.target.closest(".product-card");
      const productName = productCard
        ? productCard.querySelector(".product-title").textContent.trim()
        : `Product ${e.target.value}`;
      console.log(`Checkbox clicked: ${e.target.value} - ${productName}`);
      toggleCompareProduct(e.target.value, productName);
    }

    if (e.target.id === "add-to-compare") {
      const productId = e.target.dataset.productId;
      const productName = document
        .querySelector(".product-title")
        .textContent.trim();
      console.log(`Add to Compare clicked: ${productId} - ${productName}`);
      toggleCompareProduct(productId, productName);
    }

    if (e.target.classList.contains("remove-compare")) {
      console.log(`Remove from compare clicked: ${e.target.dataset.productId}`);
      toggleCompareProduct(e.target.dataset.productId);
    }

    if (e.target.id === "compare-button") {
      console.log("Compare button clicked");
      const compareProducts =
        JSON.parse(localStorage.getItem("compareProducts")) || [];
      if (
        compareProducts.length >= MIN_COMPARE_PRODUCTS &&
        compareProducts.length <= MAX_COMPARE_PRODUCTS
      ) {
        const compareUrl = new URL(window.location.origin + "/compare");
        compareProducts.forEach((product) => {
          compareUrl.searchParams.append("products", product.id);
        });
        console.log("Redirecting to compare page:", compareUrl.toString());
        window.location.href = compareUrl.toString();
      } else {
        console.log("Invalid number of products selected for comparison");
        alert(
          x`Please select between ${MIN_COMPARE_PRODUCTS} and ${MAX_COMPARE_PRODUCTS} products to compare.`
        );
      }
    }
  });

  updateCompareUI();
  console.log("Initial compare UI update completed");
});


// --- Filter Functionality ---
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
// Chart creation logic
if (document.querySelector(".compare-container")) {
  createCharts();
}

