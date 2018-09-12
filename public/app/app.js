var app = angular.module('myApp',['ngResource']);

var EventsOOM = function($resource){
	return $resource('/api/eventsOOM')
};
var EventsMCRN = function($resource){
        return $resource('/api/eventsMCRN')
};

app.controller('eventOOMController',function($scope,$http){
	$http({
	method:'GET',
	url: 'api/eventsOOM'
	}).then (function(response){$scope.eventsOOM = response.data
	},function (error){
	});
	
});
app.controller('eventMCRNController',function($scope,$http){
	$http({
	method:'GET',
	url: 'api/eventsMCRN'
	}).then (function(response){$scope.eventsMCRN = response.data
	},function (error){
	});
	
});
