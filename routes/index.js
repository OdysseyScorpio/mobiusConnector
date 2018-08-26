var express = require('express');
var mongoose = require('mongoose');
var router = express.Router();

//model
//=============================================================================
var Event = require('../models/events');

router.use(function(req,res,next){
	console.log('Something is happenning');
	next();//make sure we go to the next routes and dont stop there
});

router.get('/',function(req,res){
	res.json({ message:'welcome to routing rest api'});
});

router.post('/events',function(req,res){
	var newEvent = new Event();//create a new instance of the event model
	newEvent.name = req.body.name;
	
    //save the event and check for error
	newEvent.save(function(err){
		if(err)
			res.send(err);
		
		res.json({message:'Event added successfully'});
		console.log(req.body.name);
	});
	
});

router.get('/events',function(req,res){
	Event.find(function(err,events){
		if(err)
			res.send(err);
		
		res.json(events);
	});
});

router.get('/events/:id',function(req,res){
	Event.findById(req.params.id,function(err,event){
		if(err)
			res.send(err);
		
		res.json(event);
	});
});

router.put('/events/:id',function(req,res){
	Event.findById(req.params.id,function(err,event){
		if(err)
			res.send(err);
		
		event.name = req.body.name;//update the event name
		
		//save the event after change
		event.save(function(err){
			if(err)
				res.send(err);
			
			res.json(event);
		});
	});
});

router.delete('/events/:id',function(req,res){
	Event.remove({'_id':req.params.id},function(err){
		if(err)
			res.end(err);
		
		res.json({ message:'Event Successfully Deleted' });
	});
});

module.exports = router;