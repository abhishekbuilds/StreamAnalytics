const btcVolumeCtx = document.getElementById('btcVolumeChart').getContext('2d');
const ethVolumeCtx = document.getElementById('ethVolumeChart').getContext('2d');
const priceComparisonCtx = document.getElementById('priceComparisonChart').getContext('2d');
const tradeCountCtx = document.getElementById('tradeCountChart').getContext('2d');
const btcAvgPriceLogCtx = document.getElementById('btcAvgPriceLogChart').getContext('2d');
const ethAvgPriceLogCtx = document.getElementById('ethAvgPriceLogChart').getContext('2d');

function toPST(date) {
    const userTimezoneOffset = date.getTimezoneOffset() * 60000;
    const pstOffset = 480;
    return new Date(date.getTime() - userTimezoneOffset - pstOffset * 60000);
}


let btcVolumeChart = new Chart(btcVolumeCtx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [
            {
                label: 'BTC Average Volume',
                data: [],
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Average Volume'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        }
    }
});

let ethVolumeChart = new Chart(ethVolumeCtx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [
            {
                label: 'ETH Average Volume',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Average Volume'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        }
    }
});

let priceComparisonChart = new Chart(priceComparisonCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'BTC Average Price',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                fill: false
            },
            {
                label: 'ETH Average Price',
                data: [],
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Average Price in USD'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        },
        plugins: {
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'x'
                },
                zoom: {
                    wheel: {
                        enabled: true
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'x'
                }
            }
        }
    }
});

let tradeCountChart = new Chart(tradeCountCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'BTC Trade Count',
                data: [],
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1,
                fill: false
            },
            {
                label: 'ETH Trade Count',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Trade Counts'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        }
    }
});

let btcAvgPriceLogChart = new Chart(btcAvgPriceLogCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'BTC Price',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            y: {
                type: 'logarithmic',
                position: 'left',
                title: {
                    display: true,
                    text: 'Price'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true
    }
});

let ethAvgPriceLogChart = new Chart(ethAvgPriceLogCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'ETH Price',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            y: {
                type: 'logarithmic',
                position: 'left',
                title: {
                    display: true,
                    text: 'Price'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true
    }
});

function updateCharts(dataBTC, dataETH) {
    // Update BTC chart
    btcVolumeChart.data.labels = dataBTC.map(item => {
        const date = new Date(item.window_start);
        date.setHours(date.getHours() - 8);
        return date.toLocaleTimeString('en-US', { hour12: true });
    });
    btcVolumeChart.data.datasets[0].data = dataBTC.map(item => item.average_volume);
    btcVolumeChart.update();

    // Update ETH chart
    ethVolumeChart.data.labels = dataETH.map(item => {
        const date = new Date(item.window_start);
        date.setHours(date.getHours() - 8);
        return date.toLocaleTimeString('en-US', { hour12: true });
    });
    ethVolumeChart.data.datasets[0].data = dataETH.map(item => item.average_volume);
    ethVolumeChart.update();

    if (dataBTC.length > 0 && dataETH.length > 0) {
        priceComparisonChart.data.labels = dataBTC.map(item => {
            const date = new Date(item.window_start);
            date.setHours(date.getHours() - 8);
            return date.toLocaleTimeString('en-US', { hour12: true });
        });
        priceComparisonChart.data.datasets[0].data = dataBTC.map(item => item.average_price);
        priceComparisonChart.data.datasets[1].data = dataETH.map(item => item.average_price);
        priceComparisonChart.update();
    }

    if (dataETH.length > 0 && dataETH.length > 0) {
        tradeCountChart.data.labels = dataBTC.map(item => {
            const date = new Date(item.window_start);
            date.setHours(date.getHours() - 8);
            return date.toLocaleTimeString('en-US', { hour12: true });
        });
        tradeCountChart.data.datasets[0].data = dataBTC.map(item => item.trade_count);
        tradeCountChart.data.datasets[1].data = dataETH.map(item => item.trade_count);
        tradeCountChart.update();
    }

    btcAvgPriceLogChart.data.labels = dataBTC.map(item => {
        const date = new Date(item.window_start);
        date.setHours(date.getHours() - 8);
        return date.toLocaleTimeString('en-US', { hour12: true });
    });
    btcAvgPriceLogChart.data.datasets[0].data = dataBTC.map(item => item.average_price);
    btcAvgPriceLogChart.update();

    ethAvgPriceLogChart.data.labels = dataETH.map(item => {
        const date = new Date(item.window_start);
        date.setHours(date.getHours() - 8);
        return date.toLocaleTimeString('en-US', { hour12: true });
    });
    ethAvgPriceLogChart.data.datasets[0].data = dataETH.map(item => item.average_price);
    ethAvgPriceLogChart.update();
}

function ajaxCall() {
    fetch('http://localhost:5001/latestData')
        .then(response => response.json())
        .then(data => {
            if (data['BINANCE:BTCUSDT'] && data['BINANCE:ETHUSDT']) {
                updateCharts(data['BINANCE:BTCUSDT'], data['BINANCE:ETHUSDT']);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

ajaxCall();

setInterval(ajaxCall, 1000);