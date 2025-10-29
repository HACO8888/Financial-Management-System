/**
 * 財務管理系統 - 主要 JavaScript 功能
 */

// 當 DOM 載入完成後執行
document.addEventListener('DOMContentLoaded', function () {

  // 初始化所有工具提示
  initTooltips();

  // 自動隱藏 Flash 訊息
  autoHideAlerts();

  // 初始化表單驗證
  initFormValidation();

  // 初始化數字格式化
  formatCurrencyInputs();

  // 初始化確認對話框
  initConfirmDialogs();

  // 初始化資料表排序
  initTableSort();

  // 平滑捲動
  initSmoothScroll();
});

/**
 * 初始化 Bootstrap 工具提示
 */
function initTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

/**
 * 自動隱藏 Alert 訊息（5秒後）
 */
function autoHideAlerts() {
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
}

/**
 * 表單驗證增強
 */
function initFormValidation() {
  const forms = document.querySelectorAll('.needs-validation');

  Array.from(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
}

/**
 * 格式化貨幣輸入欄位
 */
function formatCurrencyInputs() {
  const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');

  currencyInputs.forEach(function (input) {
    // 限制小數位數為 2 位
    input.addEventListener('input', function (e) {
      const value = parseFloat(this.value);
      if (!isNaN(value)) {
        this.value = value.toFixed(2);
      }
    });

    // 失去焦點時格式化
    input.addEventListener('blur', function (e) {
      const value = parseFloat(this.value);
      if (!isNaN(value) && value >= 0) {
        this.value = value.toFixed(2);
      } else {
        this.value = '';
      }
    });
  });
}

/**
 * 確認對話框
 */
function initConfirmDialogs() {
  const confirmButtons = document.querySelectorAll('[data-confirm]');

  confirmButtons.forEach(function (button) {
    button.addEventListener('click', function (e) {
      const message = this.getAttribute('data-confirm');
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });
}

/**
 * 表格排序功能（簡易版）
 */
function initTableSort() {
  const sortableTables = document.querySelectorAll('.table-sortable');

  sortableTables.forEach(function (table) {
    const headers = table.querySelectorAll('th[data-sort]');

    headers.forEach(function (header) {
      header.style.cursor = 'pointer';
      header.innerHTML += ' <i class="bi bi-arrow-down-up text-muted"></i>';

      header.addEventListener('click', function () {
        sortTable(table, this);
      });
    });
  });
}

/**
 * 排序表格
 */
function sortTable(table, header) {
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const columnIndex = Array.from(header.parentElement.children).indexOf(header);
  const isAscending = header.classList.contains('sort-asc');

  // 排序
  rows.sort(function (a, b) {
    const aValue = a.children[columnIndex].textContent.trim();
    const bValue = b.children[columnIndex].textContent.trim();

    // 嘗試數字比較
    const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
    const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));

    if (!isNaN(aNum) && !isNaN(bNum)) {
      return isAscending ? aNum - bNum : bNum - aNum;
    }

    // 字串比較
    return isAscending ?
      aValue.localeCompare(bValue) :
      bValue.localeCompare(aValue);
  });

  // 更新表格
  rows.forEach(function (row) {
    tbody.appendChild(row);
  });

  // 更新排序圖示
  table.querySelectorAll('th').forEach(function (th) {
    th.classList.remove('sort-asc', 'sort-desc');
  });

  header.classList.toggle('sort-asc', !isAscending);
  header.classList.toggle('sort-desc', isAscending);
}

/**
 * 平滑捲動到錨點
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

/**
 * 數字計數動畫
 */
function animateValue(element, start, end, duration) {
  let startTimestamp = null;
  const step = function (timestamp) {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const value = progress * (end - start) + start;
    element.textContent = Math.floor(value).toLocaleString();
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

/**
 * 載入指示器
 */
function showLoadingSpinner(message = '載入中...') {
  const spinner = document.createElement('div');
  spinner.className = 'spinner-wrapper';
  spinner.id = 'global-spinner';
  spinner.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2 text-muted">${message}</p>
        </div>
    `;
  document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
  const spinner = document.getElementById('global-spinner');
  if (spinner) {
    spinner.remove();
  }
}

/**
 * AJAX 表單提交
 */
function submitFormAjax(form, successCallback, errorCallback) {
  const formData = new FormData(form);
  const url = form.action;
  const method = form.method || 'POST';

  showLoadingSpinner();

  fetch(url, {
    method: method,
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => response.json())
    .then(data => {
      hideLoadingSpinner();
      if (data.success) {
        if (successCallback) successCallback(data);
      } else {
        if (errorCallback) errorCallback(data);
      }
    })
    .catch(error => {
      hideLoadingSpinner();
      console.error('Error:', error);
      if (errorCallback) errorCallback(error);
    });
}

/**
 * 顯示通知訊息
 */
function showNotification(message, type = 'info') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.setAttribute('role', 'alert');
  alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

  const container = document.querySelector('.container-fluid') || document.querySelector('.container');
  if (container) {
    container.insertBefore(alertDiv, container.firstChild);

    // 自動隱藏
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alertDiv);
      bsAlert.close();
    }, 5000);
  }
}

/**
 * 格式化貨幣顯示
 */
function formatCurrency(amount) {
  return new Intl.NumberFormat('zh-TW', {
    style: 'currency',
    currency: 'TWD',
    minimumFractionDigits: 2
  }).format(amount);
}

/**
 * 格式化日期顯示
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(date);
}

/**
 * 複製文字到剪貼簿
 */
function copyToClipboard(text) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(function () {
      showNotification('已複製到剪貼簿', 'success');
    }).catch(function (err) {
      console.error('複製失敗:', err);
    });
  } else {
    // 舊版瀏覽器的備用方案
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showNotification('已複製到剪貼簿', 'success');
  }
}

/**
 * 防抖函數
 */
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

/**
 * 節流函數
 */
function throttle(func, limit) {
  let inThrottle;
  return function () {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

/**
 * 檢查元素是否在視窗中
 */
function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

/**
 * 延遲載入圖片
 */
function lazyLoadImages() {
  const images = document.querySelectorAll('img[data-src]');

  const imageObserver = new IntersectionObserver(function (entries, observer) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });

  images.forEach(function (img) {
    imageObserver.observe(img);
  });
}

/**
 * 導出到 CSV
 */
function exportTableToCSV(tableId, filename = 'data.csv') {
  const table = document.getElementById(tableId);
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll('tr');

  rows.forEach(function (row) {
    const cols = row.querySelectorAll('td, th');
    const csvRow = [];
    cols.forEach(function (col) {
      csvRow.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
    });
    csv.push(csvRow.join(','));
  });

  const csvContent = csv.join('\n');
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');

  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// 導出給全域使用
window.FinanceApp = {
  showLoadingSpinner,
  hideLoadingSpinner,
  submitFormAjax,
  showNotification,
  formatCurrency,
  formatDate,
  copyToClipboard,
  debounce,
  throttle,
  isElementInViewport,
  lazyLoadImages,
  exportTableToCSV,
  animateValue
};