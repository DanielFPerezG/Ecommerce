Chart.register(ChartDataLabels);
/*-----------------Donut Chart Cupon-------------------------------*/

var DoughnutChartCuponCanvas = document.getElementById('DoughnutChartCupon').getContext('2d');
    var DoughnutCuponData = {
        type: 'doughnut',
        labels: DoughnutChartCuponLabels,
        datasets: [
            {
                data: DoughnutChartCuponData,
                backgroundColor: DoughnutChartCuponBackgroundColor,
                borderColor: DoughnutChartCuponBorderColor,
            }
        ]
    }

    var DoughnutCuponOptions     = {
        maintainAspectRatio: false,
        responsive: true,
        animation: {
        animateScale: true,
        animateRotate: true
    },
    tooltips: {
        enabled: true
    },
    legend: {
        display: true,
        position: 'top'
    },
        plugin: [ChartDataLabels]
    }

    var DoughnutChartCupon = new Chart(DoughnutChartCuponCanvas, {
    type: 'doughnut',
    data: DoughnutCuponData,
    options: DoughnutCuponOptions
    })

/*-----------------Bar Chart Topic-------------------------------*/

var barChartTopicCanvas = document.getElementById('barChartTopic').getContext('2d');

// Define las variables fuera de la función
var barChartTopicData = {
    type: 'bar',
    labels: barChartTopicLabels,
    datasets: [
        {
            data: barChartTopicProductData,
            backgroundColor: barChartTopicBackgroundColor,
            borderColor: barChartTopicBorderColor,
            borderWidth: 1
        }
    ]
};

var barChartTopicOptions = {
    maintainAspectRatio: false,
    responsive: true,
    animation: {
        animateScale: true,
        animateRotate: true
    },
    tooltips: {
        enabled: true
    },
    plugins: {
        legend: {
            display: false
        }
    },
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

var barChartTopic = new Chart(barChartTopicCanvas, {
    type: 'bar',
    data: barChartTopicData,
    options: barChartTopicOptions
});

// Define la función para actualizar el gráfico
function updateBarChart(chartType) {
    var newLabels, newData;

    // Determina los nuevos datos según el tipo de gráfico seleccionado
    if (chartType === 'profit') {
        newLabels = barChartTopicProfitLabels;
        newData = barChartTopicProfitData;
    } else {
        newLabels = barChartTopicLabels;
        newData = barChartTopicProductData;
    }

    // Actualiza los datos del gráfico
    barChartTopic.data.labels = newLabels;
    barChartTopic.data.datasets[0].data = newData;

    // Vuelve a renderizar el gráfico
    barChartTopic.update();
}


/*-----------------Bar Chart Profit-------------------------------*/
var barChartProfitCanvas = document.getElementById('barChartProfit').getContext('2d');

var barChartProfitData = {
        type: 'bar',
        labels: barChartProfitTopic,
        datasets: [
            {
                label: 'Ingresos',
                data: barChartProfitRevenue,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
            },
            {
                label: 'Gastos',
                data: barChartProfitCost,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
            },
            {
                label: 'Ingresos Brutos',
                data: barChartProfitProfit,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
            },
        ]
    }

    var barChartProfitOptions     = {
        maintainAspectRatio: false,
        responsive: true,
        animation: {
        animateScale: true,
        animateRotate: true
    },
    tooltips: {
        enabled: true
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        display: false,
        stacked: true
      }
    },
    legend: {
        display: true,
        position: 'top'
    },
        plugin: [ChartDataLabels]
    }

    var barChartProfit = new Chart(barChartProfitCanvas, {
    type: 'bar',
    data: barChartProfitData,
    options: barChartProfitOptions
    })

/*-----------------Line Chart Orders By Day-------------------------------*/
var dailyOrderChartCanvas = document.getElementById('dailyOrderChart').getContext('2d');

var dailyOrderChartData = {
        type: 'line',
        labels: dailyOrderChartLabels,
        datasets: [
            {
                label: 'Ordenes',
                data: dailyOrderChartData,
                borderColor: dailyOrderChartBorderColor,
            }
        ]
    }

    var dailyOrderChartOptions     = {
        maintainAspectRatio: false,
        responsive: true,
        animation: {
        animateScale: true,
        animateRotate: true
    },
    tooltips: {
        enabled: true
    },
    legend: {
        display: true,
        position: 'top'
    },
    scales: {
        y: {
            suggestedMin: 0, // Establece el valor mínimo del eje Y a 0
            beginAtZero: true, // Esto también asegura que comience en 0
        }
    },
        plugins: {
    datalabels: {
      anchor: 'end',
      align: 'top',
      // otras opciones del plugin
    }
  }
    }

    var dailyOrderChart = new Chart(dailyOrderChartCanvas, {
    type: 'line',
    data: dailyOrderChartData,
    options: dailyOrderChartOptions
    })