var tweetServices = angular.module('tweetServices', ['ngResource']);

tweetServices.factory('Tweet', ['$resource',
  function($resource){
    return $resource('/api/tweet/:tweetId.json', {}, {
      query: {method:'GET', params:{tweetId:'tweets'}, isArray:true}
    });
  }]);