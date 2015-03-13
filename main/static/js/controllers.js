var tweetCodingApp = angular.module('tweetCodingApp', ['ngCookies']);

tweetCodingApp.run(['$anchorScroll', function($anchorScroll) {
  $anchorScroll.yOffset = 60;   // always scroll by 50 extra pixels
}])

tweetCodingApp.run(['$http', '$cookies', function($http, $cookies) {
	$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
	$http.defaults.headers.put['X-CSRFToken'] = $cookies['csrftoken'];
}]);
 
tweetCodingApp.controller('TweetListCtrlA', function($scope, $sce) {

});



tweetCodingApp.controller('TweetListCtrl', 
	['$scope', '$document', '$cookies', '$sce', '$http', '$location', '$anchorScroll', '$q',
	function($scope, $document, $cookies, $sce, $http, $location, $anchorScroll, $q) {

	$scope.codes = [];
	$scope.selected = 0;
	$scope.tweets = [];
	$scope.next = 0;
	$scope.user = null;
	//$scope.csrftoken = $cookies.get('csrftoken');

	$scope.page = angular.element("body").data("page");
	console.log("page: " + $scope.page);

    /*
     *
     * http requests
     *
     */



	var user_promise = $http.get('/api/turkuser/current/.json');
	/*
		.success(function(data){
			$scope.user = data;
		})
		.error(function(data,status,headers,config){
			console.error("error getting user:" + status);
		});
*/

	var codes_promise = $http.get('/api/code/.json');
	/*
		.success(function(data){
			//$scope.codes = data;
			Array.prototype.push.apply($scope.codes, data);
			//$scope.$apply();
		})
		.error(function(data,status,headers,config){
			console.log('error getting codes: ' + status)
		});
	*/


	var tweets_promise = $http.get('/api/tweet/.json');
	/*
		.success(function(data){
			for(var i = 0; i < data.length; i++) {
				data[i].codes = [];
			}

			$scope.tweets = data;
		})
		.error(function(data, status, headers, config){
			console.error("error getting tweets: " + status);
		});
	*/

	var instance_promise = $http.get('/api/codeinstance/.json');

	//var instances_promise = $http.get('/api/code_instance/.json')

	$q.all([user_promise, codes_promise, tweets_promise, instance_promise])
		.then(function(data){
			console.dir(data[0]);
			console.dir(data[1]);
			console.dir(data[2]);
			console.dir(data[3]);

			var tweets = data[2].data;
			var instances = data[3].data;

			for(var i = 0; i < tweets.length; i++) {
				tweets[i].codes = [];
				for(j = 0; j < instances.length; j++) {
					if(instances[j].tweet == tweets[i].id && instances[j].deleted == false) {
						tweets[j].codes.push(instances[j]);
					}
				}
			}


			$scope.user = data[0].data;
			$scope.codes = data[1].data;
			$scope.tweets = tweets;

			//$scope.$apply();
			$scope.$broadcast("data:loaded");

			$scope.schema0_visible = ($scope.page == 0 || $scope.user.condition == 0 || $scope.user.condition == 1);
			$scope.schema1_visible = ($scope.page == 1 || ($scope.user.condition == 0 || $scope.user.condition == 1));

		});



	/*
	 *
	 * translators
	 *
	 */
	$scope.tweetLookupById = function(id) {
		var len = $scope.tweets.length;

		for(var i = 0; i < len; i++ ) {
			if( $scope.tweets[i].id == id ) {
				return $scope.tweets[i];
			}
		}

		return null;
	}

	$scope.tweetLookupByIndex = function(idx) {
		if($scope.tweets.length > idx) {

		}
	}

	$scope.codeLookupById = function(id) {
		var len = $scope.codes.length;

		for(var i = 0; i < len; i++ ) {
			if($scope.codes[i].id == id ) {
				return $scope.codes[i];
			}
		}

		return null;
	}

	$scope.codeLookupByIndex = function(idx) {
		if($scope.codes.length > idx) {
			return $scope.codes[idx];
		}

		return {id: -1, name: "<<invalid>>"}
	}

	$scope.getSelectedTweet = function() {
		if($scope.tweets.length > $scope.selected) {
			return $scope.tweets[$scope.selected];
		}

		return null;
	}



	/*
	 *
	 * filters
	 *
	 */
	$scope.codeFilterBySchema0 = function(code_instance) {
		if(code_instance.code != undefined && $scope.codes.length >= code_instance.code) {
			var code = $scope.codeLookupById(code_instance.code);
			return code.schema === 0;
		}
	}
	$scope.codeFilterBySchema1 = function(code_instance) {
		if(code_instance.code != undefined && $scope.codes.length >= code_instance.code) {
			var code = $scope.codeLookupById(code_instance.code);
			return code.schema === 1;
		}
	}

	$scope.incomplete = function() {
		var count = 0;

		for(var i = 0; i < $scope.tweets.length; i++ ) {
			var tweet = $scope.tweets[i];

			for( var j = 0; j < tweet.codes.length; j++ ) {
				// validate the code
				if(tweet.codes[j].code < 4  ) {
					count++;
					break;
				}
			}
		}

		return count == 20;
	}

	$scope.oneTweet = function() {
		return $scope.user.condition == 1 || $scope.user.condition == 3;
	}


	/*
	 *
	 * actions
	 *
	 */
	$scope.setSelectedTweetIdx = function(idx) {
		if(idx >= 0 && idx < $scope.tweets.length ) {
			$scope.selected = idx;

			$location.hash("tweet-" + idx);
			$anchorScroll();
		}
	}

	$scope.moveNext = function(ev){
		if($scope.selected +1 < $scope.tweets.length) {
			$scope.setSelectedTweetIdx($scope.selected+1);
		}
		if(ev) {
			ev.stopPropagation();
			ev.preventDefault();
		}
	}

	$scope.movePrev = function(ev){
		if($scope.selected > 0) {
			//$scope.tweets[$scope.selected].selected = false;
			//$scope.selected -= 1;
			$scope.setSelectedTweetIdx($scope.selected-1);
			//$scope.tweets[$scope.selected].selected = true;
		}
		if(ev) {
			ev.stopPropagation();
			ev.preventDefault();
		}		
	}


	$scope.addCode = function(idTweet, idCode) {
		var code = $scope.codeLookupById(idCode),
			tweet = $scope.tweetLookupById(idTweet),
			temp_id = Math.floor(Math.random() * 99999);

		if(tweet) {
			tweet.codes.push({
				code: idCode,
				date: Date.now(),
				temp_id: temp_id
			});

			$http.post("/api/codeinstance/", {
				"deleted": false,
				"code": idCode,
				"tweet": idTweet,
				"assignment": $scope.user.id
			})
			.success(function(data){
				for(var i = 0; i < tweet.codes.length; i++) {
					if(tweet.codes[i].temp_id == temp_id) {
						//tweet.codes[i].deleted = data.deleted;
						tweet.codes[i].date = data.date;
						tweet.codes[i].id = data.id;
					}
				}
			})
			.error(function(data, status, headers, config){
				console.error("error adding code (" + temp_id + ") : " + status);
			});
		}
	}

	$scope.removeCode = function(idTweet, idCode) {
		var tweet = $scope.tweetLookupById(idTweet);

		if(tweet != null && tweet.codes ) {
			for(var i = 0; i < tweet.codes.length; i++) {
				if( tweet.codes[i].code == idCode ) {
					code = tweet.codes.splice(i,1)[0];

					if(code.id && code.id >= 0) {
						code.deleted = true;
						delete code.temp_id;
						code.tweet = idTweet;
						code.assignment = $scope.user.id;
						$http.put("/api/codeinstance/" + code.id + "/", code)
							.success(function(data) {
								console.log("deleted code: " + code.id);
							})
							.error(function(data,status,headers,config){
								console.error("error deleting code :" + status );
							})
					}

					return true;
				}
			}
		} else {
			console.error('tweet is null');
		}

		return false
	}


	$scope.toggleCode = function(tweet, idCode) {
		if(tweet != null) {
			if(!$scope.removeCode(tweet.id, idCode)) {
				$scope.addCode(tweet.id, idCode);
			}
		}
	}

	$scope.toggleCodeByTweetId = function(idTweet, idCode) {
		var tweet = $scope.tweetLookupById(idTweet);

		$scope.toggleCode(tweet, idCode);
	}

	$scope.toggleCodeOnSelectedTweet = function(idCode) {
		var tweet = $scope.getSelectedTweet();

		$scope.toggleCode(tweet, idCode);
	}

	/*
	 *
	 * event handlers
	 *
	 */
	$scope.itemClicked = function($index) {
		//console.log('+' + $index);
		$scope.selected = $index;
		//$scope.setSelectedTweetIdx($index);
	}


	$scope.onKeyPress = function(ev) {
		console.dir(ev);
		console.log("keycode: " + ev.keyCode);
		var handled = false;
		//console.log("-selected: " + $scope.selected);		switch(ev.keyCode) {


		if($scope.schema0_visible && ev.keyCode >= 49 && ev.keyCode <= 51) {
			$scope.toggleCodeOnSelectedTweet( ev.keyCode - 48 );
			handled = true;
		}else if($scope.schema1_visible && ev.keyCode >= 52 && ev.keyCode < 55) {
			$scope.toggleCodeOnSelectedTweet( ev.keyCode - 48 );
			handled = true;
		} else {
			switch(ev.keyCode) {
				case 38:
					$scope.movePrev();
					handled = true;
					break;
				case 40:
				case 13:
					$scope.moveNext();
					handled = true;
					break;
			}
		}

		
		//$scope.apply($scope.selected);
		//$scope.$apply();

		if(handled) {
			$scope.$apply();
			return false;
		}

	}

	$scope.onRemoveCodeClicked = function(ev, tweet, code) { 
		console.dir(code);
		ev.preventDefault();
		ev.stopPropagation();

		$scope.removeCode(tweet.id, code.code )

		return false;
	}



	// add global keybinding
	angular.element(window).on('keydown', $scope.onKeyPress);
	//$document.bind("keypress", $scope.onKeyPress);
	/*
	$scope.$on('keypress', function(onEvent, onKeyPress){ 
		console.log("%%");
		console.dir(onEvent);
	});
*/



}]);


tweetCodingApp.controller('TweetCodeNavBar', ['$scope', 
function($scope) {
	//$scope.

	$scope.$on('data:loaded', function(event, args) {
		console.log('data:loaded');
		console.dir(event);
		console.dir(args);
	});
}]);