//main.js
angular
.module('app')
.controller('cardChartCtrl1', cardChartCtrl1)
.controller('cardChartCtrl2', cardChartCtrl2)
.controller('cardChartCtrl3', cardChartCtrl3)
.controller('cardChartCtrl4', cardChartCtrl4)
.controller('trafficDemoCtrl', trafficDemoCtrl)
.controller('socialBoxCtrl', socialBoxCtrl)
.controller('sparklineChartCtrl', sparklineChartCtrl)
.controller('barChartCtrl', barChartCtrl)
.controller('horizontalBarsCtrl', horizontalBarsCtrl)
.controller('horizontalBarsType2Ctrl', horizontalBarsType2Ctrl)
.controller('userInfoCtrl', userInfoCtrl)
.controller('usersTableCtrl', usersTableCtrl);

//convert Hex to RGBA
function convertHex(hex,opacity){
  hex = hex.replace('#','');
  r = parseInt(hex.substring(0,2), 16);
  g = parseInt(hex.substring(2,4), 16);
  b = parseInt(hex.substring(4,6), 16);

  result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
  return result;
}

cardChartCtrl1.$inject = ['$scope'];
function cardChartCtrl1($scope) {

  $.getJSON("/getUserGroups", getUserGroups);

  data = [];

  function getUserGroups(groups) {
    //staff = groups['staff'];
    data = [ groups['tek1'],  groups['tek1'],  groups['tek1'],  groups['tek1'], groups['tek1'], groups['tek1'], groups['tek1']]
    $scope.tek1 = groups['tek1'];
  }

  $scope.labels = ['Monday','Tuesday','Wednesday','Thursay','Friday','Saturday','Sunday'];
  $scope.data = data;

  $scope.colors = [{
    backgroundColor: brandPrimary,
    borderColor: 'rgba(255,255,255,.55)',
  }];
  $scope.options = {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        gridLines: {
          color: 'transparent',
          zeroLineColor: 'transparent'
        },
        ticks: {
          fontSize: 2,
          fontColor: 'transparent',
        }

      }],
      yAxes: [{
        display: false,
        ticks: {
          display: false,
          min: Math.min.apply(Math, $scope.data[0]) - 5,
          max: Math.max.apply(Math, $scope.data[0]) + 5,
        }
      }],
    },
    elements: {
      line: {
        borderWidth: 1
      },
      point: {
        radius: 4,
        hitRadius: 10,
        hoverRadius: 4,
      },
    },
  }
}

cardChartCtrl2.$inject = ['$scope'];
function cardChartCtrl2($scope) {

  $.getJSON("/getUserGroups", getUserGroups);

  data = [];

  function getUserGroups(groups) {
    //staff = groups['staff'];
    data = [ groups['tek2'],  groups['tek2'],  groups['tek2'],  groups['tek2'], groups['tek2'], groups['tek2'], groups['tek2']]
    $scope.tek2 = groups['tek2'];
  }

  $scope.labels = ['Monday','Tuesday','Wednesday','Thursay','Friday','Saturday','Sunday'];
  $scope.data = data;

  $scope.colors = [{
    backgroundColor: brandInfo,
    borderColor: 'rgba(255,255,255,.55)',
  }];
  $scope.options = {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        gridLines: {
          color: 'transparent',
          zeroLineColor: 'transparent'
        },
        ticks: {
          fontSize: 2,
          fontColor: 'transparent',
        }

      }],
      yAxes: [{
        display: false,
        ticks: {
          display: false,
          min: Math.min.apply(Math, $scope.data[0]) - 5,
          max: Math.max.apply(Math, $scope.data[0]) + 5
        }
      }],
    },
    elements: {
      line: {
        tension: 0.00001,
        borderWidth: 1
      },
      point: {
        radius: 4,
        hitRadius: 10,
        hoverRadius: 4,
      },

    },
  }
}

cardChartCtrl3.$inject = ['$scope'];
function cardChartCtrl3($scope) {

  $.getJSON("/getUserGroups", getUserGroups);

  data = [];

  function getUserGroups(groups) {
    //staff = groups['staff'];
    data = [ groups['tek3'],  groups['tek3'],  groups['tek3'],  groups['tek3'], groups['tek3'], groups['tek3'], groups['tek3']]
    $scope.tek3 = groups['tek3'];
  }

  $scope.labels = ['Monday','Tuesday','Wednesday','Thursay','Friday','Saturday','Sunday'];
  $scope.data = data;

  $scope.data4 = [
    [35, 23, 56, 22, 97, 23, 64]
  ];
  $scope.colors = [{
    backgroundColor: 'rgba(255,255,255,.2)',
    borderColor: 'rgba(255,255,255,.55)',
  }];
  $scope.options = {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        display: false
      }],
      yAxes: [{
        display: false
      }]
    },
    elements: {
      line: {
        borderWidth: 2
      },
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
      },
    },
  }
}

function random(min,max) {
  return Math.floor(Math.random()*(max-min+1)+min);
}

cardChartCtrl4.$inject = ['$scope'];
function cardChartCtrl4($scope) {

  var elements = 16;
  var labels = [];
  var data = [];
  //
  //for (var i = 2000; i <= 2000 + elements; i++) {
  //  labels.push(i);
  //  data.push(random(40,100));
  //}
  $.getJSON("/getUserGroups", getUserGroups);

  function getUserGroups(groups) {
    //staff = groups['staff'];
    data = [ groups['staff'],  groups['staff'],  groups['staff'],  groups['staff'], groups['staff'], groups['staff'], groups['staff']]
    $scope.staff = groups['staff'];
  }

  $scope.labels = ['Monday','Tuesday','Wednesday','Thursay','Friday','Saturday','Sunday'];

  $scope.data = data;

  $scope.colors = [{
    backgroundColor: 'rgba(255,255,255,.3)',
    borderWidth: 0
  }];
  $scope.options = {
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        display: false,
        barPercentage: 0.6,
      }],
      yAxes: [{
        display: false
      }]
    },
  }
}

trafficDemoCtrl.$inject = ['$scope'];
function trafficDemoCtrl($scope){

  $scope.date = moment().format('MM/DD/YYYY');

  function newDate(days) {
    return moment().add(days, 'd').toDate();
  }

  function newDateString(days) {
    return moment().add(days, 'd').format();
  }

  function random(min,max) {
    return Math.floor(Math.random()*(max-min+1)+min);
  }

  var elements = 27;
  var data1 = [];
  var data2 = [];
  var data3 = [];



  $.getJSON("/dashboardlogs", setDataPoints);


  var dataPoints = [];
  var dataLabels = [];
  var dataValue = [];
  function setDataPoints(data) {

    for (var i = 0; i < data.length; i++) {
      y = 0
      if (data[i].active){
        y = 1
      }
      //console.log(newDate(data[i].timestamp))
      dataPoints.push({
      //x: moment(data[i].timestamp).utcOffset('+0200'),
      x: data[i].timestamp,
      y: y
      });
      dataLabels.push(moment(data[i].timestamp).utcOffset('+0100').format('HH:mm'));
      dataValue.push(y);
    }

    $scope.dataPoints = dataPoints;
  }

  function updateDataPoints(data) {
    $.getJSON("/dashboardlogs", setDataPoints);
  }

  var interval = setInterval(updateDataPoints, 30000);

  for (var i = 0; i <= elements; i++) {
    data1.push(random(150,250));
    data2.push(random(65,75));
    data3.push(65);
  }

  $scope.labelsX = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Thursday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  $scope.series = ['Current', 'Previous', 'BEP'];
  $scope.newSeries = ['Log'];
  $scope.data = [ data1, data2, data3];
  $scope.dataLabels = dataLabels;
  $scope.dataValue = dataValue;

  $scope.colors = ['blue'];
  $scope.options = {
    responsive: true,
    title: {
      display: true,
      text: 'Activity Log'
    },
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        gridLines: {
          drawOnChartArea: false,
        },
        ticks: {
          callback: function(value) {
            return value;
          }
        }
      }],
      yAxes: [{
        ticks: {
          major: {
            fontStyle: 'bold',
            fontColor: '#20a8d8'
          },
          callback:  function(value, index, values) {
                  if (value == 0){
                   return 'Inactive';
                  }
                 if (value == 1){
                    return 'Active';
                  }
          }				                      
        }
      }]
    },
    elements: {
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3,
      }
    },
  }
}

dateRangeCtrl.$inject = ['$scope'];
function dateRangeCtrl($scope) {
  $scope.date = {
    startDate: moment().subtract(5, 'days'),
    endDate: moment()
  };
  $scope.opts = {
    drops: 'down',
    opens: 'left',
    ranges: {
      'Today': [moment(), moment()],
      'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
      'Last 7 days': [moment().subtract(7, 'days'), moment()],
      'Last 30 days': [moment().subtract(30, 'days'), moment()],
      'This month': [moment().startOf('month'), moment().endOf('month')]
    }
  };

  //Watch for date changes
  $scope.$watch('date', function(newDate) {
    //console.log('New date set: ', newDate);
  }, false);

  function gd(year, month, day) {
    return new Date(year, month - 1, day).getTime();
  }
}

socialBoxCtrl.$inject = ['$scope'];
function socialBoxCtrl($scope) {

  $scope.labels = ['January','February','March','April','May','June','July'];
  $scope.data1 = [
    [65, 59, 84, 84, 51, 55, 40]
  ];
  $scope.data2 = [
    [1, 13, 9, 17, 34, 41, 38]
  ];
  $scope.data3 = [
    [78, 81, 80, 45, 34, 12, 40]
  ];
  $scope.data4 = [
    [35, 23, 56, 22, 97, 23, 64]
  ];
  $scope.colors = [{
    backgroundColor: 'rgba(255,255,255,.1)',
    borderColor: 'rgba(255,255,255,.55)',
    pointHoverBackgroundColor: '#fff'
  }];
  $scope.options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      xAxes: [{
        display:false,
      }],
      yAxes: [{
        display:false,
      }]
    },
    elements: {
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3,
      }
    },
  }
}

sparklineChartCtrl.$inject = ['$scope'];
function sparklineChartCtrl($scope) {
  $scope.labels = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
  $scope.data1 = [
    [65, 59, 84, 84, 51, 55, 40]
  ];
  $scope.data2 = [
    [1, 13, 9, 17, 34, 41, 38]
  ];
  $scope.data3 = [
    [78, 81, 80, 45, 34, 12, 40]
  ];
  $scope.data4 = [
    [35, 23, 56, 22, 97, 23, 64]
  ];
  $scope.default = [{
    backgroundColor: 'transparent',
    borderColor: '#d1d4d7',
  }];
  $scope.primary = [{
    backgroundColor: 'transparent',
    borderColor: brandPrimary,
  }];
  $scope.info = [{
    backgroundColor: 'transparent',
    borderColor: brandInfo,
  }];
  $scope.danger = [{
    backgroundColor: 'transparent',
    borderColor: brandDanger,
  }];
  $scope.warning = [{
    backgroundColor: 'transparent',
    borderColor: brandWarning,
  }];
  $scope.success = [{
    backgroundColor: 'transparent',
    borderColor: brandSuccess,
  }];
  $scope.options = {
    scales: {
      xAxes: [{
        display:false,
      }],
      yAxes: [{
        display:false,
      }]
    },
    elements: {
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
        hoverBorderWidth: 3,
      }
    },
  }
}

horizontalBarsCtrl.$inject = ['$scope'];
function horizontalBarsCtrl($scope) {

  $scope.data = [
    {
      day: 'Monday',    new: 5, recurring: 90
    },
    {
      day: 'Tuesday',   new: 56, recurring: 94
    },
    {
      day: 'Wednesday', new: 12, recurring: 67
    },
    {
      day: 'Thursday',  new: 43, recurring: 91
    },
    {
      day: 'Friday',    new: 22, recurring: 73
    },
    {
      day: 'Saturday',  new: 53, recurring: 82
    },
    {
      day: 'Sunday',    new: 9,  recurring: 69
    }
  ];

}

horizontalBarsType2Ctrl.$inject = ['$scope'];
function horizontalBarsType2Ctrl($scope) {

  $scope.gender = [
    {
      title: 'Male',
      icon: 'icon-user',
      value: 43
    },
    {
      title: 'Female',
      icon: 'icon-user-female',
      value: 37
    },
  ];

  $scope.source = [
    {
      title: 'Organic Search',
      icon: 'icon-globe',
      value: 191235,
      percent: 56
    },
    {
      title: 'Facebook',
      icon: 'icon-social-facebook',
      value: 51223,
      percent: 15
    },
    {
      title: 'Twitter',
      icon: 'icon-social-twitter',
      value: 37564,
      percent: 11
    },
    {
      title: 'LinkedIn',
      icon: 'icon-social-linkedin',
      value: 27319,
      percent: 8
    }
  ];
}

usersTableCtrl.$inject = ['$scope', '$timeout'];
function usersTableCtrl($scope, $timeout) {

  $.getJSON("/activity", getActivity);
  users = []
  function getActivity(activity) {

    for (var i = 0; i < activity['data'].length; i++) {
        if (activity['data'][i]['active'] == false){
          activity['data'][i]['status'] = 'offline';
        }
        else{
          activity['data'][i]['status'] = 'active';
        }
        activity['data'][i]['activity'] = '10 sec ago';
        activity['data'][i]['usage'] = '50';
        activity['data'][i]['period'] = 'Jun 11, 2015 - Jul 10, 2015';

        if (activity['data'][i]['email'] != activity['email']){
          users.push(activity['data'][i]);
        }
    }

  }
  $scope.users = users;
}

userInfoCtrl.$inject = ['$scope', '$timeout'];
function userInfoCtrl($scope, $timeout) {

  $.getJSON("/userInfo", getuserInfo);

  userInfo = []

  function getuserInfo(data) {
    //console.log("Inside User Info : ");
    $scope.userInfo = data[0];
    //console.log(data[0]);
  }

  //$scope.userInfo = userInfo;
  //console.log("User Info : ");
  //console.log($scope.userInfo)

}




clientsTableCtrl.$inject = ['$scope', '$timeout'];
function clientsTableCtrl($scope, $timeout) {

  $scope.users = [
    {
      avatar: '1.jpg',
      status: 'active',
      name: 'Yiorgos Avraamu',
      registered: 'Jan 1, 2015',
      activity: '10 sec ago',
      transactions: 189,
      comments: 72
    },
    {
      avatar: '2.jpg',
      status: 'busy',
      name: 'Avram Tarasios',
      registered: 'Jan 1, 2015',
      activity: '5 minutes ago',
      transactions: 156,
      comments: 76
    },
    {
      avatar: '3.jpg',
      status: 'away',
      name: 'Quintin Ed',
      registered: 'Jan 1, 2015',
      activity: '1 hour ago',
      transactions: 189,
      comments: 72
    },
    {
      avatar: '4.jpg',
      status: 'offline',
      name: 'Enéas Kwadwo',
      registered: 'Jan 1, 2015',
      activity: 'Last month',
      transactions: 189,
      comments: 72
    },
    {
      avatar: '5.jpg',
      status: 'active',
      name: 'Agapetus Tadeáš',
      registered: 'Jan 1, 2015',
      activity: 'Last week',
      transactions: 189,
      comments: 72
    },
    {
      avatar: '6.jpg',
      status: 'busy',
      name: 'Friderik Dávid',
      registered: 'Jan 1, 2015',
      activity: 'Yesterday',
      transactions: 189,
      comments: 72
    }
  ]
}

function random(min,max) {
  return Math.floor(Math.random()*(max-min+1)+min);
}

barChartCtrl.$inject = ['$scope'];
function barChartCtrl($scope) {

  var elements = 16;
  var labels = [];
  var data = [];
  var data1 = [];
  var data2 = [];

  for (var i = 0; i <= elements; i++) {
    labels.push('1');
    data.push(random(40,100));
    data1.push(random(20,100));
    data2.push(random(60,100));
  }

  $scope.labels = labels;

  $scope.data = [data];
  $scope.data1 = [data1];
  $scope.data2 = [data2];

  $scope.options = {
    showScale: false,
    scaleFontSize: 0,
    scaleShowGridLines: false,
    barStrokeWidth : 0,
    barBackground: 'rgba(221, 224, 229, 1)',

    // pointDot :false,
    // scaleLineColor: 'transparent',
  };

  $scope.colors = [{
    backgroundColor : brandInfo,
    borderColor : 'rgba(0,0,0,1)',
    highlightFill: '#818a91',
    pointborderColor: '#000'
  }];
}
