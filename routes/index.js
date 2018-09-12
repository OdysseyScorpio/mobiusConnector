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
})





router.get('/eventsOOM',function(req,res){

    MongoClient.connect('mongodb://127.0.0.1/events', function(err,db) {
        var dbo=db.db("events")
        Promise.all([
        dbo.collection('events').find({event:"MissionCompleted","Faction" : "The Order of Mobius"},
        {systemname:1,stationname:1,Commodity:1,Commodity_Localised:1,Count:1,DestinationStation:1,DestinationSystem:1,Donation:1,LocalisedName:1,PassengerCount:1,
        PassengerVIPs:1,PassengerWanted:1,PassenterType:1,Reward:1,Influence:1,commandername:1,MissionID:1,timestamp:1,Wing:1,Mobiusappversion :1,_id:0}).toArray(),
        dbo.collection('events').find({event:"MissionAccepted"},
        {systemname:1,stationname:1,Commodity:1,Commodity_Localised:1,Count:1,DestinationStation:1,DestinationSystem:1,Donation:1,LocalisedName:1,PassengerCount:1,
        PassengerVIPs:1,PassengerWanted:1,PassenterType:1,Reward:1,Influence:1,commandername:1,MissionID:1,timestamp:1,Wing:1,Mobiusappversion :1,_id:0}).toArray()
        ]).then( ([completed,accepted ]) => {


                for ( var c = 0 ; c < completed.length; c++) {
                        for (var a = 0 ; a < accepted.length; a++) {
                                if(completed[c]["MissionID"] == accepted[a]["MissionID"]){


completed[c]['OriginalSystem'] = accepted[a]['systemname']
completed[c]['OriginalStation'] = accepted[a]['stationname']
completed[c]['Commodity'] = accepted[a]['Commodity']
completed[c]['Commodity_Localised'] = accepted[a]['Commodity_Localised']
completed[c]['Count'] = accepted[a]['Count']
completed[c]['DestinationStation'] = accepted[a]['DestinationStation']
completed[c]['DestinationSystem'] = accepted[a]['DestinationSystem']
completed[c]['Donation'] = completed[c]['Donation']
completed[c]['LocalisedName'] = accepted[a]['LocalisedName']
completed[c]['PassengerCount'] = accepted[a]['PassengerCount']
completed[c]['PassengerVIPs'] = accepted[a]['PassengerVIPs']
completed[c]['PassengerWanted'] = accepted[a]['PassengerWanted']
completed[c]['PassenterType'] = accepted[a]['PassenterType']
completed[c]['Reward'] = completed[c]['Reward']
completed[c]['Influence'] = accepted[a]['Influence']
completed[c]['commandername'] = accepted[a]['commandername']
completed[c]['MissionID'] = accepted[a]['MissionID']
completed[c]['StartTimestamp'] = accepted[a]['timestamp']
completed[c]['EndTimestamp'] = completed[c]['timestamp']
completed[c]['Wing'] = accepted[a]['Wing']
completed[c]['Mobiusappversion'] = completed[c]['Mobiusappversion']


if(completed[c]['systemname']!==undefined){completed[c]['OriginalSystem'] = accepted[a]['systemname']}else{completed[c]['systemname']=''}
if(completed[c]['stationname']!==undefined){completed[c]['OriginalStation'] = accepted[a]['stationname']}else{completed[c]['stationname']=''}
if(completed[c]['Commodity']!==undefined){completed[c]['Commodity'] = accepted[a]['Commodity']}else{completed[c]['Commodity']=''}
if(completed[c]['Commodity_Localised']!==undefined){completed[c]['Commodity_Localised'] = accepted[a]['Commodity_Localised']}else{completed[c]['Commodity_Localised']=''}
if(completed[c]['Count']!==undefined){completed[c]['Count'] = accepted[a]['Count']}else{completed[c]['Count']=''}
if(completed[c]['DestinationStation']!==undefined){completed[c]['DestinationStation'] = accepted[a]['DestinationStation']}else{completed[c]['DestinationStation']=''}
if(completed[c]['DestinationSystem']!==undefined){completed[c]['DestinationSystem'] = accepted[a]['DestinationSystem']}else{completed[c]['DestinationSystem']=''}
if(completed[c]['Donation']!==undefined){completed[c]['Donation'] = completed[c]['Donation']}else{completed[c]['Donation']=''}
if(completed[c]['LocalisedName']!==undefined){completed[c]['LocalisedName'] = accepted[a]['LocalisedName']}else{completed[c]['LocalisedName']=''}
if(completed[c]['PassengerCount']!==undefined){completed[c]['PassengerCount'] = accepted[a]['PassengerCount']}else{completed[c]['PassengerCount']=''}
if(completed[c]['PassengerVIPs']!==undefined){completed[c]['PassengerVIPs'] = accepted[a]['PassengerVIPs']}else{completed[c]['PassengerVIPs']=''}
if(completed[c]['PassengerWanted']!==undefined){completed[c]['PassengerWanted'] = accepted[a]['PassengerWanted']}else{completed[c]['PassengerWanted']=''}
if(completed[c]['PassenterType']!==undefined){completed[c]['PassenterType'] = accepted[a]['PassenterType']}else{completed[c]['PassenterType']=''}
if(completed[c]['Reward']!==undefined){completed[c]['Reward'] = completed[c]['Reward']}else{completed[c]['Reward']=''}
if(completed[c]['Influence']!==undefined){completed[c]['Influence'] = accepted[a]['Influence']}else{completed[c]['Influence']=''}
if(completed[c]['commandername']!==undefined){completed[c]['commandername'] = accepted[a]['commandername']}else{completed[c]['commandername']=''}
if(completed[c]['MissionID']!==undefined){completed[c]['MissionID'] = accepted[a]['MissionID']}else{completed[c]['MissionID']=''}
if(completed[c]['timestamp']!==undefined){completed[c]['StartTimestamp'] = accepted[a]['timestamp']}else{completed[c]['timestamp']=''}
if(completed[c]['timestamp']!==undefined){completed[c]['EndTimestamp'] = completed[c]['timestamp']}else{completed[c]['timestamp']=''}
if(completed[c]['Wing']!==undefined){completed[c]['Wing'] = accepted[a]['Wing']}else{completed[c]['Wing']=''}
if(completed[c]['Mobiusappversion']!==undefined){completed[c]['Mobiusappversion'] = completed[c]['Mobiusappversion']}else{completed[c]['Mobiusappversion']=''}



					

                               }

                        }
                }
                res.json(completed)
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

router.get('/load.py',function(req,res){
        var path = require('path');
        console.log(__dirname)
        res.sendFile(path.resolve('./Mobius/load.py'));
});


module.exports = router
