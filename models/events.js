var mongoose = require('mongoose');
var Schema = mongoose.Schema({

},
{strict: false});

module.exports = mongoose.model('event',Schema);
