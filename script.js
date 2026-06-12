let globalData = bbmData.filter(row => row.Tahun); // Filter row kosong
let bbmChart = null;

const CONST_UANG = 100000;

document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("year-slider");
    const fuelSelect = document.getElementById("fuel-type");
    
    // Atur batas Min & Max Slider berdasarkan dataset
    const years = globalData.map(d => d.Tahun);
    slider.min = Math.min(...years);
    slider.max = Math.max(...years);
    slider.value = Math.max(...years); // Default ke tahun terbaru

    // Inisialisasi awal
    initChart(fuelSelect.value);
    updateDashboard(slider.value, fuelSelect.value);

    // Event Listeners
    slider.addEventListener("input", (e) => {
        updateDashboard(e.target.value, fuelSelect.value);
    });

    fuelSelect.addEventListener("change", (e) => {
        // Sesuaikan slider batas minimum jika Pertamax (mulai 1999)
        if (e.target.value === "Pertamax") {
            const pertamaxYears = globalData.filter(d => d.Harga_Pertamax_Nominal > 0).map(d => d.Tahun);
            if(pertamaxYears.length > 0) {
                slider.min = Math.min(...pertamaxYears);
                if (parseInt(slider.value) < slider.min) {
                    slider.value = slider.min;
                }
            }
        } else {
            slider.min = Math.min(...years);
        }
        
        updateChart(e.target.value);
        updateDashboard(slider.value, e.target.value);
    });
});

function formatRupiah(number) {
    if (!number) return "Rp 0";
    return "Rp " + number.toLocaleString('id-ID');
}

function updateDashboard(year, fuelType) {
    year = parseInt(year);
    document.getElementById("year-display").innerText = year;

    const rowData = globalData.find(d => d.Tahun === year);
    if (!rowData) return;

    let hargaNominal = 0;
    let hargaReal = 0;

    if (fuelType === "Premium/Pertalite") {
        hargaNominal = rowData.Harga_Premium_Nominal;
        hargaReal = rowData.Harga_Premium_Real;
    } else if (fuelType === "Solar") {
        hargaNominal = rowData.Harga_Solar_Nominal;
        hargaReal = rowData.Harga_Solar_Real;
    } else if (fuelType === "Pertamax") {
        hargaNominal = rowData.Harga_Pertamax_Nominal;
        hargaReal = rowData.Harga_Pertamax_Real;
    }

    const eventText = rowData.Ringkasan_Event || "Estimasi harga stabil.";

    // Jika harga tidak tersedia untuk tahun tersebut
    if (!hargaNominal || hargaNominal === 0) {
        document.getElementById("price-nominal").innerText = "-";
        document.getElementById("price-real").innerText = "-";
        document.getElementById("history-context").innerHTML = `<span style="color:#e63946">Belum ada data untuk jenis BBM ini pada tahun ${year}.</span>`;
        document.getElementById("liter-result").innerText = "0 Liter";
        document.getElementById("motorcycle-result").innerText = `Setara dengan 0x isi full tangki motor`;
        document.getElementById("tank-liquid").style.height = `0%`;
        return;
    }

    // Update Teks DOM Kanan (Metrik & Konteks)
    document.getElementById("price-nominal").innerText = formatRupiah(hargaNominal);
    document.getElementById("price-real").innerText = formatRupiah(hargaReal);
    document.getElementById("history-context").innerText = eventText;

    // Kalkulasi Tangki Liter
    const volume = CONST_UANG / hargaNominal;
    document.getElementById("liter-result").innerText = volume.toFixed(1) + " Liter";
    
    const tangkiMotor = (volume / 4.2).toFixed(1);
    document.getElementById("motorcycle-result").innerText = `Setara dengan ${tangkiMotor}x isi full tangki motor`;

    // Ambil harga terendah dari jenis BBM yang dipilih sepanjang sejarah untuk skala maksimal
    let colName = 'Harga_Premium_Nominal';
    if (fuelType === "Solar") colName = 'Harga_Solar_Nominal';
    if (fuelType === "Pertamax") colName = 'Harga_Pertamax_Nominal';
    
    const validPrices = globalData.map(d => d[colName]).filter(v => v > 0);
    const minHargaAllTime = Math.min(...validPrices);
    const maxVolumeAllTime = CONST_UANG / minHargaAllTime;
    
    let heightPercent = (Math.sqrt(volume) / Math.sqrt(maxVolumeAllTime)) * 100;
    
    if (heightPercent < 5) heightPercent = 5;
    if (heightPercent > 100) heightPercent = 100;

    document.getElementById("tank-liquid").style.height = `${heightPercent}%`;
}

function extractChartData(fuelType) {
    const years = globalData.map(d => d.Tahun);
    let nominals = [];
    let reals = [];

    if (fuelType === "Premium/Pertalite") {
        nominals = globalData.map(d => d.Harga_Premium_Nominal);
        reals = globalData.map(d => d.Harga_Premium_Real);
    } else if (fuelType === "Solar") {
        nominals = globalData.map(d => d.Harga_Solar_Nominal);
        reals = globalData.map(d => d.Harga_Solar_Real);
    } else if (fuelType === "Pertamax") {
        nominals = globalData.map(d => d.Harga_Pertamax_Nominal);
        reals = globalData.map(d => d.Harga_Pertamax_Real);
    }

    return { years, nominals, reals };
}

function initChart(fuelType) {
    const ctx = document.getElementById('bbmChart').getContext('2d');
    const { years, nominals, reals } = extractChartData(fuelType);

    bbmChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [
                {
                    label: 'Harga Nominal (Riil)',
                    data: nominals,
                    borderColor: '#222222',
                    backgroundColor: 'rgba(34, 34, 34, 0.05)',
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#222222',
                    tension: 0.2
                },
                {
                    label: 'Daya Beli Setara Masa Kini (Inflasi)',
                    data: reals,
                    borderColor: '#4A8B6A',
                    backgroundColor: 'rgba(74, 139, 106, 0.05)',
                    borderWidth: 2.5,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#4A8B6A',
                    tension: 0.2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                tooltip: {
                    backgroundColor: '#FFFFFF',
                    titleColor: '#2C5545',
                    bodyColor: '#666666',
                    borderColor: '#E2E0D8',
                    borderWidth: 1,
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'Inter', size: 13 },
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += formatRupiah(context.parsed.y);
                            }
                            return label;
                        }
                    }
                },
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        font: { family: 'Inter', size: 13, weight: '600' },
                        color: '#666666',
                        usePointStyle: true,
                        boxWidth: 8
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { family: 'Inter', size: 12 },
                        color: '#999999',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    border: { display: false },
                    grid: {
                        color: '#E2E0D8',
                        drawTicks: false
                    },
                    ticks: {
                        font: { family: 'Inter', size: 12 },
                        color: '#999999',
                        callback: function(value) {
                            return 'Rp ' + (value / 1000) + 'k';
                        }
                    }
                }
            }
        }
    });
}

function updateChart(fuelType) {
    if (!bbmChart) return;
    const { nominals, reals } = extractChartData(fuelType);
    
    bbmChart.data.datasets[0].data = nominals;
    bbmChart.data.datasets[1].data = reals;
    bbmChart.update();
}
