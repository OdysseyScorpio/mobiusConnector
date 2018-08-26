var mongoose = require('mongoose');
var Schema = mongoose.Schema({
	name:String
},
{strict: false});

module.exports = mongoose.model('event',Schema);