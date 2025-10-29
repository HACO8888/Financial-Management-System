/**
 * 財務管理系統 - 圖表工具函數
 * 使用 Chart.js 建立各種財務圖表
 */

/**
 * 預設圖表配置
 */
const defaultChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 15,
        font: {
          size: 12
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: {
        size: 14,
        weight: 'bold'
      },
      bodyFont: {
        size: 13
      },
      displayColors: true,
      callbacks: {
        label: function (context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += '$' + context.parsed.y.toLocaleString('zh-TW', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            });
          }
          return label;
        }
      }
    }
  }
};

/**
 * 顏色配置
 */
const chartColors = {
  income: 'rgba(25, 135, 84, 0.8)',     // 綠色 - 收入
  expense: 'rgba(220, 53, 69, 0.8)',    // 紅色 - 支出
  net: 'rgba(13, 202, 240, 0.8)',       // 藍色 - 淨額
  primary: 'rgba(13, 110, 253, 0.8)',   // 主色
  success: 'rgba(25, 135, 84, 0.8)',
  danger: 'rgba(220, 53, 69, 0.8)',
  warning: 'rgba(255, 193, 7, 0.8)',
  info: 'rgba(13, 202, 240, 0.8)',

  // 多色調色盤（用於圓餅圖）
  palette: [
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(201, 203, 207, 0.8)',
    'rgba(255, 99, 71, 0.8)',
    'rgba(144, 238, 144, 0.8)',
    'rgba(173, 216, 230, 0.8)'
  ]
};

/**
 * 建立圓餅圖（類別分布）
 */
function createPieChart(canvasId, labels, data, title = '') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: chartColors.palette,
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    options: {
      ...defaultChartOptions,
      plugins: {
        ...defaultChartOptions.plugins,
        title: {
          display: title !== '',
          text: title,
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  });
}

/**
 * 建立甜甜圈圖
 */
function createDoughnutChart(canvasId, labels, data, title = '') {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: chartColors.palette,
        borderColor: '#fff',
        borderWidth: 2
      }]
    },
    options: {
      ...defaultChartOptions,
      cutout: '60%',
      plugins: {
        ...defaultChartOptions.plugins,
        title: {
          display: title !== '',
          text: title,
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    }
  });
}

/**
 * 建立長條圖（收入vs支出）
 */
function createBarChart(canvasId, labels, incomeData, expenseData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '收入',
          data: incomeData,
          backgroundColor: chartColors.income,
          borderColor: chartColors.income.replace('0.8', '1'),
          borderWidth: 1
        },
        {
          label: '支出',
          data: expenseData,
          backgroundColor: chartColors.expense,
          borderColor: chartColors.expense.replace('0.8', '1'),
          borderWidth: 1
        }
      ]
    },
    options: {
      ...defaultChartOptions,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

/**
 * 建立折線圖（趨勢圖）
 */
function createLineChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const processedDatasets = datasets.map((dataset, index) => ({
    label: dataset.label,
    data: dataset.data,
    borderColor: dataset.color || chartColors.palette[index],
    backgroundColor: (dataset.color || chartColors.palette[index]).replace('0.8', '0.1'),
    borderWidth: 2,
    tension: 0.4,
    fill: dataset.fill !== undefined ? dataset.fill : true,
    pointRadius: 3,
    pointHoverRadius: 5
  }));

  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: processedDatasets
    },
    options: {
      ...defaultChartOptions,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  });
}

/**
 * 建立堆疊長條圖
 */
function createStackedBarChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const processedDatasets = datasets.map((dataset, index) => ({
    label: dataset.label,
    data: dataset.data,
    backgroundColor: dataset.color || chartColors.palette[index],
    borderColor: (dataset.color || chartColors.palette[index]).replace('0.8', '1'),
    borderWidth: 1
  }));

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: processedDatasets
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: {
          stacked: true
        },
        y: {
          stacked: true,
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

/**
 * 建立混合圖表（收入支出 + 淨額趨勢）
 */
function createMixedChart(canvasId, labels, incomeData, expenseData, netData) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          type: 'bar',
          label: '收入',
          data: incomeData,
          backgroundColor: chartColors.income,
          borderColor: chartColors.income.replace('0.8', '1'),
          borderWidth: 1
        },
        {
          type: 'bar',
          label: '支出',
          data: expenseData,
          backgroundColor: chartColors.expense,
          borderColor: chartColors.expense.replace('0.8', '1'),
          borderWidth: 1
        },
        {
          type: 'line',
          label: '淨額',
          data: netData,
          borderColor: chartColors.net,
          backgroundColor: chartColors.net.replace('0.8', '0.1'),
          borderWidth: 3,
          tension: 0.4,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      ]
    },
    options: {
      ...defaultChartOptions,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

/**
 * 建立雷達圖（多維度分析）
 */
function createRadarChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const processedDatasets = datasets.map((dataset, index) => ({
    label: dataset.label,
    data: dataset.data,
    borderColor: dataset.color || chartColors.palette[index],
    backgroundColor: (dataset.color || chartColors.palette[index]).replace('0.8', '0.2'),
    borderWidth: 2,
    pointRadius: 3,
    pointHoverRadius: 5
  }));

  return new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: processedDatasets
    },
    options: {
      ...defaultChartOptions,
      scales: {
        r: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return '$' + value.toLocaleString();
            }
          }
        }
      }
    }
  });
}

/**
 * 更新圖表資料
 */
function updateChartData(chart, newLabels, newData) {
  chart.data.labels = newLabels;

  if (Array.isArray(newData[0])) {
    // 多個資料集
    newData.forEach((data, index) => {
      if (chart.data.datasets[index]) {
        chart.data.datasets[index].data = data;
      }
    });
  } else {
    // 單一資料集
    chart.data.datasets[0].data = newData;
  }

  chart.update();
}

/**
 * 銷毀圖表
 */
function destroyChart(chart) {
  if (chart) {
    chart.destroy();
  }
}

/**
 * 匯出圖表為圖片
 */
function exportChartAsImage(chart, filename = 'chart.png') {
  const url = chart.toBase64Image();
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
}

// 導出給全域使用
window.ChartUtils = {
  createPieChart,
  createDoughnutChart,
  createBarChart,
  createLineChart,
  createStackedBarChart,
  createMixedChart,
  createRadarChart,
  updateChartData,
  destroyChart,
  exportChartAsImage,
  chartColors,
  defaultChartOptions
};