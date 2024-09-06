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

  // Filter change handlers
  const filterInputs = filterForm.querySelectorAll(
    "select, input[type='checkbox']"
  );
  filterInputs.forEach((input) => {
    input.addEventListener("change", function () {
      filterForm.submit();
    });
  });

  // Sort and order change handlers
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

  // Debounce function for search input
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

  // Multi-select dropdown for Product Types
  const categorySelect = document.getElementById("category");
  if (categorySelect) {
    $(categorySelect).select2({
      placeholder: "Select Product Types",
      allowClear: true,
      closeOnSelect: false,
    });

    // Trigger form submission when Select2 selection changes
    $(categorySelect).on("change", function () {
      filterForm.submit();
    });
  }

});
