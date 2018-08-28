var express = require('express');
var mongoose = require('mongoose');
var router = express.Router();
var MongoClient = require('mongodb').MongoClient, format = require('util').format;

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
	newEvent.name = req.body;

MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
console.log("Connecting to DB")
    if (err) throw err;
console.log("Connected to Database");
       var document = req.body;

var dbo=db.db("events")
    // insert record
        dbo.collection('events').insert(document, function(err, records) {


        if (err) throw err;
        console.log("Record added as " + records.insertedIds);
	res.json({message:'Event added successfully'});	
	db.close();
    });
});
});



router.get('/news',function(req,res){

        MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
        var dbo=db.db("events")
        console.log("Start");
	

//	dbo.collection('news').find({},{_id:0,update:1},{sort:'-timestamp'}).limit(1,function(err,items){
//	console.log(items)
//	console.log("here")
//	console.log(err)
//	})



        console.log("Start");
	//db.news.find({},{_id:0,update:1}).sort({timestamp:-1}).pretty()
	//dbo.collection('news').find   ({timestamp:{$exists:true}},{_id:0,update:1},{sort:{timestamp:-1}}).limit(2,function(err,items){

	//dbo.collection('news').findOne({timestamp:{$exists:true}}},{update:1,_id:0}).sort({timestamp:-1}),function(err,items) {
	//dbo.collection('news').findOne({timestamp:{$exists:true}},{update:1,_id:0},function(err,items) {
//	 dbo.collection('news').findOne({timestamp:{$exists:true}},{update:1,_id:0},function(err,items) {

        console.log("Done");
        if (err) throw err;
        console.log(items);
        res.json({items});
     });
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
