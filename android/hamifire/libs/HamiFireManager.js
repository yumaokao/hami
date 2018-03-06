'use strict';

const google = require('googleapis');

class HamiFireManager {
  constructor(auth) {
    this.service = google.drive('v3');
    this.auth = auth;
  }

  findHamiRootId() {
    return new Promise((resolve, reject) => {
      this.service.files.list({
        auth: this.auth
      }, {
        qs: {
          q: "mimeType='application/vnd.google-apps.folder' and name='hamis'",
          pageSize: 10,
          fields: "nextPageToken, files(id, name)"
        }
      }, (err, response) => {
        if (err) {
          reject(err);
          return;
        }
        var files = response.files;
        if (files.length != 1) {
          reject("Multiple or zero folders named 'hamis'");
        }
        this.hamiRootId = files[0].id
        // for (var i = 0; i < files.length; i++) {
          // var file = files[i];
          // console.log('%s (%s)', file.name, file.id);
        // }
        resolve(this);
      });
    });
  }

  findHamiOrgAllId() {
    return new Promise((resolve, reject) => {
      var qstring = "mimeType='application/vnd.google-apps.folder'";
      qstring += ` and '${this.hamiRootId}' in parents and name='全部'`;
      this.service.files.list({
        auth: this.auth
      }, {
        qs: {
          q: qstring,
          pageSize: 10,
          fields: "nextPageToken, files(id, name)"
        }
      }, (err, response) => {
        if (err) {
          reject(err);
          return;
        }
        var files = response.files;
        if (files.length != 1) {
          reject("Multiple or zero folders named 'hamis/全部'");
        }
        this.hamiOrgAllId = files[0].id
        resolve(this);
      });
    });
  }

  listHamiBooks(parentId, nextPageToken='') {
    var qs = {
      q: `'${parentId}' in parents`,
      pageSize: 10,
      fields: "nextPageToken, files(id, name)"
    };
    if (nextPageToken) {
      qs.pageToken = nextPageToken;
    }

    return new Promise((resolve, reject) => {
      this.service.files.list({
        auth: this.auth
      }, {
        qs: qs
      }, (err, response) => {
        if (err) {
          reject(err);
          return;
        }
        var files = response.files;
        for (var i = 0; i < files.length; i++) {
          var file = files[i];
          console.log('%s (%s)', file.name, file.id);
        }
        // console.log(response.nextPageToken);
        if (response.nextPageToken)
          return this.listHamiBooks(this.hamiOrgAllId, response.nextPageToken);
        resolve(this);
      });
    });
  }

  listAllHamiBooks() {
    return this.listHamiBooks(this.hamiOrgAllId);
  }
}

module.exports = HamiFireManager
