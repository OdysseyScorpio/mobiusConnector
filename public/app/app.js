var app = angular.module('myApp',['ngResource']);

app.factory('Event',function($resource){
	return $resource('/api/eventsOOM')
});

app.controller('eventController',function($scope,$http){
	$http({
	method:'GET',
	url: 'api/eventsOOM'
	}).then (function(response){$scope.eventsOOM = response.data
	},function (error){
	});
	
});
