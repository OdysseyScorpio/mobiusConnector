var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var logger = require('morgan');


//var app = express();

var express = require('express')
  , http = require('http')
  , app = express()
  , server = http.createServer(app)


var routes = require('./routes/index');

//Connecting database
//=============================================================================
var configDB = require('./db');
mongoose.connect(configDB.url);


app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended:true }));

app.use(express.static(__dirname+'/public'));


var port = process.env.PORT || 3000 ;

//ROUTES FOR OUR API
//=============================================================================
var router = express.Router();

// test route to make sure everything is working (accessed at GET http://localhost:3000/api)
router.get('/',function(req,res){
	res.json({
		message:'hurray! welcome to rest api app'
	});
});
app.use('/', router);

app.use('/api',routes);

//catch 404 and forward to error handler
app.use(function(req, res, next) {
    res.end('Page Not Found!');
});

//START THE SERVER
//=============================================================================
//app.listen(port,'192.186.1.125');


server.listen(3000,'vps583405.ovh.net',function(){
 server.close(function(){
   server.listen(3000,'54.38.214.40')
 })
})



console.log('app listening at '+port);
