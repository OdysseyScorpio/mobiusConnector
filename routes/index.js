var express = require('express');
var mongoose = require('mongoose');
var router = express.Router();
var MongoClient = require('mongodb').MongoClient, format = require('util').format;

//model
//=============================================================================
var Event = require('../models/events');

router.use(function(req,res,next){
	next();//make sure we go to the next routes and dont stop there
});

router.get('/',function(req,res){
	res.json({ message:'welcome to routing rest api'});
});

router.post('/events',function(req,res){
	var newEvent = new Event();//create a new instance of the event model
	newEvent.name = req.body;
	MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
    if (err) throw err;

		var document = req.body;
		var dbo=db.db("events")
	    // insert record
        dbo.collection('events').insert(document, function(err, records) {
	        if (err) throw err;
			res.json({message:'Event added successfully'});	
			db.close();
	    });
	});
});

router.get('/news',function(req,res){

    MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
    	var dbo=db.db("events")
    	dbo.collection('news').find({timestamp:{$exists:true}},{update:1,_id:0}).toArray(function(err,items) {
			if (err) throw err;
			update =items[items.length-1]
    		res.json({update});
		});
	});
});

router.get('/version',function(req,res){

    MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
    	var dbo=db.db("version")
    	dbo.collection('version').findOne({timestamp:{$exists:true}},{version:1,_id:0},function(err,items) {
			if (err) throw err;
			version =items[0].version
    		res.json({version});
		});
	});
});


module.exports = router;
