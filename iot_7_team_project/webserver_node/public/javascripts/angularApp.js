var app = angular.module('smartCart', ['ui.router']);

app.config([
  '$stateProvider',
  '$urlRouterProvider',
  function($stateProvider, $urlRouterProvider) {
    $stateProvider
    .state('home', {
      url: '/home',
      templateUrl: '/home.html',
      controller: 'MainCtrl',
      resolve: {
        orderPromise: ['orders', function(orders){
          return orders.getAll();
        }]
      }
    })
    .state('orders', {
      url: '/orders/{id}',
      templateUrl: '/orders.html',
      controller: 'OrdersCtrl',
      resolve: {
        order: ['$stateParams', 'orders', function($stateParams, orders) {
          return orders.get($stateParams.id);
        }]
      }
    });

  $urlRouterProvider.otherwise('home');
}]);

app.factory('orders', ['$http', function($http){
  var o = {
    orders: []
  };

  o.getAll = function() {
    return $http.get('/orders').success(function(data){
      angular.copy(data, o.orders);
    });
  };
  o.create = function(order) {
    return $http.post('/orders', order).success(function(data){
      o.orders.push(data);
    });
  };

  o.get = function(id) {
  return $http.get('/orders/' + id).then(function(res){
    return res.data;
    });
  };

  o.addProduct = function(id, product) {
    return $http.post('/orders/' + id + '/products', product);
  };


  return o;
}]);

app.controller('MainCtrl', [
  '$scope',
  'orders',
  function($scope, orders){
    $scope.test = 'Hello world!';
    $scope.orders = orders.orders;
    $scope.addPost = function(){
      if(!$scope.time || $scope.time === ''){
        return ;
      }
      orders.create({
        time : $scope.time,
      });
      $scope.time = '';
    };
}]);


app.controller('OrdersCtrl',[
  '$scope',
  'orders',
  'order',
  function($scope, orders, order){
    $scope.order = order;
    $scope.addProduct = function(){
      if($scope.name === '' || $scope.price === '') {return;}
      orders.addProduct(order._id,{
        name : $scope.name,
        price : $scope.price,
      }).success(function(product){
        $scope.order.products.push(product);
      });
      $scope.name = '';
      $scope.price = '';
    };
}]);
