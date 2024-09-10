document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded");

  function logElementStatus(id, querySelector = false) {
    const element = querySelector
      ? document.querySelector(id)
      : document.getElementById(id);
    console.log(`${id}: ${element ? "Found" : "Not found"}`);
    return element;
  }

  const compareButton = logElementStatus("compare-button");
  const compareBadgesContainer = logElementStatus("compare-badges");
  const compareCheckboxes = document.querySelectorAll(".compare-checkbox");
  const addToCompareBtn = logElementStatus("add-to-compare");
  console.log(`Compare checkboxes: ${compareCheckboxes.length} found`);

  function updateCompareUI() {
    console.log("Updating Compare UI");
    const compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    console.log("Compare products:", compareProducts);

    if (compareButton) {
      compareButton.style.display =
        compareProducts.length >= 2 ? "block" : "none";
    }

    compareCheckboxes.forEach((checkbox) => {
      const isChecked = compareProducts.some(
        (product) => product.id === checkbox.value
      );
      checkbox.checked = isChecked;
      console.log(
        `Checkbox ${checkbox.value}: ${isChecked ? "Checked" : "Unchecked"}`
      );
    });

    if (compareBadgesContainer) {
      compareBadgesContainer.innerHTML = "";
      compareProducts.forEach((product) => {
        const badge = document.createElement("div");
        badge.className = "compare-badge";
        badge.innerHTML = `
          <span>${product.name || `Product ${product.id}`}</span>
          <button class="remove-compare" data-product-id="${
            product.id
          }">&times;</button>
        `;
        compareBadgesContainer.appendChild(badge);
      });
    }

    // Update "Add to Compare" button on product detail page
    if (addToCompareBtn) {
      const productId = addToCompareBtn.dataset.productId;
      const isInCompare = compareProducts.some(
        (product) => product.id === productId
      );
      addToCompareBtn.textContent = isInCompare
        ? "Remove from Compare"
        : "Add to Compare";
      console.log(
        `Add to Compare button updated: ${addToCompareBtn.textContent}`
      );
    }
  }

  function toggleCompareProduct(productId, productName) {
    console.log("Toggling compare product:", { productId, productName });
    let compareProducts =
      JSON.parse(localStorage.getItem("compareProducts")) || [];
    const index = compareProducts.findIndex(
      (product) => product.id === productId
    );

    if (index > -1) {
      compareProducts.splice(index, 1);
      console.log(`Removed product ${productId} from compare list`);
    } else {
      compareProducts.push({ id: productId, name: productName });
      console.log(`Added product ${productId} to compare list`);
    }

    localStorage.setItem("compareProducts", JSON.stringify(compareProducts));
    updateCompareUI();
  }

  document.addEventListener("click", function (e) {
    console.log("Click event detected on:", e.target);

    if (e.target.classList.contains("compare-checkbox")) {
      const productCard = e.target.closest(".product-card");
      const productName = productCard
        ? productCard.querySelector(".product-title").textContent.trim()
        : "Unknown Product";
      console.log("Compare checkbox clicked:", {
        id: e.target.value,
        name: productName,
      });
      toggleCompareProduct(e.target.value, productName);
    }

    if (e.target.id === "add-to-compare") {
      const productName = document
        .querySelector(".product-title")
        .textContent.trim();
      const productId = e.target.dataset.productId;
      console.log("Add/Remove compare clicked:", {
        id: productId,
        name: productName,
      });
      toggleCompareProduct(productId, productName);
    }

    if (e.target.classList.contains("remove-compare")) {
      const productId = e.target.dataset.productId;
      const productName = e.target.previousElementSibling.textContent;
      console.log("Remove from compare clicked:", {
        id: productId,
        name: productName,
      });
      toggleCompareProduct(productId, productName);
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
