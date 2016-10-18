var mongoose = require('mongoose');

var ProSchema = new mongoose.Schema({
  name : String,
  price : String,

  order : { type: mongoose.Schema.Types.ObjectId, ref : 'Order'}
});

mongoose.model('Product', ProSchema);
