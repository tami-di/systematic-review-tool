google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.load('current', {'packages':['corechart']});
// set chart to show


var barchart_category_name = ""
var barchart_data = ""
function set_bar_chart_data(category, visualization_name,data, is_year){
     barchart_category_name = category
     barchart_data = data
}

var piechart_category_name = ""
var piechart_data = ""
function set_pie_chart_data(category, visualization_name,data, is_year){
     piechart_category_name = category
     piechart_data = data
}

var linechart_category_name = ""
var linechart_data = ""
function set_line_chart_data(category, visualization_name,data, is_year){
     linechart_category_name = category
     linechart_data = data
}


function drawLineColors() {
      chartinfo = linechart_category_name.replace("_tested","")

      language = "en"
      if(chartinfo == "metric"){
        vgridlines = 20
        data_name = "metric"
        }
      else if(chartinfo == "model"){
        vgridlines = 14
        data_name = "models"}
      else if(chartinfo == "study"){
        vgridlines = 18
        data_name = "study"}
      else if(chartinfo=="network"){
        vgridlines = 19
        data_name = "network"
      }

      data_name = linechart_category_name.replace("_tested","")
      if(data_name == "model"){
            arrayData = []
            ordered_names = ["One to one like",
                              "Geometric\n or spatially\n embedded",
                              "Multiple dependencies",
                              "Coupled power grid",
                              "Load transfer among networks",
                              "Mixed interactions",
                              "Directed support-dependency",
                              "Mapping",
                              "Contagion or influence",
                              "Supply-chain",
                              "Defined by probabilities"
                              ]
            ordered_models = ["One to one like",
                              "Geometric or spatially embedded",
                              "Multiple dependencies",
                              "Coupled power grid",
                              "Load transfer among networks",
                              "Mixed interactions",
                              "Directed support-dependency",
                              "Mapping",
                              "Contagion or influence",
                              "Supply-chain",
                              "Defined by probabilities"]
            arrayData.push(["year",ordered_names[0],
                                    ordered_names[1],
                                    ordered_names[2],
                                    ordered_names[3],
                                    ordered_names[4],
                                    ordered_names[5],
                                    ordered_names[6],
                                    ordered_names[7],
                                    ordered_names[8],
                                    ordered_names[9],
                                    ordered_names[10]])
            var i;
            for(i = 2010;i < 2018;i++){
                console.log(i+"-"+linechart_data[i][ordered_models[0]])
                console.log(i+"-"+linechart_data[i][ordered_models[1]])
                console.log(i+"-"+linechart_data[i][ordered_models[2]])
                console.log(i+"-"+linechart_data[i][ordered_models[3]])
                console.log(i+"-"+linechart_data[i][ordered_models[4]])
                console.log(i+"-"+linechart_data[i][ordered_models[5]])
                console.log(i+"-"+linechart_data[i][ordered_models[6]])
                console.log(i+"-"+linechart_data[i][ordered_models[7]])
                console.log(i+"-"+linechart_data[i][ordered_models[8]])
                console.log(i+"-"+linechart_data[i][ordered_models[9]])
                console.log(i+"-"+linechart_data[i][ordered_models[10]])
                arrayData.push([i,linechart_data[i][ordered_models[0]],
                                linechart_data[i][ordered_models[1]],
                                linechart_data[i][ordered_models[2]],
                                linechart_data[i][ordered_models[3]],
                                linechart_data[i][ordered_models[4]],
                                linechart_data[i][ordered_models[5]],
                                linechart_data[i][ordered_models[6]],
                                linechart_data[i][ordered_models[7]],
                                linechart_data[i][ordered_models[8]],
                                linechart_data[i][ordered_models[9]],
                                linechart_data[i][ordered_models[10]]])
            }


      }
      if(data_name == "metric"){
            arrayData = []
            ordered_names = ["Counting elements",
                              "Breaking point",
                              "Time",
                              "Probability",
                              "Rate",
                              "Cost",
                              "Path length",
                              "Performance"]
            ordered_models = ["Counting elements",
                              "Breaking point",
                              "Time",
                              "Probability",
                              "Rate",
                              "Cost",
                              "Path length",
                              "Performance"]
            arrayData.push(["year",ordered_names[0],
                                    ordered_names[1],
                                    ordered_names[2],
                                    ordered_names[3],
                                    ordered_names[4],
                                    ordered_names[5],
                                    ordered_names[6],
                                    ordered_names[7]])
            var i;
            for(i = 2010;i < 2018;i++){

                arrayData.push([i,linechart_data[i][ordered_models[0]],
                                linechart_data[i][ordered_models[1]],
                                linechart_data[i][ordered_models[2]],
                                linechart_data[i][ordered_models[3]],
                                linechart_data[i][ordered_models[4]],
                                linechart_data[i][ordered_models[5]],
                                linechart_data[i][ordered_models[6]],
                                linechart_data[i][ordered_models[7]]])
            }

      }
      if(data_name == "study"){
            arrayData = []
            ordered_names = ["Size of the giant connected component",
                              "Coupling",
                              "Percolation",
                              "Targeted attacks",
                              "Load and capacity",
                              "Cascading time",
                              "Length",
                              "Avalanche"]
            ordered_models = ["Size of the giant connected component",
                              "Coupling",
                              "Percolation",
                              "Targeted attacks",
                              "Load and capacity",
                              "Cascading time",
                              "Length",
                              "Avalanche"]
            arrayData.push(["year",ordered_names[0],
                                    ordered_names[1],
                                    ordered_names[2],
                                    ordered_names[3],
                                    ordered_names[4],
                                    ordered_names[5],
                                    ordered_names[6],
                                    ordered_names[7]])
            var i;
            for(i = 2010;i < 2018;i++){

                arrayData.push([i,linechart_data[i][ordered_models[0]],
                                linechart_data[i][ordered_models[1]],
                                linechart_data[i][ordered_models[2]],
                                linechart_data[i][ordered_models[3]],
                                linechart_data[i][ordered_models[4]],
                                linechart_data[i][ordered_models[5]],
                                linechart_data[i][ordered_models[6]],
                                linechart_data[i][ordered_models[7]]])
            }

      }
      if(data_name == "network"){
            arrayData = []
            ordered_names = ["Simulated",
                              "Real and simulated"]
            ordered_models = ["simulated",
                              "both"]
            arrayData.push(["year",ordered_names[0],
                                    ordered_names[1]])
            var i;
            for(i = 2010;i < 2018;i++){
                arrayData.push([i,linechart_data[i][ordered_models[0]],
                                linechart_data[i][ordered_models[1]]])
            }

      }

      // this new DataTable object holds all the data
      var data = new google.visualization.arrayToDataTable(arrayData);
      // CAPACITY - En-route ATFM delay - YY - CHART
      var crt_ertdlyYY = new google.visualization.ChartWrapper({
         chartType: 'LineChart',
         containerId: 'chart_div',
         dataTable: data,
         options:{
            hAxis: {
                title: 'Year',
                gridlines: {count:7},
                format: ''
            },
            vAxis: {
                title: 'Amount of papers using each kind of '+data_name,
                gridlines: {count:vgridlines}
            },
            colors: ['#41b6c4','#fe9929','#980043','#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a'],
            title: 'Number of papers using each kind of '+data_name+' per year',
            width: 1300,
            height: 700,
            chartArea:{width:'65.8%'},
            pointShape:'circle',
            pointSize: '6'
         }
      });
      crt_ertdlyYY.draw();
}


function drawPieChart() {

        var data = google.visualization.arrayToDataTable([
          ['Task', 'Hours per Day'],
          ['Simulated',     piechart_data['simulated']],
          ['Real and simulated',      piechart_data['both']]
        ]);

        var options = {
          title: '% of paper using each kind of network',
          colors: ['#41b6c4','#fe9929','#980043','#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a'],
          width: 700,
          height: 700
        };

        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }

function drawBarChartForCorrelations() {
    monotone = false
    colors = ['#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a']
    if(monotone){
        colors = ['#1b9e77','#1b9e77','#1b9e77','#1b9e77','#1b9e77','#1b9e77','#1b9e77','#1b9e77']
    }
    total = 57.0
    var data = google.visualization.arrayToDataTable([
        ['Escenario','Número de artículos',{ role: 'style' }, { role: 'annotation' }],
        ['Modelo: Tipo one to one\nMétrica: Cantidad\nEstudio: Tamaño de la componente gigante\n Datos: Simulados',9*100/total,colors[0],""+(9*100/total).toFixed(1)],
        ['Modelo: Tipo one to one\nMétrica: Punto de quiebre\nEstudio: Tamaño de la componente gigante\n Datos: Simulados',7*100/total,colors[1],""+(7*100/total).toFixed(1)],
        ['Modelo: Tipo one to one\nMétrica: Punto de quiebre\nEstudio: percolación\n Datos: Simulados',6*100/total,colors[2],""+(6*100/total).toFixed(1)],
        ['Modelo: Tipo one to one\nMétrica: Cantidad\nEstudio: Acoplamiento\n Datos: Simulados',6*100/total,colors[3],""+(6*100/total).toFixed(1)],
        ['Modelo: Tipo one to one\nMétrica: Cantidad\nEstudio: Ataques intencionales\n Datos: Simulados',5*100/total,colors[4],""+(5*100/total).toFixed(1)]
    ])
    var options = {
        //  colors: ['#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a'],
          title: '',
          width: 2000,//1000,
          height: 1500,//1000,
          legend: { position: "none" },
          vAxis: { maxValue: 100, title:'Porcentaje de artículos publicados por escenario'},
          //vAxis: { maxValue: 100, title:'Porcentaje de artículos que utilizaron cada tipo de '+chartinfo},
          chartArea:{height:'50%'}
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}


function drawBarChart() {
        chartinfo_eng = barchart_category_name
        colors = ['#41b6c4','#fe9929','#980043','#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a']
        total = 102.0
        var data_networks= ""
        var data_models = ""
        var data_time = ""
        var data_metrics = ""
        var data_studies = ""


        if (barchart_category_name == "time"){

            var time_list = [['Year', '% of papers',{ role: 'style' }, { role: 'annotation' }]]
            i = 0
            var key = 0;
            for(key = 2005;key < 2017;key++) {
                var pair = barchart_data[key]

                time_list.push([String(key),pair*100/total,colors[0],""+(pair*100/total).toFixed(1)])
                //time_list.push([String(key),pair,colors[0],""+pair])
                i += 1
            }
            var data_time = google.visualization.arrayToDataTable(time_list)
        }

        barchart_data = order_dict_by_value(barchart_data)

        if (barchart_category_name == "model"){

            var model_list = [['Model type', '% of papers',{ role: 'style' }, { role: 'annotation' }]]
            i = 0
            for(var key in barchart_data) {
                var pair = barchart_data[key]
                model_list.push([pair[0],pair[1]*100/total,colors[i%8],""+(pair[1]*100/total).toFixed(1)])
                i += 1
            }
            var data_models = google.visualization.arrayToDataTable(model_list)
        }

        if (barchart_category_name == "metric"){

            var metric_list = [['Metric type', '% of papers',{ role: 'style' }, { role: 'annotation' }]]
            i = 0
            for(var key in barchart_data) {
                var pair = barchart_data[key]
                metric_list.push([pair[0],pair[1]*100/total,colors[i%8],""+(pair[1]*100/total).toFixed(1)])
                i += 1
            }
            var data_metrics = google.visualization.arrayToDataTable(metric_list)
        }

        if (barchart_category_name == "study"){

            var studies_list = [['Studies', '% of papers',{ role: 'style' }, { role: 'annotation' }]]
            i = 0
            for(var key in barchart_data) {
                var pair = barchart_data[key]
                studies_list.push([pair[0],pair[1]*100/total,colors[i%8],""+(pair[1]*100/total).toFixed(1)])
                i += 1
            }
            var data_studies = google.visualization.arrayToDataTable(studies_list)
        }







        var vaxis;
        if(chartinfo_eng == "time"){
            vaxis= { maxValue: 100, title:'% of papers published per year'}
          }else{
          //,
          vaxis= { maxValue: 100, title:'% of papers using each kind of '+chartinfo_eng}}

        var options = {
        //  colors: ['#1b9e77', '#d95f02','#7570b3','#666666','#66a61e','#e6ab02','#a6761d','#e7298a'],
          title: '',
          width: 1400,//1400,
          height: 900,//1000,
          legend: { position: "none" },
          vAxis: vaxis ,
          chartArea:{height:'50%'}
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        if(chartinfo_eng == "metric"){
          data = data_metrics}
        else if(chartinfo_eng == "model"){
          data = data_models}
        else if(chartinfo_eng == "study"){
          data = data_studies
        }else if (chartinfo_eng=="time"){
          data= data_time
        }
        chart.draw(data, options);
}

function order_dict_by_value(dict){
    var items = Object.keys(dict).map(function(key) {
                    return [key, dict[key]];
                });

    items.sort(function(first, second) {
            return second[1] - first[1];
        });
    return items
}