function drawPatientsStats(labels, data, colors) {
    const ctx = document.getElementById('patientsStats');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số bệnh nhân',
                data: data,
                borderWidth: 1,
                backgroundColor: colors
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
function drawMedicinesStats(labels, data, colors) {
    const ctx = document.getElementById('medicinesStats');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng sử dụng',
                data: data,
                borderWidth: 1,
                backgroundColor: colors
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function drawRevenueStats(labels, data, colors) {
    const ctx = document.getElementById('revenueStats');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'đồng',
                data: data,
                borderWidth: 1,
                backgroundColor: colors

            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}