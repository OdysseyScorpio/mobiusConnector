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
    	dbo.collection('news').find({timestamp:{$exists:true}},{update:1,link:1,motd:1,versionmsg:1,_id:0}).toArray(function(err,items) {
			if (err) throw err;
			update =items[items.length-1]
    		res.json({update});
		});
	});
});

router.get('/version',function(req,res){
 	
    MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
    	var dbo=db.db("events")
    	dbo.collection('pluginversion').find({}).sort({timestamp:-1}).toArray(function(err,items) {
			console.log(err)
			console.log(items)
			console.log(items.version)

			if (err) throw err;
			version =items[0].version
    		res.json({version});
		});
	});
});


router.get('/listening',function(req,res){

    MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
        var dbo=db.db("events")
        dbo.collection('listening').find({},{_id:0,timestamp:0}).toArray(function(err,items) {
                        console.log(err)
                        console.log(items)
                       
                        if (err) throw err;
                        
                res.json({items});
                });
        });
});


router.get('/download',function(req,res){
	var path = require('path');
	console.log(__dirname)
	res.sendFile(path.resolve('./Mobius/load.py'));
});


module.exports = router;
