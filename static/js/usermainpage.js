
'use strict';

function userTrackedInfo(results) {
  console.log(results);
  $('#user_tracking').html(results);
}

function getUserData() {
  $.get('/tracked-info.json', userTrackedInfo);
}

// getUserData();
