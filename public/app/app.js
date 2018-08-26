var app = angular.module('myApp',['ngResource']);

app.factory('Event',function($resource){
	return $resource('/api/events/:id',{ id:'@_id' },{
		update:{ method:'PUT'}
	});
});

app.controller('eventController',function($scope,Event){
	
	$scope.event = new Event();
	var refresh = function(){
		$scope.events = Event.query();
		$scope.event = "";
	}
	refresh();
	
	$scope.remove = function(event){
		event.$delete(function(){
			refresh();
		});
	}
	
	$scope.add = function(event){
		Event.save(event,function(event){
			refresh();
		});
	}
	
	$scope.edit = function(id){
		$scope.event = Event.get({id:id});
	}
	
	$scope.update = function(event){
		event.$update(function(){
			refresh();
		});
	}
});