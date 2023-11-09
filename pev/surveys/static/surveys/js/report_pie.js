$(function () {

    var $surveyChart = $("#vote-chart");
    $.ajax({
        url: $.data("url"),
        success: function (data) {

            var ctx = $surveyChart[0].getContext("2d");

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Vote',
                        backgroundColor: 'blue',
                        data: data.data
                    }]
                },

                options: {
                    responsive: true,
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Vote Chart'
                    }
                }
            });

        }
    });

});