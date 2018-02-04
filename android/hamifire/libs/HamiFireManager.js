'use strict';

const google = require('googleapis');

class HamiFireManager {
  constructor(auth) {
    this.auth = auth;
  }

  findHamiRoot() {
    return new Promise((resolve, reject) => {
      var service = google.drive('v3');
      service.files.list({
        auth: this.auth,
        q: "mimeType='application/vnd.google-apps.folder' and name='hamis'",
        pageSize: 10,
        fields: "nextPageToken, files(id, name)"
      }, (err, response) => {
        if (err) {
          reject(err);
          return;
        }
        var files = response.files;
        console.log(response);
        for (var i = 0; i < files.length; i++) {
          var file = files[i];
          console.log('%s (%s)', file.name, file.id);
        }
        resolve(this);
      });
    });
  }

  listAllHamiBooks() {
    var service = google.drive('v3');
    service.files.list({
      auth: this.auth,
      pageSize: 10,
      fields: "nextPageToken, files(id, name)"
    }, function(err, response) {
      if (err) {
        console.log('The API returned an error: ' + err);
        return;
    }
      var files = response.files;
      if (files.length == 0) {
        console.log('No files found.');
      } else {
        console.log('Files:');
        for (var i = 0; i < files.length; i++) {
          var file = files[i];
          console.log('%s (%s)', file.name, file.id);
        }
      }
    });
    return this;
  }
}

module.exports = HamiFireManager
