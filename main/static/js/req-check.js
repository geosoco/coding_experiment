window.RequirementCheck = (function(){

	var module = {};


	//
	// let twitter start loading
	//
	window.twttr = (function(d, s, id) {
	  var js, fjs = d.getElementsByTagName(s)[0],
	    t = window.twttr || {};
	  if (d.getElementById(id)) return t;
	  js = d.createElement(s);
	  js.id = id;
	  js.src = "https://platform.twitter.com/widgets.js";
	  fjs.parentNode.insertBefore(js, fjs);
	 
	  t._e = [];
	  t.ready = function(f) {
	    t._e.push(f);
	  };
	 
	  return t;
	}(document, "script", "twitter-wjs"));	


	var _reqCheck = function(onSuccess, onCookiesFailed, onTwitterFailed, onTwitterCheckUpdate) {
		this.onSuccess = onSuccess;
		this.onCookiesFailed = onCookiesFailed;
		this.onTwitterFailed = onTwitterFailed;
		this.onTwitterCheckUpdate = onTwitterCheckUpdate;


		this.cookieEnabled = null;
		this.twitterEnabled = null;
		this.twitterChecking = true;


		this.start_twitter_check();

		if(this.are_cookies_enabled() === false) {
			if(this.onCookiesFailed) {
				this.onCookiesFailed(this);
			}
		}

		this.check_all();

	};


	/*
	 * This code is taken from here: http://www.sveinbjorn.org/cookiecheck
	 *
	 * returns true if cookes are enabled. Also sets property on class
	 *
	 */
	_reqCheck.prototype.are_cookies_enabled = function()
	{
		var cookieEnabled = (navigator.cookieEnabled) ? true : false;

		if (typeof navigator.cookieEnabled == "undefined" && !cookieEnabled)
		{ 
			document.cookie="testcookie";
			cookieEnabled = (document.cookie.indexOf("testcookie") != -1) ? true : false;
		}

		this.cookieEnabled = cookieEnabled;

		return (cookieEnabled);
	}


	/*
	 * twitter_enabled
	 *
	 *	returns true if the script has loaded and initialized
	 */
	_reqCheck.prototype.twitter_enabled = function()
	{

		var enabled = (typeof(twttr.init) !== "undefined" && twttr.init == true );
		if(this.twitterChecking === false) {
			this.twitterEnabled = enabled;
		}
		return enabled;
	}


	_reqCheck.prototype.notifyTwitterCheckUpdate = function(num_checks_left) {

		if(this.onTwitterCheckUpdate) {
			this.onTwitterCheckUpdate(this, num_checks_left)
		}

	}

	/*
	 * start_twitter_check
	 *
	 * Waits for 10 seconds to check if twitter has loaded. 
	 * Checks every second until it times out.
	 */
	_reqCheck.prototype.start_twitter_check = function() {

		var self = this, 
			num_checks_left = 10,
			check_fn = function() {
				if(num_checks_left > 0) {
					if(self.twitter_enabled() === false) {
						self.notifyTwitterCheckUpdate(num_checks_left);
						setTimeout(check_fn, 1000);
						num_checks_left--;
					} else {
						self.twitterChecking = false;
						self.check_all();
						self.notifyTwitterCheckUpdate(num_checks_left);
					}
				} else {
					// we're no longer checking
					self.twitterChecking = false;

					// these are the final results so do the callback
					if(self.twitter_enabled() === false) {

						if(self.onTwitterFailed) {
							self.onTwitterFailed(self);
						}
					} else {
						self.check_all();
						self.notifyTwitterCheckUpdate(num_checks_left);
					}
				}
			}


		check_fn();
	}	

	/*
	 *
	 *
	 *
	 *
	 */
	 _reqCheck.prototype.check_all = function(onSuccess) {
		if(this.twitter_enabled() === true  && this.are_cookies_enabled() === true ) {
			if(this.onSuccess) {
				this.onSuccess(this);
			}
		}
	}




	module.ReqCheck = _reqCheck;

	return module;

})();

