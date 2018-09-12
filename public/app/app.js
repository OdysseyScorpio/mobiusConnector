var app = angular.module('myApp',['ngResource']);

app.factory('Event',function($resource){
	return $resource('/api/eventsOOM')
});

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
	}).then (function(response){$scope.eventsOOM = response.data
	},function (error){
	});
	
});