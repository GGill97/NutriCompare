
document.addEventListener("DOMContentLoaded", function () {
  // Comparison functionality
  const compareForm = document.getElementById("compare-form");
  const compareCheckboxes = document.querySelectorAll(".compare-checkbox");
  const compareButton = document.getElementById("compare-button");

  if (compareForm && compareCheckboxes.length > 0 && compareButton) {
    compareCheckboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", updateCompareButton);
    });
  }

  function updateCompareButton() {
    const selectedCount = Array.from(compareCheckboxes).filter(
      (cb) => cb.checked
    ).length;
    if (selectedCount >= 2) {
      compareButton.classList.remove("d-none");
      compareButton.classList.add("d-block");
      compareButton.querySelector(
        ".btn"
      ).textContent = `Compare ${selectedCount} Products`;
    } else {
      compareButton.classList.remove("d-block");
      compareButton.classList.add("d-none");
    }
  }

  // Filter form submission
  const filterForm = document.getElementById("filter-form");
  const searchInput = document.getElementById("search");
  if (filterForm) {
    filterForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(filterForm);
      const searchParams = new URLSearchParams(formData);
      window.location.href = `${filterForm.action}?${searchParams.toString()}`;
    });

    // Add event listener for real-time search (optional)
    if (searchInput) {
      searchInput.addEventListener(
        "input",
        debounce(function () {
          filterForm.submit();
        }, 300)
      );
    }
  }

  // Sort change handler
  const sortSelect = document.getElementById("sort");
  const orderSelect = document.getElementById("order");
  if (sortSelect && orderSelect) {
    sortSelect.addEventListener("change", function () {
      filterForm.submit();
    });
    orderSelect.addEventListener("change", function () {
      filterForm.submit();
    });
  }

  // Price range slider
  const priceSlider = document.getElementById("price-range");
  const minPriceInput = document.getElementById("min-price");
  const maxPriceInput = document.getElementById("max-price");

  if (priceSlider && minPriceInput && maxPriceInput) {
    const updatePriceInputs = (values) => {
      minPriceInput.value = values[0];
      maxPriceInput.value = values[1];
    };

    noUiSlider.create(priceSlider, {
      start: [parseFloat(minPriceInput.value), parseFloat(maxPriceInput.value)],
      connect: true,
      range: {
        min: parseFloat(minPriceInput.min),
        max: parseFloat(maxPriceInput.max),
      },
    });

    priceSlider.noUiSlider.on("update", updatePriceInputs);

    minPriceInput.addEventListener("change", function () {
      priceSlider.noUiSlider.set([this.value, null]);
    });

    maxPriceInput.addEventListener("change", function () {
      priceSlider.noUiSlider.set([null, this.value]);
    });
  }

  // Protein type dropdown
  const proteinTypeDropdown = document.getElementById("protein-type-dropdown");
  const proteinTypeOptions = document.getElementById("protein-type-options");

  if (proteinTypeDropdown && proteinTypeOptions) {
    proteinTypeDropdown.addEventListener("click", function () {
      proteinTypeOptions.style.display =
        proteinTypeOptions.style.display === "none" ? "block" : "none";
    });

    document.addEventListener("click", function (event) {
      if (!proteinTypeDropdown.contains(event.target)) {
        proteinTypeOptions.style.display = "none";
      }
    });
  }
});


document.addEventListener("DOMContentLoaded", function () {
  // ... (previous code remains the same) ...

  // Function to handle dropdowns
  function setupDropdown(dropdownId, optionsId) {
      const dropdown = document.getElementById(dropdownId);
      const options = document.getElementById(optionsId);

      if (dropdown && options) {
          dropdown.addEventListener("click", function (event) {
              event.stopPropagation();
              options.style.display = options.style.display === "none" ? "block" : "none";
          });

          document.addEventListener("click", function (event) {
              if (!dropdown.contains(event.target)) {
                  options.style.display = "none";
              }
          });
      }
  }

  // Setup dropdowns
  setupDropdown("protein-type-dropdown", "protein-type-options");
  setupDropdown("price-range-dropdown", "price-range-options");
  setupDropdown("protein-content-dropdown", "protein-content-options");

  // Update dropdown headers based on selected options
  function updateDropdownHeader(dropdownId, optionsName) {
      const dropdown = document.getElementById(dropdownId);
      const options = document.getElementsByName(optionsName);
      const header = dropdown.querySelector('.select-header');

      const selectedOptions = Array.from(options)
          .filter(option => option.checked)
          .map(option => option.nextSibling.textContent.trim());

      if (selectedOptions.length > 0) {
          header.textContent = selectedOptions.join(", ");
      } else {
          header.textContent = `Select ${dropdownId.replace("-dropdown", "").replace(/-/g, " ")}`;
      }
  }

  // Add event listeners to update headers
  document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', function() {
          const dropdownId = this.closest('.custom-select').id;
          updateDropdownHeader(dropdownId, this.name);
      });
  });

  // Initial update of headers
  updateDropdownHeader("protein-type-dropdown", "category");
  updateDropdownHeader("price-range-dropdown", "price_range");
  updateDropdownHeader("protein-content-dropdown", "protein_range");
});
