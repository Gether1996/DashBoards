var dashboardSlug = document.getElementById('dashboard-slug').textContent.trim();
var submitBtn = document.getElementById('submit-btn')
var dataInput = document.getElementById('data-input')
var user = document.getElementById('user').textContent.trim()
var dataBox = document.getElementById('data-box')

var socket = new WebSocket(`ws://${window.location.host}/ws/stats/${dashboardSlug}/`);
console.log(socket);

socket.onopen = function(e) {
    console.log('WebSocket connection opened.');
};

submitBtn.addEventListener('click', ()=> {
    var dataValue = dataInput.value
    socket.send(JSON.stringify({
        'message': dataValue,
        'sender': user,
    }));
})

socket.onmessage = function(e) {
    var {sender, message} = JSON.parse(e.data)
    updateChart()

    dataBox.innerHTML += `<p>${sender}: ${message}</p>`
};

socket.onclose = function(e) {
    console.log('WebSocket connection closed.');
};

socket.onerror = function(e) {
    console.error('WebSocket error:', e);
};

var ctx = document.getElementById('myChart').getContext('2d');
let chart;

var fetchChartData = async () => {
    var response = await fetch(window.location.href + 'chart/');
    var data = await response.json();
    console.log(data);
    return data;
};

var drawChart = async () => {
    var data = await fetchChartData();
    var { chartData, chartLabels } = data;

    chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartLabels,
            datasets: [{
                label: '% of contribution',
                data: chartData,
                borderWidth: 1,
            }],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
};

var updateChart = async() => {
    if (chart) {
        chart.destroy()
    }

    await drawChart()
}

drawChart();

addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        document.getElementById('submit-btn').click();
        document.getElementById('data-input').value = '';
    }
});