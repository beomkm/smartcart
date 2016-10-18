var mongoose = require('mongoose');

var OrderSchema = new mongoose.Schema({
  time : String,
  products : [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product'}]
});

mongoose.model('Order', OrderSchema);
