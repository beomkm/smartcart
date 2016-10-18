var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});


var mongoose = require('mongoose');
var Order = mongoose.model('Order');
var Product = mongoose.model('Product');

router.get('/orders', function(req, res, next) {
  Order.find(function(err, orders){
    if(err){ return next(err); }

    res.json(orders);
  });
});

router.post('/orders', function(req, res, next) {
  var order = new Order(req.body);

  order.save(function(err, order){
    if(err){ return next(err); }

    res.json(order);
  });
});

router.param('order', function(req, res, next, id) {
  var query = Order.findById(id);

  query.exec(function (err, order){
    if (err) { return next(err); }
    if (!order) { return next(new Error("can't find post")); }

    req.order = order;
    return next();
  });
});

router.param('product', function(req, res, next, id) {
  var query = Product.findById(id);

  query.exec(function (err, product){
    if (err) { return next(err); }
    if (!product) { return next(new Error("can't find comment")); }

    req.product = product;
    return next();
  });
});


router.get('/orders/:order', function(req, res, next) {
  req.order.populate('products', function(err, order) {
    if (err) { return next(err); }
    res.json(order);
  });
});



router.post('/orders/:order/products', function(req, res, next) {
  var product = new Product(req.body);
  product.order = req.order;

  product.save(function(err, product){
    if(err){ return next(err); }

    req.order.products.push(product);
    req.order.save(function(err, order) {
      if(err){ return next(err); }

      res.json(product);
    });
  });
});

router.delete('/orders/:id', function(req, res, next){
  Order.remove({ _id: req.params.id }, function(err, order){
    if(err){ return next(err); }

    res.json(order);
  });
});

module.exports = router;
